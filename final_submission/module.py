#!/usr/bin/env python

"""
A function for calculating risks of carrying linked alleles based on phenotype
"""

import requests
from collections import defaultdict
from difflib import get_close_matches
import concurrent.futures


GWAS_URL = "https://www.ebi.ac.uk/gwas/rest/api/"
PVAL_THRESHOLD = 1e-2
LDLINK_TOKEN = "0cbd402f83ac"



#get EFO_id (experimental factor ontology id) of input phenotype.
#use get_close_matches to return most possible one evem if the input does not exactly match with the term (e.g., Alzheimer's disease and Alzheimer disease). 
def get_efo(phenotype_term):

    #search GWAS catalog for the phenotype
    search_url = f"{GWAS_URL}efoTraits/search/findByEfoTrait?trait={phenotype_term}"
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()

    trait_map={}
    
    for trait_entry in data["_embedded"]["efoTraits"]:
        trait_name = trait_entry["trait"].lower().strip()
        efo_id = trait_entry["shortForm"]
        trait_map[trait_name] = (trait_entry["trait"], efo_id)

    candidates = list(trait_map.keys())
    best_match = get_close_matches(phenotype_term,candidates,n=1,cutoff=0.6)

    if best_match:
        matched_name = best_match[0]
        official_name, efo_id = trait_map[matched_name]

        return{
            "user_input": phenotype_term,
            "matched_trait": official_name,
            "efo_id": efo_id #self.efo_id=efo_id
        }
    else:
        return None



#get SNPs for input efo_id.
def get_snp(efo_id, pval_limit = PVAL_THRESHOLD):
    
    #Search GWAS catalog for SNPs
    search_url =f"{GWAS_URL}efoTraits/{efo_id}/associations?size=10000"
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()
    risk_snps = []

    #Parse the response
    for assoc in data["_embedded"]["associations"]:

        pval = assoc.get("pvalue")
        odds = assoc.get("orPerCopyNum")
        raf = assoc.get("riskFrequency", "NR") #NR = not reported

        loci = assoc.get("loci",[])

        for locus in loci:

            strongest_risk_alleles = locus.get("strongestRiskAlleles", [])
            for risk_allele in strongest_risk_alleles:
                risk_allele_name = risk_allele.get("riskAlleleName")
                if risk_allele_name and "-" in risk_allele_name:
                    snp, allele = risk_allele_name.split("-")

                    risk_snps.append({
                        "snp": snp,
                        "risk_allele": allele,
                        "risk_frequency": raf,
                        "odds_ratio": odds,
                        "pvalue":pval
                    })

    high_conf_snps=[]

    #filter by p-value threshold
    for snp in risk_snps:
        if snp.get("risk_allele")!="?" and snp.get("pvalue") and snp.get("pvalue") <pval_limit:
            high_conf_snps.append(snp)

    return high_conf_snps




#get linked variants of input SNP
#input one SNP -> one or more variants linked to input SNP
#param: 
#snp_id = input SNPs
#pop = population (refer to "population_list.md")
#genome_build = (GRCh37 or GRCh38 or GRCh38 High Coverage)
#window = window size
#r2_d = r2 or d prime, which you want to use to set a threshold
#threshold = threshold for r2 or d prime (the one you set at r2_d)
#token = necessary to access the LDproxy API
def get_linked_variants(snp_id, pop, genome_build = "grch38", window = 500000, r2_d = "r2", threshold = 0.8, token = LDLINK_TOKEN):
        
    url = "https://ldlink.nih.gov/LDlinkRest/ldproxy"
    params = {
        "var": snp_id,
        "pop": pop,
        "r2_d": r2_d,
        "window": window,
        "genome_build": genome_build,
        "token": token
    }

    response = requests.get(url, params = params) # LDproxy returns tab-delimited text not JSON
    response.raise_for_status()
    linked_variants = []
    lines = response.text.splitlines()
    
    if len(lines)<=1:
        return linked_variants #no data

    header = lines[0].split("\t")

    for line in lines[1:]:
        fields = line.split("\t")
        if len(fields)>=10:

            if r2_d == "r2":
                if float(fields[6])>=threshold:
                    linked_variants.append({
                        "rs": fields[0],
                        "coord": fields[1],
                        "alleles": fields[2],                            
                        "maf": float(fields[3]),
                        "distance": int(fields[4]),
                        "dprime": float(fields[5]),
                        "r2": float(fields[6]),
                        "correlated_alleles": fields[7],
                        "forgedb_score": fields[8],
                        "regulomedb_score": fields[9],
                        "function": fields[10]
                    })
            else:
                if float(fields[5])>=threshold:
                    linked_variants.append({
                        "rs": fields[0],
                        "coord": fields[1],
                        "alleles": fields[2],
                        "maf": float(fields[3]),
                        "distance": int(fields[4]),
                        "dprime": float(fields[5]),
                        "r2": float(fields[6]),
                        "correlated_alleles": fields[7],
                        "forgedb_score": fields[8],
                        "regulomedb_score": fields[9],
                        "function": fields[10]
                    })   
    return linked_variants






