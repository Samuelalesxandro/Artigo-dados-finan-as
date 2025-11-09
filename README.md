# Predição de Surpresas Econômicas: Pacote de Reprodutibilidade

Este repositório contém todos os códigos, dados e documentação necessários para reproduzir os resultados do artigo científico **"Predição de Surpresas Econômicas: Uma Abordagem de Machine Learning com Integração de Dados de Mercado Financeiro"**.

---

## 📋 Estrutura do Projeto

```
├── README.md                                    # Este arquivo
├── requirements.txt                             # Dependências Python
├── data/                                        # Dados brutos e processados
│   ├── final_data_merged_1.csv                 # Dataset final com features de mercado
│   └── data_description.md                     # Descrição detalhada dos dados
├── scripts/                                     # Scripts de processamento e modelagem
│   ├── 01_data_processing.py                   # Limpeza e cálculo de retornos
│   ├── 02_data_merging.py                      # Junção temporal de dados
│   ├── 03_final_model_generation.py            # Treinamento e avaliação do modelo
│   └── 04_feature_importance_plot.py           # Geração de gráficos
├── results/                                     # Resultados do modelo
│   ├── final_model_results_validated.txt       # Métricas de desempenho
│   ├── feature_importance_final_validated.png  # Gráfico de importância
│   └── roc_curve_final_validated.png           # Curva ROC
├── paper/                                       # Artigo científico
│   ├── Artigo_Cientifico_Revisado_Final.pdf    # Versão PDF
│   └── Artigo_Cientifico_Revisado_Final.md     # Versão Markdown
└── notebooks/                                   # Notebooks Jupyter (opcional)
    └── exploratory_analysis.ipynb              # Análise exploratória
```

---

## 🔧 Requisitos e Instalação

### Requisitos de Sistema
- Python 3.11+
- 8GB RAM (mínimo)
- 2GB de espaço em disco

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais
- `pandas==2.3.4`
- `numpy==2.3.4`
- `lightgbm==4.5.0`
- `scikit-learn==1.6.1`
- `category-encoders==2.6.4`
- `matplotlib==3.10.0`
- `seaborn==0.13.2`

---

## 📊 Descrição dos Dados

### Dataset Principal: `final_data_merged_1.csv`

**Dimensões:** 40.316 linhas × 60 colunas

**Colunas Principais:**

1. **Identificação e Temporalidade:**
   - `id`: Identificador único do evento
   - `Data`: Data do evento (formato: YYYY-MM-DD)
   - `time`: Hora do evento (formato: HH:MM:SS)

2. **Características do Evento:**
   - `zone`: Zona geográfica (e.g., USA, Europe, Asia)
   - `currency`: Moeda associada (e.g., USD, EUR, BRL)
   - `importance`: Importância do evento (low, medium, high)
   - `event`: Tipo de evento econômico (e.g., GDP, Unemployment Rate, CPI)

3. **Valores Econômicos:**
   - `actual`: Valor divulgado
   - `forecast`: Previsão de mercado
   - `previous`: Valor anterior

4. **Variável Alvo:**
   - `Y_Binary_Surprise`: Surpresa positiva (1) ou não (0)

5. **Features de Mercado Financeiro (Retornos t-1):**
   - `Retorno_t_1_OuroFuturos`: Retorno do ouro no dia anterior
   - `Retorno_t_1_DowJonesIndustrialAverage`: Retorno do Dow Jones
   - `Retorno_t_1_Ibovespa`: Retorno do Ibovespa
   - `Retorno_t_1_GasóleoLondresFuturos`: Retorno do gasóleo
   - `Retorno_t_1_CréditoCarbonoFuturos`: Retorno do crédito de carbono
   - `Retorno_t_1_Minériodeferrorefinado62%FeCFRFuturos`: Retorno do minério de ferro
   - `Retorno_t_1_PrincipaisÍndicesMundiaisHoje`: Retorno de índices globais
   - `Retorno_t_1_ÍndicesdeCommodities`: Retorno de índices de commodities

---

## 🚀 Reproduzindo os Resultados

### Passo 1: Processamento de Dados Históricos

```bash
python scripts/01_data_processing.py
```

