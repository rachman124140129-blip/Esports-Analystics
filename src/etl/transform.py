import os
import json
import glob
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

def get_latest_file(prefix):
    """Mencari file JSON terbaru berdasarkan awalan nama file."""
    files = glob.glob(os.path.join(RAW_DIR, f"{prefix}_*.json"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_json_to_df(filepath):
    """Membaca file JSON ke dalam Pandas DataFrame."""
    if not filepath:
        return pd.DataFrame()
    with open(filepath, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def transform_performance_data():
    print("Mulai proses Transformasi Data...")
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    perf_file = get_latest_file("player_performances")
    df_perf = load_json_to_df(perf_file)

    if df_perf.empty:
        print("❌ Data performa tidak ditemukan di data/raw/")
        return

    print("✅ Raw Data berhasil dimuat. Melakukan kalkulasi metrik...")

    df_perf['kda_ratio'] = (df_perf['kills'] + df_perf['assists']) / df_perf['deaths'].replace(0, 1)
    
    df_perf['kda_ratio'] = df_perf['kda_ratio'].round(2)

    output_path = os.path.join(PROCESSED_DIR, "cleaned_performances.csv")
    df_perf.to_csv(output_path, index=False)
    
    print(f"Transformasi selesai! Data tersimpan di: {output_path}")
    print("\n--- Preview Data KDA Pemain ---")
    print(df_perf[['player_id', 'champion_hero_played', 'kills', 'deaths', 'assists', 'kda_ratio']].head())

if __name__ == "__main__":
    transform_performance_data()