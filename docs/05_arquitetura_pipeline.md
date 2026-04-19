# 05 - Arquitetura do Pipeline

## Visão Geral

O pipeline foi desenvolvido em Python com organização modular, separando responsabilidades por etapa do ciclo de vida dos dados.

Essa abordagem permite:

- maior clareza
- manutenção facilitada
- reuso de funções
- evolução futura para orquestração

---

## Estrutura de Módulos

### `main.py`
Ponto de entrada da execução do pipeline.

### `src/config.py`
Configuração de caminhos, diretórios e arquivos de entrada/saída.

### `src/utils.py`
Funções utilitárias de apoio:
- padronização de nomes
- normalização textual
- classificação por faixa de preço
- divisão segura

### `src/ingest.py`
Responsável por:
- ler os arquivos brutos
- padronizar colunas
- persistir a camada bronze

### `src/clean.py`
Responsável por:
- tratamento de nulos
- remoção de duplicidades
- padronização de tipos
- regras de consistência

### `src/quality.py`
Responsável por:
- executar checks de qualidade
- gerar relatório em CSV e Excel

### `src/enrich.py`
Responsável por:
- cálculo de métricas derivadas
- enriquecimento analítico
- extração heurística de atributos semânticos a partir do título

### `src/pipeline.py`
Responsável por:
- orquestrar o fluxo completo
- gerar silver
- gerar gold
- retornar os principais dataframes

---

## Fluxo de Execução

1. Leitura dos arquivos raw
2. Padronização inicial
3. Persistência bronze
4. Limpeza e tratamento
5. Data Quality
6. Enriquecimento
7. Persistência silver
8. Geração de tabelas gold
9. Consumo pelo dashboard

---

## Estrutura de Pastas

```text
case_tecnico_diandra/
├── main.py
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── src/
├── app/
├── outputs/
└── docs/