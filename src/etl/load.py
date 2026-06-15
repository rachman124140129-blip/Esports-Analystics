import os
import json
import glob
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.db_connector import get_db_engine

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

def get_target_file(directory, prefix, ext="json"):
    """Mencari file target. Jika JSON, ambil yang terbaru (timestamp)."""
    if ext == "json":
        files = glob.glob(os.path.join(directory, f"{prefix}_*.{ext}"))
        return max(files, key=os.path.getctime) if files else None
    else:
        file_path = os.path.join(directory, f"{prefix}.{ext}")
        return file_path if os.path.exists(file_path) else None

def load_data_to_db():
    print("Mulai proses Load Data ke PostgreSQL...")
    engine = get_db_engine()
    
    if not engine:
        print("❌ Koneksi database gagal. Proses Load dihentikan.")
        return

    tables_to_load = [
        {"table": "tournaments", "prefix": "tournaments", "dir": RAW_DIR, "ext": "json"},
        {"table": "teams", "prefix": "teams", "dir": RAW_DIR, "ext": "json"},
        {"table": "players", "prefix": "players", "dir": RAW_DIR, "ext": "json"},
        {"table": "matches", "prefix": "matches", "dir": RAW_DIR, "ext": "json"},
        {"table": "player_performance", "prefix": "cleaned_performances", "dir": PROCESSED_DIR, "ext": "csv"}
    ]

    for item in tables_to_load:
        file_path = get_target_file(item["dir"], item["prefix"], item["ext"])
        
        if not file_path:
            print(f"⚠️ File untuk '{item['table']}' tidak ditemukan. Lewati.")
            continue
        
        print(f"Membaca data untuk '{item['table']}'...")
        
        if item["ext"] == "json":
            with open(file_path, 'r') as f:
                data = json.load(f)
                df = pd.DataFrame(data)
        else:
            df = pd.read_csv(file_path)
        
        try:
            df.to_sql(item['table'], con=engine, if_exists='append', index=False)
            print(f" Berhasil memuat {len(df)} baris ke tabel '{item['table']}'\n")
        except Exception as e:
            print(f" Gagal memuat tabel '{item['table']}'. Data kemungkinan sudah ada (Duplicate Primary Key).\n")

    print("🎉 SELAMAT! Seluruh Pipeline ETL (Extract, Transform, Load) berhasil dieksekusi!")

if __name__ == "__main__":
    load_data_to_db()