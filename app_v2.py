import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("peg_products_v2.csv")  # <- Corrected CSV file name

st.set_page_config(page_title="PEG Selector v2", layout="wide")

st.title("PEG Selector v2")

# Sidebar filters
st.sidebar.header("Filter PEG Products")

# Get unique values for filters
commercial_partners = df["Commercial Partner"].unique()
polymer_architectures = df["Polymer Architecture"].unique()
intended_applications = df["Intended Application"].unique()

# Sidebar multi-selects
selected_partner = st.sidebar.multiselect("Commercial Partner", commercial_partners)
selected_architecture = st.sidebar.multiselect("Polymer Architecture", polymer_architectures)
selected_application = st.sidebar.multiselect("Intended Application", intended_applications)

# Filter dataframe based on selections
filtered_df = df.copy()

if selected_partner:
    filtered_df = filtered_df[filtered_df["Commercial Partner"].isin(selected_partner)]
if selected_architecture:
    filtered_df = filtered_df[filtered_df["Polymer Architecture"].isin(selected_architecture)]
if selected_application:
    filtered_df = filtered_df[filtered_df["Intended Application"].isin(selected_application)]

st.write(f"Showing {len(filtered_df)} products")

# Display products with expandable detail view
for idx, row in filtered_df.iterrows():
    with st.expander(row["Product Name"]):
        st.write(f"**Commercial Partner:** {row['Commercial Partner']}")
        st.write(f"**Molecular Weight (kDa):** {row['Molecular Weight (kDa)']}")
        st.write(f"**Functional Group / Reactivity:** {row['Functional Group / Reactivity']}")
        st.write(f"**Polymer Architecture:** {row['Polymer Architecture']}")
        st.write(f"**Solubility:** {row['Solubility']}")
        st.write(f"**Intended Application:** {row['Intended Application']}")
        st.write(f"**Polydispersity Index (PDI):** {row['Polydispersity Index (PDI)']}")
        st.write(f"**Application:** {row['Application']}")
        if "Product URL" in row:
            st.markdown(f"[Product Link]({row['Product URL']})")
