#!/usr/bin/env python3
"""
Fix the Flask app structure and paths
"""
import os
import shutil

def fix_app_structure():
    print("🔧 Fixing application structure...")
    
    # Ensure proper directory structure
    directories = ['api/templates', 'api/static', 'database', 'ml_model']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Move app.py to api directory if it's in root
    if os.path.exists('app.py'):
        shutil.move('app.py', 'api/app.py')
        print("✅ Moved app.py to api/app.py")
    
    # Ensure index.html is in templates
    if os.path.exists('index.html'):
        shutil.move('index.html', 'api/templates/index.html')
        print("✅ Moved index.html to api/templates/index.html")
    
    # Create a proper requirements file
    requirements = """flask==2.3.3
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2
joblib==1.3.2
"""
    
    with open('api/requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created requirements.txt")
    
    print("\n🎉 Structure fixed successfully!")
    print("📋 Next steps:")
    print("1. Install dependencies: pip install -r api/requirements.txt")
    print("2. Run the app: python api/app.py")
    print("3. Visit: http://localhost:5000")

if __name__ == '__main__':
    fix_app_structure()