# ⚡ AttendX AI - Smart Facial Recognition Attendance System

An intelligent, real-time facial recognition attendance management platform built using **Python**, **OpenCV**, and **Streamlit**. Designed to modernize traditional classroom attendance with role-based dual portals for students and educators.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
</p>

---

## 📌 Project Overview

Traditional attendance taking is time-consuming, prone to human error, and susceptible to proxy attendance. **AttendX AI** solves this by providing a unified, AI-driven platform where students can seamlessly verify their identity via live camera input, while teachers maintain complete oversight over student records and analytics.

### 🌟 Why AttendX AI?
- ⏱️ **Saves Classroom Time:** Eliminates manual roll calls entirely.
- 🎯 **Eliminates Proxy:** Real-time face detection ensures valid attendance logging.
- 🔐 **Dual Portal Access:** Distinct, dedicated interfaces for **Students** and **Teachers**.
- 📊 **Instant Export:** One-click download of attendance reports in CSV/Excel formats.

---

## ✨ Key Features

### 👨‍🎓 **Student Portal**
- **Live Facial Verification:** Capture instant webcam snapshots to mark attendance.
- **Visual Target Overlay:** Bounding boxes provide real-time face alignment feedback.
- **Automated Duplicate Prevention:** Smart checking prevents students from logging attendance twice in a single day.

### 👨‍🏫 **Teacher Portal & Management**
- **Student Enrollment:** Register new students on-the-fly with profile photo uploads.
- **Analytics Dashboard:** Real-time metrics showing total registered students, total logs, and system status.
- **Data Export & Control:** Filter, inspect, download attendance logs, or reset database records securely.

---

## 🔄 System Architecture & Workflow

```text
  [ Live Webcam / Image Upload ]
                │
                ▼
  [ OpenCV Preprocessing & Detection ]
                │
                ▼
  [ Known Faces Database Match ]
                │
       ┌────────┴────────┐
       ▼                 ▼
 [ Verified ]     [ Unrecognized ]
       │                 │
       ▼                 ▼
[ Log Attendance ] [ Prompt User ]
  (attendance.csv)
