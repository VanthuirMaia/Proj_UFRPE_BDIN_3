# Dashboard — Despesas do MEC (2020–2024)

Projeto de BI utilizando Python, com dados reais do Portal da Transparência do Governo Federal.

**Ferramenta:** Streamlit + Plotly  
**Fonte:** api.portaldatransparencia.gov.br — endpoint `/despesas/por-orgao`  
**Órgão:** Ministério da Educação — código SIAFI 26000

## Estrutura

```
mec_dashboard/
├── data/
│   ├── raw/                  # CSVs brutos extraídos da API
│   └── despesas_consolidado.csv  # Gerado pelo etl.py
├── etl.py                    # Leitura, limpeza e consolidação
├── dashboard.py              # Visualização com Streamlit
└── requirements.txt
```

## Como executar

```bash
pip install -r requirements.txt

# 1. Rodar o ETL (gera o CSV consolidado)
python etl.py

# 2. Subir o dashboard
streamlit run dashboard.py
```
