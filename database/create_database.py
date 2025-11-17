import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

class MedicalDatabase:
    def __init__(self, db_path='medical_data.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
                phone_number TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS examinations (
                exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                exam_date DATE NOT NULL,
                physician_id INTEGER,
                symptoms TEXT,
                diagnosis TEXT,
                treatment TEXT,
                medication TEXT,
                next_appointment DATE,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                role TEXT CHECK(role IN ('physician', 'supervisor', 'ministry')) NOT NULL,
                department TEXT,
                full_name TEXT NOT NULL
            )
        ''')
        
        # Insert sample data if tables are empty
        if not cursor.execute("SELECT COUNT(*) FROM patients").fetchone()[0]:
            self.insert_sample_data(conn)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    def insert_sample_data(self, conn):
        """Insert sample data into the database"""
        cursor = conn.cursor()
        
        # Sample patients
        patients = [
            ('John', 'Smith', '1985-03-15', 'M', '+1-555-0101'),
            ('Maria', 'Garcia', '1978-07-22', 'F', '+1-555-0102'),
            ('David', 'Johnson', '1992-11-30', 'M', '+1-555-0103'),
            ('Sarah', 'Williams', '1988-05-14', 'F', '+1-555-0104'),
            ('Michael', 'Brown', '1975-09-08', 'M', '+1-555-0105'),
            ('Emily', 'Davis', '1995-12-03', 'F', '+1-555-0106'),
            ('Robert', 'Miller', '1982-02-19', 'M', '+1-555-0107'),
            ('Lisa', 'Wilson', '1970-08-11', 'F', '+1-555-0108'),
            ('James', 'Taylor', '1990-04-25', 'M', '+1-555-0109'),
            ('Jennifer', 'Anderson', '1987-06-17', 'F', '+1-555-0110'),
            ('Daniel', 'Thomas', '1973-01-29', 'M', '+1-555-0111'),
            ('Jessica', 'Jackson', '1993-10-05', 'F', '+1-555-0112'),
            ('William', 'White', '1968-03-12', 'M', '+1-555-0113'),
            ('Amanda', 'Harris', '1984-07-08', 'F', '+1-555-0114'),
            ('Christopher', 'Martin', '1979-11-21', 'M', '+1-555-0115')
        ]
        
        cursor.executemany('''
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone_number)
            VALUES (?, ?, ?, ?, ?)
        ''', patients)
        
        # Sample users
        users = [
            ('dr_smith', 'physician', 'Cardiology', 'Dr. Sarah Smith'),
            ('dr_johnson', 'physician', 'Neurology', 'Dr. Mark Johnson'),
            ('super_lee', 'supervisor', 'Administration', 'Supervisor Lee'),
            ('ministry_health', 'ministry', 'Public Health', 'Ministry Official')
        ]
        
        cursor.executemany('''
            INSERT INTO users (username, role, department, full_name)
            VALUES (?, ?, ?, ?)
        ''', users)
        
        # Sample examinations
        symptoms_diagnosis = [
            ('Chest pain, shortness of breath', 'Hypertension', 'Lifestyle changes, medication', 'Lisinopril 10mg'),
            ('Headache, dizziness', 'Migraine', 'Rest, hydration', 'Ibuprofen 400mg'),
            ('Fever, cough, fatigue', 'Influenza', 'Rest, fluids', 'Tamiflu 75mg'),
            ('Joint pain, swelling', 'Rheumatoid Arthritis', 'Physical therapy', 'Methotrexate 15mg'),
            ('Abdominal pain, nausea', 'Gastritis', 'Diet modification', 'Omeprazole 20mg'),
            ('Back pain, limited mobility', 'Herniated Disc', 'Physical therapy', 'Naproxen 500mg'),
            ('Skin rash, itching', 'Contact Dermatitis', 'Topical treatment', 'Hydrocortisone cream'),
            ('Sore throat, fever', 'Strep Throat', 'Antibiotics', 'Amoxicillin 500mg'),
            ('Eye redness, discharge', 'Conjunctivitis', 'Eye drops', 'Tobramycin drops'),
            ('Shortness of breath, wheezing', 'Asthma', 'Inhaler therapy', 'Albuterol inhaler')
        ]
        
        examinations = []
        for i, (symptoms, diagnosis, treatment, medication) in enumerate(symptoms_diagnosis):
            patient_id = (i % 15) + 1
            exam_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            physician_id = random.randint(1, 2)
            next_appointment = (datetime.now() + timedelta(days=random.randint(14, 90))).strftime('%Y-%m-%d')
            
            examinations.append((
                patient_id, exam_date, physician_id, symptoms, 
                diagnosis, treatment, medication, next_appointment
            ))
        
        cursor.executemany('''
            INSERT INTO examinations 
            (patient_id, exam_date, physician_id, symptoms, diagnosis, treatment, medication, next_appointment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', examinations)
        
        print("Sample data inserted successfully!")

    def export_to_csv(self):
        """Export database tables to CSV files"""
        conn = sqlite3.connect(self.db_path)
        
        # Export patients
        patients_df = pd.read_sql_query('''
            SELECT patient_id, first_name, last_name, date_of_birth, gender 
            FROM patients
        ''', conn)
        patients_df.to_csv('patients_sample.csv', index=False)
        
        # Export examinations
        exams_df = pd.read_sql_query('''
            SELECT e.*, p.first_name, p.last_name 
            FROM examinations e 
            JOIN patients p ON e.patient_id = p.patient_id
        ''', conn)
        exams_df.to_csv('examinations_sample.csv', index=False)
        
        conn.close()
        print("CSV files exported successfully!")

# Create and populate the database
if __name__ == "__main__":
    db = MedicalDatabase()
    db.export_to_csv()