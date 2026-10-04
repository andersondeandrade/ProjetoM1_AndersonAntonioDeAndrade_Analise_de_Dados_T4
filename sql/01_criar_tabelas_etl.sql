SELECT * FROM tab_supermarket LIMIT 5; #testando conexão com o banco de dados e a tabela criada
SELECT "Branch", "Sales" FROM tab_supermarket LIMIT 5; #testando uma coluna

#query que responde as perguntas 1 e 2 (faturamento e quantidade de vendas por filial)
SELECT 
    "Branch" AS filial,
    COUNT(*) AS quantidade_vendas,
    SUM("Sales"::numeric) AS faturamento_total
FROM tab_supermarket
GROUP BY "Branch"
ORDER BY faturamento_total DESC;

#Query que responde perguntas sobre produto (quais vendem mais, faturamento, avaliação)
SELECT 
    "Product line" AS linha_produto,
    COUNT(*) AS quantidade_vendida,
    SUM("Sales"::numeric) AS faturamento_total,
    AVG("Rating"::numeric) AS nota_media
FROM tab_supermarket
GROUP BY "Product line"
ORDER BY faturamento_total DESC;