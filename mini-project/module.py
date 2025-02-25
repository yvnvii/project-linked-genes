import requests

ENSEMBL_API = "https://rest.ensembl.org"

def get_phenotypes(gene_symbol, species):
  """Fetches phenotypes associated with a gene from Ensembl API."""
  url = f"{ENSEMBL_API}/phenotype/gene/{species}/{gene_symbol}?content-type=application/json"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    print(data)
  else:
    print(f"Error fetching phenotypes for {gene_symbol}: {response.status_code}")
    return []

#example usage
user_species = input("Enter species name: ")
user_genes = input("Enter gene names: ")
genelist = user_genes.split()
for gene in genelist:
  phenotypes = get_phenotypes(user_genes, user_species)
  print(f"Phenotypes for {gene}: {phenotypes}")


def get_genes(phenotype_term, species):
  url = f"{ENSEMBL_API}/phenotype/term/{species}/{phenotype_term}?content-type=application/json"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    genes = [entry["Gene"] for entry in data if "Gene" in entry]
    genes = genes + [entry["Variation"] for entry in data if "Variation" in entry]
    return genes
  else:
    print(f"Error fetching genes for {phenotype_term}: {response.status_code}")
    return []
'''
#example
user_species = input("Enter species name: ")
user_phenotype = input("Enter phenotype term: ")
genes = get_genes(user_phenotype, user_species)
print(f"Genes for {user_phenotype}: {genes}")
'''
