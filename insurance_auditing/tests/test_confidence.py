import copy
import unittest
from insurance_audit.confidence import choose


class ConfidenceTests(unittest.TestCase):
    def setUp(self):
        self.policy={'version':'1','minimum_empirical_n':30,'h1_groups':{'explicit:0':{'n':100,'confidence':.95},'elided:1':{'n':3,'confidence':.65}},
                     'target_judgment':{'explicit':.8,'elided':.7},'outcome_invariant_cap':.65}
        self.row={'hospital':'H1','mapping_evidence':'explicit','flagged':0,'expected_total_cents':100}

    def test_supported_sparse_novel_and_unresolved_are_distinct(self):
        self.assertEqual(choose(self.row,self.policy),(.95,'h1_supported:explicit:0'))
        r=dict(self.row,mapping_evidence='elided',flagged=1)
        self.assertEqual(choose(r,self.policy),(.65,'sparse:elided:1'))
        self.assertEqual(choose(dict(self.row,hospital='H5'),self.policy),(.8,'novel_reviewed:explicit'))
        self.assertEqual(choose(dict(self.row,unresolved=True),self.policy),(None,'unresolved'))
        self.assertEqual(choose(dict(self.row,outcome_invariant_uncertainty=True),self.policy)[0],.65)

    def test_nonfinite_or_invalid_confidence_fails(self):
        for x in [float('nan'),float('inf'),-1,1.1,True]:
            p=copy.deepcopy(self.policy);p['h1_groups']['explicit:0']['confidence']=x
            with self.assertRaises(ValueError):choose(self.row,p)
