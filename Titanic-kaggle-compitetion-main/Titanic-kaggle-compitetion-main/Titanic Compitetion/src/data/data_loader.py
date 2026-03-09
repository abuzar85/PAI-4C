import pandas as pd
import numpy as np
import os
from src.utils.logger import setup_logger

logger = setup_logger("DataLoader")

class DataLoader:
    """Class to load titanic dataset"""
    
    def __init__(self, raw_path: str, test_path: str):
        self.raw_path = raw_path
        self.test_path = test_path
        
    def load_train_data(self) -> pd.DataFrame:
        """Load the train data as a dataframe"""
        try:
            if not os.path.exists(self.raw_path):
                raise FileNotFoundError(f"Train data file not found at {self.raw_path}")
            
            df = pd.read_csv(self.raw_path)
            logger.info(f"Loaded train data with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading train data: {e}")
            raise

    def load_test_data(self) -> pd.DataFrame:
        """Load the test data as a dataframe"""
        try:
            if not os.path.exists(self.test_path):
                raise FileNotFoundError(f"Test data file not found at {self.test_path}")
            
            df = pd.read_csv(self.test_path)
            logger.info(f"Loaded test data with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading test data: {e}")
            raise
