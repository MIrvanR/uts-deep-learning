# SESI I: E-Commerce Customer Lifetime Value (CLV) & Purchasing Behavior Clustering

Implementasi segmentasi pelanggan (*Customer Segmentation*) menggunakan teknik *Unsupervised Machine Learning* (K-Means Clustering) dan analisis transaksional RFM (*Recency, Frequency, Monetary*) beserta estimasi *Customer Lifetime Value* (CLV).

## 🚀 Fitur Utama
1. **Pembersihan & Preprocessing Data (`data_preprocessing.py`)**:
   - Pembersihan data transaksi (handling missing CustomerID & invalid records).
   - Agregasi matriks RFM:
     - **Recency**: Hari sejak transaksi terakhir.
     - **Frequency**: Jumlah invoice unik.
     - **Monetary**: Total nilai belanja akumulatif.
     - **CLV Proxy**: Estimasi nilai jangka panjang pelanggan.
   - Standarisasi skala fitur dengan `StandardScaler`.
2. **Pemodelan & Evaluasi Klaster (`cluster_model.py`)**:
   - Penentuan jumlah klaster optimal melalui metode **Elbow (Inertia Curve)**.
   - Pelatihan algoritma **K-Means Clustering**.
   - Evaluasi kualitas pemisahan klaster menggunakan **Silhouette Score**.
   - Profiling persona pelanggan (*Champions*, *At Risk*, *Recent Active*, *Hibernating*).
   - Visualisasi plot segmentasi dan kurva elbow.

## 🛠️ Cara Menjalankan
```bash
pip install -r requirements.txt
python cluster_model.py
```
