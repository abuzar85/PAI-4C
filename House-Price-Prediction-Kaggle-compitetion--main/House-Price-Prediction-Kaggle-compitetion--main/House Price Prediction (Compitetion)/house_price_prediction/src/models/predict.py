import joblib
import pandas as pd
import logging

class Predictor:
    """
    Class to handle predictions using a saved model.
    """
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.logger = logging.getLogger(__name__)

    def load_model(self):
        if self.model is None:
            self.logger.info(f"Loading custom model from {self.model_path}")
            self.model = joblib.load(self.model_path)
        return self.model

    def predict(self, input_data: pd.DataFrame):
        model = self.load_model()
        self.logger.info("Making prediction...")
        prediction = model.predict(input_data)
        return prediction
