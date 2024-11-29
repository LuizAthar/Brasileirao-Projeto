from flask import render_template, request
from app import app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from collections import Counter

# Carregando os datasets necessários para a aplicação
# Esses arquivos contêm dados de partidas realizadas, não realizadas, classificação e previsões
partidas_realizadas = pd.read_csv("datasets/Partidas_Realizadas.csv")
partidas_nao_realizadas = pd.read_csv("datasets/Partidas_Nao_Realizadas.csv")
classificacao = pd.read_csv("datasets/Classificacao.csv")
previcao = pd.read_csv("datasets/previcao.csv")

############################################################################################################################
# Função calcular_estatisticas
# Calcula estatísticas básicas sobre as partidas realizadas, incluindo:
# - Percentual de vitórias dos mandantes.
# - Percentual de empates.
# - Percentual de vitórias dos visitantes.
# Também identifica os 5 placares mais frequentes.
############################################################################################################################
def calcular_estatisticas(partidas):
    estatisticas = {}

    # Calculando o total de vitórias, empates e derrotas
    vitorias_mandantes = partidas[partidas['Placar_Mandante'] > partidas['Placar_Visitante']].shape[0]
    empates = partidas[partidas['Placar_Mandante'] == partidas['Placar_Visitante']].shape[0]
    vitorias_visitantes = partidas[partidas['Placar_Mandante'] < partidas['Placar_Visitante']].shape[0]
    total_partidas = partidas.shape[0]

    # Calculando os percentuais de cada tipo de resultado
    estatisticas['vitorias_mandantes'] = vitorias_mandantes / total_partidas * 100
    estatisticas['empates'] = empates / total_partidas * 100
    estatisticas['vitorias_visitantes'] = vitorias_visitantes / total_partidas * 100

    # Identificando os 5 placares mais frequentes
    placares = partidas.apply(lambda row: f"{row['Placar_Mandante']}x{row['Placar_Visitante']}", axis=1)
    placares_freq = Counter(placares).most_common(5)
    estatisticas['placares_freq'] = placares_freq

    return estatisticas

############################################################################################################################
# Função gerar_grafico_barras
# Gera um gráfico de barras que mostra a distribuição dos resultados:
# - Vitórias dos mandantes.
# - Vitórias dos visitantes.
# - Empates.
# O gráfico é retornado em formato Base64 para ser renderizado no HTML.
############################################################################################################################
def gerar_grafico_barras(partidas):
    resultados = partidas.copy()

    # Adicionando uma nova coluna para categorizar os resultados
    resultados['Resultado'] = resultados.apply(
        lambda row: 'Mandante' if row['Placar_Mandante'] > row['Placar_Visitante']
        else ('Visitante' if row['Placar_Mandante'] < row['Placar_Visitante'] else 'Empate'), axis=1
    )

    # Criando o gráfico de barras
    plt.figure(figsize=(8, 6))
    sns.countplot(data=resultados, x='Resultado', hue='Resultado', palette='viridis', legend=False)
    plt.title("Distribuição de Resultados")
    plt.xlabel("Resultado")
    plt.ylabel("Quantidade")

    # Salvando o gráfico como Base64
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return img_base64

############################################################################################################################
# Função gerar_grafico_pizza
# Gera um gráfico de pizza com os 10 times que mais venceram como mandantes.
# O gráfico é salvo como Base64 para renderização no HTML.
############################################################################################################################
def gerar_grafico_pizza():
    # Filtrando partidas onde o mandante venceu
    vitorias_mandantes = partidas_realizadas[partidas_realizadas['Placar_Mandante'] > partidas_realizadas['Placar_Visitante']]

    # Contando vitórias por time
    vitorias_por_time = vitorias_mandantes['Mandante'].value_counts()

    # Selecionando os 10 times com mais vitórias
    top_10_vitorias = vitorias_por_time.head(10)

    # Criando o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(
        top_10_vitorias,
        labels=top_10_vitorias.index,
        autopct='%1.1f%%',
        startangle=155,
        colors=sns.color_palette("pastel")
    )
    plt.title("Top 10 Times com Mais Vitórias como Mandantes")

    # Salvando o gráfico como Base64
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return img_base64

############################################################################################################################
# Função gerar_classificacao_top_10
# Filtra e retorna os 10 melhores times da classificação geral com base em pontos.
############################################################################################################################
def gerar_classificacao_top_10():
    classificacao_2024 = classificacao[(classificacao['Rodada'] >= 1) & (classificacao['Rodada'] <= 38)]
    top_10_classificacao = classificacao_2024.sort_values(by='Pontos', ascending=False).head(10)
    return top_10_classificacao

############################################################################################################################
# Rota /
# Rota principal do sistema:
# - Calcula estatísticas gerais.
# - Gera gráficos de barras e pizza.
# - Exibe a classificação geral e o top 10.
# - Permite filtrar jogos por rodada selecionada.
############################################################################################################################
@app.route('/', methods=['GET'])
def dashboard():
    # Obtendo rodadas disponíveis para filtro
    rodadas_disponiveis = partidas_nao_realizadas['Rodada'].unique().tolist()
    selected_rodada = request.args.get('rodada', None)

    # Filtrando partidas da rodada selecionada, caso exista
    if selected_rodada:
        partidas_filtradas = partidas_nao_realizadas[partidas_nao_realizadas['Rodada'] == int(selected_rodada)]
    else:
        partidas_filtradas = partidas_nao_realizadas

    # Calculando estatísticas e gerando gráficos
    estatisticas = calcular_estatisticas(partidas_realizadas)
    img_barras = gerar_grafico_barras(partidas_realizadas)
    classificacao_html = gerar_classificacao()
    top_10_classificacao = gerar_classificacao_top_10()
    img_pizza = gerar_grafico_pizza()

    # Renderizando o HTML com todas as informações
    return render_template('dashboard.html', 
                           estatisticas=estatisticas, 
                           img_barras=img_barras,
                           classificacao_html=classificacao_html, 
                           partidas_nao_realizadas=partidas_filtradas,
                           rodadas=rodadas_disponiveis,
                           selected_rodada=selected_rodada,
                           top_10_classificacao=top_10_classificacao,
                           img_pizza=img_pizza)

