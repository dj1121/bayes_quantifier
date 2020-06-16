# -----------------------------------------------------------
# Main driver file, specify a hypothesis, data, grammar, output
# and train a model to get results.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------
import argparse
import primitives
import data_handling
from hypotheses import *
from LOTlib3.Grammar import Grammar
from math import log
from multiset import *


def create_grammar():
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data",type=str, help = "Path to data", default ="./../data")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../out/")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    data = data_handling.load(args.data)
    grammar = create_grammar()
    h = HypothesisA(grammar=grammar)
    # l = h.compute_likelihood(data)
    # print(h)
    # print(l)