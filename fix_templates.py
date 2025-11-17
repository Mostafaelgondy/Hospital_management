#!/usr/bin/env python3
"""
Quick fix script to create missing templates and directories
"""

import os
import shutil

def fix_template_issue():
    print("🔧 Fixing template issue...")
    
    # Create templates directory
    templates_dir = 'api/templates'
    os.makedirs(templates_dir, exist_ok=True)
    print(f"✅ Created directory: {templates_dir}")
    
    # Create the index.html template
    index_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Medical Disease Prediction System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Medical Disease Prediction System</h1>
        <div id="status"></div>
        
        <div>
            <h2>System Status</h2>
            <button class="btn" onclick="checkHealth()">Check Health</button>
            <button class="btn" onclick="testPrediction()">Test Prediction</button>
        </div>
        
        <div id="results" style="margin-top: 20px;"></div>
    </div>

    <script>
        async function checkHealth() {
            const status = document.getElementById('status');
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                status.innerHTML = `<div class="status success">✅ System Healthy - Model: ${data.model_loaded ? 'Loaded' : 'Not Loaded'}, Database: ${data.database ? 'Connected' : 'Missing'}</div>`;
            } catch (error) {
                status.innerHTML = `<div class="status error">❌ Health check failed: ${error}</div>`;
            }
        }

        async function testPrediction() {
            const results = document.getElementById('results');
            results.innerHTML = '<p>Testing prediction...</p>';
            
            const testData = {
                age: 45,
                gender: 0,
                bmi: 25.5,
                blood_pressure_sys: 120,
                blood_pressure_dia: 80,
                cholesterol: 200,
                blood_sugar: 100,
                headache: 1,
                dizziness: 1,
                chest_pain: 0,
                fatigue: 0,
                frequent_urination: 0,
                thirst: 0,
                fever: 0,
                cough: 0,
                shortness_breath: 0,
                wheezing: 0,
                chest_tightness: 0,
                joint_pain: 0,
                swelling: 0,
                stiffness: 0,
                nausea: 0,
                sensitivity_light: 0,
                abdominal_pain: 0,
                bloating: 0
            };

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(testData)
                });
                const data = await response.json();
                
                if (data.error) {
                    results.innerHTML = `<div class="status error">❌ Prediction error: ${data.error}</div>`;
                } else {
                    results.innerHTML = `
                        <div class="status success">
                            <h3>✅ Prediction Successful!</h3>
                            <p><strong>Disease:</strong> ${data.prediction}</p>
                            <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
                            <p><strong>Probabilities:</strong></p>
                            <ul>
                                ${Object.entries(data.probabilities).map(([disease, prob]) => 
                                    `<li>${disease}: ${(prob * 100).toFixed(1)}%</li>`
                                ).join('')}
                            </ul>
                        </div>
                    `;
                }
            } catch (error) {
                results.innerHTML = `<div class="status error">❌ Prediction failed: ${error}</div>`;
            }
        }

        // Check health on page load
        window.onload = checkHealth;
    </script>
</body>
</html>'''
    
    with open(f'{templates_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("✅ Created index.html template")
    
    print("\n🎉 Template issue fixed!")
    print("🔧 Now restart your Flask application:")
    print("   python api/app.py")
    print("🌐 Then visit: http://localhost:5000")

if __name__ == '__main__':
    fix_template_issue()