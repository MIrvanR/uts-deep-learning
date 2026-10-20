"""
main.py
Orchestrator Pipeline Komoditas Pangan Lokal:
1. Memanggil Fetcher untuk penarikan data
2. Memanggil Transformer untuk pembersihan & validasi tipe data
3. Menyimpan data terstruktur ke SQLite DB (food_prices.db) dengan timestamp otomatis
4. Menampilkan ringkasan fluktuasi harga komoditas pangan

SESI II: Global Infrastructure to Address Local Challenge with HPC
Judul: Modular Pipeline untuk Agregasi Real-Time Harga Komoditas Pangan Lokal
"""

import os
import sys
import sqlite3
import logging
import pandas as pd

from fetcher import CommodityDataFetcher
from transformer import CommodityDataTransformer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class CommodityStorageManager:
    def __init__(self, db_path="food_prices.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Inisialisasi tabel database SQLite jika belum ada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commodity_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    commodity_name TEXT NOT NULL,
                    price REAL NOT NULL,
                    unit TEXT NOT NULL,
                    market_name TEXT NOT NULL,
                    region TEXT NOT NULL,
                    record_date TEXT NOT NULL,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        logging.info(f"Database SQLite siap digunakan: {self.db_path}")

    def save_to_sqlite(self, df):
        """Menyimpan Pandas DataFrame ke tabel SQLite."""
        if df.empty:
            logging.warning("DataFrame kosong, tidak ada data yang disimpan.")
            return 0
            
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql("commodity_prices", conn, if_exists="append", index=False)
            logging.info(f"{len(df)} baris berhasil disisipkan ke tabel 'commodity_prices'.")
            
        return len(df)

    def print_daily_summary(self):
        """Mengambil ringkasan statistik harga rata-rata per komoditas pangan."""
        query = """
            SELECT 
                commodity_name,
                unit,
                COUNT(*) as total_titik_pasar,
                MIN(price) as harga_terendah,
                AVG(price) as harga_rata_rata,
                MAX(price) as harga_tertinggi
            FROM commodity_prices
            GROUP BY commodity_name, unit
            ORDER BY harga_rata_rata DESC
        """
        with sqlite3.connect(self.db_path) as conn:
            summary_df = pd.read_sql_query(query, conn)
            
        print("\n" + "="*80)
        print("  RINGKASAN FLUKTUASI HARGA KOMODITAS PANGAN LOKAL (DATABASE SQLITE)")
        print("="*80)
        summary_df["harga_rata_rata"] = summary_df["harga_rata_rata"].map(lambda x: f"Rp {x:,.0f}")
        summary_df["harga_terendah"] = summary_df["harga_terendah"].map(lambda x: f"Rp {x:,.0f}")
        summary_df["harga_tertinggi"] = summary_df["harga_tertinggi"].map(lambda x: f"Rp {x:,.0f}")
        print(summary_df.to_string(index=False))
        print("="*80 + "\n")

def run_pipeline():
    logging.info("Memulai eksekusi Modular Food Commodity Pipeline...")
    try:
        # Langkah 1: Pengambilan Data (Fetcher)
        fetcher = CommodityDataFetcher()
        raw_payload = fetcher.fetch_live_prices()
        
        # Langkah 2: Pembersihan & Validasi (Transformer)
        transformer = CommodityDataTransformer()
        clean_df = transformer.transform(raw_payload)
        
        # Langkah 3: Penyimpanan ke SQLite & Pelaporan (Storage)
        storage = CommodityStorageManager("food_prices.db")
        rows_saved = storage.save_to_sqlite(clean_df)
        
        # Langkah 4: Tampilkan Agregasi Ringkasan
        storage.print_daily_summary()
        logging.info("[SUKSES] Seluruh tahapan pipeline komoditas selesai tanpa kendala.")
        
    except Exception as e:
        logging.error(f"[ERROR] Terjadi kegagalan kritis pada pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
