import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Título
st.title("📈 Dashboard de Vendas Interativo")
st.markdown("---")

# Carregar dados (exemplo)
@st.cache_data  # Cache para carregar dados apenas uma vez
def load_data():
    data = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", periods=90, freq="D"),
        "Produto": ["Celular", "Notebook", "Tablet", "Fone"] * 22 + ["Celular", "Notebook"],
        "Região": ["Norte", "Sul", "Leste", "Oeste"] * 22 + ["Norte", "Sul"],
        "Vendas": [100 + i*2 for i in range(90)],
        "Clientes": [50 + i for i in range(90)]
    })
    data["Mês"] = data["Data"].dt.month_name()
    return data

df = load_data()

# Sidebar (filtros)
st.sidebar.header("Filtros")
produto = st.sidebar.multiselect(
    "Selecione o Produto:",
    options=df["Produto"].unique(),
    default=df["Produto"].unique()
)

regiao = st.sidebar.multiselect(
    "Selecione a Região:",
    options=df["Região"].unique(),
    default=df["Região"].unique()
)

mes = st.sidebar.multiselect(
    "Selecione o Mês:",
    options=df["Mês"].unique(),
    default=df["Mês"].unique()
)

# Aplicar filtros
df_filtrado = df.query(
    "Produto == @produto & Região == @regiao & Mês == @mes"
)

# Métricas (KPI cards)
st.subheader("Métricas Principais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vendas", f"R$ {df_filtrado['Vendas'].sum():,.0f}")
col2.metric("Total de Clientes", df_filtrado['Clientes'].sum())
col3.metric("Média por Venda", f"R$ {df_filtrado['Vendas'].mean():,.2f}")

# Gráficos
st.markdown("---")
fig1 = px.line(
    df_filtrado,
    x="Data",
    y="Vendas",
    color="Produto",
    title="Vendas Diárias por Produto"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    df_filtrado.groupby("Região")["Vendas"].sum().reset_index(),
    x="Região",
    y="Vendas",
    title="Vendas por Região"
)
st.plotly_chart(fig2, use_container_width=True)

# Tabela interativa
st.markdown("---")
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado, hide_index=True)