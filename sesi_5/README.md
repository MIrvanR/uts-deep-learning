# SESI V: Dasbor Analisis Performa Penjualan Ritel Regional (Prinsip Shneiderman)

Aplikasi dasbor interaktif berbasis web yang dibangun menggunakan **Streamlit** dan **Plotly**, menerapkan prinsip dasar *Human-Computer Interaction* (HCI) dan visualisasi data: **Shneiderman's Visual Information Seeking Mantra**:
> *"Overview first, zoom and filter, then details-on-demand."*

## 🎨 Arsitektur Antarmuka & Prinsip Visualisasi
1. **Zoom and Filter (Sidebar)**:
   - Pengguna dapat menyaring data berdasarkan satu atau beberapa **Wilayah Cabang Regional** (*DKI Jakarta, Jawa Barat, Jawa Tengah, Jawa Timur, Bali*).
   - Filter multiselect berdasarkan **Kategori Produk**.
   - Pemilihan rentang tanggal dinamis (*Date Range Picker*).
2. **Overview First (Makro & KPI)**:
   - Kartu metrik KPI: *Total Pendapatan*, *Unit Terjual*, *Total Transaksi*, dan *Average Order Value (AOV)*.
   - Grafik garis tren pendapatan bulanan interaktif (*Clean Plotly Line Chart*) yang dirancang bebas elemen dekoratif berlebihan (*no chartjunk*).
   - Grafik pangsa pasar regional dan kontribusi kategori produk.
3. **Details-on-Demand (Mikro & Rincian)**:
   - Tabel interaktif data transaksi mentah di bagian bawah.
   - Kolom pencarian teks instan (berdasarkan ID Transaksi atau Metode Pembayaran).
   - Tombol unduhan data terfilter ke format CSV.

## 🚀 Cara Menjalankan Dasbor
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
Aplikasi akan otomatis terbuka pada browser di alamat `http://localhost:8501`.
