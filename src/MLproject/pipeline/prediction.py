import joblib 
import numpy as np
import pandas as pd
from pathlib import Path
import os



class PredictionPipeline:
    def __init__(self):
        # Use absolute path from current working directory
        model_path = Path(os.getcwd()) / 'artifacts' / 'model_trainer' / 'model.joblib'
        if not model_path.exists():
            # Try relative path from src directory
            model_path = Path('artifacts') / 'model_trainer' / 'model.joblib'
        self.model = joblib.load(model_path)

    
    def predict(self, data):
        prediction = self.model.predict(data)

        return prediction