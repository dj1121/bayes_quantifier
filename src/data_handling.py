# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.DataAndObjects import FunctionData
from LOTlib3.DataAndObjects import Obj
from itertools import combinations_with_replacement
from itertools import combinations
import os
from collections import Counter
from multiset import *
import pandas as pd


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
Enumerate all contexts of objects. Used to get weights of possible
quantifier meaning.

- n_colors: Number of different colors allowed in a context

"""
def get_contexts(data_dir, n_colors_context):

    objs = set()
    colors = set()
    color_to_int = {"red": 0, "blue": 1, "green": 2, "yellow": 3}

    # Load all experiments in data directory
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r'))

        # Get number of objects by searching for "obj" in column names
        for column_name in df.columns:
            if "obj" in column_name:
                objs.add(column_name)
        
        # Get number of colors by searching unique names in "target" col
        df = df.target.dropna()
        for color in df.unique():
            colors.add(color_to_int[color])


    # Generate possible contexts
    contexts = []

    # Get possible combos of colors possible in any context
    colors = list(colors)
    color_combos = ""
    for key in color_to_int:
        color_combos += str(color_to_int[key])
    color_combos = list(combinations(color_combos, n_colors_context))
    
    # Generate all possible contexts given color combo i, add those to total list
    for i in color_combos:
        i = "".join(list(i))
        c = list(combinations_with_replacement(i, len(objs)))
        contexts += c

    # Remove duplicates and convert each context to a multiset then to FunctionData
    contexts = list(set(contexts))
    for i in range(0, len(contexts)):
        contexts[i] = list(contexts[i])
        set_a = Multiset()
        set_b = Multiset()
        for item in contexts[i]:
            if len(set_a) == 0 and len(set_b) == 0:
                set_a.add(item)
            elif item not in set_a:
                set_b.add(item)
            else:
                set_a.add(item)
        contexts[i] = FunctionData(input=[set_a, set_b], output=None)

    return contexts