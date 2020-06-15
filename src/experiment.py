# Main driver file for the program. Set up experiments and run them from here.
import argparse
import grammars
import data_handling


def run_experiment(model, grammar_path, data_dir, out_dir):
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-model', help='which model to run', type=str, required=True)
    parser.add_argument('-grammar_path', help='specify a grammar type to generate', type=str, required=True)
    parser.add_argument('-data_dir', help='directory of data for model', default="./../data", type=str, required=True)
    parser.add_argument('-out_dir', help='path to output', type=str, default='./tmp')
    args = parser.parse_args()

    run_experiment(args.model, args.grammar_path, args.data_dir, args.out_dir)