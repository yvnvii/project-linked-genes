#!/usr/bin/env python

"""Fetch Ensemble data

Example changes
---------------
- 4-space indent is more common in Python
- Constants (ENSEMBLE_API) should be defined outside the class
- Class should have an __init__ method to define and store variables.
- Add __main__ at end of module to allow testing within the editor.
"""

import requests
import json
import emoji
import re

ENSEMBL_API = "https://rest.ensembl.org"


class Module:
	def __init__(self, gene_symbol, species):
		self.gene = gene_symbol
		self.species = species

	def get_phenotypes(self):
		"""Fetches phenotypes associated with a gene from Ensembl API."""
		url = f"{Module.ENSEMBL_API}/phenotype/gene/{species}/{gene_symbol}?content-type=application/json"
		response = requests.get(url)
		if response.status_code == 200:
			data = response.json()
			phenotypes = [entry["description"] for entry in data if "description"in entry]
			return (phenotypes)
		else:
			print(emoji.emojize(":warning: "), f"Error fetching phenotypes for {gene_symbol}: {response.status_code}")
			return []
