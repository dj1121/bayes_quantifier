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
import re

# LOTLib3
from LOTlib3.DataAndObjects import FunctionData

    
def generate_possible_contexts(colors, shapes, max_num_objects):
    """
    Generate possible contexts. Outputs to a csv file with the following code
        - rt = red triangle
        - bt = blue triangle
        - rc = red circle
        - bc = blue circle
    Outputs to data folder

    Parameters:
        - colors (list (str)) List of unique color names as seen in data (i.e. ['red', 'blue'])
        - shapes (list (float)) List of unique shape numbers (i.e. 3.0, 100.0)
        - max_num_objects (int) Maximum number of objects per context

    Returns:
        - contexts (list (multiset)) Return all contexts as a list
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
                if curr_tuple[k] == "blue":
                    curr_A_set.add("blue_3") # Blue triangle
                elif curr_tuple[k] == "red":
                    curr_A_set.add("red_3") # Red triangle

            A_B_possible.append((curr_A_set, []))
    
    # Given each A set, generate possible B sets
    for tup in A_B_possible:

        # Get details of current set
        curr_A_set = tup[0]
        n_red_triangles = 0
        n_blue_triangles = 0
        for obj in curr_A_set:
            if "blue" in obj:
                n_blue_triangles += 1
            else:
                n_red_triangles += 1

        # Generate all B sets corresponding to this A set (adding same num red triangles, then red circles)
        for i in range(0, max_num_objects - n_blue_triangles - n_red_triangles + 1):
            possible_B_set = Multiset()
            for j in range(0, n_red_triangles):
                possible_B_set.add("red_3")
            for k in range(0,i):
                possible_B_set.add("red_100")
            tup[1].append(possible_B_set)

    # Build contexts from A/B possible sets
    for tup in A_B_possible:
        a_set = tup[0]
        for b_set in tup[1]:
            contexts.append(FunctionData(input=[a_set,b_set], output=None, alpha=1.0))

    # Output to csv file
    with open("./../data/" + "contexts.csv", "w") as f:
        f.write("set_A,set_B\n")
        for context in contexts:
            i = context.input
            a = str(i[0])
            a = re.sub(r'OBJECT|<|{|}|<|>|:| |,|', '', a)
            a = re.sub(r'3', '3;', a)
            a = re.sub(r'100', '100;', a)
            b = str(i[1])
            b = re.sub(r'OBJECT|<|{|}|<|>|:| |,|', '', b)
            b = re.sub(r'3', '3;', b)
            b = re.sub(r'100', '100;', b)
            f.write(a + "," + b + "\n")
    
    return contexts
 
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
                    context_objects.append(row[col])
                elif "corrAns" in col:
                    label = (row[col] == "t")
                elif "shape" in col:
                    context_objects[shape_num] = context_objects[shape_num] + "_" + str(int(row[col]))
                    shape_num += 1
                else:
                    continue
            
            # Split objects into appropriate sets
            for o in context_objects:
                if 'gray' in o:
                    continue
                if "3" in o:
                    set_A.add(o)
                if 'red' in o:
                    set_B.add(o)

            # Add this context/label to dataset
            data.append(FunctionData(input=[set_A, set_B], output=label, alpha=alpha))

    return data, n_contexts