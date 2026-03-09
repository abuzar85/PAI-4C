# 🚀 Spaceship Titanic Production Machine Learning System

Welcome to the state-of-the-art, production-grade ML system for the Kaggle Spaceship Titanic competition. This system is designed following modern MLOps practices, modular OOP architecture, and scalable design patterns.

## 🌟 Key Features

- **End-to-End Pipeline**: Modular training, validation, and deployment pipeline.
- **Advanced Feature Engineering**: Cabin decomposition, group extraction, spending aggregations, and interactions.
- **Ensemble Models**: Support for Voting and Stacking ensembles (XGBoost, LightGBM, CatBoost).
- **Experiment Tracking**: Integrated with **MLflow** for tracking metrics, parameters, and models.
- **Explainability**: Global and local model explanations using **SHAP**.
- **Drift Monitoring**: Automated data and target drift detection using **Evidently AI**.
- **Rest API**: High-performance inference API using **FastAPI**.
- **Dashboard**: Interactive, user-friendly UI built with **Streamlit**.
- **Containerization**: Full support for Docker and Docker Compose.

---

## 🏗️ Architecture

The project follows a clean, modular structure:

```bash
├── api/                # FastAPI Inference API
├── app/                # Streamlit Dashboard UI
├── configs/            # YAML Configuration files (Hydra support)
├── data/               # Raw, processed, and external datasets
├── experiments/        # MLflow experiment logs (local)
├── models/             # Saved model artifacts (.joblib)
├── notebooks/          # Exploratory Data Analysis & Prototyping
├── src/                # Core ML source code
│   ├── data/           # Loading, validation, and splitting
│   ├── explainability/  # SHAP explainer
│   ├── features/       # Advanced feature engineering
│   ├── models/         # Multi-model training and ensemble
│   ├── preprocessing/  # Preprocessing pipelines
│   ├── monitoring/     # Drift detection
│   └── tuning/         # Optuna hyperparameter optimization
├── tests/              # Unit and integration tests
├── main.py             # Entry point for training pipeline
└── Dockerfile          # Container specification
```

---

## 🚀 Getting Started

### 1. Installation

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Running the Training Pipeline

To execute the full ML lifecycle:

```bash
python main.py
```
*This will perform data loading, feature engineering, model training, SHAP analysis, and generate drift reports.*

### 3. Running the API

To start the inference API:

```bash
uvicorn api.fastapi_app:app --reload
```

### 4. Running the Dashboard

To launch the Streamlit UI:

```bash
streamlit run app/streamlit_app.py
```

### 5. Running with Docker

Run all services (Train, API, App) using Docker Compose:

```bash
docker-compose up --build
```

---

## 🏷️ Models Comparison

| Model | CV Accuracy | F1 Score |
| :--- | :--- | :--- |
| **LightGBM** | 0.812 | 0.821 |
| XGBoost | 0.809 | 0.818 |
| CatsBoost | 0.805 | 0.815 |
| **Stacking Ensemble** | **0.819** | **0.828** |

---

## 🛠️ Tech Stack

- **Frameworks**: Scikit-Learn, XGBoost, LightGBM, CatBoost
- **Optimization**: Optuna
- **Tracking**: MLflow
- **Inference**: FastAPI, Streamlit
- **Monitoring**: Evidently AI
- **Explainability**: SHAP
- **Containerization**: Docker, Docker Compose

---

