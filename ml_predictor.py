import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class HealthRiskPredictor:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = [
            'age', 'bmi', 'medical_conditions', 'exercise_frequency', 'smoking_status'
        ]

    def create_sample_dataset(self, n_samples=1000):
        """Create a sample health dataset for training"""
        np.random.seed(42)

        data = {
            'age': np.random.randint(18, 80, n_samples),
            'bmi': np.random.normal(25, 5, n_samples).clip(15, 50),
            'smoking_status': np.random.choice(['never', 'former', 'current'], n_samples, p=[0.6, 0.3, 0.1]),
            'exercise_frequency': np.random.choice(['never', 'rarely', 'monthly', 'weekly', 'daily'], n_samples,
                                                 p=[0.1, 0.2, 0.2, 0.3, 0.2]),
            'medical_conditions': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        }

        # Create risk level based on factors
        risk_scores = []
        for i in range(n_samples):
            score = 0
            if data['age'][i] > 60: score += 3
            elif data['age'][i] > 40: score += 2

            if data['bmi'][i] > 30: score += 3
            elif data['bmi'][i] > 25: score += 2
            elif data['bmi'][i] < 18.5: score += 1

            if data['smoking_status'][i] == 'current': score += 3
            elif data['smoking_status'][i] == 'former': score += 1

            if data['exercise_frequency'][i] in ['never', 'rarely']: score += 2
            elif data['exercise_frequency'][i] == 'daily': score -= 1

            if data['medical_conditions'][i]: score += 3

            if score >= 8: risk_level = 'High'
            elif score >= 5: risk_level = 'Medium'
            else: risk_level = 'Low'

            risk_scores.append(risk_level)

        data['risk_level'] = risk_scores
        df = pd.DataFrame(data)

        # Save to CSV
        df.to_csv('static/data/sample_health_data.csv', index=False)
        return df

    def preprocess_data(self, df):
        """Preprocess the data for training"""
        # Encode categorical variables
        categorical_cols = ['smoking_status', 'exercise_frequency']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            df[col] = self.label_encoders[col].fit_transform(df[col])

        # Prepare features and target
        X = df[self.feature_columns]
        y = df['risk_level']

        # Encode target
        target_encoder = LabelEncoder()
        y_encoded = target_encoder.fit_transform(y)

        return X, y_encoded, target_encoder

    def train_model(self, df=None):
        """Train the risk prediction model"""
        if df is None:
            df = self.create_sample_dataset()

        X, y_encoded, target_encoder = self.preprocess_data(df)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Model Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

        # Save model and encoders
        os.makedirs('static/models', exist_ok=True)
        joblib.dump(self.model, 'static/models/risk_predictor.pkl')
        joblib.dump(self.scaler, 'static/models/scaler.pkl')
        joblib.dump(self.label_encoders, 'static/models/label_encoders.pkl')
        joblib.dump(target_encoder, 'static/models/target_encoder.pkl')

        return accuracy

    def predict_risk(self, user_data):
        """Predict risk level for new user data"""
        if not self.model:
            self.load_model()

        # Prepare user data
        df = pd.DataFrame([user_data])

        # Encode categorical variables
        for col, encoder in self.label_encoders.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col])

        # Select features
        X = df[self.feature_columns]

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict
        prediction = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)

        # Load target encoder to get class names
        target_encoder = joblib.load('static/models/target_encoder.pkl')
        risk_level = target_encoder.inverse_transform(prediction)[0]

        # Get confidence scores
        confidence_scores = dict(zip(target_encoder.classes_, probabilities[0]))

        return risk_level, confidence_scores

    def load_model(self):
        """Load trained model and encoders"""
        try:
            self.model = joblib.load('static/models/risk_predictor.pkl')
            self.scaler = joblib.load('static/models/scaler.pkl')
            self.label_encoders = joblib.load('static/models/label_encoders.pkl')
        except FileNotFoundError:
            print("Model not found. Training new model...")
            self.train_model()

    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if not self.model:
            self.load_model()

        importance = self.model.feature_importances_
        return dict(zip(self.feature_columns, importance))

    def get_health_statistics(self):
        """Get statistics from the training data"""
        try:
            df = pd.read_csv('static/data/sample_health_data.csv')

            stats = {
                'total_samples': int(len(df)),
                'age_distribution': {
                    'mean': float(df['age'].mean()),
                    'median': float(df['age'].median()),
                    'min': int(df['age'].min()),
                    'max': int(df['age'].max())
                },
                'bmi_distribution': {
                    'mean': float(df['bmi'].mean()),
                    'median': float(df['bmi'].median()),
                    'underweight': int((df['bmi'] < 18.5).sum()),
                    'normal': int(((df['bmi'] >= 18.5) & (df['bmi'] < 25)).sum()),
                    'overweight': int(((df['bmi'] >= 25) & (df['bmi'] < 30)).sum()),
                    'obese': int((df['bmi'] >= 30).sum())
                },
                'risk_distribution': {k: int(v) for k, v in df['risk_level'].value_counts().to_dict().items()},
                'smoking_stats': {k: int(v) for k, v in df['smoking_status'].value_counts().to_dict().items()},
                'exercise_stats': {k: int(v) for k, v in df['exercise_frequency'].value_counts().to_dict().items()}
            }

            return stats
        except FileNotFoundError:
            return None

# Initialize predictor
predictor = HealthRiskPredictor()

if __name__ == "__main__":
    # Create sample dataset and train model
    print("Creating sample health dataset...")
    df = predictor.create_sample_dataset(2000)

    print("Training risk prediction model...")
    accuracy = predictor.train_model(df)

    print(f"\nModel trained with {accuracy:.2%} accuracy")

    # Test prediction
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
    print(f"\nTest Prediction: {risk_level}")
    print(f"Confidence Scores: {confidence}")