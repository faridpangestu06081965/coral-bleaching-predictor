# Coral Bleaching Predictor

Aplikasi web lokal berbasis **Flask** untuk memprediksi risiko **pemutihan terumbu karang (coral bleaching)** menggunakan model **XGBoost** yang dilatih dari data pemantauan karang global.

Antarmuka menyediakan formulir enam parameter lingkungan, lalu menampilkan hasil klasifikasi (`0` = karang sehat, `1` = potensi memutih) beserta profil parameter, tingkat kepentingan fitur, dan keterangan sumber data.

## Fitur

- **Prediksi real-time** lewat `fetch` API tanpa reload halaman
- **Gauge klasifikasi** dua zona (Sehat / Memutih)
- **Radar profil parameter** — membandingkan input pengguna dengan median dataset latih
- **Tingkat kepentingan fitur** dari `model.feature_importances_`
- **Preset input** (Karang Sehat, Stres Panas, Perairan Dalam) yang diambil dari nilai nyata dataset
- **Dua bahasa** (Indonesia / Inggris) dengan pilihan tersimpan di `localStorage`
- **Desain responsif** — glassmorphism di atas latar foto terumbu karang
- Menghormati `prefers-reduced-motion` dan mendukung navigasi keyboard

## Teknologi

| Lapisan | Teknologi |
| --- | --- |
| Backend | Flask, joblib, NumPy |
| Model | XGBoost (scikit-learn API) |
| Pelatihan | pandas, scikit-learn |
| Frontend | HTML, CSS, JavaScript (vanilla, tanpa framework) |

## Struktur Proyek

```
.
├── app.py                        # Server Flask (rute / dan /predict)
├── train.py                      # Skrip pelatihan model XGBoost
├── xgboost_coral_model.pkl       # Model terlatih (dimuat oleh app.py)
├── requirements.txt
├── templates/
│   └── index.html                # UI + logika frontend & i18n
└── static/
    ├── style.css
    └── img/
        ├── reef-wide.jpg
        └── reef-tall.jpg
```

## Menjalankan

```bash
# 1. (Opsional) buat virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 2. Pasang dependensi
pip install -r requirements.txt

# 3. Jalankan server
python app.py
```

Buka <http://127.0.0.1:5000>.

Model `xgboost_coral_model.pkl` sudah disertakan, jadi aplikasi bisa langsung dijalankan. Untuk melatih ulang, ikuti bagian [Dataset](#dataset) di bawah lalu jalankan `python train.py`.

## API

### `POST /predict`

Body JSON dengan enam parameter:

```json
{
  "Temperature_Mean": 301.11,
  "SSTA": 0.16,
  "SSTA_DHW": 1.11,
  "TSA_DHW": 0.0,
  "Windspeed": 5.0,
  "Depth_m": 5.0
}
```

Respons:

```json
{
  "prediction": 0,
  "label": "Aman: Kondisi Karang Sehat",
  "status": "safe"
}
```

`status` bernilai `safe` (prediksi `0`) atau `danger` (prediksi `1`). Jika input tidak lengkap atau tidak valid, server mengembalikan `400` dengan `{"error": "..."}`.

> Urutan fitur harus persis seperti di `app.py` (`FEATURES`) dan `train.py` — XGBoost tidak menyimpan nama kolom.

## Model

| Item | Nilai |
| --- | --- |
| Algoritma | XGBoost Classifier |
| Konfigurasi | `n_estimators=200`, `max_depth=6` |
| Learning rate | `0.05`, `eval_metric='logloss'` |
| Penyeimbangan kelas | `scale_pos_weight` (rasio kelas) |
| Pembagian data | Latih: tahun `< 2015` · Uji: tahun `>= 2015` |
| Jumlah data | 25.355 latih · 7.361 uji |
| Akurasi uji | 64.2% |
| F1 kelas pemutihan | 52.3% |

Target: `Bleaching_Occurred = 1` bila `Percent_Bleaching > 0`.

Tingkat kepentingan fitur (`model.feature_importances_`, ternormalisasi):

| Fitur | Bobot |
| --- | --- |
| Depth | 25.8% |
| Temperature Mean | 24.0% |
| TSA DHW | 19.9% |
| Windspeed | 12.0% |
| SSTA DHW | 10.1% |
| SSTA | 8.2% |

## Dataset

Dataset **tidak disertakan** di repo ini karena berukuran besar. Untuk melatih ulang model, letakkan berkas `global_bleaching_environmental.csv` di direktori akar proyek.

| Item | Keterangan |
| --- | --- |
| Berkas | `global_bleaching_environmental.csv` |
| Sumber | BCO-DMO (Biological and Chemical Oceanography Data Management Office) |
| Penggabungan data | Data satelit suhu permukaan laut NOAA |
| Periode | 1980 – 2020 |
| Total rekaman | 41.361 baris |
| Rekaman terpakai | 32.716 baris (setelah pembersihan) |
| Cakupan | 91 negara · 5 samudra |
| Kontributor lapangan | Reef Check, Donner, AGRRA, FRRP, Kumagai, dll. |
| Definisi target | `Percent_Bleaching > 0` → pemutihan |

Kolom lingkungan yang dipakai: `Temperature_Mean` (Kelvin), `SSTA`, `SSTA_DHW`, `TSA_DHW`, `Windspeed`, `Depth_m`.

> **Catatan satuan:** `Temperature_Mean` berada dalam **Kelvin** (rentang data 290.9 – 303.5 K), bukan Celsius.

## Catatan & Keterbatasan

- Hasil prediksi bersifat **estimasi** dari model machine learning dan **bukan pengganti pengamatan lapangan**.
- Akurasi model terbatas (64.2%), dengan F1 kelas minoritas 52.3% — model cenderung lebih baik mengenali kondisi tanpa pemutihan.
- Nilai validasi UI (rentang, median, preset) diambil dari statistik nyata dataset, bukan angka yang dikarang.
- Statistik pada kartu "Keterangan Model & Sumber Data" dihitung dari dataset dan model yang sama.

## Lisensi

Belum ditentukan. Tambahkan berkas `LICENSE` jika proyek ini akan dipublikasikan lebih lanjut.