#linked variant list -> phenotypes
#param:
#get ALL linked variants of input SNPs
#use get_linked_variants in loop to go through input list of SNPs
#population = population (refer to "population_list.md")
#max_workers = max CPU for pararell computing

def get_all_linked_variants(snp_list, population, genome_build = "grch38", r2_d = "r2", threshold = 0.8, max_workers = 10):

    if snp_list is None:
        raise ValueError("No SNPs found. Please run get_snp() first.")

    snp_entries = snp_list
    def fetch_linked(snp_entry):
        snp_id = snp_entry["snp"]
        risk_allele = snp_entry["risk_allele"]
        original_odds_ratio = snp_entry["odds_ratio"]
            
        if not snp_id.startswith("rs"):
            return {"SNP": snp_id, "Risk_Allele": risk_allele, "odds_ratio": original_odds_ratio, "Linked SNP": []}
        try:
            linked = get_linked_variants(
                snp_id = snp_id,
                pop = population,
                genome_build = genome_build,
                r2_d = r2_d,
                threshold = threshold,
                token = LDLINK_TOKEN
            )
            return {"SNP": snp_id, "Risk_Allele": risk_allele, "Linked SNP": linked}
        except Exception as e:
            print(f"Effor fetching {snp_id}:{e}")
            return {"SNP":snp_id, "Linked SNP": []}

    snp_ids = [snp["snp"] for snp in snp_list]

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor:
        future_to_snp = {executor.submit(fetch_linked, snp_entry):snp_entry for snp_entry in snp_entries}
        for future in concurrent.futures.as_completed(future_to_snp):
            results.append(future.result())
            
    return results





#transform input list of linked SNPs to match risk increasing allele of original input phenotype and linked allele of linked SNPs that are correlated with risk increasing allele of original phenotype.

def transform_linked_snps(data):
    result = []
    for entry in data:
        risk_snp = entry.get('SNP')
        risk_allele = entry.get('Risk_Allele')
        odds_ratio = entry.get('odds_ratio')
        linked_snps = entry.get('Linked SNP', [])

        linked_result = []
        if linked_snps:
            for linked in linked_snps:
                correlated_info = linked.get('correlated_alleles', '')
                alleles = linked.get('alleles', '')
                r2_value = linked.get('r2')

                if not correlated_info or not alleles:
                    continue  # Skip if critical info missing
    
                pairs = [pair.strip() for pair in correlated_info.split(",") if "=" in pair]
                mapping = {original.strip(): linked_allele.strip() for original, linked_allele in (pair.split("=") for pair in pairs)}
    
                correlated = mapping.get(risk_allele)

                if correlated:
                        # Extract alleles properly
                    allele_list = alleles.strip('()').split('/')
                    non_correlated = [allele for allele in allele_list if allele != correlated]
                    non_correlated = non_correlated[0] if non_correlated else None

                    linked_result.append({
                        'rs': linked.get('rs'),
                        'Correlated Allele with Risk Allele': correlated,
                        'Non Correlated Allele with Risk Allele': non_correlated,
                        'r2': r2_value
                    })

        result.append({
            'SNP': risk_snp,
            'Risk_Allele': risk_allele,
            'odds_ratio': odds_ratio,
            'Linked SNP': linked_result
        })

    return result









