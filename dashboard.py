"""
dashboard.py — Visualização das despesas do MEC (2020–2024)
Ferramenta: Streamlit + Plotly
Fonte: Portal da Transparência do Governo Federal
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Despesas MEC | Portal da Transparência",
    page_icon="🏛️",
    layout="wide",
)

# ── Dados ──────────────────────────────────────────────────────────────────────

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/despesas_consolidado.csv")
    return df

df = carregar_dados()

# ── Cabeçalho ──────────────────────────────────────────────────────────────────

st.title("🏛️ Despesas do Ministério da Educação")
st.caption("Fonte: Portal da Transparência do Governo Federal · Código SIAFI 26000 · 2020–2024")
st.divider()

# ── Filtros na sidebar ─────────────────────────────────────────────────────────

st.sidebar.header("Filtros")

anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano",
    options=anos_disponiveis,
    default=anos_disponiveis,
)

orgaos_disponiveis = sorted(df["orgao"].unique())
orgao_selecionado = st.sidebar.selectbox(
    "Órgão (para análise individual)",
    options=["Todos"] + orgaos_disponiveis,
)

# Aplica filtro de ano
df_filtrado = df[df["ano"].isin(anos_selecionados)]

st.sidebar.divider()
st.sidebar.markdown("**Dados carregados**")
st.sidebar.markdown(f"- {len(df_filtrado)} registros")
st.sidebar.markdown(f"- {df_filtrado['orgao'].nunique()} órgãos")
st.sidebar.markdown(f"- {len(anos_selecionados)} ano(s)")

# ── KPIs ───────────────────────────────────────────────────────────────────────

total_emp = df_filtrado["empenhado"].sum()
total_liq = df_filtrado["liquidado"].sum()
total_pago = df_filtrado["pago"].sum()
taxa_exec = total_liq / total_emp * 100 if total_emp > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Empenhado", f"R$ {total_emp/1e9:.1f}B")
col2.metric("Total Liquidado", f"R$ {total_liq/1e9:.1f}B")
col3.metric("Total Pago", f"R$ {total_pago/1e9:.1f}B")
col4.metric("Taxa de Execução", f"{taxa_exec:.1f}%", help="Liquidado ÷ Empenhado")

st.divider()

# ── Gráfico 1: Evolução anual ──────────────────────────────────────────────────

st.subheader("Evolução Anual da Execução Orçamentária")
st.caption("Auxilia decisões de planejamento orçamentário e identificação de tendências de subexecução.")

anual = df_filtrado.groupby("ano")[["empenhado", "liquidado", "pago"]].sum().reset_index()
anual_melted = anual.melt(id_vars="ano", var_name="Tipo", value_name="Valor")
anual_melted["Valor (R$ B)"] = anual_melted["Valor"] / 1e9

fig_linha = px.line(
    anual_melted,
    x="ano", y="Valor (R$ B)", color="Tipo",
    markers=True,
    color_discrete_map={"empenhado": "#3B82F6", "liquidado": "#10B981", "pago": "#F59E0B"},
    labels={"ano": "Ano", "Valor (R$ B)": "R$ Bilhões", "Tipo": ""},
)
fig_linha.update_layout(hovermode="x unified", legend_title_text="")
st.plotly_chart(fig_linha, use_container_width=True)

# ── Gráfico 2 e 3 lado a lado ─────────────────────────────────────────────────

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Taxa de Execução por Ano")
    st.caption("Indica se o orçamento autorizado está sendo efetivamente executado.")

    fig_taxa = go.Figure()
    fig_taxa.add_trace(go.Bar(
        x=anual["ano"], y=(anual["liquidado"] / anual["empenhado"] * 100).round(1),
        name="% Liquidado/Emp.", marker_color="#8B5CF6"
    ))
    fig_taxa.add_trace(go.Bar(
        x=anual["ano"], y=(anual["pago"] / anual["empenhado"] * 100).round(1),
        name="% Pago/Emp.", marker_color="#EC4899"
    ))
    fig_taxa.update_layout(
        barmode="group", yaxis_range=[60, 105],
        yaxis_ticksuffix="%", legend_title_text="",
        xaxis_title="Ano"
    )
    st.plotly_chart(fig_taxa, use_container_width=True)

with col_b:
    st.subheader("Distribuição por Órgão (2024)")
    st.caption("Mostra a concentração de gastos entre os órgãos vinculados ao MEC.")

    df24 = df_filtrado[df_filtrado["ano"] == max(anos_selecionados)] if anos_selecionados else df_filtrado
    pie_df = df24.groupby("orgao")["pago"].sum().nlargest(8).reset_index()
    resto = df24.groupby("orgao")["pago"].sum().iloc[8:].sum()
    if resto > 0:
        pie_df = pd.concat([pie_df, pd.DataFrame([{"orgao": "Demais órgãos", "pago": resto}])], ignore_index=True)

    fig_pizza = px.pie(
        pie_df, names="orgao", values="pago",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig_pizza.update_traces(textinfo="percent", hovertemplate="%{label}<br>R$ %{value:,.0f}<extra></extra>")
    st.plotly_chart(fig_pizza, use_container_width=True)

# ── Gráfico 4: Top 10 órgãos ──────────────────────────────────────────────────

st.subheader("Top 10 Órgãos por Valor Pago (Acumulado)")
st.caption("Ranking que apoia decisões de priorização, auditoria e alocação de recursos.")

top10 = df_filtrado.groupby("orgao")["pago"].sum().nlargest(10).reset_index().sort_values("pago")
top10["pago_bi"] = top10["pago"] / 1e9

fig_top10 = px.bar(
    top10, x="pago_bi", y="orgao", orientation="h",
    text=top10["pago_bi"].apply(lambda v: f"R$ {v:.1f}B"),
    color="pago_bi",
    color_continuous_scale="Blues",
    labels={"pago_bi": "R$ Bilhões", "orgao": ""},
)
fig_top10.update_traces(textposition="outside")
fig_top10.update_layout(coloraxis_showscale=False, height=420)
st.plotly_chart(fig_top10, use_container_width=True)

# ── Tabela detalhada ───────────────────────────────────────────────────────────

with st.expander("📋 Ver dados detalhados"):
    if orgao_selecionado != "Todos":
        tabela = df_filtrado[df_filtrado["orgao"] == orgao_selecionado]
    else:
        tabela = df_filtrado

    st.dataframe(
        tabela[["ano", "orgao", "empenhado", "liquidado", "pago", "taxa_execucao", "taxa_pagamento"]]
        .sort_values(["ano", "pago"], ascending=[True, False])
        .reset_index(drop=True),
        use_container_width=True,
    )

st.divider()
st.caption("Portal da Transparência · api.portaldatransparencia.gov.br/api-de-dados/despesas/por-orgao")
