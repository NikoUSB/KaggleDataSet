import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
from pymongo import MongoClient

# Conexión a MongoDB
URI = "mongodb+srv://User:Password@cluster.krvhb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
try:
    client = MongoClient(URI)
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectarse a la base de datos:", e)
    exit()

db = client["KaggleDataSets"]
collection = db["ChessGames"]

# Cargar datos desde MongoDB
data = list(collection.find().limit(100000))
df = pd.DataFrame(data)

# Limpiar columnas innecesarias
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# Limpiar nulos si es necesario
df['White'] = df['White'].fillna("Unknown")
df['Black'] = df['Black'].fillna("Unknown")
df['Result'] = df['Result'].fillna("Unknown")

# ------------------------
# Top 10 Blancos ganadores
# ------------------------
white_winners = df[df['Result'] == '1-0']['White'].value_counts().head(10).reset_index()
white_winners.columns = ['Jugador', 'Victorias como Blancas']

fig_white = px.bar(white_winners,
                   x='Jugador',
                   y='Victorias como Blancas',
                   title='Top 10 Jugadores con más victorias como Blancas',
                   labels={'Jugador': 'Jugador', 'Victorias como Blancas': 'Victorias'},
                   color='Victorias como Blancas')

# ------------------------
# Top 10 Negros ganadores
# ------------------------
black_winners = df[df['Result'] == '0-1']['Black'].value_counts().head(10).reset_index()
black_winners.columns = ['Jugador', 'Victorias como Negras']

fig_black = px.bar(black_winners,
                   x='Jugador',
                   y='Victorias como Negras',
                   title='Top 10 Jugadores con más victorias como Negras',
                   labels={'Jugador': 'Jugador', 'Victorias como Negras': 'Victorias'},
                   color='Victorias como Negras')

# ------------------------
# Distribución de Resultados
# ------------------------
result_dist = df['Result'].value_counts().reset_index()
result_dist.columns = ['Resultado', 'Cantidad']

fig_result = px.pie(result_dist,
                    names='Resultado',
                    values='Cantidad',
                    title='Distribución de Resultados de Partidas')

# ------------------------
# Layout de la app Dash
# ------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Partidas de Ajedrez", style={'textAlign': 'center', 'padding': '20px'}),

    html.Div([
        dcc.Graph(figure=fig_white)
    ], style={'width': '100%', 'padding': '20px 0'}),

    html.Div([
        dcc.Graph(figure=fig_black)
    ], style={'width': '100%', 'padding': '20px 0'}),

    html.Div([
        dcc.Graph(figure=fig_result)
    ], style={'width': '100%', 'padding': '20px 0'}),
])


if __name__ == '__main__':
    app.run_server(debug=True)
