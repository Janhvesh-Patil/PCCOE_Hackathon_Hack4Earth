import requests
import json

# Test 1: Health check
print("Test 1: Health Check")
response = requests.get('http://localhost:5000/')
print(response.json())
print()

# Test 2: Prediction
print("Test 2: Prediction Test")
data = {
    "temperature_2m_max": 38.0,
    "temperature_2m_min": 25.0,
    "wind_speed_10m_max": 12.0,
    "wind_gusts_10m_max": 20.0,
    "precipitation_sum": 0.0
}

response = requests.post('http://localhost:5000/predict', json=data)
result = response.json()

print(f"Risk: {result['risk']}")
print(f"Confidence: {result['confidence']}")
print(f"Recommendations: {result['recommendations'][:2]}")  # First 2