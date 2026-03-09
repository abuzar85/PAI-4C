import pandas as pd
import logging

class DataCleaner:
    """
    Class to handle data cleaning operations.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Starting data cleaning...")
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        if len(df) < initial_count:
            self.logger.info(f"Removed {initial_count - len(df)} duplicate rows.")

        # Strip whitespaces from strings
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        self.logger.info("Data cleaning completed.")
        return df
