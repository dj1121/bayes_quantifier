# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from LOTlib3.DataAndObjects import FunctionData
import csv
from multiset import *

colors = {'red': 0, 'blue': 1, 'green': 2, 'yellow': 3}
ans = {'c': True, 'm': False}

# Import (training) data here and convert to numbered
data = []
with open('./data/monotone/12h05.39.006.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        x = Multiset([])
        y = Multiset([])
        out = None
        if row[37] in colors: # col 37 is "obj1"
            for col in range(37,43):
                curr_obj = colors[row[col]]
                if len(x) == 0 and len(y) == 0:
                    x.add(curr_obj)
                else:
                    if curr_obj in x:
                        x.add(curr_obj)
                    else:
                        y.add(curr_obj)
            out = ans[row[43]]

        # print("x: ", x)
        # print("y: ", y)
        # print("out: ", out)

        if len(x) > 0 and len(y) > 0 and out != None:  
            data.append(FunctionData(input = [x,y], output=out, alpha=0.95)) # Put into format needed for LOTLib

    # data = load_data.load(filename or directory)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Grammar
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from LOTlib3.Grammar import Grammar
from LOTlib3.Eval import primitive
import primitives

# Start symbol
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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Hypothesis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from math import log
from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis

class QuantHypothesis(LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, display="lambda A, B: %s", **kwargs)  # display = str(self.value)
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    def compute_single_likelihood(self, datum):

        if self(*datum.input) == datum.output: # pass data input to hypothesis (as a function), goes to "call"
            return log((1.0-datum.alpha)/100. + datum.alpha)
        else:
            return log((1.0-datum.alpha)/100.)

    def weight(self, data):
        print()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    h = QuantHypothesis()
    print(h)
    l = h.compute_likelihood(data)
    print(l)