import shap
import matplotlib.pyplot as plt
import logging
import os

class SHAPExplainer:
    """
    Model explainability using SHAP.
    Automatically detects model type and handles pipelines.
    """
    def __init__(self, model, X_sample):
        self.model = model
        self.X_sample = X_sample
        self.logger = logging.getLogger(__name__)
        
    def explain(self):
        self.logger.info("Generating SHAP explanations...")

        # Handle pipeline
        if hasattr(self.model, 'named_steps'):
            # Extract regressor and preprocessor
            preprocessor = self.model.named_steps['preprocessor']
            regressor = self.model.named_steps['regressor']
            
            # Transform data for SHAP
            X_transformed = preprocessor.transform(self.X_sample)
            
            # Generate feature names
            feature_names = []
            for name, transformer, columns in preprocessor.transformers_:
                if name == 'num':
                    if 'poly' in transformer.named_steps:
                        poly = transformer.named_steps['poly']
                        feature_names.extend(poly.get_feature_names_out(columns))
                    else:
                        feature_names.extend(columns)
                elif name == 'cat':
                    ohe = transformer.named_steps['onehot']
                    feature_names.extend(ohe.get_feature_names_out(columns))
        else:
            # Model is not a pipeline
            regressor = self.model
            X_transformed = self.X_sample
            feature_names = X_transformed.columns

        # Select correct SHAP explainer
        import sklearn
        from sklearn.base import RegressorMixin
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

        if isinstance(regressor, (sklearn.linear_model.LinearRegression, sklearn.linear_model.Lasso, sklearn.linear_model.Ridge)):
            explainer = shap.LinearExplainer(
                            regressor,
                            X_transformed,
                            feature_perturbation="interventional"
                        )
        elif isinstance(regressor, (RandomForestRegressor, GradientBoostingRegressor)):
            explainer = shap.TreeExplainer(regressor)
        else:
            # Fallback for any model (pipeline or other)
            explainer = shap.KernelExplainer(regressor.predict, X_transformed)

        shap_values = explainer(X_transformed)

        # Plot SHAP summary
        plt.figure(figsize=(12, 6))
        shap.summary_plot(shap_values, X_transformed, feature_names=feature_names, show=False)
        os.makedirs('models/saved_models', exist_ok=True)
        plt.tight_layout()
        plt.savefig('models/saved_models/shap_summary.png')
        self.logger.info("SHAP summary plot saved to models/saved_models/shap_summary.png")

        return shap_values