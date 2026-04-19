# Case Técnico Diandra / Dadosfera - Amazon Product Catalog Analytics

## Visão Geral

Este projeto foi desenvolvido como solução para o case técnico, com o objetivo de transformar uma base bruta de catálogo de produtos da Amazon em uma estrutura analítica confiável, organizada e pronta para consumo.

A proposta foi construída com foco em **engenharia de dados + análise exploratória + camada de consumo**, cobrindo desde a ingestão dos arquivos até a disponibilização de um **Data App em Streamlit**.

A solução prioriza:

- arquitetura
- boas práticas de organização
- qualidade de dados
- modelagem analítica simples e escalável
- geração de valor de negócio com visualização interativa

---

## Objetivo da Solução

Transformar os arquivos brutos:

- `amazon_products.csv`
- `amazon_categories.csv`

em uma base enriquecida e reutilizável, com:

- tratamento e padronização
- validação de qualidade
- enriquecimento de atributos
- geração de agregações analíticas
- exploração via dashboard

---

## O que foi entregue

- Pipeline em Python
- Organização em camadas: **raw / bronze / silver / gold**
- Limpeza e padronização dos dados
- Regras de **Data Quality** com relatório automatizado
- Tabela analítica enriquecida por produto
- Agregações em camada gold
- Dashboard interativo em **Streamlit**
- Documentação técnica em Markdown

---

## Principais Resultados

### Panorama da base
- **1.426.336 produtos**
- **Preço médio:** US$ 43,38
- **Classificação média:** 4,00
- **257.811.582 avaliações**
- **202.514.600 compras no último mês**
- **0,60% dos produtos são best sellers**

### Principais insights
- Forte concentração em categorias de varejo massificado, especialmente moda, acessórios e brinquedos
- Predominância da faixa de preço **low**, seguida de **mid**
- Produtos **best seller** representam pequena fração do catálogo, mas apresentam:
  - menor preço médio
  - melhor avaliação média
  - muito mais reviews
  - muito mais compras recentes
  - score de popularidade significativamente maior

---

## Arquitetura da Solução

A arquitetura segue uma abordagem em camadas:

- **Raw** → arquivos originais recebidos
- **Bronze** → cópia estruturada da ingestão
- **Silver** → dados limpos, padronizados e enriquecidos
- **Gold** → visões analíticas agregadas para dashboard e exploração

### Fluxo resumido

1. Leitura dos arquivos brutos
2. Padronização de colunas
3. Persistência bronze
4. Limpeza e tratamento
5. Validação de qualidade
6. Enriquecimento analítico e semântico
7. Persistência silver
8. Geração de tabelas gold
9. Consumo via Streamlit

## Observação sobre os arquivos de entrada

Os arquivos brutos utilizados no desenvolvimento (`amazon_products.csv` e `amazon_categories.csv`) não foram versionados no repositório devido ao volumhttps://www.kaggle.com/datasets/asaniczka/amazon-products-dataset-2023-1-4m-productse, mas podem ser acessados em:

Para executar o projeto localmente, basta posicionar os arquivos em:

data/raw/

## Estrutura do Projeto

case_tecnico_diandra/


## Como Executar o Projeto

### Clonar o repositório

```bash
git clone <https://github.com/DiandraDuan/DIANDRA_PEREIRA_DDF_TECH_042026.git>
cd CASE_TECNICO_DIANDRA

### Instalar dependências

```bash
pip install -r requirements.txt

### Executar pipeline
```bash
python main.py

### Executar pipeline
```bash
streamlit run app/streamlit_app.py

│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── amazon_products.csv
│   │   └── amazon_categories.csv
│   ├── bronze/
│   │   ├── products_raw.csv
│   │   └── categories_raw.csv
│   ├── silver/
│   │   ├── products_clean.csv
│   │   ├── categories_clean.csv
│   │   └── products_enriched.csv
│   └── gold/
│       ├── gold_category_analytics.csv
│       ├── gold_price_band_analytics.csv
│       └── gold_bestseller_analytics.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── ingest.py
│   ├── clean.py
│   ├── enrich.py
│   ├── quality.py
│   └── pipeline.py
│
├── app/
│   └── streamlit_app.py
│
├── outputs/
│   ├── quality_reports/
│   │   ├── quality_report.csv
│   │   └── quality_report.xlsx
│   └── logs/
│
└── docs/
    ├── 01_planejamento.md
    ├── 02_dicionario_dados.md
    ├── 03_data_quality.md
    ├── 04_modelagem.md
    ├── 05_arquitetura_pipeline.md
