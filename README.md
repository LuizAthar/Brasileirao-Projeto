Projeto Brasileirão ⚽

Esse projeto foi desenvolvido com o objetivo de analisar partidas do Brasileirão e fazer previsões dos resultados com base em dados históricos. 
Ele apresenta estatísticas, gráficos interativos e previsões de jogos futuros, usando Python e Flask para criar uma interface web acessível.

---------------     ---------------     ---------------     ---------------     ---------------     ---------------     ---------------     

🛠️ Como Rodar o Projeto
Siga os passos abaixo para rodar o projeto no seu computador:

1º Clone o repositório:

git clone https://github.com/SamuelMauli/Brasileirao-Projeto

2º Entre na pasta do projeto:

python -m venv .venv

3º Instale as dependências do projeto:

pip install -r requirements.txt

4º Inicie o servidor:

python run.py

5º Acesse a aplicação no navegador: 

http://127.0.0.1:5000/

---------------     ---------------     ---------------     ---------------     ---------------     ---------------     ---------------     

📂 Estrutura do Projeto
O projeto está organizado da seguinte forma:

app/:
Contém os principais arquivos da aplicação Flask.
__init__.py: Inicializa o Flask.
routes.py: Define as rotas da aplicação.
---------------     ---------------     
datasets/:
Pasta com os dados usados no projeto:
Partidas_Realizadas.csv: Dados de partidas realizadas.
Partidas_Nao_Realizadas.csv: Lista de partidas futuras.
---------------     ---------------     
Classificacao.csv: 
Classificação do campeonato.
previcao.csv: Resultados previstos.
---------------     ---------------     
run.py:
Arquivo principal que inicia o servidor Flask.
---------------     ---------------     
requirements.txt:
Lista de bibliotecas necessárias.

---------------     ---------------     ---------------     ---------------     ---------------     ---------------     ---------------

📊 Funcionalidades
O projeto conta com as seguintes funcionalidades:

Dashboard Interativo:

Estatísticas gerais das partidas realizadas (ex.: vitórias, empates, derrotas).
Gráficos de barras e pizza mostrando tendências e desempenhos.
Classificação oficial atualizada e top 10 times.
---------------     ---------------
Previsões:

Exibição de previsões de partidas não realizadas.
Placar estimado para cada time usando aprendizado de máquina.
Gráficos Gerados:

Distribuição de resultados.
Ranking dos 10 times com mais vitórias como mandantes.

---------------     ---------------     ---------------     ---------------     ---------------     ---------------     ---------------

📈 Tecnologias Usadas
O projeto foi desenvolvido utilizando as seguintes ferramentas e bibliotecas:

Flask: Framework web para criar a aplicação.
Pandas: Manipulação e análise dos dados.
Matplotlib e Seaborn: Criação de gráficos.
Plotly: Visualizações interativas.
Random Forest: Algoritmo para prever os placares.

---------------     ---------------     ---------------     ---------------     ---------------     ---------------     ---------------

📝 Contribuições
Este projeto foi desenvolvido por um grupo de alunos:
Samuel Mauli
Luiz Gabriel Vicentin Lopes
Pedro Ferreira Rossi
Luiz Eduardo Aben Athar Ribeiro




