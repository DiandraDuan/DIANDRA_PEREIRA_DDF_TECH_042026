# 02 - Dicionário de Dados

## Visão Geral

A solução utiliza duas bases principais:

1. `amazon_products.csv`
2. `amazon_categories.csv`

A primeira representa o catálogo de produtos e a segunda funciona como dimensão de categorias.

---

## Tabela: amazon_products.csv

| Campo original | Campo padronizado | Tipo esperado | Descrição |
|---|---:|---:|---|
| asin | asin | string | Identificador único do produto na Amazon |
| title | title | string | Título do produto |
| imgUrl | img_url | string | URL da imagem do produto |
| productURL | product_url | string | URL da página do produto |
| stars | stars | float | Classificação média do produto |
| reviews | reviews | int | Quantidade de avaliações |
| price | price | float | Preço atual do produto |
| listPrice | list_price | float | Preço de lista do produto |
| category_id | category_id | int | Chave de categoria |
| isBestSeller | is_best_seller | bool | Indicador de best seller |
| boughtInLastMonth | bought_in_last_month | int | Quantidade comprada no último mês |

---

## Tabela: amazon_categories.csv

| Campo original | Campo padronizado | Tipo esperado | Descrição |
|---|---:|---:|---|
| id | category_id | int | Identificador da categoria |
| category_name | category_name | string | Nome da categoria |

---

## Tabela Enriquecida: products_enriched

A tabela enriquecida foi construída a partir do merge entre produtos e categorias, adicionando atributos derivados.

### Principais colunas derivadas

| Campo | Tipo | Descrição |
|---|---:|---|
| discount_value | float | Diferença entre `list_price` e `price` |
| discount_pct | float | Percentual de desconto |
| price_band | string | Faixa de preço (`low`, `mid`, `high`, `premium`) |
| review_density | float | Relação entre reviews e preço |
| popularity_score | float | Score composto de popularidade |
| title_product_type | string | Tipo de produto inferido do título |
| title_color | string | Cor inferida do título |
| title_material | string | Material inferido do título |
| has_discount | bool | Flag de desconto |
| is_premium | bool | Flag de produto premium |
| high_rating_flag | bool | Flag para rating >= 4.5 |
| high_traction_flag | bool | Flag para compras recentes >= 1000 |

---

## Regras de Padronização

- Todos os nomes de colunas foram convertidos para `snake_case`
- Tipos numéricos foram convertidos com tratamento de erro (`coerce`)
- Campos textuais foram normalizados (trim e remoção de espaços duplicados)
- Campos booleanos foram padronizados para `True/False`

---

## Observações

- O `asin` foi tratado como chave principal do produto
- A `category_id` foi tratada como chave estrangeira para a dimensão de categorias
- O enriquecimento textual foi feito com regras heurísticas baseadas no campo `title`