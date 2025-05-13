#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup, find_packages

# build command
setup(
    name="ldexplorer",
    version="0.0.1",
    author="Yuki Ogawa",
    author_email="yo2368@columbia.edu",
    license="GPLv3",
    description="A package for calculating risks of carrying linked alleles only based on phenotypic traits",
    classifiers=["Programming Language :: Python :: 3"],
    packages=find_packages(where="final_submission", include=["ldexplorer", "ldexplorer.*"]),
    package_dir={"": "final_submission"},
    entry_points={
        "console_scripts": ["ldexplorer = ldexplorer.__main__:main", "bayesian = ldexplorder.bayesian:main"]
    },
)

