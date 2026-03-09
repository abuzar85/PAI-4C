import pandas as pd
import yaml
import mlflow
import os
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from src.data.data_loader import DataLoader
from src.data.data_validation import DataValidator
from src.features.feature_engineering import FeatureEngineer
from src.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from src.models.train_model import ModelTrainer
from src.tuning.optuna_tuner import HyperparameterTuner
from src.explainability.shap_explainer import SHAPExplainer
from src.monitoring.data_drift import DriftDetector
from src.utils.logger import setup_logger

logger = setup_logger("TrainingPipeline")

class TrainingPipeline:
    """Class to orchestrate the full training and monitoring workflow"""
    
    def __init__(self, config_path: str):
        # Determine the project root directory
        # config_path is usually 'configs/config.yaml' or '../configs/config.yaml'
        self.config_path = os.path.abspath(config_path)
        self.project_root = os.path.dirname(os.path.dirname(self.config_path))
        
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        # Resolve data paths relative to project root if they are relative
        for key in ['raw_path', 'test_path', 'processed_path']:
            path = self.config['data'][key]
            if not os.path.isabs(path):
                self.config['data'][key] = os.path.join(self.project_root, path)

        # Resolve model save path
        model_path = self.config['model']['saved_models_path']
        if not os.path.isabs(model_path):
            self.config['model']['saved_models_path'] = os.path.join(self.project_root, model_path)

        # Resolve MLflow tracking URI if it's a local file
        if self.config['model']['mlflow_tracking_uri'].startswith("sqlite:///"):
            db_path = self.config['model']['mlflow_tracking_uri'].replace("sqlite:///", "")
            if not os.path.isabs(db_path):
                abs_db_path = os.path.join(self.project_root, db_path)
                self.config['model']['mlflow_tracking_uri'] = f"sqlite:///{abs_db_path}"

        self.data_loader = DataLoader(self.config['data']['raw_path'], self.config['data']['test_path'])

        
        # Define expected columns for validation
        expected_cols = self.config['features']['numerical_cols'] + \
                        self.config['features']['categorical_cols'] + \
                        [self.config['features']['cabin_col'], "PassengerId", "Name"]
        self.data_validator = DataValidator(expected_cols, self.config['data']['target'])
        
        self.feature_engineer = FeatureEngineer(self.config['features']['cabin_col'])
        self.preprocessing_pipeline = PreprocessingPipeline(
            numerical_cols=self.config['features']['numerical_cols'] + ['GroupSize', 'TotalSpend', 'Age_Spend', 'CabinNum'],
            categorical_cols=self.config['features']['categorical_cols'] + ['CabinSide', 'CabinDeck', 'Deck_Side']
        )
        
        # Initialize MLflow
        mlflow.set_tracking_uri(self.config['model']['mlflow_tracking_uri'])
        mlflow.set_experiment(self.config['model']['experiment_name'])
        
        # Ensure model directory exists
        os.makedirs(self.config['model']['saved_models_path'], exist_ok=True)
        
    def run(self):
        """Run the training lifecycle"""
        
        # 1. Load Data
        df = self.data_loader.load_train_data()
        test_df = self.data_loader.load_test_data()
        
        # 2. Validate Data
        if not self.data_validator.validate(df):
            logger.error("Data validation failed. Aborting training.")
            return

        # 3. Feature Engineering
        logger.info("Starting feature engineering...")
        df_engineered = self.feature_engineer.transform(df)
        
        # 4. Target Label Encoding
        y = df_engineered[self.config['data']['target']].astype(int)
        X = df_engineered.drop(columns=[self.config['data']['target']] + self.config['data']['drop_cols'] + [self.config['features']['cabin_col'], 'Group'])
        
        # 5. Preprocessing Pipeline
        logger.info("Applying preprocessing...")
        preprocessor = self.preprocessing_pipeline.get_pipeline()
        X_preprocessed = preprocessor.fit_transform(X)
        
        # Use simple pandas df for consistency after preprocessing (getting feature names is easier with pipeline)
        try:
             # Scikit-learn >= 1.0 support
             feature_names = preprocessor.get_feature_names_out()
             X_processed_df = pd.DataFrame(X_preprocessed.toarray() if hasattr(X_preprocessed, "toarray") else X_preprocessed, columns=feature_names)
        except:
             X_processed_df = pd.DataFrame(X_preprocessed.toarray() if hasattr(X_preprocessed, "toarray") else X_preprocessed)

        # 6. Train-Test Split (Wait, this is hold-out evaluation before final training)
        X_train, X_holdout, y_train, y_holdout = train_test_split(
            X_processed_df, y, test_size=self.config['model']['test_size'], random_state=42, stratify=y
        )
        
        # 7. Hyperparameter Tuning (Optional, will take a while, maybe subset for demo?)
        # For now training with default XGBoost or tuned one
        # tuner = HyperparameterTuner(X_train, y_train, n_trials=5)
        # best_params = tuner.tune_ xgboost()
        
        # 8. Model Training & Evaluation
        logger.info("Training LightGBM model...")
        lgbm_model = LGBMClassifier(random_state=42, verbose=-1)
        trainer = ModelTrainer(lgbm_model, "LightGBM", self.config)
        trainer.train(X_train, y_train)
        metrics = trainer.evaluate(X_holdout, y_holdout)
        
        # 9. SHAP Explainability
        logger.info("Generating model explanations...")
        shap_explainer = SHAPExplainer(lgbm_model, X_holdout.iloc[:100])
        shap_explainer.generate_explanations()
        
        # 10. Drift Monitoring
        # Compare training data (reference) and hold-out data (current) as proxy
        try:
            logger.info("Checking for data drift...")
            drift_detector = DriftDetector(X_train.iloc[:500], X_holdout.iloc[:500])
            drift_detector.generate_drift_report()
        except Exception as e:
            logger.warning(f"Data drift detection skipped or failed: {e}")

        
        # 11. Save Preprocessor for Inference
        preprocessor_path = os.path.join(self.config['model']['saved_models_path'], "preprocessor.joblib")
        import joblib
        joblib.dump(preprocessor, preprocessor_path)
        logger.info(f"Preprocessor saved to {preprocessor_path}")
        
        logger.info("Training pipeline finished successfully.")
        return metrics

