#!/usr/bin/env python3
"""
Setup script for Medical Data Management System
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_system():
    """Main setup function"""
    print("🏥 Medical Data Management System Setup")
    print("=" * 50)
    
    # Create directory structure
    directories = ['database', 'ml_model', 'api', 'docs', 'tests', 'api/templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # # Install requirements
    # if run_command("pip install -r api/requirements.txt", "Installing Python dependencies"):
    #     print("✅ All dependencies installed successfully!")
    # else:
    #     print("❌ Failed to install dependencies")
    #     return False
    
    # Initialize database
    if run_command("python database/create_database.py", "Initializing database"):
        print("✅ Database initialized successfully!")
    else:
        print("❌ Failed to initialize database")
        return False
    
    # Train ML model
    if run_command("python ml_model/train_model.py", "Training ML model"):
        print("✅ ML model trained successfully!")
    else:
        print("❌ Failed to train ML model")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the API server: python api/app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Use the web interface to interact with the system")
    
    return True

if __name__ == "__main__":
    setup_system()
