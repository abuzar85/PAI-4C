import optuna
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from src.utils.logger import setup_logger

logger = setup_logger("OptunaTuner")

class HyperparameterTuner:
    """Class to handle hyperparameter optimization for models using Optuna"""
    
    def __init__(self, X: pd.DataFrame, y: pd.Series, n_trials: int = 50, cv_folds: int = 5):
        self.X = X
        self.y = y
        self.n_trials = n_trials
        self.cv_folds = cv_folds
        
    def tune_xgboost(self):
        """Perform optimization for XGBoost model"""
        
        def objective(trial):
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
                'gamma': trial.suggest_float('gamma', 0, 10),
                'random_state': 42,
            }
            
            model = XGBClassifier(**params)
            skf = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=42)
            score = cross_val_score(model, self.X, self.y, cv=skf, scoring='accuracy').mean()
            return score
            
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=self.n_trials)
        
        logger.info(f"Finished XGBoost Tuning: Best Accuracy = {study.best_value:.4f}")
        return study.best_params
        
    def tune_lgbm(self):
        """Perform optimization for LightGBM model"""
        
        def objective(trial):
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'max_depth': trial.suggest_int('max_depth', 3, 15),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'num_leaves': trial.suggest_int('num_leaves', 20, 150),
                'feature_fraction': trial.suggest_float('feature_fraction', 0.5, 1.0),
                'bagging_fraction': trial.suggest_float('bagging_fraction', 0.5, 1.0),
            }
            
            model = LGBMClassifier(**params, random_state=42, verbose=-1)
            skf = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=42)
            score = cross_val_score(model, self.X, self.y, cv=skf, scoring='accuracy').mean()
            return score
            
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=self.n_trials)
        
        logger.info(f"Finished LGBM Tuning: Best Accuracy = {study.best_value:.4f}")
        return study.best_params
