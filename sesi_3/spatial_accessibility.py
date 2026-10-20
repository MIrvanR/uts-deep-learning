"""
spatial_accessibility.py
Analisis Aksesibilitas Spasial dan Buffer Zone Fasilitas Kesehatan:
1. Membaca data spasial batas administrasi kecamatan & titik faskes (GeoJSON)
2. Transformasi Sistem Koordinat Proyeksi (CRS) ke format metrik (EPSG:3857) untuk kalkulasi jarak akurat
3. Pembuatan zona penyangga (Spatial Buffering) radius 3 km (3000 meter)
4. Analisis tumpang susun spasial (Spatial Intersection) & perhitungan persentase cakupan wilayah
5. Pembuatan visualisasi peta statis (PNG) dan peta interaktif (HTML Folium)

SESI III: Career and Competition in Industrial Era with GIS
Judul: Analisis Aksesibilitas Spasial dan Buffer Zone Fasilitas Kesehatan
"""

import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import folium

from data.generate_spatial_data import create_geojson_datasets

class HealthcareAccessibilityAnalyzer:
    def __init__(self, districts_path="data/districts.geojson", facilities_path="data/health_facilities.geojson"):
        self.districts_path = districts_path
        self.facilities_path = facilities_path
        self.gdf_districts = None
        self.gdf_facilities = None
        self.gdf_buffers = None
        self.metric_crs = "EPSG:3857" # Proyeksi Web Mercator berbasis meter

    def load_data(self):
        """Memuat dataset GeoJSON ke dalam GeoDataFrame."""
        if not os.path.exists(self.districts_path) or not os.path.exists(self.facilities_path):
            print("[INFO] Berkas GeoJSON belum ada, membuat data spasial dasar...")
            create_geojson_datasets()
            
        self.gdf_districts = gpd.read_file(self.districts_path)
        self.gdf_facilities = gpd.read_file(self.facilities_path)
        
        print("\n[SPATIAL LOAD] Berhasil memuat data geospasial:")
        print(f" -> Batas Kecamatan: {len(self.gdf_districts)} fitur wilayah (CRS: {self.gdf_districts.crs})")
        print(f" -> Fasilitas Kesehatan: {len(self.gdf_facilities)} titik faskes (CRS: {self.gdf_facilities.crs})")
        return self.gdf_districts, self.gdf_facilities

    def perform_spatial_buffering(self, buffer_radius_meters=3000):
        """
        Memproyeksikan titik ke sistem koordinat metrik dan membuat zona penyangga (buffer)
        dengan radius tertentu (misal 3.000 meter = 3 km).
        """
        print(f"\n[SPATIAL BUFFER] Memproyeksikan ke {self.metric_crs} dan membuat buffer {buffer_radius_meters/1000:.1f} km...")
        
        # Reproyeksi ke CRS metrik
        fac_metric = self.gdf_facilities.to_crs(self.metric_crs)
        dist_metric = self.gdf_districts.to_crs(self.metric_crs)
        
        # Buat geometri buffer
        buffers_metric = fac_metric.copy()
        buffers_metric["geometry"] = fac_metric.geometry.buffer(buffer_radius_meters)
        
        # Reproyeksi kembali ke WGS84 (EPSG:4326) untuk pemetaan web
        self.gdf_buffers = buffers_metric.to_crs("EPSG:4326")
        
        # Simpan versi metrik untuk analisis interseksi luas
        self.fac_metric = fac_metric
        self.dist_metric = dist_metric
        self.buffers_metric = buffers_metric
        
        print(f"[OK] {len(self.gdf_buffers)} buffer zone berhasil dibentuk.")
        return self.gdf_buffers

    def calculate_accessibility_coverage(self, output_csv="outputs/accessibility_coverage_report.csv"):
        """
        Melakukan spatial intersection antara wilayah kecamatan dan gabungan buffer zone faskes
        untuk menghitung persentase wilayah kecamatan yang terlayani faskes.
        """
        print("\n[SPATIAL INTERSECTION] Menghitung rasio cakupan layanan kesehatan per kecamatan...")
        
        # Gabungkan seluruh buffer menjadi satu kesatuan poligon layanan terintegrasi (Unary Union)
        unified_service_area = self.buffers_metric.geometry.union_all()
        
        report_data = []
        for _, row in self.dist_metric.iterrows():
            district_geom = row.geometry
            district_area_km2 = district_geom.area / 1e6
            
            # Interseksi spasial
            covered_geom = district_geom.intersection(unified_service_area)
            covered_area_km2 = covered_geom.area / 1e6
            coverage_pct = (covered_area_km2 / district_area_km2) * 100 if district_area_km2 > 0 else 0
            
            report_data.append({
                "Kecamatan": row["kecamatan"],
                "Luas_Total_km2": round(district_area_km2, 2),
                "Luas_Terlayani_km2": round(covered_area_km2, 2),
                "Persentase_Cakupan": f"{coverage_pct:.2f}%",
                "Kategori_Aksesibilitas": "Sangat Baik (>80%)" if coverage_pct >= 80 else ("Cukup (50-80%)" if coverage_pct >= 50 else "Perlu Penambahan Faskes (<50%)")
            })
            
        report_df = pd.DataFrame(report_data)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        report_df.to_csv(output_csv, index=False)
        
        print("\n--- Laporan Aksesibilitas Fasilitas Kesehatan ---")
        print(report_df.to_string(index=False))
        print(f"\n[OUTPUT] Laporan cakupan spasial disimpan ke: {output_csv}")
        return report_df

    def create_static_map(self, output_png="outputs/healthcare_accessibility_map.png"):
        """Membuat visualisasi kartografi statis menggunakan Matplotlib & GeoPandas."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 1. Batas administrasi kecamatan
        self.gdf_districts.plot(ax=ax, color="#e9ecef", edgecolor="#495057", linewidth=1.5, alpha=0.9, label="Batas Kecamatan")
        
        # 2. Zona penyangga (buffer 3 km)
        self.gdf_buffers.plot(ax=ax, color="#48cae4", edgecolor="#0077b6", alpha=0.35, linestyle="--", label="Radius Layanan 3 km")
        
        # 3. Titik fasilitas kesehatan
        self.gdf_facilities.plot(ax=ax, color="#d90429", markersize=75, edgecolor="black", zorder=5, label="Fasilitas Kesehatan")
        
        # Beri label nama faskes dan kecamatan
        for _, row in self.gdf_districts.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row["kecamatan"], xy=(centroid.x, centroid.y), ha="center", fontsize=9, fontweight="bold", color="#212529")
            
        for _, row in self.gdf_facilities.iterrows():
            pt = row.geometry
            ax.annotate(row["nama_faskes"], xy=(pt.x, pt.y + 0.003), ha="center", fontsize=8, color="#9d0208", fontweight="semibold")
            
        plt.title("Peta Aksesibilitas Spasial dan Buffer Zone 3 km Fasilitas Kesehatan\n(Geospatial Engineering with GeoPandas)", fontsize=13, fontweight="bold")
        plt.xlabel("Bujur (Longitude)", fontsize=10)
        plt.ylabel("Lintang (Latitude)", fontsize=10)
        plt.grid(True, linestyle=":", alpha=0.5)
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(output_png), exist_ok=True)
        plt.savefig(output_png, dpi=200)
        plt.close()
        print(f"[VISUALISASI] Peta statis berhasil disimpan ke: {output_png}")

    def create_interactive_map(self, output_html="outputs/healthcare_accessibility_map.html"):
        """Membuat visualisasi peta interaktif menggunakan Folium dengan layer switcher."""
        center_lat = self.gdf_districts.to_crs(self.metric_crs).geometry.centroid.to_crs("EPSG:4326").y.mean()
        center_lon = self.gdf_districts.to_crs(self.metric_crs).geometry.centroid.to_crs("EPSG:4326").x.mean()
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="OpenStreetMap")
        
        # Layer 1: Kecamatan (Choropleth/Batas)
        district_layer = folium.GeoJson(
            self.gdf_districts,
            name="Batas Administrasi Kecamatan",
            style_function=lambda x: {
                "fillColor": "#adb5bd",
                "color": "#343a40",
                "weight": 2,
                "fillOpacity": 0.2
            },
            tooltip=folium.GeoJsonTooltip(fields=["kecamatan", "populasi"], aliases=["Kecamatan:", "Populasi:"])
        )
        district_layer.add_to(m)
        
        # Layer 2: Buffer Zones (3 km)
        buffer_layer = folium.GeoJson(
            self.gdf_buffers,
            name="Zona Penyangga (Radius 3 km)",
            style_function=lambda x: {
                "fillColor": "#00b4d8",
                "color": "#0077b6",
                "weight": 1.5,
                "fillOpacity": 0.25,
                "dashArray": "5, 5"
            }
        )
        buffer_layer.add_to(m)
        
        # Layer 3: Marker Titik Fasilitas Kesehatan
        facility_fg = folium.FeatureGroup(name="Fasilitas Kesehatan")
        for _, row in self.gdf_facilities.iterrows():
            lat = row.geometry.y
            lon = row.geometry.x
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 200px;">
                <h4 style="margin: 0; color: #d90429;">{row['nama_faskes']}</h4>
                <p style="margin: 5px 0;"><b>Kategori:</b> {row['kategori']}<br>
                <b>Kapasitas Bed:</b> {row['kapasitas_bed']} unit</p>
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=row["nama_faskes"],
                icon=folium.Icon(color="red", icon="plus", prefix="fa")
            ).add_to(facility_fg)
            
        facility_fg.add_to(m)
        folium.LayerControl().add_to(m)
        
        os.makedirs(os.path.dirname(output_html), exist_ok=True)
        m.save(output_html)
        print(f"[VISUALISASI] Peta interaktif berhasil disimpan ke: {output_html}")

def main():
    print("=" * 80)
    print("  STUDI KASUS SESI III: ANALISIS AKSESIBILITAS SPASIAL FASILITAS KESEHATAN")
    print("  Geospatial Engineering: Buffering (3 km) + Spatial Intersection (GeoPandas)")
    print("=" * 80)
    
    analyzer = HealthcareAccessibilityAnalyzer()
    analyzer.load_data()
    analyzer.perform_spatial_buffering(buffer_radius_meters=3000)
    analyzer.calculate_accessibility_coverage()
    analyzer.create_static_map()
    analyzer.create_interactive_map()
    print("\n[SELESAI] Seluruh analisis geospasial berhasil diselesaikan.")

if __name__ == "__main__":
    main()
