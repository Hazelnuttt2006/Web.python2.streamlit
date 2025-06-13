import streamlit as st
import pandas as pd
import plotly.express as px
from annotated_text import annotated_text
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("Billionaires Statistics Dataset.csv", encoding="utf-8-sig")
    df.rename(columns={
        'finalWorth': 'NetWorth',
        'personName': 'Name',
        'age': 'Age',
        'gender': 'Gender'
    }, inplace=True)
    df = df.dropna(subset=["Age", "NetWorth", "Gender", "country"])
    df['gender'] = df['Gender'].replace({"M": "Male", "F": "Female"})
    return df

df = load_data()

# ✅ Add the missing key_insights dictionary here:
key_insights = {
    "Under 20": "👶 Billionaires under 20 are extremely rare and often come from inherited wealth.",
    "21–30": "💡 Tech and crypto have enabled young founders in this age group to build massive fortunes quickly.",
    "31–40": "🚀 This group includes fast-growing entrepreneurs and innovators scaling global businesses.",
    "41–50": "📈 Typically successful business leaders with well-established companies and diversified investments.",
    "51–60": "🏢 Senior executives and serial entrepreneurs dominate this age group.",
    "61+": "📊 The wealthiest age group overall, often due to decades of compounding and industry dominance."
}

def show():
    # --------- Age Group Wealth Analysis ---------
    st.title("💰 Which Age Group Holds the Most Wealth?")

    st.markdown("""
    <p style="font-size:16px;">
    This analysis showcases the top 10 billionaires by net worth, based on the 2023 dataset. The list highlights the wealthiest individuals across various age groups, ranked by their total wealth. The data reveals how these billionaires have accumulated massive fortunes, with younger billionaires benefitting from industries like technology and social media, while older billionaires often have diversified portfolios across multiple sectors.
    </p>
    """, unsafe_allow_html=True)

    with st.expander("📘 Detailed Insights about Age & Wealth"):
        annotated_text(
            ("61+", "**age group**", "#FFD700"),
            " holds the ",
            ("largest", "*total*", "#FFD700"),
            " share of total billionaire net worth.",
            "\n- ",
            ("Net worth grows with age", "📈", "#FFD700"),
            ", especially ",
            ("after age", "**40**", "#FFD700"),
            ".",
            "\n- ",
            ("Under-30 billionaires", "**remain rare**", "#FFD700"),
            ", despite media attention.",
            "\n- ",
            ("Wealth often peaks", "**after age 50**", "#FFD700"),
            ", reflecting compounding and long-term growth."
        )

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

    age_groups = ["All", "Under 20", "21–30", "31–40", "41–50", "51–60", "61+"]
    colA, colB = st.columns([1, 3])
    with colA:
        selected_group = st.selectbox("🎯 Select Age Group", age_groups)
    with colB:
        st.markdown("""<br>""", unsafe_allow_html=True)
        if selected_group != "All":
            st.markdown(key_insights.get(selected_group, ""))
        else:
            st.markdown("Select an age group to view key insights.")

    filtered_df = df.copy()
    if selected_group != "All":
        filtered_df = df[df["Age Group"] == selected_group]

    filtered_df = filtered_df.dropna(subset=["NetWorth"])

    top10 = filtered_df.sort_values(by="NetWorth", ascending=False).head(10)
    top10 = top10.assign(Rank=top10['NetWorth'].rank(ascending=False, method='min').astype(int))

    fig = px.bar(
        top10,
        x="Age",
        y="NetWorth",
        hover_name="Name",
        hover_data={"NetWorth": True, "Age": True, "Name": False},
        color="Age",
        color_continuous_scale=px.colors.sequential.Tealgrn
    )
    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Net Worth (Billion $)",
        hoverlabel=dict(bgcolor="black", font_color="white", font_size=12)
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if selected_group == "All":
            st.subheader("📊 Top 10 Billionaires")
        else:
            st.subheader(f"📊 Top Billionaires in {selected_group} Group")

        st.dataframe(
            top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
            use_container_width=True
        )

    st.markdown("---")

    # --------- Gender Ratio Analysis ---------
    st.title("🌍 How Are Billionaires Around The World Distributed By Gender?")

    st.markdown("""
    This dashboard analyzes the gender distribution of worldwide billionaires based on 2023 data.

    - **Male billionaires vastly outnumber female billionaires**, accounting for over **85–90%** of the ultra-wealthy population.
    - **Developed countries** tend to have higher female representation compared to emerging economies.
    - The **gender gap is narrowing** among younger generations.
    """)

    countries = df['country'].value_counts().index.tolist()
    selected_country = st.selectbox("🌐 Select a country:", options=["Top 10"] + countries, key="country_select")

    if selected_country == "Top 10":
        top10_countries = df['country'].value_counts().head(10).index.tolist()
        st.markdown("Showing average of top 10 countries.")
        df_country = df[df['country'].isin(top10_countries)]
    else:
        df_country = df[df['country'] == selected_country]

    gender_counts = df_country['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    gender_counts['Percentage'] = (gender_counts['Count'] / gender_counts['Count'].sum() * 100).round(2)

    fig_pie = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        hole=0.5,
        color_discrete_sequence=['#1f77b4', '#ff7f0e'],
        title=f"Gender Distribution of Billionaires in {selected_country}"
    )
    fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', pull=[0.05] * len(gender_counts))
    fig_pie.update_layout(showlegend=False)

    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader(f"📋 Gender Statistics Table in {selected_country}")
    st.dataframe(gender_counts, use_container_width=True)

    st.markdown("---")

    # --------- Lollipop Chart: Industry vs Self-Made ---------
    st.title("🏭 Are Self-Made Billionaires Concentrated in Certain Industries?")

    st.markdown("""
    This section analyzes how billionaires are distributed across industries based on their self-made status.  
    Use the checkboxes to filter between self-made and non-self-made billionaires.
    """)

    count_df = df.groupby(['industries', 'selfMade']).size().reset_index(name='count')
    self_made_options = sorted(count_df['selfMade'].unique().tolist())

    selected_true = st.checkbox("Show Self-Made: True", value=True)
    selected_false = st.checkbox("Show Self-Made: False", value=True)

    fig_lollipop = go.Figure()

    for status, color in zip([True, False], ['blue', 'orange']):
        if (status and selected_true) or (not status and selected_false):
            temp_df = count_df[count_df['selfMade'] == status].sort_values('count', ascending=True)
            fig_lollipop.add_trace(go.Scatter(
                x=temp_df['count'],
                y=temp_df['industries'],
                mode='lines+markers',
                line=dict(color='gray', width=2),
                marker=dict(color=color, size=10),
                name=f'Self-Made: {status}'
            ))

    fig_lollipop.update_layout(
        xaxis_title='Number of Billionaires',
        yaxis_title='Industry',
        title='Lollipop Chart by Self-Made Status',
        template='plotly_white',
        height=600
    )

    st.plotly_chart(fig_lollipop, use_container_width=True)

    st.subheader("📋 Industry Breakdown Table")
    display_df = count_df.copy()
    if not selected_true:
        display_df = display_df[display_df['selfMade'] != True]
    if not selected_false:
        display_df = display_df[display_df['selfMade'] != False]

    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
