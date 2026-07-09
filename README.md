# Implementasi Transfer Learning MobileNetV2 untuk Klasifikasi Penyakit Daun Teh

Proyek ini adalah implementasi *Transfer Learning* menggunakan arsitektur **MobileNetV2** untuk mengklasifikasikan 6 jenis penyakit pada daun teh, yang dibangun menjadi aplikasi *web* berbasis **Flask**. Proyek ini dibuat untuk memenuhi persyaratan tugas kuliah *Computer Vision* / AI.

## Fitur
1. **Klasifikasi Penyakit Daun Teh**: Mendukung 6 kelas (Algal Spot, Brown Blight, Gray Blight, Healthy, Helopeltis, Red Spot).
2. **Transfer Learning & Fine Tuning**: Menggunakan MobileNetV2 pre-trained pada ImageNet.
3. **Aplikasi Web Flask**: Antarmuka modern yang responsif (dibangun dengan Bootstrap 5) dengan nuansa warna hijau teh.
4. **Riwayat Prediksi**: Menyimpan riwayat hasil prediksi menggunakan *database* SQLite.
5. **Informasi Penyakit**: Halaman khusus untuk mengetahui detail setiap penyakit dan cara penanganannya.

## Dataset
Dataset yang digunakan terdiri dari 5867 gambar dengan kelas berikut:
- `algal_spot` (1000 gambar)
- `brown_blight` (867 gambar)
- `gray_blight` (1000 gambar)
- `healthy` (1000 gambar)
- `helopeltis` (1000 gambar)
- `red_spot` (1000 gambar)

Pastikan dataset Anda diekstrak di path `dataset/Tea_Leaf_Disease/`.

## Instalasi

1. **Clone repositori ini atau ekstrak folder proyek.**
2. **Buka terminal dan arahkan ke direktori proyek.**
3. **Buat virtual environment (opsional namun disarankan):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
4. **Instal dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

## Cara Training Model (Opsional)
Jika Anda ingin melatih ulang model:
1. Pastikan dataset sudah berada di `dataset/Tea_Leaf_Disease/`.
2. Jalankan perintah berikut di terminal:
   ```bash
   python train.py
   ```
3. Proses ini akan menyimpan model di folder `model/` dengan nama `tea_leaf_mobilenetv2.keras`. Selain itu, akan dihasilkan plot *Loss* dan *Accuracy*, serta tercetak *Confusion Matrix* di konsol.

## Cara Menjalankan Aplikasi Web
Setelah model terlatih atau file `tea_leaf_mobilenetv2.keras` tersedia di folder `model/`:
1. Jalankan aplikasi Flask:
   ```bash
   python app.py
   ```
2. Buka *browser* dan akses URL yang diberikan, biasanya: `http://127.0.0.1:5000/`.
3. Bisa di jalankan melalui online Buka *browser* dan akses URL ini https://web-production-4cd3a.up.railway.app/ 

## Deployment
Proyek ini sudah dilengkapi dengan `requirements.txt`, `runtime.txt`, dan `Procfile`.
- **Render / Heroku**: Anda dapat melakukan *deploy* langsung dengan menghubungkan akun GitHub Anda. Pastikan *Build Command* di set ke `pip install -r requirements.txt` dan *Start Command* ke `gunicorn app:app`.
- **PythonAnywhere**: Upload semua file melalui FTP atau *Web Console*, buat sebuah *Web App* berbasis Flask, pastikan *virtualenv* terinstal dari `requirements.txt`, lalu sesuaikan konfigurasi *WSGI file* untuk menunjuk ke `app:app`.
