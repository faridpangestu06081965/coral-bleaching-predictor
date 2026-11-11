from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Muat model XGBoost sekali saat server dinyalakan (lebih cepat & efisien)
MODEL_PATH = 'xgboost_coral_model.pkl'
model = joblib.load(MODEL_PATH)

# Urutan fitur harus PERSIS sama seperti saat training (lihat train.py)
FEATURES = [
    'Temperature_Mean',
    'SSTA',
    'SSTA_DHW',
    'TSA_DHW',
    'Windspeed',
    'Depth_m',
]


@app.route('/')
def index():
    """Menampilkan halaman utama (form input)."""
    return render_template('index.html', features=FEATURES)


@app.route('/predict', methods=['POST'])
def predict():
    """Menerima 6 input numerik, mengembalikan hasil prediksi dalam JSON."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Data input tidak ditemukan.'}), 400

        # Ambil nilai float sesuai urutan fitur
        values = []
        for feature in FEATURES:
            if feature not in data or data[feature] in (None, ''):
                return jsonify({'error': f'Parameter {feature} wajib diisi.'}), 400
            values.append(float(data[feature]))

        # Bentuk (1, 6) agar sesuai ekspektasi XGBoost
        X_input = np.array([values], dtype=float)

        prediction = int(model.predict(X_input)[0])

        if prediction == 1:
            result = {
                'prediction': 1,
                'label': 'Bahaya: Potensi Pemutihan Karang Tinggi',
                'status': 'danger',
            }
        else:
            result = {
                'prediction': 0,
                'label': 'Aman: Kondisi Karang Sehat',
                'status': 'safe',
            }

        return jsonify(result)

    except (TypeError, ValueError):
        return jsonify({'error': 'Input tidak valid. Masukkan angka yang benar.'}), 400
    except Exception as exc:
        return jsonify({'error': f'Terjadi kesalahan: {exc}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
