# -----------------------------------------------------------
# Main driver file, specify a hypothesis, data, grammar, output
# and train a model to get results.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------
import argparse
import primitives
import os
import data_handling
import grammars
import hypotheses
from collections import Counter
from LOTlib3.Samplers.MetropolisHastings import MetropolisHastingsSampler
from LOTlib3.TopN import TopN
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_dir",type=str, help = "Path to data (monotone, non_convex, or non_monotone)", default ="./../data/monotone/")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../out/")
    parser.add_argument("-n_colors_context", type=int, help= "Number of colors allowed in each context", default=2)
    parser.add_argument("-g_type",type=str, help = "What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py", default ="quant")
    parser.add_argument("-h_type",type=str, help = "What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py", default ="A")
    args = parser.parse_args()
    return args

def infer(data, out, h0, grammar):
    print(h0)
    print(h0.compute_prior())
    # print(h0.compute_likelihood(data))

    # tn = TopN(N=10) # store the top N
    # for h in MetropolisHastingsSampler(h0, data, steps=1000):
    #     tn.add(h)

    # for h in tn.get_all(sorted=True):
    #     print(h.posterior_score, h)

if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    # Load data, get possible contexts, create grammar
    data = data_handling.load(args.data_dir)
    contexts = data_handling.get_contexts(args.data_dir, args.n_colors_context)
    grammar = grammars.create_grammar(args.g_type)    
    out = args.out

    # Run the main algorithm to do inference
    h0 = hypotheses.create_hypothesis(args.h_type, grammar, contexts)
    infer(data, out, h0, grammar)

    