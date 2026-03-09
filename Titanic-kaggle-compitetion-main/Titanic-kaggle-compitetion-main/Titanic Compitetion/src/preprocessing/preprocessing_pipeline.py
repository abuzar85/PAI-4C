import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from src.utils.logger import setup_logger

logger = setup_logger("PreprocessingPipeline")

class PreprocessingPipeline:
    """Class to define preprocessing steps for the titanic dataset"""
    
    def __init__(self, numerical_cols: list, categorical_cols: list):
        self.numerical_cols = numerical_cols
        self.categorical_cols = categorical_cols
        self.preprocessor = None
        
    def get_pipeline(self):
        """Build the full preprocessing pipeline"""
        
        # Define numerical transformer
        num_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # Define categorical transformer
        cat_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine transformers
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', num_transformer, self.numerical_cols),
                ('cat', cat_transformer, self.categorical_cols)
            ])
        
        logger.info("Preprocessing pipeline created")
        return self.preprocessor
