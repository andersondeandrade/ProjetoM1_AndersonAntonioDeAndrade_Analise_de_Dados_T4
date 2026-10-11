# ESTATÍSTICA DESCRITIVA, PERGUNTAS DE NEGÓCIO E GRÁFICOS (camada Resultados)

import os
import matplotlib
matplotlib.use('Agg')  # só salva as imagens, sem abrir janelas
import matplotlib.pyplot as plt
import pandas as pd

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)
CAMINHO_TRATADA = os.path.join(PASTA_PROJETO, 'data', 'processed', 'vendas_tratadas.csv')
PASTA_RESULTADOS = os.path.join(PASTA_PROJETO, 'resultados')

ORDEM_DIAS = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira',
              'Sexta-feira', 'Sábado', 'Domingo']
COR_BASE = '#9db4c0'
COR_DESTAQUE = '#1f6f8b'

respostas = []  # guarda as respostas para salvar em arquivo


def carregar_dados():
    return pd.read_csv(CAMINHO_TRATADA, parse_dates=['data_venda'])


def registrar(pergunta, resposta):
    print(f"\n{pergunta}\n  -> {resposta}")
    respostas.append(f"{pergunta}\n  -> {resposta}\n")


def cores_destaque(serie, maior=True):
    """Pinta de destaque a barra de maior (ou menor) valor."""
    alvo = serie.max() if maior else serie.min()
    return [COR_DESTAQUE if valor == alvo else COR_BASE for valor in serie]


def grafico_barras(serie, titulo, rotulo_y, arquivo, horizontal=False,
                   formato='{:,.2f}', limite=None):
    fig, ax = plt.subplots(figsize=(9, 5))
    cores = cores_destaque(serie)
    if horizontal:
        serie = serie.sort_values()
        cores = cores_destaque(serie)
        barras = ax.barh(serie.index, serie.values, color=cores)
        ax.set_xlabel(rotulo_y)
        if limite:
            ax.set_xlim(*limite)
    else:
        barras = ax.bar(serie.index, serie.values, color=cores)
        ax.set_ylabel(rotulo_y)
        if limite:
            ax.set_ylim(*limite)
    ax.bar_label(barras, labels=[formato.format(v) for v in serie.values], padding=3)
    ax.set_title(titulo, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(PASTA_RESULTADOS, arquivo), dpi=150)
    plt.close(fig)


def estatisticas_descritivas(df):
    descritivas = df[['preco_unitario', 'quantidade', 'valor_total', 'avaliacao']].describe().round(2)
    descritivas.to_csv(os.path.join(PASTA_RESULTADOS, 'estatisticas_descritivas.csv'),
                       encoding='utf-8-sig')
    print("ESTATÍSTICAS DESCRITIVAS")
    print(descritivas)


def pergunta_1_e_2(df):
    por_filial = df.groupby('filial').agg(
        faturamento=('valor_total', 'sum'), vendas=('id_venda', 'count')).round(2)
    maior_fat = por_filial['faturamento'].idxmax()
    maior_qtd = por_filial['vendas'].idxmax()
    registrar("1. Qual filial apresentou o maior faturamento?",
              f"{maior_fat} ({por_filial.loc[maior_fat, 'faturamento']:,.2f})")
    registrar("2. Qual filial realizou a maior quantidade de vendas?",
              f"{maior_qtd} ({por_filial.loc[maior_qtd, 'vendas']} vendas)")
    grafico_barras(por_filial['faturamento'].sort_values(ascending=False),
                   'Faturamento total por filial', 'Faturamento',
                   '01_faturamento_por_filial.png', formato='{:,.0f}')
    grafico_barras(por_filial['vendas'].sort_values(ascending=False),
                   'Quantidade de vendas por filial', 'Nº de vendas',
                   '02_vendas_por_filial.png', formato='{:.0f}')


