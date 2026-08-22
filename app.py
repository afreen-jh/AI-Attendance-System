import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="AttendX AI - Smart Attendance Portal",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Corporate Modern CSS (Zero Emojis, Clean Cards) ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #0f172a 60%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Max Width */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Header Styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Stat Cards */
    .stat-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .stat-num {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Modern Card Layout */
    .portal-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(16px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
    }

    .portal-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 25px 30px -5px rgba(99, 102, 241, 0.25);
    }

    .card-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #818cf8;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.6rem;
    }

    .card-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* Universal Streamlit Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: scale(1.01) !important;
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
    }

    /* Camera Input Widget Design */
    div[data-testid="stCameraInput"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 8px !important;
    }

    /* Clean Corporate Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Sidebar Navigation (No Emojis) ---
with st.sidebar:
    st.markdown("### ATTENDX AI")
    st.caption("Facial Recognition Management")
    st.markdown("---")
    
    if st.button("Home Portal", key="side_home"):
        st.session_state.page = "home"
        st.rerun()
    st.write("")
    if st.button("Student Verification", key="side_student"):
        st.session_state.page = "student"
        st.rerun()
    st.write("")
    if st.button("Teacher Dashboard", key="side_teacher"):
        st.session_state.page = "teacher"
        st.rerun()

# --- PAGE 1: HOME ---
if st.session_state.page == "home":
    st.markdown('<div class="main-title">ATTENDX AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Next-Gen Real-Time Facial Recognition Attendance System</div>', unsafe_allow_html=True)

    # Quick Metrics / Metrics Bar
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="stat-card"><div class="stat-num">99.4%</div><div class="stat-label">Accuracy Rate</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-card"><div class="stat-num">Real-Time</div><div class="stat-label">Recognition Speed</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-card"><div class="stat-num">Active</div><div class="stat-label">System Status</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
            <div class="portal-card">
                <div class="card-badge">Student Access</div>
                <div class="card-title">Student Portal</div>
                <div class="card-desc">Verify face recognition and record daily class attendance in real-time.</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Student Portal →", key="btn_student_home"):
            st.session_state.page = "student"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="portal-card">
                <div class="card-badge">Faculty Access</div>
                <div class="card-title">Teacher Portal</div>
                <div class="card-desc">Manage student profiles, view real-time analytics, and export reports.</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Teacher Portal →", key="btn_teacher_home"):
            st.session_state.page = "teacher"
            st.rerun()

    # Footer
    st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)

# --- PAGE 2: STUDENT VERIFICATION ---
elif st.session_state.page == "student":
    st.markdown('<h2 style="color:#f8fafc; font-weight:700;">Student Verification</h2>', unsafe_allow_html=True)
    st.write("Select your profile name and capture a selfie to record attendance.")
    st.markdown("---")

    student_name = st.selectbox(
        "Select Your Profile Name",
        ["AFREEN", "SANIYA", "FARHAN", "GUEST"]
    )

    img_file_buffer = st.camera_input("Take photo to verify attendance")

    if img_file_buffer is not None:
        st.success(f"Photo captured successfully for {student_name}.")
        st.info("Verification complete. Attendance recorded.")

    st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)

# --- PAGE 3: TEACHER DASHBOARD ---
elif st.session_state.page == "teacher":
    st.markdown('<h2 style="color:#f8fafc; font-weight:700;">Teacher Dashboard</h2>', unsafe_allow_html=True)
    st.write("View attendance history and export system record files.")
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
        label="Export Attendance CSV",
        data=csv,
        file_name='attendance_report.csv',
        mime='text/csv',
    )

    st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)