# -----------------------------------------------------------
# Functions for loading and working with experimental/LOT data.
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.DataAndObjects import FunctionData
from multiset import *
import os
import pandas as pd

def load(data_dir):

    data = [] # A list of FunctionData objects (what LOTlib uses)

    # Load all experiments in data directory
    for f_name in os.listdir(data_dir):
        path = data_dir + f_name
        df = pd.read_csv(open(path, 'r'))

        # Get relevant columns (objs and labels)
        df = df.loc[:, 'obj1':'corrAns'].dropna()
        print(df)

    
        # Get output label column (all rows)
            
            

    

        
    




    # return [ FunctionData(input=[Obj(shape='square', color='red')], output=True, alpha=0.99) ]

"""
Enumerate all contexts of objects. Used to get weights of possible
quantifier meaning.
"""
def enum_contexts(data):
    print()