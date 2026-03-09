import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from src.utils.logger import setup_logger

logger = setup_logger("FeatureEngineer")

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Class to perform advanced feature engineering on the spaceship titanic dataset"""
    
    def __init__(self, cabin_col: str = "Cabin", passenger_id_col: str = "PassengerId"):
        self.cabin_col = cabin_col
        self.passenger_id_col = passenger_id_col
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply feature transformations to the dataframe"""
        df = X.copy()
        
        # 1. Cabin decomposition: Side, Deck, Num
        df[self.cabin_col] = df[self.cabin_col].fillna('U/0/U')
        df['CabinSide'] = df[self.cabin_col].apply(lambda x: str(x).split('/')[-1] if '/' in str(x) else 'U')
        df['CabinDeck'] = df[self.cabin_col].apply(lambda x: str(x).split('/')[0] if '/' in str(x) else 'U')
        
        def extract_cabin_num(x):
            try:
                parts = str(x).split('/')
                return int(parts[1]) if len(parts) > 1 else 0
            except (ValueError, IndexError):
                return 0
                
        df['CabinNum'] = df[self.cabin_col].apply(extract_cabin_num)

        
        # 2. Passenger group extraction
        df['Group'] = df[self.passenger_id_col].apply(lambda x: x.split('_')[0])
        
        # 3. Family Size / Group Size
        group_counts = df.groupby('Group')['Group'].transform('count')
        df['GroupSize'] = group_counts
        
        # 4. Spending aggregation
        spending_cols = ["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
        df[spending_cols] = df[spending_cols].fillna(0)
        df['TotalSpend'] = df[spending_cols].sum(axis=1)
        df['NoSpend'] = (df['TotalSpend'] == 0).astype(int)
        
        # 5. Interaction features
        df['Age_Spend'] = df['Age'] * df['TotalSpend']
        
        # 6. Interaction Between Deck and Side
        df['Deck_Side'] = df['CabinDeck'] + '_' + df['CabinSide']
        
        # 7. Rare category grouping (already handled by encoders later usually, but can be done here)
        
        logger.info(f"Feature engineering completed: Shape: {df.shape}")
        return df
