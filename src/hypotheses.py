# -----------------------------------------------------------
# Define some new hypotheses not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from math import log

class HypothesisA(LOTHypothesis):
    """
    A hypothesis type which assumes two sets and a simple likelihood function
    as seen in Goodman et al. 2010.
    """

    # Class attributes
    degree_monotonicity = 0
    degree_convexity = 0
    lam_1 = 0
    lam_2 = 0
    data = None

    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)

        self.lam_1 = kwargs.get('lam_1', 0.0)
        self.lam_2 = kwargs.get('lam_2', 0.0)

        # Only compute degrees if lambda weights present (otherwise it's a waste of resources)
        if self.lam1 > 0:
            self.degree_monotonicity = self.compute_degree_monotonicity()
        
        if self.lam2 > 0:
            self.degree_convexity = self.compute_degree_monotonicity()
        
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    def compute_single_likelihood(self, datum):
        return log(datum.alpha if self(*datum.input) == datum.output else 1.0 - datum.alpha)

    def eval(self, datum):
        """
        See if the hypothesis evaluates the data point to the correct label
        (logically true when should be true, logically false when should be false)
        """
        return self(*datum.input) == datum.output
    
    def compute_prior(self):
        """
        Overriden prior computation to allow for degrees of monotonicity and convexity.
        """
        return super().compute_prior() + (self.lam_1 * self.degree_monotonicity) + (self.lam_2 * self.degree_monotonicity)

    def compute_degree_monotonicity(self):
        """
        Compute degree of monotonicity, similar to that seen in Carcassi et al. 2019
        """
        return 0

    def compute_degree_convexity(self):
        """
        Compute degree of convexity
        """
        return 0

def create_hypothesis(h_type, grammar, data, lam):
    """
    Uses a grammar and a specified hypothesis type to create an object
    of the desired hypothesis class. This is used to be able to return
    a hypothesis of a specific user-designed type as seen in the classes defined
    in this file.

    Parameters:
        - h_type (str): Hypothesis type. To create more types, simply create new classes in this file
        and add capability to this function to return a hypothesis of that type.
        - grammar (LOTLib3.Grammar): A grammar with which possible hypotheses of the type passed in will
        be generated
        - data (list): Data to pass in in order to compute degree of monotonicity
        - lam (float): Lambda value [0,1] to give weight to degree of monotonicity

    Returns:
        - (LOTLib3.Hypothesis): A hypothesis of the type specified with the grammar specified.
        - None: If the hypothesis specified does not exist yet (you must create it).
    """
    if h_type == "A":
        return HypothesisA(grammar=grammar, data=data, lam=lam)
    else:
        raise Exception("There exists no h_type \'" + h_type + '\'. Check hypotheses.py for types of hypotheses to use.')