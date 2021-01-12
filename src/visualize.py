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

    model_accuracies = []

    for f_name in os.listdir(out + exp_id):
        if ".png" in f_name:
            continue
        path = out + exp_id + "/" + f_name
        df = pd.read_csv(path, sep="|")
        model_accuracies.append(df['acc'])

    model_accuracies = np.array(model_accuracies)
    avg_mod_accuracies = pd.Series(np.average(model_accuracies, axis=0))
    human_accuracies = h_acc(data_dir)
    avg_hum_accuracies = pd.Series(np.average(human_accuracies, axis=0))

    ###########################
    #### Average Curve ####
    ###########################
    plt.figure()

    r2 = r2_score(avg_hum_accuracies, avg_mod_accuracies)

    # Seaborn
    sns.set(style="darkgrid")
    plt.plot(avg_hum_accuracies)
    plt.plot(avg_mod_accuracies)

    # Labels
    plt.xlabel("# Contexts Seen", fontsize=12)
    plt.xticks(np.arange(0, 100, 12))
    plt.yticks((np.arange(0, 1.1, 0.1)))
    plt.ylabel("Accuracy", fontsize=12)
    plt.title("Avg. Human and Model Accuracy Over Data Seen \n(" + exp_id + ")" + "\nr^2: " + str(r2))
    plt.legend(["Average Human Accuracy " + "n=" + str(len(human_accuracies)), 'Average Model Accuracy ' + "n=" + str(len(model_accuracies))])

    # plt.show()
    plt.savefig(out + exp_id + "/" + exp_id + '_acc.png', dpi=400)

    ###########################
    #### Individual Curves ####
    ###########################
    for i in range(0, len(model_accuracies)):
        plt.figure()

        # Seaborn
        sns.set(style="darkgrid")
        plt.plot(human_accuracies[i])
        plt.plot(model_accuracies[i])

        # Labels
        plt.xlabel("# Contexts Seen", fontsize=12)
        plt.xticks(np.arange(0, 100, 12))
        plt.yticks((np.arange(0, 1.1, 0.1)))
        plt.ylabel("Accuracy", fontsize=12)
        plt.title("Human and Model Accuracy Over Data Seen, " + "Model/Human # " + str(i+1) +  "\n(" + exp_id + ")")
        plt.legend(['Human Accuracy', 'Model Accuracy'])

        # plt.show()
        plt.savefig(out + exp_id + "/" + exp_id + '_acc' + str(i+1) + '.png', dpi=400)

    plt.close('all')

# plt_hm_acc("./../data/at_most_2/", "./../results/", exp_id="01122356_at_most_2_0.0_0.0", exp_type="at_most_2")
