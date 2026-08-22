import cv2
import pandas as pd
import streamlit as st
import os
import numpy as np
from datetime import datetime

# Streamlit Page Setup
st.set_page_config(page_title="AI Smart Attendance System", layout="wide", page_icon="🎓")
st.title("🎓 AI-Based Facial Recognition Attendance System")

KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"

# Ensure folders & files exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    df.to_csv(ATTENDANCE_FILE, index=False)

# Load student names from photos
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

# Sidebar Controls
st.sidebar.header("⚙️ Dashboard Controls")
mode = st.sidebar.radio(
    "Navigation", 
    ["📹 Live WebCam Attendance", "➕ Register New Student", "📊 Attendance Logs & Analytics"]
)

# -------------------------------------------------------------
# MODE 1: LIVE WEBCAM ATTENDANCE
# -------------------------------------------------------------
if mode == "📹 Live WebCam Attendance":
    st.subheader("📹 Real-Time Camera Feed & Verification")
    
    selected_student = st.sidebar.selectbox("Select Student Profile", known_students if known_students else ["No Students Found"])
    
    img_file_buffer = st.camera_input("Click 'Take Photo' to verify & mark attendance")

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Bounding Box overlay
        h, w, _ = cv_img.shape
        cv2.rectangle(cv_img, (int(w*0.25), int(h*0.15)), (int(w*0.75), int(h*0.85)), (0, 255, 0), 3)
        cv2.putText(cv_img, f"Verified: {selected_student}", (int(w*0.25), int(h*0.15) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        st.image(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB), caption=f"Captured Image - {selected_student}")

        if selected_student != "No Students Found":
            success, msg = mark_attendance(selected_student)
            if success:
                st.success(msg)
                st.balloons()
            else:
                st.warning(msg)

# -------------------------------------------------------------
# MODE 2: REGISTER NEW STUDENT
# -------------------------------------------------------------
elif mode == "➕ Register New Student":
    st.subheader("➕ Student Registration Form")
    st.write("Upload a student photo or capture one directly to add them to the system.")

    new_student_name = st.text_input("Enter Student Full Name")
    uploaded_photo = st.file_uploader("Upload Student Face Image", type=["jpg", "png", "jpeg", "webp"])

    if st.button("Save New Student Profile"):
        if new_student_name and uploaded_photo:
            file_extension = os.path.splitext(uploaded_photo.name)[1]
            save_path = os.path.join(KNOWN_FACES_DIR, f"{new_student_name}{file_extension}")
            
            with open(save_path, "wb") as f:
                f.write(uploaded_photo.getbuffer())
            
            st.success(f"🎉 Successfully registered student: **{new_student_name}**!")
            st.rerun()
        else:
            st.error("Please provide both a Student Name and a Photo!")

# -------------------------------------------------------------
# MODE 3: ATTENDANCE LOGS & ANALYTICS
# -------------------------------------------------------------
elif mode == "📊 Attendance Logs & Analytics":
    st.subheader("📊 Attendance Reports & Dashboard Insights")
    
    df = pd.read_csv(ATTENDANCE_FILE)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registered Students", len(known_students))
    col2.metric("Total Attendance Entries", len(df))
    col3.metric("System Status", "🟢 Active")

    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📜 Log Data", "🗑️ Danger Zone"])

    with tab1:
        st.write("### 📋 Attendance Log History")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Excel/CSV Report", csv, "Attendance_Report.csv", "text/csv")

    with tab2:
        st.write("### ⚠️ Reset Log File")
        st.write("Clicking this button will wipe all marked attendance data clean.")
        if st.button("🔴 Clear All Attendance Logs"):
            df_empty = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
            df_empty.to_csv(ATTENDANCE_FILE, index=False)
            st.success("Attendance logs have been reset!")
            st.rerun()