import pandas as pd
import logging
from sklearn.feature_selection import SelectKBest, f_regression

class FeatureSelector:
    """
    Class to handle feature selection.
    """
    def __init__(self, k=10):
        self.k = k
        self.logger = logging.getLogger(__name__)

    def select_features(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        self.logger.info(f"Selecting top {self.k} features...")
        
        # Only select numeric columns for SelectKBest f_regression
        numeric_X = X.select_dtypes(include=['number'])
        
        if numeric_X.shape[1] < self.k:
            self.logger.warning("Number of features is less than k. Adjusting k.")
            k = numeric_X.shape[1]
        else:
            k = self.k

        selector = SelectKBest(score_func=f_regression, k=k)
        selector.fit(numeric_X, y)
        
        cols = selector.get_support(indices=True)
        selected_features = numeric_X.iloc[:, cols]
        
        # Add back categorical features for the final pipeline
        categorical_X = X.select_dtypes(exclude=['number'])
        final_X = pd.concat([selected_features, categorical_X], axis=1)
        
        self.logger.info("Feature selection completed.")
        return final_X
