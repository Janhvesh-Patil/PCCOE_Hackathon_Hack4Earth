"""
Configuration settings for Flask API
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model settings
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_FILE = 'heatwave_risk_model.pkl'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)

# API settings
API_VERSION = '1.0'
API_TITLE = 'Heatwave Risk Prediction API'

# Risk thresholds (from training)
RISK_THRESHOLDS = {
    'low_to_medium': 35,
    'medium_to_high': 40
}

# Feature information
FEATURES = {
    'temperature_2m_max': {
        'type': 'float',
        'unit': '°C',
        'description': 'Maximum temperature',
        'example': 38.0
    },
    'temperature_2m_min': {
        'type': 'float',
        'unit': '°C',
        'description': 'Minimum temperature',
        'example': 25.0
    },
    'wind_speed_10m_max': {
        'type': 'float',
        'unit': 'km/h',
        'description': 'Maximum wind speed',
        'example': 12.0
    },
    'wind_gusts_10m_max': {
        'type': 'float',
        'unit': 'km/h',
        'description': 'Maximum wind gusts',
        'example': 20.0
    },
    'precipitation_sum': {
        'type': 'float',
        'unit': 'mm',
        'description': 'Total precipitation',
        'example': 0.0
    }
}