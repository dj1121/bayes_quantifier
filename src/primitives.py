# -----------------------------------------------------------
# Define some new primitives not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Eval import primitive
from multiset import *

@primitive
def card_gt(x,y):
    return x > y

@primitive
def card_gteq(x,y):
    return x >= y

@primitive
def card_lt(x,y):
    return x < y

@primitive
def card_lteq(x,y):
    return x <= y

@primitive
def card_eq(x, y):
    return x == y

# Debugging purposes
@primitive
def intersect_card_gteq_3(x, y):
    return len(x.intersection(y)) >= 3