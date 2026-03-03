# 🏛️ Dashboard de Execução Orçamentária — Ministério da Educação (2020–2024)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Dashboard interativo para análise da execução orçamentária do Ministério da Educação, construído com dados reais do **Portal da Transparência do Governo Federal**. O projeto aplica um pipeline ETL completo — da extração dos dados brutos à visualização — como suporte à tomada de decisão baseada em evidências no setor público.

---

## Sobre o Projeto

Os dados foram coletados via API oficial da CGU (Controladoria-Geral da União), cobrindo os exercícios fiscais de **2020 a 2024**, com granularidade por órgão vinculado ao MEC (código SIAFI 26000). O pipeline processa 17 arquivos CSV brutos, realiza limpeza e normalização, e entrega um dataset consolidado pronto para análise.

O dashboard responde perguntas como:

- O orçamento do MEC está crescendo? A execução acompanha esse crescimento?
- Quais órgãos concentram a maior parte dos recursos?
- Há anos com subexecução orçamentária sistemática?
- Como os gastos se distribuem entre os órgãos vinculados?

---

## Recursos Visuais

| Recurso                                                  | Decisão que apoia                       |
| -------------------------------------------------------- | --------------------------------------- |
| KPI Cards (empenhado, liquidado, pago, taxa de execução) | Diagnóstico situacional rápido          |
| Gráfico de linhas — Evolução anual                       | Planejamento e tendências orçamentárias |
| Barras agrupadas — Taxa de execução por ano              | Controle de desempenho e accountability |
| Barras horizontais — Top 10 órgãos                       | Priorização e alocação de recursos      |
| Gráfico de pizza — Distribuição por órgão (2024)         | Transparência e concentração de gastos  |

Todos os gráficos são interativos e respondem aos filtros de ano e órgão na sidebar.

---

## Estrutura do Projeto

```
projeto/
├── data/
│   ├── raw/                        # CSVs brutos extraídos da API (17 arquivos)
│   └── despesas_consolidado.csv    # Dataset limpo gerado pelo etl.py
├── etl.py                          # Pipeline: leitura → limpeza → consolidação
├── dashboard.py                    # Dashboard interativo (Streamlit + Plotly)
├── requirements.txt                # Dependências Python
└── README.md
```

---

## Pipeline ETL

O `etl.py` executa as seguintes etapas sobre os arquivos brutos:

1. **Leitura** — carrega todos os CSVs da pasta `data/raw/`
2. **Deduplicação** — remove snapshots duplicados (1.869 → 584 registros únicos)
3. **Normalização monetária** — converte valores do padrão BR (`"47.931.776.674,75"`) para `float64`
4. **Validação** — remove nulos e verifica valores negativos
5. **Métricas derivadas** — calcula `taxa_execucao` e `taxa_pagamento` por órgão/ano
6. **Exportação** — salva `data/despesas_consolidado.csv`

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Dependências listadas em `requirements.txt`

### Instalação e execução

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar o ETL (gera o CSV consolidado)
python etl.py

# 3. Subir o dashboard
streamlit run dashboard.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`.

---

## Fonte de Dados

| Campo             | Detalhe                                           |
| ----------------- | ------------------------------------------------- |
| Portal            | Portal da Transparência do Governo Federal        |
| Órgão responsável | Controladoria-Geral da União (CGU)                |
| Endpoint          | `GET /api-de-dados/despesas/por-orgao`            |
| Órgão analisado   | Ministério da Educação — SIAFI 26000              |
| Período           | 2020 – 2024                                       |
| Documentação      | https://portaldatransparencia.gov.br/api-de-dados |

---

## Autor

Desenvolvido por **Vanthuir Maia** como atividade da disciplina _Banco de Dados e Inteligência de Negócios_ — curso de Tomada de Decisão Baseada em Evidências no Setor Público · UFRPE.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/vanthuir-maia-47767810b/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/VanthuirMaia)
