import sys
import joblib
import pandas as pd
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.features.feature_engineering import FeatureEngineer
from src.utils.logger import setup_logger

logger = setup_logger("FastAPI")

app = FastAPI(title="Spaceship Titanic Predictor API", version="1.0.0")

# Input Schema for the API
class PassengerInfo(BaseModel):
    PassengerId: str
    HomePlanet: str = "Earth"
    CryoSleep: bool = False
    Cabin: str = "B/0/P"
    Destination: str = "TRAPPIST-1e"
    Age: float = 25.0
    VIP: bool = False
    RoomService: float = 0.0
    FoodCourt: float = 0.0
    ShoppingMall: float = 0.0
    Spa: float = 0.0
    VRDeck: float = 0.0
    Name: str = "Unknown"

# Global variables for model and preprocessor
model = None
preprocessor = None
fe = FeatureEngineer()

def load_artifacts():
    global model, preprocessor
    try:
        model_path = PROJECT_ROOT / "models" / "saved_models" / "LightGBM.joblib"
        preprocessor_path = PROJECT_ROOT / "models" / "saved_models" / "preprocessor.joblib"
        
        if model_path.exists():
            model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.warning(f"Model not found at {model_path}")
        
        if preprocessor_path.exists():
            preprocessor = joblib.load(preprocessor_path)
            logger.info(f"Preprocessor loaded from {preprocessor_path}")
        else:
            logger.warning(f"Preprocessor not found at {preprocessor_path}")
            
    except Exception as e:
        logger.error(f"Error loading artifacts: {e}")

# Load artifacts on startup
load_artifacts()

@app.get("/")
def home():
    return {"message": "Welcome to Spaceship Titanic Inference API"}

@app.post("/predict")
def predict_passenger(passenger: PassengerInfo):
    """Predict if a passenger was transported using the full pipeline"""
    
    if model is None or preprocessor is None:
        # Try loading again in case they were just trained
        load_artifacts()
        if model is None or preprocessor is None:
            raise HTTPException(status_code=500, detail="Model or preprocessor not loaded. Train the system first.")
        
    try:
        # 1. Convert input to DataFrame
        # Support both Pydantic v1 and v2
        data_dict = passenger.model_dump() if hasattr(passenger, "model_dump") else passenger.dict()
        input_data = pd.DataFrame([data_dict])
        
        # 2. Feature Engineering
        df_engineered = fe.transform(input_data)
        
        # 3. Drop unnecessary columns (must match training)
        drop_cols = ["PassengerId", "Name", "Cabin", "Group"]
        X = df_engineered.drop(columns=[col for col in drop_cols if col in df_engineered.columns])
        
        # 4. Preprocessing
        X_preprocessed = preprocessor.transform(X)
        
        # 5. Prediction
        prediction = model.predict(X_preprocessed)
        probability = model.predict_proba(X_preprocessed)[:, 1][0]
        
        return {
            "is_transported": bool(prediction[0]),
            "probability": float(probability),
            "passenger_id": passenger.PassengerId
        }
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

