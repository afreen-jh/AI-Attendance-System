# ⚡ AttendX AI - Smart Attendance Portal

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-attendance-system-v2.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AttendX AI** is a next-generation, real-time facial recognition and attendance management web application built using **Streamlit**, **OpenCV**, and **Python**. It features a modern SaaS-inspired UI complete with live time tracking, dynamic session-state database storage, secure faculty authentication, and instant CSV data exports.

</div>

---

## 🚀 Live Demo

Experience the application live on Streamlit Cloud:
👉 [View AttendX AI Live App](https://ai-attendance-system-v2.streamlit.app)

---

## ✨ Key Features

* **🏠 Interactive Dual Portal:** Sleek session-state navigation designed seamlessly for both student and teacher roles.
* **👤 Dynamic Student Registration & Verification:**
  * Register new student profiles with custom **Student ID**, **Enrollment No**, **Full Name**, and **Branch**.
  * Captures live selfies via device camera for face recognition matching.
  * Automatically records real-time dates and localized timestamps into memory.
* **🔒 Secure Teacher Dashboard:**
  * Password-protected administrative login gate (`username: sarah` | `password: admin123`).
  * Real-time table viewing of all dynamically registered students and verified attendance logs.
  * Instant **CSV Export** functionality for attendance reporting and master sheets.
* **⚡ Modern UI/UX:** Styled with custom CSS, dark-mode gradients, glassmorphism cards, and vibrant responsive components.

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Python, Streamlit
* **Computer Vision & Math:** OpenCV, NumPy
* **Data Processing & State Management:** Pandas, Streamlit Session State
* **Deployment:** Streamlit Community Cloud

---

## 📁 Project Structure

```text
AI-Attendance-System/
│
├── .devcontainer/        # Development container configurations
├── .streamlit/           # Streamlit app configurations (theme/layout)
├── known_faces/          # Stored facial landmark assets and image samples
├── app.py                # Main Streamlit application and UI logic
├── requirements.txt      # Python dependencies list
├── packages.txt          # System-level dependencies (e.g., libgl1 for OpenCV)
├── README.md             # Project documentation
└── .gitignore            # Git exclusion rules
