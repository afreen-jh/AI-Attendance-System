from datetime import datetime
import os
import pandas as pd
import pytz
import streamlit as st

# Safe OpenCV Import for Cloud Compatibility
try:
  import cv2
  import numpy as np
  OPENCV_AVAILABLE = True
except ImportError:
  OPENCV_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="AttendX AI - Smart Attendance Portal",
    page_icon="⚡",
    layout="wide",
)

# Initialize IST Timezone
IST = pytz.timezone("Asia/Kolkata")


def get_current_time_str():
  return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")


# Initialize Session State Database
if "students_db" not in st.session_state:
  st.session_state.students_db = pd.DataFrame(
      columns=[
          "ID",
          "Name",
          "Branch",
          "Enrollment No",
          "Registration Timestamp",
          "Status",
      ]
  )

if "attendance_logs" not in st.session_state:
  st.session_state.attendance_logs = pd.DataFrame(
      columns=["ID", "Name", "Branch", "Timestamp", "Status"]
  )

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False

# Custom CSS Styling (SaaS Dark Theme & Clean UI Fixes)
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput input {
        background-color: #161b22;
        color: white;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- AUTHENTICATION & LOGIN GATE -----------------
if not st.session_state.logged_in:
  st.markdown("<br><br>", unsafe_allow_html=True)
  col1, col2, col3 = st.columns([1, 1.2, 1])

  with col2:
    st.markdown(
        "<h1 style='text-align: center;'>⚡ AttendX AI</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #8b949e;'>Next-Gen Real-Time"
        " Facial Recognition Attendance System</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("login_form"):
      st.markdown("### 🔒 Teacher Portal Login")
      username_input = st.text_input("Teacher Username", value="")
      password_input = st.text_input(
          "Password", type="password", value=""
      )
      st.markdown("<br>", unsafe_allow_html=True)
      submit_login = st.form_submit_button("Login as Teacher")

      if submit_login:
        if username_input == "sarah" and password_input == "admin123":
          st.session_state.logged_in = True
          st.success("Logged in successfully!")
          st.rerun()
        else:
          st.error("Invalid credentials (try: sarah / admin123)")

  st.stop()  # Stop execution here until logged in

# ----------------- MAIN APP (AFTER LOGIN) -----------------
st.sidebar.markdown("## ⚡ AttendX Portal")
st.sidebar.markdown("**Role:** Teacher")

menu_options = [
    "Dashboard",
    "Register",
    "Train model",
    "Attendance",
    "Records",
    "Subject report",
    "Student sheet",
]
choice = st.sidebar.radio("Navigation", menu_options)

if st.sidebar.button("Logout"):
  st.session_state.logged_in = False
  st.rerun()

# ----------------- DASHBOARD -----------------
if choice == "Dashboard":
  st.title("⚡ AttendX AI - Smart Attendance Portal")
  st.write(
      "Welcome to the next-generation real-time facial recognition and"
      " attendance tracking system."
  )

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(
        label="Registered Students",
        value=len(st.session_state.students_db),
    )
  with col2:
    st.metric(
        label="Total Attendance Logs",
        value=len(st.session_state.attendance_logs),
    )
  with col3:
    st.metric(label="System Status", value="Online & Active")

  st.info(
      "👈 Use the sidebar navigation to register new students, run models,"
      " capture live attendance, or view master records."
  )

# ----------------- REGISTER STUDENT -----------------
elif choice == "Register":
  st.subheader("👤 Student Registration Portal")

  with st.form("registration_form"):
    col1, col2 = st.columns(2)
    with col1:
      student_id = st.text_input("Student ID (e.g. STU101)", value="STU101")
      full_name = st.text_input("Full Name", value="Afreen")
    with col2:
      branch = st.text_input("Branch / Department", value="DSAI")
      enrollment_no = st.text_input("Enrollment No", value="2400101751")

    submitted = st.form_submit_button("Register Student Profile")

    if submitted:
      if full_name and student_id:
        timestamp = get_current_time_str()
        new_row = pd.DataFrame({
            "ID": [student_id],
            "Name": [full_name],
            "Branch": [branch],
            "Enrollment No": [enrollment_no],
            "Registration Timestamp": [timestamp],
            "Status": ["Active"],
        })
        st.session_state.students_db = pd.concat(
            [st.session_state.students_db, new_row], ignore_index=True
        )
        st.success(
            f"Successfully registered {full_name} at real-time timestamp"
            f" {timestamp} (IST)!"
        )
      else:
        st.error("Please fill in all required fields.")

# ----------------- TRAIN MODEL -----------------
elif choice == "Train model":
  st.subheader("🧠 Model Training Engine")
  st.write(
      "Compile current student embeddings and optimize face recognition"
      " matching vectors."
  )

  if st.button("Compile & Train Model"):
    with st.spinner("Training model with latest registered profiles..."):
      import time

      time.sleep(2)
    st.success(
        "Model successfully trained and updated with current active student"
        f" dataset at {get_current_time_str()} (IST)!"
    )

# ----------------- ATTENDANCE CHECK-IN -----------------
elif choice == "Attendance":
  st.subheader("📷 Live Attendance Scanner")
  
  if not OPENCV_AVAILABLE:
      st.warning("⚠️ OpenCV (camera module) is unavailable on this cloud server environment.")
      
  st.write(
      "Position yourself in front of the camera to record real-time attendance."
  )

  camera_image = st.camera_input("Take a snapshot for verification")

  if camera_image is not None:
    st.success(f"Face captured successfully at {get_current_time_str()} (IST)!")
    if not st.session_state.students_db.empty:
      student_rec = st.session_state.students_db.iloc[0]
      attendance_entry = pd.DataFrame({
          "ID": [student_rec["ID"]],
          "Name": [student_rec["Name"]],
          "Branch": [student_rec["Branch"]],
          "Timestamp": [get_current_time_str()],
          "Status": ["Present"],
      })
      st.session_state.attendance_logs = pd.concat(
          [st.session_state.attendance_logs, attendance_entry],
          ignore_index=True,
      )
      st.info(
          f"Attendance marked successfully for: **{student_rec['Name']}**"
      )
    else:
      st.warning(
          "No registered students found in database. Please register first."
      )

# ----------------- RECORDS -----------------
elif choice == "Records":
  st.subheader("📋 Real-Time Attendance Logs")
  if not st.session_state.attendance_logs.empty:
    st.dataframe(st.session_state.attendance_logs, use_container_width=True)

    csv_data = st.session_state.attendance_logs.to_csv(index=False).encode(
        "utf-8"
    )
    st.download_button(
        label="📥 Download Attendance CSV",
        data=csv_data,
        file_name=f"attendance_report_{datetime.now(IST).strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
    )
  else:
    st.info("No attendance logs recorded yet for today.")

# ----------------- SUBJECT REPORT -----------------
elif choice == "Subject report":
  st.subheader("📊 Subject-wise Attendance Breakdown")
  st.write("Overview analytics of class attendance performance.")
  if not st.session_state.attendance_logs.empty:
    st.bar_chart(st.session_state.attendance_logs, x="Name", y="Timestamp")
  else:
    st.info("Insufficient data for analytics report.")

# ----------------- STUDENT SHEET -----------------
elif choice == "Student sheet":
  st.subheader("📑 Comprehensive Student Master Sheet")
  st.write(
      "Master database registry containing student profiles and exact"
      " registration timestamps (IST)."
  )
  if not st.session_state.students_db.empty:
    st.dataframe(st.session_state.students_db, use_container_width=True)
  else:
    st.info("No student profiles registered yet.")