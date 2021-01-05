# -----------------------------------------------------------
# Define some new hypotheses not included with LOTLib initially
#
# 2020 Devin Johnson, University of Washington Linguistics
# Email: dj1121@uw.edu
# -----------------------------------------------------------

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib3.DataAndObjects import FunctionData
from LOTlib3.Miscellaneous import nicelog as log
from os import path

class HypothesisA(LOTHypothesis):
    """
    A hypothesis type which assumes two sets and a simple likelihood function
    as seen in Goodman et al. 2010. Also incporates degrees of monotonicity 
    and conservativity.
    """

    # Class attributes
    lam_1 = 0.0
    lam_2 = 0.0
    all_contexts = None

    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)

        # These attributes will be common to all hypotheses sampled in experiment (are passed)
        # This init is only called on h0 (the starting hypothesis)
        self.lam_1 = kwargs.get('lam_1', 0.0)
        self.lam_2 = kwargs.get('lam_2', 0.0)
        self.all_contexts = kwargs.get('all_contexts', None)
        
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
                  'cons_t': 0,
                  'cons_f': 0,
                  'M_t_sub_t': 0,
                  'M_t_sub_f': 0,
                  'M_f_sub_t': 0,
                  'M_f_sub_f': 0,
                  'M_t_super_t': 0,
                  'M_t_super_f': 0,
                  'M_f_super_t': 0,
                  'M_f_super_f': 0,
                  'M_t_cons_t': 0,
                  'M_t_cons_f': 0,
                  'M_f_cons_t': 0,
                  'M_f_cons_f': 0 
                  }       

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
            
            # Cons T/F for curr context
            curr_cons_truth = None
            if self.cons_q_m(context):
                counts['cons_t'] += 1
                curr_cons_truth = True
            else:
                counts['cons_f'] += 1
                curr_cons_truth = False

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

            # TT, TF, FT, FF for curr and cons model
            if curr_truth and curr_cons_truth:
                counts['M_t_cons_t'] += 1
            elif curr_truth and not curr_cons_truth:
                counts['M_t_cons_f'] += 1
            elif not curr_truth and curr_cons_truth:
                counts['M_f_cons_t'] += 1
            elif not curr_truth and not curr_cons_truth:
                counts['M_f_cons_f'] += 1
            
        probs = {'M_t': float(counts['M_t']/len(self.all_contexts)),
                  'M_f': float(counts['M_f']/len(self.all_contexts)),
                  'sub_t': float(counts['sub_t']/len(self.all_contexts)),
                  'sub_f': float(counts['sub_f']/len(self.all_contexts)),
                  'super_t': float(counts['super_t']/len(self.all_contexts)),
                  'super_f': float(counts['super_f']/len(self.all_contexts)),
                  'cons_t': float(counts['cons_t']/len(self.all_contexts)),
                  'cons_f': float(counts['cons_f']/len(self.all_contexts)),
                  'M_t_sub_t': float(counts['M_t_sub_t']/len(self.all_contexts)),
                  'M_t_sub_f': float(counts['M_t_sub_f']/len(self.all_contexts)),
                  'M_f_sub_t': float(counts['M_f_sub_t']/len(self.all_contexts)),
                  'M_f_sub_f': float(counts['M_f_sub_f']/len(self.all_contexts)),
                  'M_t_super_t': float(counts['M_t_super_t']/len(self.all_contexts)),
                  'M_t_super_f': float(counts['M_t_super_f']/len(self.all_contexts)),
                  'M_f_super_t': float(counts['M_f_super_t']/len(self.all_contexts)),
                  'M_f_super_f': float(counts['M_f_super_f']/len(self.all_contexts)),
                  'M_t_cons_t': float(counts['M_t_cons_t']/len(self.all_contexts)),
                  'M_t_cons_f': float(counts['M_t_cons_f']/len(self.all_contexts)),
                  'M_f_cons_t': float(counts['M_f_cons_t']/len(self.all_contexts)),
                  'M_f_cons_f': float(counts['M_f_cons_f']/len(self.all_contexts))}
        
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
            curr_B_set = context.input[1]
            m_B_set = m.input[1]
            if m_B_set.issubset(curr_B_set) and self.eval_q_m(context):
                return True
        return False

    def sub_q_m(self, m):
        """
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
            curr_B_set = context.input[1]
            m_B_set = m.input[1]
            if curr_B_set.issubset(m_B_set) and self.eval_q_m(context):
                return True
        return False

    def cons_q_m(self, m):
        """
        Find if the hypothesis evaluates to true its conservation, where B' = A \cap B
        
        Parameters:
            - self
            - m (List of multisets): A given context (data input)

        Returns:
            - True if there exists a conservation model m' where the hypothesis evaluates to true    
        """
        # A' = A and B' = A \cap B
        conservation_model = FunctionData(input=[m.input[0], m.input[0].intersection(m.input[1])], output=None)
        
        return self.eval_q_m(conservation_model)

    def compute_prior(self):
        """
        Overriden prior computation to allow for degrees of monotonicity and conservativity.
        NOTE: The super function computes a log probability. Thus, we can add the degrees.
        """

        # Add these attributes to value attribute of hypothesis (so they are unique to each sampled hypothesis)
        if self.value is not None and (self.lam_1 > 0 or self.lam_2 > 0):

            setattr(self.value, 'probs', self.calc_degree_probs())
            
            if self.lam_1 > 0.0:
                setattr(self.value, 'degree_monotonicity', self.compute_degree_monotonicity())
            else:
                setattr(self.value, 'degree_monotonicity', 0.0)

            if self.lam_2 > 0.0:
                setattr(self.value, 'degree_conservativity', self.compute_degree_conservativity())
            else:
                setattr(self.value, 'degree_conservativity', 0.0)
                
            # Don't let these values get copied when sampling hypotheses
            self.value.NoCopy.add('probs')
            self.value.NoCopy.add('degree_monotonicity')
            self.value.NoCopy.add('degree_conservativity')


        # Fix this so that higher degree (0.9999) = bigger negative
        return super().compute_prior() + (self.lam_1 * log(self.value.degree_monotonicity)) + (self.lam_2 * log(self.value.degree_conservativity))

    def compute_degree_monotonicity(self):
        """
        Compute degree of monotonicity, similar to that seen in Posdijk
        Takes the max of the upward monotonicity measure and downward
        """
        
        k = 0.00001

        # Get H(1Q)
        h_1_q = -((self.value.probs['M_t'] * log(self.value.probs['M_t'])) + (self.value.probs['M_f'] * log(self.value.probs['M_f'])))

        if h_1_q == 0.0:
            return 1.0

        # Get H(1Q | 1Q<)
        h_1_q_sub = -((self.value.probs['M_t_sub_t'] * log(self.value.probs['M_t_sub_t'] / (self.value.probs['sub_t'] + k))) +\
                    (self.value.probs['M_t_sub_f'] * log(self.value.probs['M_t_sub_f'] / (self.value.probs['sub_f'] + k))) +\
                    (self.value.probs['M_f_sub_t'] * log(self.value.probs['M_f_sub_t'] / (self.value.probs['sub_t'] + k))) +\
                    (self.value.probs['M_f_sub_f'] * log(self.value.probs['M_f_sub_f'] / (self.value.probs['sub_f'] + k))))

        # Get H(1Q | 1Q>)
        h_1_q_super = -((self.value.probs['M_t_super_t'] * log(self.value.probs['M_t_super_t'] / (self.value.probs['super_t'] + k) )) +\
                    (self.value.probs['M_t_super_f'] * log(self.value.probs['M_t_super_f'] / (self.value.probs['super_f'] + k))) +\
                    (self.value.probs['M_f_super_t'] * log(self.value.probs['M_f_super_t'] / (self.value.probs['super_t'] + k))) +\
                    (self.value.probs['M_f_super_f'] * log(self.value.probs['M_f_super_f'] / (self.value.probs['super_f'] + k))))
        
        up_degree = float(1 - (h_1_q_sub / h_1_q))
        down_degree = float(1 - (h_1_q_super / h_1_q))
    
        return max(up_degree, down_degree)

    def compute_degree_conservativity(self):
        """
        Compute degree of conservativity, evaluate truth in <M, A, A \cap B>
        i.e. B' = A \cap B
        """
        
        k = 0.00001

        # Get H(1Q)
        h_1_q = -((self.value.probs['M_t'] * log(self.value.probs['M_t'])) + (self.value.probs['M_f'] * log(self.value.probs['M_f'])))

        if h_1_q == 0:
            return 1

        # Get H(1Q | 1Q con)
        h_1_q_cons = -((self.value.probs['M_t_cons_t'] * log(self.value.probs['M_t_cons_t'] / (self.value.probs['cons_t'] + k))) +\
                    (self.value.probs['M_t_cons_f'] * log(self.value.probs['M_t_cons_f'] / (self.value.probs['cons_f'] + k))) +\
                    (self.value.probs['M_f_cons_t'] * log(self.value.probs['M_f_cons_t'] / (self.value.probs['cons_t'] + k))) +\
                    (self.value.probs['M_f_cons_f'] * log(self.value.probs['M_f_cons_f'] / (self.value.probs['cons_f'] + k))))

        return float(1 - (h_1_q_cons / h_1_q))

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
        - lam_2 (float): Lambda value [0,1] to give weight to degree of conservativity
        - all_contexts (float): For measuring degrees

    Returns:
        - (LOTLib3.Hypothesis): A hypothesis of the type specified with the grammar specified.
        - None: If the hypothesis specified does not exist yet (you must create it).
    """
    if h_type == "A":
        return HypothesisA(grammar=grammar, lam_1=lam_1, lam_2=lam_2, all_contexts=all_contexts)
    else:
        raise Exception("There exists no h_type \'" + h_type + '\'. Check hypotheses.py for types of hypotheses to use.')

# def log(val):
#     """
#     Returns 0 if value is zero, otherwise returns log of value 
#     """
#     if val == 0:
#         return -float('inf')
#     return log(val,2)