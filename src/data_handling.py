# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------
import os
import numpy as np
from multiset import *
from itertools import combinations_with_replacement
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# LOTLib3
from LOTlib3.DataAndObjects import FunctionData, Obj

    
def generate_possible_contexts(colors, shapes, max_num_objects):
    """
    Generate possible contexts

    Parameters:
        - colors (list (str)) List of unique color names as seen in data (i.e. ['red', 'blue'])
        - shapes (list (float)) List of unique shape numbers (i.e. 3.0, 100.0)
        - max_num_objects (int) Maximum number of objects per context

    Returns:
        - 
    """
    contexts = []

    A_B_possible = [] # List of tuples of format (possible A set, [list of possible B sets corresponding])

    # Generate A sets
    for i in range(0, max_num_objects + 1):
        c = list(combinations_with_replacement(colors, i)) # Generate all possible combos of length i and colors
        
        for j in range(0, len(c)): # List of tuples
            curr_A_set = Multiset() # Construct a possible A set from current tuple
            curr_tuple = c[j]

            for k in range(0, len(curr_tuple)):
                curr_A_set.add(Obj(color=curr_tuple[k], shape=3.0))

            A_B_possible.append((curr_A_set, []))
    
    # Generate B sets
    print(A_B_possible)

    

                

def load(data_dir, alpha):
    """
    Loads and returns training data for the model (contexts -> labels).
    For example, with 10 humans seeing 96 contexts each, there will be
    960 data points. Data is stored as a list of FunctionData objects. 
    Each FunctionData object represents a datum with an input 
    which is a list of two multisets of colored objects, and an output which is 
    true or false denoting if the input represents the current concept being learned.

    NOTE: This loading method gives a certain structure to data (i.e. two multisets, A and B). In particular, given default experiment,
    set A = all triangles and set B = all red objects. If such a structure is not desired as input, then another function ought to be 
    created and thus another type of hypothesis (which works over another data input type) in hypotheses.py.

    Parameters:
        - data_dir (str): Path to where data is stored. By default, there are multiple CSV files for one experiment type (representing each human). 
        - alpha (float): Assumed noisiness of data being loaded (i.e. incorrect labels, etc.)

    Returns:
        - data (list): A list of FunctionData objects, LOTLib's specific data type for input/output pairs.
        - n_contexts (int): Number of contexts seen per each human
    """

    data = []  
    n_contexts = 0  # Number of contexts seen per each human

    # Load all data files in experiment directory
    for f_name in os.listdir(data_dir):
        n_contexts = 0
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r', encoding="utf-8"))

        # Iterate over rows and columns, create FunctionData objects
        df = df.loc[:, 'obj1':'shape8'].dropna()
        for index, row in df.iterrows():

            n_contexts += 1
            context_objects = [] # all objects in context
            set_A = Multiset() # all triangles in context
            set_B = Multiset() # all red objects in context
            label = None       # Whether quantifier is true in this context of set A and B

            # Construct objects from this row's (datapoint's) columns
            shape_num = 0
            for col in df:
                if "obj" in col:
                    context_objects.append(Obj(color=row[col], shape=None))
                elif "corrAns" in col:
                    label = (row[col] == "t")
                elif "shape" in col:
                    context_objects[shape_num].shape = row[col]
                    shape_num += 1
                else:
                    continue
            
            # Split objects into appropriate sets
            for o in context_objects:
                if o.color == 'gray':
                    continue
                if o.shape == 3.0:
                    set_A.add(o)
                if o.color == 'red':
                    set_B.add(o)

            # Add this context/label to dataset
            data.append(FunctionData(input=[set_A, set_B], output=label, alpha=alpha))

    return data, n_contexts


generate_possible_contexts(['red', 'blue'], [3.0, 100.0], 8)