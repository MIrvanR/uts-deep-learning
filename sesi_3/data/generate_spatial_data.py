"""
generate_spatial_data.py
Generator Data Spasial Format GeoJSON:
1. data/districts.geojson: Poligon batas administrasi kecamatan wilayah perkotaan
2. data/health_facilities.geojson: Titik sebaran fasilitas kesehatan (Rumah Sakit & Puskesmas)

SESI III: Career and Competition in Industrial Era with GIS
Judul: Analisis Aksesibilitas Spasial dan Buffer Zone Fasilitas Kesehatan
"""

import json
import os

def create_geojson_datasets(output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Batas Administrasi Kecamatan (MultiPoligon / Poligon Sederhana WGS84)
    # Wilayah representatif perkotaan (Area Yogyakarta / Sekitarnya, Lat: -7.80, Lon: 110.37)
    districts = {
        "type": "FeatureCollection",
        "name": "Batas_Administrasi_Kecamatan",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [
            {
                "type": "Feature",
                "properties": {"id": 1, "kecamatan": "Kecamatan Sentral", "populasi": 68500, "luas_km2": 14.2},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [110.350, -7.780], [110.380, -7.780], [110.380, -7.805],
                        [110.350, -7.805], [110.350, -7.780]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"id": 2, "kecamatan": "Kecamatan Timur Sejahtera", "populasi": 84200, "luas_km2": 18.5},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [110.380, -7.780], [110.420, -7.780], [110.420, -7.810],
                        [110.380, -7.805], [110.380, -7.780]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"id": 3, "kecamatan": "Kecamatan Barat Makmur", "populasi": 52100, "luas_km2": 16.0},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [110.315, -7.785], [110.350, -7.780], [110.350, -7.815],
                        [110.315, -7.815], [110.315, -7.785]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"id": 4, "kecamatan": "Kecamatan Selatan Asri", "populasi": 71000, "luas_km2": 21.0},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [110.340, -7.805], [110.410, -7.810], [110.410, -7.845],
                        [110.340, -7.845], [110.340, -7.805]
                    ]]
                }
            }
        ]
    }
    
    # 2. Titik Lokasi Fasilitas Kesehatan (Points)
    health_facilities = {
        "type": "FeatureCollection",
        "name": "Titik_Fasilitas_Kesehatan",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [
            {
                "type": "Feature",
                "properties": {"id": 101, "nama_faskes": "RSUD Kota Madya", "kategori": "Rumah Sakit Umum", "kapasitas_bed": 220},
                "geometry": {"type": "Point", "coordinates": [110.368, -7.792]}
            },
            {
                "type": "Feature",
                "properties": {"id": 102, "nama_faskes": "Puskesmas Sentral Induk", "kategori": "Puskesmas Rawat Inap", "kapasitas_bed": 25},
                "geometry": {"type": "Point", "coordinates": [110.358, -7.798]}
            },
            {
                "type": "Feature",
                "properties": {"id": 103, "nama_faskes": "RS Mata Pratama", "kategori": "Rumah Sakit Khusus", "kapasitas_bed": 60},
                "geometry": {"type": "Point", "coordinates": [110.395, -7.790]}
            },
            {
                "type": "Feature",
                "properties": {"id": 104, "nama_faskes": "Puskesmas Timur Bahagia", "kategori": "Puskesmas Non-Rawat Inap", "kapasitas_bed": 5},
                "geometry": {"type": "Point", "coordinates": [110.408, -7.799]}
            },
            {
                "type": "Feature",
                "properties": {"id": 105, "nama_faskes": "Klinik Medika Selatan", "kategori": "Klinik Pratama", "kapasitas_bed": 12},
                "geometry": {"type": "Point", "coordinates": [110.365, -7.825]}
            }
        ]
    }
    
    districts_file = os.path.join(output_dir, "districts.geojson")
    with open(districts_file, "w", encoding="utf-8") as f:
        json.dump(districts, f, indent=2)
        
    faskes_file = os.path.join(output_dir, "health_facilities.geojson")
    with open(faskes_file, "w", encoding="utf-8") as f:
        json.dump(health_facilities, f, indent=2)
        
    print(f"[GIS DATA] Berhasil membuat data spasial:")
    print(f" -> {districts_file}")
    print(f" -> {faskes_file}")

if __name__ == "__main__":
    create_geojson_datasets()
