# SESI IV: Predictive Maintenance - Klasifikasi Kegagalan Mesin Industri (IoT Sensor Data)

Pipeline *Supervised Machine Learning* berbasis sensor telemetri IoT industri untuk mendeteksi potensi anomali dan kerusakan mesin manufaktur secara dini, mencegah *downtime*, dan mendeteksi fenomena *overfitting*.

## ⚙️ Fitur & Metodologi
1. **Dataset Sensor Multivariat**:
   - `air_temp_k`: Suhu udara lingkungan (Kelvin).
   - `process_temp_k`: Suhu operasional mesin (Kelvin).
   - `rotational_speed_rpm`: Kecepatan putaran poros mesin (RPM).
   - `torque_nm`: Torsi mekanis (Nm).
   - `tool_wear_min`: Durasi keausan alat pemotong (menit).
   - `vibration_mms`: Tingkat getaran sensor (mm/s).
   - Target biner `machine_failure` (1 = Mesin Rusak, 0 = Normal).
2. **Preprocessing**:
   - Pembagian data berstrata $80:20$ (Train/Test Split).
   - Standarisasi fitur dengan `StandardScaler`.
3. **Model Klasifikasi Terpilih**:
   - **Random Forest Classifier** (Bagging Ensemble).
   - **Gradient Boosting Classifier** (Sequential Boosting Ensemble).
4. **Evaluasi & Deteksi Overfitting**:
   - Perhitungan metrik **Precision**, **Recall**, dan **F1-Score**.
   - Evaluasi komparatif akurasi data latih vs data uji untuk menganalisis batas generalisasi model.

## 🚀 Cara Menjalankan
```bash
pip install -r requirements.txt
python predictive_maintenance.py
```
