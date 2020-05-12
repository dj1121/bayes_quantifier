from LOTlib3.Eval import primitive

# Define some new primitives not included with LOTLib initially
@primitive
def cardinalityx_(A, x):
    return len(A) == x

@primitive
def issuper_(A, B):
    return A.issuperset(B)