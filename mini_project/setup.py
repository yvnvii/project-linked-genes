#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
    name="linkedgenes",
    version="0.0.1",
    author="Yuki Ogawa",
    author_email="yo2368@columbia.edu",
    license="GPLv3",
    description="A package for exploring genes, phenotypes, and linked genes",
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={
        "console_scripts": ["linkedgenes = mini_project.__main__:main"]
    },
)
