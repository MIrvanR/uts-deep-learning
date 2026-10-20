# SESI III: Analisis Aksesibilitas Spasial dan Buffer Zone Fasilitas Kesehatan

Proyek pemrosesan data geospasial (*Geospatial Engineering*) untuk memetakan titik sebaran fasilitas kesehatan (RS & Puskesmas), membentuk zona penyangga (*Spatial Buffering*) radius 3 km, serta menganalisis persentase keterjangkauan wilayah administratif kecamatan menggunakan pustaka `geopandas`, `shapely`, `matplotlib`, dan `folium`.

## 🗺️ Metodologi Analisis Spasial
1. **Transformasi Sistem Koordinat Proyeksi (CRS)**:
   - Mengonversi data dari WGS84 (`EPSG:4326`) ke proyeksi metrik (`EPSG:3857`) agar operasi jarak penyangga berbasis meter presisi.
2. **Spatial Buffering (3.000 Meter)**:
   - Membentuk radius keterjangkauan layanan kesehatan dasar sejauh 3 km dari masing-masing fasilitas kesehatan.
3. **Spatial Intersection & Unary Union**:
   - Menghitung tumpang susun geometri layanan terhadap poligon batas administrasi kecamatan untuk mengukur persentase luas area yang terlayani (*Coverage Ratio*).
4. **Visualisasi Kartografi**:
   - Peta Statis resolusi tinggi (`outputs/healthcare_accessibility_map.png`).
   - Peta Interaktif berbasis web dengan *Layer Control* dan *Tooltip* (`outputs/healthcare_accessibility_map.html`).

## 🚀 Cara Menjalankan
```bash
pip install -r requirements.txt
python spatial_accessibility.py
```
