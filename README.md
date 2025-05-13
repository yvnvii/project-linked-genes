# 🧬 LDExplorer 🧬

**LDExplorer** is a tool for exploring linkage disequilibrium (LD) patterns in SNPs associated with a specific phenotype across a human population. It uses the GWAS Catalog and LDLink APIs to identify associated SNPs, find linked variants, and retrieve traits related to those linked variants.

---

## 🚀 Features

- Match phenotype to its corresponding GWAS EFO ID
- Identify SNPs associated with the phenotype (based on p-value threshold)
- Retrieve linked SNPs using LDLink (based on LD statistics like r²)
- Identify correlated alleles and their associated traits
- Filter results by odds ratio, presence of trait info, or trait keywords
- Export results to JSON (optionally to CSV)

---

## ⚙️ Versions

There are three versions you can use.

### 1. Command-line tool

working example:

make sure you are in "project-linked-genes" directory
```bash
ldexplorer --phenotype "preeclampsia" --population EUR --output result.json
```
This returns all linked SNPs with traits and risk alleles. The result is saved in .json file in the same directory.


2. Streamlit tool
3. Jupyter Notebook

---

## 🧱 Installation

1. Clone this repository:

```bash
git clone https://github.com/yvnvii/project-linked-genes.git
cd prokect-linked-genes
pip install -e .

```

[Link Text](https://docs.google.com/presentation/d/1to-E5VGYmTZpUr2RKmmmfa3kL9oDQN7IqkT8eVcG2sI/edit?usp=sharing)
