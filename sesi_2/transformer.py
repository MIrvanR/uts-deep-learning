"""
transformer.py
Modul Transformasi & Validasi Data Komoditas Pangan:
- Membersihkan string mentah (regex parsing simbol mata uang dan satuan ukuran)
- Validasi skema, null checks, dan validasi tipe data numerik
- Mengubah payload JSON menjadi Pandas DataFrame terstruktur siap simpan

SESI II: Global Infrastructure to Address Local Challenge with HPC
Judul: Modular Pipeline untuk Agregasi Real-Time Harga Komoditas Pangan Lokal
"""

import re
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class CommodityDataTransformer:
    def __init__(self):
        self.required_keys = ["commodity", "price_raw", "market", "region", "date"]

    def parse_price_and_unit(self, price_str):
        """
        Mengekstrak nilai numerik harga dan satuan dari format teks seperti:
        'Rp 14.500/kg' -> (14500.0, 'kg')
        'Rp 18.000/liter' -> (18000.0, 'liter')
        """
        if not isinstance(price_str, str):
            return None, None
            
        # Ekstrak angka (hilangkan 'Rp', titik, dan spasi)
        clean_num_match = re.search(r"(\d[\d\.]*)", price_str)
        if not clean_num_match:
            return None, None
            
        num_str = clean_num_match.group(1).replace(".", "")
        try:
            price_val = float(num_str)
        except ValueError:
            return None, None
            
        # Ekstrak satuan setelah tanda garis miring (/)
        unit_match = re.search(r"\/([a-zA-Z]+)", price_str)
        unit = unit_match.group(1).lower() if unit_match else "kg"
        
        return price_val, unit

    def transform(self, raw_payload):
        """
        Mengubah raw JSON payload menjadi DataFrame bersih terstandarisasi.
        """
        logging.info("Memulai proses transformasi dan validasi skema data...")
        if not raw_payload or "data" not in raw_payload:
            raise ValueError("Payload tidak valid atau tidak memiliki kunci 'data'.")
            
        raw_items = raw_payload["data"]
        cleaned_records = []
        
        for idx, item in enumerate(raw_items):
            # 1. Validasi keberadaan kunci wajib
            if not all(k in item for k in self.required_keys):
                logging.warning(f"Baris {idx} dilewati karena kunci skema tidak lengkap: {item}")
                continue
                
            price_val, unit = self.parse_price_and_unit(item["price_raw"])
            
            # 2. Validasi nilai harga
            if price_val is None or price_val <= 0:
                logging.warning(f"Baris {idx} dilewati karena harga tidak valid: {item['price_raw']}")
                continue
                
            cleaned_records.append({
                "commodity_name": item["commodity"].strip(),
                "price": price_val,
                "unit": unit,
                "market_name": item["market"].strip(),
                "region": item["region"].strip(),
                "record_date": item["date"].strip(),
                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
        df = pd.DataFrame(cleaned_records)
        
        # 3. Penegakan tipe data (Data Type Enforcement)
        df["price"] = df["price"].astype(float)
        df["record_date"] = pd.to_datetime(df["record_date"]).dt.strftime("%Y-%m-%d")
        
        logging.info(f"Transformasi selesai. {len(df)} rekaman valid terstruktur siap disimpan.")
        return df

if __name__ == "__main__":
    from fetcher import CommodityDataFetcher
    fetcher = CommodityDataFetcher()
    payload = fetcher.fetch_live_prices()
    transformer = CommodityDataTransformer()
    df = transformer.transform(payload)
    print("\nTabel Hasil Transformasi:")
    print(df.head())
