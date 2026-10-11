# ETL: raw_vendas (PostgreSQL) -> limpeza, tipagem e colunas derivadas -> vendas_tratadas

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
PASTA_PROCESSED = os.path.join(PASTA_PROJETO, 'data', 'processed')
CAMINHO_TRATADA = os.path.join(PASTA_PROCESSED, 'vendas_tratadas.csv')
CAMINHO_DICIONARIO = os.path.join(PASTA_PROCESSED, 'dicionario_dados_vendas_tratadas.csv')

# nomes originais do CSV -> nomes do dicionário de dados do projeto
RENOMEAR = {
    'Invoice ID': 'id_venda', 'Branch': 'filial', 'City': 'cidade',
    'Customer type': 'tipo_cliente', 'Gender': 'genero',
    'Product line': 'linha_produto', 'Unit price': 'preco_unitario',
    'Quantity': 'quantidade', 'Tax 5%': 'imposto', 'Sales': 'valor_total',
    'Date': 'data_venda', 'Time': 'hora_venda', 'Payment': 'forma_pagamento',
    'cogs': 'custo_mercadoria', 'gross margin percentage': 'margem_percentual',
    'gross income': 'receita_bruta', 'Rating': 'avaliacao',
}

COLUNAS_TEXTO = ['id_venda', 'filial', 'cidade', 'tipo_cliente', 'genero',
                 'linha_produto', 'forma_pagamento']
COLUNAS_NUMERICAS = ['preco_unitario', 'quantidade', 'imposto', 'valor_total',
                     'custo_mercadoria', 'margem_percentual', 'receita_bruta',
                     'avaliacao']
COLUNAS_OBRIGATORIAS = ['id_venda', 'filial', 'cidade', 'linha_produto',
                        'forma_pagamento', 'valor_total', 'data_venda']

DIAS_SEMANA = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira',
               3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}

COLUNAS_FINAIS = ['id_venda', 'filial', 'cidade', 'tipo_cliente', 'genero',
                  'linha_produto', 'preco_unitario', 'quantidade', 'imposto',
                  'valor_total', 'data_venda', 'hora_venda', 'forma_pagamento',
                  'custo_mercadoria', 'margem_percentual', 'receita_bruta',
                  'avaliacao', 'dia_semana', 'mes', 'periodo_dia']

DICIONARIO = [
    ('id_venda', 'VARCHAR(50)', 'Identificador único da venda (PK)', 'Invoice ID'),
    ('filial', 'VARCHAR(10)', 'Filial onde a venda ocorreu', 'Branch'),
    ('cidade', 'VARCHAR(100)', 'Cidade da filial', 'City'),
    ('tipo_cliente', 'VARCHAR(50)', 'Member ou Normal', 'Customer type'),
    ('genero', 'VARCHAR(20)', 'Gênero do cliente', 'Gender'),
    ('linha_produto', 'VARCHAR(150)', 'Categoria do produto', 'Product line'),
    ('preco_unitario', 'NUMERIC(10,2)', 'Preço de uma unidade (>= 0)', 'Unit price'),
    ('quantidade', 'INTEGER', 'Unidades vendidas (> 0)', 'Quantity'),
    ('imposto', 'NUMERIC(10,2)', 'Imposto de 5% da venda (>= 0)', 'Tax 5%'),
    ('valor_total', 'NUMERIC(12,2)', 'Valor total = custo + imposto (>= 0)', 'Sales'),
    ('data_venda', 'DATE', 'Data da venda (texto MM/DD/YYYY convertido)', 'Date'),
    ('hora_venda', 'TIME', 'Horário da venda (convertido)', 'Time'),
    ('forma_pagamento', 'VARCHAR(50)', 'Ewallet, Cash ou Credit card', 'Payment'),
    ('custo_mercadoria', 'NUMERIC(12,2)', 'Custo da mercadoria = preço x quantidade', 'cogs'),
    ('margem_percentual', 'NUMERIC(10,2)', 'Margem bruta percentual (constante no dataset)', 'gross margin percentage'),
    ('receita_bruta', 'NUMERIC(12,2)', 'Receita bruta (idêntica ao imposto neste dataset)', 'gross income'),
    ('avaliacao', 'NUMERIC(4,2)', 'Nota do cliente, de 0 a 10', 'Rating'),
    ('dia_semana', 'VARCHAR(15)', 'DERIVADA: dia da semana em português', 'data_venda'),
    ('mes', 'INTEGER', 'DERIVADA: mês da venda (1 a 12)', 'data_venda'),
    ('periodo_dia', 'VARCHAR(10)', 'DERIVADA: Manhã (<12h), Tarde (12h-17h) ou Noite (>=18h)', 'hora_venda'),
]


def criar_engine():
    load_dotenv(os.path.join(PASTA_PROJETO, 'config.env'))
    url = URL.create(
        'postgresql+psycopg2',
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        database=os.getenv('DB_NAME'),
    )
    return create_engine(url)


def extrair_raw(engine):
    """Lê a camada Raw (tudo texto) direto do PostgreSQL."""
    return pd.read_sql('SELECT * FROM raw_vendas', engine)


def periodo_do_dia(hora):
    if hora < 12:
        return 'Manhã'
    if hora < 18:
        return 'Tarde'
    return 'Noite'


