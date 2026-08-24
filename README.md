# ⚡ AttendX AI - Smart Attendance Portal

**AttendX AI** is a next-generation, real-time facial recognition and attendance management web application built using **Streamlit**, **OpenCV**, and **Python**. It features a modern SaaS-inspired UI complete with live time tracking, dynamic session-state database storage, secure faculty authentication, and instant CSV data exports.

---

## 🚀 Live Demo

Experience the application live on Streamlit Cloud:
👉 [View AttendX AI Live App](https://ai-attendance-system-v2.streamlit.app) 


---   



## ✨ Key Features

* **🏠 Interactive Dual Portal:** Sleek session-state navigation designed for both student and teacher roles.
* **👤 Dynamic Student Registration & Verification:**
  * Register new student profiles with custom **Student ID**, **Enrollment No**, **Full Name**, and **Branch**.
  * Captures live selfies via device camera for face recognition matching.
  * Automatically records real-time dates and localized timestamps into memory.
* **🔒 Secure Teacher Dashboard:**
  * Password-protected administrative login gate (`username: sarah` | `password: admin123`).
  * Real-time table viewing of all dynamically registered students and verified attendance logs.
  * Instant **CSV Export** functionality for attendance reporting and master sheets.
* **⚡ Modern UI/UX:** Styled with custom CSS, dark-mode gradients, glassmorphism cards, and vibrant emojis.

---

## 🔄 How It Works

1. **Teacher Registration:** Faculty logs into the portal and navigates to the **Register** tab to add new students dynamically with their details and face capture.
2. **Model Training:** Teachers compile the updated dataset via the **Train model** section to update embedding matrices.
3. **Live Attendance Check-In:** Students or teachers use the **Attendance** camera view to scan faces, which instantly verifies and pushes real-time logs to the **Records** and **Student Master Sheet**.

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Python, Streamlit
* **Computer Vision:** OpenCV, NumPy
* **Data Processing:** Pandas (with Session State memory management)
* **Deployment:** Streamlit Community Cloud

---

## 📦 Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/afreen-jh/AI-Attendance-System.git](https://github.com/afreen-jh/AI-Attendance-System.git)
   cd AI-Attendance-System
