"""
Objetivo: apresentar os dados sobre a economia dos países em dashboards
- Deve ser possível ver os dados mundiais por ano
- Deve ser possível ver os dados por país
"""

# imports
import streamlit as st
import pandas as pd
import plotly.express as px

# configurações da página
st.set_page_config(layout="wide")

# dataframe
df = pd.read_csv("project2/global_income_inequality.csv")

# organização dos dados
df["Year"] = pd.to_datetime(df["Year"], format="%Y").dt.year
df = df.sort_values("Year")

# dashboard
year = st.sidebar.selectbox("Ano", df["Year"].unique())

df_filter = df[df["Year"] == year]
df_filter = df_filter.sort_values("Country")
df_filter[["Country", "Population", "Average Income (USD)", "Income Group", "Gini Index", "Top 10% Income Share (%)"]]


# caixas
col1 = st.columns(1)[0]

# gráficos 

# gráfico de renda média anual[2024] A repository to save my small data science projects, specially data analysis of datasets from Kraggle. The projects are a way to practice what I'm currently learning in Data Science with online free courses.
df_mean = df.groupby("Year")["Average Income (USD)"].mean().reset_index()
fig_year = px.bar(df_mean, x="Year", y="Average Income (USD)", title="Renda média por ano")
col1.plotly_chart(fig_year)