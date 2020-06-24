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
            obj_set = Multiset()
            label = None
            for col in df:
                if "obj" in col:
                    obj_set.add(colors[row[col]])
                else:
                    # If "corrAns" column is c, output = true, else = false
                    label = (row[col] == "c")
            
            # Add to data
            data.append(FunctionData(input=[obj_set], output=label, alpha=0.99))

    return data

"""
Enumerate all contexts of objects. Used to get weights of possible
quantifier meaning.
"""
def enum_contexts(data):
    print()