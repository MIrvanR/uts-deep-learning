# Studi Kasus Terpadu: UTS Deep Learning

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/Repository-UTS--Deep--Learning-181717.svg?logo=github)](https://github.com/MIrvanR/uts-deep-learning)

Repositori ini memuat implementasi lengkap dan komprehensif dari **6 Sesi Studi Kasus** yang mencakup berbagai domain terapan kecerdasan buatan (*Artificial Intelligence*), pembelajaran mesin (*Machine Learning*), analisis geospasial (*GIS*), arsitektur *software integration*, visualisasi data (*HCI*), hingga *Deep Learning* penginderaan jauh (*Remote Sensing*).

---

## 📂 Struktur Repositori

Struktur repositori disusun secara modular per folder sesi:

```text
uts-deep-learning/
├── sesi_1/   # E-Commerce Customer Lifetime Value & RFM Clustering
├── sesi_2/   # Modular Pipeline Agregasi Harga Komoditas Pangan Lokal (SQLite)
├── sesi_3/   # Analisis Aksesibilitas Spasial & Buffer Zone Faskes (GeoPandas)
├── sesi_4/   # Predictive Maintenance Klasifikasi Mesin IoT (Scikit-Learn)
├── sesi_5/   # Dasbor Penjualan Ritel Interaktif Prinsip Shneiderman (Streamlit)
├── sesi_6/   # Klasifikasi Tutupan Lahan Pertanian Menggunakan CNN (PyTorch)
├── .gitignore
└── README.md
```

---

## 📌 Ringkasan 6 Sesi Studi Kasus

| Sesi | Topik Kurikulum | Judul Studi Kasus | Teknologi & Pustaka Utama | Output Utama |
| :---: | :--- | :--- | :--- | :--- |
| **Sesi 1** | *Patterns of Data with Analysis and AI* | **E-Commerce CLV & Purchasing Behavior Clustering** | Scikit-Learn, Pandas, NumPy, Matplotlib | Kurva Elbow, Scatter Klaster, `segmented_customers.csv` |
| **Sesi 2** | *Global Infrastructure with HPC* | **Modular Pipeline Agregasi Harga Komoditas Pangan** | Requests, Pandas, SQLite3, Regex | Database terstruktur `food_prices.db` & summary table |
| **Sesi 3** | *Career & Competition in GIS* | **Aksesibilitas Spasial & Buffer Zone Faskes** | GeoPandas, Shapely, Folium, Matplotlib | Peta statis (PNG), Peta interaktif (HTML), Laporan CSV |
| **Sesi 4** | *Introduction to Machine Learning* | **Predictive Maintenance: Klasifikasi IoT Sensor** | Scikit-Learn (Random Forest, Gradient Boosting) | Evaluasi Precision-Recall-F1 & Analisis Overfitting |
| **Sesi 5** | *HCI & Data Visualization* | **Dasbor Penjualan Ritel (Prinsip Shneiderman)** | Streamlit, Plotly Express, Pandas | Web Dashboard Interaktif (*Overview, Zoom/Filter, Details*) |
| **Sesi 6** | *Remote Sensing and AI* | **Klasifikasi Tutupan Lahan Pertanian CNN** | PyTorch, TorchVision, Matplotlib | Model terlatih (`.pth`), Kurva Loss & Akurasi ($100\%$) |

---

## 🔍 Penjelasan Rinci Setiap Sesi

### 🔹 SESI 1: E-Commerce Customer Lifetime Value (CLV) & Purchasing Behavior Clustering
* **Peran:** *Data Scientist* Profesional
* **Direktori:** [`sesi_1/`](sesi_1/)
* **Deskripsi:** Segmentasi pelanggan (*Customer Segmentation*) menggunakan teknik *Unsupervised Learning* berbasis model transaksional RFM (*Recency, Frequency, Monetary*) dan estimasi *Customer Lifetime Value* (CLV).
* **Komponen Teknis:**
  - `data_preprocessing.py`: Pemuatan data transaksi e-commerce, imputasi/pembersihan missing CustomerID, agregasi matriks RFM & CLV Proxy, serta standarisasi fitur dengan `StandardScaler`.
  - `cluster_model.py`: Penentuan nilai $K$ optimal menggunakan metode **Elbow** (Inertia $K=2..8$), pelatihan algoritma **K-Means**, evaluasi kualitas klaster menggunakan **Silhouette Score** ($0.3080$), profiling persona belanja (*Champions, At Risk, Recent Active, Hibernating*), dan visualisasi scatter plot.
* **Cara Menjalankan:**
  ```bash
  cd sesi_1
  pip install -r requirements.txt
  python cluster_model.py
  ```

---

### 🔹 SESI 2: Modular Pipeline untuk Agregasi Real-Time Harga Komoditas Pangan Lokal
* **Peran:** *Software System Integrator*
* **Direktori:** [`sesi_2/`](sesi_2/)
* **Deskripsi:** Arsitektur pipeline pemrosesan data modular untuk mengambil, membersihkan, memvalidasi, dan mengagregasi fluktuasi harga komoditas pangan harian pasar lokal secara otomatis ke basis data SQLite.
* **Komponen Teknis:**
  - `fetcher.py`: Penarikan data via HTTP Request dengan timeout dan header aman, dilengkapi *graceful fallback mechanism* ke feed cadangan pasar lokal terdesentralisasi bila server eksternal offline.
  - `transformer.py`: Pembersihan data mentah, validasi skema wajib, pembersihan string harga numerik dan satuan via regex (misal `"Rp 14.500/kg"` $\rightarrow$ `14500.0` dan `"kg"`), serta penegakan tipe data Pandas.
  - `main.py`: *Orchestrator* pipeline yang menyimpan data ke database SQLite lokal (`food_prices.db`) dengan timestamp otomatis dan menampilkan tabel ringkasan rata-rata harga pasar.
* **Cara Menjalankan:**
  ```bash
  cd sesi_2
  pip install -r requirements.txt
  python main.py
  ```

---

### 🔹 SESI 3: Analisis Aksesibilitas Spasial dan Buffer Zone Fasilitas Kesehatan
* **Peran:** *Geospatial Data Engineer*
* **Direktori:** [`sesi_3/`](sesi_3/)
* **Deskripsi:** Pemrosesan data titik lokasi faskes (RS & Puskesmas), pembuatan zona penyangga (*Spatial Buffering*) radius 3 km, dan analisis tumpang susun spasial (*Spatial Intersection*) untuk mengukur persentase keterjangkauan wilayah kecamatan.
* **Komponen Teknis:**
  - `data/generate_spatial_data.py`: Generator data batas administrasi kecamatan (`districts.geojson`) dan titik sebaran faskes (`health_facilities.geojson`).
  - `spatial_accessibility.py`: Reproyeksi koordinat ke format metrik (`EPSG:3857`), pembuatan buffer 3.000 meter, operasi `union_all()` dan kalkulasi rasio cakupan luas per kecamatan.
  - **Output:** Peta statis resolusi tinggi (`outputs/healthcare_accessibility_map.png`), peta interaktif web berbasis Folium (`outputs/healthcare_accessibility_map.html`), dan laporan evaluasi keterjangkauan (`outputs/accessibility_coverage_report.csv`).
* **Cara Menjalankan:**
  ```bash
  cd sesi_3
  pip install -r requirements.txt
  python spatial_accessibility.py
  ```

---

### 🔹 SESI 4: Predictive Maintenance: Klasifikasi Kegagalan Mesin Industri (IoT Sensor Data)
* **Peran:** *Machine Learning Engineer*
* **Direktori:** [`sesi_4/`](sesi_4/)
* **Deskripsi:** Alur kerja *Supervised Machine Learning* berbasis data sensor telemetri IoT industri (*Air Temp, Process Temp, Rotational Speed, Torque, Tool Wear, Vibration*) untuk mendeteksi potensi kerusakan mesin pabrik secara preventif.
* **Komponen Teknis:**
  - `predictive_maintenance.py`: Pembagian data berstrata $80:20$, normalisasi `StandardScaler`, pelatihan model **Random Forest Classifier** dan **Gradient Boosting Classifier**.
  - **Evaluasi & Deteksi Overfitting:**
    - *Random Forest:* Test Acc $96.33\%$, Precision $94.44\%$, Recall $62.96\%$, F1-Score $75.56\%$.
    - *Gradient Boosting:* Test Acc $96.67\%$, Precision $94.74\%$, Recall $66.67\%$, F1-Score $78.26\%$.
    - Analisis selisih akurasi Train vs Test ($\text{Gap} \approx 3\%$), membuktikan kedua model bebas dari masalah *overfitting* yang merusak.
* **Cara Menjalankan:**
  ```bash
  cd sesi_4
  pip install -r requirements.txt
  python predictive_maintenance.py
  ```

---

### 🔹 SESI 5: Dasbor Analisis Performa Penjualan Ritel Regional (Prinsip Shneiderman)
* **Peran:** *Frontend & Data Visualization Developer*
* **Direktori:** [`sesi_5/`](sesi_5/)
* **Deskripsi:** Aplikasi web interaktif performa penjualan ritel yang mengimplementasikan prinsip perancangan antarmuka Shneiderman: *"Overview first, zoom and filter, then details-on-demand"*.
* **Komponen Teknis:**
  - `dashboard.py`: Aplikasi Streamlit dengan Plotly Express & Graph Objects.
  - **Zoom and Filter:** Sidebar filter multiselect untuk Wilayah Cabang, Kategori Produk, dan Date Range.
  - **Overview First:** Metrik KPI ringkas (*Total Revenue, Units Sold, Total Orders, AOV*) serta grafik tren bulanan bersih tanpa *chartjunk*.
  - **Details-on-Demand:** Tabel interaktif data transaksi mentah, kolom pencarian cepat, dan fitur ekspor CSV.
* **Cara Menjalankan:**
  ```bash
  cd sesi_5
  pip install -r requirements.txt
  streamlit run dashboard.py
  ```

---

### 🔹 SESI 6: Klasifikasi Tutupan Lahan Pertanian Menggunakan CNN Sederhana
* **Peran:** *Deep Learning Specialist*
* **Direktori:** [`sesi_6/`](sesi_6/)
* **Deskripsi:** Pembangunan model *Convolutional Neural Network* (CNN) menggunakan **PyTorch** untuk klasifikasi citra mikro/patch satelit penginderaan jauh (*Remote Sensing*) ke dalam 4 kategori tutupan lahan: *Hutan Primer, Pertanian/Sawit, Badan Air, Lahan Terbuka*.
* **Komponen Teknis:**
  - `land_cover_cnn.py`: Arsitektur CNN kustom 2 blok konvolusi (`Conv2d` $\rightarrow$ `BatchNorm2d` $\rightarrow$ `ReLU` $\rightarrow$ `MaxPool2d`) + Fully Connected Layers dengan `Dropout(0.30)`.
  - Fungsi *Training Loop* dengan optimizer `Adam(lr=0.001)` dan loss function `nn.CrossEntropyLoss()`.
  - Fungsi validasi akurasi uji per epoch, visualisasi kurva loss & akurasi (`outputs/cnn_training_performance.png`), dan penyimpanan bobot model (`outputs/land_cover_cnn.pth`).
* **Cara Menjalankan:**
  ```bash
  cd sesi_6
  pip install -r requirements.txt
  python land_cover_cnn.py
  ```

---

## ⚙️ Persyaratan Sistem & Instalasi Global

Semua skrip dikembangkan dan diuji menggunakan **Python 3.10+**.

Untuk menginstal seluruh pustaka yang digunakan di semua sesi:
```bash
pip install pandas numpy scikit-learn matplotlib requests geopandas shapely folium streamlit plotly torch torchvision
```

---

## 👨‍💻 Penulis
* **Mohamad Irvan Ramadhansyah** ([@MIrvanR](https://github.com/MIrvanR))
