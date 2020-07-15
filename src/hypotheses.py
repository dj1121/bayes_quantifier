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
        print(self.w_mi)
        
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    def compute_single_likelihood(self, datum):
        return (datum.alpha * self.w_mi) + ((1-datum.alpha) * self.w_mi)

    # weight of m_i (hypothesis) 
    def weight(self):
        # Get probability of hypothesis m_i being true in any context
        n_true = 0
        contexts = data_handling.get_contexts(self.data_dir)
        for datum in contexts:
            if self(*datum.input) == datum.output: # Evaluate hypothesis on this context
                n_true += 1
        p_true = n_true/n_contexts
        return 1/(0.1 + p_true)

        


def create_hypothesis(h_type, grammar, data_dir):
    if h_type == "A":
        return HypothesisA(grammar=grammar, data_dir=data_dir)
    else:
        raise Exception("There exists no h_type \'" + h_type + '\'. Check hypotheses.py for types of hypotheses to use.')