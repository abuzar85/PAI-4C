import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
import os
from src.utils.logger import setup_logger

logger = setup_logger("ModelEvaluator")

class ModelEvaluator:
    """Class to generate model evaluation plots and reports"""
    
    def __init__(self, y_true, y_pred, y_proba):
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_proba = y_proba
        
    def plot_confusion_matrix(self, save_path: str = "reports/plots/confusion_matrix.png"):
        """Plot and save confusion matrix"""
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
            
        cm = confusion_matrix(self.y_true, self.y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.savefig(save_path)
        plt.close()
        logger.info(f"Confusion Matrix saved to {save_path}")
        
    def plot_roc_curve(self, save_path: str = "reports/plots/roc_curve.png"):
        """Plot and save ROC curve and calculate AUC"""
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
            
        fpr, tpr, thresholds = roc_curve(self.y_true, self.y_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.savefig(save_path)
        plt.close()
        logger.info(f"ROC curve saved to {save_path}")
        
    def get_classification_report(self):
        """Return text classification report"""
        report = classification_report(self.y_true, self.y_pred)
        logger.info(f"Classification Report: \n{report}")
        return report
