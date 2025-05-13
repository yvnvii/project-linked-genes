# 🧬 LDExplorer 🧬

**LDExplorer** is a tool for exploring linkage disequilibrium (LD) patterns in SNPs associated with a specific phenotype across a human population. It uses the GWAS Catalog and LDLink APIs to identify associated SNPs, find linked variants, and retrieve traits related to those linked variants.

---

## 🚀 Features

- Match phenotype to its corresponding GWAS EFO ID
- Identify SNPs associated with the phenotype (based on p-value threshold)
- Retrieve linked SNPs using LDLink (based on LD statistics like r²)
- Identify correlated alleles and their associated traits
- Filter results by odds ratio, presence of trait info, or trait keywords
- Export results to JSON

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

With the result, you get OR and P(S).
And ook up P(T) = How common the trait is in the population by yourself. Then run bayesian calculation to get the chance of having the SNP variant given the trait.

```bash
bayesian --or 2.0 --ps 0.3 --pt 0.05
```
This returns

```bash
Input values:
  OR = 2.0
  P(S) = 0.3
  P(T) = 0.05

Solution 1:
  P(T|S) = 0.075335
  P(S|T) = 0.45201
```

P(T|S) = Chance you have the trait if you have the SNP
P(S|T) = Chance someone has a certain SNP if we know they have the trait

## 2. Streamlit tool

```bash
cd final_submission
streamlit run ldexplorer_streamlit.py 
```

## 3. Jupyter Notebook
```bash
cd final_submission/notebook
```

---

## 🧱 Installation

1. Clone this repository:

```bash
git clone https://github.com/yvnvii/project-linked-genes.git
cd prokect-linked-genes
pip install -e .

```

[Bayesian Calculation Slide](https://docs.google.com/presentation/d/1to-E5VGYmTZpUr2RKmmmfa3kL9oDQN7IqkT8eVcG2sI/edit?usp=sharing)
