import streamlit as st
import pandas as pd
import os

def show():
    st.subheader("Business IT 2 | Python 2")

    # === Custom Styling ===
    st.markdown("""
        <style>
        .custom-title {
            color: black;
            font-weight: bold;
            font-size: 50px;
            margin-bottom: 0px;
        }
        .custom-line {
            border-bottom: 5px solid #fbc02d;
            margin-top: 5px;
            margin-bottom: 25px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-title">Billionaires Statistics Dataset (2023)</div>', unsafe_allow_html=True)

    # === Introduction ===
    with st.expander("📘 How to Use This App", expanded=False):
        st.markdown("""
        - This app displays insights from the 2023 Billionaires dataset.
        - Use the **Filter Options** below to explore data based on country, net worth, and industry.
        - You can select multiple values in each filter. The table updates automatically.
        - If no data appears, try widening your filter range.
        """)

    st.write("### Dataset Overview")
    st.write(
        "This dataset contains information on global billionaires in 2023, including their rank, net worth (in USD billions), age, country of citizenship, source of wealth, and industry. "
        "It provides valuable insights into wealth distribution, industry trends, and geographic concentrations of ultra-high net worth individuals."
    )

    # === Dataset Variables ===
    st.write("### Dataset Variables 📝")
    st.markdown('<div class="custom-line"></div>', unsafe_allow_html=True)
    st.markdown("**1. `rank`**: Billionaire's rank in 2023 by net worth on Forbes list.")
    st.markdown("**2. `name`**: Full name of the billionaire.")
    st.markdown("**3. `net_worth`**: Net worth in USD billions.")
    st.markdown("**4. `age`**: Age of the billionaire in 2023.")
    st.markdown("**5. `country`**: Country of citizenship.")
    st.markdown("**6. `source`**: Primary source of wealth (e.g., Technology, Finance, Retail).")
    st.markdown("**7. `industry`**: Industry sector associated with the billionaire's wealth.")

    # === Load Dataset ===
    st.subheader("Preview and Filter Data")

    @st.cache_data
    def load_data():
        file_path = os.path.join(os.getcwd(), "Billionaires Statistics Dataset.csv")
        return pd.read_csv(file_path)

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Could not find the dataset file 'Billionaires Statistics Dataset.csv'. Make sure it is in the app directory.")
        return

    # === Preprocessing ===
    df.columns = [col.strip().lower() for col in df.columns]
    wealth_cols = ['net_worth', 'networth', 'finalworth', 'finalworth']
    for col in wealth_cols:
        if col in df.columns:
            df = df.rename(columns={col: 'net_worth'})
            break

    if 'industry' not in df.columns:
        if 'source' in df.columns:
            df = df.rename(columns={'source': 'industry'})
        else:
            df['industry'] = 'Unknown'

    df['country'] = df['country'].fillna('Unknown')
    df['industry'] = df['industry'].fillna('Unknown')

    # === Preview ===
    st.write("#### Data Preview (First 5 Rows)")
    st.dataframe(df.head(5), use_container_width=True)

    # === Filter UI ===
    st.write("---")
    st.write("Use the filter options below to explore specific subsets of billionaires based on their country, net worth, and industry.")
    
    with st.expander("🔍 Filter Options", expanded=False):
        # Country filter
        countries = sorted(df['country'].unique())
        sel_countries = st.multiselect(
            "🌍 Select Country (searchable):",
            options=countries,
            default=countries[:10],
            help="Select one or more countries to see billionaires holding that nationality."
        )

        # Net worth slider
        min_w, max_w = float(df['net_worth'].min()), float(df['net_worth'].max())
        sel_range = st.slider(
            "💰 Select Net Worth Range (in billion USD):",
            min_value=min_w,
            max_value=max_w,
            value=(min_w, max_w),
            step=0.5,
            help="Adjust to include only billionaires whose net worth falls within this range."
        )

        # Industry filter
        industries = sorted(df['industry'].unique())
        sel_industries = st.multiselect(
            "🏭 Select Industry:",
            options=industries,
            default=industries[:8],
            help="Choose industries that represent the primary wealth sector of the billionaires."
        )

    # === Filtering ===
    df_filtered = df[
        df['country'].isin(sel_countries) &
        df['net_worth'].between(sel_range[0], sel_range[1]) &
        df['industry'].isin(sel_industries)
    ]

    if df_filtered.empty:
        st.warning("No records found. Try adjusting the filters.")
    else:
        st.write(f"**Filtered records:** {len(df_filtered)}")
        st.dataframe(df_filtered, use_container_width=True)

    # === Optional Chart ===
    if st.checkbox("📊 Show industry distribution chart"):
        st.bar_chart(df_filtered['industry'].value_counts())

    st.write("---")
    st.caption("Use the filters above (🔍) to explore billionaire characteristics by country, wealth, and industry.")


