import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.feature_selection import RFECV
from src.utils.logger import setup_logger

logger = setup_logger("FeatureSelector")

class FeatureSelector:
    """Class to perform feature selection using various strategies"""
    
    def __init__(self, model):
        self.model = model
        
    def select_via_permutation_importance(self, X: pd.DataFrame, y: pd.Series, n_repeats: int = 10):
        """Perform permutation importance selection and return top features"""
        logger.info(f"Running permutation importance (n_repeats={n_repeats})...")
        
        result = permutation_importance(self.model, X, y, n_repeats=n_repeats, random_state=42)
        importance_df = pd.DataFrame({
            "feature": X.columns,
            "importance": result.importances_mean,
            "std": result.importances_std
        }).sort_values(by="importance", ascending=False)
        
        logger.info(f"Top 5 permutation importance features: {importance_df.head(5)}")
        return importance_df
        
    def select_via_rfe(self, X: pd.DataFrame, y: pd.Series, cv: int = 5):
        """Recursive Feature Elimination with Cross Validation"""
        logger.info(f"Running Recursive Feature Elimination (RFECV)...")
        
        # Note: Model must have coef_ or feature_importances_ attribute
        selector = RFECV(self.model, step=1, cv=cv, scoring="accuracy")
        selector = selector.fit(X, y)
        
        selected_features = X.columns[selector.support_]
        logger.info(f"RFECV selected {len(selected_features)} features out of {len(X.columns)}")
        
        return selected_features.tolist()
