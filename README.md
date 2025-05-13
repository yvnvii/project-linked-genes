# LDExplorer

**LDExplorer** is a command-line tool for exploring linkage disequilibrium (LD) patterns in SNPs associated with a specific phenotype across a human population. It uses the GWAS Catalog and LDLink APIs to identify associated SNPs, find linked variants, and retrieve traits related to those linked variants.

---

## 🚀 Features

- Match phenotype to its corresponding GWAS EFO ID
- Identify SNPs associated with the phenotype (based on p-value threshold)
- Retrieve linked SNPs using LDLink (based on LD statistics like r²)
- Identify correlated alleles and their associated traits
- Filter results by odds ratio, presence of trait info, or trait keywords
- Export results to JSON (optionally to CSV)

---

## 🧱 Installation

1. Clone this repository:

```bash
git clone https://github.com/your-username/ldexplorer.git
pip install -e .

```

[Link Text](https://docs.google.com/presentation/d/1to-E5VGYmTZpUr2RKmmmfa3kL9oDQN7IqkT8eVcG2sI/edit?usp=sharing)
