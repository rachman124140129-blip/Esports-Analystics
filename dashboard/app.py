import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import sys
import os
from dotenv import load_dotenv

# --- KONFIGURASI HALAMAN ---
# Konfigurasi halaman WAJIB berada di paling atas sebelum logika layout lainnya
st.set_page_config(
    page_title="Rachman Hady - Portofolio", 
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

# --- FUNGSI BARU: TARIK DATA HERO ---
@st.cache_data
def load_hero_data():
    engine = get_db_engine()
    query = """
    SELECT 
        ge.name AS "Hero",
        COUNT(pp.perf_id) AS "Total Pick",
        SUM(pp.kills) AS "Total Kills",
        SUM(pp.deaths) AS "Total Deaths",
        SUM(pp.assists) AS "Total Assists",
        ROUND(AVG(pp.kda_ratio), 2) AS "Avg KDA Ratio"
    FROM player_performance pp
    JOIN game_entities ge ON pp.entity_id = ge.entity_id
    GROUP BY ge.name
    ORDER BY "Avg KDA Ratio" DESC;
    """
    try:
        return pd.read_sql(query, con=engine)
    except:
        return pd.DataFrame()

df_hero = load_hero_data()

# ==========================================
# 1. INISIALISASI MEMORI (SESSION STATE)
# ==========================================
# Cek apakah pengguna sudah menekan tombol masuk
if 'sudah_masuk' not in st.session_state:
    st.session_state['sudah_masuk'] = False

# Fungsi untuk mengubah status saat tombol diklik
def masuk_portofolio():
    st.session_state['sudah_masuk'] = True

# ==========================================
# 2. HALAMAN COVER (LANDING PAGE)
# ==========================================
if not st.session_state['sudah_masuk']:
    
    # CSS Khusus untuk Cover
    st.markdown("""
    <style>
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    .cover-subtitle { font-size: 22px; letter-spacing: 3px; color: #888; margin-bottom: -15px; }
    .cover-title { font-size: 65px; font-weight: 900; margin-bottom: -15px; line-height: 1.1; }
    .cover-role { font-size: 22px; font-weight: 300; color: #555; margin-bottom: 20px; }
    /* Desain Tombol Ala MPL */
    .stButton>button { border-radius: 5px; border: 2px solid #e50000; color: white; background-color: transparent; height: 50px; font-weight: bold; letter-spacing: 1px;}
    .stButton>button:hover { background-color: #e50000; color: white; border-color: #e50000;}
    </style>
    """, unsafe_allow_html=True)

    col_cover_text, col_cover_img = st.columns([1.5, 1], gap="xxsmall")
    
    with col_cover_text:
        st.markdown('<p class="cover-subtitle">HAY! THERE</p>', unsafe_allow_html=True)
        st.markdown('<p class="cover-title">I AM RACHMAN</p>', unsafe_allow_html=True)
        st.markdown('<p class="cover-role">A STUDENT FROM ITERA |</p>', unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
    <p style='color: #94a3b8; font-size: 20px; margin-top: 15px; margin-bottom: 30px; line-height: 1.6; font-weight: 400;'>
    Selamat datang di portofolio data interaktif saya.<br>
    Proyek ini merupakan simulasi end-to-end <b>E-Sports Analytics Pipeline</b>.<br>
    Mengubah barisan data mentah menjadi wawasan strategis menggunakan kombinasi Python, PostgreSQL, dan Streamlit.
    </p>
    """, unsafe_allow_html=True)
        
    with col_cover_img:
        # Menggunakan logo esports untuk cover
        st.image("dashboard/dataAnalisLogo.png", width=600)
        st.markdown("<style>div.stButton > button { margin-top: -20px; }</style>", unsafe_allow_html=True)
        
        # Tombol Sakti untuk Melanjutkan
        st.button("Masuk", on_click=masuk_portofolio, use_container_width=True)
        

# ==========================================
# 3. HALAMAN UTAMA (SETELAH TOMBOL DIKLIK)
# ==========================================
else:
    # --- CSS HEADER ALA MPL ID ---
    st.markdown("""
        <style>
            header {visibility: hidden;}
            .block-container {padding-top: 1rem; padding-bottom: 0rem;}
            /* Mencegah layar bergetar dengan mengunci scrollbar vertikal */
            html, body {overflow-y: scroll !important;}
        </style>
    """, unsafe_allow_html=True)

    # Membuat baris untuk Logo dan Menu
    col_logo, col_menu = st.columns([1.5, 4.5])

    with col_logo:
        st.markdown("<h2 style='color: white; margin-top: 5px; font-style: italic;'>RH.<br><span style='color: #e50000;'>The Intruder</span></h2>", unsafe_allow_html=True)

    with col_menu:
        menu_selection = option_menu(
            menu_title=None,  
            options=["HOME (PROFIL)", "STATISTIK", "ANALISIS HERO", "BERITA (ABOUT)"],
            icons=["house", "bar-chart-fill", "controller", "info-circle"], 
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#4a0000", "border-radius": "0px"},
                "icon": {"color": "white", "font-size": "14px"}, 
                "nav-link": {"font-size": "13px", "text-align": "center", "margin":"0px", "--hover-color": "#800000"},
                "nav-link-selected": {"background-color": "#e50000"},
            }
        )

    if df_leaderboard.empty:
        st.error("Data gagal dimuat. Periksa koneksi database.")
    else:
        # --- HALAMAN 1: PROFIL (HOME) ---
        if menu_selection == "HOME (PROFIL)":
            col_foto, col_teks = st.columns([1, 2.5], gap="large")
            with col_foto:
                # Menggunakan foto dirimu untuk di dalam profil
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
            st.markdown("### 🏆 Papan Peringkat KDA: Team Liquid PH & ONIC")
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
                    color_continuous_scale=px.colors.sequential.Reds 
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=0), font=dict(color="#ffffff")
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

        # --- HALAMAN 3: ANALISIS HERO ---
        elif menu_selection == "ANALISIS HERO":
            st.markdown("### ⚔️ Statistik Performa Hero (Champion)")
            
            if df_hero.empty:
                st.warning("Data hero belum tersedia di database.")
            else:
                col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
                with col_kpi1:
                    st.metric(label="Total Hero Dimainkan", value=f"{df_hero['Hero'].nunique()} Hero")
                with col_kpi2:
                    hero_mvp = df_hero.iloc[0]['Hero']
                    st.metric(label="Hero dengan KDA Tertinggi", value=f"{hero_mvp}")
                with col_kpi3:
                    total_kills = df_hero['Total Kills'].sum()
                    st.metric(label="Total Kills Keseluruhan", value=f"{total_kills} Kills")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_tabel, col_grafik = st.columns([1, 1.5], gap="large")
                
                with col_tabel:
                    st.markdown("**Detail Rekapitulasi Hero**")
                    st.dataframe(df_hero, use_container_width=True, hide_index=True)
                    
                with col_grafik:
                    st.markdown("**Grafik Rata-rata KDA per Hero**")
                    fig = px.bar(
                        df_hero, 
                        x="Hero", 
                        y="Avg KDA Ratio", 
                        color="Avg KDA Ratio", 
                        text="Avg KDA Ratio",
                        color_continuous_scale=px.colors.sequential.Reds 
                    )
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)", 
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0, r=0, t=10, b=0), 
                        font=dict(color="#ffffff")
                    )
                    fig.update_traces(textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
            
        # --- HALAMAN 4: BERITA (ABOUT) ---
        elif menu_selection == "BERITA (ABOUT)":
            st.markdown("### 🌐 System Architecture & Patch Notes")
            st.markdown(
                "Selamat datang di pusat komando **Esports Analytics Pipeline**. Platform ini dibangun di atas "
                "arsitektur data modern untuk menyimulasikan pemrosesan metrik e-sports secara terintegrasi."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            tab_arsitektur, tab_tech, tab_patch = st.tabs(["🏗️ Arsitektur Data", "🛠️ Tech Stack", "📜 Patch Notes"])
            
            with tab_arsitektur:
                st.markdown("**Alur Pemrosesan Data (End-to-End Pipeline)**")
                col_etl, col_dw, col_viz = st.columns(3)
                
                with col_etl:
                    st.info("**1. Data Ingestion (ETL)**")
                    st.write(
                        "Skrip Python (`extract.py` & `transform.py`) otomatis mengekstrak data mentah, "
                        "membersihkannya dengan **Pandas**, dan mengkalkulasi metrik turunan (seperti KDA) "
                        "sebelum masuk ke database."
                    )
                    
                with col_dw:
                    st.warning("**2. Data Warehouse**")
                    st.write(
                        "Data bersih dimuat ke dalam **PostgreSQL** (`load.py`) mematuhi skema relasional 3NF. "
                        "Memastikan integritas entitas menggunakan sistem Foreign Key dan UUID."
                    )
                    
                with col_viz:
                    st.error("**3. Visualization**")
                    st.write(
                        "Data di-query langsung dari database dan disajikan menjadi dasbor interaktif "
                        "menggunakan **Streamlit** dan **Plotly**, memberikan insight performa secara langsung."
                    )

            with tab_tech:
                st.markdown("**Infrastruktur Teknologi Terkini**")
                st.markdown("""
                > **Bahasa Pemrograman:** Python 3.12+  
                > **Pemrosesan Data & Analitik:** Pandas, NumPy  
                > **Database & Konektor:** PostgreSQL, pgAdmin 4, SQLAlchemy, Psycopg2  
                > **Pengembangan Antarmuka Web:** Streamlit, Streamlit-Option-Menu  
                > **Visualisasi Grafis:** Plotly Express  
                > **Version Control & Repository:** Git, GitHub  
                """)
                
            with tab_patch:
                st.markdown("**Riwayat Pembaruan Sistem (Version Control)**")
                
                with st.expander("🔴 Versi 1.1.0 - The Analytics Update (Current)", expanded=True):
                    st.markdown("""
                    - **[FEATURE]** Integrasi halaman 'Analisis Hero' dengan data tabel `game_entities`.
                    - **[UI/UX]** Perombakan total tampilan menjadi navigasi horizontal ala MPL ID (Merah/Marun).
                    - **[FIX]** Penyelesaian isu *scrollbar jitter* (layar bergetar) menggunakan CSS lock.
                    - **[FEATURE]** Penambahan antarmuka 'Profil Data Engineer' di halaman utama.
                    - **[FEATURE]** Penambahan Splash Screen (Cover Page) terintegrasi.
                    """)
                    
                with st.expander("⚪ Versi 1.0.0 - Pipeline Genesis"):
                    st.markdown("""
                    - **[CORE]** Pembuatan skema database relasional di PostgreSQL.
                    - **[CORE]** Pembuatan skrip generator data simulasi (Mock Data Turnamen M7).
                    - **[CORE]** Skrip ekstraksi dan transformasi berhasil terhubung menggunakan SQLAlchemy.
                    """)