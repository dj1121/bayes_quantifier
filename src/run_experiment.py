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
import time
from matplotlib import pyplot as plt
from matplotlib import style
from collections import Counter
from LOTlib3.Samplers.MetropolisHastings import MetropolisHastingsSampler
from LOTlib3.TopN import TopN
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_dir",type=str, help = "Path to data (monotone, non_convex, or non_monotone)", default ="./../data/monotone/")
    parser.add_argument("-out",type=str, help = "Path to store outputs", default ="./../out/")
    parser.add_argument("-g_type",type=str, help = "What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py", default ="quant")
    parser.add_argument("-h_type",type=str, help = "What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py", default ="A")
    parser.add_argument("-sample_steps",type=int, help = "How many steps to run the sampler", default=5000)
    args = parser.parse_args()
    return args


def infer(data, out, h0, grammar, sample_steps):
    tn = TopN(N=10) # store the top N
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open(out + timestr + ".txt", 'w', encoding='utf-8') as f:
        for h in MetropolisHastingsSampler(h0, data, steps=sample_steps):
            tn.add(h)
            f.write(str(h) + "|" + str(h.compute_posterior(data)) + "\n")

        f.write("## Top N:\n")
        for h in tn.get_all(sorted=True):
            f.write("## " + str(h) + " " + str(h.posterior_score) + "\n")
        f.close()

    # Make learning curve
    with open(out + timestr + ".txt", 'r', encoding='utf-8') as f:     
        steps = []
        posteriors = []
        
        i = 0
        for line in f:
            if "#" not in line:
                l = line.split("|")
                steps.append(int(i))
                posteriors.append(float(l[1]))
                i += 1
        plt.xlabel('Steps', fontsize=18)
        plt.ylabel('Posterior Score', fontsize=16)
        plt.title("Concept Learning Curve (5000 steps)")
        plt.plot(steps,posteriors)
        plt.show()


if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    # Load data, craeate grammar
    data = data_handling.load(args.data_dir)
    grammar = grammars.create_grammar(args.g_type)
    sample_steps = args.sample_steps  
    out = args.out
    

    # Run the main algorithm to do inference
    h0 = hypotheses.create_hypothesis(args.h_type, grammar)
    infer(data, out, h0, grammar, sample_steps)

    