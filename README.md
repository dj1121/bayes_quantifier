# Semantic Universals in Bayesian Learning of Quantifiers
This repository contains code for experiments in the following paper:

-To come-

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- [multiset](https://pypi.org/project/multiset/)
- [LOTLib3](https://github.com/piantado/LOTlib3) (IMPORTANT: Either specify a path to your LOTLib3 folder or place it in the src folder)
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

## Running an Experiment

To test out the program for yourself on some sample data (monotone only) with default parameters, you can simply run (from inside the src folder):

`python run_experiment.py monotone`

To run a custom experiment, the program can be specified on the command line as follows (from inside the src folder):

`python run_experiment.py [exp_type] -data_dir [data_dir] -out [out] -g_type [g_type] -h_type [h_type] -sample_steps [sample_steps] -alpha [alpha]`

The parameters serve the following functions:

- exp_type (REQUIRED): String specifying the experiment type (monotone, non-convex, non-monotone, etc.)
- data_dir (default = ./../sample_data/monotone/): String specifying where training data is located
- out (default = ./../model_out/): String specifying where model performance results will be stored
- g_type (default = quant): What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py
- h_type (default = A): What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py
- sample_steps (default = 5000): How many steps to run the metropolis-hasting sampler
- alpha (default = 0.99): Assumed noisiness of data (min = 1.0)

NOTE: The data directory (data_dir) only points to where your experimental data files are located. Experimental data MUST be further divided into folders based
upon experiment. The exp_type argument is then used to find the correct folder of data inside the data_dir. In sum, your data file structure, given multiple experiment types,
should look like this:

```
data_dir
|-- monotone
|      -- mono_1.csv
|      -- mono_2.csv
|      -- ....csv
|-- non_monotone
|      -- non_mono_1.csv
|      -- non_mono_2.csv
|      -- ....csv
|-- non_convex
|      -- non_convex_1.csv
|      -- non_convex_2.csv
|      -- ....csv
|-- ...
|      -- ....csv
|      -- ....csv
|      -- ....csv
```


## Making Hypotheses
Hypothesis are specified in hypotheses.py. Each hypothesis must have its own class which specifies its method of display and
how the likelihood is calculated over a single data point. For example, by default, the code provided uses a user-defined hypothesis
called HypothesisA, which inherits from LOTHypothesis:

```
class HypothesisA(LOTHypothesis):
    """
    A hypothesis type which assumes two sets and a simple likelihood function
    as seen in Goodman et al. 2010.
    """

    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, display="lambda A, B: %s", **kwargs)
        
    def __call__(self, *args):
        try:
            return LOTHypothesis.__call__(self, *args)
        except ZeroDivisionError:
            return float("nan")

    def compute_single_likelihood(self, datum):
        return log(datum.alpha if self(*datum.input) == datum.output else 1.0 - datum.alpha)
```

Should you desire, you can make a new hypothesis (for example, HypothesisB) by writing a similar class in the hypotheses.py file and add a clause such as:

`if h_type == "B":
        return HypothesisB(grammar=grammar)`

to the create_hypothesis function. For more information, refer to the [LOTLib3 documentation](https://github.com/piantado/LOTlib3/blob/master/Documentation/Tutorial.md).

## Making Grammars
Grammars can be created in grammars.py in the create_grammar function. Simply add to the existing if/then structure and define a PCFG-like grammar as shown below. By default, this code uses the following grammar, called "quant":

```
if g_type == "quant":
        grammar = Grammar(start='BOOL')

        grammar.add_rule('BOOL', 'issubset_', ['SET', 'SET'], 1.0)
        grammar.add_rule('BOOL', 'issuper_', ['SET', 'SET'], 1.0)
        grammar.add_rule('BOOL', 'equal_', ['SET', 'SET'], 1.0)
        grammar.add_rule('BOOL', 'lt', ['NUM', 'NUM'], 1.0)
        grammar.add_rule('BOOL', 'gt', ['NUM', 'NUM'], 1.0)
        grammar.add_rule('BOOL', 'num_eq', ['NUM', 'NUM'], 1.0)

        grammar.add_rule('NUM', 'cardinality_', ['SET'], 1.0)
        for n in range(0,10):
            grammar.add_rule('NUM', str(n), None, 1.0)

        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'A', None, 5)
        grammar.add_rule('SET', 'B', None, 5)
        
        return grammar
```

This grammar assumes hypotheses will be defined over two sets and applies uniform probability weight to all productions. Creating new grammars allows for easy experimentation over possible priors. For more information on grammars, refer to [LOTLib3 documentation](https://github.com/piantado/LOTlib3/blob/master/Documentation/Tutorial.md)

## Analyzing Results
By default, this program outputs .csv results files and three learning curves indicating model/human performance. Since human data is confidential, sample human data is provided. The model learns from the same experimental contexts that humans see. Output files are stored by default in results/exp_id/, a folder which is created in the main directory of the program.

Output files are named according to the date, time, and result type. For example, if a monotone quantifier learning experiment was run on September 14th, 2020 at 10:53:14 and the results file names woudld start with:

`20200914-105314_monotone_`

### _acc Files
Files ending in `_acc` store the accuracy results of a learning model. Each line shows the top hypothesis (most probable) per amount of data seen (line 1 = one data point, line 30 = thirty data points, etc.) and the accuracy of running that hypothesis over all the data currently seen. Since there are as many models as there are humans, there may be multiple `_acc` files like:
```
20200914-105314_monotone_acc_1.csv
20200914-105314_monotone_acc_2.csv
...
```

Some example lines:

```
hypothesis|acc
lambda A, B: issubset_(B, A)|1.0
lambda A, B: issubset_(A, A)|1.0
```

This means that after seeing one data point (first line), the model guesses that the concept is `lambda A, B: issubset_(B, A)` and after running this hypothesis over all the data points, it evaluated to true on all. Thus, the accuracy is 1.0.



### _prob Files
Files ending in `_prob` store the (log) posterior probabilities of the learning model. Each line also shows the top hypothesis (most probable) per amount of data seen and its posterior probability. Since there are as many models as there are humans, there may be multiple `_prob` files like:
```
20200914-105314_monotone_prob_1.csv
20200914-105314_monotone_prob_2.csv
...
``` 
Example lines:
```
hypothesis|post_prob
lambda A, B: issuper_(A, B)|-3.7128326951364294
lambda A, B: equal_(B, B)|-3.7228830309899306
```

Naturally, we would expect these (log) probabilities to decrease over time as we converge to better hypotheses by having seen more data points.

### Learning Curves
In the results folder, by default for each experiment, one can also find the following learning curves:
- <b>Human Learning Curve:</b> A plot of average human accuracy over # contexts seen with an error band of one standard deviation.

- <b>Model Learning Curve:</b> A plot of the concepts with (log) top posterior probability at each amount of data seen.

- <b>Human/Model Learning Curve:</b> A plot of average human accuracy and average model accuracy over each amount of data seen.