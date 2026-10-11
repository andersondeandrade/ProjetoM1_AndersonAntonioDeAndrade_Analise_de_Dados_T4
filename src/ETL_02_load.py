#populando a tabela db_metalurgia com dos dados do arquivo CSV

#importar bibliotecas
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# carregar credenciais (config.env na raiz do projeto)
PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
load_dotenv(os.path.join(PASTA_PROJETO, 'config.env'))

#definir o caminho do arquivo CSV
CAMINHO_CSV = os.path.join(PASTA_PROJETO, 'data', 'raw', 'SuperMarket Analysis.csv')

# montar a conexão com o PostgreSQL
url = URL.create(
    'postgresql+psycopg2',
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
)
engine = create_engine(url)

# ler o CSV tudo como texto, sem alterar nada (camada Raw = cópia fiel)
df_supermarket = pd.read_csv(CAMINHO_CSV, dtype=str,keep_default_na=False) #lendo o arquivo csv e armazenando em um dataframe

# gravar na tabela raw_vendas
df_supermarket.to_sql('raw_vendas', engine, if_exists='replace', index=False) #populando a tabela tab_supermarket com os dados do dataframe

print(f"Carga de dados completa: {len(df_supermarket)} registros inseridos em raw_vendas")

#fechar a conexão com o banco de dados
engine.dispose()

#fim do código