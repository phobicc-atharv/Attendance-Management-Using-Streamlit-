import streamlit as st
from db_handler import init_firebase_db, ADMIN_PIN
from student_page import student_attendance_page
from admin_page import admin_page

def apply_custom_css():
    st.markdown("""
        <style>
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .stApp {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffffff
            background-size: 400% 400%;
            animation: gradient-shift 15s ease infinite;
        }

        .st-emotion-cache-18ni91u, .st-emotion-cache-h5rbmh {
            padding-top: 1rem;
        }

        .st-emotion-cache-16txte5 {
            background-color: #e0e6f0;
            border-right: 2px solid #ccd2e0;
            box-shadow: 4px 0 10px rgba(0,0,0,0.15);
            transition: background-color 0.3s ease;
        }
        .st-emotion-cache-1r6r8n7 {
            font-size: 1.6rem;
            font-weight: 700;
            color: #1a1a1a;
        }

        div[data-testid="stMetric"] > div {
             border-radius: 15px;
             padding: 20px;
             box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
             transition: transform 0.4s ease-in-out, box-shadow 0.4s ease-in-out;
        }
        div[data-testid="stMetric"] > div:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(30, 144, 255, 0.4);
        }

        [data-testid="stColumn"] button {
            transition: all 0.4s ease-in-out;
            font-weight: bold;
            height: 5rem;
            font-size: 1.35rem;
            border-radius: 12px;
        }

        [data-testid*="stColumn"] button[kind="primary"] {
            background-color: #008080;
            border: none;
        }
        [data-testid*="stColumn"] button[kind="primary"]:hover {
            background-color: #005f5f;
            box-shadow: 0 6px 15px rgba(0, 128, 128, 0.6);
        }

        [data-testid*="stColumn"] button[kind="secondary"] {
            background-color: #ff8c00;
            color: #fff;
            border: none;
        }
        [data-testid*="stColumn"] button[kind="secondary"]:hover {
            background-color: #cc7000;
            box-shadow: 0 6px 15px rgba(255, 140, 0, 0.6);
        }

        div[data-testid="stHorizontalBlock"] > div:first-child > div:nth-child(2) {
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }

        .stAlert {
            border-radius: 10px;
        }

        button:has(> div > p) {
              transition: all 0.4s ease-in-out;
        }

        div[data-testid="stVerticalBlock"] button[kind="secondary"]:not(:hover) {
            background-color: #dc3545 !important;
            color: white !important;
        }
        div[data-testid="stVerticalBlock"] button[kind="secondary"]:hover {
            background-color: #c82333 !important;
        }


        </style>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Attendance Manager Pro", layout="wide")

    apply_custom_css()

    init_firebase_db()

    st.sidebar.title("📚 Attendance Manager Pro")
    st.sidebar.markdown("---")

    mode = st.sidebar.radio("🔍 Select Mode", ["Student Access", "Admin Access"])

    st.sidebar.markdown(
        """
        <style>
        div[data-testid="stSidebar"] div[role="radiogroup"] {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            background-color: #f7f7f7;
        }
        </style>
        """, unsafe_allow_html=True
    )

    if mode == "Student Access":
        student_attendance_page()

    elif mode == "Admin Access":
        if 'admin_logged_in' not in st.session_state:
            st.session_state.admin_logged_in = False

        if st.session_state.admin_logged_in:
            admin_page()
            if st.sidebar.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
        else:
            st.header("🔑 Admin Login")
            pin = st.text_input("Enter Admin PIN", type="password", key="admin_pin_input")

            if st.button("✅ Login"):
                if pin == ADMIN_PIN:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid PIN.")
            st.info(f"💡 Hint: The mock admin PIN is `{ADMIN_PIN}`")

if __name__ == "__main__":
    main()
