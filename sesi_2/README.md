# SESI II: Modular Pipeline untuk Agregasi Real-Time Harga Komoditas Pangan Lokal

Arsitektur perangkat lunak berbasis pipeline modular untuk mengambil, membersihkan, memvalidasi, dan menyimpan fluktuasi harga komoditas pangan harian pasar lokal ke dalam basis data SQLite secara otomatis.

## 🧱 Arsitektur Sistem Modular
- **`fetcher.py`**: Modul penarikan data harga komoditas via HTTP Request dengan mekanisme *timeout*, *headers*, dan *fallback logic* ke feed pasar lokal terdesentralisasi jika server eksternal offline.
- **`transformer.py`**: Modul sanitasi teks, parsing harga dan satuan (regex), penegakan tipe data (*type enforcement*), dan validasi skema berbasis Pandas.
- **`main.py`**: Skrip *orchestrator* yang menjalankan pipeline secara terurut, menyimpan ke database SQLite (`food_prices.db`) dengan timestamp otomatis, dan menyajikan ringkasan statistik harga pasar.

## 🚀 Cara Menjalankan
```bash
pip install -r requirements.txt
python main.py
```
