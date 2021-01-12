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

# Personal Code
import primitives
import data_handling
import grammars
import hypotheses
import visualize

# LOTLib
from LOTlib3.Samplers.MetropolisHastings import MetropolisHastingsSampler
from LOTlib3.TopN import TopN
from LOTlib3.DataAndObjects import FunctionData, Obj
from LOTlib3.Miscellaneous import Infinity
from LOTlib3 import break_ctrlc

# Other
from multiset import *
import numpy as np
from math import exp

TIME = time.strftime("%m%d%M%S")

def parse_args():
    """
    Parse all command line arguments

    Parameters:
        - None

    Returns:
        - args (argparse.Namespace): The list of arguments passed in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-exp_type", type=str, help="Experiment type (specify folder name of data for quantifier of choice)", default="at_most_2") # Required
    parser.add_argument("-data_dir",type=str, help = "Path to main data directory (not specific quantifier)", default ="./../sample_data/")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../results/")
    parser.add_argument("-g_type",type=str, help = "What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py", default ="quant")
    parser.add_argument("-h_type",type=str, help = "What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py", default ="A")
    parser.add_argument("-sample_steps",type=int, help = "How many steps to run the sampler", default=50)
    parser.add_argument("-alpha",type=float, help = "Assumed noisiness of data (min = 1.0)", default=0.99)
    parser.add_argument("-lam_1",type=float, help = "How much weight to give to degree of monotonicity [0,1]", default=0.0)
    parser.add_argument("-lam_2",type=float, help = "How much weight to give to degree of conservativity [0,1]", default=0.0)
    args = parser.parse_args()
    return args

def infer(data, out, exp_id, h0, grammar, sample_steps, model_num):
    """
    Using data, grammar, and a starting hypothesis, takes sample_steps number
    of samples over data and stores the best ranking hypothesis in TopN. In other
    words, conducts inference/compute posterior over data given.

    Parameters:
        - data (list): A list of FunctionData objects, a data type of LOTLib specifying input/output pairs for training
        - out (str): A path to where output files will be stored (model accuracy, probabilities, etc.)
        - exp_id (str): Identifier for this experiment run
        - h0 (LOTlib3.LOTHypothesis): A hypothesis randomly sampled from the grammar specified to serve as a starting hypothesis for inferencing
        - grammar (LOTlib3.Grammar): A PCFG grammar specifying the space of possible hypotheses
        - sample_steps (int): Number of samples to perform in inferencing over the given data
        - model_num (int): What number model we are training (since data may be split per human)

    Returns:
        - None
    """
    
    # Store the top 10 hypotheses (n=10)
    TN = TopN(N=10)

    infer_data = data[0:-1]
    eval_data = data

    # Record top N concept(s) with top posterior probability over this data/steps
    # Infer with data/labels from all previous contexts (not current), 0th context = inference with no labels seen yet
    i = 1
    for h in break_ctrlc(MetropolisHastingsSampler(h0, infer_data, steps=sample_steps)):
        # print("Sample #", i, "--- Hypothesis Length:", h.value.count_nodes(),\
        #     "Mono:", h.value.degree_monotonicity, "Cons:", h.value.degree_conservativity)
        TN.add(h)
        i += 1

    # With 10 best hypotheses, record avg accuracy over all data provided so far (including this context)
    with open(args.out + exp_id + "/" + exp_id + "_" + str(model_num) +  ".csv", 'a', encoding='utf-8') as f:
        accs = []
        total = len(eval_data)
        for h in TN.get_all(sorted=True):
            num_correct = 0
            for datum in eval_data:
                # If the model guesses the right training label
                if h.eval_q_m(datum) == datum.output:
                    num_correct += 1
            accs.append(num_correct/total)
        f.write(str(float(np.mean(accs))) + "\n")
        f.close()

def train(data, h0, n_contexts, out, exp_id, sample_steps):
    """
    Train as many models as there are humans, each with n contexts (training data points). 
    Each model is trained on same data as the corresponding human sees 
    (i.e. human 1/model 1 sees datapoints 1-96, human 2/model 2 sees 97-192, etc.). Accuracy
    and probability results stored during training in experiment results folder.

    Parameters:
        - data (list): A list of FunctionData objects, LOTLib's specific data type for input/output pairs.
        - h0 (LOTlib3.LOTHypothesis): A hypothesis randomly sampled from the grammar specified to serve as a starting hypothesis for inferencing
        - n_contexts (int): Number of contexts (data points) each human/model sees
        - out (str): A path to where output files will be stored (model accuracy, probabilities, etc.)
        - exp_id (str): Identifier for this experiment run
        - sample_steps (int): Number of samples to perform in inferencing over the given data
    
    Returns:
        - None
    """
    # Split data per n amount of contexts per human
    # A separate model is trained on each set of data (as each human sees)
    data_split = []
    for i in range(0, len(data), n_contexts):
        data_split.append(data[i:i+n_contexts])    

    # Inference over of data seen so far by given model (mimicking humans seeing contexts in succession)
    for i in range(0, len(data_split)):
        # Create headings of output CSV
        with open(out + exp_id + "/" + exp_id + "_" + str(i+1) +  ".csv", 'a', encoding='utf-8') as f:
            f.write("acc\n")

        model_i_data = data_split[i]
        print("Training Model:", i + 1, "of", len(data_split))
        for j in range(len(model_i_data)):
            data_chunk = model_i_data[0:j+1]
            print("Model " + str(i + 1) + ", Context #:", j + 1, ", Inferring with Contexts #:", 0, "to", j)
            infer(data_chunk, args.out, exp_id, h0, grammar, sample_steps, model_num=i+1)

if __name__ == "__main__":
    
    args = parse_args()
    
    # Make results folder
    lam_1 = args.lam_1
    lam_2 = args.lam_2
    if not os.path.exists(args.out): 
        os.makedirs(args.out)
    data_path = args.data_dir + "/" + args.exp_type + "/"
    exp_id = TIME + "_" + args.exp_type + "_" + str(lam_1) + "_" + str(lam_2)
    os.mkdir(args.out + exp_id + "/")

    # Load all possible contexts (for degrees of univ.)
    # Better than doing in hypothesis class since this only needs calculation once
    all_contexts = data_handling.generate_possible_contexts(['red','blue'], [3.0, 100.0], 8)

    # Load data, create grammar
    data, n_contexts = data_handling.load(data_path, args.alpha)
    grammar = grammars.create_grammar(args.g_type)
    sample_steps = args.sample_steps

    # # For bug testing purposes
    # test_hypothesis = hypotheses.create_hypothesis(args.h_type, grammars.create_grammar("error_testing"), lam_1, lam_2, all_contexts)

    # Select a starting hypothesis and train
    h0 = hypotheses.create_hypothesis(args.h_type, grammar, lam_1, lam_2, all_contexts)
    train(data, h0, n_contexts, args.out, exp_id, sample_steps)

    # Plot outputs
    visualize.plt_hm_acc(data_path, args.out, exp_id, args.exp_type)