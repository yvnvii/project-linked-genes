import requests
import json
import emoji


class Module:

  ENSEMBL_API = "https://rest.ensembl.org"


  @staticmethod
  def get_phenotypes(gene_symbol, species):
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

  @staticmethod
  def get_genes(phenotype_term, species):
    url = f"{Module.ENSEMBL_API}/phenotype/term/{species}/{phenotype_term}?content-type=application/json"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      genes = [entry["Gene"] for entry in data if "Gene" in entry]
      genes = genes + [entry["Variation"] for entry in data if "Variation" in entry]
      return genes
    else:
      print(emoji.emojize(":warning: "),f"Error fetching genes for {phenotype_term}: {response.status_code}")
      return []

  def get_phenotypes_call(self):
    #example usage
    user_species = input(emoji.emojize(":magnifying_glass_tilted_right: Enter species name: "))
    user_genes = input(emoji.emojize(":dna: Enter gene names: "))
    genelist = user_genes.split()

    for gene in genelist:
      phenotypes = self.get_phenotypes(gene, user_species)
      if phenotypes:
        with open(f"{user_species}_{gene}.txt", "a") as file:
          file.write(json.dumps(phenotypes, indent=2) + "\n")
        print(emoji.emojize(":floppy_disk: "), f"phenotypes for {gene} saved to {user_species}_{gene}.txt")
      else:
        print(emoji.emojize(":cross_mark: "), f"No phenotypes found for {gene}")

  def get_genotypes_call(self):
    user_species = input(emoji.emojize(":magnifying_glass_tilted_right: Enter species name: "))
    user_phenotypes = input(emoji.emojize(":microbe: Enter phenotype term: "))
    phenotypelist = user_phenotypes.split()

    for pheno in phenotypelist:
      genes = self.get_genes(pheno, user_species)
      if genes:
        with open(f"{user_species}_{pheno}.txt", "a") as file:
          file.write(json.dumps(genes, indent=2) + "\n")
        print(emoji.emojize(":floppy_disk: "), f"genes for {pheno} saved to {user_species}_{pheno}.txt")
      else:
        print(emoji.emojize(":cross_mark: "),f"No phenotypes found for {pheno}")




