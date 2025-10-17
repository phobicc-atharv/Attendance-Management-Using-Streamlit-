# 📚 Streamlit Attendance Manager Pro

A modern, easy-to-use **Student Attendance Management System** built with **Streamlit** for the frontend and **Google Firebase Firestore** as a scalable, real-time backend. This application offers a secure, two-mode interface for both students and administrators to manage check-in and check-out records seamlessly.

---

## ✨ Features

### 1. Student Access (Check-In/Check-Out)
* **Simple Interface:** Students enter their **Student ID** for identification.
* **One-Click Attendance:** Dedicated **CHECK IN** and **CHECK OUT** buttons instantly record timestamped logs.
* **Recent Activity:** Displays a student's last 10 records for quick verification.

### 2. Admin Access (Dashboard & Management)
* **Secure Login:** Access is protected by a configurable Admin PIN.
* **Key Metrics:** Overview of **Total Students**, **Total Logs**, and **Unique Check-ins Today**.
* **Full Report:** View all attendance logs in a dynamic table and **download the complete CSV report**.
* **Student Management:**
    * **Registration:** Easily add new students (ID & Name).
    * **Deletion:** Securely remove existing student records with confirmation.
    * **Student List:** View all currently registered students.

---

## 🛠️ Setup and Installation

### 1. Prerequisites

* Python 3.8+
* Google Firebase Project

### 2. Get the Firebase Service Account Key

To connect to your Firestore database, you need a service account key:

1.  Go to your **Firebase Project Console**.
2.  Navigate to **Project settings** (gear icon) -> **Service accounts**.
3.  Click **Generate new private key** and save the downloaded JSON file.
4.  **Rename this file** to match the name used in `db_handler.py`:
    `attendance-management-98055-firebase-adminsdk-fbsvc-23ecb43446.json`
5.  Place this JSON file in the **root directory** of the project.

### 3. Install Dependencies

Clone this repository and install the required Python packages:

```bash
git clone <your-repo-link>
cd <your-repo-name>
pip install -r requirements.txt
# (Note: You may need to create a requirements.txt file with: streamlit, firebase-admin, pandas)
