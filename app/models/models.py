# models/models.py

import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')

def load_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model
