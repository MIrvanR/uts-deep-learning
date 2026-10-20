"""
dashboard.py
Aplikasi Dasbor Analisis Performa Penjualan Ritel Regional
Menerapkan Prinsip Visualisasi Shneiderman:
1. Overview First : Metrik KPI utama & tren pendapatan bulanan makro (Plotly no chartjunk)
2. Zoom and Filter: Sidebar interaktif pemfilteran Wilayah Cabang, Kategori, & Tanggal
3. Details on Demand: Tabel interaktif data transaksi mentah dengan pencarian & unduhan

SESI V: Human-Computer Interaction & Data Visualization
Judul: Dasbor Analisis Performa Penjualan Ritel Regional (Prinsip Shneiderman)
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data.generate_sales_data import create_retail_dataset

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Dasbor Penjualan Ritel Regional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Pemuatan Data dengan Caching
@st.cache_data
def load_sales_data(data_path="data/sales_data.csv"):
    if not os.path.exists(data_path):
        create_retail_dataset(data_path)
    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

data_file = os.path.join(os.path.dirname(__file__), "data", "sales_data.csv")
df_raw = load_sales_data(data_file)

# 3. IMPLEMENTASI PRINSIP SHNEIDERMAN: ZOOM AND FILTER (SIDEBAR)
st.sidebar.title("🔍 Filter & Navigasi")
st.sidebar.markdown("*Prinsip Shneiderman: Zoom and Filter*")

# Filter Wilayah Cabang
all_regions = sorted(df_raw["Region"].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Pilih Wilayah Cabang:",
    options=all_regions,
    default=all_regions
)

# Filter Kategori Produk
all_categories = sorted(df_raw["Category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=all_categories,
    default=all_categories
)

# Filter Rentang Tanggal
min_date = df_raw["Date"].min().date()
max_date = df_raw["Date"].max().date()
selected_dates = st.sidebar.date_input(
    "Rentang Waktu Transaksi:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Validasi dan Aplikasi Filter
if not selected_regions or not selected_categories:
    st.warning("Silakan pilih minimal satu Wilayah dan satu Kategori pada bilah filter samping.")
    st.stop()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_dt, end_dt = selected_dates
else:
    start_dt, end_dt = min_date, max_date

filtered_df = df_raw[
    (df_raw["Region"].isin(selected_regions)) &
    (df_raw["Category"].isin(selected_categories)) &
    (df_raw["Date"].dt.date >= start_dt) &
    (df_raw["Date"].dt.date <= end_dt)
].copy()

# Header Utama Aplikasi
st.title("📈 Dasbor Analisis Performa Penjualan Ritel Regional")
st.caption("Implementasi Prinsip Interaksi Manusia-Komputer: *Overview First, Zoom and Filter, Details-on-Demand*")
st.markdown("---")

# 4. IMPLEMENTASI PRINSIP SHNEIDERMAN: OVERVIEW FIRST (RINGKASAN MAKRO & KPI)
total_revenue = filtered_df["TotalRevenue"].sum()
total_transactions = len(filtered_df)
total_units = filtered_df["Quantity"].sum()
avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Pendapatan", f"Rp {total_revenue:,.0f}")
col2.metric("📦 Unit Terjual", f"{total_units:,} pcs")
col3.metric("🧾 Total Transaksi", f"{total_transactions:,}")
col4.metric("📊 Rata-rata Nilai Pesanan (AOV)", f"Rp {avg_order_value:,.0f}")

st.markdown("### 📊 Tren Pendapatan Bulanan (Overview)")

# Agregasi Bulanan
monthly_agg = filtered_df.groupby("Month").agg({
    "TotalRevenue": "sum",
    "Quantity": "sum",
    "TransactionID": "count"
}).reset_index()

# Visualisasi Plotly Bersih (Bebas Chartjunk / Edward Tufte & Shneiderman Compliant)
fig_trend = px.line(
    monthly_agg,
    x="Month",
    y="TotalRevenue",
    markers=True,
    title="Tren Pendapatan Bulanan (Clean Line Chart)",
    labels={"Month": "Periode Bulan", "TotalRevenue": "Total Pendapatan (IDR)"}
)
fig_trend.update_traces(
    line=dict(color="#1f77b4", width=3),
    marker=dict(size=8, color="#0d47a1")
)
fig_trend.update_layout(
    template="plotly_white",
    hovermode="x unified",
    margin=dict(l=40, r=40, t=50, b=40),
    xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickformat=",")
)
st.plotly_chart(fig_trend, use_container_width=True)

# Visualisasi Tambahan: Kontribusi Pendapatan per Kategori & Wilayah
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    cat_agg = filtered_df.groupby("Category")["TotalRevenue"].sum().reset_index()
    fig_cat = px.bar(
        cat_agg,
        x="TotalRevenue",
        y="Category",
        orientation="h",
        title="Distribusi Pendapatan per Kategori Produk",
        labels={"TotalRevenue": "Pendapatan (IDR)", "Category": "Kategori"},
        color_discrete_sequence=["#2ca02c"]
    )
    fig_cat.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_cat, use_container_width=True)

with chart_col2:
    reg_agg = filtered_df.groupby("Region")["TotalRevenue"].sum().reset_index()
    fig_reg = px.pie(
        reg_agg,
        names="Region",
        values="TotalRevenue",
        title="Pangsa Pasar per Wilayah Regional",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_reg.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_reg, use_container_width=True)

st.markdown("---")

# 5. IMPLEMENTASI PRINSIP SHNEIDERMAN: DETAILS-ON-DEMAND (DATA MENTAH)
st.markdown("### 📋 Rincian Transaksi Mentah (*Details-on-Demand*)")
st.write(f"Menampilkan **{len(filtered_df)}** baris transaksi sesuai filter yang aktif.")

# Fitur Pencarian Cepat
search_keyword = st.text_input("Cari berdasarkan ID Transaksi atau Metode Pembayaran:", "")
display_df = filtered_df.copy()
if search_keyword:
    display_df = display_df[
        display_df["TransactionID"].str.contains(search_keyword, case=False) |
        display_df["PaymentMethod"].str.contains(search_keyword, case=False)
    ]

# Tampilkan tabel interaktif
st.dataframe(
    display_df.style.format({
        "UnitPrice": "Rp {:,.0f}",
        "TotalRevenue": "Rp {:,.0f}",
        "Quantity": "{:,} pcs"
    }),
    use_container_width=True,
    height=320
)

# Tombol Ekspor CSV
csv_data = display_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Unduh Data Transaksi Terfilter (CSV)",
    data=csv_data,
    file_name="transaksi_ritel_terfilter.csv",
    mime="text/csv"
)
