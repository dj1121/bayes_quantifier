# Semantic Universals in Bayesian Learning of Quantifiers
This repository contains code for experiments in the following paper:

-To come-

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- [multiset](https://pypi.org/project/multiset/)
- [LOTLib3](https://github.com/piantado/LOTlib3)
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

## Running an Experiment

To test out the program for yourself on some sample data with default parameters, you can simply run (from inside the src folder):

`python run_experiment.py`

To run a custom experiment, the program can be specified on the command line as follows (from inside the src folder):

`python run_experiment.py [data_dir] [out] [g_type] [h_type] [sample_steps] [alpha]`

The parameters serve the following functions:

- data_dir (default = ./../sample_data/monotone/): String specifying where training data is located
- out (default = ./../model_out/): String specifying where model performance results will be stored
- g_type (default = quant): What type of grammar to use, defined in grammars.py {quant,...}. Define your own in grammars.py
- h_type (default = A): What type of hypothesis to use, defined in hypotheses.py {A,B,...}. Define your own in hypotheses.py
- sample_steps (default = 5000): How many steps to run the metropolis-hasting sampler
- alpha (default = 0.99): Assumed noisiness of data (min = 1.0)


## Making Hypotheses
-To come-

## Making Grammars
-To come-

## Analyzing Results
-To come-