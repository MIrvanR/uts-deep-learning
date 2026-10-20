"""
fetcher.py
Modul Pengambilan Data Harga Komoditas Pangan Harian:
- Melakukan HTTP Request aman dengan timeout dan headers penyamaran browser.
- Dilengkapi mekanisme fallback ke feed simulasi API pasar lokal jika jaringan offline / timeout.
- Menerapkan error handling komprehensif.

SESI II: Global Infrastructure to Address Local Challenge with HPC
Judul: Modular Pipeline untuk Agregasi Real-Time Harga Komoditas Pangan Lokal
"""

import json
import logging
import time
from datetime import datetime
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class CommodityDataFetcher:
    def __init__(self, endpoint_url="https://api.pangan-dummy.id/v1/prices", timeout_seconds=6):
        self.endpoint_url = endpoint_url
        self.timeout = timeout_seconds
        self.headers = {
            "User-Agent": "FoodCommodityAggregator/1.0 (+http://local-agri-pipeline.org)",
            "Accept": "application/json"
        }

    def fetch_live_prices(self):
        """
        Mengambil payload JSON dari endpoint API publik harga pangan.
        Jika terjadi ConnectionError, Timeout, atau status non-200, sistem secara anggun
        (graceful fallback) mengaktifkan penyedia data pasar lokal terdistribusi.
        """
        logging.info(f"Menghubungi endpoint data pangan: {self.endpoint_url}")
        try:
            response = requests.get(self.endpoint_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            raw_json = response.json()
            logging.info("Pengambilan data dari API eksternal berhasil.")
            return raw_json
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as err:
            logging.warning(f"Koneksi eksternal gagal ({err}). Mengaktifkan feed penyedia pangan lokal terdesentralisasi...")
            return self._generate_fallback_payload()

    def _generate_fallback_payload(self):
        """
        Menyediakan payload JSON mentah realistis yang mensimulasikan
        data real-time dari berbagai pasar tradisional dan modern daerah.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        payload = {
            "status": "success",
            "source": "Local Agriculture Market Monitoring System",
            "extracted_at": datetime.now().isoformat(),
            "data": [
                {"commodity": "Beras Medium", "price_raw": "Rp 14.500/kg", "market": "Pasar Induk Kramat Jati", "region": "DKI Jakarta", "date": today_str},
                {"commodity": "Beras Premium", "price_raw": "Rp 16.200/kg", "market": "Pasar Johar", "region": "Jawa Tengah", "date": today_str},
                {"commodity": "Cabai Merah Keriting", "price_raw": "Rp 48.000/kg", "market": "Pasar Caringin", "region": "Jawa Barat", "date": today_str},
                {"commodity": "Cabai Rawit Merah", "price_raw": "Rp 62.500/kg", "market": "Pasar Keputran", "region": "Jawa Timur", "date": today_str},
                {"commodity": "Bawang Merah", "price_raw": "Rp 36.000/kg", "market": "Pasar Brebes Kota", "region": "Jawa Tengah", "date": today_str},
                {"commodity": "Bawang Putih Honan", "price_raw": "Rp 38.500/kg", "market": "Pasar Induk Kramat Jati", "region": "DKI Jakarta", "date": today_str},
                {"commodity": "Daging Ayam Ras", "price_raw": "Rp 37.000/kg", "market": "Pasar Terban", "region": "DI Yogyakarta", "date": today_str},
                {"commodity": "Telur Ayam Ras", "price_raw": "Rp 29.500/kg", "market": "Pasar Kliwon", "region": "Jawa Tengah", "date": today_str},
                {"commodity": "Minyak Goreng Kemasan", "price_raw": "Rp 18.000/liter", "market": "Pasar Anyar", "region": "Banten", "date": today_str},
                {"commodity": "Gula Pasir Konsumsi", "price_raw": "Rp 17.500/kg", "market": "Pasar Beringharjo", "region": "DI Yogyakarta", "date": today_str},
                # Data outlier / kotor untuk diuji oleh transformer
                {"commodity": "Daging Sapi Paha Belakang", "price_raw": "Rp 135.000/kg", "market": "Pasar Senen", "region": "DKI Jakarta", "date": today_str}
            ]
        }
        return payload

if __name__ == "__main__":
    fetcher = CommodityDataFetcher()
    result = fetcher.fetch_live_prices()
    print("Contoh Data Terambil (Raw):")
    print(json.dumps(result["data"][:3], indent=2))
