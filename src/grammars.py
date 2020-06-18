# -----------------------------------------------------------
# Define some grammars and functions to deal with them
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Grammar import Grammar

# Define each grammar type
####

"""
* To be extended to create certain grammar types *
For now just returns one grammar for testing
"""
def create_grammar(g_type):
    grammar = Grammar(start='BOOL')

    # Rules ending in nonterminals
    grammar.add_rule('BOOL', 'issubset_', ['SET', 'SET'], 1.0)
    grammar.add_rule('BOOL', 'issuper_', ['SET', 'SET'], 1.0)
    grammar.add_rule('BOOL', 'equal_', ['SET', 'SET'], 1.0)
    grammar.add_rule('BOOL', 'lt', ['NUM', 'NUM'], 1.0)
    grammar.add_rule('BOOL', 'gt', ['NUM', 'NUM'], 1.0)
    grammar.add_rule('BOOL', 'num_eq', ['NUM', 'NUM'], 1.0)

    grammar.add_rule('NUM', 'cardinality_', ['SET'], 1.0)

    grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 1.0)
    grammar.add_rule('SET', 'union_', ['SET', 'SET'], 1.0)
    grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 1.0)


    # Rules ending in terminals
    grammar.add_rule('SET', 'A', None, 1.0)
    grammar.add_rule('SET', 'B', None, 1.0)
    for n in range(0,10):
        grammar.add_rule('NUM', str(n), None, 1.0)

    return grammar