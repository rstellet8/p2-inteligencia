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

- featureDiscovery: Limpeza, transformação, criação de novos features
- sepAmostra: Extrai uma amostra de 10000 linhas dos dados originais
- description: extrai a descrição das colunas para um DataFrame
- getIntRate: extrai informações sobre a taxa de juros dos EUA do site do FRED
- getCPI: extrai informações sobre a inflação dos EUA do site do FRED

## Ordem de leitura

1. [featureDiscovery.ipynb](https://github.com/rstellet8/p2-inteligencia/blob/main/featureDiscovery.ipynb): onde é feita a seleção e limpeza das variáveis
2. [modelagem.ipynb](https://github.com/rstellet8/p2-inteligencia/blob/main/modelagem.ipynb): onde é feita a modelagem das variáveis

### Opcionais

- [utils/sepAmostra.ipynb](https://github.com/rstellet8/p2-inteligencia/blob/main/utils/sepAmostra.ipynb): Script usado para retirar uma amostra de 10000 linhas dos dados orinais;
- [utils/description.ipynb](https://github.com/rstellet8/p2-inteligencia/blob/main/utils/description.ipynb): Script usado para obter a descrição dos dados em uma DataFrame;
- [utils/getCPI.ipynb](https://github.com/rstellet8/p2-inteligencia/blob/main/utils/getCPI.ipynb): extrai os dados oficiais do CPI do site do FRED;
- [utils/getIntRate.ipynb](https://github.com/rstellet8/p2-inteligencia/blob/main/utils/getIntRate.ipynb): extrai os dados oficiais da taxa de juros básica do site do FRED.
