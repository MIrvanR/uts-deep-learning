# SESI VI: Klasifikasi Tutupan Lahan Pertanian Menggunakan CNN Sederhana (Remote Sensing AI)

Implementasi model *Deep Learning* berbasis arsitektur **Convolutional Neural Network (CNN)** menggunakan pustaka **PyTorch** untuk mendeteksi dan mengklasifikasikan kategori tutupan lahan (*Land Cover Classification*) dari citra satelit mikro (*patch*) guna memantau deforestasi dan atribusi lahan pertanian.

## 🛰️ Arsitektur Model CNN Kustom
- **Blok Konvolusi 1**:
  - `Conv2d` (3 channel input RGB $\rightarrow$ 32 channel output, kernel $3\times3$, padding 1)
  - `BatchNorm2d` (32)
  - Aktivasi `ReLU`
  - `MaxPool2d` (kernel $2\times2$, stride 2) $\rightarrow$ Output spasial $16\times16$
- **Blok Konvolusi 2**:
  - `Conv2d` (32 $\rightarrow$ 64 channel output, kernel $3\times3$, padding 1)
  - `BatchNorm2d` (64)
  - Aktivasi `ReLU`
  - `MaxPool2d` (kernel $2\times2$, stride 2) $\rightarrow$ Output spasial $8\times8$
- **Blok Fully Connected (Dense)**:
  - `Flatten` ($64 \times 8 \times 8 = 4.096$ fitur)
  - `Linear` ($4.096 \rightarrow 128$)
  - `ReLU` & `Dropout` ($p=0.30$)
  - `Linear` ($128 \rightarrow 4$ kelas)

## 🌾 Kategori Tutupan Lahan
1. **Kelas 0 - Hutan Primer / Alami**: Vegetasi kanopi lebat dengan nilai reflektansi hijau gelap & NIR tinggi.
2. **Kelas 1 - Lahan Pertanian & Sawit**: Pola spektral hijau terang dengan tekstur larikan tanaman budidaya.
3. **Kelas 2 - Badan Air / Sungai**: Danau atau sungai dengan tingkat serapan cahaya tinggi (reflektansi rendah).
4. **Kelas 3 - Lahan Terbangun / Terbuka**: Area pemukiman, infrastruktur jalan, atau tanah terbuka (*bare soil*).

## 📊 Optimalisasi Pembelajaran
- **Loss Function**: `nn.CrossEntropyLoss()`
- **Optimizer**: `optim.Adam(lr=0.001)`
- **Validasi Evaluasi**: Uji akurasi otomatis pada data pengujian (*Test Set*) di setiap akhir *epoch*.

## 🚀 Cara Menjalankan
```bash
pip install -r requirements.txt
python land_cover_cnn.py
```
Grafik kurva pembelajaran (*Loss* & *Accuracy*) akan otomatis tersimpan di `outputs/cnn_training_performance.png`.
