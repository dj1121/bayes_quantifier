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
from hypotheses import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data",type=str, help = "Path to data (monotone, non_convex, or non_monotone)", default ="./../data/monotone/")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../out/")
    parser.add_argument("-g_type",type=str, help = "What type of grammar to use, defined in grammars.py {quant, num,...}. Define your own in grammars.py", default ="quant")
    parser.add_argument("-h_type",type=str, help = "What type of hypothesis to use, defined in hypotheses.py {A,B,C,...}. Define your own in hypotheses.py", default ="A")
    args = parser.parse_args()
    return args

def learn(data, out, h, g): 
    l = h.compute_likelihood(data)
    print(h)
    print(l)

if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    data = data_handling.load(args.data)
    out = args.out

    # # Get the grammar type (should be defined in grammars.py)
    # g = grammars.create_grammar(args.g_type)
    # if g == None:
    #     raise Exception("There exists no g_type \'" + args.g_type + '\'. Try one of: {sem}. To see each grammar definition, refer to grammars.py.')

    # # Get the hypothesis (should be defined in hypotheses.py)
    # h = None
    # if args.h_type == "A":
    #     h = HypothesisA(grammar=g)
    # else:
    #     raise Exception("There exists no h_type \'" + args.h_type + '\'. Try one of: {A}.')
    
    
    # # Run the main algorithm to do inference
    # learn(data, out, h, g)