def transformar(df):
    """Limpa, tipa e cria colunas derivadas. Mostra um relatório de cada etapa."""
    total_inicial = len(df)
    df = df.rename(columns=RENOMEAR)[list(RENOMEAR.values())].copy()

    # 1. texto: remove espaços e transforma vazio em nulo
    for coluna in COLUNAS_TEXTO + ['data_venda', 'hora_venda']:
        df[coluna] = df[coluna].astype('string').str.strip().replace('', pd.NA)

    # 2. tipagem numérica (valores inválidos viram nulo e são contados)
    for coluna in COLUNAS_NUMERICAS:
        convertida = pd.to_numeric(df[coluna], errors='coerce')
        invalidos = convertida.isna().sum() - df[coluna].isna().sum()
        if invalidos:
            print(f"[aviso] {invalidos} valor(es) não numérico(s) em {coluna}")
        df[coluna] = convertida

    # 3. tipagem de data e hora
    data = pd.to_datetime(df['data_venda'], format='%m/%d/%Y', errors='coerce')
    hora = pd.to_datetime(df['hora_venda'], format='%I:%M:%S %p', errors='coerce')
    print(f"[info] datas inválidas: {data.isna().sum()} | horas inválidas: {hora.isna().sum()}")
    df['data_venda'] = data
    df['hora_venda'] = hora

    # 4. valores ausentes: remove linhas sem campos obrigatórios
    print("[info] nulos por coluna:", int(df.isna().sum().sum()), "no total")
    antes = len(df)
    df = df.dropna(subset=COLUNAS_OBRIGATORIAS + ['hora_venda'])
    print(f"[info] linhas removidas por nulo em campo obrigatório: {antes - len(df)}")

    # 5. duplicidades
    antes = len(df)
    df = df.drop_duplicates(subset='id_venda', keep='first')
    print(f"[info] linhas removidas por id_venda duplicado: {antes - len(df)}")

    # 6. regras de negócio (mesmas dos CHECKs do banco)
    valido = (
        (df['preco_unitario'] >= 0) & (df['quantidade'] > 0)
        & (df['imposto'] >= 0) & (df['valor_total'] >= 0)
        & (df['custo_mercadoria'] >= 0) & (df['receita_bruta'] >= 0)
        & df['avaliacao'].between(0, 10)
    )
    print(f"[info] linhas que violam regras de negócio (removidas): {(~valido).sum()}")
    df = df[valido].copy()

    # 7. arredondamento para as casas decimais do banco
    for coluna in ['preco_unitario', 'imposto', 'valor_total', 'custo_mercadoria',
                   'margem_percentual', 'receita_bruta', 'avaliacao']:
        df[coluna] = df[coluna].round(2)
    df['quantidade'] = df['quantidade'].astype(int)

    # 8. conferência: valor_total = custo + imposto
    diferenca = (df['valor_total'] - (df['custo_mercadoria'] + df['imposto'])).abs()
    print(f"[info] linhas com valor_total diferente de custo + imposto: {(diferenca >= 0.02).sum()}")

    # 9. colunas derivadas (feature engineering)
    df['dia_semana'] = df['data_venda'].dt.dayofweek.map(DIAS_SEMANA)
    df['mes'] = df['data_venda'].dt.month
    df['periodo_dia'] = df['hora_venda'].dt.hour.map(periodo_do_dia)

    # 10. formato final de data e hora
    df['data_venda'] = df['data_venda'].dt.date
    df['hora_venda'] = df['hora_venda'].dt.time

    df = df[COLUNAS_FINAIS].reset_index(drop=True)
    print(f"[ok] {total_inicial} linhas lidas -> {len(df)} linhas tratadas")
    return df


def salvar_arquivos(df):
    """Salva a base tratada e o dicionário de dados em data/processed/."""
    os.makedirs(PASTA_PROCESSED, exist_ok=True)
    df.to_csv(CAMINHO_TRATADA, index=False, encoding='utf-8-sig')
    pd.DataFrame(DICIONARIO, columns=['coluna', 'tipo', 'descricao', 'origem']).to_csv(
        CAMINHO_DICIONARIO, index=False, encoding='utf-8-sig')
    print(f"[ok] salvo: {CAMINHO_TRATADA}")
    print(f"[ok] salvo: {CAMINHO_DICIONARIO}")


def carregar_tratada(df, engine):
    """Carrega a base na tabela vendas_tratadas (criada por sql/02_criar_tabelas.sql)."""
    if not inspect(engine).has_table('vendas_tratadas'):
        print("[aviso] tabela vendas_tratadas não existe. "
              "Rode sql/02_criar_tabelas.sql e execute este script de novo.")
        return
    with engine.begin() as conexao:
        conexao.execute(text('TRUNCATE TABLE vendas_tratadas'))
    df.to_sql('vendas_tratadas', engine, if_exists='append', index=False)
    print(f"[ok] {len(df)} linhas carregadas em vendas_tratadas")


def main():
    engine = criar_engine()
    df_raw = extrair_raw(engine)
    df_tratado = transformar(df_raw)
    salvar_arquivos(df_tratado)
    carregar_tratada(df_tratado, engine)
    engine.dispose()


if __name__ == '__main__':
    main()