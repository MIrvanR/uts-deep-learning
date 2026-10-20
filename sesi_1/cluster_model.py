"""
cluster_model.py
Modul Pemodelan K-Means Clustering & Evaluasi Klaster:
1. Penentuan K Optimal dengan Metode Elbow (Inertia Analysis)
2. Pelatihan K-Means dengan K Terpilih
3. Evaluasi Kualitas Klaster menggunakan Silhouette Score
4. Profiling dan Visualisasi Segmentasi Pelanggan

SESI I: Patterns of Data with Analysis and AI
Judul: E-Commerce Customer Lifetime Value (CLV) & Purchasing Behavior Clustering
"""

import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_preprocessing import load_and_clean_data, compute_rfm_clv, scale_features

def find_optimal_clusters_elbow(X, k_range=range(2, 9), output_plot="elbow_curve.png"):
    """
    Menghitung inertia (Within-Cluster Sum of Squares) untuk berbagai nilai K
    dan menghasilkan grafik kurva Elbow untuk menentukan titik belok (elbow point).
    """
    inertias = []
    k_values = list(k_range)
    
    print("\n[ELBOW METHOD] Menghitung inersia untuk penentuan jumlah klaster optimal...")
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        print(f" -> K = {k} | Inertia = {kmeans.inertia_:.2f}")
        
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, inertias, "bo-", linewidth=2, markersize=8)
    plt.title("Metode Elbow untuk Penentuan Jumlah Klaster Optimal (K)", fontsize=12, fontweight="bold")
    plt.xlabel("Jumlah Klaster (K)", fontsize=11)
    plt.ylabel("Inertia (Within-Cluster Sum of Squares)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_plot, dpi=200)
    plt.close()
    print(f"[VISUALISASI] Kurva Elbow berhasil disimpan ke: {output_plot}")
    return inertias

def build_kmeans_model(rfm_df, scaled_features, n_clusters=4, output_plot="customer_clusters.png"):
    """
    Melatih model K-Means dengan K yang dipilih, menghitung Silhouette Score,
    dan melakukan profiling karakteristik perilaku belanja untuk masing-masing segmen.
    """
    print(f"\n[K-MEANS] Melatih model K-Means dengan {n_clusters} klaster...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_features)
    
    # 1. Evaluasi dengan Silhouette Score
    score = silhouette_score(scaled_features, cluster_labels)
    print(f"[EVALUASI] Silhouette Score: {score:.4f} (Mendekati 1 = Pemisahan klaster sangat baik)")
    
    # 2. Tambahkan label klaster ke data RFM asli
    segmented_rfm = rfm_df.copy()
    segmented_rfm["Cluster"] = cluster_labels
    
    # 3. Profiling Segmentasi Pelanggan
    profile = segmented_rfm.groupby("Cluster").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean",
        "CLV_Proxy": "mean",
        "CustomerID": "count"
    }).rename(columns={"CustomerID": "Jumlah_Pelanggan"}).round(2)
    
    # Penamaan Persona Bisnis berdasarkan profil
    cluster_names = {}
    for cl in profile.index:
        rec = profile.loc[cl, "Recency"]
        mon = profile.loc[cl, "Monetary"]
        if mon > profile["Monetary"].median() and rec < profile["Recency"].median():
            cluster_names[cl] = "Champions / High-Value Loyal"
        elif rec > profile["Recency"].median() and mon > profile["Monetary"].median():
            cluster_names[cl] = "At Risk / Former High-Spender"
        elif rec < profile["Recency"].median():
            cluster_names[cl] = "Recent Active Buyers"
        else:
            cluster_names[cl] = "Hibernating / Low Engagement"
            
    segmented_rfm["Persona"] = segmented_rfm["Cluster"].map(cluster_names)
    
    print("\n--- Profil Karakteristik Segmentasi Pelanggan ---")
    print(profile)
    
    # 4. Visualisasi Klaster: Recency vs Monetary
    plt.figure(figsize=(9, 6))
    scatter = plt.scatter(
        segmented_rfm["Recency"],
        segmented_rfm["Monetary"],
        c=segmented_rfm["Cluster"],
        cmap="tab10",
        alpha=0.75,
        edgecolors="k",
        s=55
    )
    plt.title(f"Segmentasi Pelanggan E-Commerce (K-Means, K={n_clusters})\nSilhouette Score: {score:.3f}", fontsize=12, fontweight="bold")
    plt.xlabel("Recency (Hari sejak transaksi terakhir)", fontsize=11)
    plt.ylabel("Monetary (Total Belanja dalam USD)", fontsize=11)
    plt.colorbar(scatter, label="Cluster ID")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_plot, dpi=200)
    plt.close()
    print(f"[VISUALISASI] Plot segmentasi pelanggan disimpan ke: {output_plot}")
    
    # Simpan hasil segmentasi ke CSV
    segmented_rfm.to_csv("segmented_customers.csv", index=False)
    print(f"[OUTPUT] Berkas hasil segmentasi disimpan ke: segmented_customers.csv")
    
    return segmented_rfm, score

def main():
    print("=" * 75)
    print("  STUDI KASUS SESI I: E-COMMERCE CLV & PURCHASING BEHAVIOR CLUSTERING")
    print("  Data Science Pipeline: RFM + K-Means Clustering + Silhouette Evaluation")
    print("=" * 75)
    
    # Langkah 1: Pemuatan & Pembersihan Data
    raw_df = load_and_clean_data("ecommerce_transactions.csv")
    
    # Langkah 2: Agregasi RFM & CLV
    rfm_df = compute_rfm_clv(raw_df)
    
    # Langkah 3: Standarisasi Fitur
    scaled_features, _ = scale_features(rfm_df)
    
    # Langkah 4: Analisis K Optimal dengan Metode Elbow
    find_optimal_clusters_elbow(scaled_features)
    
    # Langkah 5: Pelatihan K-Means & Profiling Pelanggan
    build_kmeans_model(rfm_df, scaled_features, n_clusters=4)
    print("\n[SELESAI] Pipeline Clustering Sesi I Berhasil Dijalankan.")

if __name__ == "__main__":
    main()
