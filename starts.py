import streamlit as st
import pandas as pd
import plotly.express as px
from annotated_text import annotated_text

def show():
    st.title("💰 Which Age Group Holds the Most Wealth?")

    # Using annotated_text to highlight parts of the paragraph
    st.markdown(""" 
    This analysis showcases the top 10 billionaires by net worth, based on the 2023 dataset. The list highlights the wealthiest individuals across various age groups, ranked by their total wealth. The data reveals how these billionaires have accumulated massive fortunes, with younger billionaires benefitting from industries like technology and social media, while older billionaires often have diversified portfolios across multiple sectors. The top 10 showcase the diverse paths to achieving billionaire status, emphasizing how long-term growth, strategic investments, and industry dominance contribute to their financial success.

    ---
    """, unsafe_allow_html=True)

    # Create an empty container
    single_column = st.empty()

    # Use annotated_text to highlight certain words in the container
    with single_column:
        annotated_text(
            ("61+", "**age group**", "#FFD700"),
            " holds the ",
            ("largest", "*total*", "#FFD700"),
            " share of total billionaire net worth, underscoring the long-term nature of wealth accumulation.",
            "\n- ",
            ("Net worth grows consistently with age", "📈", "#FFD700"),
            ", with sharp increases observed ",
            ("after age", "**40**", "#FFD700"),
            ".",
            "\n- ",
            ("Billionaires under 30 remain" , "**a minority**", "#FFD700"),
            ", contributing a small share despite media attention on young tech founders.",
            "\n- ",
            ("Wealth consolidation typically peaks", "**after age 50**", "#FFD700"),
            ", highlighting the power of compounding and strategic financial planning."
        )

    # Load data
    df = pd.read_csv("Billionaires Statistics Dataset.csv", encoding="utf-8-sig")

    # Normalize column names
    df.rename(columns={
        'finalWorth': 'NetWorth',
        'personName': 'Name',
        'age': 'Age',
        'gender': 'Gender'
    }, inplace=True)

    df = df.dropna(subset=["Age", "NetWorth", "Gender"])

    # Define the age group
    def get_age_group(age):
        if age <= 20:
            return "Under 20"
        elif age <= 30:
            return "21–30"
        elif age <= 40:
            return "31–40"
        elif age <= 50:
            return "41–50"
        elif age <= 60:
            return "51–60"
        else:
            return "61+"

    df["Age Group"] = df["Age"].apply(get_age_group)

    # Filter by age group
    age_groups = ["All", "Under 20", "21–30", "31–40", "41–50", "51–60", "61+"]
    selected_group = st.selectbox("🎯 Select Age Group", age_groups)

    filtered_df = df.copy()
    if selected_group != "All":
        filtered_df = df[df["Age Group"] == selected_group]

    # Top 10
    top10 = filtered_df.sort_values(by="NetWorth", ascending=False).head(10)
    top10['Rank'] = top10['NetWorth'].rank(ascending=False, method='min')

    # Plot the graph
    fig = px.bar(
        top10,
        x="Age",
        y="NetWorth",
        hover_name="Name",
        hover_data={"NetWorth": True, "Age": True, "Name": False},
        color="Age",
        title=f"Top 10 Billionaires by Net Worth in {selected_group} Age Group"
    )
    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Net Worth (Billion $)",
        hoverlabel=dict(bgcolor="black", font_color="white", font_size=12)
    )

    # Display the graph and table
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("📊 Top 10 Billionaires")
        st.dataframe(
            top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
            use_container_width=True
        )
