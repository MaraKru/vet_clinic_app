import sqlite3
import pandas as pd
import streamlit as st


DB_FILE = "vet_clinic.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            drug TEXT NOT NULL,
            weight REAL NOT NULL,
            detail TEXT NOT NULL,
            dose REAL NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
    """)
    # ON DELETE CASCADE = if you delete a pet, its prescriptions will be deleted

    conn.commit()   # saves changes
    conn.close() 


def get_all_patients():
    conn = get_db_connection()
    df_patients = pd.read_sql("SELECT * FROM patients ORDER BY name", conn)
    df_prescriptions = pd.read_sql("SELECT * FROM prescriptions", conn)
    conn.close()
    return df_patients, df_prescriptions


def add_patient_record(pet_name, species, drug, weight, detail, dose_val, record_type):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM patients WHERE name = ?", (pet_name,))
        patient = cur.fetchone()  # it gives me the data (if it exists)
        
        if patient:
            patient_id = patient[0]  
            # cause fetchone gives a tuple like "(5,)", we should access by index
        else:
            cur.execute("INSERT INTO patients (name, species) VALUES (?, ?)", (pet_name, species))
            patient_id = cur.lastrowid  # we should know that id a db just created 
            
        cur.execute("""
            INSERT INTO prescriptions (patient_id, drug, weight, detail, dose, type) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (patient_id, drug, weight, detail, dose_val, record_type))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()  # delete all Ive done if 
        st.error(f"Ошибка при сохранении: {e}")  # failed to save
        return False
    finally:   # it always executed
        conn.close()


def delete_patient_from_db(pet_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE name = ?", (pet_name,))
    conn.commit()
    conn.close()


def clear_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM prescriptions")
    cur.execute("DELETE FROM patients")
    conn.commit()
    conn.close()