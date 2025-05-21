import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
import os

#Extract
#Cargar datos
# Nombre del archivo esperado dentro del dataset
filename = "chess_games.csv"

# Ruta esperada (esta puede variar, pero en general KaggleHub guarda datasets en ~/.cache/kagglehub/)
dataset_path = os.path.expanduser("~/.cache/kagglehub/datasets/arevel/chess-games/files")
file_path = os.path.join(dataset_path, filename)

# Verificar si el archivo ya existe antes de descargar
if os.path.exists(file_path):
    print("✔ El archivo ya existe localmente. Cargando datos desde disco...")
else:
    print("⬇ El archivo no existe. Descargando desde Kaggle...")
    path = kagglehub.dataset_download("arevel/chess-games")
    print("✅ Descarga completada.")
    file_path = os.path.join(path, filename)

df = pd.read_csv(file_path)
print("📄 Datos cargados correctamente.")

#Mostrar si hay datos faltantes en el DataFrame
print("Datos faltantes en el DataFrame:")
print(df.isnull().sum())

# Limpiar valores nulos
df['WhiteRatingDiff'] = df['WhiteRatingDiff'].fillna(0)
df['BlackRatingDiff'] = df['BlackRatingDiff'].fillna(0)

#Mostrar datos del DataFrame Limpio
print("Datos del DataFrame limpio:")
print(df.info())

#Transform

#Conectar a MongoDB
from pymongo import MongoClient
URI = "mongodb+srv://User:Password@cluster.krvhb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
try:
    connection = MongoClient(URI)
    print("Conexión exitosa a MongoDB.")
except Exception as e:
    print("Error al conectar a MongoDB:", e)
    exit(1)

db = connection['KaggleDataSets']
collection = db['ChessGames']

#Verificar si la colección ya contiene datos
if collection.count_documents({}) > 0:
    print("La colección ya contiene datos.")

#Insertar datos en la colección
else:
    subdf = df.head(10000)
    data = subdf.to_dict(orient='records')
    collection.insert_many(data)
    print("Datos insertados correctamente.")

#Mostrar primeros 10 datos de la colección
print("Primeros 10 datos de la colección:")
for i, doc in enumerate(collection.find().limit(10)):
    print(f"Documento {i+1}: {doc}")