**O que faz:**
- Lê arquivos CSV de dados históricos de ativos financeiros
- Calcula retornos diários (t-1) para cada ativo
- Salva os dados processados em `processed_historical_data.pkl`

### Passo 2: Junção Temporal de Dados

```bash
python scripts/02_data_merging.py
```

**O que faz:**
- Carrega os dados de eventos econômicos
- Realiza junção temporal com os retornos de ativos (t-1)
- Garante que não há vazamento de informações (data leakage)
- Salva o dataset final em `data/final_data_merged_1.csv`

### Passo 3: Treinamento e Avaliação do Modelo

```bash
python scripts/03_final_model_generation.py
```

**O que faz:**
- Carrega e prepara os dados (feature engineering, target encoding)
- Treina o modelo LightGBM com hiperparâmetros otimizados
- Avalia o modelo no conjunto de teste
- Gera e salva:
  - Métricas de desempenho (`results/final_model_results_validated.txt`)
  - Gráfico de importância de variáveis (`results/feature_importance_final_validated.png`)
  - Curva ROC (`results/roc_curve_final_validated.png`)

**Tempo estimado:** ~5 minutos

### Passo 4: Geração de Gráficos Adicionais (Opcional)

```bash
python scripts/04_feature_importance_plot.py
```

---

## 📈 Resultados Esperados

Ao executar os scripts acima, você deve obter os seguintes resultados:

| Métrica | Valor Esperado |
|---------|----------------|
| **AUC Score** | **0.7485** |
| **Acurácia** | **67.31%** |
| **Recall (Surpresa Positiva)** | **71.50%** |
| **F1-Score (Ponderado)** | **67.51%** |

**Nota:** Pequenas variações (±0.5%) podem ocorrer devido a diferenças de ambiente computacional.

---

## 🔬 Metodologia

### 1. Feature Engineering

**Variáveis Temporais:**
- `day_of_week`: Dia da semana (0-6)
- `month`: Mês (1-12)
- `hour`: Hora do evento (0-23)

**Codificação de Importância:**
- `importance_encoded`: low=1, medium=2, high=3

**Target Encoding:**
- Aplicado às variáveis categóricas: `zone`, `currency`, `event`
- Biblioteca: `category_encoders.TargetEncoder`

### 2. Modelo: LightGBM

**Hiperparâmetros Otimizados:**
```python
{
    'n_estimators': 377,
    'learning_rate': 0.0138,
    'num_leaves': 20,
    'min_child_samples': 57,
    'subsample': 0.9806,
    'colsample_bytree': 0.9223,
    'scale_pos_weight': 1.3696  # Calculado automaticamente
}
```

**Otimização:**
- Método: Otimização Bayesiana (Hyperopt)
- Iterações: 50
- Métrica objetivo: AUC (maximização)
- Validação cruzada: 3 folds

### 3. Divisão de Dados

- **Treinamento:** 80% (32.252 amostras)
- **Teste:** 20% (8.064 amostras)
- **Estratificação:** Sim (mantém proporção de classes)

---

## 📝 Citação

Se você utilizar este código ou dados em sua pesquisa, por favor cite:

```bibtex
@article{surpresas_economicas_2025,
  title={Predição de Surpresas Econômicas: Uma Abordagem de Machine Learning com Integração de Dados de Mercado Financeiro},
  author={[Autores]},
  journal={[Nome da Revista]},
  year={2025},
  volume={[Volume]},
  pages={[Páginas]}
}
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

---

## 📧 Contato

Para dúvidas ou sugestões, entre em contato:
- **Email:** [seu-email@exemplo.com]
- **GitHub:** [seu-usuario]

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🙏 Agradecimentos

Agradecemos à [Instituição] pelo suporte financeiro e infraestrutura computacional.

---

## 📚 Referências

1. Ke, G., et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30.

2. Bergstra, J., et al. (2011). Algorithms for hyper-parameter optimization. *Advances in Neural Information Processing Systems*, 24.

3. Micci-Barreca, D. (2001). A preprocessing scheme for high-cardinality categorical attributes. *ACM SIGKDD Explorations Newsletter*, 3(1), 27-32.

---

**Última atualização:** Novembro de 2025
