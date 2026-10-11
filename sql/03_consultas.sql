--query que responde as perguntas 1 e 2 (faturamento e quantidade de vendas por filial)
SELECT 
    "Branch" AS filial,
    COUNT(*) AS quantidade_vendas,
    SUM("Sales"::numeric) AS faturamento_total
FROM raw_vendas
GROUP BY "Branch"
ORDER BY faturamento_total DESC;

--Query que responde perguntas sobre produto (quais vendem mais, faturamento, avaliação)
SELECT 
    "Product line" AS linha_produto,
    COUNT(*) AS quantidade_vendida,
    SUM("Sales"::numeric) AS faturamento_total,
    AVG("Rating"::numeric) AS nota_media
FROM raw_vendas
GROUP BY "Product line"
ORDER BY faturamento_total DESC;

SELECT COUNT(*) FROM raw_vendas;

SELECT COUNT(*) FROM vendas_tratadas; --conferindo se a quantidade de registros na tabela tratada é igual à quantidade de registros na tabela raw (deve ser igual, pois não houve exclusão de registros, apenas transformação de tipos e validação de constraints)