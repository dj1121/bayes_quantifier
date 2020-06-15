# Functions for loading and working with experimental data.

from LOTlib3.DataAndObjects import FunctionData
import csv
from multiset import *
import pandas as pd

# def load(f):
#     colors = {'red': 0, 'blue': 1, 'green': 2, 'yellow': 3}
#     ans = {'c': True, 'm': False}

#     # Import (training) data here and convert to numbered
#     data = []
#     with open('./data/monotone/12h05.39.006.csv') as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             x = Multiset([])
#             y = Multiset([])
#             out = None
#             if row[37] in colors: # col 37 is "obj1"
#                 for col in range(37,43):
#                     curr_obj = colors[row[col]]
#                     if len(x) == 0 and len(y) == 0:
#                         x.add(curr_obj)
#                     else:
#                         if curr_obj in x:
#                             x.add(curr_obj)
#                         else:
#                             y.add(curr_obj)
#                 out = ans[row[43]

#             if len(x) > 0 and len(y) > 0 and out != None:  
#                 data.append(FunctionData(input = [x,y], output=out, alpha=0.95)) # Put into format needed for LOTLib
    
#     return data

def enum_contexts(data):
    print()