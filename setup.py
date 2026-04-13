#!/usr/bin/env python3
"""
Setup script for Health Assessment Application
This script initializes the ML model and creates sample data.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_predictor import predictor

def setup_application():
    """Set up the application with ML model and sample data"""
    print("🏥 Health Assessment Application Setup")
    print("=" * 50)

    # Create necessary directories
    os.makedirs('static/data', exist_ok=True)
    os.makedirs('static/models', exist_ok=True)

    print("📁 Created necessary directories")

    # Create sample dataset and train model
    print("📊 Creating sample health dataset...")
    df = predictor.create_sample_dataset(2000)

    print("🤖 Training machine learning model...")
    accuracy = predictor.train_model(df)

    print(f"🎯 Model accuracy: {accuracy:.1f}")
    print("✅ Model saved to static/models/")

    # Test the model
    print("🧪 Testing model prediction...")
    test_data = {
        'age': 45,
        'bmi': 28.5,
        'smoking_status': 'former',
        'exercise_frequency': 'weekly',
        'family_history': 1,
        'medical_conditions': 0,
        'medications': 1
    }

    risk_level, confidence = predictor.predict_risk(test_data)
    print(f"   Test Result: {risk_level} risk")
    print(f"   Confidence: {confidence}")

    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the app: python app.py")
    print("3. Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    setup_application()