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

def show():
    # --------- Age Group Wealth Analysis ---------
    st.title("\U0001F4B0 Which Age Group Holds the Most Wealth?")

    st.markdown(
    """
    <p style="font-size:16px;">
    This analysis showcases the top 10 billionaires by net worth, based on the 2023 dataset. The list highlights the wealthiest individuals across various age groups, ranked by their total wealth. The data reveals how these billionaires have accumulated massive fortunes, with younger billionaires benefitting from industries like technology and social media, while older billionaires often have diversified portfolios across multiple sectors. The top 10 showcase the diverse paths to achieving billionaire status, emphasizing how long-term growth, strategic investments, and industry dominance contribute to their financial success.
    </p>
    """, 
    unsafe_allow_html=True
)

    single_column = st.empty()

    with single_column:
        annotated_text(
            ("61+", "**age group**", "#FFD700"),
            " holds the ",
            ("largest", "*total*", "#FFD700"),
            " share of total billionaire net worth, underscoring the long-term nature of wealth accumulation.",
            "\n- ",
            ("Net worth grows consistently with age", "\U0001F4C8", "#FFD700"),
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
    selected_group = st.selectbox("\U0001F3AF Select Age Group", age_groups)

    filtered_df = df.copy()
    if selected_group != "All":
        filtered_df = df[df["Age Group"] == selected_group]

    filtered_df = filtered_df.dropna(subset=["NetWorth"])

    top10 = filtered_df.sort_values(by="NetWorth", ascending=False).head(10)
    top10 = top10.assign(Rank=top10['NetWorth'].rank(ascending=False, method='min').astype(int))

    key_insights = {
        "Under 20":"✅ **Under 20 Age Group**\nBillionaires under 20 are a rare and unique group, often driven by innovation in technology, gaming, or even social media platforms...",
        "21–30": "✅ **21-30 Age Group**\nThis youngest billionaire group represents a small portion of total wealth but signals a promising rise of tech-savvy entrepreneurs...",
        "31–40": "✅ **31-40 Age Group**\nBillionaires aged 31–40 begin to show more influence on the overall wealth landscape...",
        "41–50": "✅ **41-50 Age Group**\nThis age group marks a transition toward wealth consolidation...",
        "51–60": "✅ **51-60 Age Group**\nWith decades of experience, billionaires in their 50s often have diversified portfolios and stable positions...",
        "61+": "✅ **60+ Age Group**\nThis is the most affluent age group, holding the largest share of total billionaire wealth..."
    }

    if selected_group != "All":
        st.markdown(key_insights.get(selected_group, ""))
    else:
        st.markdown("Select an age group to view key insights.")

    fig = px.bar(
        top10,
        x="Age",
        y="NetWorth",
        hover_name="Name",
        hover_data={"NetWorth": True, "Age": True, "Name": False},
        color="Age",
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
            st.subheader("\U0001F4CA Top 10 Billionaires")
        else:
            st.subheader(f"\U0001F4CA Top Billionaires in {selected_group} Group")

        st.dataframe(
            top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
            use_container_width=True
        )

    st.markdown("---")

    # --------- Gender Ratio Analysis ---------
    st.title("\U0001F30D How Are Billionaires Around The World Distributed By Gender?")

    st.markdown("""
    This dashboard analyzes the gender distribution of worldwide billionaires based on 2023 data...
    """)

    countries = df['country'].value_counts().index.tolist()
    selected_country = st.selectbox("Select a country:", countries, key="country_select")

    df_country = df[df['country'] == selected_country]

    gender_counts = df_country['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    gender_counts['Percentage'] = (gender_counts['Count'] / gender_counts['Count'].sum() * 100).round(2)

    fig_pie = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=f"Gender Distribution of Billionaires in {selected_country}"
    )
    fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', pull=[0.05] * len(gender_counts))
    fig_pie.update_layout(showlegend=False)

    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader(f"Gender Statistics Table in {selected_country}")
    st.dataframe(gender_counts, use_container_width=True)

    st.markdown("---")

    # --------- Lollipop Chart: Industry vs Self-Made ---------
    st.title("🏭 Are Self-Made Billionaires Concentrated in Certain Industries?")

    st.markdown("""
    This section analyzes how billionaires are distributed across industries based on their self-made status.  
    You can use the dropdown to filter between self-made and non-self-made individuals.  
    The **lollipop chart** clearly shows which industries foster self-made success stories versus inherited wealth.
    """)

    # Prepare data for lollipop chart
    count_df = df.groupby(['industries', 'selfMade']).size().reset_index(name='count')

    self_made_options = count_df['selfMade'].unique().tolist()
    selected_self_made = st.selectbox('🔍 Select Self-Made Status:', self_made_options)

    filtered_df = count_df[count_df['selfMade'] == selected_self_made]
    filtered_df = filtered_df.sort_values('count', ascending=True)

    fig_lollipop = go.Figure()

    # Add stems
    fig_lollipop.add_trace(go.Scatter(
        x=filtered_df['count'],
        y=filtered_df['industries'],
        mode='lines',
        line=dict(color='gray', width=2),
        showlegend=False
    ))

    # Add markers
    fig_lollipop.add_trace(go.Scatter(
        x=filtered_df['count'],
        y=filtered_df['industries'],
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Billionaires'
    ))

    fig_lollipop.update_layout(
        xaxis_title='Number of Billionaires',
        yaxis_title='Industry',
        title=f'Lollipop Chart for Self-Made Status: {selected_self_made}',
        template='plotly_white',
        height=600
    )

    st.plotly_chart(fig_lollipop, use_container_width=True)

    st.subheader(f"📋 Industry Table - Self-Made Billionaires: {selected_self_made}")

    # Loại bỏ cột 'selfMade' trước khi hiển thị bảng
    filtered_df_display = filtered_df.drop(columns=['selfMade']).reset_index(drop=True)

    st.dataframe(filtered_df_display, use_container_width=True)
