from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)

# FIX: Allow frontend to access API
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:8080",  # Your React dev server
            "http://localhost:5173",  # Vite default
            "http://localhost:3000",  # Create React App default
            "http://127.0.0.1:8080"  # Alternative localhost
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Load model
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, 'models', 'heatwave_risk_model.pkl')
# model = pickle.load(open(MODEL_PATH, 'rb'))
model = pickle.load(open('../Model/heatwave_risk_model.pkl', 'rb'))

RISK_LABELS = {0: 'Low', 1: 'Medium', 2: 'High'}


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'model_loaded': True,
        'message': 'Heatwave Risk Prediction API'
    })


@app.route('/predict', methods=['POST', 'OPTIONS'])  # Add OPTIONS!
def predict():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()

        features = [
            data['temperature_2m_max'],
            data['temperature_2m_min'],
            data['wind_speed_10m_max'],
            data['wind_gusts_10m_max'],
            data['precipitation_sum']
        ]

        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]

        return jsonify({
            'risk': RISK_LABELS[prediction],
            'risk_code': int(prediction),
            'confidence': {
                'low': float(probabilities[0]),
                'medium': float(probabilities[1]),
                'high': float(probabilities[2])
            },
            'recommendations': get_recommendations(RISK_LABELS[prediction])
        })
    except Exception as e:
        print(f"Error in prediction: {e}")  # Log error
        return jsonify({'error': str(e)}), 500


def get_recommendations(risk_level):
    recommendations = {
        'Low': [
            "Conditions are safe for outdoor activities",
            "Stay hydrated with regular water intake",
            "Normal precautions are sufficient"
        ],
        'Medium': [
            "Stay hydrated - drink water every 30-45 minutes",
            "Limit outdoor activities during peak afternoon hours",
            "Wear light, loose-fitting clothing",
            "Take frequent breaks in shaded areas"
        ],
        'High': [
            "Stay indoors as much as possible",
            "Drink water every 20-30 minutes",
            "Avoid ALL outdoor activities between 11 AM - 5 PM",
            "Seek air-conditioned environments",
            "Know heatstroke symptoms: confusion, dizziness, nausea"
        ]
    }
    return recommendations.get(risk_level, [])


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting Flask API...")
    print("📍 Running on: http://localhost:5000")
    print("✅ CORS enabled for port 8080")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)