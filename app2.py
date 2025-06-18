import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base SQLite
DB_PATH = "meteo_data.db"
conn = sqlite3.connect(DB_PATH)

@st.cache_data
def load_data():
    query = "SELECT * FROM meteo"
    df = pd.read_sql_query(query, conn)
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time', 'temperature', 'ville'])
    return df

df = load_data()

st.title("🌦️ Visualisation des données météo en France")

# Liste des villes disponibles
villes = sorted(df['ville'].dropna().unique())
ville_selection = st.selectbox("Choisissez une ville :", villes)

# Filtrage des données
df_ville = df[df['ville'] == ville_selection]

if df_ville.empty:
    st.warning(f"Aucune donnée disponible pour {ville_selection}.")
else:
    st.subheader(f"📊 Indicateurs météo pour {ville_selection}")

    col1, col2, col3, col4 = st.columns(4)

    try:
        col1.metric("🌡️ Moy. Température (°C)", f"{df_ville['temperature'].mean():.1f}")
        col2.metric("🔺 Max / Min Temp (°C)", 
                    f"{df_ville['temperature'].max():.1f} / {df_ville['temperature'].min():.1f}")
        col3.metric("💨 Vent moyen (km/h)", f"{df_ville['windspeed'].mean():.1f}")
        is_day_pct = df_ville['is_day'].mean() * 100
        col4.metric("☀️ % Période jour", f"{is_day_pct:.0f}%")
    except Exception as e:
        st.error(f"Erreur dans les indicateurs : {e}")

    # Tableau de données
    st.subheader(f"📋 Données météo détaillées pour {ville_selection}")
    st.dataframe(df_ville.sort_values("time", ascending=False), use_container_width=True)

    # Graphique température
    if "temperature" in df_ville.columns and not df_ville["temperature"].isnull().all():
        st.subheader("📈 Température au fil du temps")
        st.line_chart(df_ville.set_index("time")["temperature"])
    else:
        st.info("Pas de données de température valides.")

    # Autres graphes
    with st.expander("🔍 Voir les vents et météo détaillée"):
        col1, col2 = st.columns(2)

        with col1:
            if "windspeed" in df_ville.columns:
                st.markdown("💨 Vitesse du vent (km/h)")
                st.line_chart(df_ville.set_index("time")["windspeed"])
            else:
                st.info("Données de vent indisponibles.")

        with col2:
            if "weathercode" in df_ville.columns:
                st.markdown("🌦️ Codes météo (weathercode)")
                st.bar_chart(df_ville["weathercode"].value_counts())
            else:
                st.info("Données météo indisponibles.")

    # Date de mise à jour
    try:
        st.caption(f"📅 Dernière mise à jour : {df['date_recolte'].max()}")
    except:
        st.caption("Date de mise à jour non disponible.")
