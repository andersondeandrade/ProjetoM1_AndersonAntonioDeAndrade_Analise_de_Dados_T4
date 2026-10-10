#criar bando de dados

#importar bibliotecas
import psycopg2     # conversa diretamente com o PostgreSQL
from psycopg2 import sql  # para criar queries dinamicas

import os
from dotenv import load_dotenv

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
load_dotenv(os.path.join(PASTA_PROJETO, 'config.env'))

HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
USUARIO = os.getenv('DB_USER')
SENHA = os.getenv('DB_PASSWORD')
DBNAME = 'postgres'                 # banco usado só para conectar e criar o outro
NOME_BASE = os.getenv('DB_NAME')    # banco que será criado (DB_SUPERMARKET)

#Criar conexão com o banco de dados POSTGGRESQL
conexao = psycopg2.connect(
    host=HOST,
    port=PORT,
    dbname=DBNAME,
    user=USUARIO,
    password=SENHA,
    
)

conexao.autocommit = True  # para não precisar dar commit a cada comando

cursor = conexao.cursor()  # criar um cursor para executar comandos SQL

#verificar se ja existe um banco de dados com o mesmo nome
cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (NOME_BASE,))

#se a não encontrar o banco de dados, criar um novo banco de dados
if cursor.fetchone() is None:
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(NOME_BASE)))
    print(f"Banco de dados {NOME_BASE} criado com sucesso!")
else:
    print(f"Banco de dados {NOME_BASE} já existe.")
    
# fechar o cursor e a conexão
cursor.close()
conexao.close()

#fim do código