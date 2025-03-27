# Goal of the project: Is it clear to you from the proposal.md how the goal can be accomplished using Python and the specified packages?
Yes, the goal is clear to me! I was a little confused about what "linked genes" mean when I read this part, but I found the explanation latter. It might be worthwhile to define "linked genes" are genes that are closely related in their genomic region rather than genes that are under same selection pressure in this paragraph. 


# The Data: Is it clear to you from the proposal.md what the data for this project is, or will look like?
Yes!

# The code: (Look at the Python code files in detail first and try to comprehend a bit of what is written so far)
# Does the current code include a proper skeleton (pseudocode) for starting this project?
Yes! The structure of the package is very clear.

# What can this code do so far?
- In the `__main__.py`: The package accepts one of the two arguments (--g2p or --p2g) to return phenotypes from given genes or genes from given phenotypes
- In the `module.py`: there are seven functions that can be used to fetch genes, phenotypes, and genomic locations from the ENSEMBL database.
	- `get_phenotypes`, `get_genes` and `get_ld_variants`: directly interact with the ENSEMBL database by requesting one gene or one phenotype per time
	- `get_phenotypes_call`, `get_genotypes_call` and `get_ld_variants_call`: interact with users by printing guildlines and can receive multiple genes or phenotypes from users by a for loop to run the three functions above
	- `clean_input`: is used for removing spaces around gene names

# Given the project description, what are some individual functions that could be written to accomplish parts of this goal?


# Code contributions/ideas: 
1. As `clean_input` function is only be used in `get_phenotypes_call` function once, maybe you can use add this one line of code in the `get_phenotypes_call` directly without defining another function.
2. If you want to use a class, I think people usually will use a `__init__` function to store the attributes of the class, like
```python
def __init__(self, gene_symbol, species, phenotype_term):
    self.gene = gene_symbol
    self.species = species
    self.phenotype = phenotype_term
    self.species = species
```
It is helpful for other developers to check what attributes are included in this class, and might also be helpful for you if you want to add or remove any attributes or use the same attributes in other functions in this class. 
3. It looks like currently the software is zero tolerant to any typos in the gene names or phenotype traits. Perhaps it worths to create another function to check typos and suggest the correct genes/phenotypes.
4. In your future enhancements, you suggest to create bar plots or pie charts of shared traits. `toyplot` library might be a good place to start as this library is minimal.
