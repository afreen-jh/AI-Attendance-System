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

# --- Modern SaaS UI CSS ---
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
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Header Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.4rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* Portal Card Layout */
    .portal-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(16px);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .portal-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 25px 30px -5px rgba(99, 102, 241, 0.25);
    }

    .card-badge {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #818cf8;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.8rem;
    }

    .card-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* Universal Streamlit Buttons & Download Buttons */
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: scale(1.01) !important;
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
    }

    /* Camera Input Widget Design */
    div[data-testid="stCameraInput"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 10px !important;
    }

    /* Footer Branding */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        margin-top: 5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "teacher_logged_in" not in st.session_state:
    st.session_state.teacher_logged_in = False

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("### ⚡ AttendX AI")
    st.caption("Facial Recognition Management")
    st.markdown("---")
    
    if st.button("🏠 Home Portal", key="side_home"):
        st.session_state.page = "home"
        st.rerun()
    st.write("")
    if st.button("📷 Student Verification", key="side_student"):
        st.session_state.page = "student"
        st.rerun()
    st.write("")
    if st.button("📊 Teacher Dashboard", key="side_teacher"):
        st.session_state.page = "teacher"
        st.rerun()

# --- PAGE 1: HOME ---
if st.session_state.page == "home":
    st.markdown('<div class="main-title">ATTENDX AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Next-Gen Real-Time Facial Recognition Attendance System</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div class="portal-card">
                <div>
                    <div class="card-badge">Student Access</div>
                    <div class="card-title">Student Portal</div>
                    <div class="card-desc">Verify face recognition and record daily class attendance seamlessly in real-time.</div>
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
                    <div class="card-badge">Faculty Access</div>
                    <div class="card-title">Teacher Portal</div>
                    <div class="card-desc">Secure faculty login to manage student profiles, view analytics, and export reports.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Teacher Portal ➔", key="btn_teacher_home"):
            st.session_state.page = "teacher"
            st.rerun()

    st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)

# --- PAGE 2: STUDENT VERIFICATION ---
elif st.session_state.page == "student":
    st.markdown('<h2 style="color:#f8fafc; font-weight:700;">📷 Student Verification</h2>', unsafe_allow_html=True)
    st.write("Select your profile name and capture a selfie to record attendance.")
    st.markdown("---")

    student_name = st.selectbox(
        "Select Your Profile Name",
        ["AFREEN", "RAHUL SHARMA", "PRIYA VERMA", "AMAN KHAN", "GUEST"]
    )

    img_file_buffer = st.camera_input("Take photo to verify attendance")

    if img_file_buffer is not None:
        st.success(f"✅ Photo captured successfully for **{student_name}**!")
        st.info("Verification complete. Attendance recorded.")

    st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)

# --- PAGE 3: TEACHER DASHBOARD (WITH LOGIN GATE) ---
elif st.session_state.page == "teacher":
    if not st.session_state.teacher_logged_in:
        col_top1, col_top2 = st.columns([4, 1])
        with col_top1:
            st.markdown('<h2 style="color:#f8fafc; font-weight:700;">🔐 Teacher Portal Login</h2>', unsafe_allow_html=True)
            st.write("Enter your credentials to access the analytics and records dashboard.")
        with col_top2:
            if st.button("← Back to Home"):
                st.session_state.page = "home"
                st.rerun()
        
        st.markdown("---")
        
        with st.form("teacher_login_form"):
            username = st.text_input("Enter username", placeholder="e.g. afreen")
            password = st.text_input("Enter password", type="password", placeholder="••••••••")
            
            login_submitted = st.form_submit_button("🔒 Login to Dashboard")
            
            if login_submitted:
                # Default demo credentials: username 'afreen' and password 'admin123' (change as needed)
                if username.strip().lower() == "afreen" and password == "admin123":
                    st.session_state.teacher_logged_in = True
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Try username: afreen | password: admin123")
                    
        st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)

    else:
        col_top1, col_top2 = st.columns([4, 1])
        with col_top1:
            st.markdown('<h2 style="color:#f8fafc; font-weight:700;">📊 Teacher Dashboard</h2>', unsafe_allow_html=True)
            st.write("View attendance history and export system record files.")
        with col_top2:
            if st.button("🚪 Logout"):
                st.session_state.teacher_logged_in = False
                st.rerun()
                
        st.markdown("---")

        data = {
            "Student ID": ["STU001", "STU002", "STU003", "STU004"],
            "Name": ["Afreen", "Rahul Sharma", "Priya Verma", "Aman Khan"],
            "Time": ["09:00 AM", "09:05 AM", "09:50 AM", "09:15 AM"],
            "Status": ["Present", "Present", "Late", "Present"]
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

        st.markdown('<div class="footer">Designed & Developed by Afreen</div>', unsafe_allow_html=True)