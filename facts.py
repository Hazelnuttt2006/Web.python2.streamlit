import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from annotated_text import annotated_text
import os
import base64  # Missing import

# ---------------------- DATA LOADING & PROCESSING ----------------------
@st.cache_data
def load_data():
    file_path = "Billionaires Statistics Dataset.csv"
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    df = df.dropna(subset=['country'])

    country_info = {
        'country_code': ['USA', 'CHN', 'IND', 'GER', 'BRA', 'FRA', 'JPN', 'CAN', 'RUS', 'GBR'],
        'country': ['United States', 'China', 'India', 'Germany', 'Brazil', 'France', 'Japan', 'Canada', 'Russia', 'United Kingdom']
    }
    country_df = pd.DataFrame(country_info)
    df = df.merge(country_df, on='country', how='left')

    count_df = df['country'].value_counts().reset_index()
    count_df.columns = ['country', 'Billionaire_Count']
    df = df.merge(count_df, on='country', how='left')

    if 'finalWorth' in df.columns:
        df['finalWorth'] = pd.to_numeric(df['finalWorth'], errors='coerce').fillna(0)
    else:
        df['finalWorth'] = 0

    return df

# ---------------------- PAGE LAYOUT & VISUALIZATION ----------------------
def show():
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
    st.title("Billionaires Statistics - 2023")
    st.markdown("### 🌟 Top 3 Richest Billionaires in 2023")

    billionaires = [
        {"name": "Jeff Bezos", "net_worth": "$160B", "image": "jeff_bezos.jpg"},
        {"name": "Elon Musk", "net_worth": "$250B", "image": "elon_musk.jpg"},
        {"name": "Bernard Arnault", "net_worth": "$220B", "image": "bernard_arnault.jpg"}
    ]

    col1, col2, col3 = st.columns(3)
    for i, b in enumerate(billionaires):
        with [col1, col2, col3][i]:  # Proper indentation
            if os.path.exists(b["image"]):
                st.markdown(
                    f"""
                    <div style='text-align: center;'>
                        <img src="data:image/jpeg;base64,{base64.b64encode(open(b["image"], "rb").read()).decode()}"
                             style="width:200px; height:250px; object-fit:cover; border-radius:12px;" />
                        <p style="margin-top: 8px; font-size: 16px; color: gray;">{b['name']} – {b['net_worth']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning(f"Image not found: {b['image']}")

    colored_header("An introduction 💡", "Overview of Billionaires around the world in 2023", color_name="yellow-70")

    annotated_text(
        ("Billionaires", "💸", "#FFC200"),
        ", are individuals whose net worth exceeds 1 billion USD. Despite global economic challenges, the billionaire population grew significantly in 2023.",
        ("Country-wise", "🌍", "#FFC200"),
        ", the data shows how wealth is distributed around the world."
    )

    annotated_text(
        "The United States remains the leader in billionaire count, followed by China. "
        "Many emerging economies are also witnessing a rise in billionaires. "
        "Major industries include technology, finance, and healthcare."
    )

    colored_header("The Billionaire Economy 💰", "Understanding global billionaire distribution and wealth in 2023", color_name="yellow-70")
    st.write("In 2023, global billionaire wealth became more diverse. While still led by the US and China, more countries are now home to ultra-wealthy individuals.")
    annotated_text("More than 2,700 billionaires around the world have a combined net worth in the trillions of dollars, spanning industries like tech and healthcare.")

    df = load_data()
    if df is None:
        st.error("❌ Dataset file 'Billionaires Statistics Dataset.csv' not found.")
        return

    st.markdown("<div class='custom-header'>Billionaires by Country (2023)</div>", unsafe_allow_html=True)
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
    st.markdown("<div class='custom-subtitle'>Billionaire Count by Country</div>", unsafe_allow_html=True)

    fig_count = px.choropleth(
        df,
        locations='country_code',
        locationmode="ISO-3",
        color='Billionaire_Count',
        color_continuous_scale="YlOrBr",
        labels={'Billionaire_Count': 'Number of Billionaires'},
        hover_name='country',
        hover_data=["country", "Billionaire_Count"]
    )
    st.plotly_chart(fig_count)
    st.caption("📺 This map shows the number of billionaires per country (2023).")

    st.markdown("<div class='custom-header' style='margin-top: 30px;'>Billionaire Net Worth by Country</div>", unsafe_allow_html=True)
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
    st.markdown("<div class='custom-subtitle'>Billionaire Net Worth Distribution (2023)</div>", unsafe_allow_html=True)

    fig_wealth = px.choropleth(
        df,
        locations='country_code',
        locationmode="ISO-3",
        color='finalWorth',
        color_continuous_scale="YlOrBr",
        labels={'finalWorth': 'Net Worth (in Billion USD)'},
        hover_name='country',
        hover_data=["country", "finalWorth"]
    )
    st.plotly_chart(fig_wealth)
    st.caption("🌎 This map displays the total billionaire net worth per country in 2023.")

# ---------------------- RUN APP ----------------------
if __name__ == "__main__":
    show()

