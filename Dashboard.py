import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="SDG 7 Dashboard",
    layout="wide"
)

st.title("🌱 SDG 7: Affordable and Clean Energy Dashboard")

# Load data
df = pd.read_csv("cleaned_energy_data.csv")

# Sidebar
st.sidebar.header("Filters")

selected_year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].max())
)

filtered_df = df[df["Year"] == selected_year]

# KPI Section
st.subheader(f"Key Indicators ({selected_year})")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Renewable Share (%)",
    round(filtered_df["Renewable_Share"].mean(), 2)
)

col2.metric(
    "Average GDP per Capita",
    round(filtered_df["GDP_per_Capita"].mean(), 2)
)

col3.metric(
    "Average CO₂ Emissions",
    round(filtered_df["CO2_Emissions"].mean(), 2)
)

st.divider()

# Renewable Share by Country
st.subheader("Renewable Energy Share by Country")

fig1 = px.bar(
    filtered_df.sort_values(
        "Renewable_Share",
        ascending=False
    ),
    x="Country Name",
    y="Renewable_Share",
    title=f"Renewable Energy Share ({selected_year})"
)

st.plotly_chart(fig1, use_container_width=True)

# GDP vs Renewable Share
st.subheader("GDP per Capita vs Renewable Energy")

fig2 = px.scatter(
    filtered_df,
    x="GDP_per_Capita",
    y="Renewable_Share",
    hover_name="Country Name",
    size="Electricity_Access",
    title="GDP per Capita vs Renewable Energy Share"
)

st.plotly_chart(fig2, use_container_width=True)

# CO2 vs Renewable Share
st.subheader("CO₂ Emissions vs Renewable Energy")

fig3 = px.scatter(
    filtered_df,
    x="CO2_Emissions",
    y="Renewable_Share",
    hover_name="Country Name",
    title="CO₂ Emissions vs Renewable Energy Share"
)

st.plotly_chart(fig3, use_container_width=True)

# Country Trend
st.subheader("Renewable Energy Trend Over Time")

country = st.selectbox(
    "Select Country",
    sorted(df["Country Name"].unique())
)

country_df = df[df["Country Name"] == country]

fig4 = px.line(
    country_df,
    x="Year",
    y="Renewable_Share",
    markers=True,
    title=f"{country} Renewable Energy Trend"
)

st.plotly_chart(fig4, use_container_width=True)

# Correlation Heatmap
st.subheader("Correlation Between Variables")

corr = df[
    [
        "Renewable_Share",
        "GDP_per_Capita",
        "Electricity_Access",
        "Urban_Population",
        "CO2_Emissions",
        "Energy_Consumption"
    ]
].corr()

fig5 = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Matrix"
)

st.plotly_chart(fig5, use_container_width=True)

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())