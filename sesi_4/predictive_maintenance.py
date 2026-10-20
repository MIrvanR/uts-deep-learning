"""
predictive_maintenance.py
Studi Kasus Machine Learning: Predictive Maintenance Mesin Industri berbasis Sensor IoT
Tahapan Lengkap:
1. Pemuatan & Pembentukan Dataset Multivariat Sensor IoT Mesin Industri
2. Train-Test Split (80:20) dan Normalisasi Fitur menggunakan StandardScaler
3. Pelatihan Model: Random Forest Classifier & Gradient Boosting Classifier
4. Evaluasi Kinerja: Precision, Recall, F1-Score, Confusion Matrix
5. Deteksi Overfitting melalui Komparasi Metrik Training vs Testing

SESI IV: Introduction to Machine Learning
Judul: Predictive Maintenance: Klasifikasi Kegagalan Mesin Industri (IoT Sensor Data)
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generate_iot_sensor_dataset(output_path="data/sensor_maintenance_data.csv", n_samples=1500, random_state=42):
    """
    Menghasilkan data telemetri sensor IoT mesin industri (terinspirasi dari dataset AI4I Predictive Maintenance).
    Fitur:
    - air_temp_k          : Suhu udara lingkungan mesin (Kelvin)
    - process_temp_k      : Suhu operasional internal mesin (Kelvin)
    - rotational_speed_rpm: Kecepatan putaran motor spindel (RPM)
    - torque_nm           : Torsi mekanis (Newton meter)
    - tool_wear_min       : Akumulasi waktu keausan alat pemotong (menit)
    - vibration_mms       : Getaran dinamis bantalan mesin (mm/s)
    - machine_failure     : Status kegagalan (1: Rusak/Failure, 0: Normal)
    """
    np.random.seed(random_state)
    
    air_temp = np.random.normal(300.0, 2.0, n_samples)
    process_temp = air_temp + np.random.normal(10.0, 1.0, n_samples)
    rotational_speed = np.random.normal(1530.0, 180.0, n_samples)
    torque = np.random.normal(40.0, 10.0, n_samples)
    tool_wear = np.random.uniform(0, 240, n_samples)
    vibration = np.random.exponential(1.5, n_samples) + 0.5
    
    # Formulasi fisik kegagalan mesin (Power Failures, Tool Wear Overheat, Mechanical Stress)
    temp_diff = process_temp - air_temp
    mechanical_power = (torque * rotational_speed) / 9550.0 # Daya mekanis kW
    
    # Logit probabilitas kegagalan
    failure_logit = (
        -0.5
        + 0.02 * (tool_wear - 150)
        + 0.08 * (torque - 50)
        + 0.50 * (vibration - 3.0)
        - 0.003 * (rotational_speed - 1500)
        + 0.15 * (temp_diff - 10)
    )
    failure_prob = 1 / (1 + np.exp(-failure_logit))
    machine_failure = (failure_prob > 0.50).astype(int)
    
    df = pd.DataFrame({
        "air_temp_k": np.round(air_temp, 2),
        "process_temp_k": np.round(process_temp, 2),
        "rotational_speed_rpm": np.round(rotational_speed, 1),
        "torque_nm": np.round(torque, 2),
        "tool_wear_min": np.round(tool_wear, 1),
        "vibration_mms": np.round(vibration, 2),
        "machine_failure": machine_failure
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[DATASET] Dataset IoT sensor berhasil disiapkan: {output_path} ({n_samples} baris)")
    return df

class PredictiveMaintenancePipeline:
    def __init__(self, data_path="data/sensor_maintenance_data.csv", test_size=0.20, random_state=42):
        self.data_path = data_path
        self.test_size = test_size
        self.random_state = random_state
        self.feature_cols = [
            "air_temp_k", "process_temp_k", "rotational_speed_rpm",
            "torque_nm", "tool_wear_min", "vibration_mms"
        ]
        self.scaler = StandardScaler()
        self.models = {}
        self.evaluation_results = []

    def prepare_data(self):
        """Memuat dataset, melakukan stratifikasi 80:20, dan normalisasi StandardScaler."""
        if not os.path.exists(self.data_path):
            generate_iot_sensor_dataset(self.data_path)
            
        df = pd.read_csv(self.data_path)
        X = df[self.feature_cols].values
        y = df["machine_failure"].values
        
        # Train-Test Split (80:20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        
        # Normalisasi Fitur menggunakan StandardScaler (fit pada train, transform pada test)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("\n" + "="*75)
        print("[TAHAP PREPROCESSING & SPLIT]")
        print("="*75)
        print(f"Total Sampel Data Sensor: {len(df)}")
        print(f"Data Latih (Training 80%) : {X_train.shape[0]} sampel")
        print(f"Data Uji   (Testing 20%)  : {X_test.shape[0]} sampel")
        print(f"Jumlah Fitur Telemetri  : {len(self.feature_cols)}")
        print(f"Rasio Kegagalan (Failure Rate): {df['machine_failure'].mean()*100:.2f}%")
        
        self.X_train_scaled = X_train_scaled
        self.X_test_scaled = X_test_scaled
        self.y_train = y_train
        self.y_test = y_test
        return X_train_scaled, X_test_scaled, y_train, y_test

    def train_and_evaluate_models(self):
        """
        Melatih Random Forest dan Gradient Boosting Classifier,
        menghitung metrik (Precision, Recall, F1) dan mendeteksi overfitting.
        """
        self.models = {
            "Random Forest": RandomForestClassifier(
                n_estimators=100, max_depth=7, min_samples_split=4, random_state=self.random_state
            ),
            "Gradient Boosting": GradientBoostingClassifier(
                n_estimators=100, learning_rate=0.08, max_depth=3, random_state=self.random_state
            )
        }
        
        print("\n" + "="*75)
        print("[PELATIHAN & EVALUASI MODEL PREDICTIVE MAINTENANCE]")
        print("="*75)
        
        for name, model in self.models.items():
            print(f"\n--- Pelatihan Model: {name} ---")
            model.fit(self.X_train_scaled, self.y_train)
            
            # Prediksi Train & Test
            train_preds = model.predict(self.X_train_scaled)
            test_preds = model.predict(self.X_test_scaled)
            
            # Metrik Evaluasi Data Test
            prec = precision_score(self.y_test, test_preds, zero_division=0)
            rec = recall_score(self.y_test, test_preds, zero_division=0)
            f1 = f1_score(self.y_test, test_preds, zero_division=0)
            test_acc = accuracy_score(self.y_test, test_preds)
            train_acc = accuracy_score(self.y_train, train_preds)
            train_f1 = f1_score(self.y_train, train_preds, zero_division=0)
            
            # Selisih / Gap untuk analisis Overfitting
            acc_gap = (train_acc - test_acc) * 100
            f1_gap = (train_f1 - f1) * 100
            
            cm = confusion_matrix(self.y_test, test_preds)
            
            self.evaluation_results.append({
                "Model": name,
                "Test_Accuracy": test_acc,
                "Precision": prec,
                "Recall": rec,
                "F1_Score": f1,
                "Train_Accuracy": train_acc,
                "Acc_Overfit_Gap": acc_gap,
                "F1_Overfit_Gap": f1_gap,
                "Confusion_Matrix": cm
            })
            
            print(f" -> Accuracy (Testing) : {test_acc*100:.2f}%")
            print(f" -> Precision          : {prec*100:.2f}% (Tingkat ketepatan alarm kerusakan)")
            print(f" -> Recall             : {rec*100:.2f}% (Kemampuan mendeteksi mesin yang rusak)")
            print(f" -> F1-Score           : {f1*100:.2f}% (Keseimbangan Precision & Recall)")
            print(f" -> Confusion Matrix   : TN={cm[0,0]}, FP={cm[0,1]}, FN={cm[1,0]}, TP={cm[1,1]}")
            print(f" -> Analisis Overfit   : Train Acc = {train_acc*100:.2f}% vs Test Acc = {test_acc*100:.2f}% (Gap: {acc_gap:+.2f}%)")
            
            if acc_gap < 5.0:
                print("    [STATUS GENERALISASI] Optimal: Model stabil tanpa indikasi overfitting signifikan.")
            else:
                print("    [STATUS GENERALISASI] Waspada: Terdeteksi gejala overfitting sedang.")
                
        return pd.DataFrame(self.evaluation_results).drop(columns=["Confusion_Matrix"])

    def plot_evaluation(self, output_path="outputs/predictive_maintenance_eval.png"):
        """Visualisasi perbandingan metrik evaluasi dan kurva train vs test."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df_res = pd.DataFrame(self.evaluation_results)
        models = df_res["Model"]
        x = np.arange(len(models))
        width = 0.2
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Subplot 1: Metrik Kinerja Testing
        ax1 = axes[0]
        ax1.bar(x - width, df_res["Precision"]*100, width, label="Precision", color="#3a86ff")
        ax1.bar(x, df_res["Recall"]*100, width, label="Recall", color="#ff006e")
        ax1.bar(x + width, df_res["F1_Score"]*100, width, label="F1-Score", color="#8338ec")
        ax1.set_title("Metrik Evaluasi Uji (Precision, Recall, F1)", fontsize=11, fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(models)
        ax1.set_ylabel("Persentase (%)")
        ax1.set_ylim(0, 105)
        ax1.legend()
        ax1.grid(axis="y", linestyle="--", alpha=0.6)
        
        # Subplot 2: Train vs Test Accuracy (Deteksi Overfitting)
        ax2 = axes[1]
        ax2.bar(x - width/2, df_res["Train_Accuracy"]*100, width, label="Training Accuracy", color="#06d6a0")
        ax2.bar(x + width/2, df_res["Test_Accuracy"]*100, width, label="Testing Accuracy", color="#ffd166")
        ax2.set_title("Analisis Overfitting: Training vs Testing Accuracy", fontsize=11, fontweight="bold")
        ax2.set_xticks(x)
        ax2.set_xticklabels(models)
        ax2.set_ylabel("Akurasi (%)")
        ax2.set_ylim(0, 105)
        ax2.legend()
        ax2.grid(axis="y", linestyle="--", alpha=0.6)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=200)
        plt.close()
        print(f"\n[VISUALISASI] Grafik evaluasi kinerja model disimpan ke: {output_path}")

def main():
    print("=" * 80)
    print("  STUDI KASUS SESI IV: PREDICTIVE MAINTENANCE IoT MESIN INDUSTRI")
    print("  Machine Learning Engineering: Random Forest vs Gradient Boosting")
    print("=" * 80)
    
    pipeline = PredictiveMaintenancePipeline()
    pipeline.prepare_data()
    summary = pipeline.train_and_evaluate_models()
    pipeline.plot_evaluation()
    print("\n[SELESAI] Pipeline Predictive Maintenance Sesi IV berhasil dijalankan.")

if __name__ == "__main__":
    main()
