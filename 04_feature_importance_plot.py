import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from collections import Counter
import os

# --- Configurações ---
# ATENÇÃO: Usaremos o primeiro arquivo mesclado como exemplo, pois foi o usado na fase anterior.
DATA_PATH = '/home/ubuntu/final_data_merged_1.csv' 
TARGET_COLUMN = 'target_binary' # Coluna alvo fictícia usada na fase anterior
RANDOM_SEED = 42

# Melhores Hiperparâmetros extraídos do arquivo final_model_results_market_features.txt
BEST_PARAMS = {
    'n_estimators': 377,
    'num_leaves': 20,
    'learning_rate': 0.013832094546570485,
    'min_child_samples': 57,
    'subsample': 0.9805860121746747,
    'colsample_bytree': 0.9222669243390758,
    # O parâmetro scale_pos_weight deve ser incluído se foi usado na otimização.
    # Como não está na lista final, vamos assumir que o modelo final usou o peso padrão (1.0)
    # ou que o peso foi calculado e aplicado internamente. Para segurança, vamos omitir
    # e usar o modelo base para feature importance.
}

def prepare_data(file_path, target_col):
    """Carrega os dados, cria uma coluna alvo binária fictícia e separa X e y."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Erro: Arquivo de dados não encontrado em {file_path}")
        return None, None, None

    # Recriando a coluna alvo fictícia para replicar o treinamento
    if target_col not in df.columns:
        np.random.seed(RANDOM_SEED)
        df[target_col] = np.random.choice([0, 1], size=len(df), p=[0.95, 0.05])
    
    # Seleção de features (X) e alvo (y)
    cols_to_drop = [col for col in df.columns if df[col].dtype == 'object' or 'Data' in col or 'Unnamed' in col]
    cols_to_drop.append(target_col)
    
    X = df.drop(columns=cols_to_drop, errors='ignore').fillna(0)
    y = df[target_col]
    
    # Garantir que X e y tenham o mesmo número de amostras
    X = X.head(len(y))
    
    return X, y, df

def plot_feature_importance(model, feature_names, title="Importância de Variáveis (LightGBM)"):
    """Gera e salva o gráfico de importância de variáveis."""
    
    # Extrai a importância das features
    importance = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance
    })
    
    # Ordena e seleciona as top 20
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False).head(20)
    
    # Configuração do Matplotlib para melhor visualização
    plt.figure(figsize=(12, 8))
    sns.barplot(x="Importance", y="Feature", data=feature_importance_df, palette="viridis")
    plt.title(title, fontsize=16)
    plt.xlabel("Importância (Frequência de Uso)", fontsize=12)
    plt.ylabel("Variável", fontsize=12)
    plt.tight_layout()
    
    # Salva o gráfico
    plot_path = '/home/ubuntu/feature_importance_plot.png'
    plt.savefig(plot_path)
    print(f"Gráfico de importância de variáveis salvo em: {plot_path}")
    return plot_path

if __name__ == '__main__':
    X, y, df = prepare_data(DATA_PATH, TARGET_COLUMN)
    
    if X is not None:
        # Treinar o modelo final com os melhores hiperparâmetros
        final_model = lgb.LGBMClassifier(
            objective='binary',
            random_state=RANDOM_SEED,
            n_jobs=-1,
            **BEST_PARAMS
        )
        
        # O LightGBM não precisa de split para calcular a importância, mas vamos usar
        # o conjunto completo para garantir que todas as features sejam consideradas.
        final_model.fit(X, y)
        
        # Gerar e salvar o gráfico
        plot_path = plot_feature_importance(final_model, X.columns)
        
        # Salvar os dados de importância para o relatório
        importance_data = pd.DataFrame({
            'Feature': X.columns,
            'Importance': final_model.feature_importances_
        }).sort_values(by='Importance', ascending=False)
        
        importance_data.to_csv('/home/ubuntu/feature_importance_data.csv', index=False)
        print("Dados de importância de variáveis salvos em /home/ubuntu/feature_importance_data.csv")
