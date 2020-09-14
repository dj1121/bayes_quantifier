# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

# Python Imports
import os

# Analysis Tools
import numpy as np
from multiset import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# LOTLib3
from LOTlib3.DataAndObjects import FunctionData

def load(data_dir, alpha):
    """
    Loads and returns training data for the model (contexts -> labels).
    Data is stored as a list of FunctionData objects. Each FunctionData object
    represents a datum (one piece of data) with an input which is a list of two
    multisets of colored objects, and an output which is true or false denoting 
    if the input represents the current concept being learned.

    NOTE: This loading method gives a certain structure to data (i.e. two multisets). If such a structure is not desired as input,
    then another function ought to be created and thus another type of hypothesis (which works over another data input type)
    in hypotheses.py.

    Parameters:
        - data_dir (str): Path to where data is stored. By default, there are multiple CSV files for one experiment type (representing each human). 
        - alpha (float): Assumed noisiness of data being loaded (i.e. incorrect labels, etc.)

        TODO: What data are we using? Just the first human?

    Returns:
        - data (list): A list of FunctionData objects, LOTLib's specific data type for input/output pairs.
    """

    data = []
    colors = {"red": 0, "blue": 1, "green": 2, "yellow": 3}

    # Load all data files in experiment directory
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r', encoding="utf-8"))

        # Iterate over rows and columns, create FunctionData objects
        df = df.loc[:, 'obj1':'corrAns'].dropna()
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

            if len(obj_sets) == 1: # If all items are same color, make an empty multiset as the second argument
                data.append(FunctionData(input=[obj_sets[key] for key in obj_sets] + [Multiset()], output=label, alpha=alpha))
            else:
                data.append(FunctionData(input=[obj_sets[key] for key in obj_sets], output=label, alpha=alpha))

    return data

def plot_learn_curves(data_dir, out):
    """
    Plots learning curves:
        - Human Learning Curve: A plot of average human accuracy over # contexts seen with an error band of 1 standard deviation.
        - Model Learning Curve: A the concepts with (log) top posterior probability at each amount of data seen.
        - Human/Model Learninr Curve: A plot of average human accuracy AND (non-average) model accuracy over each amount of data seen.

    To make more plots, add code below and preface it with plt.figure(n) to start a new plot.

    Parameters:
        - data_dir (str): Path to where human experiment data stored (used for plotting human performance)
        - out (str): Path to where model output stored (used for plotting model performance) and path where plots (png files) will be saved

    Returns:
        - None
    """

    ########################
    # HUMAN LEARNING CURVE #
    ########################

    plt.figure(0)

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


    human_accuracies = np.array(human_accuracies)
    avg_accuracies = pd.Series(np.average(human_accuracies, axis=0))
    sd_accuracies = pd.Series(np.std(human_accuracies, axis=0))

    # Seaborn
    sns.set(style="darkgrid")
    plt.fill_between(x=np.arange(len(avg_accuracies)),
                 y1=avg_accuracies - sd_accuracies,
                 y2=avg_accuracies + sd_accuracies,
                 alpha=0.25
                 )
    plt.plot(np.arange(len(avg_accuracies)), avg_accuracies)

    # Labels
    plt.xlabel("# Contexts Seen")
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Avg. Human Accuracy")
    plt.title("Human Learning Curve: \n" + out)
    # plt.show()
    plt.savefig(out + '_human_plot.png', dpi=200)


    #########################################################
    # MODEL LEARNING CURVE (top concept at each # data seen)#
    #########################################################

    plt.figure(1)

    df = pd.read_csv(out + "_prob.csv", sep='|')
    concepts = df['concept']
    model_probs = df['post_prob']

    # Seaborn
    sns.set(style="darkgrid")
    plt.plot(np.arange(len(model_probs)), model_probs)

    # Labels
    plt.xlabel("# Contexts Seen")
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Posterior Probability (Log)")
    plt.title("Best Posterior Score per Data Seen \n" + out)
    # Print the concept out for every 12th concept
    style = dict(size=7, color='gray')
    for i in range(0, len(model_probs), 11):
        plt.text(i, model_probs[i], concepts[i], **style)
    # plt.show()
    plt.savefig(out + '_prob.png', dpi=200)


    ################################
    # HUMAN + MODEL LEARNING CURVE #
    ################################
    plt.figure(2)

    df = pd.read_csv(out + "_acc.csv", sep='|')
    concepts = df['concept']
    model_acc = df['acc']

    # Seaborn
    sns.set(style="darkgrid")
    plt.plot(avg_accuracies)
    plt.plot(model_acc)

    # Labels
    plt.xlabel("# Contexts Seen")
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Accuracy")
    plt.title("Human and Model Accuracy Over Data Seen \n" + out)
    plt.legend(['Average Human Accuracy', 'Model Accuracy'])

    # plt.show()
    plt.savefig(out + '_acc.png', dpi=200)