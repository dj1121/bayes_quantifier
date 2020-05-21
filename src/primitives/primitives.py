from LOTlib3.Eval import primitive

# Define some new primitives not included with LOTLib initially
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