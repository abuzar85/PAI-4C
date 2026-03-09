import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from src.data.data_loader import DataLoader
from src.preprocessing.cleaning import DataCleaner
from src.preprocessing.feature_engineering import FeatureEngineer
from src.models.train_model import ModelTrainer
from src.models.evaluate_model import ModelEvaluator
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

class TrainingPipeline:
    """
    Orchestrator class for the entire training workflow.
    """
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.logger = logging.getLogger(__name__)

    def run(self):
        # 1. Load Data
        loader = DataLoader(self.data_path)
        df = loader.load_data()

        # 2. Clean Data
        cleaner = DataCleaner()
        df = cleaner.clean(df)

        # 3. Feature Engineering
        engineer = FeatureEngineer()
        df = engineer.engineer_features(df)

        # 4. Split Data
        X = df.drop('price', axis=1)
        y = df['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 5. Model Training & Comparison
        models = {
            "LinearRegression": LinearRegression(),
            "Ridge": Ridge(),
            "Lasso": Lasso(),
            "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=100, random_state=42),
            "LightGBM": LGBMRegressor(n_estimators=100, random_state=42, verbose=-1),
            "CatBoost": CatBoostRegressor(n_estimators=100, random_state=42, verbose=0)
        }

        evaluator = ModelEvaluator()
        best_r2 = -float('inf')
        best_model_name = ""
        best_pipeline = None

        results = {}

        for name, model in models.items():
            trainer = ModelTrainer(model)
            pipeline = trainer.train(X_train, y_train)
            metrics = evaluator.evaluate(pipeline, X_test, y_test)
            results[name] = metrics
            
            if metrics['R2 Score'] > best_r2:
                best_r2 = metrics['R2 Score']
                best_model_name = name
                best_pipeline = pipeline

        self.logger.info(f"Base Best Model: {best_model_name} with R2: {best_r2:.4f}")

        # 6. Hyperparameter Tuning for the best model (if it's XGB or LGBM or RF)
        from src.tuning.hyperparameter_tuning import HyperparameterTuner
        
        # We need preprocessed data for tuning in our implementation
        preprocessor = best_pipeline.named_steps['preprocessor']
        X_train_transformed = preprocessor.transform(X_train)
        tuner = HyperparameterTuner(X_train_transformed, y_train)
        
        if best_model_name == "XGBoost":
            best_params = tuner.tune_xgboost(n_trials=10)
            models[best_model_name] = XGBRegressor(**best_params, random_state=42)
        elif best_model_name == "LightGBM":
            best_params = tuner.tune_lightgbm(n_trials=10)
            models[best_model_name] = LGBMRegressor(**best_params, random_state=42, verbose=-1)
        
        # Retrain the best model with tuned parameters
        trainer = ModelTrainer(models[best_model_name])
        best_pipeline = trainer.train(X_train, y_train)
        final_metrics = evaluator.evaluate(best_pipeline, X_test, y_test)
        self.logger.info(f"Final Tuned {best_model_name} R2: {final_metrics['R2 Score']:.4f}")

        # 7. Explainability
        from src.explainability.shap_explainer import SHAPExplainer
        explainer = SHAPExplainer(best_pipeline, X_test.iloc[:50])
        explainer.explain()

        # Save Best Model
        trainer.save_model("models/saved_models/best_model.joblib")
        
        return results, best_model_name
