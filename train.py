import pandas as pd
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

# 1. Muat Data
print("Memuat dataset...")
df = pd.read_csv('global_bleaching_environmental.csv', low_memory=False)

# 2. Pembersihan Data Target
df['Percent_Bleaching'] = pd.to_numeric(df['Percent_Bleaching'], errors='coerce')
df = df.dropna(subset=['Percent_Bleaching'])

# Batas pemutihan (Tetap > 0 agar perbandingannya adil dengan model sebelumnya)
df['Bleaching_Occurred'] = (df['Percent_Bleaching'] > 0).astype(int)

# 3. Pemilihan Fitur (TAMBAH KEDALAMAN DAN KECEPATAN ANGIN)
features = ['Temperature_Mean', 'SSTA', 'SSTA_DHW', 'TSA_DHW', 'Windspeed', 'Depth_m']

# Paksa semua kolom fitur menjadi angka (ubah 'nd' menjadi NaN)
for col in features:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Hapus baris yang kosong pada fitur-fitur baru ini
df = df.dropna(subset=features + ['Date_Year', 'Bleaching_Occurred'])

# 4. Pembagian Data berdasarkan Tahun
print("Membagi data training dan testing berdasarkan tahun...")
train_df = df[df['Date_Year'] < 2015]
test_df = df[df['Date_Year'] >= 2015]

X_train = train_df[features]
y_train = train_df['Bleaching_Occurred']

X_test = test_df[features]
y_test = test_df['Bleaching_Occurred']

# 5. Pelatihan Model XGBoost (GANTI ALGORITMA)
print("Melatih model XGBoost (Advanced)...")

# Di XGBoost, untuk menangani data imbalanced, kita hitung rasio mayoritas vs minoritas
ratio = float(y_train.value_counts()[0]) / y_train.value_counts()[1]

# Parameter disetel agar model tidak menebak sembarangan (mencegah overfitting)
model = XGBClassifier(
    n_estimators=200, 
    learning_rate=0.05, 
    max_depth=6, 
    scale_pos_weight=ratio, 
    random_state=42,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# 6. Evaluasi Model
print("Mengevaluasi hasil prediksi...\n")
y_pred = model.predict(X_test)

print("=== Laporan Klasifikasi (XGBoost) ===")
print(classification_report(y_test, y_pred))

# Tambahan: Tingkat Kepentingan Fitur
importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print("\n=== Tingkat Kepentingan Fitur ===")
print(importances)
import joblib
# Menyimpan model agar bisa dipanggil oleh website
joblib.dump(model, 'xgboost_coral_model.pkl')
print("Model berhasil disimpan sebagai xgboost_coral_model.pkl")