# -----------------------------------------------------------
# Functions for visualizing results.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score

def h_acc(data_dir):
    """
    Calculates human accuracies from each of the human data files in the data_dir.
    This varian uses % of people who got the nth context right

    Parameters:
        - data_dir (str): Path to where human experiment data stored (used for plotting human performance)

    Returns:
        - human_accuracies (numpy array): A matrix of all human accuracies (each row = human, each col = context)
    """
    
    human_answers = []

    # Load all experiment data in data directory (each participant)
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r', encoding="utf-8"))
        
        # Length-n list where n = # of contexts, each element is 1 if human answered correctly, else 0
        ans = np.array(df['key_resp_monotonicity.corr'].dropna())

        # Add this as a row to human accuraceies MxN where M = # humans, N = # contexts
        human_answers.append(ans)

    human_answers = (np.array(human_answers)).T
    
    human_accuracies = []
    for i, row in enumerate(human_answers):
        unique, counts = np.unique(human_answers[i, :], return_counts=True)
        result = dict(zip(unique, counts))
        acc = result[1.0] / len(human_answers[i, :])
        human_accuracies.append(acc)

    human_accuracies = np.array(human_accuracies)
    
    return human_accuracies

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
    
    # Get model and human accuracies separately
    model_post_preds = []

    for f_name in os.listdir(out + exp_id):
        if ".png" in f_name:
            continue
        path = out + exp_id + "/" + f_name
        df = pd.read_csv(path, sep="|")
        model_post_preds.append(df['post_pred'])

    model_post_preds = (np.array(model_post_preds)).T
    avg_mod_post_preds = np.average(model_post_preds, axis=1)
    human_percent_correct = h_acc(data_dir)

    # Plot
    plt.figure()
    r2 = r2_score(human_percent_correct, avg_mod_post_preds)

    sns.set(style="darkgrid")
    plt.plot(human_percent_correct)
    plt.plot(avg_mod_post_preds)

    # Labels
    plt.xlabel("# Contexts Seen", fontsize=12)
    plt.xticks(np.arange(0, 100, 12))
    plt.yticks((np.arange(0, 1.1, 0.1)))
    plt.title("Human and Model Learning Curves \n(" + exp_id + ")" + "\nr^2: " + str(r2))
    plt.legend(["% Humans Correct", 'Avg. Posterior Predictive'])

    # plt.show()
    plt.savefig(out + exp_id + "/" + exp_id + '_acc.png', dpi=400)
    plt.close('all')

# plt_hm_acc("./../data/between_3_6/", "./../results/", exp_id="01203813_between_3_6_0.0_0.0", exp_type="between_3_6")
