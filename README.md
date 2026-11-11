# Coral Bleaching Predictor: Flask + XGBoost Web App

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-Classifier-orange.svg)
![Machine_Learning](https://img.shields.io/badge/Machine-Learning-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A locally hosted **Flask** web application that predicts the risk of **coral bleaching** using an **XGBoost** classifier trained on a global coral-monitoring dataset. The app serves a six-parameter environmental form and returns a classification (`0` = healthy reef, `1` = bleaching risk) alongside the input profile, feature importances, and dataset/model provenance.

## 📌 Project Overview & Engineering Highlights

This project simulates a reef survey: the user enters six ocean-environmental measurements, and the model estimates whether the reef is under bleaching stress.

- 🌊 **Environmental Input Model**: Six numeric features — `Temperature_Mean` (Kelvin), `SSTA`, `SSTA_DHW`, `TSA_DHW`, `Windspeed`, `Depth_m` — captured in the exact order expected by the trained model.
- 🌡️ **Heat-Stress Features**: Sea Surface Temperature Anomaly and Degree Heating Weeks (`SSTA`, `SSTA_DHW`, `TSA_DHW`) encode the thermal stress that drives bleaching events.
- 🧠 **Gradient-Boosted Classifier**: XGBoost (`n_estimators=200`, `max_depth=6`, `learning_rate=0.05`) with `scale_pos_weight` to counter class imbalance, evaluated on a temporal hold-out split.
- 📊 **Real-Time Glassmorphism Dashboard**: A vanilla HTML/CSS/JS interface with a classification gauge, a six-axis radar chart (input vs. dataset median), and feature-importance bars — all updated via `fetch` with no page reload.
- 🌐 **Bilingual UI (ID / EN)**: Full internationalization through a `data-i18n` attribute system and a JavaScript dictionary, with the choice persisted in `localStorage`.

## 📈 Prediction Output & Model Behavior

Based on the trained model and the temporal hold-out evaluation:

1. **Healthy vs. Bleaching**: The model returns `status: "safe"` (`prediction = 0`) or `status: "danger"` (`prediction = 1`). The UI renders this on a two-zone gauge.
2. **Balanced but Limited**: Test accuracy is **64.2%** with an F1 of **52.3%** on the bleaching (minority) class — the model recognizes non-bleaching conditions more reliably than bleaching events.
3. **Feature Influence**: Depth (25.8%) and mean temperature (24.0%) are the strongest drivers, followed by thermal-stress weeks and wind speed.

## 🛠️ Tech Stack & Requirements

| Layer | Technology |
| --- | --- |
| Backend | Flask, joblib, NumPy |
| Model | XGBoost (scikit-learn API) |
| Training | pandas, scikit-learn |
| Frontend | HTML, CSS, JavaScript (vanilla, no framework) |

- **Environment**: Python 3.10+, Flask 3.1
- **Dependencies**: see [`requirements.txt`](requirements.txt)

## 🚀 Quick Start

To run the prediction server locally:

1. (Optional) create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   # source .venv/bin/activate   # macOS / Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open <http://127.0.0.1:5000>.

The model `xgboost_coral_model.pkl` is included, so the app runs out of the box. To retrain, place the dataset (see [Dataset](#-dataset)) in the project root and run `python train.py`.

## 🧱 Project Structure

```
.
├── app.py                        # Flask server (/ and /predict routes)
├── train.py                      # XGBoost training script
├── xgboost_coral_model.pkl       # Trained model (loaded by app.py)
├── requirements.txt
├── templates/
│   └── index.html                # UI + frontend logic & i18n
└── static/
    ├── style.css
    └── img/
        ├── reef-wide.jpg
        └── reef-tall.jpg
```

## 🔌 API

### `POST /predict`

JSON body with six parameters:

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

Response:

```json
{
  "prediction": 0,
  "label": "Aman: Kondisi Karang Sehat",
  "status": "safe"
}
```

`status` is `safe` (prediction `0`) or `danger` (prediction `1`). If the input is missing or invalid, the server returns `400` with `{"error": "..."}`.

> The feature order must match `FEATURES` in `app.py` and `train.py` exactly — XGBoost does not store column names.

## 🧪 Model

| Item | Value |
| --- | --- |
| Algorithm | XGBoost Classifier |
| Configuration | `n_estimators=200`, `max_depth=6` |
| Learning rate | `0.05`, `eval_metric='logloss'` |
| Class balancing | `scale_pos_weight` (class ratio) |
| Data split | Train: year `< 2015` · Test: year `>= 2015` |
| Sample count | 25,355 train · 7,361 test |
| Test accuracy | 64.2% |
| Bleaching-class F1 | 52.3% |

Target: `Bleaching_Occurred = 1` when `Percent_Bleaching > 0`.

Feature importance (`model.feature_importances_`, normalized):

| Feature | Weight |
| --- | --- |
| Depth | 25.8% |
| Temperature Mean | 24.0% |
| TSA DHW | 19.9% |
| Windspeed | 12.0% |
| SSTA DHW | 10.1% |
| SSTA | 8.2% |

## 📂 Dataset

The dataset is **not included** in this repository due to its size. To retrain the model, place `global_bleaching_environmental.csv` in the project root.

| Item | Detail |
| --- | --- |
| File | `global_bleaching_environmental.csv` |
| Source | BCO-DMO (Biological and Chemical Oceanography Data Management Office) |
| Data merge | NOAA sea surface temperature satellite data |
| Period | 1980 – 2020 |
| Total records | 41,361 rows |
| Records used | 32,716 rows (after cleaning) |
| Coverage | 91 countries · 5 oceans |
| Field contributors | Reef Check, Donner, AGRRA, FRRP, Kumagai, etc. |
| Target definition | `Percent_Bleaching > 0` → bleaching |

Environmental columns used: `Temperature_Mean` (Kelvin), `SSTA`, `SSTA_DHW`, `TSA_DHW`, `Windspeed`, `Depth_m`.

> **Unit note:** `Temperature_Mean` is in **Kelvin** (data range 290.9 – 303.5 K), not Celsius.

## ⚠️ Notes & Limitations

- Predictions are **estimates** from a machine-learning model and are **not a replacement for field observation**.
- Model accuracy is limited (64.2%), with a minority-class F1 of 52.3% — the model detects non-bleaching conditions better than bleaching events.
- All UI values (ranges, medians, presets) are derived from real dataset statistics, not hard-coded guesses.
- Statistics on the "Model & Data Source" card are computed from the same dataset and model.

## 📄 License

MIT. Add a `LICENSE` file at the project root if the repository is published further.
