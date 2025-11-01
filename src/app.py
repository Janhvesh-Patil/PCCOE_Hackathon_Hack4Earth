"""
Flask API for Heatwave Risk Prediction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# ============================================================================
# LOAD MODEL AT STARTUP
# ============================================================================

# Get the absolute path to model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'Model', 'heatwave_risk_model.pkl')

print("=" * 70)
print("🚀 LOADING ML MODEL...")
print(f"📂 Model path: {MODEL_PATH}")

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ ERROR: Model file not found!")
    print(f"   Expected location: {MODEL_PATH}")
    print("   Please ensure heatwave_risk_model.pkl is in models/ folder")
    model = None
except Exception as e:
    print(f"❌ ERROR loading model: {e}")
    model = None

print("=" * 70)

# Risk label mapping
RISK_LABELS = {
    0: 'Low',
    1: 'Medium',
    2: 'High'
}

# Feature names (must match training order!)
FEATURE_NAMES = [
    'temperature_2m_max',
    'temperature_2m_min',
    'wind_speed_10m_max',
    'wind_gusts_10m_max',
    'precipitation_sum'
]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Heatwave Risk Prediction API',
        'model_loaded': model is not None,
        'version': '1.0'
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict heatwave risk level

    Expected JSON input:
    {
        "temperature_2m_max": 38.0,
        "temperature_2m_min": 25.0,
        "wind_speed_10m_max": 12.0,
        "wind_gusts_10m_max": 20.0,
        "precipitation_sum": 0.0
    }
    """

    # Check if model is loaded
    if model is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'ML model failed to load at startup'
        }), 500

    # Get JSON data from request
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must contain JSON data'
            }), 400

        # Validate all required features are present
        missing_features = [f for f in FEATURE_NAMES if f not in data]
        if missing_features:
            return jsonify({
                'error': 'Missing features',
                'missing': missing_features,
                'required': FEATURE_NAMES
            }), 400

        # Extract features in correct order
        features = [data[feature] for feature in FEATURE_NAMES]

        # Validate feature values
        for i, (feature_name, value) in enumerate(zip(FEATURE_NAMES, features)):
            if not isinstance(value, (int, float)):
                return jsonify({
                    'error': 'Invalid feature type',
                    'feature': feature_name,
                    'expected': 'number',
                    'received': type(value).__name__
                }), 400

        # Convert to numpy array (2D array for single prediction)
        X = np.array([features])

        # Make prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]

        # Get risk level
        risk_level = RISK_LABELS[prediction]

        # Prepare response
        response = {
            'risk': risk_level,
            'risk_code': int(prediction),
            'confidence': {
                'low': float(probabilities[0]),
                'medium': float(probabilities[1]),
                'high': float(probabilities[2])
            },
            'input_features': {
                'temperature_max': features[0],
                'temperature_min': features[1],
                'wind_speed': features[2],
                'wind_gusts': features[3],
                'precipitation': features[4]
            },
            'recommendations': get_recommendations(risk_level)
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'features_required': FEATURE_NAMES,
        'risk_levels': list(RISK_LABELS.values())
    })


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_recommendations(risk_level):
    """Get health recommendations based on risk level"""

    recommendations = {
        'Low': [
            "Conditions are safe for outdoor activities",
            "Stay hydrated with regular water intake",
            "Normal precautions are sufficient"
        ],
        'Medium': [
            "Stay hydrated - drink water every 30-45 minutes",
            "Limit outdoor activities during peak afternoon hours (12 PM - 4 PM)",
            "Wear light, loose-fitting clothing",
            "Take frequent breaks in shaded areas",
            "Check on vulnerable individuals (elderly, children)"
        ],
        'High': [
            "⚠️ HEAT EMERGENCY - Stay indoors as much as possible",
            "Drink water every 20-30 minutes, even if not thirsty",
            "Avoid ALL outdoor activities between 11 AM - 5 PM",
            "Seek air-conditioned environments",
            "Check on elderly neighbors and family members frequently",
            "Know heatstroke symptoms: confusion, dizziness, rapid heartbeat, nausea",
            "Call emergency services if anyone shows heat illness symptoms"
        ]
    }

    return recommendations.get(risk_level, [])


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🌐 STARTING FLASK SERVER")
    print("=" * 70)
    print("📍 URL: http://localhost:5000")
    print("🔗 Endpoints:")
    print("   GET  /           - Health check")
    print("   POST /predict    - Predict heatwave risk")
    print("   GET  /health     - Detailed status")
    print("=" * 70)
    print("\n🧪 Test with:")
    print("   curl http://localhost:5000/")
    print("\n🛑 Stop with: Ctrl+C")
    print("=" * 70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)