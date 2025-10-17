import streamlit as st
from db_handler import get_all_students_db, record_attendance_db, get_attendance_records_db, init_firebase_db
from datetime import datetime
import pandas as pd

def student_attendance_page():
    st.header("⌚ Student Check-In/Check-Out System")
    st.markdown("---")

    current_students = get_all_students_db()

    student_id = st.text_input("🔑 Enter your Student ID (e.g., S001)", key="student_id_input").upper().strip()
    student_name = current_students.get(student_id, {}).get('name')

    if student_id:
        if student_name:
            st.success(f"👋 Welcome back, **{student_name}**! Please record your attendance below.")
        else:
            st.warning("⚠️ Invalid Student ID. Please ensure your ID is correct.")
            return

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚪 CHECK IN", type="primary", use_container_width=True, help="Record your start time"):
                if student_id and student_name:
                    if record_attendance_db(student_id, 'IN'):
                        st.toast(f"✅ Check-In successful for {student_name}", icon="✅")
                    else:
                        st.error("Error recording attendance. Is the Firebase connection active?")
                else:
                    st.error("Please enter your Student ID first.")

        with col2:
            if st.button("🚶 CHECK OUT", type="secondary", use_container_width=True, help="Record your end time"):
                if student_id and student_name:
                    if record_attendance_db(student_id, 'OUT'):
                        st.toast(f"👋 Check-Out successful for {student_name}", icon="👋")
                    else:
                        st.error("Error recording attendance. Is the Firebase connection active?")
                else:
                    st.error("Please enter your Student ID first.")

    st.markdown("---")

    if student_id and student_name:
        st.subheader(f"📊 Recent Activity")

        all_logs = get_attendance_records_db()
        recent_logs = [log for log in all_logs if log.get('id') == student_id]

        if recent_logs:
            recent_df = pd.DataFrame(recent_logs).sort_values(by='timestamp', ascending=False).head(10)
            recent_df['Time'] = pd.to_datetime(recent_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

            st.dataframe(
                recent_df[['Time', 'type']].rename(columns={'type': 'Type'}),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Type": st.column_config.Column(
                        "Type",
                        help="Check-In or Check-Out",
                        width="small",
                    )
                }
            )
        else:
            st.info("No recent records found for this student.")

if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Student Attendance")
    if 'init_success' not in st.session_state:
        st.session_state.init_success = init_firebase_db()

    if st.session_state.init_success:
        student_attendance_page()
    else:
        st.error("Cannot run student page: Firebase connection failed.")
