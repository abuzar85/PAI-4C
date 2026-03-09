import logging
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.impute import SimpleImputer
import os
import pandas as pd

class ModelTrainer:
    """
    Class to handle model training and pipeline creation.
    """
    def __init__(self, model):
        self.model = model
        self.pipeline = None
        self.logger = logging.getLogger(__name__)

    def create_pipeline(self, X: pd.DataFrame):
        self.logger.info("Creating Scikit-learn Pipeline...")
        
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
        categorical_features = X.select_dtypes(include=['object']).columns

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )

        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', self.model)
        ])
        
        return self.pipeline

    def train(self, X_train, y_train):
        if self.pipeline is None:
            self.create_pipeline(X_train)
        
        self.logger.info(f"Training {self.model.__class__.__name__}...")
        self.pipeline.fit(X_train, y_train)
        self.logger.info("Training completed.")
        return self.pipeline

    def save_model(self, path: str):
        self.logger.info(f"Saving model to {path}...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.pipeline, path)
        self.logger.info("Model saved successfully.")
