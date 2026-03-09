import pandas as pd
import os
import json
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset
from src.utils.logger import setup_logger

logger = setup_logger("DriftDetector")

class DriftDetector:
    """Class to detect data and target drift using Evidently AI"""
    
    def __init__(self, reference_df: pd.DataFrame, current_df: pd.DataFrame):
        self.reference_df = reference_df
        self.current_df = current_df

        
    def generate_drift_report(self, report_path: str = "reports/drift/"):
        """Calculate and save data drift report in HTML and JSON format"""
        if not os.path.exists(report_path):
            os.makedirs(report_path)
            
        logger.info("Generating data and target drift reports...")
        
        # 1. Create a data drift report with presets
        # We use presets for standard production monitoring
        report = Report(metrics=[
            DataDriftPreset(),
            DataSummaryPreset()
        ])
        
        try:
            # report.run() returns a Snapshot (Run) object in Evidently 0.7+
            snapshot = report.run(reference_data=self.reference_df, current_data=self.current_df)
            
            # Save HTML report for human review
            html_file = os.path.join(report_path, "drift_report.html")
            snapshot.save_html(html_file)
            
            # Save JSON report for system monitoring
            json_file = os.path.join(report_path, "drift_report.json")
            snapshot.save_json(json_file)
            
            logger.info(f"Drift report successfully saved to {html_file} and {json_file}")
            return html_file
        except Exception as e:
            logger.error(f"Error generating drift report: {e}")
            raise