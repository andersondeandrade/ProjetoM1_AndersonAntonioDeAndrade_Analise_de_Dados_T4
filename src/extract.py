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

# Query 3: forma de pagamento mais utilizada
query_pagamento = """
    SELECT 
        "Payment" AS forma_pagamento,
        COUNT(*) AS quantidade
    FROM tab_supermarket
    GROUP BY "Payment"
    ORDER BY quantidade DESC;
"""
df_pagamento = pd.read_sql(query_pagamento, engine)
caminho_pagamento = os.path.join(PASTA_PROJETO, 'data', 'raw', 'forma_pagamento.csv')
df_pagamento.to_csv(caminho_pagamento, index=False)
print("\nForma de pagamento mais usada:")
print(df_pagamento)

# Query 4: valor médio das vendas
query_media = """
    SELECT AVG("Sales"::numeric) AS valor_medio_venda
    FROM tab_supermarket;
"""
df_media = pd.read_sql(query_media, engine)
print("\nValor médio das vendas:")
print(df_media)

# Query 6: quantidade de vendas por dia da semana (em português)
query_periodo = """
    SELECT 
        CASE EXTRACT(DOW FROM TO_DATE("Date", 'MM/DD/YYYY'))
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana,
        COUNT(*) AS quantidade_vendas
    FROM tab_supermarket
    GROUP BY EXTRACT(DOW FROM TO_DATE("Date", 'MM/DD/YYYY'))
    ORDER BY quantidade_vendas DESC;
"""
df_periodo = pd.read_sql(query_periodo, engine)
caminho_periodo = os.path.join(PASTA_PROJETO, 'data', 'raw', 'vendas_por_dia_semana.csv')
df_periodo.to_csv(caminho_periodo, index=False, encoding='utf-8-sig')
print("\nVendas por dia da semana:")
print(df_periodo)