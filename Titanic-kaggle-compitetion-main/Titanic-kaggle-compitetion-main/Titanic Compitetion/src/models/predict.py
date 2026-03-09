import pandas as pd
import joblib
import os
from src.utils.logger import setup_logger

logger = setup_logger("Predictor")

class Predictor:
    """Class to handle Kaggle submission generation"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            logger.error(f"No model found at {model_path}. Predictor will fail.")
            
    def generate_submission(self, X_test: pd.DataFrame, passenger_ids: pd.Series, output_path: str = "data/processed/submission.csv"):
        """Perform predictions and save to submission format"""
        if not self.model:
            logger.error("Model not available for predictions.")
            return None
        
        logger.info(f"Generating predictions for {len(X_test)} passengers...")
        y_pred = self.model.predict(X_test)
        
        # Format as Kaggle submission
        submission_df = pd.DataFrame({
            "PassengerId": passenger_ids,
            "Transported": y_pred.astype(bool)
        })
        
        submission_df.to_csv(output_path, index=False)
        logger.info(f"Kaggle submission saved to {output_path}")
        return submission_df
