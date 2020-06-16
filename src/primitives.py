# -----------------------------------------------------------
# Define some new primitives not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Eval import primitive

@primitive
def issuper_(A, B):
    return A.issuperset(B)

@primitive
def gt(x, y):
    return x > y

@primitive
def lt(x,y):
    return x < y


@primitive
def num_eq(x, y):
    return x == y