def pergunta_3_e_4(df):
    por_linha = df.groupby('linha_produto').agg(
        faturamento=('valor_total', 'sum'), avaliacao=('avaliacao', 'mean'))
    linha_fat = por_linha['faturamento'].idxmax()
    linha_nota = por_linha['avaliacao'].idxmax()
    registrar("3. Qual linha de produto apresentou o maior faturamento?",
              f"{linha_fat} ({por_linha.loc[linha_fat, 'faturamento']:,.2f})")
    registrar("4. Qual linha de produto recebeu a melhor avaliação média?",
              f"{linha_nota} (nota média {por_linha.loc[linha_nota, 'avaliacao']:.2f})")
    grafico_barras(por_linha['faturamento'], 'Faturamento por linha de produto',
                   'Faturamento', '03_faturamento_por_linha_produto.png',
                   horizontal=True, formato='{:,.0f}')
    # eixo de 0 a 10 para não exagerar visualmente diferenças pequenas entre as notas
    grafico_barras(por_linha['avaliacao'], 'Avaliação média por linha de produto',
                   'Nota média (0 a 10)', '04_avaliacao_por_linha_produto.png',
                   horizontal=True, formato='{:.2f}', limite=(0, 10))


def pergunta_5(df):
    pagamentos = df['forma_pagamento'].value_counts()
    top = pagamentos.idxmax()
    percentual = pagamentos.max() / len(df) * 100
    registrar("5. Qual foi a forma de pagamento mais utilizada?",
              f"{top} ({pagamentos.max()} vendas, {percentual:.1f}% do total)")
    grafico_barras(pagamentos, 'Vendas por forma de pagamento', 'Nº de vendas',
                   '05_forma_pagamento.png', formato='{:.0f}')


def pergunta_6_e_7(df):
    media = df['valor_total'].mean()
    mediana = df['valor_total'].median()
    maior = df.loc[df['valor_total'].idxmax()]
    registrar("6. Qual foi o valor médio das vendas?",
              f"{media:,.2f} (mediana {mediana:,.2f})")
    registrar("7. Qual foi a maior venda registrada?",
              f"{maior['valor_total']:,.2f} (venda {maior['id_venda']}, "
              f"filial {maior['filial']}, {maior['linha_produto']})")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={'width_ratios': [3, 1]})
    ax1.hist(df['valor_total'], bins=25, color=COR_BASE, edgecolor='white')
    ax1.axvline(media, color=COR_DESTAQUE, linestyle='--', label=f'Média: {media:,.2f}')
    ax1.axvline(mediana, color='#e07a5f', linestyle=':', label=f'Mediana: {mediana:,.2f}')
    ax1.set_title('Distribuição do valor das vendas', fontweight='bold')
    ax1.set_xlabel('Valor da venda')
    ax1.set_ylabel('Nº de vendas')
    ax1.legend()
    ax2.boxplot(df['valor_total'], patch_artist=True,
                boxprops={'facecolor': COR_BASE})
    ax2.annotate(f"Maior venda\n{maior['valor_total']:,.2f}",
                 xy=(1, maior['valor_total']), xytext=(1.1, maior['valor_total'] - 150),
                 arrowprops={'arrowstyle': '->'})
    ax2.set_title('Boxplot', fontweight='bold')
    ax2.set_xticks([])
    for eixo in (ax1, ax2):
        eixo.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(PASTA_RESULTADOS, '06_distribuicao_valor_vendas.png'), dpi=150)
    plt.close(fig)


def pergunta_8(df):
    dias = df['dia_semana'].value_counts().reindex(ORDEM_DIAS)
    top = dias.idxmax()
    registrar("8. Em qual dia da semana ocorreu a maior quantidade de vendas?",
              f"{top} ({dias.max()} vendas)")
    grafico_barras(dias, 'Vendas por dia da semana', 'Nº de vendas',
                   '08_vendas_por_dia_semana.png', formato='{:.0f}')


def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    df = carregar_dados()
    print(f"Base tratada carregada: {len(df)} linhas\n")
    estatisticas_descritivas(df)
    pergunta_1_e_2(df)
    pergunta_3_e_4(df)
    pergunta_5(df)
    pergunta_6_e_7(df)
    pergunta_8(df)
    with open(os.path.join(PASTA_RESULTADOS, 'respostas_negocio.txt'), 'w',
              encoding='utf-8') as arquivo:
        arquivo.write('\n'.join(respostas))
    print(f"\nGráficos e respostas salvos em {PASTA_RESULTADOS}")


if __name__ == '__main__':
    main()