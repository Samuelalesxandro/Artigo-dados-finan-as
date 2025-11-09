import pandas as pd
import numpy as np
import pickle
import os

# Arquivos principais
MAIN_FILE_1 = '/home/ubuntu/final_data_with_SESI.csv'
MAIN_FILE_2 = '/home/ubuntu/time_series_analysis.csv'
PROCESSED_DATA_PATH = '/home/ubuntu/processed_historical_data.pkl'

def load_main_file(file_path):
    """Carrega e prepara o arquivo principal, garantindo a coluna 'Data' no formato datetime."""
    try:
        # Tenta ler o arquivo com o separador ',' e encoding 'latin-1'
        df = pd.read_csv(file_path, sep=',', encoding='latin-1', decimal=',')
    except Exception:
        # Se falhar, tenta ler com o separador ',' e encoding 'utf-8'
        df = pd.read_csv(file_path, sep=',', encoding='utf-8', decimal=',')

    # Baseado na análise do arquivo final_data_with_SESI(1).csv, a coluna de data
    # parece ser a segunda (índice 1) e não tem cabeçalho.
    # Para o time_series_analysis(1).csv, a coluna de data é a primeira (índice 0).
    
    # Tentativa de inferir a coluna de data
    date_col_name = None
    
    # Tentativa 1: Coluna com nome 'Data' (se houver cabeçalho)
    if 'Data' in df.columns:
        date_col_name = 'Data'
    # Tentativa 2: Coluna com nome 'data' (se houver cabeçalho)
    elif 'data' in df.columns:
        date_col_name = 'data'
    # Tentativa 3: Primeira coluna (para time_series_analysis)
    elif file_path == MAIN_FILE_2 and df.shape[1] > 0:
        date_col_name = df.columns[0]
    # Tentativa 4: Segunda coluna (para final_data_with_SESI)
    elif file_path == MAIN_FILE_1 and df.shape[1] > 1:
        date_col_name = df.columns[1]
    
    if date_col_name is None:
        print(f"Erro: Não foi possível identificar a coluna de data em {os.path.basename(file_path)}. Pulando.")
        return None

    # Renomear a coluna de data para 'Data' para padronização
    if date_col_name != 'Data':
        df.rename(columns={date_col_name: 'Data'}, inplace=True)

    # Conversão para datetime
    # O formato de data no final_data_with_SESI(1).csv parece ser M/D/YYYY (e.g., 1/1/2020)
    # O formato de data no time_series_analysis(1).csv parece ser YYYY-MM-DD (e.g., 2020-01-01)
    
    # Tenta inferir o formato
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce', infer_datetime_format=True)
    df.dropna(subset=['Data'], inplace=True)
    
    return df

def merge_data(main_df, processed_dfs, output_path):
    """Realiza a junção dos dados históricos processados com o DataFrame principal."""
    if main_df is None:
        return

    print(f"Iniciando junção para {os.path.basename(output_path)}...")
    
    # Inicializa o DataFrame de junção com o principal
    merged_df = main_df.copy()
    
    # Itera sobre os DataFrames processados e faz a junção
    for df_hist in processed_dfs:
        # A coluna de junção é 'Data'
        merged_df = pd.merge(merged_df, df_hist, on='Data', how='left')
        
    # Salva o resultado
    merged_df.to_csv(output_path, index=False)
    print(f"Junção concluída. Novo arquivo salvo em: {output_path}")
    print(f"Formato final do arquivo: {merged_df.shape}")
    print(f"Colunas adicionadas: {[col for col in merged_df.columns if col.startswith('Retorno_t_1_')]}")
    
    return merged_df

if __name__ == '__main__':
    # 1. Carregar dados processados
    try:
        with open(PROCESSED_DATA_PATH, 'rb') as f:
            processed_dfs = pickle.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo de dados históricos processados não encontrado. Execute a Fase 2 primeiro.")
        exit()

    # 2. Carregar e processar arquivos principais
    main_df_1 = load_main_file(MAIN_FILE_1)
    main_df_2 = load_main_file(MAIN_FILE_2)

    # 3. Realizar a junção e salvar
    if main_df_1 is not None:
        merged_df_1 = merge_data(main_df_1, processed_dfs, '/home/ubuntu/final_data_merged_1.csv')
    
    if main_df_2 is not None:
        merged_df_2 = merge_data(main_df_2, processed_dfs, '/home/ubuntu/final_data_merged_2.csv')
        
    print("\nProcesso de junção de dados concluído.")
