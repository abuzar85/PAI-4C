from src.pipeline.training_pipeline import TrainingPipeline
from src.utils.helpers import setup_logging
import logging

def main():
    # Setup standard logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting House Price Prediction Project...")
    
    # Path to the dataset
    data_path = "data/raw/housing.csv"
    
    # Run the training pipeline
    pipeline = TrainingPipeline(data_path)
    results, best_model = pipeline.run()
    
    logger.info("Project workflow execution completed successfully.")
    logger.info(f"Results Summary: {results}")

if __name__ == "__main__":
    main()
