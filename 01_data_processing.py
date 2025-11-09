import pandas as pd
import numpy as np
import glob
import os

# Lista de arquivos históricos a serem processados
HISTORICAL_FILES = glob.glob('/home/ubuntu/upload/DadosHistóricos-*.csv') + \
                   glob.glob('/home/ubuntu/upload/PrincipaisÍndicesMundiaisHoje.csv') + \
                   glob.glob('/home/ubuntu/upload/ÍndicesdeCommodities.csv')

# Arquivos principais
MAIN_FILE_1 = '/home/ubuntu/upload/final_data_with_SESI(1).csv'
MAIN_FILE_2 = '/home/ubuntu/upload/time_series_analysis(1).csv'

def clean_and_calculate_return(file_path):
    """
    Lê o arquivo CSV histórico, limpa os dados, calcula o retorno do dia anterior
    e retorna um DataFrame com 'data' e a nova variável de retorno.
    """
    try:
        # Tenta ler o arquivo com o separador ';' e encoding 'latin-1'
        df = pd.read_csv(file_path, sep=',', encoding='latin-1', decimal=',')
    except Exception:
        # Se falhar, tenta ler com o separador ',' e encoding 'utf-8'
        df = pd.read_csv(file_path, sep=',', encoding='utf-8', decimal=',')

    # O nome do ativo será baseado no nome do arquivo
    asset_name = os.path.basename(file_path).replace('DadosHistóricos-', '').replace('.csv', '').replace('(1)', '').replace(' ', '_')
    
    # Colunas esperadas: Data e Preço de Fechamento (ou a primeira coluna de preço)
    # Baseado na análise, a coluna de data é a primeira e o preço é a segunda.
    # Os arquivos históricos têm cabeçalhos que não foram lidos na pré-análise,
    # então vamos assumir que a primeira coluna é a data e a segunda é o preço de fechamento.
    # Vamos renomear as colunas para facilitar o acesso.
    
    # Se o arquivo não tiver cabeçalho (como sugerido pela pré-análise),
    # vamos tentar inferir as colunas.
    if df.shape[1] >= 2:
        df.columns = ['Data', 'Preco_Fechamento'] + list(df.columns[2:])
    else:
        print(f"Aviso: Arquivo {asset_name} tem menos de 2 colunas. Pulando.")
        return None

    # 1. Limpeza e Conversão da Coluna 'Data'
    # O formato esperado é DD.MM.YYYY (ou similar)
    df['Data'] = df['Data'].str.replace('"', '').str.strip()
    
    # Tentativa de conversão para datetime. O parâmetro `dayfirst=True` é crucial.
    try:
        df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y', errors='coerce')
    except ValueError:
        try:
            df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
        except:
            print(f"Erro ao converter a coluna 'Data' em {asset_name}. Pulando.")
            return None
            
    df.dropna(subset=['Data'], inplace=True)
    
    # 2. Limpeza e Conversão da Coluna 'Preco_Fechamento'
    # O preço está na segunda coluna e usa ',' como separador decimal.
    # Vamos limpar a coluna de preço, removendo aspas e substituindo ',' por '.'
    price_col = 'Preco_Fechamento'
    
    # Tenta limpar a coluna de preço, removendo aspas e substituindo ',' por '.'
    df[price_col] = df[price_col].astype(str).str.replace('"', '').str.strip()
    
    # Se o arquivo foi lido com decimal=',', o pandas já deve ter convertido para float.
    # Se não, fazemos a substituição manual.
    if df[price_col].dtype == object:
        df[price_col] = df[price_col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    
    df.dropna(subset=[price_col], inplace=True)
    
    # 3. Ordenação e Cálculo do Retorno do Dia Anterior
    df.sort_values(by='Data', inplace=True)
    
    # Cálculo do retorno (Retorno = (Preço Atual / Preço Anterior) - 1)
    # O retorno do dia anterior (t-1) é o retorno de hoje (t)
    # O retorno de hoje é calculado com o preço de ontem (shift(1))
    # Retorno_t = (Preco_t / Preco_{t-1}) - 1
    # Para obter o retorno do dia anterior (t-1), precisamos do retorno de t-1,
    # que é o retorno de hoje (t) deslocado para trás.
    
    # Retorno diário
    df['Retorno_Diario'] = df[price_col].pct_change()
    
    # Retorno do dia anterior (t-1)
    # O retorno de hoje (t) é o retorno do dia anterior (t-1) para o modelo.
    # O retorno do dia anterior é o retorno diário deslocado em 1 dia.
    new_col_name = f'Retorno_t_1_{asset_name}'
    df[new_col_name] = df['Retorno_Diario'].shift(1)
    
    # Seleciona apenas as colunas 'Data' e a nova variável de retorno
    result_df = df[['Data', new_col_name]].copy()
    
    print(f"Processado {asset_name}. Coluna de retorno: {new_col_name}")
    return result_df

def process_all_historical_files():
    """Processa todos os arquivos históricos e retorna uma lista de DataFrames."""
    processed_dfs = []
    for file_path in HISTORICAL_FILES:
        print(f"Iniciando processamento de: {os.path.basename(file_path)}")
        df = clean_and_calculate_return(file_path)
        if df is not None:
            processed_dfs.append(df)
    return processed_dfs

if __name__ == '__main__':
    processed_data = process_all_historical_files()
    
    # Salva os DataFrames processados em um arquivo temporário para a próxima fase
    import pickle
    with open('/home/ubuntu/processed_historical_data.pkl', 'wb') as f:
        pickle.dump(processed_data, f)
    
    print(f"Total de {len(processed_data)} arquivos históricos processados e salvos em /home/ubuntu/processed_historical_data.pkl")
    
    # Verifica as primeiras linhas de um dos DataFrames processados para debug
    if processed_data:
        print("\nExemplo do primeiro DataFrame processado:")
        print(processed_data[0].head())
