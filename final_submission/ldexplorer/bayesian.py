#!/usr/bin/env python

"""
Command-line tool to estimate:
1. P(T|S): Probability of having the trait given the SNP
2. P(S|T): Probability of having the SNP given the trait

Uses symbolic solving of Bayes' Theorem based on:
- Odds Ratio (OR)
- SNP frequency in population (P(S))
- Trait frequency in population (P(T))
"""

import argparse
import sympy as sp


def estimate_trait_given_snp(OR_val, PS_val, PT_val):
    w = sp.Symbol('w', real=True)
    OR, PS, PT = sp.symbols('OR PS PT', real=True)

    # Solve OR = [w(1 - PS - PT + w)] / [(PS - w)(PT - w)]
    equation = sp.Eq(OR, (w * (1 - PS - PT + w)) / ((PS - w) * (PT - w)))
    solutions = sp.solve(equation, w)

    # Evaluate valid numeric solutions
    numeric_solutions = [sol.evalf(subs={OR: OR_val, PS: PS_val, PT: PT_val}) for sol in solutions]
    valid_results = []

    for sol in numeric_solutions:
        if sol.is_real and 0 <= sol <= min(PS_val, PT_val):
            p_trait_given_snp = float(sol) / PS_val
            valid_results.append(round(p_trait_given_snp, 6))

    return valid_results


def estimate_snp_given_trait(p_trait_given_snp, PS_val, PT_val):
    if PT_val == 0:
        return None
    return round((p_trait_given_snp * PS_val) / PT_val, 6)


def main():
    parser = argparse.ArgumentParser(description="Estimate P(T|S) and P(S|T) using Bayes' Theorem and GWAS-style inputs.")
    parser.add_argument("--or", dest="odds_ratio", type=float, required=True, help="Odds ratio (OR) between SNP and trait")
    parser.add_argument("--ps", type=float, required=True, help="SNP frequency in population (P(S))")
    parser.add_argument("--pt", type=float, required=True, help="Trait frequency in population (P(T))")

    args = parser.parse_args()

    OR_val = args.odds_ratio
    PS_val = args.ps
    PT_val = args.pt

    print(f"Input values:")
    print(f"  OR = {OR_val}")
    print(f"  P(S) = {PS_val}")
    print(f"  P(T) = {PT_val}\n")

    p_trait_given_snp_solutions = estimate_trait_given_snp(OR_val, PS_val, PT_val)

    if not p_trait_given_snp_solutions:
        print("No valid solution for P(T|S) found with given inputs.")
        return

    for idx, pt_given_s in enumerate(p_trait_given_snp_solutions, 1):
        ps_given_t = estimate_snp_given_trait(pt_given_s, PS_val, PT_val)
        print(f"Solution {idx}:")
        print(f"  P(T|S) = {pt_given_s}")
        print(f"  P(S|T) = {ps_given_t}\n")


if __name__ == "__main__":
    main()

