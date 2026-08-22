import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="AttendX AI - Smart Attendance Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Global CSS (Fixes Mismatched Boxes & Colors) ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0B0F19;
        color: #F9FAFB;
    }
    
    /* Layout Max Width & Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
    }

    /* Primary Headers */
    h1, h2, h3 {
        color: #38BDF8 !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Cards & Containers */
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        border: 1px solid #1F2937 !important;
        background-color: #111827 !important;
        border-radius: 12px !important;
    }

    /* Camera Input and Select Boxes */
    div[data-testid="stCameraInput"] {
        border: 1px solid #1F2937 !important;
        border-radius: 12px !important;
        background-color: #111827 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("⚡ AttendX AI")
    st.caption("Facial Recognition Portal")
    st.markdown("---")
    
    if st.button("🏠 Home Portal", use_container_width=True):
        st.session_state.page = "home"
    if st.button("🎓 Student Verification", use_container_width=True):
        st.session_state.page = "student"
    if st.button("👨‍🏫 Teacher Dashboard", use_container_width=True):
        st.session_state.page = "teacher"

# --- PAGE 1: HOME ---
if st.session_state.page == "home":
    st.title("⚡ ATTENDX AI")
    st.write("Next-Gen Real-Time Facial Recognition Attendance System")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎓 Student Portal")
        st.write("Verify face & mark daily attendance in real-time.")
        if st.button("Open Student Portal ➔", key="btn_student"):
            st.session_state.page = "student"
            st.rerun()

    with col2:
        st.subheader("👨‍🏫 Teacher Portal")
        st.write("Manage student profiles, analytics & export reports.")
        if st.button("Open Teacher Portal ➔", key="btn_teacher"):
            st.session_state.page = "teacher"
            st.rerun()

    st.markdown("<br><br><center><small>✨ Designed & Developed by Afreen ✨</small></center>", unsafe_allow_html=True)

# --- PAGE 2: STUDENT VERIFICATION ---
elif st.session_state.page == "student":
    st.title("📷 Student Verification & Attendance")
    st.write("Select your profile name and take a quick selfie to record attendance.")

    student_name = st.selectbox(
        "Select Your Profile Name",
        ["AFREEN", "SANIYA", "FARHAN", "GUEST"]
    )

    img_file_buffer = st.camera_input("Take photo to verify attendance")

    if img_file_buffer is not None:
        st.success(f"✅ Photo captured successfully for {student_name}!")
        st.info("Verification complete. Attendance recorded.")

# --- PAGE 3: TEACHER DASHBOARD ---
elif st.session_state.page == "teacher":
    st.title("📊 Attendance Analytics & Dashboard")
    st.write("View attendance history and export record files.")

    # Sample Data Table
    data = {
        "Student ID": ["STU001", "STU002", "STU003"],
        "Name": ["Afreen", "Saniya", "Farhan"],
        "Time": ["09:00 AM", "09:05 AM", "09:12 AM"],
        "Status": ["Present", "Present", "Late"]
    }
    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Attendance CSV",
        data=csv,
        file_name='attendance_report.csv',
        mime='text/csv',
    )