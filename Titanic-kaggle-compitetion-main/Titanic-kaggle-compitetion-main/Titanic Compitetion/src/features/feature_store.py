import pandas as pd
import os
from src.utils.logger import setup_logger

logger = setup_logger("FeatureStore")

class FeatureStore:
    """Class to store and retrieve engineered features locally"""
    
    def __init__(self, storage_path: str = "data/processed/"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            
    def store_features(self, df: pd.DataFrame, feature_set_name: str):
        """Save feature set to parquet or csv"""
        path = os.path.join(self.storage_path, f"{feature_set_name}.parquet")
        df.to_parquet(path, index=False)
        logger.info(f"Stored features to {path}")
        
    def retrieve_features(self, feature_set_name: str) -> pd.DataFrame:
        """Load feature set from local storage"""
        path = os.path.join(self.storage_path, f"{feature_set_name}.parquet")
        if os.path.exists(path):
            df = pd.read_parquet(path)
            logger.info(f"Retrieved features from {path}")
            return df
        else:
             logger.error(f"Feature set {feature_set_name} not found")
             return None
