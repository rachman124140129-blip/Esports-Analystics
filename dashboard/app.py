import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu # Import modul baru

# --- KONFIGURASI HALAMAN ---
# initial_sidebar_state="collapsed" akan menyembunyikan sidebar bawaan
st.set_page_config(
    page_title="MPL Analytics Pro", 
    page_icon="🔴", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- KONFIGURASI DATABASE ---
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.db_connector import get_db_engine

@st.cache_data
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

# --- HEADER ALA MPL ID (NAVIGASI ATAS) ---
# Menggunakan CSS untuk menyembunyikan header bawaan Streamlit agar lebih bersih
st.markdown("""
    <style>
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

# Membuat baris untuk Logo dan Menu
col_logo, col_menu = st.columns([1.5, 4.5])

with col_logo:
    # Menggunakan teks bergaya sebagai pengganti logo, kamu bisa ganti dengan st.image() jika ada file logo
    st.markdown("<h2 style='color: white; margin-top: 5px; font-style: italic;'>RH.<br><span style='color: #e50000;'>The Intruder</span></h2>", unsafe_allow_html=True)

with col_menu:
    menu_selection = option_menu(
        menu_title=None,  # Sembunyikan judul menu
        options=["HOME (PROFIL)", "STATISTIK", "ANALISIS HERO", "BERITA (ABOUT)"],
        icons=["house", "bar-chart-fill", "controller", "info-circle"], # Ikon Bootstrap
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#4a0000", "border-radius": "0px"},
            "icon": {"color": "white", "font-size": "14px"}, 
            "nav-link": {"font-size": "13px", "text-align": "center", "margin":"0px", "--hover-color": "#800000"},
            "nav-link-selected": {"background-color": "#e50000"},
        }
    )

# --- HEADER ALA MPL ID (NAVIGASI ATAS) ---
st.markdown("""
    <style>
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        /* Mencegah layar bergetar dengan mengunci scrollbar vertikal */
        html, body {overflow-y: scroll !important;}
    </style>
""", unsafe_allow_html=True)

if df_leaderboard.empty:
    st.error("Data gagal dimuat. Periksa koneksi database.")
else:
    # --- HALAMAN 1: PROFIL (HOME) ---
    if menu_selection == "HOME (PROFIL)":
        col_foto, col_teks = st.columns([1, 2.5], gap="large")
        with col_foto:
            st.image("dashboard/jajaja.jpeg", use_container_width=True)
            
        with col_teks:
            st.subheader("Rachman Hady | Teknik Informatika ITERA 2024")
            
            st.markdown(
                "Mahasiswa Teknik Informatika Institut Teknologi Sumatera (ITERA) semester 4.<br>"
                "Memiliki minat pada AI Engineering dan Machine Learning, saya juga menyukai scene kompetitif dari game yang saya mainkan. "
                "Hal inilah yang menginspirasi saya membuat analisis e-sports ini.", 
                unsafe_allow_html=True
            )
            
            st.write(
                "Platform ini mensimulasikan *pipeline* data setingkat industri e-sports "
                "dengan tumpukan teknologi: Python, PostgreSQL, dan Streamlit."
            )
    # --- HALAMAN 2: STATISTIK ---
    elif menu_selection == "STATISTIK":
        st.markdown("### 🏆 Papan Peringkat KDA: Team Liquid PH")
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.metric(label="Total Partisipan", value=f"{df_leaderboard['Player'].nunique()} Player")
        with col_kpi2:
            st.metric(label="KDA Tertinggi", value=f"{df_leaderboard['KDA Ratio'].max()} (MVP)")
        with col_kpi3:
            st.metric(label="Rata-rata Kills", value=f"{round(df_leaderboard['Kills'].mean(), 1)} / Match")
        
        st.markdown("<br>", unsafe_allow_html=True)

        col_tabel, col_grafik = st.columns([1, 1.5])
        with col_tabel:
            st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)
            
        with col_grafik:
            fig = px.bar(
                df_leaderboard, x="Player", y="KDA Ratio", color="KDA Ratio", text="KDA Ratio",
                color_continuous_scale=px.colors.sequential.Reds # Warna grafik menjadi merah
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0), font=dict(color="#ffffff")
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

    # --- HALAMAN 3 & 4 (Placeholder) ---
    elif menu_selection == "ANALISIS HERO":
        st.subheader("Data Hero")
        st.info("Statistik spesifik hero akan ditarik dari tabel `game_entities`.")
        
    elif menu_selection == "BERITA (ABOUT)":
        st.subheader("Patch Notes & Update Pipeline")
        st.write("Versi 1.0: Integrasi PostgreSQL dan Dashboard Streamlit selesai.")