import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# 1. Carregar e Limpar os Dados
# O arquivo CSV deve estar na mesma pasta do projeto
df = pd.read_csv("ecommerce_estatistica.csv")


def limpar_genero(genero):
    genero = str(genero).lower()
    if "masculino" in genero or "meninos" in genero:
        return "Masculino"
    elif "feminino" in genero or "meninas" in genero or "gordinha" in genero:
        return "Feminino"
    elif "unissex" in genero or "sem gênero" in genero or "bebês" in genero:
        return "Unissex"
    else:
        return "Outros"


df["Gênero_Limpo"] = df["Gênero"].apply(limpar_genero)

# 2. Criar os Gráficos Interativos com Plotly

# 2.1. Histograma
fig_hist = px.histogram(df, x="Preço", nbins=30, title="Distribuição de Preços dos Produtos",
                        labels={"Preço": "Preço (R$)", "count": "Frequência"})

# 2.2. Gráfico de Dispersão
fig_scatter = px.scatter(df, x="Preço", y="Nota", title="Relação entre Preço e Nota de Avaliação",
                         labels={"Preço": "Preço (R$)", "Nota": "Nota (Avaliação)"}, opacity=0.5)

# 2.3. Mapa de Calor (Heatmap)
corr_cols = ["Nota", "N_Avaliações", "Desconto", "Preço"]
corr = df[corr_cols].corr()
fig_heatmap = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu",
                        title="Mapa de Calor de Correlação entre Variáveis Numéricas")

# 2.4. Gráfico de Barras
top_marcas = df["Marca"].value_counts().head(10).reset_index()
top_marcas.columns = ["Marca", "Quantidade de Produtos"]
fig_bar = px.bar(top_marcas, x="Quantidade de Produtos", y="Marca", orientation="h",
                 title="Top 10 Marcas com Mais Produtos Listados",
                 color="Marca", color_discrete_sequence=px.colors.qualitative.Vivid)
fig_bar.update_layout(showlegend=False)

# 2.5. Gráfico de Pizza
genero_counts = df["Gênero_Limpo"].value_counts().reset_index()
genero_counts.columns = ["Gênero", "Contagem"]
fig_pie = px.pie(genero_counts, values="Contagem", names="Gênero",
                 title="Distribuição de Produtos por Gênero (Dados Limpos)",
                 color_discrete_sequence=px.colors.qualitative.Safe)

# 2.6. Gráfico de Densidade
fig_density = px.density_contour(df, x="Desconto", title="Estimativa de Densidade da Porcentagem de Desconto",
                                 labels={"Desconto": "Desconto (%)"})

# 2.7. Gráfico de Regressão (Visualização de Dispersão sem linha de tendência)
fig_reg = px.scatter(df, x="Preço", y="N_Avaliações",
                     title="Relação: Número de Avaliações vs. Preço do Produto",
                     labels={"Preço": "Preço (R$)", "N_Avaliações": "Número de Avaliações"},
                     opacity=0.5)

# 3. Layout da Aplicação Dash
app = Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1(children="Análise de Dados de E-commerce", style={"textAlign": "center"}),
    html.Div(children="Dashboard Interativo para Visualização de Estatísticas",
             style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        html.H3("1. Distribuição de Preços"),
        dcc.Graph(figure=fig_hist),

        html.H3("2. Preço vs. Nota"),
        dcc.Graph(figure=fig_scatter),

        html.H3("3. Correlação entre Variáveis"),
        dcc.Graph(figure=fig_heatmap),

        html.H3("4. Top 10 Marcas"),
        dcc.Graph(figure=fig_bar),

        html.H3("5. Distribuição por Gênero"),
        dcc.Graph(figure=fig_pie),

        html.H3("6. Densidade de Descontos"),
        dcc.Graph(figure=fig_density),

        html.H3("7. Relação Preço vs. Avaliações"),
        dcc.Graph(figure=fig_reg),
    ])
])

# 4. Rodar a Aplicação
if __name__ == "__main__":
    app.run(debug=True)
