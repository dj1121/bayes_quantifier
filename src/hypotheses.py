# -----------------------------------------------------------
# Define some new hypotheses not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from math import log
import data_handling


class HypothesisA(LOTHypothesis):

    w_mi = None

    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)
        self.w_mi = self.weight()
        
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    # TODO: Fix
    def compute_single_likelihood(self, datum):
        print("weight", self.w_mi)
        return (datum.alpha * self.w_mi) + ((1-datum.alpha) * self.w_mi)

    # weight of m_i (hypothesis) 
    def weight(self):
        # Get probability of hypothesis m_i being true in any context
        n_true = 0
        contexts = data_handling.get_contexts(self.data_dir, self.n_colors_context)
        for datum in contexts:
            if self(*datum.input): # Evaluate hypothesis on this context
                n_true += 1
        p_true = n_true/len(contexts)
        return 1/(0.1 + p_true)

        


def create_hypothesis(h_type, grammar, data_dir, n_colors_context):
    if h_type == "A":
        return HypothesisA(grammar=grammar, data_dir=data_dir, n_colors_context=n_colors_context)
    else:
        raise Exception("There exists no h_type \'" + h_type + '\'. Check hypotheses.py for types of hypotheses to use.')