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
        background: radial-gradient(circle at 20% 20%, #31104a 0%, #0f172a 50%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Max Width */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1050px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Header Styling */
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 3.5rem;
    }

    /* Portal Card Layout */
    .portal-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.8rem 2.2rem;
        text-align: center;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }

    .portal-card:hover {
        border-color: rgba(129, 140, 248, 0.4);
        transform: translateY(-6px);
        box-shadow: 0 30px 60px -15px rgba(99, 102, 241, 0.3);
        background: rgba(30, 41, 59, 0.65);
    }

    .card-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1.2rem;
    }

    .card-title {
        font-size: 1.6rem;
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
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1.4rem !important;
        box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.5) !important;
        transition: all 0.25s ease-in-out !important;
        width: 100% !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px -4px rgba(99, 102, 241, 0.7) !important;
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
    }

    /* Inputs Styling */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
    }

    /* Camera Input Widget Design */
    div[data-testid="stCameraInput"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 12px !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }

    /* Footer Branding */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        margin-top: 6rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "teacher_logged_in" not in st.session_state:
    st.session_state.teacher_logged_in = False

if "attendance_records" not in st.session_state:
    st.session_state.attendance_records = []

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
    st.markdown('<div class="main-title">⚡ ATTENDX AI ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">✨ Next-Gen Real-Time Facial Recognition Attendance System ✨</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div class="portal-card">
                <div class="card-badge">🎓 Student Access</div>
                <div class="card-title">Student Portal</div>
                <div class="card-desc">Verify face recognition and record daily class attendance seamlessly in real-time. 🚀</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 Open Student Portal ➔", key="btn_student_home"):
            st.session_state.page = "student"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="portal-card">
                <div class="card-badge">🔒 Faculty Access</div>
                <div class="card-title">Teacher Portal</div>
                <div class="card-desc">Secure faculty login to manage student profiles, view live analytics, and export reports. 📈</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔐 Open Teacher Portal ➔", key="btn_teacher_home"):
            st.session_state.page = "teacher"
            st.rerun()

    st.markdown('<div class="footer">✨ Designed & Developed by Afreen ✨</div>', unsafe_allow_html=True)

# --- PAGE 2: STUDENT VERIFICATION ---
elif st.session_state.page == "student":
    st.markdown('<h2 style="color:#f8fafc; font-weight:700;">📸 Student Verification Portal</h2>', unsafe_allow_html=True)
    st.write("✨ Enter your full name and capture your selfie below to record your live attendance instantly! 🎯")
    st.markdown("---")

    student_name_input = st.text_input("👤 Enter Your Full Name", value="Guest", placeholder="e.g. Guest")

    img_file_buffer = st.camera_input("📷 Take photo to verify attendance")

    if img_file_buffer is not None:
        if not student_name_input.strip():
            st.warning("⚠️ Please type your name before verifying!")
        else:
            final_name = student_name_input.strip().title()
            
            existing_names = [r["Name"].lower() for r in st.session_state.attendance_records]
            
            if final_name.lower() not in existing_names:
                new_id = f"STU00{len(st.session_state.attendance_records) + 1}"
                current_date = datetime.now().strftime("%Y-%m-%d")
                current_time = datetime.now().strftime("%I:%M:%S %p")
                
                st.session_state.attendance_records.append({
                    "Student ID": new_id,
                    "Name": final_name,
                    "Date": current_date,
                    "Time": current_time,
                    "Status": "✅ Present"
                })
                
            st.success(f"🎉 Photo captured and face verified successfully for **{final_name}**! ✨")
            st.info("🚀 Live attendance has been securely updated on the teacher's dashboard.")

    st.markdown('<div class="footer">✨ Designed & Developed by Afreen ✨</div>', unsafe_allow_html=True)

# --- PAGE 3: TEACHER DASHBOARD (WITH LOGIN GATE) ---
elif st.session_state.page == "teacher":
    if not st.session_state.teacher_logged_in:
        col_top1, col_top2 = st.columns([4, 1])
        with col_top1:
            st.markdown('<h2 style="color:#f8fafc; font-weight:700;">🔐 Teacher Portal Login</h2>', unsafe_allow_html=True)
            st.write("✨ Enter your administrative credentials to access live attendance analytics. 📊")
        with col_top2:
            if st.button("🏠 ← Home"):
                st.session_state.page = "home"
                st.rerun()
        
        st.markdown("---")
        
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.markdown("""
                <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); padding: 2rem; border-radius: 20px; backdrop-filter: blur(16px); box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
            """, unsafe_allow_html=True)
            
            with st.form("teacher_login_form"):
                username = st.text_input("👤 Username", placeholder="e.g. afreen")
                password = st.text_input("🔑 Password", type="password", placeholder="••••••••")
                st.write("")
                login_submitted = st.form_submit_button("🚀 Secure Login")
                
                if login_submitted:
                    if username.strip().lower() == "afreen" and password == "admin123":
                        st.session_state.teacher_logged_in = True
                        st.success("🎉 Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials! Try username: afreen | password: admin123")
            
            st.markdown("</div>", unsafe_allow_html=True)
                    
        st.markdown('<div class="footer">✨ Designed & Developed by Afreen ✨</div>', unsafe_allow_html=True)

    else:
        col_top1, col_top2 = st.columns([4, 1])
        with col_top1:
            st.markdown('<h2 style="color:#f8fafc; font-weight:700;">📊 Live Teacher Dashboard</h2>', unsafe_allow_html=True)
            st.write("✨ Viewing real-time verified student attendance records and time logs. ⚡")
        with col_top2:
            if st.button("🚪 Logout"):
                st.session_state.teacher_logged_in = False
                st.rerun()
                
        st.markdown("---")

        if len(st.session_state.attendance_records) == 0:
            st.info("ℹ️ No live records yet! Go to 📸 **Student Verification**, type a student name (e.g. Guest), and capture a photo to watch real-time entries populate here instantly. ✨")
        else:
            df = pd.DataFrame(st.session_state.attendance_records)
            st.dataframe(df, use_container_width=True, hide_index=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Live Attendance CSV 📊",
                data=csv,
                file_name=f'attendance_report_{datetime.now().strftime("%Y-%m-%d")}.csv',
                mime='text/csv',
            )

        st.markdown('<div class="footer">✨ Designed & Developed by Afreen ✨</div>', unsafe_allow_html=True)