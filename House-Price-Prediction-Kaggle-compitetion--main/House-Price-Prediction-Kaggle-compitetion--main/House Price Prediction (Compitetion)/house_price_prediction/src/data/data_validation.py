import pandas as pd
import logging

class DataValidator:
    """
    Class to validate the integrity and schema of the data.
    """
    def __init__(self, expected_columns):
        self.expected_columns = expected_columns
        self.logger = logging.getLogger(__name__)

    def validate(self, df: pd.DataFrame) -> bool:
        self.logger.info("Validating data schema...")
        
        # Check if all expected columns exist
        missing_cols = [col for col in self.expected_columns if col not in df.columns]
        if missing_cols:
            self.logger.error(f"Missing columns: {missing_cols}")
            return False
            
        # Check for null values
        null_counts = df.isnull().sum().sum()
        if null_counts > 0:
            self.logger.warning(f"Found {null_counts} null values in the dataset.")
            
        self.logger.info("Data validation successful.")
        return True
