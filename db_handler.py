import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
import time

SERVICE_ACCOUNT_KEY = 'attendance-management-98055-firebase-adminsdk-fbsvc-23ecb43446.json'
ADMIN_PIN = "1234"
db = None

def init_firebase_db():
    global db

    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred)

            db = firestore.client()
            st.success("🔥 Firebase connection established successfully!")
            return True
        except FileNotFoundError:
            st.error(f"❌ CRITICAL: Firebase Service Account Key not found at '{SERVICE_ACCOUNT_KEY}'. Data operations are disabled.")
            db = None
            return False
        except Exception as e:
            st.error(f"❌ Firebase Initialization Error: {e}")
            db = None
            return False
    else:
        db = firestore.client()
        return True


def register_student_db(student_id, name):
    if db:
        student_ref = db.collection('students').document(student_id)

        if student_ref.get().exists:
            return False

        data = {
            'name': name,
            'registered_on': firestore.SERVER_TIMESTAMP
        }
        student_ref.set(data)
        return True
    return False

def record_attendance_db(student_id, entry_type):
    if db:
        student_ref = db.collection('students').document(student_id)
        student_doc = student_ref.get()
        if not student_doc.exists:
            return False

        data = {
            'id': student_id,
            'name': student_doc.to_dict().get('name', 'Unknown Student'),
            'type': entry_type,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        db.collection('attendance_logs').add(data)
        return True
    return False

def get_all_students_db():
    if db:
        students = {}
        try:
            for doc in db.collection('students').stream():
                data = doc.to_dict()
                students[doc.id] = {'name': data.get('name', 'Unknown'), 'registered_on': data.get('registered_on', None)}
            return students
        except Exception as e:
            st.error(f"Error fetching students: {e}")
            return {}
    return {}


def get_attendance_records_db():
    if db:
        logs = []
        try:
            query = db.collection('attendance_logs').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
            for doc in query:
                log = doc.to_dict()
                if log.get('timestamp'):
                    log['timestamp'] = log['timestamp'].astimezone().isoformat()
                logs.append(log)
            return logs
        except Exception as e:
            st.error(f"Error fetching attendance logs: {e}")
            return []
    return []

def delete_student_db(student_id):
    if db:
        try:
            student_ref = db.collection('students').document(student_id)

            if student_ref.get().exists:
                student_ref.delete()
                return True
            else:
                return False
        except Exception as e:
            st.error(f"Firestore deletion error: {e}")
            return False
    return False
