import os
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from src.utils.logger import setup_logger

logger = setup_logger("ModelTrainer")

class ModelTrainer:
    """Class to handle model training and evaluation using k-fold cross validation"""
    
    def __init__(self, model, model_name: str, config: dict):
        self.model = model
        self.model_name = model_name
        self.config = config
        self.random_fold = config['model']['random_seed']
        self.cv_folds = config['model']['cv_folds']
        
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Perform stratified k-fold cross validation and train the final model"""
        
        skf = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=self.random_fold)
        cv_scores = []
        
        logger.info(f"Starting Stratified 5-Fold Cross Validation for {self.model_name}...")
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
            X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
            y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
            
            # Train model on this fold
            self.model.fit(X_tr, y_tr)
            
            # Predict for validation
            y_pred = self.model.predict(X_val)
            acc = accuracy_score(y_val, y_pred)
            cv_scores.append(acc)
            
            logger.info(f"Fold {fold+1}: Accuracy = {acc:.4f}")
            
        mean_acc = np.mean(cv_scores)
        std_acc = np.std(cv_scores)
        
        logger.info(f"Finished 5-Fold CV. Mean Accuracy: {mean_acc:.4f} (+/- {std_acc:.4f})")
        
        # Train final model on full dataset
        self.model.fit(X_train, y_train)
        
        # Log final model and metrics to MLflow
        with mlflow.start_run(run_name=f"{self.model_name}_Production"):
            mlflow.log_param("model", self.model_name)
            mlflow.log_metric("mean_cv_accuracy", mean_acc)
            mlflow.log_metric("std_cv_accuracy", std_acc)
            mlflow.sklearn.log_model(self.model, f"{self.model_name}_model")
            
        # Save final model locally
        save_path = os.path.join(self.config['model']['saved_models_path'], f"{self.model_name}.joblib")
        joblib.dump(self.model, save_path)
        logger.info(f"Final {self.model_name} model saved to: {save_path}")
        
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series):
        """Evaluate the final model on the hold-out test set"""
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_proba)
        }
        
        logger.info(f"Final Evaluation results for {self.model_name}: {metrics}")
        return metrics
