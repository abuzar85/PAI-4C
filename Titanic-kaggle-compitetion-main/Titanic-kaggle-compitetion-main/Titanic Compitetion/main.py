import argparse
from src.pipeline.training_pipeline import TrainingPipeline
from src.utils.logger import setup_logger

logger = setup_logger("Main")

def main():
    parser = argparse.ArgumentParser(description="Spaceship Titanic Production ML Pipeline")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to the config file")
    args = parser.parse_args()
    
    logger.info("Starting Spaceship Titanic Production Machine Learning System")
    
    try:
        pipeline = TrainingPipeline(args.config)
        metrics = pipeline.run()
        
        if metrics:
            logger.info(f"Pipeline executed successfully with metrics: {metrics}")
        else:
            logger.error("Pipeline failed to return results.")
            
    except Exception as e:
        logger.error(f"Error in running pipeline: {e}")
        raise
        
if __name__ == "__main__":
    main()
