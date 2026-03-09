import pandas as pd
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from src.utils.logger import setup_logger

logger = setup_logger("EnsembleLearner")

class EnsembleLearner:
    """Class to implement ensemble learning strategies"""
    
    def __init__(self, models: list, model_names: list):
        self.models = list(zip(model_names, models))
        self.final_estimator = LogisticRegression()
        
    def get_voting_ensemble(self, voting='soft'):
        """Build and return a voting classifier ensemble"""
        logger.info(f"Building Voting Ensemble ({voting}) with models: {self.models}")
        return VotingClassifier(estimators=self.models, voting=voting)
        
    def get_stacking_ensemble(self):
        """Build and return a stacking classifier ensemble"""
        logger.info(f"Building Stacking Ensemble with models: {self.models}")
        return StackingClassifier(estimators=self.models, final_estimator=self.final_estimator)
        
    def get_blending_ensemble(self):
        """Implement manual blending if needed or simple average"""
        # Manual implementation can be tricky, for simplicity will return stacking
        logger.info("Blending manually can be implemented using k-fold, current implementation using stacking")
        return self.get_stacking_ensemble()
