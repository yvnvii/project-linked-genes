import streamlit as st
import json
import pandas as pd
from ldexplorer.module import LD

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

odds_min = st.sidebar.slider("Min Odds Ratio", 0.0, 10.0, 0.0)
odds_max = st.sidebar.slider("Max Odds Ratio", 0.0, 10.0, 10.0)

with_trait = st.sidebar.checkbox("Only show variants with trait info", value=False)
trait_filter = st.sidebar.text_input("Trait Keyword Filter (optional)")

run_button = st.sidebar.button("Run LD Analysis")

# --- Main App ---
st.title("🧬 LDExplorer: Linkage Disequilibrium & Trait SNP Analyzer")

def flatten_results(data_dict):
    """Flatten nested dict structure to a table for CSV/export."""
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
            raw_result = ld.execute()

            filtered_result = ld.get_filtered(
                odds_ratio_max=odds_max,
                odds_ratio_min=odds_min,
                with_trait=with_trait,
                trait_filter=trait_filter if trait_filter else None
            )

            st.success("Analysis complete!")
            st.markdown(f"### Results for **{phenotype}** in **{pop_label}**")

            # Display JSON block
            with st.expander("🔍 View Raw JSON"):
                st.json(filtered_result)

            # Create and show flattened table
            df = flatten_results(filtered_result)
            st.markdown("### 📊 Filtered Result Table")
            st.dataframe(df)

            # Download JSON
            result_json = json.dumps(filtered_result, indent=2)
            st.download_button("📥 Download Results as JSON", result_json, file_name="ldexplorer_results.json", mime="application/json")

            # Download CSV
            csv_data = df.to_csv(index=False)
            st.download_button("📥 Download Results as CSV", csv_data, file_name="ldexplorer_results.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.markdown("👉 Use the sidebar to configure your parameters and click **Run LD Analysis**.")

