# Genetic Linkage-Based Risk Estimator

This project aims to create a tool that estimates an individual's genetic risk of inheriting a known disease based on a parent’s diagnosis, by leveraging genetic linkage and phenotypic trait associations — without requiring DNA sequencing.

Instead of expensive genetic tests, the tool uses publicly available genomic data from Ensembl to:
- Identify genes linked to a disease-causing gene,
- Fetch known traits associated with those linked genes,
- And assess how many of those traits are shared between a parent and child.

By comparing phenotypic similarity across genetically linked regions, the program provides a low-cost, accessible method to estimate genetic risk, especially for single-gene (monogenic) disorders like cystic fibrosis, Huntington's disease, and Tay-Sachs.

### in development

To install and contribute to the development of this tool locally, follow the steps below:

```bash
# Install dependencies (update the list as needed)
conda install requests emoji -c conda-forge

# Clone the repository
git clone https://github.com/yvnvii/project-linked-genes.git
cd project-linked-genes

# Install the package in editable mode
pip install -e .
