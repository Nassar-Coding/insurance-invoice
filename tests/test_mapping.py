"""The four-state matcher: what it decides, and what it refuses to look at."""
import json
import unittest
from dataclasses import replace
from pathlib import Path

from insurance_audit.audit import audit
from insurance_audit.io import load_hospital
from insurance_audit.mapping import (CANDIDATE_FLOOR, MIN_MARGIN, MIN_SCORE, NO_MATCH_FLOOR, classify,
                                     coverage, names_no_contracted_service, one_edit_apart, rank, score, tokens)
from insurance_audit.schema import load_bundle

ROOT = Path(__file__).resolve().parents[1]
CONTRACT, MAPS, _ = load_bundle(ROOT, 'H1')
SERVICES = CONTRACT['services']
LEXICON = MAPS['lexicon']


def state(description):
    return classify(description, SERVICES, LEXICON)


class TokenisationTests(unittest.TestCase):
    def test_a_service_code_suffix_is_not_part_of_the_wording(self):
        self.assertEqual(tokens('Case - Intensive Ophth /NG-3641'), ['case', 'intensive', 'ophth'])

    def test_case_and_punctuation_do_not_change_the_tokens(self):
        self.assertEqual(tokens('ADVANCED  Neurological - Consultation'), tokens('advanced neurological consultation'))

    def test_one_edit_apart_only_applies_to_long_words(self):
        self.assertTrue(one_edit_apart('neurological', 'neurolgical'))
        self.assertTrue(one_edit_apart('cardiac', 'cardiab'))
        self.assertFalse(one_edit_apart('renal', 'penal'))
        self.assertFalse(one_edit_apart('care', 'cart'))


class FourStateTests(unittest.TestCase):
    def test_an_exact_contracted_name_matches(self):
        result = state('Advanced Neurological Consultation')
        self.assertEqual((result['state'], result['service_id']), ('MATCH', 'H1-S006'))
        self.assertEqual(result['best_score'], 1.0)

    def test_an_abbreviation_and_a_reordering_still_match(self):
        for description in ('Consultation Adv', 'Adv Neuro Consult'):
            with self.subTest(description=description):
                self.assertEqual(state(description)['service_id'], 'H1-S006')

    def test_a_typo_in_a_long_word_still_matches(self):
        self.assertEqual(state('Advanced Neurolgical Consultation')['service_id'], 'H1-S006')

    def test_a_word_no_contracted_service_explains_is_a_no_match(self):
        for description in ('Adv Renal Consultation', 'Occ Advanced Orthopaedic Recovery Rm'):
            with self.subTest(description=description):
                result = state(description)
                self.assertEqual(result['state'], 'NO_MATCH')
                self.assertEqual(result['service_id'], None)
                self.assertLess(result['best_explained_share'], NO_MATCH_FLOOR)

    def test_names_no_contracted_service_reports_the_closest_service(self):
        unknown, evidence = names_no_contracted_service('Adv Renal Consultation', SERVICES, LEXICON)
        self.assertTrue(unknown)
        self.assertEqual(evidence['no_match_floor'], NO_MATCH_FLOOR)
        self.assertIsNotNone(evidence['closest_service_id'])
        self.assertFalse(names_no_contracted_service('Consultation Adv', SERVICES, LEXICON)[0])

    def test_equally_good_candidates_are_a_tie_not_a_guess(self):
        # "Visit Amb Hm" scores identically against the ambulatory home visit and
        # the ambulatory visit: the wording does not choose between them.
        result = state('Visit Amb Hm')
        self.assertEqual(result['state'], 'TIE')
        self.assertIsNone(result['service_id'])
        self.assertEqual(result['candidates'], ['H1-S008', 'H1-S011'])
        self.assertLess(result['margin'], MIN_MARGIN)

    def test_a_weak_reading_offers_candidates_and_commits_to_none(self):
        result = classify('Consultation', SERVICES, LEXICON, min_score=0.99)
        self.assertEqual(result['state'], 'WEAK')
        self.assertIsNone(result['service_id'])
        self.assertTrue(all(value >= CANDIDATE_FLOOR for value, ident in rank('Consultation', SERVICES, LEXICON)
                            if ident in result['candidates']))

    def test_the_plan_thresholds_are_the_declared_starting_points(self):
        self.assertEqual((MIN_SCORE, MIN_MARGIN), (0.60, 0.08))

    def test_score_never_exceeds_one_and_repeats_do_not_inflate_it(self):
        self.assertLessEqual(score(tokens('care care care'), tokens('Advanced Cardiac Recovery Room Occupancy'),
                                   LEXICON), 1.0)
        self.assertEqual(coverage(tokens('care care care'), tokens('Wound Care'), LEXICON), 1 / 3)


class PriceIsNeverEvidenceTests(unittest.TestCase):
    """Perturbing any money or quantity field must not move a single mapping."""

    def test_no_money_field_appears_in_the_matcher_code(self):
        import ast
        tree = ast.parse((ROOT / 'src/insurance_audit/mapping.py').read_text())
        for node in ast.walk(tree):
            # Prose may name the fields; executable code may not touch them.
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                continue
            for field in ('unit_price_cents', 'line_total_cents', 'invoice_total_cents', 'quantity_cents'):
                if isinstance(node, ast.Attribute):
                    self.assertNotEqual(node.attr, field, f'{field} must never reach the matcher')
                if isinstance(node, ast.Name):
                    self.assertNotEqual(node.id, field, f'{field} must never reach the matcher')
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    self.assertNotEqual(node.value, field, f'{field} must never reach the matcher')

    def test_perturbing_prices_and_quantities_changes_no_mapping(self):
        data = load_hospital(ROOT / 'data/source', 'H1')
        before = audit(data, CONTRACT, MAPS)
        mapped = lambda run: [(t['invoice_id'], l['line_id'], l['service_id'], l['mapping_grade'])
                              for t in run['traces'] for l in t['lines']]
        original = mapped(before)
        self.assertTrue(original)
        data.lines = [replace(row, unit_price_cents=row.unit_price_cents * 3 + 7,
                              line_total_cents=row.line_total_cents * 5 + 11) for row in data.lines]
        data.invoices = [replace(row, invoice_total_cents=row.invoice_total_cents * 2 + 13)
                         for row in data.invoices]
        self.assertEqual(mapped(audit(data, CONTRACT, MAPS)), original)

    def test_the_unknown_service_finding_ignores_price_entirely(self):
        for price in (0, 1, 10 ** 9):
            with self.subTest(price=price):
                self.assertTrue(names_no_contracted_service('Adv Renal Consultation', SERVICES, LEXICON)[0])


if __name__ == '__main__':
    unittest.main()
