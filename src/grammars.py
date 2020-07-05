# -----------------------------------------------------------
# Define some grammars and functions to deal with them
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Grammar import Grammar


def create_grammar(g_type):

    if g_type == "quant":
        grammar = Grammar(start='BOOL')

        grammar.add_rule('BOOL', 'issubset_', ['SET', 'SET'], 1.0/6.0)
        grammar.add_rule('BOOL', 'issuper_', ['SET', 'SET'], 1.0/6.0)
        grammar.add_rule('BOOL', 'equal_', ['SET', 'SET'], 1.0/6.0)
        grammar.add_rule('BOOL', 'lt', ['NUM', 'NUM'], 1.0/6.0)
        grammar.add_rule('BOOL', 'gt', ['NUM', 'NUM'], 1.0/6.0)
        grammar.add_rule('BOOL', 'num_eq', ['NUM', 'NUM'], 1.0/6.0)

        grammar.add_rule('NUM', 'cardinality_', ['SET'], 1.0/12.0)
        for n in range(0,10):
            grammar.add_rule('NUM', str(n), None, 1.0/12.0)

        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 1.0/5.0)
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], 1.0/5.0)
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 1.0/5.0)
        grammar.add_rule('SET', 'A', None, 1.0/5.0)
        grammar.add_rule('SET', 'B', None, 1.0/5.0)
        
        return grammar

    else:
        raise Exception("There exists no g_type \'" + g_type + '\'. To see possible grammar types, refer to grammars.py.')