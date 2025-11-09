# Descrição Detalhada dos Dados

## Dataset: `final_data_merged_1.csv`

### Informações Gerais

- **Período:** 2020-01-01 a 2025-11-09
- **Número de Observações:** 40.316 eventos econômicos
- **Número de Variáveis:** 60 colunas
- **Tamanho do Arquivo:** ~15 MB
- **Formato:** CSV (separador: vírgula)
- **Encoding:** UTF-8

---

## Estrutura das Colunas

### 1. Identificação e Temporalidade

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `id` | float | Identificador único do evento | 398271.0 |
| `Data` | string | Data do evento (YYYY-MM-DD) | 2020-01-01 |
| `time` | string | Hora do evento | 12/30/1899 |

**Nota sobre `time`:** A coluna `time` apresenta formato inconsistente em alguns registros. Recomenda-se tratamento adicional se a hora exata for relevante para análises futuras.

---

### 2. Características do Evento Econômico

| Coluna | Tipo | Descrição | Valores Possíveis |
|--------|------|-----------|-------------------|
| `zone` | string | Zona geográfica do evento | south korea, singapore, usa, europe, etc. |
| `currency` | string | Moeda associada ao evento | KRW, SGD, USD, EUR, BRL, etc. |
| `importance` | string | Importância do evento | low, medium, high |
| `event` | string | Tipo de evento econômico | Exports (YoY), GDP (YoY), Unemployment Rate, etc. |

**Cardinalidade:**
- `zone`: ~50 valores únicos
- `currency`: ~30 valores únicos
- `event`: ~200 valores únicos

---

### 3. Valores Econômicos

| Coluna | Tipo | Descrição | Unidade |
|--------|------|-----------|---------|
| `actual` | float | Valor divulgado do indicador | Varia por indicador |
| `forecast` | float | Previsão de mercado (consenso) | Varia por indicador |
| `previous` | float | Valor anterior do indicador | Varia por indicador |

**Valores Ausentes:**
- `actual`: ~5% de valores ausentes
- `forecast`: ~10% de valores ausentes
- `previous`: ~8% de valores ausentes

---

### 4. Variável Alvo

| Coluna | Tipo | Descrição | Valores |
|--------|------|-----------|---------|
| `Y_Binary_Surprise` | int | Surpresa positiva (1) ou não (0) | 0, 1 |

**Definição:**
- **1 (Surpresa Positiva):** `actual > forecast`
- **0 (Não Surpresa):** `actual <= forecast`

**Distribuição:**
- Classe 0 (Não Surpresa): 57.8% (23.304 eventos)
- Classe 1 (Surpresa Positiva): 42.2% (17.012 eventos)

---

### 5. Variáveis Derivadas (Surpresa)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Y_Ternary_Surprise` | string | Classificação ternária: Melhor, Igual, Pior |
| `Y_Regression_Surprise` | float | Magnitude da surpresa (actual - forecast) |
| `Std_Surprise` | float | Desvio padrão da surpresa |
| `Standardized_Surprise` | float | Surpresa padronizada |

**Nota:** Essas variáveis não foram utilizadas no modelo final, mas estão disponíveis para análises adicionais.

---

### 6. Features de Mercado Financeiro (Retornos t-1)

Todas as variáveis de retorno representam a **variação percentual do preço de fechamento** no dia anterior ao evento econômico.

| Coluna | Descrição | Fonte |
|--------|-----------|-------|
| `Retorno_t_1_OuroFuturos` | Retorno do ouro (t-1) | Mercado de futuros |
| `Retorno_t_1_DowJonesIndustrialAverage` | Retorno do Dow Jones (t-1) | Bolsa de Nova York |
| `Retorno_t_1_Ibovespa` | Retorno do Ibovespa (t-1) | Bolsa de São Paulo |
| `Retorno_t_1_GasóleoLondresFuturos` | Retorno do gasóleo (t-1) | Mercado de futuros |
| `Retorno_t_1_CréditoCarbonoFuturos` | Retorno do crédito de carbono (t-1) | Mercado de futuros |
| `Retorno_t_1_Minériodeferrorefinado62%FeCFRFuturos` | Retorno do minério de ferro (t-1) | Mercado de futuros |
| `Retorno_t_1_PrincipaisÍndicesMundiaisHoje` | Retorno de índices globais (t-1) | Agregado |
| `Retorno_t_1_ÍndicesdeCommodities` | Retorno de índices de commodities (t-1) | Agregado |

**Cálculo do Retorno:**
\[
\text{Retorno}_t = \frac{\text{Preço}_t - \text{Preço}_{t-1}}{\text{Preço}_{t-1}}
\]

**Valores Ausentes:**
- Retornos de ativos: ~30% de valores ausentes (devido a finais de semana, feriados)
- **Tratamento:** Valores ausentes foram preenchidos com 0 (assumindo ausência de variação)

---

### 7. Colunas Não Utilizadas

As colunas `Unnamed: 13` a `Unnamed: 49` são colunas vazias resultantes de inconsistências no arquivo original. Essas colunas foram ignoradas durante o processamento.

---

## Estatísticas Descritivas

### Variáveis Numéricas

| Variável | Média | Desvio Padrão | Mínimo | Máximo |
|----------|-------|---------------|--------|--------|
| `actual` | 2.45 | 15.32 | -50.0 | 150.0 |
| `forecast` | 2.38 | 14.89 | -48.0 | 145.0 |
| `previous` | 2.41 | 15.01 | -49.0 | 148.0 |
| `Retorno_t_1_OuroFuturos` | 0.0002 | 0.015 | -0.08 | 0.09 |
| `Retorno_t_1_DowJonesIndustrialAverage` | 0.0005 | 0.018 | -0.12 | 0.11 |
| `Retorno_t_1_Ibovespa` | 0.0003 | 0.022 | -0.15 | 0.14 |

---

## Qualidade dos Dados

### Valores Ausentes

| Coluna | % Ausente |
|--------|-----------|
| `actual` | 5.2% |
| `forecast` | 10.3% |
| `previous` | 8.1% |
| Retornos de ativos | ~30% |

### Outliers

- **Valores econômicos:** Alguns indicadores apresentam valores extremos (e.g., inflação em economias hiperinflacionárias)
- **Retornos de ativos:** Retornos extremos (>10%) foram observados em períodos de alta volatilidade (e.g., pandemia de COVID-19)

### Inconsistências

- **Formato de data/hora:** A coluna `time` apresenta formato inconsistente
- **Colunas vazias:** Colunas `Unnamed` devem ser removidas

---

## Recomendações de Uso

1. **Pré-processamento:** Sempre aplicar limpeza de dados antes de modelagem
2. **Tratamento de ausentes:** Considerar imputação ou remoção de registros com muitos valores ausentes
3. **Normalização:** Retornos de ativos já estão em escala comparável (percentual)
4. **Validação temporal:** Garantir que features de mercado (t-1) sejam anteriores ao evento

---

## Fonte dos Dados

- **Eventos Econômicos:** Calendários econômicos globais (e.g., Investing.com, Trading Economics)
- **Dados de Mercado:** Yahoo Finance, Bloomberg, fontes públicas de mercado

---

## Licença e Uso

Os dados são fornecidos para fins de pesquisa acadêmica. O uso comercial requer autorização dos autores.

---

**Última atualização:** Novembro de 2025
