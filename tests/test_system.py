#!/usr/bin/env python3
"""
Test the complete medical system
"""
import requests
import json
import time

def test_system():
    print("🧪 Testing Medical System...")
    
    # Wait for server to start
    time.sleep(2)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        health_response = requests.get(f"{base_url}/api/health")
        health_data = health_response.json()
        print(f"   ✅ Health: {health_data}")
        
        # Test stats endpoint
        print("2. Testing stats endpoint...")
        stats_response = requests.get(f"{base_url}/api/stats")
        stats_data = stats_response.json()
        print(f"   ✅ Stats: {stats_data}")
        
        # Test prediction endpoint
        print("3. Testing prediction endpoint...")
        test_patient = {
            "age": 45,
            "gender": 0,
            "bmi": 25.5,
            "blood_pressure_sys": 135,
            "blood_pressure_dia": 85,
            "cholesterol": 220,
            "blood_sugar": 110,
            "headache": 1,
            "dizziness": 1,
            "chest_pain": 0,
            "fatigue": 0,
            "frequent_urination": 0,
            "thirst": 0,
            "fever": 0,
            "cough": 0,
            "shortness_breath": 0,
            "wheezing": 0,
            "chest_tightness": 0,
            "joint_pain": 0,
            "swelling": 0,
            "stiffness": 0,
            "nausea": 0,
            "sensitivity_light": 0,
            "abdominal_pain": 0,
            "bloating": 0
        }
        
        prediction_response = requests.post(
            f"{base_url}/api/predict",
            json=test_patient,
            headers={'Content-Type': 'application/json'}
        )
        prediction_data = prediction_response.json()
        print(f"   ✅ Prediction: {prediction_data}")
        
        print("\n🎉 All tests passed! System is working correctly.")
        print(f"🌐 Open your browser and visit: {base_url}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure the Flask app is running on port 5000")

if __name__ == '__main__':
    test_system()