import requests
import json
from datetime import datetime
import numpy as np
import os

import pandas as pd 
from time import sleep

# Mes 50 villes de france
villes = [
    {"nom": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"nom": "Marseille", "lat": 43.2965, "lon": 5.3698},
    {"nom": "Lyon", "lat": 45.7640, "lon": 4.8357},
    {"nom": "Toulouse", "lat": 43.6047, "lon": 1.4442},
    {"nom": "Nice", "lat": 43.7102, "lon": 7.2620},
    {"nom": "Nantes", "lat": 47.2184, "lon": -1.5536},
    {"nom": "Strasbourg", "lat": 48.5734, "lon": 7.7521},
    {"nom": "Montpellier", "lat": 43.6108, "lon": 3.8767},
    {"nom": "Bordeaux", "lat": 44.8378, "lon": -0.5792},
    {"nom": "Lille", "lat": 50.6292, "lon": 3.0573},
    {"nom": "Rennes", "lat": 48.1173, "lon": -1.6778},
    {"nom": "Reims", "lat": 49.2583, "lon": 4.0317},
    {"nom": "Le Havre", "lat": 49.4944, "lon": 0.1079},
    {"nom": "Saint-Étienne", "lat": 45.4397, "lon": 4.3872},
    {"nom": "Toulon", "lat": 43.1242, "lon": 5.9280},
    {"nom": "Angers", "lat": 47.4784, "lon": -0.5632},
    {"nom": "Grenoble", "lat": 45.1885, "lon": 5.7245},
    {"nom": "Dijon", "lat": 47.3220, "lon": 5.0415},
    {"nom": "Nîmes", "lat": 43.8367, "lon": 4.3601},
    {"nom": "Aix-en-Provence", "lat": 43.5297, "lon": 5.4474},
    {"nom": "Brest", "lat": 48.3904, "lon": -4.4861},
    {"nom": "Clermont-Ferrand", "lat": 45.7772, "lon": 3.0870},
    {"nom": "Limoges", "lat": 45.8336, "lon": 1.2611},
    {"nom": "Tours", "lat": 47.3941, "lon": 0.6848},
    {"nom": "Amiens", "lat": 49.8950, "lon": 2.3023},
    {"nom": "Perpignan", "lat": 42.6887, "lon": 2.8948},
    {"nom": "Metz", "lat": 49.1193, "lon": 6.1757},
    {"nom": "Besançon", "lat": 47.2378, "lon": 6.0241},
    {"nom": "Orléans", "lat": 47.9029, "lon": 1.9093},
    {"nom": "Mulhouse", "lat": 47.7508, "lon": 7.3359},
    {"nom": "Rouen", "lat": 49.4432, "lon": 1.0993},
    {"nom": "Caen", "lat": 49.1829, "lon": -0.3707},
    {"nom": "Nancy", "lat": 48.6921, "lon": 6.1844},
    {"nom": "Saint-Denis", "lat": 48.9362, "lon": 2.3574},
    {"nom": "Argenteuil", "lat": 48.9472, "lon": 2.2460},
    {"nom": "Montreuil", "lat": 48.8638, "lon": 2.4480},
    {"nom": "Roubaix", "lat": 50.6929, "lon": 3.1744},
    {"nom": "Tourcoing", "lat": 50.7230, "lon": 3.1617},
    {"nom": "Nanterre", "lat": 48.8924, "lon": 2.2066},
    {"nom": "Avignon", "lat": 43.9493, "lon": 4.8055},
    {"nom": "Vitry-sur-Seine", "lat": 48.7872, "lon": 2.3956},
    {"nom": "Créteil", "lat": 48.7904, "lon": 2.4554},
    {"nom": "Poitiers", "lat": 46.5802, "lon": 0.3404},
    {"nom": "Colmar", "lat": 48.0790, "lon": 7.3585},
    {"nom": "Aulnay-sous-Bois", "lat": 48.9420, "lon": 2.4932},
    {"nom": "Saint-Pierre", "lat": 21.3399, "lon": 55.4781},
    {"nom": "Cannes", "lat": 43.5528, "lon": 7.0174},
    {"nom": "Calais", "lat": 50.9513, "lon": 1.8587}
]


# récupération des donées dans le df
donnees_meteo = []

for v in villes:
    nom = v["nom"]
    lat = v["lat"]
    lon = v["lon"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json();
        meteo = data.get("current_weather",{})
        meteo["ville"] = nom
        meteo["date_recolte"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        donnees_meteo.append(meteo)
    else:
        print(f" Erreur pour {nom}")

    sleep(1)  

    df = pd.DataFrame(donnees_meteo)


# Nettoyage des donées avec Numpy

print("Valeurs manquantes par colonne :")
print(df.isnull().sum())

df = df.dropna(subset=['temperature'])

print(f"Nombre de doublons avant suppression : {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Nombre de doublons après suppression : {df.duplicated().sum()}")

df['date_recolte'] = pd.to_datetime(df['date_recolte'], errors='coerce')

df = df.dropna(subset=['date_recolte'])

print(f"Données nettoyées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
print(df.head())

#charger les données dans ma base sqllite

import sqlite3

conn = sqlite3.connect('meteo_data.db')

df.to_sql('meteo', conn, if_exists='append', index=False)

print(" Données chargées dans la nvl base SQLite 'meteo_data.db' table 'meteo'.")
