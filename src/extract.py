# EXTRAÇÃO: roda as consultas SQL na raw_vendas e exporta os resultados em CSV

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
PASTA_RAW = os.path.join(PASTA_PROJETO, 'data', 'raw')
load_dotenv(os.path.join(PASTA_PROJETO, 'config.env'))

url = URL.create(
    'postgresql+psycopg2',
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
)
engine = create_engine(url)


def executar_e_salvar(query, nome_arquivo, titulo):
    """Executa a consulta, salva o resultado em data/raw/ e mostra na tela."""
    df = pd.read_sql(query, engine)
    df.to_csv(os.path.join(PASTA_RAW, nome_arquivo), index=False, encoding='utf-8-sig')
    print(f"\n{titulo}")
    print(df)
    return df


# Perguntas 1, 2 e 5: faturamento e quantidade de vendas por filial
executar_e_salvar("""
    SELECT
        "Branch" AS filial,
        COUNT(*) AS quantidade_vendas,
        SUM("Sales"::numeric) AS faturamento_total
    FROM raw_vendas
    GROUP BY "Branch"
    ORDER BY faturamento_total DESC;
""", 'vendas_por_filial.csv', 'Resumo por filial:')

# Perguntas 2 e 7: faturamento, quantidade e avaliação por linha de produto
executar_e_salvar("""
    SELECT
        "Product line" AS linha_produto,
        COUNT(*) AS quantidade_vendida,
        SUM("Sales"::numeric) AS faturamento_total,
        AVG("Rating"::numeric) AS nota_media
    FROM raw_vendas
    GROUP BY "Product line"
    ORDER BY faturamento_total DESC;
""", 'vendas_por_produto.csv', 'Resumo por linha de produto:')

# Pergunta 3: forma de pagamento mais utilizada
executar_e_salvar("""
    SELECT
        "Payment" AS forma_pagamento,
        COUNT(*) AS quantidade
    FROM raw_vendas
    GROUP BY "Payment"
    ORDER BY quantidade DESC;
""", 'forma_pagamento.csv', 'Forma de pagamento mais usada:')

# Pergunta 4: valor médio das vendas
executar_e_salvar("""
    SELECT AVG("Sales"::numeric) AS valor_medio_venda
    FROM raw_vendas;
""", 'valor_medio_venda.csv', 'Valor médio das vendas:')

# Maior venda registrada
executar_e_salvar("""
    SELECT
        "Invoice ID" AS id_venda,
        "Branch" AS filial,
        "Product line" AS linha_produto,
        "Sales"::numeric AS valor_venda
    FROM raw_vendas
    ORDER BY "Sales"::numeric DESC
    LIMIT 1;
""", 'maior_venda.csv', 'Maior venda registrada:')

# Pergunta 6: quantidade de vendas por dia da semana (em português)
executar_e_salvar("""
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
    FROM raw_vendas
    GROUP BY EXTRACT(DOW FROM TO_DATE("Date", 'MM/DD/YYYY'))
    ORDER BY quantidade_vendas DESC;
""", 'vendas_por_dia_semana.csv', 'Vendas por dia da semana:')

engine.dispose()
print("\nCSVs salvos com sucesso em data/raw/")