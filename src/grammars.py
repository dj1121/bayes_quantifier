# -----------------------------------------------------------
# Allows definition of grammars and provides functions to deal with them
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Grammar import Grammar


def create_grammar(g_type):

    """
    Creates a grammar of a specified type and allows definition of grammar rules with their
    probabilities.

    Parameters:
        - g_type (str): Grammar type specified on command line. If you wish to create a new
        grammar type, add a new type in the "if" clause and define it below.

    Returns:
    - grammar (LOTLib3.Grammar): Grammar of specified type
    - None: If the specified grammar type does not exist (you must create).
    """

    if g_type == "quant":
        grammar = Grammar(start='BOOL')

        grammar.add_rule('BOOL', 'issubset_', ['SET', 'SET'], 1.0)
        grammar.add_rule('BOOL', 'issuper_', ['SET', 'SET'], 1.0)
        grammar.add_rule('BOOL', 'equal_', ['SET', 'SET'], 1.0)
        grammar.add_rule('BOOL', 'lt', ['NUM', 'NUM'], 1.0)
        grammar.add_rule('BOOL', 'gt', ['NUM', 'NUM'], 1.0)
        grammar.add_rule('BOOL', 'num_eq', ['NUM', 'NUM'], 1.0)

        grammar.add_rule('NUM', 'cardinality_', ['SET'], 1.0)
        for n in range(0,10):
            grammar.add_rule('NUM', str(n), None, 1.0)

        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'A', None, 5)
        grammar.add_rule('SET', 'B', None, 5)
        
        return grammar

    else:
        raise Exception("There exists no g_type \'" + g_type + '\'. To see possible grammar types, refer to grammars.py.')