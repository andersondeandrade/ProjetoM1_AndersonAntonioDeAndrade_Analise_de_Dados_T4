#CONEXÃO COM A BASE DB_SUPERMARKET

#criar bando de dados

#importar bibliotecas
import os
import psycopg2     # conversa diretamente com o PostgreSQL
from dotenv import load_dotenv
from psycopg2 import sql  # para criar queries dinamicas

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
load_dotenv(os.path.join(PASTA_PROJETO, 'config.env'))

HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
USUARIO = os.getenv('DB_USER')
SENHA = os.getenv('DB_PASSWORD')
DB_SUPERMARKET = os.getenv('DB_NAME')

#Criar conexão com o banco de dados POSTGGRESQL
conexao = psycopg2.connect(
    host=HOST,
    port=PORT,
    dbname=DB_SUPERMARKET,
    user=USUARIO,
    password=SENHA,
)

print(f"Conexão com o banco de dados {DB_SUPERMARKET} estabelecida com sucesso!")


#fechar a conexão
conexao.close()