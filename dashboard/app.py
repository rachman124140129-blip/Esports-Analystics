import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.db_connector import get_db_engine

st.set_page_config(page_title="E-Sports Analytics Dashboard", layout="wide")
st.title("📊 E-Sports Data Analytics Pipeline Dashboard")
st.subheader("Turnamen: M7 World Championship Simulation")
st.markdown("---")

def load_dashboard_data():
    engine = get_db_engine()
    query = """
    SELECT 
        p.username AS "Player", 
        pp.entity_id AS "Hero ID", 
        pp.kills AS "Kills", 
        pp.deaths AS "Deaths", 
        pp.assists AS "Assists", 
        pp.kda_ratio AS "KDA Ratio"
    FROM player_performance pp
    JOIN players p ON pp.player_id = p.player_id
    ORDER BY pp.kda_ratio DESC;
    """
    try:
        return pd.read_sql(query, con=engine)
    except:
        return pd.DataFrame()

df_leaderboard = load_dashboard_data()

if df_leaderboard.empty:
    st.warning("Data belum tersedia.")
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("### 🏆 Papan Peringkat Performa Pemain (KDA)")
        st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)
    with col2:
        st.write("### 📈 Grafik Rasio KDA per Pemain")
        fig = px.bar(
            df_leaderboard, x="Player", y="KDA Ratio", color="KDA Ratio",
            text="KDA Ratio", title="Perbandingan KDA Ratio Kontestan",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.write("### 📌 Ringkasan Performa Turnamen")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Partisipan", f"{df_leaderboard['Player'].nunique()} Pemain")
    kpi2.metric("KDA Tertinggi", f"{df_leaderboard['KDA Ratio'].max()}")
    kpi3.metric("Rata-rata Kills per Match", f"{round(df_leaderboard['Kills'].mean(), 1)}")