import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page config (FIRST Streamlit command)
# --------------------------------------------------
st.set_page_config(
    page_title="PEG Selector Demo",
    layout="wide"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv("peg_products_v2.csv")

# --------------------------------------------------
# App title
# --------------------------------------------------
st.title("PEG Selector Demo")
st.write("Select PEG properties to filter products.")

# --------------------------------------------------
# Sidebar Filters (v1 logic preserved)
# --------------------------------------------------
st.sidebar.header("Filter PEG Products")

# --- Keyword Search ---
search_query = st.sidebar.text_input(
    "Search Product Name",
    placeholder="e.g. PEG 20K NHS"
)

# --- Molecular Weight Slider ---
min_mw = int(df["Molecular Weight (kDa)"].min())
max_mw = int(df["Molecular Weight (kDa)"].max())

mw_range = st.sidebar.slider(
    "Molecular Weight (kDa)",
    min_value=min_mw,
    max_value=max_mw,
    value=(min_mw, max_mw)
)

# --- Multiselect Filters (chip-style UX) ---
partner_options = sorted(df["Commercial Partner"].dropna().unique())
architecture_options = sorted(df["Polymer Architecture"].dropna().unique())
reactivity_options = sorted(df["Functional Group / Reactivity"].dropna().unique())
application_options = sorted(df["Intended Application"].dropna().unique())

selected_partners = st.sidebar.multiselect(
    "Commercial Partner",
    partner_options
)

selected_architectures = st.sidebar.multiselect(
    "Polymer Architecture",
    architecture_options
)

selected_reactivities = st.sidebar.multiselect(
    "Functional Group / Reactivity",
    reactivity_options
)

selected_applications = st.sidebar.multiselect(
    "Intended Application",
    application_options
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

# Search
if search_query:
    filtered_df = filtered_df[
        filtered_df["Product Name"]
        .str.contains(search_query, case=False, na=False)
    ]

# Molecular weight
filtered_df = filtered_df[
    (filtered_df["Molecular Weight (kDa)"] >= mw_range[0]) &
    (filtered_df["Molecular Weight (kDa)"] <= mw_range[1])
]

# Categorical filters
if selected_partners:
    filtered_df = filtered_df[
        filtered_df["Commercial Partner"].isin(selected_partners)
    ]

if selected_architectures:
    filtered_df = filtered_df[
        filtered_df["Polymer Architecture"].isin(selected_architectures)
    ]

if selected_reactivities:
    filtered_df = filtered_df[
        filtered_df["Functional Group / Reactivity"].isin(selected_reactivities)
    ]

if selected_applications:
    filtered_df = filtered_df[
        filtered_df["Intended Application"].isin(selected_applications)
    ]

st.markdown(f"**Showing {len(filtered_df)} products**")

# --------------------------------------------------
# Product Display (Accordion / Dropdown)
# --------------------------------------------------
for _, row in filtered_df.iterrows():
    with st.expander(row["Product Name"]):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")
            st.markdown(f"**Molecular Weight (kDa):** {row['Molecular Weight (kDa)']}")
            st.markdown(f"**Functional Group / Reactivity:** {row['Functional Group / Reactivity']}")
            st.markdown(f"**Polymer Architecture:** {row['Polymer Architecture']}")
            st.markdown(f"**Solubility:** {row['Solubility']}")

        with col2:
            st.markdown(f"**Intended Application:** {row['Intended Application']}")
            st.markdown(f"**Application:** {row['Application']}")
            st.markdown(f"**Polydispersity Index (PDI):** {row['Polydispersity Index (PDI)']}")

        # Vendor URL
        if pd.notna(row["Product Page"]):
            st.markdown(
                f"🔗 **Vendor Product Page:** [View Product]({row['Product Page']})"
            )
