import streamlit as st
import json
import pandas as pd
from ldexplorer.module import LD
import sympy as sp
from ldexplorer.bayesian import estimate_trait_given_snp, estimate_snp_given_trait


tab1, tab2 = st.tabs(["LD Explorer", "Bayesian Inference"])


# --- Population List ---
population_dict = {
    "All Populations (ALL)": "ALL",
    "African (AFR)": "AFR",
    "Yoruba in Ibadan, Nigeria (YRI)": "YRI",
    "Luhya in Webuye, Kenya (LWK)": "LWK",
    "Gambian in Western Gambia (GWD)": "GWD",
    "Mende in Sierra Leone (MSL)": "MSL",
    "Esan in Nigeria (ESN)": "ESN",
    "Americans of African Ancestry in SW USA (ASW)": "ASW",
    "African Caribbeans in Barbados (ACB)": "ACB",
    "Ad Mixed American (AMR)": "AMR",
    "Mexican Ancestry from Los Angeles, USA (MXL)": "MXL",
    "Puerto Ricans from Puerto Rico (PUR)": "PUR",
    "Colombians from Medellin, Colombia (CLM)": "CLM",
    "Peruvians from Lima, Peru (PEL)": "PEL",
    "East Asian (EAS)": "EAS",
    "Han Chinese in Beijing, China (CHB)": "CHB",
    "Japanese in Tokyo, Japan (JPT)": "JPT",
    "Southern Han Chinese (CHS)": "CHS",
    "Chinese Dai in Xishuangbanna, China (CDX)": "CDX",
    "Kinh in Ho Chi Minh City, Vietnam (KHV)": "KHV",
    "European (EUR)": "EUR",
    "Utah Residents from North and West Europe (CEU)": "CEU",
    "Toscani in Italia (TSI)": "TSI",
    "Finnish in Finland (FIN)": "FIN",
    "British in England and Scotland (GBR)": "GBR",
    "Iberian population in Spain (IBS)": "IBS",
    "South Asian (SAS)": "SAS",
    "Gujarati Indian from Houston, Texas (GIH)": "GIH",
    "Punjabi from Lahore, Pakistan (PJL)": "PJL",
    "Bengali from Bangladesh (BEB)": "BEB",
    "Sri Lankan Tamil from the UK (STU)": "STU",
    "Indian Telugu from the UK (ITU)": "ITU"
}

# --- Sidebar Inputs ---
st.sidebar.header("LDExplorer Controls")

phenotype = st.sidebar.text_input("Phenotype (e.g., Alzheimer's disease)", "preeclampsia")
pop_label = st.sidebar.selectbox("Population", list(population_dict.keys()))
population = population_dict[pop_label]

odds_min = st.sidebar.slider("Min Odds Ratio", 0.0, 1.0, 0.0)
odds_max = st.sidebar.slider("Max Odds Ratio", 0.0, 1.0, 1.0)

with_trait = st.sidebar.checkbox("Only show variants with trait info", value=False)
trait_filter = st.sidebar.text_input("Trait Keyword Filter (optional)")

# New additions: LD method and threshold
ld_measure = st.sidebar.selectbox("LD Measure", ["r2", "dprime"])
ld_threshold = st.sidebar.slider("LD Threshold", 0.0, 1.0, 0.8)

run_button = st.sidebar.button("Run LD Analysis")

# --- Main App ---
st.title("🧬 LDExplorer: Linkage Disequilibrium & Trait SNP Analyzer")

def flatten_results(data_dict):
    rows = []
    for snp_key, snp_data in data_dict.items():
        for linked in snp_data.get("Linked SNP", []):
            rs_id = linked.get("linked_rs")
            r2 = linked.get("r2")
            for entry in linked.get("correlated_allele", []):
                rows.append({
                    "Input SNP": snp_key,
                    "Linked RS": rs_id,
                    "Correlated Allele": entry.get("correlated_allele"),
                    "Trait": entry.get("trait"),
                    "Odds Ratio": entry.get("odds_ratio"),
                    "Risk Frequency": entry.get("risk_frequency"),
                    "Beta": entry.get("beta"),
                    "Beta Unit": entry.get("beta_unit"),
                    "Beta Direction": entry.get("beta_direction"),
                    "R²": r2
                })
    return pd.DataFrame(rows)

if run_button:
    with st.spinner("Running analysis... this may take a few minutes ⏳"):
        try:
            ld = LD(phenotype, population)
            ld.ld_snp = ld.snp = None  # Reset prior if rerun
            ld.ld_snp = ld.ld_snp_trait = None

            # Inject LD parameters before execution
            get_snp_result = ld.execute()
            ld.ld_snp = ld.ld_snp = ld.ld_snp_trait
            ld.ld_snp = ld.ld_snp_trait = ld.ld_snp_trait = get_snp_result

            filtered_result = ld.get_filtered(
                odds_ratio_max=odds_max,
                odds_ratio_min=odds_min,
                with_trait=with_trait,
                trait_filter=trait_filter if trait_filter else None
            )

            st.success("Analysis complete!")
            st.markdown(f"### Results for **{phenotype}** in **{pop_label}**")

            with st.expander("🔍 View Raw JSON"):
                st.json(filtered_result)

            df = flatten_results(filtered_result)
            st.markdown("### 📊 Filtered Result Table")
            st.dataframe(df)

            result_json = json.dumps(filtered_result, indent=2)
            st.download_button("📥 Download Results as JSON", result_json, file_name="ldexplorer_results.json", mime="application/json")

            csv_data = df.to_csv(index=False)
            st.download_button("📥 Download Results as CSV", csv_data, file_name="ldexplorer_results.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.markdown("👉 Use the sidebar to configure your parameters and click **Run LD Analysis**.")


with tab2:
    st.header("🧮 Bayesian SNP-Trait Inference")
    with st.form("bayes_form"):
        OR_input = st.number_input("Odds Ratio (OR)", min_value=0.0, step=0.01, value=1.0)
        PS_input = st.number_input("Risk Frequency (SNP Frequency in Population) (P(S))", min_value=0.0, max_value=1.0, step=0.01, value=0.2)
        PT_input = st.number_input("Trait Frequency in Population (P(T))", min_value=0.0, max_value=1.0, step=0.001, value=0.01)
        submitted = st.form_submit_button("Run Bayesian Inference")

    if submitted:
        p_t_given_s = estimate_trait_given_snp(OR_input, PS_input, PT_input)
        if p_t_given_s is None:
            st.error("❌ Could not compute a valid solution for P(T|S). Please check your inputs.")
        else:
            p_s_given_t = estimate_snp_given_trait(p_t_given_s, PS_input, PT_input)
            st.success("✅ Calculation Successful")
            st.markdown(f"**P(T|S)** = `{p_t_given_s}`")
            st.markdown(f"**P(S|T)** = `{p_s_given_t}`")
