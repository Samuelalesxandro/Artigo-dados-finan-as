# -*- coding: utf-8 -*-
"""
Script Final para Geração de Artefatos do Modelo

Este script treina o modelo LightGBM com os hiperparâmetros otimizados, avalia o desempenho
e gera os seguintes artefatos:
- Resultados do modelo (métricas de desempenho)
- Gráfico de importância de variáveis
- Curva ROC
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, recall_score, classification_report, roc_curve, auc
from category_encoders import TargetEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configurações ---
DATA_PATH = '/home/ubuntu/final_data_merged_1.csv'
RANDOM_SEED = 42

# Parâmetros otimizados (extraídos dos scripts fornecidos)
BEST_PARAMS = {
    'n_estimators': 377,
    'num_leaves': 20,
    'learning_rate': 0.013832094546570485,
    'min_child_samples': 57,
    'subsample': 0.9805860121746747,
    'colsample_bytree': 0.9222669243390758,
}

def load_and_prepare_data(file_path):
    """Carrega e prepara os dados para o modelo final."""
    df = pd.read_csv(file_path, header=0, low_memory=False, sep=',')
    df.fillna(0, inplace=True)

    # Conversão de tipos
    numeric_cols = ['actual', 'forecast', 'previous'] + [col for col in df.columns if 'Retorno_t_1' in col]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Y_Binary_Surprise'] = pd.to_numeric(df['Y_Binary_Surprise'], errors='coerce').astype(int)

    # Feature Engineering
    df['date'] = pd.to_datetime(df['Data'], errors='coerce', format='%Y-%m-%d')
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['hour'] = pd.to_datetime(df['time'], errors='coerce').dt.hour.fillna(0).astype(int)
    
    importance_map = {'low': 1, 'medium': 2, 'high': 3}
    df['importance_encoded'] = df['importance'].map(importance_map).fillna(0).astype(int)

    return df

# Carregar e preparar os dados
df_final = load_and_prepare_data(DATA_PATH)

# Definir X e y
features = [
    'previous', 'importance_encoded', 'day_of_week', 'month', 'hour',
    'Retorno_t_1_OuroFuturos', 'Retorno_t_1_DowJonesIndustrialAverage', 'Retorno_t_1_Ibovespa',
    'Retorno_t_1_GasóleoLondresFuturos', 'Retorno_t_1_CréditoCarbonoFuturos',
    'Retorno_t_1_Minériodeferrorefinado62%FeCFRFuturos',
    'Retorno_t_1_PrincipaisÍndicesMundiaisHoje', 'Retorno_t_1_ÍndicesdeCommodities',
    'zone', 'currency', 'event'
]
categorical_features = ['zone', 'currency', 'event']

X = df_final[features].copy()
y = df_final['Y_Binary_Surprise']

# Target Encoding
encoder = TargetEncoder(cols=categorical_features)
X = encoder.fit_transform(X, y)

# Divisão de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y)

# Treinar o modelo final com os melhores parâmetros
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
final_model = lgb.LGBMClassifier(
    random_state=RANDOM_SEED, objective='binary', metric='auc',
    scale_pos_weight=scale_pos_weight, **BEST_PARAMS
)
final_model.fit(X_train, y_train)

# Avaliação no conjunto de teste
y_pred = final_model.predict(X_test)
y_pred_proba = final_model.predict_proba(X_test)[:, 1]

# Métricas
final_auc = roc_auc_score(y_test, y_pred_proba)
final_accuracy = accuracy_score(y_test, y_pred)
final_f1 = f1_score(y_test, y_pred, average='weighted')
final_recall_pos = recall_score(y_test, y_pred, pos_label=1)
report_str = classification_report(y_test, y_pred, target_names=['Não Positiva (0)', 'Positiva (1)'])

# Salvar Resultados
results_summary = f"""
# Resultados do Modelo Final Otimizado (LightGBM)

## Métricas de Desempenho
- AUC Score: {final_auc:.4f}
- Acurácia: {final_accuracy:.4f}
- F1-Score (Ponderado): {final_f1:.4f}
- Recall (Surpresa Positiva): {final_recall_pos:.4f}

## Parâmetros Otimizados
{BEST_PARAMS}

## Relatório de Classificação
{report_str}
"""
with open('/home/ubuntu/final_model_results_validated.txt', 'w') as f:
    f.write(results_summary)

# Gráfico de Importância de Variáveis
feature_imp = pd.DataFrame(sorted(zip(final_model.feature_importances_, X.columns)), columns=['Value','Feature'])
feature_imp = feature_imp.sort_values(by="Value", ascending=False).head(10)

plt.figure(figsize=(12, 8))
sns.barplot(x="Value", y="Feature", data=feature_imp, palette='viridis')
plt.title('Importância de Variáveis (Modelo Final Validado)', fontsize=16, fontweight='bold')
plt.xlabel('Importância', fontsize=12)
plt.ylabel('Variável', fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/feature_importance_final_validated.png', dpi=300)

# Curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'Curva ROC (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.savefig('/home/ubuntu/roc_curve_final_validated.png', dpi=300)

print("Processo concluído. Resultados, gráfico de importância e curva ROC salvos.")

