import joblib 
import numpy as np
import pandas as pd
from pathlib import Path
import os



class PredictionPipeline:
    def __init__(self):
        # Get the project root directory (3 levels up from this file: src/MLproject/pipeline/)
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        
        # Build the model path
        model_path = project_root / 'artifacts' / 'model_trainer' / 'model.joblib'
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        self.model = joblib.load(model_path)

    
    def predict(self, data):
        prediction = self.model.predict(data)

        return prediction