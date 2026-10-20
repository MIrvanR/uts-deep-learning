"""
generate_sales_data.py
Generator data transaksi penjualan ritel regional untuk aplikasi Streamlit Dashboard.

SESI V: Human-Computer Interaction & Data Visualization
Judul: Dasbor Analisis Performa Penjualan Ritel Regional (Prinsip Shneiderman)
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def create_retail_dataset(output_path="data/sales_data.csv", n_records=1200, random_state=42):
    np.random.seed(random_state)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    regions = ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Bali & Nusa Tenggara"]
    categories = {
        "Elektronik & Gadget": (1500000, 8500000),
        "Fashion & Busana": (85000, 650000),
        "Bahan Makanan & Kuliner": (25000, 220000),
        "Peralatan Rumah Tangga": (120000, 1450000)
    }
    
    start_date = datetime(2026, 1, 1)
    records = []
    
    for i in range(n_records):
        cat = np.random.choice(list(categories.keys()), p=[0.25, 0.30, 0.25, 0.20])
        min_p, max_p = categories[cat]
        unit_price = int(np.random.uniform(min_p, max_p))
        qty = int(np.random.choice([1, 2, 3, 4, 5, 8], p=[0.50, 0.25, 0.12, 0.08, 0.03, 0.02]))
        total_rev = unit_price * qty
        
        days_offset = np.random.randint(0, 360)
        t_date = start_date + timedelta(days=days_offset)
        
        records.append({
            "TransactionID": f"TRX-{20260000 + i}",
            "Date": t_date.strftime("%Y-%m-%d"),
            "Month": t_date.strftime("%Y-%m"),
            "Region": np.random.choice(regions, p=[0.35, 0.25, 0.18, 0.14, 0.08]),
            "Category": cat,
            "Quantity": qty,
            "UnitPrice": unit_price,
            "TotalRevenue": total_rev,
            "PaymentMethod": np.random.choice(["QRIS / E-Wallet", "Transfer Bank", "Kartu Kredit", "Tunai"])
        })
        
    df = pd.DataFrame(records)
    df.sort_values(by="Date", inplace=True)
    df.to_csv(output_path, index=False)
    print(f"[DATA] Dataset penjualan ritel berhasil dibuat: {output_path} ({n_records} transaksi)")
    return df

if __name__ == "__main__":
    create_retail_dataset()
