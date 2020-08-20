# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.DataAndObjects import FunctionData
import os
import numpy as np
from collections import Counter
from multiset import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


"""
Load human data from experiments
"""
def load(data_dir):

    data = [] # A list of FunctionData objects (what LOTlib uses)
    colors = {"red": 0, "blue": 1, "green": 2, "yellow": 3}

    # Load all experiments in data directory
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r', encoding="utf-8"))

        # Get relevant columns (objs and labels)
        df = df.loc[:, 'obj1':'corrAns'].dropna()
        # Iterate over rows and columns, create FunctionData objects
        for index, row in df.iterrows():
            obj_sets = {}
            label = None
            for col in df:
                if "obj" in col:
                    if row[col] not in obj_sets:
                        obj_sets[row[col]] = Multiset()
                        obj_sets[row[col]].add(colors[row[col]])
                    else:
                        obj_sets[row[col]].add(colors[row[col]])
                else:
                    # If "corrAns" column is c, output = true, else = false
                    label = (row[col] == "c")

            if len(obj_sets) == 1: # All items are same color, make an empty set as the second argument
                data.append(FunctionData(input=[obj_sets[key] for key in obj_sets] + [Multiset()], output=label, alpha=0.99))
            else:
                data.append(FunctionData(input=[obj_sets[key] for key in obj_sets], output=label, alpha=0.99))

    return data

"""
Plots a learning curve from human data and model data
"""
def plot_learn_curve(data_dir, model_out):
    
    # Ten human participants, 96 accuracy points on each
    human_accuracies = []

    # Load all experiment data in data directory (each participant)
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r', encoding="utf-8"))

        # Get answer column for this participant (objs and labels)
        series = df['key_resp_monotonicity.corr'].dropna()

        # Participant performance (get accuracy at each step)
        accuracies = []
        for i in range(1, len(series) + 1):
            corr_so_far = series[0:i].value_counts()
            acc = 0
            if 1.0 in corr_so_far.keys() and 0.0 in corr_so_far.keys():
                acc = corr_so_far[1.0] / (corr_so_far[1.0] + corr_so_far[0.0])
            elif corr_so_far.keys()[0] == 1.0:
                acc = 1
            accuracies.append(acc)

        human_accuracies.append(accuracies)
    
    # Get average of human accuracies at each step
    human_accuracies = np.array(human_accuracies)
    avg_accuracies = np.average(human_accuracies, axis=0)
    
    output = pd.Series(avg_accuracies)
    sns.set(style="darkgrid")
    sns.relplot(kind="line", data=output)
    plt.xlabel("# Contexts Seen")
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Avg. Human Accuracy")
    plt.title("Human Learning Curve: Monotone Quantifier")
    plt.show()



plot_learn_curve("../data/monotone/", "none")