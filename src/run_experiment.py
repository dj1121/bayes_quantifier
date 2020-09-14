# -----------------------------------------------------------
# Main driver file, specify a hypothesis, data, sample steps, grammar, output
# and train/test a model to get results.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

# Python Imports
import os
import argparse
import time
from math import log

# Personal Code
import primitives
import data_handling
import grammars
import hypotheses

# LOTLib
from LOTlib3.Samplers.MetropolisHastings import MetropolisHastingsSampler
from LOTlib3.TopN import TopN

TIME = time.strftime("%Y%m%d-%H%M%S")

def parse_args():
    """
    Parse all command line arguments

    Parameters:
        - None

    Returns:
        - args (argparse.Namespace): The list of arguments passed in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_dir",type=str, help = "Path to data (monotone, non_convex, or non_monotone)", default ="./../sample_data/monotone/")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../model_out/")
    parser.add_argument("-g_type",type=str, help = "What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py", default ="quant")
    parser.add_argument("-h_type",type=str, help = "What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py", default ="A")
    parser.add_argument("-sample_steps",type=int, help = "How many steps to run the sampler", default=5000)
    parser.add_argument("-alpha",type=float, help = "Assumed noisiness of data (min = 1.0)", default=0.99)
    args = parser.parse_args()
    return args

def infer(data, out, h0, grammar, sample_steps):
    """
    Using data, grammar, and a starting hypothesis, takes sample_steps number
    of samples over data and stores the best ranking hypothesis in TopN. In other
    words, conducts inference/compute posterior over data given. Writes results to
    output files stored in model_out.

    Parameters:
        - data (list): A list of FunctionData objects, a data type of LOTLib specifying input/output pairs for training
        - out (str): A path to where output files will be stored (model accuracy, probabilities, etc.)
        - h0 (LOTlib3.LOTHypothesis): A hypothesis randomly sampled from the grammar specified to serve as a starting hypothesis for inferencing
        - grammar (LOTlib3.Grammar): A PCFG grammar specifying the space of possible hypotheses
        - sample_steps (int): Number of samples to perform in inferencing over the given data

    Returns:
        - None
    """
    
    # Store the top hypothesis (n=1)
    TN = TopN(N=1)

    # Record top N concept(s) with top posterior probability over this data/steps
    with open(out + "_prob.csv", 'a', encoding='utf-8') as f:
        for h in MetropolisHastingsSampler(h0, data, steps=sample_steps):
            TN.add(h)
        for h in TN.get_all(sorted=True):
            f.write(str(h) + "|" + str(h.posterior_score) + "\n")
        f.close()
    
    # With best concept(s), record accuracy over all data provided
    with open(out + "_acc.csv", 'a', encoding='utf-8') as f:
        num_correct = 0
        total = len(data)
        for h in TN.get_all(sorted=True):
            for datum in data:
                if h.compute_single_likelihood(datum) == log(datum.alpha):
                    num_correct += 1
            f.write(str(h) + "|" + str(float(num_correct/total)) + "\n")
        f.close()

if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    # Load data, create grammar
    data = data_handling.load(args.data_dir, args.alpha)
    grammar = grammars.create_grammar(args.g_type)
    sample_steps = args.sample_steps  
    out = args.out + TIME

    # Create headings of output CSV
    with open(out + "_prob.csv", 'a', encoding='utf-8') as f:
        f.write("concept|post_prob\n")
    with open(out + "_acc.csv", 'a', encoding='utf-8') as f:
        f.write("concept|acc\n")
    
    # Run the main algorithm to do inference over each amount of data seen (1 context, 2,...96)
    h0 = hypotheses.create_hypothesis(args.h_type, grammar)
    data = data[0:2] # TODO: Just use first human's data as training? Change in the dataloading part once figured out
    for i in range(len(data)):
        print("Data chunk: ", i)
        data_chunk = data[0:i+1]
        infer(data_chunk, out, h0, grammar, sample_steps)

    # Plot outputs
    data_handling.plot_learn_curves(args.data_dir, out)