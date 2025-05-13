#!/usr/bin/env python

"""
Command line interface to ldexplorer
"""


import argparse
import json

from .module import LD, get_filtered


def main():
    parser = argparse.ArgumentParser(description="Run LD analysis based on phenotype and population.")
    parser.add_argument("--phenotype", type=str, required=True, help="Phenotype term (e.g., 'Alzheimer's disease')")
    parser.add_argument("--population", type=str, required=True, help="Population code (e.g., EUR, AFR, EAS)")
    parser.add_argument("--min_odds", type=float, default=None, help="Minimum odds ratio filter")
    parser.add_argument("--max_odds", type=float, default=None, help="Maximum odds ratio filter")
    parser.add_argument("--with_trait", action="store_true", help="Filter to only include entries with trait information")
    parser.add_argument("--trait_filter", type=str, default=None, help="Only include traits that match this string")
    parser.add_argument("--output", type=str, default=None, help="Save output to a JSON file")

    args = parser.parse_args()

    try:
        ld = LD(args.phenotype, args.population)
        print(f"Starting LD analysis for '{args.phenotype}' in population '{args.population}'")

        result = ld.execute()

        filtered_result = get_filtered(
            result,
            odds_ratio_max=args.max_odds,
            odds_ratio_min=args.min_odds,
            with_trait=args.with_trait,
            trait_filter=args.trait_filter
        )

        if args.output:
            with open(args.output, "w") as f:
                json.dump(filtered_result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(filtered_result, indent=2))

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()