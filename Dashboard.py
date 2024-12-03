import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import Anls


# Título e cabeçalho
st.title("Dashboard interativo :streamlit:", help = "Organização de dados - 03/12/2024" )
st.header("Dataset: Top 1000 filmes IMDB")

# Cria diferentes abas no site
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Entendendo o dataset", "Análises com no_of_votes","A. com Runtime", "A. com Pontuação", "A. com gross", "A. com gênero","A. com ano"])

# Cria uma aba lateral com o título escrito
st.sidebar.title("Configurações")

#Adiciona uma caixa de escolha na aba lateral
nota = st.sidebar.selectbox("Escolha aqui qual pontuação do filme deve ser usada",
                    ["IMDB_Rating", "Avarage_score", "Meta_score"], help="Só se aplica a gráficos que utilizem a pontuação")

# As funções serão executas na aba x
with tab1:
  
    # Permite que o usuário escolha quais colunas ele deseja ver
    colunas = st.multiselect("Escolha as colunas que serão exibidas", Anls.df.columns, placeholder="Digite aqui")
    if colunas:
        # Põe texto no site e permite formatação
        st.write("### Dados selecionados: ###")
        st.dataframe(Anls.df[colunas])
    else:
        st.write(" *Nenhum* dado selecionado.")
    st.write("Esse dataset contém informações, como o nome sugere, sobre os 1000 filmes com maior pontuação IMDB.")
    st.write("Suas colunas são:")

    #Divide a exibição em colunas
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    #Os comandos serão executados na coluna x
    with col1:
        st.write(" **Series_Title** \nTítulo do filme\n")
        st.write("**Director**  \nNome do diretor")
    with col2:
        st.write("**Released_Year** \nData de lançamento do filme\n")
        st.write("**Stars(1,2,3,4)** \nNome das estrelas")
    with col3:
        st.write("**Runtime** \n Duração total do filme\n")
        st.write("**No_of_votes**  \nTotal de votos recebidos")
    with col4:
        st.write("**Genre**  \nGênero do filme\n")
        st.write("**Gross**  \nDinheiro arrecadado")
    with col5:
        st.write("**IMDB_Rating**  \nPontuação do filme no site do IMDB\n")
        st.write("**Score_diff**  \nDiferença entre a pontuação IMDB e o Metascore")
    with col6:
        st.write("**Meta_score**  \nNota dada pelo Metacritic ao filme\n")
        st.write("**Avarage_score**  \nPontuação média entre IMDB e o Metascore")
    st.write(Anls.df.describe())

#with tab2:

#with tab3:

#with tab4:

with tab5:
    st.write('## Análises utilizando a coluna "*Gross*" ##')

    st.write('#### Relação entre gênero e ganho bruto do filme ####')
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo5 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key="gross_p_genre")

    if tipo5 == "Barras":

        # Gera o gráfico de barras
        fig = px.bar(Anls.gross_p_genre,
                     x='Genre',
                     y='Gross',
                     orientation='v',  # Gráfico vertical
                     color_discrete_sequence=['#B22222'],  # Cor única para todas as barras (vermelho)
                     labels={'y': 'Gênero', 'x': 'Arrecadação'},
                     title='Relação entre ganho bruto do filme (em média) e seus gêneros')
        st.plotly_chart(fig)

        # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
        st.button("Resetar", type="primary", key="gross_p_genrex")
        if st.button("Ver tabela", help="Relação gênero e ganho bruto médio", key = "2"):
            st.dataframe(Anls.gross_p_genre)

    st.write('#### Relação entre o ganho bruto do filme e a sua pontuação ####')
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo5 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="gross_p_score")

    if tipo5 == "Dispersão":
        st.write(":warning: Selecione o tipo de pontuação nas configurações")

        # Gera o gráfico de barras
        fig = px.scatter(Anls.df,
                    # O tipo de pontuação é escolhida nas configurações
                     x=f'{nota}',
                     y='Gross',
                     orientation = 'v',# Gráfico vertical
                     color_discrete_sequence=['#B22222'],  # Cor única para a linha
                     title='Relação entre ganho bruto do filme (em média) e sua pontuação')
        st.plotly_chart(fig)

    st.write('#### Relação entre o ganho bruto do filme e o seu número de votos ####')
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo5 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="gross_p_votes")

    if tipo5 == "Dispersão":

        # Gera o gráfico de barras
        fig = px.scatter(Anls.df,
                         # O tipo de pontuação é escolhida nas configurações
                         x='No_of_Votes',
                         y='Gross',
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=['#B22222'],  # Cor única para a linha
                         title='Relação entre ganho bruto do filme (em média) e o seu número de votos')
        st.plotly_chart(fig)

