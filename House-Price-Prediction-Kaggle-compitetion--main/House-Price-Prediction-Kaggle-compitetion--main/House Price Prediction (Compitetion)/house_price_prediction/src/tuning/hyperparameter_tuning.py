import optuna
import logging
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor

class HyperparameterTuner:
    """
    Class to handle hyperparameter tuning using Optuna.
    """
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.logger = logging.getLogger(__name__)

    def tune_xgboost(self, n_trials=50):
        def objective(trial):
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            }
            model = XGBRegressor(**params, random_state=42)
            # Simplified: non-pipeline CV for tuning params, or we can use pipeline
            # Better to use pipeline to avoid leakage, but here we assume preprocessed X for tuning
            score = cross_val_score(model, self.X, self.y, cv=3, scoring='r2').mean()
            return score

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        self.logger.info(f"Best parameters for XGBoost: {study.best_params}")
        return study.best_params

    def tune_lightgbm(self, n_trials=50):
        def objective(trial):
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'num_leaves': trial.suggest_int('num_leaves', 20, 100),
            }
            model = LGBMRegressor(**params, random_state=42, verbose=-1)
            score = cross_val_score(model, self.X, self.y, cv=3, scoring='r2').mean()
            return score

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        self.logger.info(f"Best parameters for LightGBM: {study.best_params}")
        return study.best_params
