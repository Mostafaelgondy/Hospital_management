import pandas as pd
import numpy as np
import joblib
from typing import Dict, List, Any
import sqlite3

class TreatmentRecommendationSystem:
    def __init__(self, db_path='database/medical_data.db'):
        self.db_path = db_path
        self.treatment_guidelines = self.load_treatment_guidelines()
        self.patient_history = self.load_patient_history()
    
    def load_treatment_guidelines(self) -> Dict[str, Dict]:
        """Load evidence-based treatment guidelines for each disease"""
        return {
            'Hypertension': {
                'stages': {
                    'Stage 1': {'bp_range': (130, 139), 'dbp_range': (80, 89)},
                    'Stage 2': {'bp_range': (140, 179), 'dbp_range': (90, 119)},
                    'Crisis': {'bp_range': (180, 300), 'dbp_range': (120, 300)}
                },
                'treatments': {
                    'Stage 1': [
                        {
                            'type': 'Lifestyle',
                            'name': 'Dietary Changes',
                            'description': 'Reduce sodium intake, DASH diet',
                            'effectiveness': 0.7,
                            'duration': 'Lifelong',
                            'medications': [],
                            'monitoring': ['Monthly BP checks', 'Weight monitoring']
                        },
                        {
                            'type': 'Lifestyle',
                            'name': 'Exercise Regimen',
                            'description': 'Aerobic exercise 30 mins, 5 days/week',
                            'effectiveness': 0.6,
                            'duration': 'Continuous',
                            'medications': [],
                            'monitoring': ['BP response to exercise']
                        }
                    ],
                    'Stage 2': [
                        {
                            'type': 'Medication',
                            'name': 'First-line Antihypertensives',
                            'description': 'ACE inhibitors or ARBs',
                            'effectiveness': 0.85,
                            'duration': 'Long-term',
                            'medications': ['Lisinopril 10mg', 'Losartan 50mg'],
                            'monitoring': ['Renal function', 'Electrolytes']
                        },
                        {
                            'type': 'Combination',
                            'name': 'Lifestyle + Medication',
                            'description': 'Combined approach for better control',
                            'effectiveness': 0.92,
                            'duration': 'Long-term',
                            'medications': ['Lisinopril 10mg'],
                            'monitoring': ['Weekly BP', 'Renal function']
                        }
                    ],
                    'Crisis': [
                        {
                            'type': 'Emergency',
                            'name': 'Immediate Medical Care',
                            'description': 'Hospitalization and IV medications',
                            'effectiveness': 0.95,
                            'duration': 'Until stabilized',
                            'medications': ['IV Labetalol', 'IV Nitroprusside'],
                            'monitoring': ['Continuous BP', 'Cardiac monitoring']
                        }
                    ]
                }
            },
            'Diabetes': {
                'stages': {
                    'Pre-diabetes': {'a1c_range': (5.7, 6.4)},
                    'Type 2 Controlled': {'a1c_range': (6.5, 7.0)},
                    'Type 2 Uncontrolled': {'a1c_range': (7.1, 15.0)}
                },
                'treatments': {
                    'Pre-diabetes': [
                        {
                            'type': 'Lifestyle',
                            'name': 'Weight Management',
                            'description': '5-7% weight loss through diet and exercise',
                            'effectiveness': 0.8,
                            'duration': 'Lifelong',
                            'medications': ['Metformin 500mg (optional)'],
                            'monitoring': ['Quarterly A1c', 'Fasting glucose']
                        }
                    ],
                    'Type 2 Controlled': [
                        {
                            'type': 'Medication',
                            'name': 'First-line Therapy',
                            'description': 'Metformin with lifestyle modification',
                            'effectiveness': 0.75,
                            'duration': 'Long-term',
                            'medications': ['Metformin 1000mg daily'],
                            'monitoring': ['A1c every 3 months', 'Renal function']
                        }
                    ],
                    'Type 2 Uncontrolled': [
                        {
                            'type': 'Combination',
                            'name': 'Intensive Management',
                            'description': 'Multiple drug classes + insulin if needed',
                            'effectiveness': 0.88,
                            'duration': 'Long-term',
                            'medications': ['Metformin 1000mg', 'GLP-1 RA', 'Basal insulin'],
                            'monitoring': ['Frequent glucose checks', 'A1c monthly initially']
                        }
                    ]
                }
            },
            'Influenza': {
                'severity_levels': {
                    'Mild': {'symptoms': ['fever', 'cough'], 'duration_days': (1, 3)},
                    'Moderate': {'symptoms': ['fever', 'cough', 'fatigue'], 'duration_days': (4, 7)},
                    'Severe': {'symptoms': ['fever', 'cough', 'fatigue', 'shortness_breath'], 'duration_days': (7, 14)}
                },
                'treatments': {
                    'Mild': [
                        {
                            'type': 'Symptomatic',
                            'name': 'Home Care',
                            'description': 'Rest, hydration, OTC medications',
                            'effectiveness': 0.9,
                            'duration': '5-7 days',
                            'medications': ['Oseltamivir 75mg', 'Acetaminophen'],
                            'monitoring': ['Symptom resolution', 'Fever pattern']
                        }
                    ],
                    'Moderate': [
                        {
                            'type': 'Antiviral',
                            'name': 'Antiviral Therapy',
                            'description': 'Antiviral medications within 48 hours',
                            'effectiveness': 0.7,
                            'duration': '5 days',
                            'medications': ['Oseltamivir 75mg bid'],
                            'monitoring': ['Respiratory status', 'Fever curve']
                        }
                    ],
                    'Severe': [
                        {
                            'type': 'Hospital',
                            'name': 'Hospital Management',
                            'description': 'Inpatient care with IV fluids and monitoring',
                            'effectiveness': 0.85,
                            'duration': 'Until stable',
                            'medications': ['IV fluids', 'Oseltamivir', 'Antibiotics if bacterial'],
                            'monitoring': ['Oxygen saturation', 'Chest X-ray', 'Blood gases']
                        }
                    ]
                }
            },
            'Asthma': {
                'control_levels': {
                    'Well Controlled': {'symptoms_week': (0, 2), 'night_awakenings': (0, 2)},
                    'Not Well Controlled': {'symptoms_week': (3, 6), 'night_awakenings': (3, 4)},
                    'Poorly Controlled': {'symptoms_week': (7, 100), 'night_awakenings': (5, 100)}
                },
                'treatments': {
                    'Well Controlled': [
                        {
                            'type': 'Maintenance',
                            'name': 'Low-dose ICS',
                            'description': 'Inhaled corticosteroids as controller',
                            'effectiveness': 0.9,
                            'duration': 'Long-term',
                            'medications': ['Low-dose ICS', 'SABA prn'],
                            'monitoring': ['Asthma control test', 'PEF monitoring']
                        }
                    ],
                    'Not Well Controlled': [
                        {
                            'type': 'Step-up',
                            'name': 'Medium-dose ICS + LABA',
                            'description': 'Increase controller medication',
                            'effectiveness': 0.85,
                            'duration': '3 months then reassess',
                            'medications': ['Medium-dose ICS+LABA', 'SABA prn'],
                            'monitoring': ['ACT monthly', 'PEF daily']
                        }
                    ],
                    'Poorly Controlled': [
                        {
                            'type': 'Intensive',
                            'name': 'High-dose ICS + LABA + Oral steroids',
                            'description': 'Maximal medical therapy',
                            'effectiveness': 0.8,
                            'duration': 'Until controlled',
                            'medications': ['High-dose ICS+LABA', 'Oral steroids', 'SABA'],
                            'monitoring': ['Daily symptoms', 'PEF', 'Possible hospitalization']
                        }
                    ]
                }
            }
        }
    
    def load_patient_history(self):
        """Load patient treatment history from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT patient_id, diagnosis, treatment, medication, exam_date 
            FROM examinations 
            WHERE treatment IS NOT NULL
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except:
            return pd.DataFrame()
    
    def determine_disease_stage(self, disease: str, patient_data: Dict) -> str:
        """Determine the stage/severity of the disease based on patient data"""
        if disease == 'Hypertension':
            bp_sys = patient_data.get('blood_pressure_sys', 120)
            bp_dia = patient_data.get('blood_pressure_dia', 80)
            
            if bp_sys >= 180 or bp_dia >= 120:
                return 'Crisis'
            elif bp_sys >= 140 or bp_dia >= 90:
                return 'Stage 2'
            else:
                return 'Stage 1'
                
        elif disease == 'Diabetes':
            blood_sugar = patient_data.get('blood_sugar', 100)
            # For demonstration - in real system would use A1c
            if blood_sugar > 200:
                return 'Type 2 Uncontrolled'
            elif blood_sugar > 126:
                return 'Type 2 Controlled'
            else:
                return 'Pre-diabetes'
                
        elif disease == 'Influenza':
            symptom_count = sum(1 for symptom in ['fever', 'cough', 'fatigue', 'shortness_breath'] 
                              if patient_data.get(symptom, 0) == 1)
            if symptom_count >= 3:
                return 'Severe'
            elif symptom_count >= 2:
                return 'Moderate'
            else:
                return 'Mild'
                
        elif disease == 'Asthma':
            # Simplified assessment
            if patient_data.get('shortness_breath', 0) == 1 and patient_data.get('wheezing', 0) == 1:
                return 'Poorly Controlled'
            elif patient_data.get('shortness_breath', 0) == 1:
                return 'Not Well Controlled'
            else:
                return 'Well Controlled'
        
        return 'Standard'
    
    def personalize_treatment(self, disease: str, stage: str, patient_data: Dict) -> List[Dict]:
        """Personalize treatments based on patient characteristics"""
        base_treatments = self.treatment_guidelines.get(disease, {}).get('treatments', {}).get(stage, [])
        
        personalized_treatments = []
        
        for treatment in base_treatments:
            personalized_treatment = treatment.copy()
            
            # Personalize based on age
            age = patient_data.get('age', 45)
            if age > 65:
                if 'medications' in personalized_treatment:
                    # Adjust medications for elderly
                    personalized_treatment['description'] += " (Adjusted for geriatric patient)"
                    personalized_treatment['monitoring'].append('Fall risk assessment')
            
            # Personalize based on BMI
            bmi = patient_data.get('bmi', 25)
            if bmi > 30 and disease in ['Hypertension', 'Diabetes']:
                personalized_treatment['description'] += " - Focus on weight management"
                if 'Lifestyle' in personalized_treatment['type']:
                    personalized_treatment['effectiveness'] *= 1.1
            
            # Personalize based on comorbidities
            if patient_data.get('cholesterol', 200) > 240:
                personalized_treatment['monitoring'].append('Lipid profile')
            
            personalized_treatments.append(personalized_treatment)
        
        return personalized_treatments
    
    def calculate_treatment_score(self, treatment: Dict, patient_data: Dict) -> float:
        """Calculate a suitability score for treatment based on patient factors"""
        score = treatment.get('effectiveness', 0.5)
        
        # Adjust based on age
        age = patient_data.get('age', 45)
        if age > 65 and treatment['type'] == 'Medication':
            score *= 0.9  # Slightly reduce score for elderly due to polypharmacy concerns
        
        # Adjust based on complexity
        med_count = len(treatment.get('medications', []))
        if med_count > 2:
            score *= 0.85  # Preference for simpler regimens
        
        # Boost for lifestyle interventions in obese patients
        bmi = patient_data.get('bmi', 25)
        if bmi > 30 and treatment['type'] == 'Lifestyle':
            score *= 1.2
        
        return round(score, 2)
    
    def recommend_treatments(self, disease: str, patient_data: Dict) -> Dict[str, Any]:
        """Generate personalized treatment recommendations"""
        if disease not in self.treatment_guidelines:
            return {
                'error': f'No treatment guidelines available for {disease}'
            }
        
        # Determine disease stage
        stage = self.determine_disease_stage(disease, patient_data)
        
        # Get personalized treatments
        treatments = self.personalize_treatment(disease, stage, patient_data)
        
        # Score and rank treatments
        scored_treatments = []
        for treatment in treatments:
            score = self.calculate_treatment_score(treatment, patient_data)
            scored_treatment = treatment.copy()
            scored_treatment['suitability_score'] = score
            scored_treatment['recommendation_rank'] = len([t for t in scored_treatments if t['suitability_score'] > score]) + 1
            scored_treatments.append(scored_treatment)
        
        # Sort by score
        scored_treatments.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return {
            'disease': disease,
            'stage': stage,
            'treatments': scored_treatments,
            'recommendation_count': len(scored_treatments),
            'top_recommendation': scored_treatments[0] if scored_treatments else None
        }

# Global instance
treatment_system = TreatmentRecommendationSystem()