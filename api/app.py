# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import sqlite3
import os
import numpy as np
import sys

# Add parent directory to path to import from ml_model and database
sys.path.append('..')

app = Flask(__name__, template_folder='templates')

# Load the trained model with better path handling
try:
    model_path = '../ml_model/disease_prediction_model.pkl'
    if not os.path.exists(model_path):
        model_path = 'ml_model/disease_prediction_model.pkl'
    
    model_package = joblib.load(model_path)
    model = model_package['model']
    scaler = model_package['scaler']
    target_encoder = model_package['target_encoder']
    feature_columns = model_package['feature_columns']
    symptoms_list = model_package['symptoms_list']    
    print("✅ Model loaded successfully!")
    print("📊 Model type: ",model_package['model_type'])
    print("🎯 Target classes: ",target_encoder.classes_)
except Exception as e:
    print("❌ Error loading model: ",e)
    model = None
    model_package = None

class MedicalSystem:
    def __init__(self):
        # Try multiple possible database paths
        self.db_paths = [
            '../database/medical_data.db',
            'database/medical_data.db',
            'medical_data.db'
        ]
        self.db_path = self.find_database()
    
    def find_database(self):
        """Find the database file in common locations"""
        for path in self.db_paths:
            if os.path.exists(path):
                print(" Database found: ",path)
                return path
        print("❌ No database file found!")
        return None
    
    def predict_disease(self, patient_data):
        """Predict disease based on patient symptoms and data"""
        if model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Convert input to DataFrame
            input_df = pd.DataFrame([patient_data])
            
            # Ensure all feature columns are present
            for col in feature_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            # Ensure correct column order
            input_df = input_df[feature_columns]
            
            # Preprocess if needed
            if model_package['model_type'] == 'Random Forest' and scaler:
                numerical_columns = ['age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia', 
                                   'cholesterol', 'blood_sugar']
                input_df[numerical_columns] = scaler.transform(input_df[numerical_columns])
            
            # Make prediction
            prediction_encoded = model.predict(input_df)[0]
            prediction_proba = model.predict_proba(input_df)[0]
            
            disease_prediction = target_encoder.inverse_transform([prediction_encoded])[0]
            confidence = float(np.max(prediction_proba))
            
            # Get all probabilities
            probabilities = {}
            for disease, prob in zip(target_encoder.classes_, prediction_proba):
                probabilities[disease] = float(prob)
            
            return {
                "prediction": disease_prediction,
                "confidence": confidence,
                "probabilities": probabilities
            }
            
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}
    
    def get_patient_records(self):
        """Get all patient records from database"""
        if not self.db_path:
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT p.patient_id, p.first_name, p.last_name, p.date_of_birth, p.gender,
                   e.exam_date, e.symptoms, e.diagnosis, e.treatment
            FROM patients p
            LEFT JOIN examinations e ON p.patient_id = e.patient_id
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df.to_dict('records')
        except Exception as e:
            print(f"Database error: {e}")
            return []

medical_system = MedicalSystem()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for disease prediction"""
    try:
        data = request.json
        
        # Required fields validation
        required_fields = ['age', 'gender', 'bmi', 'blood_pressure_sys', 
                          'blood_pressure_dia', 'cholesterol', 'blood_sugar']
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Set default 0 for symptoms if not provided
        for symptom in symptoms_list:
            if symptom not in data:
                data[symptom] = 0
        
        # Make prediction
        result = medical_system.predict_disease(data)
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """API endpoint to get patient records"""
    try:
        records = medical_system.get_patient_records()
        return jsonify({"patients": records})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint to get system statistics"""
    try:
        if not medical_system.db_path:
            return jsonify({"error": "Database not found"}), 500
            
        conn = sqlite3.connect(medical_system.db_path)
        
        # Get counts and convert to native Python int
        patient_count = int(pd.read_sql_query("SELECT COUNT(*) as count FROM patients", conn).iloc[0]['count'])
        exam_count = int(pd.read_sql_query("SELECT COUNT(*) as count FROM examinations", conn).iloc[0]['count'])
        
        # Get disease stats and convert counts to int
        disease_stats_df = pd.read_sql_query("SELECT diagnosis, COUNT(*) as count FROM examinations GROUP BY diagnosis", conn)
        disease_stats = []
        for _, row in disease_stats_df.iterrows():
            disease_stats.append({
                "diagnosis": row['diagnosis'],
                "count": int(row['count'])  # Convert to native int
            })
        
        conn.close()
        
        return jsonify({
            "patient_count": patient_count,
            "exam_count": exam_count,
            "disease_distribution": disease_stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "database": medical_system.db_path is not None,
        "database_path": medical_system.db_path,
        "model_type": model_package['model_type'] if model_package else "None"
    })

if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Starting Medical Prediction System...")
    print("=" * 50)
    print("📊 Access the system at: http://localhost:5000")
    print("🔍 Health check at: http://localhost:5000/api/health")
    print("📈 Model loaded:", model is not None)
    print("🗄️ Database path:", medical_system.db_path)
    print("=" * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
