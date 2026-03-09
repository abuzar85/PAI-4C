import logging
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class ModelEvaluator:
    """
    Class to handle model evaluation.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def evaluate(self, model, X_test, y_test):
        self.logger.info("Evaluating model...")
        predictions = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        metrics = {
            "MAE": mae,
            "RMSE": rmse,
            "R2 Score": r2
        }
        
        for name, value in metrics.items():
            self.logger.info(f"{name}: {value:.4f}")
            
        return metrics
