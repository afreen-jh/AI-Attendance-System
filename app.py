import cv2
import pandas as pd
import streamlit as st
import os
import numpy as np
from datetime import datetime

# -------------------------------------------------------------
# PAGE CONFIG & CUSTOM CSS
# -------------------------------------------------------------
st.set_page_config(
    page_title="AttendX AI - Smart Attendance Portal", 
    layout="wide", 
    page_icon="⚡"
)

# Custom Styling for modern UI cards and theme
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #4f46e5 0%, #312e81 100%);
        color: #ffffff;
    }
    
    /* Header Branding */
    .app-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .app-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #c7d2fe;
        margin-bottom: 40px;
    }

    /* Portal Card Boxes */
    .portal-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        color: #1e293b;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
        margin: 10px;
        transition: transform 0.2s ease;
    }
    .portal-card:hover {
        transform: translateY(-5px);
    }
    
    .portal-icon {
        font-size: 4rem;
        margin-bottom: 15px;
    }
    
    .portal-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
    }
    
    .portal-desc {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 20px;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-top: 50px;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"

# Ensure necessary folders & files exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    df.to_csv(ATTENDANCE_FILE, index=False)

# Load student names
def load_known_students():
    names = []
    if os.path.exists(KNOWN_FACES_DIR):
        for file in os.listdir(KNOWN_FACES_DIR):
            if file.lower().endswith(('.jpg', '.png', '.jpeg', '.webp', '.avif')):
                clean_name = os.path.splitext(file)[0].replace(".jpg", "").replace("_", " ")
                names.append(clean_name)
    return names

known_students = load_known_students()

# Function to mark attendance
def mark_attendance(name):
    df = pd.read_csv(ATTENDANCE_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    already_marked = df[(df["Name"] == name) & (df["Date"] == today)]

    if already_marked.empty:
        new_entry = pd.DataFrame([{"Name": name, "Date": today, "Time": current_time, "Status": "Present"}])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(ATTENDANCE_FILE, index=False)
        return True, f"✅ Attendance Marked for {name}"
    else:
        return False, f"⚠️ {name} - Attendance already recorded today!"

# State navigation variable
if "portal" not in st.session_state:
    st.session_state.portal = "home"

# -------------------------------------------------------------
# LANDING PAGE / ROLE SELECTION
# -------------------------------------------------------------
st.markdown("<h1 class='app-title'>⚡ ATTENDX AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Next-Gen Real-Time Facial Recognition Attendance Portal</p>", unsafe_allow_html=True)

if st.session_state.portal == "home":
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        p_col1, p_col2 = st.columns(2)

        # STUDENT CARD
        with p_col1:
            st.markdown("""
            <div class='portal-card'>
                <div class='portal-icon'>👨‍🎓</div>
                <div class='portal-title'>Student Portal</div>
                <div class='portal-desc'>Verify face & mark daily attendance in real-time</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Enter Student Portal ↗️", key="btn_student", use_container_width=True):
                st.session_state.portal = "student"
                st.rerun()

        # TEACHER CARD
        with p_col2:
            st.markdown("""
            <div class='portal-card'>
                <div class='portal-icon'>👨‍🏫</div>
                <div class='portal-title'>Teacher Portal</div>
                <div class='portal-desc'>Manage student profiles, analytics & export reports</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Enter Teacher Portal ↗️", key="btn_teacher", use_container_width=True):
                st.session_state.portal = "teacher"
                st.rerun()

    st.markdown("<div class='footer'>✨ Designed & Developed by Afreen ✨</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# STUDENT PORTAL
# -------------------------------------------------------------
elif st.session_state.portal == "student":
    if st.sidebar.button("🏠 Back to Home"):
        st.session_state.portal = "home"
        st.rerun()

    st.subheader("📹 Student Verification & Attendance")
    st.write("Select your profile name and take a quick selfie to record attendance.")

    selected_student = st.selectbox("Select Your Profile Name", known_students if known_students else ["No Students Registered"])
    
    img_file_buffer = st.camera_input("Take photo to verify attendance")

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Draw target overlay box
        h, w, _ = cv_img.shape
        cv2.rectangle(cv_img, (int(w*0.25), int(h*0.15)), (int(w*0.75), int(h*0.85)), (0, 255, 0), 3)
        cv2.putText(cv_img, f"Verified: {selected_student}", (int(w*0.25), int(h*0.15) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        st.image(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB), caption=f"Captured Image - {selected_student}")

        if selected_student != "No Students Registered":
            success, msg = mark_attendance(selected_student)
            if success:
                st.success(msg)
                st.balloons()
            else:
                st.warning(msg)

# -------------------------------------------------------------
# TEACHER PORTAL
# -------------------------------------------------------------
elif st.session_state.portal == "teacher":
    if st.sidebar.button("🏠 Back to Home"):
        st.session_state.portal = "home"
        st.rerun()

    st.sidebar.header("⚙️ Teacher Controls")
    teacher_mode = st.sidebar.radio("Section", ["📊 Attendance Logs & Analytics", "➕ Register New Student"])

    if teacher_mode == "📊 Attendance Logs & Analytics":
        st.subheader("📊 Class Attendance Dashboard")
        
        df = pd.read_csv(ATTENDANCE_FILE)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Registered Students", len(known_students))
        col2.metric("Total Logs Recorded", len(df))
        col3.metric("System Status", "🟢 Active")

        st.markdown("---")
        
        tab1, tab2 = st.tabs(["📋 Detailed Logs", "⚙️ Danger Zone"])

        with tab1:
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Excel / CSV Log", csv, "AttendX_Attendance_Report.csv", "text/csv")

        with tab2:
            st.write("### ⚠️ Clear Attendance Database")
            if st.button("🔴 Reset Attendance Logs"):
                df_empty = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
                df_empty.to_csv(ATTENDANCE_FILE, index=False)
                st.success("Attendance database has been reset!")
                st.rerun()

    elif teacher_mode == "➕ Register New Student":
        st.subheader("➕ Add New Student to Database")
        
        new_student_name = st.text_input("Student Full Name")
        uploaded_photo = st.file_uploader("Upload Student Face Image", type=["jpg", "png", "jpeg", "webp"])

        if st.button("Register Student"):
            if new_student_name and uploaded_photo:
                file_extension = os.path.splitext(uploaded_photo.name)[1]
                save_path = os.path.join(KNOWN_FACES_DIR, f"{new_student_name}{file_extension}")
                
                with open(save_path, "wb") as f:
                    f.write(uploaded_photo.getbuffer())
                
                st.success(f"🎉 Registered student **{new_student_name}** successfully!")
                st.rerun()
            else:
                st.error("Please enter a name and upload an image!")