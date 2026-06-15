import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Memuat kredensial dari file .env
load_dotenv()

def get_db_engine():
    """
    Membuat dan mengembalikan engine koneksi SQLAlchemy ke PostgreSQL.
    """
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    connection_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(connection_url, echo=False) 
        return engine
    except Exception as e:
        print(f"Gagal membuat konfigurasi database: {e}")
        return None

if __name__ == "__main__":
    print("Mencoba menyambungkan ke PostgreSQL...")
    engine = get_db_engine()
    
    if engine:
        try:
            with engine.connect() as connection:
                print("Koneksi sukses! Python berhasil masuk ke database 'esports_analytics'.")
        except SQLAlchemyError as e:
            print(f"Koneksi gagal. Pastikan password di .env sudah benar dan pgAdmin sedang menyala.\nError: {e}")