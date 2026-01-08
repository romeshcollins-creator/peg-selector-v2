import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("peg_products_fixed.csv")

st.title("PEG Selector Demo")
st.write("Select PEG properties to filter products.")

# Get unique values for filters
peg_types = df['PEG_Type'].unique()
molecular_weights = df['Molecular_Weight'].unique()
forms = df['Form'].unique()

# Sidebar filters (unchanged behavior)
selected_type = st.sidebar.multiselect(
    "PEG Type",
    peg_types,
    default=list(peg_types)
)

selected_weight = st.sidebar.multiselect(
    "Molecular Weight",
    molecular_weights,
    default=list(molecular_weights)
)

selected_form = st.sidebar.multiselect(
    "Form",
    forms,
    default=list(forms)
)

# Filter dataframe
filtered_df = df[
    (df['PEG_Type'].isin(selected_type)) &
    (df['Molecular_Weight'].isin(selected_weight)) &
    (df['Form'].isin(selected_form))
]

st.write(f"### {len(filtered_df)} Products Found")

# Display products as expandable cards
for _, row in filtered_df.iterrows():
    with st.expander(row["Product Name"]):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")
            st.markdown(f"**Polymer Architecture:** {row['Polymer Architecture']}")
            st.markdown(f"**Intended Application:** {row['Intended Application']}")

        with col2:
            st.markdown(f"**Functional Group:** {row['Functional Group / Reactivity']}")
            st.markdown(f"**Solubility:** {row['Solubility']}")
            st.markdown(f"**PDI:** {row['Polydispersity Index (PDI)']}")

        st.markdown("---")

        st.markdown(f"**Application Notes:** {row['Application']}")
        st.markdown(f"**Product Page:** {row['Product Page']}")
