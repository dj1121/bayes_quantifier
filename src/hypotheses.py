# -----------------------------------------------------------
# Define some new hypotheses not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from math import log
from os import path

class HypothesisA(LOTHypothesis):
    """
    A hypothesis type which assumes two sets and a simple likelihood function
    as seen in Goodman et al. 2010. Also incporates degrees of monotonicity 
    and convexity.
    """

    # Class attributes
    degree_monotonicity = 0
    degree_convexity = 0
    lam_1 = 0
    lam_2 = 0
    all_contexts = None
    probs = {}

    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)

        self.lam_1 = kwargs.get('lam_1', 0.0)
        self.lam_2 = kwargs.get('lam_2', 0.0)

        if self.lam_1 > 0 or self.lam_2 > 0:
            self.all_contexts = kwargs.get('all_contexts', None) # Load in the contexts in a FunctionData/Multiset format useful for finding submodels in degree calculations
            self.probs = self.calc_degree_probs() # Calculate relevant probabilities for degrees of universality

        if self.lam_1 > 0:
            self.degree_monotonicity = self.compute_degree_monotonicity()
        
        if self.lam_2 > 0:
            self.degree_convexity = self.compute_degree_monotonicity()
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    def compute_single_likelihood(self, datum):
        return log(datum.alpha if self(*datum.input) == datum.output else 1.0 - datum.alpha)

    def calc_degree_probs(self):
        """
        Evaluate the hypothesis on contexts to get probabilities
            - p(1Q = True) = probability that evals to true over all contexts
            - p(1Q< = True) = probability that there exists a submodel which evals to true over all contexts
            - p(1Q> = True) = probability that there exists a supermodel which evals to true over all contexts
            - p(1Q = True, 1Q< = True) = prob that both true in current model and exists a submodel
            - etc... 

        Parameters:
            - self

        Returns:
            - probs (dict): Dictionary of relevant probabilities

        """

        # Get counts of all situations, i.e. number times true in current model, not true in submodels, etc.
        counts = {'M_t': 0,
                  'M_f': 0,
                  'sub_t': 0,
                  'sub_f': 0,
                  'super_t': 0,
                  'super_f': 0,
                  'M_t_sub_t': 0,
                  'M_t_sub_f': 0,
                  'M_f_sub_t': 0,
                  'M_f_sub_f': 0,
                  'M_t_super_t': 0,
                  'M_t_super_f': 0,
                  'M_f_super_t': 0,
                  'M_f_super_f': 0}       

        # Iterate over all contexts get counts
        for context in self.all_contexts:
            # T/F for curr context
            curr_truth = None
            if self.eval_q_m(context):
                counts['M_t'] += 1
                curr_truth = True
            else:
                counts['M_f'] += 1
                curr_truth = False
            
            # Sub T/F for curr context
            curr_sub_truth = None
            if self.sub_q_m(context):
                counts['sub_t'] += 1
                curr_sub_truth = True
            else:
                counts['sub_f'] += 1
                curr_sub_truth = False

            # Super T/F for curr context
            curr_super_truth = None
            if self.super_q_m(context):
                counts['super_t'] += 1
                curr_super_truth = True
            else:
                counts['super_f'] += 1
                curr_super_truth = False

            # TT, TF, FT, FF for curr and submodels
            if curr_truth and curr_sub_truth:
                counts['M_t_sub_t'] += 1
            elif curr_truth and not curr_sub_truth:
                counts['M_t_sub_f'] += 1
            elif not curr_truth and curr_sub_truth:
                counts['M_f_sub_t'] += 1
            elif not curr_truth and not curr_sub_truth:
                counts['M_f_sub_f'] += 1
            
            # TT, TF, FT, FF for curr and supermodels
            if curr_truth and curr_super_truth:
                counts['M_t_super_t'] += 1
            elif curr_truth and not curr_super_truth:
                counts['M_t_super_f'] += 1
            elif not curr_truth and curr_super_truth:
                counts['M_f_super_t'] += 1
            elif not curr_truth and not curr_super_truth:
                counts['M_f_super_f'] += 1
            
        probs = {'M_t': float(counts['M_t']/len(self.all_contexts)),
                  'M_f': float(counts['M_f']/len(self.all_contexts)),
                  'sub_t': float(counts['sub_t']/len(self.all_contexts)),
                  'sub_f': float(counts['sub_t']/len(self.all_contexts)),
                  'super_t': float(counts['super_t']/len(self.all_contexts)),
                  'super_f': float(counts['super_f']/len(self.all_contexts)),
                  'M_t_sub_t': float(counts['M_t_sub_t']/len(self.all_contexts)),
                  'M_t_sub_f': float(counts['M_t_sub_f']/len(self.all_contexts)),
                  'M_f_sub_t': float(counts['M_f_sub_t']/len(self.all_contexts)),
                  'M_f_sub_f': float(counts['M_f_sub_f']/len(self.all_contexts)),
                  'M_t_super_t': float(counts['M_t_super_t']/len(self.all_contexts)),
                  'M_t_super_f': float(counts['M_t_super_f']/len(self.all_contexts)),
                  'M_f_super_t': float(counts['M_f_super_t']/len(self.all_contexts)),
                  'M_f_super_f': float(counts['M_f_super_f']/len(self.all_contexts))}
        
        return probs

    def eval_q_m(self, m):
        """
        Evaluate the hypothesis on a given data point. That is, get its truth value on a
        given context. In theoretical terms: 1Q(M) where M is the context.

        Parameters:
            - self
            - m (List of multisets): A given context (data input)

        Returns:
            - The truth value of the hypothesis evaluated on this model (context) m

        """
        return self(*m.input)
    
    def super_q_m(self, m):
        """
        TODO: Check if subsets should be \subseteq??
        Find if the hypothesis evaluates to true in any of the supermodels of the given model (context) m.
        A supermodel is defined to be two sets A'and B' such that A = A' and B \subseteq B'
        
        Parameters:
            - self
            - m (List of multisets): A given context (data input)

        Returns:
            - True if there exists a supermodel m' where the hypothesis evaluates to true    
        """
        # Iterate over models
        for context in self.all_contexts:
            # if context == m: # Skip itself?
            #     continue
            curr_B_set = context.input[1]
            m_B_set = m.input[1]
            if m_B_set.issubset(curr_B_set) and self.eval_q_m(context):
                return True
        return False

    def sub_q_m(self, m):
        """
        TODO: Check if subsets should be \subseteq??
        Find if the hypothesis evaluates to true in any of the submodels of the given model (context) m.
        A submodel is defined to be two sets A'and B' such that A = A' and B' \subseteq B
        
        Parameters:
            - self
            - m (List of multisets): A given context (data input)

        Returns:
            - True if there exists a submodel m' where the hypothesis evaluates to true    
        """
        # Iterate over models
        for context in self.all_contexts:
            # if context == m: # Skip itself
            #     continue
            curr_B_set = context.input[1]
            m_B_set = m.input[1]
            if curr_B_set.issubset(m_B_set) and self.eval_q_m(context):
                return True
        return False

    def compute_prior(self):
        """
        Overriden prior computation to allow for degrees of monotonicity and convexity.
        """
        return super().compute_prior() + (self.lam_1 * self.degree_monotonicity) + (self.lam_2 * self.degree_monotonicity)

    def compute_degree_monotonicity(self):
        """
        Compute degree of monotonicity, similar to that seen in Posdijk
        Takes an average of the upward monotonicity measure and downward
        """

        def smooth_log(val):
            """
            This is the nested function to deal with log(0) when a probability is = 0
            """
            if val == 0:
                return 0
            return log(val)

        # Get H(1Q)
        h_1_q = (self.probs['M_t'] * smooth_log(self.probs['M_t'])) + (self.probs['M_f'] * log(self.probs['M_f']))

        # Get H(1Q | 1Q<)
        h_1_q_sub = (self.probs['M_t_sub_t'] * smooth_log(self.probs['M_t_sub_t']/self.probs['sub_t'])) +\
                    (self.probs['M_t_sub_f'] * smooth_log(self.probs['M_t_sub_f']/self.probs['sub_f'])) +\
                    (self.probs['M_f_sub_t'] * smooth_log(self.probs['M_f_sub_t']/self.probs['sub_t'])) +\
                    (self.probs['M_f_sub_f'] * smooth_log(self.probs['M_f_sub_f']/self.probs['sub_f']))

        # Get H(1Q | 1Q>)
        h_1_q_super = (self.probs['M_t_super_t'] * smooth_log(self.probs['M_t_super_t']/self.probs['super_t'])) +\
                    (self.probs['M_t_super_f'] * smooth_log(self.probs['M_t_super_f']/self.probs['super_f'])) +\
                    (self.probs['M_f_super_t'] * smooth_log(self.probs['M_f_super_t']/self.probs['super_t'])) +\
                    (self.probs['M_f_super_f'] * smooth_log(self.probs['M_f_super_f']/self.probs['super_f']))
        
        up_degree = float((1-h_1_q_sub) / h_1_q)
        down_degree = float((1-h_1_q_super) / h_1_q)

        return (up_degree + down_degree) / 2

    def compute_degree_convexity(self):
        """
        Compute degree of convexity
        """
        return 0     


def create_hypothesis(h_type, grammar, lam_1, lam_2, all_contexts):
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
        - lam_1 (float): Lambda value [0,1] to give weight to degree of monotonicity
        - lam_2 (float): Lambda value [0,1] to give weight to degree of convexity
        - all_contexts (float): For measuring degrees

    Returns:
        - (LOTLib3.Hypothesis): A hypothesis of the type specified with the grammar specified.
        - None: If the hypothesis specified does not exist yet (you must create it).
    """
    if h_type == "A":
        return HypothesisA(grammar=grammar, lam_1=lam_1, lam_2=lam_2, all_contexts=all_contexts)
    else:
        raise Exception("There exists no h_type \'" + h_type + '\'. Check hypotheses.py for types of hypotheses to use.')