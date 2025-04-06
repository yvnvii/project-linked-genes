import requests
import json
import emoji
import re

class Module:

  ENSEMBL_API = "https://rest.ensembl.org"

  def get_phenotypes(self, gene_symbol, species):

    self.gene = gene_symbol
    self.species = species

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

  def get_genes(self, phenotype_term, species):
    self.phenotype = phenotype_term
    self.species = species

    url = f"{Module.ENSEMBL_API}/phenotype/term/{species}/{phenotype_term}?content-type=application/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Only collect valid gene names
        genes = []
        for entry in data:
            gene_name = entry.get("associated_gene")
            if gene_name and gene_name != "":
                genes.append(gene_name)

        return list(set(genes))  # Remove duplicates
    else:
        print(emoji.emojize(":warning: "), f"Error fetching genes for {phenotype_term}: {response.status_code}")
        return []


  def get_ld_variants(self, species, variant_id, population):
    """
    Fetch LD variants for a specific variant ID.
    """
    url = f"{Module.ENSEMBL_API}/ld/{species}/{variant_id}/{population}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns linked variants
    return None

  def clean_input(self, text):
    """Remove surrounding quotes and spaces from input."""
    return re.sub(r'^["\']|["\']$', '', text.strip())


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
    phenotype = user_phenotypes.strip()  # Keep full input
    genes = self.get_genes(phenotype, user_species)

    if genes:
      with open(f"{user_species}_{phenotype}.txt", "a") as file:
        cleaned_genes = [self.clean_input(gene) for gene in genes] 
        file.write("\n".join(cleaned_genes) + "\n")
      print(emoji.emojize(":floppy_disk: "), f"genes for {pheno} saved to {user_species}_{phenotype}.txt")
    else:
      print(emoji.emojize(":cross_mark: "),f"No phenotypes found for {phenotype}")

    if(input("proceed to find linked genes? [y/n]: ")=="y"):
      self.get_ld_variants_call(file = f"{user_species}_{phenotype}")
    else:
      print("done")

  def get_ld_variants_call(self, file= False):

    filepath = file if file else input(emoji.emojize(":magnifying_glass_tilted_right: Enter file path with a list of genes: "))
    if not file:
        species = input(emoji.emojize(":magnifying_glass_tilted_right: Enter species name: "))
    else:
        species = file.split("_")[0]  # Extract species from filename

    population = input(emoji.emojize(":magnifying_glass_tilted_right: Enter population: "))


    output = f"ld_{filepath}.txt"

    try:
      with open(f'{filepath}.txt', 'r') as file, open(output, "a") as output_file:
        for gene in file:
          gene = gene.strip()
          variants = self.get_ld_variants(species, gene, population)
          output_file.write(f"linked variants for {gene}:\n\n")
          output_file.write(json.dumps(variants, indent=2)+"\n")
      print(emoji.emojize(":floppy_disk: "), f"genes linked to {filepath} saved to {output}")
    except FileNotFoundError:
      print(emoji.emojize(":cross_mark: "),f"No file found for {filepath}")


