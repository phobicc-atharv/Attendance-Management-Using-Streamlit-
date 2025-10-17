import streamlit as st
import pandas as pd
from datetime import datetime
import time

try:
    from db_handler import (
        get_all_students_db,
        get_attendance_records_db,
        register_student_db,
        delete_student_db
    )
except ImportError:
    st.error("Error: Could not import database functions from db_handler.py. Please ensure 'db_handler.py' exists.")


def admin_page():
    st.header("⭐ Admin Dashboard")
    st.markdown("---")

    all_students = get_all_students_db()
    all_logs = get_attendance_records_db()

    col_m1, col_m2, col_m3 = st.columns(3)

    total_students = len(all_students)
    total_logs = len(all_logs)

    col_m1.metric("Total Registered Students 🧑‍🎓", total_students)
    col_m2.metric("Total Attendance Logs 📝", total_logs)

    unique_checkins_today = 0
    if all_logs:
        today = datetime.now().date().isoformat()
        logs_df = pd.DataFrame(all_logs)
        logs_df['Date'] = pd.to_datetime(logs_df['timestamp']).dt.date.astype(str)
        logs_today = logs_df[(logs_df['Date'] == today) & (logs_df['type'] == 'IN')]
        unique_checkins_today = logs_today['id'].nunique()

    col_m3.metric("Unique Check-ins Today ✅", unique_checkins_today)

    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Full Attendance Report", "➕ Student Management"])

    with tab1:
        st.subheader("Attendance Log Viewer")

        if all_logs:
            df = pd.DataFrame(all_logs)

            df['Time'] = pd.to_datetime(df['timestamp'])
            df['Date'] = df['Time'].dt.date
            df['Clock Time'] = df['Time'].dt.strftime('%H:%M:%S')

            st.dataframe(
                df[['id', 'name', 'Date', 'Clock Time', 'type']].rename(
                    columns={'id': 'ID', 'name': 'Student Name', 'type': 'Type'}
                ).sort_values(by=['Date', 'Clock Time'], ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Type": st.column_config.SelectboxColumn(
                        "Type",
                        options=["IN", "OUT"],
                        default="IN",
                        disabled=True,
                    )
                }
            )

            @st.cache_data
            def convert_df(data_frame):
                return data_frame.to_csv(index=False).encode('utf-8')

            csv = convert_df(df)

            st.download_button(
                label="📥 Download Full Report CSV",
                data=csv,
                file_name='full_attendance_report.csv',
                mime='text/csv',
                help="Download the complete attendance log."
            )
        else:
            st.info("No attendance records found yet.")

    with tab2:
        col_reg, col_list = st.columns(2)

        with col_reg:
            st.subheader("Register New Student ➕")
            new_id = st.text_input("Student ID (e.g., S003)", key="new_student_id").upper().strip()
            new_name = st.text_input("Student Full Name", key="new_student_name").strip()

            if st.button("Register Student", type="primary", use_container_width=True):
                if new_id and new_name:
                    if register_student_db(new_id, new_name):
                        st.success(f"🎉 Student **{new_name}** registered with ID: **{new_id}**.")
                        st.rerun()
                    else:
                        st.warning(f"Student ID **{new_id}** already exists or Firebase is disconnected.")
                else:
                    st.error("Please fill in both Student ID and Name.")

            st.markdown("---")
            st.subheader("Delete Existing Student 🗑️")

            if 'delete_confirm_id' not in st.session_state:
                st.session_state.delete_confirm_id = None

            delete_id = st.text_input("Student ID to Delete (e.g., S001)", key="delete_student_id").upper().strip()

            if st.session_state.delete_confirm_id == delete_id and delete_id:
                st.warning(f"Are you sure you want to permanently delete Student ID **{delete_id}**? This cannot be undone.", icon="⚠️")

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    if st.button("Confirm DELETE", key="confirm_delete_btn", type="primary", use_container_width=True):
                        if delete_student_db(delete_id):
                            st.success(f"🗑️ Student with ID **{delete_id}** has been successfully deleted.")
                            st.session_state.delete_confirm_id = None
                            st.rerun()
                        else:
                            st.error(f"Deletion failed. Student ID **{delete_id}** not found or database error occurred.")
                with col_c2:
                    if st.button("Cancel", key="cancel_delete_btn", use_container_width=True):
                        st.session_state.delete_confirm_id = None
                        st.info("Deletion canceled.")
                        st.rerun()

            elif st.button("Initiate Delete", key="initiate_delete_btn", type="secondary", use_container_width=True):
                if delete_id:
                    if delete_id in all_students:
                        st.session_state.delete_confirm_id = delete_id
                        st.rerun()
                    else:
                        st.error(f"Student ID **{delete_id}** not found.")
                else:
                    st.error("Please enter the Student ID to delete.")

        with col_list:
            st.subheader("Currently Registered Students 📋")

            current_students = get_all_students_db()
            student_list = [{'ID': k, 'Name': v['name']} for k, v in current_students.items()]

            if student_list:
                   st.dataframe(
                       pd.DataFrame(student_list),
                       use_container_width=True,
                       hide_index=True,
                       column_config={
                           "ID": st.column_config.Column("ID", width="small"),
                           "Name": st.column_config.Column("Name", width="large"),
                         }
                )
            else:
                st.info("No students registered yet.")

if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Attendance Admin")
    admin_page()
