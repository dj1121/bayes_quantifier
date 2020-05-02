
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Primitives Functions (add new ones if needed)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from LOTlib3.Eval import primitive

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Grammar (For generating hypothesis space)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from LOTlib3.Grammar import Grammar

grammar = Grammar()

s = set([1,2,3])

# FORMAT: grammar.add_rule( <NONTERMINAL>, <FUNCTION NAME>, <ARGUMENTS>, <PROBABILITY>)

grammar.add_rule('START', '', ['FUNCTION'], 1.0)

grammar.add_rule('SET', 'S', None, 1.0)
grammar.add_rule('FUNCTION', 'lambda', ['BOOL'], 1.0, bv_type='SET')

# Simple boolean
grammar.add_rule('BOOL', 'and_', ['BOOL', 'BOOL'], 1.0)
grammar.add_rule('BOOL', 'or_', ['BOOL', 'BOOL'], 1.0)
grammar.add_rule('BOOL', 'not_', ['BOOL'], 1.0)

# Set operations
grammar.add_rule('BOOL', 'empty_', ['SET'], 1.0)
grammar.add_rule('BOOL', 'cardinality1_', ['SET'], 1.0)
grammar.add_rule('BOOL', 'cardinality2_', ['SET'], 1.0)
grammar.add_rule('BOOL', 'cardinality3_', ['SET'], 1.0)
grammar.add_rule('BOOL', 'cardinality4_', ['SET'], 1.0)
grammar.add_rule('BOOL', 'cardinality5_', ['SET'], 1.0)
grammar.add_rule('BOOL', 'cardinality6_', ['SET'], 1.0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Hypothesis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib3.Hypotheses.Likelihoods.BinaryLikelihood import BinaryLikelihood

class MyHypothesis(BinaryLikelihood, LOTHypothesis):
    def __init__(self, grammar=grammar, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, **kwargs)


# Example data (only one)
from LOTlib3.DataAndObjects import FunctionData
data = [FunctionData(input=[True], output=False, alpha=0.95)]


# Make an example hypothesis
h = MyHypothesis()
print (h.compute_prior(), h.compute_likelihood(data), h)