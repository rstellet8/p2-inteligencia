# Modelagem de Risco de crédito

## AP2 - Inteligência de Mercado

Fonte dos dados:

1. empréstimos: <https://www.kaggle.com/wordsforthewise/lending-club>

2. CPI: <https://fred.stlouisfed.org/series/USACPIALLMINMEI>

3. Taxa de Juros: <https://fred.stlouisfed.org/series/FEDFUNDS>

Documentação dos dados: <https://resources.lendingclub.com/LCDataDictionary.xlsx>

Também disponível em:

1. [Arquivo estático](https://github.com/rstellet8/p2-inteligencia/blob/main/data/docs/)

2. [Wrapper para Dataframe](https://github.com/rstellet8/p2-inteligencia/blob/main/description.py)

## Conteúdo

- sepAmostra: Extrai uma amostra de 10000 linhas dos dados originais
- featureDiscovery: Limpeza, transformação, criação de novos features
- description: extrai a descrição das colunas para um DataFrame
- getIntRate: extrai informações sobre a taxa de juros dos EUA do site do FRED
- getCPI: extrai informações sobre a inflação dos EUA do site do FRED