#get traits of linked alleles using linkage disequilibrium (ld)

def get_ld_snp_trait(data):

    ld_trait = {}

    for snp_entry in data:
        snp = snp_entry.get("SNP")
        original_risk_allele = snp_entry.get("Risk_Allele")
        original_odds_ratio = snp_entry.get("odds_ratio")

        ld_trait[snp]={
            "rs":snp,
            "risk_allele":original_risk_allele,
            "odds_ratio": original_odds_ratio,
            "Linked SNP":[]
        }
        
        for ld_snp in snp_entry.get("Linked SNP", []):
            rs = ld_snp.get("rs")
            corr_allele = ld_snp.get("Correlated Allele with Risk Allele")
            non_corr_allele = ld_snp.get("Non Correlated Allele with Risk Allele")
            r2 = ld_snp.get("r2")

            linked_entry = {
                "linked_rs":rs,
                "r2":r2,
                "correlated_allele":[{
                    "correlated_allele": corr_allele,
                    "trait":None,
                    "risk_frequency":None,
                    "odds_ratio": None,
                    "beta": None,
                    "beta_unit": None,
                    "beta_direction": None
                }],
                "non_correlated_allele":[{
                    "non_correlated_allele": non_corr_allele,
                    "trait":None,
                    "risk_frequency":None,
                    "odds_ratio": None,
                    "beta": None,
                    "beta_unit": None,
                    "beta_direction": None
                }]
            }

            if not rs:
                print("no rs")
                continue

        # Construct the correct URL for association lookup
            url = f"{GWAS_URL}associations/search/findByRsId?rsId={rs}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                response_data = response.json()
            except Exception as e:
                print(f"Failed to retrieve associations for {rs}: {e}")
                continue

            for assoc in response_data.get("_embedded", {}).get("associations", []):
                
                pval = assoc.get("pvalue")
                odds = assoc.get("orPerCopyNum")
                beta = assoc.get("betaNum")
                beta_unit = assoc.get("betaUnit")
                beta_direction = assoc.get("betaDirection")
                raf = assoc.get("riskFrequency", "NR")
                loci = assoc.get("loci", [])

                for locus in loci:
                    for risk_allele in locus.get("strongestRiskAlleles", []):
                        risk_allele_name = risk_allele.get("riskAlleleName")
                        if risk_allele_name and "-" in risk_allele_name:
                            snp_id, allele = risk_allele_name.split("-")
                        else:
                            continue

                    # Get trait link and fetch trait data

                        
                        trait_link = assoc.get("_links", {}).get("efoTraits",{}).get("href")
                        if not trait_link:
                            continue
                        try:
                            efo_response = requests.get(trait_link)
                            efo_response.raise_for_status()
                            efo_data = efo_response.json()
                            traits = efo_data.get("_embedded", {}).get("efoTraits",[])
                        except Exception as e:
                            print(f"Failed to get traits for {rs}: {e}")
                            continue

                        for trait in traits:
                            linked_trait = trait.get("trait")

                            trait_info = {
                                    "trait": linked_trait,
                                    "risk_frequency": raf,
                                    "odds_ratio": odds,
                                    "beta": beta,
                                    "beta_unit": beta_unit,
                                    "beta_direction": beta_direction,                                        
                                    "pvalue": pval   
                            }

                            if allele == corr_allele:
                                linked_entry["correlated_allele"].append(trait_info)
                            else:
                                linked_entry["non_correlated_allele"].append(trait_info)

            ld_trait[snp]["Linked SNP"].append(linked_entry)
                                
                    
    return ld_trait




