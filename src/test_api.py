"""
Test script for Flask API
Run this after starting the Flask server
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

print("=" * 70)
print("🧪 TESTING FLASK API")
print("=" * 70)

# ============================================================================
# Test 1: Health Check
# ============================================================================
print("\n1️⃣ Testing health check endpoint...")
try:
    response = requests.get(f'{BASE_URL}/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# Test 2: Low Risk Prediction
# ============================================================================
print("\n2️⃣ Testing Low Risk prediction...")
low_risk_data = {
    "temperature_2m_max": 28.0,
    "temperature_2m_min": 20.0,
    "wind_speed_10m_max": 10.0,
    "wind_gusts_10m_max": 18.0,
    "precipitation_sum": 0.0
}

try:
    response = requests.post(f'{BASE_URL}/predict', json=low_risk_data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Predicted Risk: {result['risk']}")
    print(f"   Confidence: Low={result['confidence']['low']:.1%}, "
          f"Med={result['confidence']['medium']:.1%}, "
          f"High={result['confidence']['high']:.1%}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# Test 3: High Risk Prediction
# ============================================================================
print("\n3️⃣ Testing High Risk prediction...")
high_risk_data = {
    "temperature_2m_max": 45.0,
    "temperature_2m_min": 32.0,
    "wind_speed_10m_max": 5.0,
    "wind_gusts_10m_max": 12.0,
    "precipitation_sum": 0.0
}

try:
    response = requests.post(f'{BASE_URL}/predict', json=high_risk_data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Predicted Risk: {result['risk']}")
    print(f"   Confidence: Low={result['confidence']['low']:.1%}, "
          f"Med={result['confidence']['medium']:.1%}, "
          f"High={result['confidence']['high']:.1%}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ TESTING COMPLETE")
print("=" * 70)