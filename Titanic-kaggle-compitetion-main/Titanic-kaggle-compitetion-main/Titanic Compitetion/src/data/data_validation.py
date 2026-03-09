import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger("DataValidator")

class DataValidator:
    """Class to validate incoming dataset for training or inference"""
    
    def __init__(self, expected_columns: list, target_col: str):
        self.expected_columns = expected_columns
        self.target_col = target_col
        
    def validate(self, df: pd.DataFrame, is_training: bool = True) -> bool:
        """Runs validation checks on the dataframe"""
        
        # Check standard columns exist
        for col in self.expected_columns:
            if col not in df.columns:
                logger.error(f"Missing expected column: {col}")
                return False
        
        # Check target col exists for training data
        if is_training and self.target_col not in df.columns:
            logger.error(f"Missing target column: {self.target_col} for training")
            return False
            
        # Check for empty dataframe
        if df.empty:
            logger.error(f"DataFrame is empty")
            return False
        
        logger.info("Data validation completed successfully")
        return True
