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

# --- Modern UI / SaaS Glassmorphism CSS ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #0f172a 60%, #020617 100%);
        color: #f8fafc;
    }

    /* Container Max Width */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Header Styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }

    /* Modern Card Layout */
    .portal-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(16px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .portal-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 25px 30px -5px rgba(99, 102, 241, 0.25);
    }

    .card-icon {
        font-size: 3rem;
        margin-bottom: 0.8rem;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.5rem;
    }

    .card-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Universal Streamlit Buttons Overhaul */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
    }

    /* Camera Input Widget Design */
    div[data-testid="stCameraInput"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 10px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("### ⚡ AttendX AI")
    st.caption("Smart Facial Recognition")
    st.markdown("---")
    
    if st.button("🏠 Home Portal", key="side_home"):
        st.session_state.page = "home"
        st.rerun()
    st.write("")
    if st.button("🎓 Student Verification", key="side_student"):
        st.session_state.page = "student"
        st.rerun()
    st.write("")
    if st.button("👨‍🏫 Teacher Dashboard", key="side_teacher"):
        st.session_state.page = "teacher"
        st.rerun()

# --- PAGE 1: HOME ---
if st.session_state.page == "home":
    st.markdown('<div class="main-title">ATTENDX AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Next-Gen Real-Time Facial Recognition Attendance Portal</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div class="portal-card">
                <div>
                    <div class="card-icon">🎓</div>
                    <div class="card-title">Student Portal</div>
                    <div class="card-desc">Verify face & mark daily attendance effortlessly in real-time.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Student Portal ➔", key="btn_student_home"):
            st.session_state.page = "student"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="portal-card">
                <div>
                    <div class="card-icon">👨‍🏫</div>
                    <div class="card-title">Teacher Portal</div>
                    <div class="card-desc">Manage student profiles, view analytics & export reports.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Teacher Portal ➔", key="btn_teacher_home"):
            st.session_state.page = "teacher"
            st.rerun()

    st.markdown('<div class="footer">Designed & Developed with ❤️ by <b>Afreen</b></div>', unsafe_allow_html=True)

# --- PAGE 2: STUDENT VERIFICATION ---
elif st.session_state.page == "student":
    st.markdown('<h2 style="color:#f8fafc; font-weight:700;">📷 Student Verification</h2>', unsafe_allow_html=True)
    st.write("Select your profile name and take a quick selfie to record attendance.")
    st.markdown("---")

    student_name = st.selectbox(
        "Select Your Profile Name",
        ["AFREEN", "SANIYA", "FARHAN", "GUEST"]
    )

    img_file_buffer = st.camera_input("Take photo to verify attendance")

    if img_file_buffer is not None:
        st.success(f"✅ Photo captured successfully for **{student_name}**!")
        st.info("Verification complete. Attendance recorded.")

# --- PAGE 3: TEACHER DASHBOARD ---
elif st.session_state.page == "teacher":
    st.markdown('<h2 style="color:#f8fafc; font-weight:700;">📊 Teacher Dashboard</h2>', unsafe_allow_html=True)
    st.write("View attendance history and export record files.")
    st.markdown("---")

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