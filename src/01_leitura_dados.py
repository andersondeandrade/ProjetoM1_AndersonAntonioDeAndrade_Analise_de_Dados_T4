# LEITURA E INSPEÇÃO INICIAL DO CSV 

import os
import pandas as pd

# mostra todas as colunas na tela, sem cortar com "..."
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
CAMINHO_CSV = os.path.join(PASTA_PROJETO, 'data', 'raw', 'SuperMarket Analysis.csv')

COLUNAS_CATEGORICAS = ['Branch', 'City', 'Customer type', 'Gender',
                       'Product line', 'Payment']


def carregar_dados(caminho):
    """Lê o CSV deixando o pandas inferir os tipos de cada coluna."""
    return pd.read_csv(caminho)


def titulo(texto):
    print(f"\n{'=' * 60}\n{texto}\n{'=' * 60}")


def inspecionar(df):
    titulo("1. DIMENSÕES")
    print(f"{df.shape[0]} linhas x {df.shape[1]} colunas")

    titulo("2. PRIMEIRAS LINHAS")
    print(df.head())

    titulo("3. TIPOS DE DADOS")
    print(df.dtypes)

    titulo("4. VALORES AUSENTES (por coluna)")
    print(df.isnull().sum())

    titulo("5. DUPLICIDADES")
    print("Linhas totalmente duplicadas:", df.duplicated().sum())
    print("Invoice ID repetido:", df['Invoice ID'].duplicated().sum())

    titulo("6. ESTATÍSTICAS DESCRITIVAS (colunas numéricas)")
    print(df.describe().round(2).T)

    titulo("7. VALORES ÚNICOS (colunas categóricas)")
    for coluna in COLUNAS_CATEGORICAS:
        print(f"{coluna}: {sorted(df[coluna].unique().tolist())}")

    titulo("8. CONSISTÊNCIA E INCONSISTÊNCIAS")
    datas = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    horas = pd.to_datetime(df['Time'], format='%I:%M:%S %p', errors='coerce')
    print("Datas inválidas:", datas.isna().sum(),
          f"| período: {datas.min().date()} a {datas.max().date()}")
    print("Horas inválidas:", horas.isna().sum())
    total_confere = (df['Sales'] - (df['cogs'] + df['Tax 5%'])).abs() < 0.01
    print("Linhas em que Sales = cogs + Tax 5%:", total_confere.sum(), "de", len(df))
    print("Avaliação mínima/máxima:", df['Rating'].min(), "/", df['Rating'].max())
    print("Quantidade mínima:", df['Quantity'].min())


if __name__ == '__main__':
    inspecionar(carregar_dados(CAMINHO_CSV))