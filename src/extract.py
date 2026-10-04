import os
import pandas as pd
from sqlalchemy import create_engine

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)

engine = create_engine('postgresql+psycopg2://postgres:030988@localhost:5432/DB_SUPERMARKET')

# Query 1: faturamento e quantidade por filial
query_filial = """
    SELECT 
        "Branch" AS filial,
        COUNT(*) AS quantidade_vendas,
        SUM("Sales"::numeric) AS faturamento_total
    FROM tab_supermarket
    GROUP BY "Branch"
    ORDER BY faturamento_total DESC;
"""
df_filial = pd.read_sql(query_filial, engine)
caminho_filial = os.path.join(PASTA_PROJETO, 'data', 'raw', 'vendas_por_filial.csv')
df_filial.to_csv(caminho_filial, index=False)
print("Resumo por filial:")
print(df_filial)

# Query 2: faturamento, quantidade e avaliação por linha de produto
query_produto = """
    SELECT 
        "Product line" AS linha_produto,
        COUNT(*) AS quantidade_vendida,
        SUM("Sales"::numeric) AS faturamento_total,
        AVG("Rating"::numeric) AS nota_media
    FROM tab_supermarket
    GROUP BY "Product line"
    ORDER BY faturamento_total DESC;
"""
df_produto = pd.read_sql(query_produto, engine)
caminho_produto = os.path.join(PASTA_PROJETO, 'data', 'raw', 'vendas_por_produto.csv')
df_produto.to_csv(caminho_produto, index=False)
print("\nResumo por produto:")
print(df_produto)

engine.dispose()
print("\nCSVs salvos com sucesso em data/raw/")