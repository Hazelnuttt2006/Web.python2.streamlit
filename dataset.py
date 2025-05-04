import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header



def show():

    st.subheader("Business IT 2 | Python 2")
    st.title(':blue[Billionaires Statistics Dataset (2023)]')
    st.write("### Dataset Overview")
    st.write(
        "This dataset contains information on global billionaires in 2023, including their rank, net worth (in USD billions), age, country of citizenship, source of wealth, and industry. "
        "It provides valuable insights into wealth distribution, industry trends, and geographic concentrations of ultra-high net worth individuals."
    )

    colored_header(
        label="Dataset Variables 📝",
        description="Learn about the columns in the dataset",
        color_name="light-blue-70",
    )
    
    st.markdown("**1. `rank`**: Billionaire's rank in 2023 by net worth on Forbes list.")
    st.markdown("**2. `name`**: Full name of the billionaire.")
    st.markdown("**3. `net_worth`**: Net worth in USD billions.")
    st.markdown("**4. `age`**: Age of the billionaire in 2023.")
    st.markdown("**5. `country`**: Country of citizenship.")
    st.markdown("**6. `source`**: Primary source of wealth (e.g., Technology, Finance, Retail).")
    st.markdown("**7. `industry`**: Industry sector associated with the billionaire's wealth.")

    st.subheader("Preview and Filter Data")
    try:
        df = pd.read_csv('Billionaires Statistics Dataset.csv')
    except FileNotFoundError:
        st.error("Could not find the dataset file 'Billionaires Statistics Dataset.csv'. Make sure it is in the app directory.")
        return

    cols = df.columns.tolist()

    wealth_cols = ['net_worth','networth','finalWorth','finalworth']
    wcol = next((c for c in cols if c in wealth_cols), None)
    if wcol:
        df = df.rename(columns={wcol: 'net_worth'})

    icol = next((c for c in cols if c.lower() in ('industry','source')), None)
    if icol:
        df = df.rename(columns={icol: 'industry'})
    else:
        df['industry'] = 'Unknown'

    st.write("#### Data Preview")
    st.dataframe(df.head(5), use_container_width=True)

    st.write("---")
    with st.expander("🔍 Filter Options", expanded=False):
        countries = df['country'].fillna('Unknown').unique()
        sel_countries = st.multiselect("Country", options=countries, default=list(countries), key='country')
        min_w, max_w = float(df['net_worth'].min()), float(df['net_worth'].max())
        sel_range = st.slider("Net Worth (billion USD)", min_value=min_w, max_value=max_w, value=(min_w, max_w), key='worth')
        industries = df['industry'].unique()
        sel_industries = st.multiselect("Industry", options=industries, default=list(industries), key='ind')

    df_filtered = df[
        df['country'].isin(sel_countries) &
        df['net_worth'].between(sel_range[0], sel_range[1]) &
        df['industry'].isin(sel_industries)
    ]
    st.write(f"**Filtered records:** {len(df_filtered)}")
    st.dataframe(df_filtered, use_container_width=True)

    st.write("---")
    st.caption("Use the filters above (🔍) to explore billionaire characteristics by country, wealth, and industry.")



