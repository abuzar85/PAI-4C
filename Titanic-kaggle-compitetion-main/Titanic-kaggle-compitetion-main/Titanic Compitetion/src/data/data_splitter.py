import pandas as pd
from sklearn.model_selection import train_test_split
from src.utils.logger import setup_logger

logger = setup_logger("DataSplitter")

class DataSplitter:
    """Class to split dataset into training and testing sets"""
    
    def __init__(self, test_size: float = 0.2, random_seed: int = 42):
        self.test_size = test_size
        self.random_seed = random_seed
        
    def split(self, df: pd.DataFrame, target_col: str):
        """Perform train-test split"""
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_seed, stratify=y
        )
        
        logger.info(f"Data split into: Train: {X_train.shape}, Test: {X_test.shape}")
        return X_train, X_test, y_train, y_test
