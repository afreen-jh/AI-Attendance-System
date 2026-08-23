# ⚡ AttendX AI - Smart Attendance Portal

**AttendX AI** is a next-generation, real-time facial recognition and attendance management web application built using **Streamlit**, **OpenCV**, and **Python**. It features a modern SaaS-inspired UI complete with live time tracking, localized timestamps, secure faculty authentication, and instant CSV data exports.

---

## 🚀 Live Demo
Experience the application live on Streamlit Cloud:  
👉 **[View AttendX AI Live App](https://attendx-ai-system.streamlit.app)**

---

## ✨ Key Features

* **🏠 Interactive Home Portal:** Sleek dual-card navigation designed for both students and faculty members.
* **📸 Student Verification Portal:** 
  * Defaults to **Guest** with customizable full-name input fields.
  * Captures live selfies via device camera for face verification.
  * Automatically records real-time dates and localized timestamps to prevent time zone shifts.
* **🔒 Secure Teacher Dashboard:**
  * Password-protected administrative login gate (`username: afreen` | `password: admin123`).
  * Real-time table viewing of all verified student attendance logs.
  * Instant **CSV Export** functionality for daily attendance reporting.
* **⚡ Modern UI/UX:** Styled with custom CSS, dark-mode gradients, glassmorphism cards, and vibrant emojis.

---

## 🔄 How It Works

1. **Access Portal:** Users land on the main SaaS-styled home page and choose between the **Student** or **Teacher** portal.
2. **Student Check-In:** Students enter their name (defaulting to Guest), look into their camera, and click to verify their attendance via selfie capture.
3. **Faculty Monitoring:** Teachers log into the secure dashboard using admin credentials to view live attendance logs and download CSV reports.

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Python, Streamlit
* **Computer Vision:** OpenCV, NumPy
* **Data Processing:** Pandas
* **Deployment:** Streamlit Community Cloud

---

## 📦 Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/afreen-jh/AI-Attendance-System.git](https://github.com/afreen-jh/AI-Attendance-System.git)
   cd AI-Attendance-System
