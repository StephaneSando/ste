import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base SQLite
DB_PATH = "meteo_data.db"
conn = sqlite3.connect(DB_PATH)

#@st.cache_data
def load_data():
    query = "SELECT * FROM meteo"
    df = pd.read_sql_query(query, conn)
    df['time'] = pd.to_datetime(df['time'])
    return df

df = load_data()

# Titre
st.title("Visualisation des données météo en France (UTC) ")

# Sélection de la ville
villes = sorted(df['ville'].unique())
ville_select = st.selectbox("Choisissez une ville :", villes)

# Filtrage des données
df_ville = df[df['ville'] == ville_select]


# Les KPIs
st.subheader(f"Indicateur météo pour {ville_select}")

col1, col2, col3, col4 = st.columns(4)

# Température
col1.metric(" Moy. Temperature (°C)", f"{df_ville['temperature'].mean():.1f}")
col2.metric(" Max / Min Temp (°C)", 
            f"{df_ville['temperature'].max():.1f} / {df_ville['temperature'].min():.1f}")

# Vent
col3.metric(" Vent moyen (km/h)", f"{df_ville['windspeed'].mean():.1f}")

# Jour ou Nuit
is_day_pct = df_ville['is_day'].mean() * 100  
col4.metric("% Période jour", f"{is_day_pct:.0f}%")

##### Tableau
st.subheader(f"Données météo détaillées pour {ville_select}")
st.dataframe(df_ville.sort_values("time", ascending=False), use_container_width=True)

#### Graph
st.subheader("Temperature au fil du temps")
st.line_chart(df_ville.set_index("time")["temperature"])

with st.expander(" Voir les vents et météo détaillée"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Vitesse du vent (km/h)")
        st.line_chart(df_ville.set_index("time")["windspeed"])

    with col2:
        st.markdown(" Codes météo (weathercode)")
        st.bar_chart(df_ville["weathercode"].value_counts())

# date de la mise à jour
st.caption(f"Derniere mise à jour : {df['date_recolte'].max()}")