#get filtered results.
#param:
#odds_ratio_max = max odds ratio (no more than 1).
#odds_ratio_min = minimum odds ratio (no less than 0). If you want to eliminate ones with odds_ratio = None, set (odds_ratio_max = 1, odds_ratio_min = 0).
#with_trait = True: extract ones with trait explanation, False: extract anything including trait = None.
#trait_filter = search traits that include the keyword.(e.g., trait_filter = "Alzheimer" -> trait = "Alzheimer", or "Alzheimer diesease", or "Alzheimer's disease")

def get_filtered(data, odds_ratio_max=None, odds_ratio_min=None, with_trait=False, trait_filter=None):
    """
    Filters a SNP dictionary by:
    - Non-empty 'Linked SNP'
    - Optional odds ratio range
    - Optional presence of 'trait' in correlated_allele
    - Optional keyword filtering on 'trait'

    Parameters:
    - data (dict): Original SNP dictionary
    - odds_ratio_max (float or None): Maximum odds ratio threshold
    - odds_ratio_min (float or None): Minimum odds ratio threshold
    - with_trait (bool): If True, only keep correlated_allele with a non-None 'trait'
    - trait_filter (str or None): If set, only keep correlated_allele where trait contains this keyword

    Returns:
    - dict: Filtered SNP dictionary
    """
    filtered = {}

    for snp_key, snp_data in data.items():
        or_val = snp_data.get('odds_ratio')

        # Filter by odds_ratio range if specified
        if or_val is not None:
            if odds_ratio_max is not None and or_val > odds_ratio_max:
                continue
            if odds_ratio_min is not None and or_val < odds_ratio_min:
                continue

        new_linked_snps = []
        for linked in snp_data.get('Linked SNP', []):
            correlated = linked.get('correlated_allele', [])

            # Apply 'trait' filters if required
            if with_trait:
                correlated = [c for c in correlated if c.get('trait') is not None]
            if trait_filter is not None:
                correlated = [c for c in correlated if c.get('trait') and trait_filter.lower() in c['trait'].lower()]

            if correlated:
                new_linked_snps.append({**linked, 'correlated_allele': correlated})

        if new_linked_snps:
            filtered[snp_key] = {**snp_data, 'Linked SNP': new_linked_snps}

    return filtered







class LD:

    def __init__(self, phenotype_term, population):
        self.phenotype_term = phenotype_term.lower().strip()
        self.population = population
        self.efo_id = None
        self.matched_name = None
        self.snp = None
        self.ld_snp = None
        self.ld_snp_trait = None
        self.filtered = None

    def execute(self):
        get_efo_result = get_efo(self.phenotype_term)
        if not get_efo_result:
            raise ValueError(f"Phenotype '{self.phenotype_term}' not found in GWAS catalog.")

        self.efo_id = get_efo_result.get("efo_id")
        self.matched_name = get_efo_result.get("matched_trait")
        print(f"Matched phenotype: {self.matched_name} (EFO ID: {self.efo_id})")

        get_snp_result = get_snp(self.efo_id)
        if not get_snp_result:
            raise ValueError(f"No SNPs found for EFO ID '{self.efo_id}'.")

        print(f"Found {len(get_snp_result)} SNPs with p-value < threshold")
        self.snp = get_snp_result

        self.ld_snp = get_all_linked_variants(self.snp, self.population, max_workers=10, threshold=0.8)
        print(f"Linked variants collected")

        self.ld_snp = transform_linked_snps(self.ld_snp)
        print(f"Linked variants transformed")

        self.ld_snp_trait = get_ld_snp_trait(self.ld_snp)
        print(f"Traits assigned to linked SNPs")

        return self.ld_snp_trait

    def get_filtered(self, odds_ratio_max=None, odds_ratio_min=None, with_trait=False, trait_filter=None):
        self.filtered = get_filtered(
            self.ld_snp_trait,
            odds_ratio_max=odds_ratio_max,
            odds_ratio_min=odds_ratio_min,
            with_trait=with_trait,
            trait_filter=trait_filter
        )
        return self.filtered
