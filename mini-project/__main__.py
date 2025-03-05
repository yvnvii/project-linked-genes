#!/usr/bin/env python

"""
Command line interface to darwin_day
"""

import argparse
import emoji
from mini_project.module import Module

def parse_command_line():
    "parses args for the funtion"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # add long args
    parser.add_argument(
        "--g2p",
        help="returns phenotypes from given genes",
        action="store_true")

    # add long args
    parser.add_argument(
        "--p2g",
        help="returns genes from given phenotypes",
        action="store_true")

    # parse args
    return parser.parse_args()

def main():
    "run main function on parsed args"

    print(emoji.emojize(":rocket: Main program started"))

    # get arguments from command line as a dict-like object
    args = parse_command_line()
    module_instance = Module()

    # pass argument to call function
    if args.g2p:
        module_instance.get_phenotypes_call()
        
    elif args.p2g:
        module_instance.get_genotypes_call()

    else:
        print(emoji.emojize(":warning: No valid option provided."))
        print(emoji.emojize("Use --g2p (genes to phenotypes), or --p2g (phenotypes to genes)."))

if __name__ == "__main__":
    main()
    