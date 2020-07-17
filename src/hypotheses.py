# -----------------------------------------------------------
# Define some new hypotheses not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from math import log


class HypothesisA(LOTHypothesis):

    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    # TODO: Fix to include w_t and w_not_t
    def compute_single_likelihood(self, datum):
        w_mi = self.weight(self.contexts)
        return (datum.alpha * w_mi) + ((1-datum.alpha) * w_mi)

    # weight of m_i (hypothesis) 
    def weight(self, contexts):
        # Get probability of hypothesis m_i being true in any context
        n_true = 0
        for datum in contexts:
            if self(*datum.input): # Evaluate hypothesis on this context
                n_true += 1
        p_true = n_true/len(contexts)
        return 1/(0.1 + p_true)


def create_hypothesis(h_type, grammar, contexts):
    if h_type == "A":
        return HypothesisA(grammar=grammar, contexts=contexts)
    else:
        raise Exception("There exists no h_type \'" + h_type + '\'. Check hypotheses.py for types of hypotheses to use.')