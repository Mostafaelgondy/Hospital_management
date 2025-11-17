import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

class MedicalDataGenerator:
    def __init__(self):
        self.diseases = {
            'Hypertension': {'symptoms': ['headache', 'dizziness', 'chest_pain'], 'age_group': 'adult_elderly'},
            'Diabetes': {'symptoms': ['fatigue', 'frequent_urination', 'thirst'], 'age_group': 'adult_elderly'},
            'Influenza': {'symptoms': ['fever', 'cough', 'fatigue'], 'age_group': 'all'},
            'Asthma': {'symptoms': ['shortness_breath', 'wheezing', 'chest_tightness'], 'age_group': 'all'},
            'Arthritis': {'symptoms': ['joint_pain', 'swelling', 'stiffness'], 'age_group': 'elderly'},
            'Migraine': {'symptoms': ['headache', 'nausea', 'sensitivity_light'], 'age_group': 'adult'},
            'Gastritis': {'symptoms': ['abdominal_pain', 'nausea', 'bloating'], 'age_group': 'all'},
            'Bronchitis': {'symptoms': ['cough', 'fever', 'fatigue'], 'age_group': 'all'}
        }
        
        self.symptoms_list = [
            'headache', 'dizziness', 'chest_pain', 'fatigue', 'frequent_urination',
            'thirst', 'fever', 'cough', 'shortness_breath', 'wheezing',
            'chest_tightness', 'joint_pain', 'swelling', 'stiffness', 'nausea',
            'sensitivity_light', 'abdominal_pain', 'bloating'
        ]
    
    def generate_patient_data(self, n_samples=500):
        """Generate synthetic patient data with medical conditions"""
        np.random.seed(42)
        
        data = []
        for i in range(n_samples):
            age = np.random.randint(1, 90)
            gender = np.random.choice(['M', 'F'])
            bmi = np.random.normal(25, 5)
            blood_pressure_sys = np.random.normal(120, 15)
            blood_pressure_dia = np.random.normal(80, 10)
            cholesterol = np.random.normal(200, 40)
            blood_sugar = np.random.normal(100, 20)
            
            # Select a disease based on age
            available_diseases = []
            for disease, info in self.diseases.items():
                if info['age_group'] == 'all':
                    available_diseases.append(disease)
                elif info['age_group'] == 'adult' and age >= 18:
                    available_diseases.append(disease)
                elif info['age_group'] == 'adult_elderly' and age >= 30:
                    available_diseases.append(disease)
                elif info['age_group'] == 'elderly' and age >= 50:
                    available_diseases.append(disease)
            
            if not available_diseases:
                disease = np.random.choice(list(self.diseases.keys()))
            else:
                disease = np.random.choice(available_diseases)
            
            # Generate symptoms based on the disease
            disease_symptoms = self.diseases[disease]['symptoms']
            symptoms = {symptom: 0 for symptom in self.symptoms_list}
            
            for symptom in disease_symptoms:
                symptoms[symptom] = 1
            
            # Add some random secondary symptoms
            num_secondary = np.random.randint(0, 3)
            secondary_symptoms = np.random.choice(
                [s for s in self.symptoms_list if s not in disease_symptoms],
                num_secondary, replace=False
            )
            for symptom in secondary_symptoms:
                symptoms[symptom] = 1
            
            patient_record = {
                'patient_id': i + 1,
                'age': age,
                'gender': gender,
                'bmi': max(15, min(40, bmi)),
                'blood_pressure_sys': max(80, min(180, blood_pressure_sys)),
                'blood_pressure_dia': max(50, min(120, blood_pressure_dia)),
                'cholesterol': max(150, min(300, cholesterol)),
                'blood_sugar': max(70, min(200, blood_sugar)),
                'disease': disease
            }
            
            patient_record.update(symptoms)
            data.append(patient_record)
        
        return pd.DataFrame(data)

def train_disease_model():
    """Main function to train the disease prediction model"""
    print("=== Medical Disease Prediction Model Training ===")
    
    # Generate data
    print("Generating medical dataset...")
    generator = MedicalDataGenerator()
    df = generator.generate_patient_data(500)
    print(f"Dataset generated with {len(df)} records")
    
    # Data exploration
    print("\nDataset Overview:")
    print(f"Shape: {df.shape}")
    print(f"Disease distribution:\n{df['disease'].value_counts()}")
    
    # Visualizations
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 3, 1)
    df['disease'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Disease Distribution')
    plt.xticks(rotation=45)
    
    plt.subplot(2, 3, 2)
    df['gender'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Gender Distribution')
    
    plt.tight_layout()
    plt.show()
    
    # Preprocessing
    print("Preprocessing data...")
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['gender']
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Encode target variable
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(df['disease'])
    
    # Prepare features
    symptom_columns = generator.symptoms_list
    feature_columns = ['age', 'gender', 'bmi', 'blood_pressure_sys', 
                       'blood_pressure_dia', 'cholesterol', 'blood_sugar'] + symptom_columns
    
    X = df[feature_columns]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_columns = ['age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia', 
                         'cholesterol', 'blood_sugar']
    
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[numerical_columns] = scaler.fit_transform(X_train[numerical_columns])
    X_test_scaled[numerical_columns] = scaler.transform(X_test[numerical_columns])
    
    # Model training
    print("Training models...")
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        
        if name == 'Decision Tree':
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        else:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred
        }
        
        print(f"{name} Accuracy: {accuracy:.4f}")
    
    # Select best model
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['model']
    best_accuracy = results[best_model_name]['accuracy']
    
    print(f"\nBest Model: {best_model_name}")
    print(f"Best Accuracy: {best_accuracy:.4f}")
    
    # Save model
    model_package = {
        'model': best_model,
        'scaler': scaler if best_model_name == 'Random Forest' else None,
        'target_encoder': target_encoder,
        'feature_columns': feature_columns,
        'symptoms_list': generator.symptoms_list,
        'diseases_info': generator.diseases,
        'model_type': best_model_name
    }
    
    joblib.dump(model_package, 'disease_prediction_model.pkl')
    print("Model saved as 'disease_prediction_model.pkl'")
    
    # Evaluation
    print("\n=== Model Evaluation ===")
    print(classification_report(y_test, results[best_model_name]['predictions'], 
                              target_names=target_encoder.classes_))
    
    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10))
    
    return best_accuracy

if __name__ == "__main__":
    accuracy = train_disease_model()
    print(f"\n Model training completed with accuracy: {accuracy:.2%}")