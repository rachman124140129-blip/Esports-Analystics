import pandas as pd
from sqlalchemy import create_engine

print("Memulai proses ETL...")

file_path = 'data/raw/raw_mlbb_stats.csv' 

try:
    df = pd.read_csv(file_path, sep=';')
    print(f"✅ Berhasil membaca file CSV: {len(df)} baris data ditemukan.")
except Exception as e:
    print(f"❌ Gagal membaca CSV. Error: {e}")
    exit()

df.columns = df.columns.str.strip().str.lower()

print("\n🧐 Kolom yang terdeteksi setelah dibersihkan:", df.columns.tolist())

if 'match_date' in df.columns:
    df['match_date'] = pd.to_datetime(df['match_date'])
    print("✅ Berhasil memformat kolom tanggal!")
else:
    print("\n❌ GAGAL: Kolom 'match_date' tidak ada di file Anda.")
    print("💡 Saran: Silakan buka ulang file Excel Anda dan pastikan ada kolom bernama 'match_date'.")
    exit()

db_url = 'postgresql://postgres:0p9o8i7u6Y@localhost:5432/analisis_esport'

try:
    engine = create_engine(db_url)
    df.to_sql('mlbb_match_stats', engine, if_exists='replace', index=False)
    print("\n🚀 PROSES SELESAI! Data berhasil disuntikkan ke PostgreSQL.")
except Exception as e:
    print(f"\n❌ Gagal memuat data ke PostgreSQL. Error: {e}")