# -----------------------------------------------------------
# Define some new hypotheses not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis


class HypothesisA(LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    def compute_single_likelihood(self, datum):

        if self(*datum.input) == datum.output:
            return log((1.0-datum.alpha)/100. + datum.alpha)
        else:
            return log((1.0-datum.alpha)/100.)

    def weight(self, data):
        print()