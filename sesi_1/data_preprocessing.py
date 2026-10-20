"""
data_preprocessing.py
Modul Preprocessing Data Transaksional E-Commerce:
1. Pemuatan dan Pembersihan Data (Handling Missing Values & Outliers)
2. Agregasi RFM (Recency, Frequency, Monetary) & Customer Lifetime Value (CLV)
3. Standarisasi Fitur menggunakan StandardScaler

SESI I: Patterns of Data with Analysis and AI
Judul: E-Commerce Customer Lifetime Value (CLV) & Purchasing Behavior Clustering
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

def generate_sample_transactions(output_path="ecommerce_transactions.csv", n_records=2500, n_customers=350, random_state=42):
    """
    Menghasilkan data transaksi e-commerce sintetis yang realistis
    jika dataset eksternal belum tersedia.
    """
    np.random.seed(random_state)
    base_date = datetime(2026, 1, 1)
    
    customer_ids = [f"CUST-{1000 + i}" for i in range(n_customers)]
    records = []
    
    for i in range(n_records):
        cust = np.random.choice(customer_ids)
        # Tanggal transaksi acak dalam rentang 365 hari
        days_offset = np.random.randint(0, 365)
        trans_date = base_date + timedelta(days=days_offset)
        invoice_no = f"INV-{10000 + (i // 2)}"
        quantity = np.random.choice([1, 2, 3, 4, 5, 10], p=[0.45, 0.25, 0.15, 0.08, 0.05, 0.02])
        unit_price = np.round(np.random.exponential(scale=45.0) + 5.0, 2)
        total_amount = np.round(quantity * unit_price, 2)
        
        records.append({
            "InvoiceNo": invoice_no,
            "CustomerID": cust if np.random.rand() > 0.03 else None, # Simulasi 3% missing customer ID
            "InvoiceDate": trans_date.strftime("%Y-%m-%d"),
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "TotalAmount": total_amount
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"[PREPROCESSING] Berkas transaksi berhasil dibuat: {output_path} ({len(df)} baris)")
    return df

def load_and_clean_data(csv_path="ecommerce_transactions.csv"):
    """
    Memuat dataset transaksi dan menangani inkonsistensi data:
    - Menghapus transaksi tanpa identitas pelanggan (Missing CustomerID)
    - Memastikan nilai Quantity dan TotalAmount bernilai positif
    - Mengonversi format tanggal menjadi objek datetime
    """
    if not os.path.exists(csv_path):
        print(f"[INFO] Berkas {csv_path} tidak ditemukan, membuat data baru...")
        generate_sample_transactions(csv_path)
        
    df = pd.read_csv(csv_path)
    initial_rows = len(df)
    
    # 1. Penanganan Missing Values pada CustomerID
    missing_cust = df["CustomerID"].isnull().sum()
    df = df.dropna(subset=["CustomerID"]).copy()
    
    # 2. Validasi tipe data dan integritas transaksi
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df = df[(df["Quantity"] > 0) & (df["TotalAmount"] > 0)].copy()
    
    print(f"[PREPROCESSING] Data berhasil dimuat:")
    print(f" -> Baris awal: {initial_rows}")
    print(f" -> Missing CustomerID dihapus: {missing_cust}")
    print(f" -> Baris valid tersisa: {len(df)}")
    
    return df

def compute_rfm_clv(df, reference_date=None):
    """
    Melakukan agregasi transaksional ke level pelanggan (Customer-Level):
    - Recency (R)   : Jumlah hari sejak transaksi terakhir pelanggan hingga tanggal referensi
    - Frequency (F) : Jumlah frekuensi invoice/transaksi unik
    - Monetary (M)  : Total nilai pembelanjaan akumulatif
    - CLV Proxy     : Estimasi nilai pelanggan seumur hidup (Monetary * Log(Frequency + 1))
    """
    if reference_date is None:
        reference_date = df["InvoiceDate"].max() + timedelta(days=1)
        
    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda d: (reference_date - d.max()).days,
        "InvoiceNo": "nunique",
        "TotalAmount": "sum"
    }).reset_index()
    
    rfm.rename(columns={
        "InvoiceDate": "Recency",
        "InvoiceNo": "Frequency",
        "TotalAmount": "Monetary"
    }, inplace=True)
    
    # Menghitung estimasi sederhana CLV (Customer Lifetime Value)
    rfm["CLV_Proxy"] = np.round(rfm["Monetary"] * (1 + np.log1p(rfm["Frequency"])), 2)
    
    print(f"[PREPROCESSING] Agregasi RFM & CLV berhasil untuk {len(rfm)} pelanggan unik.")
    return rfm

def scale_features(rfm_df, feature_cols=["Recency", "Frequency", "Monetary", "CLV_Proxy"]):
    """
    Melakukan standarisasi fitur numerik menggunakan StandardScaler (Z-Score)
    agar variabel dengan satuan besar (Monetary) tidak mendominasi algoritma K-Means.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(rfm_df[feature_cols])
    scaled_df = pd.DataFrame(scaled_data, columns=[f"{col}_scaled" for col in feature_cols])
    
    print(f"[PREPROCESSING] Standarisasi fitur selesai untuk kolom: {feature_cols}")
    return scaled_df, scaler

if __name__ == "__main__":
    raw_data = load_and_clean_data()
    rfm_table = compute_rfm_clv(raw_data)
    scaled_features, _ = scale_features(rfm_table)
    print("\nContoh 5 Baris Data RFM Teratas:")
    print(rfm_table.head())
