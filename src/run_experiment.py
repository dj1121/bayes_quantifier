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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_dir",type=str, help = "Path to data (monotone, non_convex, or non_monotone)", default ="./../data/monotone/")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../out/")
    parser.add_argument("-n_colors_context", type=int, help= "Number of colors allowed in each context", default=2)
    parser.add_argument("-g_type",type=str, help = "What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py", default ="quant")
    parser.add_argument("-h_type",type=str, help = "What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py", default ="A")
    args = parser.parse_args()
    return args

def infer(data, out, h, grammar):
    print(h)
    print(h.compute_prior())
    print(h.compute_likelihood(data))

    # count = Counter()
    # for h_i in MetropolisHastingsSampler(h, data, steps=1000):
    #     count[h_i] += 1
    
    # for h_i in sorted(count.keys(), key=lambda x: count[x]):
    #     print(count[h_i], h_i.posterior_score, h_i)

if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    data = data_handling.load(args.data_dir)
    out = args.out
    grammar = grammars.create_grammar(args.g_type)
    h = hypotheses.create_hypothesis(args.h_type, grammar, args.data_dir, args.n_colors_context)

    # Run the main algorithm to do inference
    infer(data, out, h, grammar)

    