import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from annotated_text import annotated_text

def show():
    # Custom styling
    st.markdown("""
        <style>
            h1, .stTitle, .stSubheader {
                color: #140f00 !important;
            }
            .custom-header {
                font-size: 24px;
                font-weight: bold;
                color: #140f00;
                margin: 10px 0 5px 0;
            }
            .custom-subtitle {
                font-size: 18px;
                font-weight: bold;
                margin: 0 0 10px 0;
            }
            hr.custom-hr {
                border: 2px solid gold;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("Business IT 2 | Python 2")
    st.title('Billionaires Statistics - 2023')

    st.write(" ")

    colored_header(
        label="An introduction 💡",
        description="Overview of Billionaires around the world in 2023",
        color_name="yellow-70",
    )

    annotated_text(
        ("Billionaires", "💸", "#FFC200"),
        ", are individuals whose net worth is at least 1 billion USD. In 2023, the global billionaire population saw significant growth despite economic challenges. The dataset provides insights into the distribution of billionaires across countries and their net worth.",
        ("Country-wise", "🌍", "#FFC200"),
        ", billionaires' data reveals how wealth is concentrated in various regions."
    )
    annotated_text(
        "The United States has the highest number of billionaires, followed by China, and a variety of emerging markets are also seeing a rise in billionaires.",
        "Billionaires' wealth is often tied to industries such as technology, finance, and healthcare."
    )

    colored_header(
        label="The Billionaire Economy 💰",
        description="Understanding the distribution and net worth of billionaires globally in 2023",
        color_name="yellow-70",
    )

    single_column2 = st.container()
    with single_column2:
        st.write("In 2023, global wealth distribution among billionaires is increasingly diverse. While traditionally dominated by the US and China, emerging economies are seeing a growing share of ultra-wealthy individuals.")
        annotated_text(
            "Over 2,700 billionaires globally, with an aggregate net worth surpassing trillions of dollars, represent industries ranging from technology to healthcare."
        )

    # ---------- Billionaire Count by Country ----------
    st.markdown("<div class='custom-header'>Billionaires by Country (2023)</div>", unsafe_allow_html=True)
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
    st.markdown("<div class='custom-subtitle'>Billionaire Count by Country</div>", unsafe_allow_html=True)

    try:
        load = pd.read_csv('Billionaires Statistics Dataset.csv')
    except FileNotFoundError:
        st.error("Dataset file 'Billionaires Statistics Dataset.csv' not found.")
        return

    country_info = {
        'country_code': ['USA', 'CHN', 'IND', 'GER', 'BRZ', 'FRA', 'JPN', 'CAN', 'RUS', 'UK'],
        'country': ['United States', 'China', 'India', 'Germany', 'Brazil', 'France', 'Japan', 'Canada', 'Russia', 'United Kingdom']
    }

    country_info = pd.DataFrame(country_info)
    load = load.dropna(subset=['country'])

    df1 = load.merge(country_info, on='country', how='left')

    billionaire_count = df1['country'].value_counts().reset_index()
    billionaire_count.columns = ['country', 'Billionaire_Count']

    df1 = df1.merge(billionaire_count, on='country', how='left')

    fig1 = px.choropleth(
        df1,
        locations='country_code',
        locationmode="country names",
        color='Billionaire_Count',
        color_continuous_scale="agsunset_r",
        labels={'Billionaire_Count': 'Number of Billionaires'},
        hover_name='country',
        hover_data=["country", "Billionaire_Count"]
    )
    st.plotly_chart(fig1)

    # ---------- Billionaire Net Worth by Country ----------
    st.markdown("<div class='custom-header' style='margin-top: 30px;'>Billionaire Net Worth by Country</div>", unsafe_allow_html=True)
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
    st.markdown("<div class='custom-subtitle'>Billionaire Net Worth Distribution in 2023</div>", unsafe_allow_html=True)

    fig2 = px.choropleth(
        df1,
        locations='country_code',
        locationmode="country names",
        color='finalWorth',
        color_continuous_scale="Viridis_r",
        labels={'finalWorth': 'Net Worth (in Billion USD)'},
        hover_name='country',
        hover_data=["country", "finalWorth"]
    )
    st.plotly_chart(fig2)
