# app_v2.py

import streamlit as st
import pandas as pd

# ==========================
# Page Config
# ==========================
st.set_page_config(page_title="PEG Selector Tool - Version 2", layout="wide")

st.title("PEG Selector Tool – Version 2")
st.write(
    """
    Filter PEG products by functional group, molecular weight, polymer architecture, and other criteria.
    Click on a product name to see all pertinent information, including a clickable vendor URL.
    """
)

# ==========================
# Load CSV
# ==========================
df = pd.read_csv("peg_products_v2.csv")
df.columns = df.columns.str.strip()  # remove spaces
# Rename columns to match code
df = df.rename(columns={
    "Functional Group / Reactivity": "Functional Group",
    "Product Page": "Product URL",
    "Molecular Weight (kDa)": "Molecular Weight"
})

# ==========================
# Sidebar Filters
# ==========================
st.sidebar.header("Filter Options")

# Functional Group filter
fg_options = sorted(df["Functional Group"].unique())
selected_fg = st.sidebar.multiselect("Functional Group", fg_options, default=fg_options)

# Polymer Architecture filter
arch_options = sorted(df["Polymer Architecture"].unique())
selected_arch = st.sidebar.multiselect("Polymer Architecture", arch_options, default=arch_options)

# Commercial Partner filter
partner_options = sorted(df["Commercial Partner"].unique())
selected_partner = st.sidebar.multiselect("Commercial Partner", partner_options, default=partner_options)

# Molecular Weight filter
mw_min = int(df["Molecular Weight"].min())
mw_max = int(df["Molecular Weight"].max())
selected_mw = st.sidebar.slider("Molecular Weight (kDa)", min_value=mw_min, max_value=mw_max, value=(mw_min, mw_max))

# ==========================
# Apply Filters
# ==========================
filtered_df = df[
    (df["Functional Group"].isin(selected_fg)) &
    (df["Polymer Architecture"].isin(selected_arch)) &
    (df["Commercial Partner"].isin(selected_partner)) &
    (df["Molecular Weight"] >= selected_mw[0]) &
    (df["Molecular Weight"] <= selected_mw[1])
]

st.write(f"### {len(filtered_df)} Products Found")

# ==========================
# Display Products with Clickable Details
# ==========================
if len(filtered_df) > 0:
    for idx, row in filtered_df.iterrows():
        # Expander per product
        with st.expander(f"{row['Product Name']} ({row['Commercial Partner']})"):
            st.markdown(f"**Product Name:** {row['Product Name']}")
            st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")
            st.markdown(f"**Molecular Weight (kDa):** {row['Molecular Weight']}")
            st.markdown(f"**Functional Group:** {row['Functional Group']}")
            st.markdown(f"**Polymer Architecture:** {row['Polymer Architecture']}")
            st.markdown(f"**Solubility:** {row['Solubility']}")
            st.markdown(f"**Intended Application:** {row['Intended Application']}")
            st.markdown(f"**Polydispersity Index (PDI):** {row['Polydispersity Index (PDI)']}")
            st.markdown(f"**Application:** {row['Application']}")
            st.markdown(f"**Vendor URL:** [{row['Product URL']}]({row['Product URL']})", unsafe_allow_html=True)
else:
    st.write("No products match your filter criteria.")

# ==========================
# Optional: Show Full Table
# ==========================
with st.expander("Show Filtered Table"):
    st.dataframe(filtered_df.reset_index(drop=True))
