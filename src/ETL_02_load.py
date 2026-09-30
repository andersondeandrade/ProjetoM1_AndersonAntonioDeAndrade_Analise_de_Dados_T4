#populando a tabela db_metalurgia com dos dados do arquivo CSV

#importar bibliotecas
import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

#definir o caminho do arquivo CSV

PASTA_SRC = os.path.dirname(os.path.abspath(__file__)) 
PASTA_PROJETO = os.path.dirname(PASTA_SRC)               # sobe um nível ->
CAMINHO_CSV = os.path.join(PASTA_PROJETO, 'data', 'raw', 'Supermarket Analysis.csv')

#monta a conexão com o banco de dados PostgreSQL e arquivo csv
engine = create_engine('postgresql+psycopg2://postgres:030988@localhost:5432/DB_SUPERMARKET')

df_supermarket = pd.read_csv(CAMINHO_CSV, dtype=str,keep_default_na=False) #lendo o arquivo csv e armazenando em um dataframe
df_supermarket.to_sql('tab_supermarket', engine, if_exists='replace', index=False) #populando a tabela tab_supermarket com os dados do dataframe

print(f"Carga de dados completa: {len(df_supermarket)} registros inseridos no banco de dados")

#fechar a conexão com o banco de dados
engine.dispose()

#fim do código