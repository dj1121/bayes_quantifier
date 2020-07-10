# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.DataAndObjects import FunctionData
from LOTlib3.DataAndObjects import Obj
import os
from multiset import *
import pandas as pd


def load(data_dir):

    data = [] # A list of FunctionData objects (what LOTlib uses)
    colors = {"red": 0, "blue": 1, "green": 2, "yellow": 3}

    # Load all experiments in data directory
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r'))

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
Enumerate all contexts of objects. Used to get weights of possible
quantifier meaning.
"""
def get_num_contexts(data_dir):
    # Load all experiments in data directory
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r'))

        # Get number of objects by searching for "obj" in col names
        num_objects = 0
        for col_name in df.columns:
            if "obj" in col_name:
                num_objects += 1
        
        # Get number of colors by searching unique names in "target" col
        num_colors = 0
        colors = set()
        df = df.target.dropna()
        for color in df.unique():
            colors.add(color)
        num_colors = len(colors)

        # Return number of contexts by simple combinatorics
        return (num_colors)**(num_objects)