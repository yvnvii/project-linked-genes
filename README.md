Linked Genes Explorer

This project is to create a program that retrieves genes that are linked to a given gene input.

This mini-project implements two methods:

# **1. Genes to phenotypes converter (command: --g2p)**
## It asks what species and genes you are looking at. You can only put one species at a time, but you can put many genes of the species in the query. Then it looks for the phenotypes of each gene and creates a file for each gene that contains a list of phenotype of the gene. The file  is automatically named as "{species}_{gene}.txt".

# **2. Phenotypes to genes converter (command: --p2g)**
## It asks what species and phenotypes your are looking at. You can only put one species at a time, but you can put many phenotypes of the species at a time in the query. Then it looks for the genes that can cause each phenotype and creates a file for each phenotype that contain a list of genes that may be implicated. The file is automatically named as "{species}_{phenotype}.txt".

Installation:
conta install [list] -c conda-forge

git clone [https://github.com/yvnvii/mini-project.git]
cd ./mini-project


