import pandas as pd
import logging
import os

class DataLoader:
    """
    Class to handle data loading from CSV files.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    def load_data(self) -> pd.DataFrame:
        self.logger.info(f"Loading data from {self.file_path}...")
        if not os.path.exists(self.file_path):
            self.logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"The path {self.file_path} does not exist.")
        
        df = pd.read_csv(self.file_path)
        self.logger.info(f"Successfully loaded data with shape {df.shape}")
        return df
