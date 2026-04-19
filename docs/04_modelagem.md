# 04 - Modelagem Analítica

## Objetivo

Construir uma estrutura analítica simples, clara e reutilizável para suportar exploração de catálogo, comparação entre grupos de produtos e visualização de indicadores de negócio.

---

## Modelo Lógico

A modelagem foi baseada em uma estrutura semelhante a um mini star schema:

- **Dimensão**
  - `amazon_categories` → dimensão de categorias

- **Fato principal**
  - `products_enriched` → tabela analítica enriquecida por produto

- **Agregações Gold**
  - `gold_category_analytics`
  - `gold_price_band_analytics`
  - `gold_bestseller_analytics`

---

## Tabela Fato: products_enriched

A tabela `products_enriched` é o principal ativo analítico do projeto e representa o catálogo de produtos já tratado e enriquecido.

### Granularidade
- 1 linha = 1 produto (1 ASIN)

### Chaves
- Chave primária: `asin`
- Chave estrangeira: `category_id`

---

## Métricas Derivadas

### discount_value
Diferença absoluta entre preço de lista e preço atual.

### discount_pct
Percentual de desconto calculado sobre o preço de lista.

### price_band
Segmentação do produto por faixa de preço:
- low
- mid
- high
- premium

### review_density
Indicador simples de intensidade de avaliações em relação ao preço.

### popularity_score
Métrica composta criada para priorização analítica, considerando:
- rating médio
- volume de avaliações (log)
- compras no último mês
- flag de best seller

Essa métrica não substitui um modelo estatístico formal, mas funciona bem como proxy de tração comercial.

---

## Features Semânticas

Com base no título do produto, foram extraídas features heurísticas:

- `title_product_type`
- `title_color`
- `title_material`

Essas features foram criadas para enriquecer a base e aproximar o case da ideia de transformação de dados desestruturados em atributos analíticos.

---

## Camadas do Projeto

### Bronze
Persistência inicial dos dados carregados.

### Silver
Dados limpos, padronizados e enriquecidos.

### Gold
Tabelas agregadas voltadas ao consumo por dashboard e análise executiva.

---

## Benefícios da Modelagem

- Separação clara entre dado bruto e dado analítico
- Reaproveitamento da base enriquecida
- Facilidade de manutenção
- Boa legibilidade para avaliadores
- Escalabilidade para futuras evoluções