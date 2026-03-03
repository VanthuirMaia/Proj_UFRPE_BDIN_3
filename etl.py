"""
etl.py — Leitura, limpeza e consolidação dos dados brutos
Fonte: Portal da Transparência (despesas por órgão, MEC/SIAFI 26000)
"""

import pandas as pd
import glob
import os

RAW_DIR = "data/raw"
OUT_DIR = "data"


def carregar_despesas():
    arquivos = glob.glob(os.path.join(RAW_DIR, "despesas_*.csv"))
    print(f"Arquivos encontrados: {len(arquivos)}")

    dfs = []
    for arq in arquivos:
        df = pd.read_csv(arq)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    print(f"Registros brutos (com duplicatas): {len(df)}")
    return df


def limpar_despesas(df):
    # Remove duplicatas — mesmo par (ano, codigoOrgao) coletado em datas distintas
    df = df.drop_duplicates()
    print(f"Registros após deduplicação: {len(df)}")

    # Remove linhas sem órgão ou ano
    df = df.dropna(subset=["ano", "orgao", "codigoOrgao"])

    # Converte valores monetários do padrão BR para float
    # Ex: "47.931.776.674,75" -> 47931776674.75
    for col in ["empenhado", "liquidado", "pago"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    # Garante tipo correto no ano
    df["ano"] = df["ano"].astype(int)

    # Colunas padronizadas
    df = df.rename(columns={
        "codigoOrgao": "codigo_orgao",
        "orgaoSuperior": "orgao_superior",
        "codigoOrgaoSuperior": "codigo_orgao_superior",
    })

    # Validação básica: valores não podem ser negativos
    for col in ["empenhado", "liquidado", "pago"]:
        negativos = (df[col] < 0).sum()
        if negativos > 0:
            print(f"  Atenção: {negativos} valores negativos em '{col}' — removidos")
            df = df[df[col] >= 0]

    return df


def calcular_metricas(df):
    df = df.copy()
    df["taxa_execucao"] = (df["liquidado"] / df["empenhado"] * 100).round(2)
    df["taxa_pagamento"] = (df["pago"] / df["empenhado"] * 100).round(2)
    return df


def salvar(df):
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    caminho = os.path.join(OUT_DIR, "despesas_consolidado.csv")
    df.to_csv(caminho, index=False)
    print(f"\nArquivo salvo: {caminho}")
    print(f"Shape final: {df.shape}")
    print(f"Anos: {sorted(df['ano'].unique())}")
    print(f"Órgãos únicos: {df['orgao'].nunique()}")


if __name__ == "__main__":
    print("=== ETL — Despesas MEC (Portal da Transparência) ===\n")

    df = carregar_despesas()
    df = limpar_despesas(df)
    df = calcular_metricas(df)
    salvar(df)

    print("\n✓ ETL concluído.")