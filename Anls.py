import pandas as pd
from wordcloud import WordCloud
from itertools import combinations, product
import millify as mils

""" Inicializando o Dataset """

df = pd.read_csv('imdb_top_1000.csv')

# Mostra os primeiros 100 ítems do dataset
df.head(100)


"""Entendendo o dataset """

# Retorna o formato do dataset, linhas x colunas
df.shape

# Mostra quais colunas possuem alguma linha com valor nulo
df.isna().any()

# Mostra uma tabela, com informações sobre cada coluna numérica (média, min, máximo, etc.)
df.describe()


""" Limpando o dataset """

# Formatando as colunas numéricas
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
df['Runtime'] = pd.to_numeric(df['Runtime'].str.replace('min', ''), errors='coerce')
df['Gross'] = pd.to_numeric(df['Gross'].str.replace(',', ''), errors='coerce')
pd.options.display.float_format = '{:.2f}'.format

# Substituindo os valores vazios pela média
df['Meta_score'] = df['Meta_score'].fillna(df['Meta_score'].mean())
df['Gross'] = df['Gross'].fillna(df['Gross'].mean())

#Retirando colunas que não são relevantes para a análise
df = df.drop(columns=['Poster_Link', 'Overview', 'Certificate'])

#Consertando uma data de lançamento
df.loc[966, 'Released_Year'] = 1995

# Criando colunas complementares para a análise
df['Score_diff'] = abs(df['IMDB_Rating'] * 10 - df['Meta_score'])
df['Avarage_score'] = (df['IMDB_Rating'] * 10 + df['Meta_score']) / 2

df.describe()

""" Gerando visualizações """

# Separa os gêneros em listas e "explode" para obter cada gênero em uma linha separada
all_genres = df['Genre'].str.split(',').explode().str.strip()

# Obtém uma lista de gêneros únicos
unique_genres = all_genres.unique()

# Cria uma cópia do Dataframe original
df_copy= df.copy()

df_copy['Genre'] = df_copy['Genre'].str.split(',')
df_exp = df_copy.explode("Genre").drop_duplicates(subset='Gross', keep='first')

# Esse bloco de código cria uma tabela com arrecadação média por gênero
gross_p_genre = df_exp.groupby('Genre')['Gross'].mean().reset_index()
gross_p_genre = gross_p_genre.sort_values(by='Gross', ascending=True)

# Esse bloco de código cria uma tabela com duração média por gênero
runtime_p_genre = df_exp.groupby('Genre')['Runtime'].mean().reset_index()
runtime_p_genre = runtime_p_genre.sort_values(by='Runtime', ascending=True)

# Esse bloco de código cria uma tabela com ano mais comum de lançamento por gênero
year_p_genre = df_exp.groupby('Genre')['Released_Year'].agg(lambda x: x.mode()[0]).reset_index()
year_p_genre = year_p_genre.sort_values(by='Released_Year', ascending=True)

# Lista com a quantidade de cada gênero
genre_counts = all_genres.value_counts()
genre_counts = genre_counts.sort_values(ascending=True)