with tab6:
    st.write('## Análises utilizando a coluna "*Genre*" ##')

    st.write("#### Ocorrência de cada gênero entre os top 1000 filmes ####")
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo6 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras", "Pizza"], key ="genre_counts")

    if tipo6 == "Barras":
        #Gera o gráfico de barras
        fig = px.bar(Anls.genre_counts,
                    x=Anls.genre_counts.index,
                    y=Anls.genre_counts.values,
                    orientation='v',  # Gráfico vertical
                    color_discrete_sequence=['#B22222'],  # Cor única para todas as barras (vermelho)
                    labels={'y': 'Gênero', 'x': 'Número de filmes'},
                    title='Ocorrência de cada gênero entre os top 1000 filmes')
        st.plotly_chart(fig)
    else:
        if tipo6 == "Pizza":
            #Gera o gráfico de Pizza ou Torta
            fig = px.pie(Anls.genre_counts,
                        values=Anls.genre_counts.values,  # Os valores são os números de filmes
                        names=Anls.genre_counts.index,  # Os rótulos são os gêneros
                        color=Anls.genre_counts.index,
                        color_discrete_sequence= px.colors.qualitative.Vivid, # Usando uma paleta de cores
                        title='Distribuição dos Gêneros entre os Top 1000 Filmes')
            st.plotly_chart(fig)

    st.write("#### Relação entre gênero e ganho bruto do filme ####")
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo6 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key ="genre_p_gross")

    if tipo6 == "Barras":

        # Gera o gráfico de barras
        fig = px.bar(Anls.gross_p_genre,
                     x='Genre',
                     y='Gross',
                     orientation='v',  # Gráfico vertical
                     color_discrete_sequence=['#B22222'],  # Cor única para todas as barras (vermelho)
                     labels={'y': 'Gênero', 'x': 'Arrecadação'},
                     title='Relação entre gênero e ganho bruto do filme (em média)')
        st.plotly_chart(fig)

        # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
        st.button("Resetar", type = "primary")
        if st.button("Ver tabela", help = "Relação gênero e ganho bruto médio"):
            st.dataframe(Anls.gross_p_genre)

    st.write("#### Relação entre gênero e duração do filme ####")
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo6 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key ="runtime_p_genre")

    if tipo6 == "Barras":

        # Gera o gráfico de barras
        fig = px.bar(Anls.runtime_p_genre,
                     x='Genre',
                     y='Runtime',
                     orientation='v',  # Gráfico vertical
                     color_discrete_sequence=['#B22222'],  # Cor única para todas as barras (vermelho)
                     labels={'y': 'Gênero', 'x': 'Duração'},
                     title='Relação entre gênero e duração do filme (em média)')
        st.plotly_chart(fig)

        # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
        st.button("Resetar", type = "primary", key = "runtime_p_genrex")
        if st.button("Ver tabela", help = "Relação gênero e duração média"):
            st.dataframe(Anls.runtime_p_genre)

    st.write("#### Relação entre gênero e ano de lançamento do filme ####")
    # Permite que o usuário faça uma escolha, nesse caso, o tipo6 de gráfico
    tipo6 = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key ="year_p_genre")

    if tipo6 == "Barras":
        # Gera o gráfico de barras
        fig = px.bar(Anls.year_p_genre,
                     x='Genre',
                     y='Released_Year',
                     orientation='v',  # Gráfico vertical
                     color_discrete_sequence=['#B22222'],  # Cor única para todas as barras (vermelho)
                     labels={'y': 'Gênero', 'x': 'Data de lançamento'},
                     title='Relação entre gênero e data de lançamento mais comum')
        st.plotly_chart(fig)

        # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
        st.button("Resetar", type = "primary", key = "year_p_genrex")
        if st.button("Ver tabela", help = "Relação gênero e data de lançamento mais comum"):
            st.dataframe(Anls.year_p_genre)

#with tab7:
