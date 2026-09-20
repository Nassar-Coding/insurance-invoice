"""Candidate-review aid; replay reads reviewed data, not this acquisition code."""
from prepare_inventory import words,LEXICON

# Omitting these final generic nouns retains the preceding substantive service
# head. Qualifiers and all other service words remain required.
OMIT_FINAL={'occupancy','administration','programme','session','service','procedure',
            'support','panel','visit','dispensing','observation','conference','fraction'}


def matched(required,options):
    required=sorted(required,key=lambda w:sum(w in o for o in options))
    def visit(i,used):
        if i==len(required):return True
        return any(visit(i+1,used|{j}) for j,o in enumerate(options) if j not in used and required[i] in o)
    return visit(0,set())


def evidence_grade(description,name):
    required=words(name);options=[set(LEXICON.get(w,[w])) for w in words(description)]
    if matched(required,options):return 'explicit'
    if len(required)>=4 and required[-1] in OMIT_FINAL and matched(required[:-1],options):return 'elided'
    return 'unresolved'
