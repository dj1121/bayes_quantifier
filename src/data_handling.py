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
    There are, by default, 960 data points since each human sees 96 contexts
    and there are 10 humans. Data is stored as a list of FunctionData objects. 
    Each FunctionData object represents a datum (one piece of data) with an input 
    which is a list of two multisets of colored objects, and an output which is 
    true or false denoting if the input represents the current concept being learned.

    NOTE: This loading method gives a certain structure to data (i.e. two multisets). If such a structure is not desired as input,
    then another function ought to be created and thus another type of hypothesis (which works over another data input type)
    in hypotheses.py.

    Parameters:
        - data_dir (str): Path to where data is stored. By default, there are multiple CSV files for one experiment type (representing each human). 
        - alpha (float): Assumed noisiness of data being loaded (i.e. incorrect labels, etc.)

    Returns:
        - data (list): A list of FunctionData objects, LOTLib's specific data type for input/output pairs.
        - n_contexts (int): Number of contexts seen per each human
    """

    data = []
    n_contexts = 0
    colors = {"red": 0, "blue": 1, "green": 2, "yellow": 3}

    # Load all data files in experiment directory
    for f_name in os.listdir(data_dir):
        n_contexts = 0
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r', encoding="utf-8"))

        # Iterate over rows and columns, create FunctionData objects
        df = df.loc[:, 'obj1':'corrAns'].dropna()
        for index, row in df.iterrows():
            n_contexts += 1
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

    return data, n_contexts

def h_acc(data_dir):
    """
    Calculates human accuracies from each of the human data files in the data_dir.

    Parameters:
        - data_dir (str): Path to where human experiment data stored (used for plotting human performance)

    Returns:
        - human_accuracies (numpy array): A matrix of all human accuracies (each row = human, each col = amount of data seen)
    """
    # Ten human participants, by default 96 accuracy points on each
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
    
    return human_accuracies

def plt_h_acc(data_dir, out, exp_id, exp_type):
    """
    Plots human learning curve, a plot of average human accuracy over # contexts seen with an error band of 1 standard deviation.
    Saves a .png file of plot in experimental results folder.

    Parameters:
        - data_dir (str): Path to where human experiment data stored (used for plotting human performance)
        - out (str): Path to where model output stored (used for plotting model performance) and path where plots (png files) will be saved
        - exp_id (str): Identifier for this experiment run
        - exp_type (str): What kind of experiment is being run (monotone, non-convex, non-monotone, etc.)

    Returns:
        - None
    """

    plt.figure()

    # Read human data files and get human accuracies
    human_accuracies = h_acc(data_dir)
    avg_hum_accuracies = pd.Series(np.average(human_accuracies, axis=0))
    sd_accuracies = pd.Series(np.std(human_accuracies, axis=0))

    # Seaborn
    sns.set(style="darkgrid")
    plt.fill_between(x=np.arange(len(avg_hum_accuracies)),
                 y1=avg_hum_accuracies - sd_accuracies,
                 y2=avg_hum_accuracies + sd_accuracies,
                 alpha=0.25
                 )
    plt.plot(np.arange(len(avg_hum_accuracies)), avg_hum_accuracies)

    # Labels
    plt.xlabel("# Contexts Seen", fontsize=12)
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Avg. Human Accuracy", fontsize=12)
    plt.title("Human Learning Curve \n(" + exp_type + ")")
    # plt.show()
    plt.savefig(out + exp_id + "/" + exp_id + '_human_plot.png', dpi=400)

def plt_mprob(data_dir, out, exp_id, exp_type):
    """
    Plots the top hypothesis over all models trained per data seen, along with the posterior probability of that hypothesis.
    NOTE: Uses default Pandas method of tiebreaking
    Saves a .png file of plot in experimental results folder.

    Parameters:
        - data_dir (str): Path to where human experiment data stored (used for plotting human performance)
        - out (str): Path to where model output stored (used for plotting model performance) and path where plots (png files) will be saved
        - exp_id (str): Identifier for this experiment run
        - exp_type (str): What kind of experiment is being run (monotone, non-convex, non-monotone, etc.)

    Returns:
        - None
    """

    plt.figure()

    dfs = []

    # Append data frames to model_probs
    for f_name in os.listdir(out + exp_id):
        path = out + exp_id + "/" + f_name
        if "_prob_" not in path:
            continue
        dfs.append(pd.read_csv(open(path, 'r', encoding="utf-8"), sep="|"))
     
    # Data frame that finds max hypothesis/prob pair per each row over all models
    df = pd.concat(dfs).min(level=0)
    model_probs = df['post_prob']
    hypotheses = df['hypothesis']
    
    # Seaborn
    sns.set(style="darkgrid")
    plt.plot(np.arange(len(model_probs)), model_probs, '.-')

    # Labels
    plt.xlabel("# Contexts Seen", fontsize=12)
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Posterior Probability (Log)", fontsize=12)
    plt.title("Best Posterior Score Per Data Seen \n(" + exp_type + ")")
    # Print the concept out for every 12th concept
    style = dict(size=7, color='gray')
    for i in range(0, len(model_probs), 11):
        plt.text(i, model_probs[i], hypotheses[i], **style)
    # plt.show()
    plt.savefig(out + exp_id + "/" + exp_id +'_prob.png', dpi=400)

def plt_hm_acc(data_dir, out, exp_id, exp_type):
    """
    Plots the average human accuracy and average model accuracy per data seen.
    Saves a .png file of plot in experimental results folder.

    Parameters:
        - data_dir (str): Path to where human experiment data stored (used for plotting human performance)
        - out (str): Path to where model output stored (used for plotting model performance) and path where plots (png files) will be saved
        - exp_id (str): Identifier for this experiment run
        - exp_type (str): What kind of experiment is being run (monotone, non-convex, non-monotone, etc.)

    Returns:
        - None
    """

    plt.figure()

    # Get average model accuracy and avg human accuracy
    model_accuracies = []

    for f_name in os.listdir(out + exp_id):
        path = out + exp_id + "/" + f_name
        if "_acc_" not in path:
            continue
        df = pd.read_csv(open(path, 'r', encoding="utf-8"), sep="|")
        model_accuracies.append(df['acc'])
    
    model_accuracies = np.array(model_accuracies)
    avg_mod_accuracies = pd.Series(np.average(model_accuracies, axis=0))
    human_accuracies = h_acc(data_dir)
    avg_hum_accuracies = pd.Series(np.average(human_accuracies, axis=0))

    # Seaborn
    sns.set(style="darkgrid")
    plt.plot(avg_hum_accuracies)
    plt.plot(avg_mod_accuracies)

    # Labels
    plt.xlabel("# Contexts Seen", fontsize=12)
    plt.xticks(np.arange(0, 100, 12))
    plt.ylabel("Accuracy", fontsize=12)
    plt.title("Human and Model Accuracy Over Data Seen \n(" + exp_type + ")")
    plt.legend(['Average Human Accuracy', 'Average Model Accuracy'])

    # plt.show()
    plt.savefig(out + exp_id + "/" + exp_id + '_acc.png', dpi=400)