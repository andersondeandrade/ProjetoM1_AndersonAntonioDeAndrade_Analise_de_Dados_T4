-- ============ CAMADA RAW: cópia fiel do CSV (criada pelo ETL_02_load.py) ============
-- raw_vendas é criada e carregada por src/ETL_02_load.py, todas as colunas em texto.

-- ============ CAMADA TRATADA: tipada, com constraints ============
CREATE TABLE IF NOT EXISTS vendas_tratadas (
    id_venda           VARCHAR(50)   PRIMARY KEY,
    filial             VARCHAR(10)   NOT NULL,
    cidade             VARCHAR(100)  NOT NULL,
    tipo_cliente       VARCHAR(50),
    genero             VARCHAR(20),
    linha_produto      VARCHAR(150)  NOT NULL,
    preco_unitario     NUMERIC(10,2) CHECK (preco_unitario >= 0),
    quantidade         INTEGER       CHECK (quantidade > 0),
    imposto            NUMERIC(10,2) CHECK (imposto >= 0),
    valor_total        NUMERIC(12,2) CHECK (valor_total >= 0),
    data_venda         DATE,
    hora_venda         TIME,
    forma_pagamento    VARCHAR(50)   NOT NULL,
    custo_mercadoria   NUMERIC(12,2) CHECK (custo_mercadoria >= 0),
    margem_percentual  NUMERIC(10,2),
    receita_bruta      NUMERIC(12,2) CHECK (receita_bruta >= 0),
    avaliacao          NUMERIC(4,2)  CHECK (avaliacao BETWEEN 0 AND 10),
    dia_semana         VARCHAR(15),
    mes                INTEGER       CHECK (mes BETWEEN 1 AND 12),
    periodo_dia        VARCHAR(10),
    CONSTRAINT chk_total_coerente
        CHECK (ABS(valor_total - (custo_mercadoria + imposto)) < 0.02)
);