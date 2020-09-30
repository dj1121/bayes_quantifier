# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------
import os
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

    NOTE: Training labels are assumed to be key_resp_monotonicity.corr

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
        df = df.loc[:, 'key_resp_monotonicity.corr':'obj6'].dropna()
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
                elif "key_resp_monotonicity.corr" in col:
                    label = (row[col] == 1) # 0 means False
                else:
                    continue
                    
            if len(obj_sets) == 1: # If all items are same color, make an empty multiset as the second argument
                data.append(FunctionData(input=[obj_sets[key] for key in obj_sets] + [Multiset()], output=label, alpha=alpha))
            else:
                data.append(FunctionData(input=[obj_sets[key] for key in obj_sets], output=label, alpha=alpha))

    return data, n_contexts
