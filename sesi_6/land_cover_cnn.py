"""
land_cover_cnn.py
Deep Learning untuk Penginderaan Jauh (Remote Sensing):
Klasifikasi Tutupan Lahan Pertanian Menggunakan Convolutional Neural Network (CNN)

Komponen Utama:
1. Arsitektur CNN Kustom (Conv2D, ReLU, Max Pooling, Fully Connected) menggunakan PyTorch
2. Dataset Citra Mikro / Patch Satelit Tutupan Lahan (4 Kategori: Hutan, Pertanian, Air, Lahan Terbuka)
3. Fungsi Training Loop Lengkap dengan Optimizer Adam & Loss Function CrossEntropyLoss
4. Fungsi Evaluasi / Validasi Akurasi pada Data Uji (Test Set)
5. Visualisasi Metrik Performa Pembelajaran

SESI VI: Deforestation Alerts and Driver Attribution with Remote Sensing and AI
Judul: Klasifikasi Tutupan Lahan Pertanian Menggunakan CNN Sederhana
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Definisi Arsitektur CNN Kustom menggunakan torch.nn
class LandCoverCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(LandCoverCNN, self).__init__()
        
        # Blok Konvolusi 1
        # Input: [Batch, 3, 32, 32] -> Output: [Batch, 32, 16, 16]
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        # Blok Konvolusi 2
        # Input: [Batch, 32, 16, 16] -> Output: [Batch, 64, 8, 8]
        self.conv_block2 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        # Blok Fully Connected (Klasifikasi)
        # 64 channels * 8 * 8 = 4096 fitur
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 128),
            nn.ReLU(),
            nn.Dropout(p=0.30),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        logits = self.classifier(x)
        return logits

# 2. Generator Dataset Citra Patch Satelit Sintetis
class SyntheticSatellitePatchDataset(Dataset):
    """
    Dataset citra mikro/patch satelit sintetis dengan karakteristik spektral realistis:
    - Kelas 0: Hutan Alami / Lebat (Dominan Hijau Gelap / High NIR)
    - Kelas 1: Lahan Pertanian & Sawit (Pola Hijau Terang / Tekstur Baris)
    - Kelas 2: Badan Air / Sungai (Dominan Biru Gelap / Reflektansi Rendah)
    - Kelas 3: Lahan Terbangun / Terbuka (Warna Cokelat / Abu-abu Terang)
    """
    def __init__(self, num_samples=1000, random_seed=42):
        np.random.seed(random_seed)
        self.images = []
        self.labels = []
        
        for _ in range(num_samples):
            cls = np.random.choice([0, 1, 2, 3])
            patch = np.zeros((3, 32, 32), dtype=np.float32)
            noise = np.random.normal(0, 0.05, (3, 32, 32)).astype(np.float32)
            
            if cls == 0:  # Hutan Lebat (Dark Green)
                patch[0, :, :] = 0.15 # Red
                patch[1, :, :] = 0.55 # Green
                patch[2, :, :] = 0.18 # Blue
            elif cls == 1: # Pertanian & Perkebunan (Light Green with crop patterns)
                patch[0, :, :] = 0.35
                patch[1, :, :] = 0.70
                patch[2, :, :] = 0.25
                patch[:, ::4, :] += 0.10 # Pola baris pertanian
            elif cls == 2: # Badan Air (Deep Blue)
                patch[0, :, :] = 0.10
                patch[1, :, :] = 0.25
                patch[2, :, :] = 0.65
            else: # Lahan Terbuka / Bangunan (Brown / Grey)
                patch[0, :, :] = 0.60
                patch[1, :, :] = 0.50
                patch[2, :, :] = 0.38
                
            patch = np.clip(patch + noise, 0.0, 1.0)
            self.images.append(patch)
            self.labels.append(cls)
            
        self.images = torch.tensor(np.array(self.images), dtype=torch.float32)
        self.labels = torch.tensor(self.labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]

# 3. Fungsi Training Loop Lengkap
def train_model(model, train_loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass & Optimize
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
        
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

# 4. Fungsi Validasi & Pengujian Akurasi
def validate_model(model, val_loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            
    val_loss = running_loss / total
    val_acc = correct / total
    return val_loss, val_acc

# 5. Visualisasi Metrik Performa Pembelajaran
def plot_training_history(history, output_path="outputs/cnn_training_performance.png"):
    epochs = range(1, len(history["train_loss"]) + 1)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    
    # Subplot 1: Loss
    axes[0].plot(epochs, history["train_loss"], "r-o", label="Training Loss")
    axes[0].plot(epochs, history["val_loss"], "b--s", label="Validation Loss")
    axes[0].set_title("Grafik CrossEntropy Loss per Epoch", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.6)
    
    # Subplot 2: Accuracy
    axes[1].plot(epochs, [a * 100 for a in history["train_acc"]], "g-o", label="Train Accuracy (%)")
    axes[1].plot(epochs, [a * 100 for a in history["val_acc"]], "m--s", label="Validation Accuracy (%)")
    axes[1].set_title("Grafik Akurasi Model Klasifikasi Tutupan Lahan", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Akurasi (%)")
    axes[1].set_ylim(40, 105)
    axes[1].legend(loc="lower right")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"\n[VISUALISASI] Kurva pelatihan CNN berhasil disimpan ke: {output_path}")

def main():
    print("=" * 80)
    print("  STUDI KASUS SESI VI: KLASIFIKASI TUTUPAN LAHAN DENGAN CNN (PYTORCH)")
    print("  Deep Learning: Remote Sensing Land Cover Classification (Adam + CrossEntropy)")
    print("=" * 80)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[DEVICE] Menggunakan perangkat akselerasi komputasi: {device}")
    
    # Siapkan Dataset (80% Train, 20% Test)
    full_dataset = SyntheticSatellitePatchDataset(num_samples=1200, random_seed=42)
    train_size = int(0.80 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    print(f"\n[DATASET] Dataset Citra Satelit Berhasil Dibagi:")
    print(f" -> Data Latih (Train Set): {len(train_dataset)} patch citra")
    print(f" -> Data Uji   (Test Set) : {len(test_dataset)} patch citra")
    print(f" -> Kelas Target: 0 (Hutan), 1 (Pertanian), 2 (Air), 3 (Lahan Terbuka)")
    
    # Inisialisasi Model, Loss Function, dan Optimizer
    model = LandCoverCNN(num_classes=4).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print("\n--- Ringkasan Arsitektur Model CNN ---")
    print(model)
    
    # Training Loop (10 Epochs)
    num_epochs = 10
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    
    print("\n" + "="*70)
    print("MULAI PROSES PELATIHAN MODEL CNN (TRAINING LOOP)")
    print("="*70)
    
    for epoch in range(1, num_epochs + 1):
        tr_loss, tr_acc = train_model(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = validate_model(model, test_loader, criterion, device)
        
        history["train_loss"].append(tr_loss)
        history["train_acc"].append(tr_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        
        print(f"Epoch [{epoch:02d}/{num_epochs:02d}] | Train Loss: {tr_loss:.4f} | Train Acc: {tr_acc*100:6.2f}% | Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:6.2f}%")
        
    # Evaluasi Akhir
    final_test_loss, final_test_acc = validate_model(model, test_loader, criterion, device)
    print("\n" + "="*70)
    print(f"[HASIL AKHIR EVALUASI DATA UJI] Akurasi Validasi Model: {final_test_acc*100:.2f}%")
    print("="*70)
    
    # Simpan Visualisasi & Model Weights
    plot_training_history(history)
    model_save_path = "outputs/land_cover_cnn.pth"
    torch.save(model.state_dict(), model_save_path)
    print(f"[MODEL SAVED] Bobot model terlatih berhasil disimpan ke: {model_save_path}")
    print("\n[SELESAI] Eksperimen Deep Learning Sesi VI berhasil diselesaikan.")

if __name__ == "__main__":
    main()
