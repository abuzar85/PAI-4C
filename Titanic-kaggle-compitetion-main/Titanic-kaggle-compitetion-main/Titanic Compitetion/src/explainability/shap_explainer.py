import shap
import matplotlib.pyplot as plt
import os
import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger("SHAPExplainer")

class SHAPExplainer:
    """Class to generate model explanations using SHAP"""
    
    def __init__(self, model, X_sample: pd.DataFrame):
        self.model = model
        self.X_sample = X_sample
        self.explainer = None
        self.shap_values = None
        
    def generate_explanations(self, output_dir: str = "reports/shap/"):
        """Calculate SHAP values and save summary plots"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        logger.info("Generating SHAP explanations...")
        
        # Linear/Tree/Kernel explainer - picking based on model type would be ideal
        # For simplicity using KernelExplainer or TreeExplainer if possible
        try:
            # Most tree-based models (XGB, LightGBM, CatBoost)
            self.explainer = shap.TreeExplainer(self.model)
            self.shap_values = self.explainer.shap_values(self.X_sample)
        except:
             # Fallback to KernelExplainer
             self.explainer = shap.KernelExplainer(self.model.predict_proba, self.X_sample.iloc[:100])
             self.shap_values = self.explainer.shap_values(self.X_sample)
        
        # Save summary plot
        plt.figure(figsize=(12, 8))
        shap.summary_plot(self.shap_values, self.X_sample, show=False)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "shap_summary.png"))
        plt.close()
        
        logger.info(f"SHAP summary plot saved to {output_dir}")
        return self.shap_values
