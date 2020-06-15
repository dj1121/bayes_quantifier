# Functions for dealing with LOT grammars

import pickle

def save_grammar(grammar, filename):
    with open(filename, 'wb') as output:
        pickle.dump(grammar, output, pickle.HIGHEST_PROTOCOL)

def load_grammar(g):
    print()