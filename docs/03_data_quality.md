# 03 - Data Quality

## Objetivo

Garantir que os dados utilizados nas análises e no Data App sejam consistentes, confiáveis e minimamente preparados para consumo analítico.

---

## Principais Regras Aplicadas

### 1. Chave primária do produto
- `asin` não pode ser nulo
- `asin` deve ser único após deduplicação

### 2. Campos obrigatórios
Foram considerados obrigatórios:
- `asin`
- `title`
- `category_id`

Registros sem esses campos foram removidos.

### 3. Conversão segura de tipos
As colunas numéricas foram convertidas com:

- `errors="coerce"`

Isso evita quebra do pipeline por registros inválidos e transforma valores inconsistentes em nulos tratáveis.

### 4. Validação de faixas numéricas
Foram tratados como inválidos:

- `price < 0`
- `list_price < 0`
- `reviews < 0`
- `bought_in_last_month < 0`
- `stars < 0` ou `stars > 5`

### 5. Consistência entre preço atual e preço de lista
- `list_price = 0` foi tratado como nulo
- `list_price < price` foi tratado como nulo, pois não representa desconto válido

### 6. Integridade referencial
Foi validado se:

- `category_id` de produtos existe na dimensão de categorias

---

## Tratamentos Aplicados

- Remoção de duplicidades por `asin`
- Remoção de registros críticos inválidos
- Substituição de nulos em `reviews` por 0
- Substituição de nulos em `bought_in_last_month` por 0
- Padronização de booleanos em `is_best_seller`

---

## Relatório Gerado

Foi gerado um relatório automatizado contendo checks de qualidade:

- `products_asin_not_null`
- `products_asin_unique`
- `products_title_not_null`
- `products_price_non_negative`
- `products_stars_between_0_5`
- `products_reviews_non_negative`
- `category_fk_valid`

Arquivos gerados:

- `outputs/quality_reports/quality_report.csv`
- `outputs/quality_reports/quality_report.xlsx`

---
