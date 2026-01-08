# app_v2.py

import streamlit as st
import pandas as pd

# ==========================
# App Title and Description
# ==========================
st.set_page_config(page_title="PEG Selector Tool - Version 2", layout="wide")

st.title("PEG Selector Tool – Version 2")
st.write(
    """
    Filter PEG products by functional group, molecular weight, polymer architecture, and other criteria.
    Click on the product name to open the product page.
    """
)

# ==========================
# Load the CSV
# ==========================
# Make sure your CSV is in the same folder or provide the correct path
df = pd.read_csv("peg_products_v2.csv")

# ==========================
# Sidebar Filters
# ==========================
st.sidebar.header("Filter Options")

# Functional Group Filter
functional_groups = df["Functional Group"].unique()
selected_fg = st.sidebar.multiselect(
    "Functional Group", functional_groups, default=functional_groups
)

# Molecular Weight Filter
mw_min = int(df["Molecular Weight"].min())
mw_max = int(df["Molecular Weight"].max())
selected_mw = st.sidebar.slider(
    "Molecular Weight (kDa)", min_value=mw_min, max_value=mw_max,
    value=(mw_min, mw_max)
)

# Polymer Architecture Filter
poly_archs = df["Polymer Architecture"].unique()
selected_arch = st.sidebar.multiselect(
    "Polymer Architecture", poly_archs, default=poly_archs
)

# Commercial Partner Filter
partners = df["Commercial Partner"].unique()
selected_partner = st.sidebar.multiselect(
    "Commercial Partner", partners, default=partners
)

# ==========================
# Apply Filters
# ==========================
filtered_df = df[
    (df["Functional Group"].isin(selected_fg)) &
    (df["Molecular Weight"] >= selected_mw[0]) &
    (df["Molecular Weight"] <= selected_mw[1]) &
    (df["Polymer Architecture"].isin(selected_arch)) &
    (df["Commercial Partner"].isin(selected_partner))
]

# ==========================
# Display Filtered Results
# ==========================
st.write(f"### {len(filtered_df)} Products Found")

if len(filtered_df) > 0:
    for index, row in filtered_df.iterrows():
        # Make the product name clickable
        st.markdown(
            f"- [{row['Product Name']}]({row['Product URL']})",
            unsafe_allow_html=True
        )
else:
    st.write("No products match your filter criteria.")

# ==========================
# Optional: Display the table for reference
# ==========================
with st.expander("Show Full Table"):
    st.dataframe(filtered_df.reset_index(drop=True))
