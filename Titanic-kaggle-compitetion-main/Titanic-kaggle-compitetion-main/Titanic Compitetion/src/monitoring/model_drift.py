from src.utils.logger import setup_logger

logger = setup_logger("ModelDrift")

class ModelDriftDetector:
    """Class to detect model performance degradation over time"""
    
    def __init__(self, reference_accuracy: float):
        self.reference_accuracy = reference_accuracy
        
    def check_drift(self, current_accuracy: float, threshold: float = 0.05):
        """Check if current accuracy has dropped significantly below reference"""
        drift = self.reference_accuracy - current_accuracy
        if drift > threshold:
            logger.warning(f"Model drift detected! Accuracy dropped by {drift:.4f}")
            return True
        logger.info(f"Model performance stable (Drift: {drift:.4f})")
        return False
