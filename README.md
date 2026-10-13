# Projects in Python 🐍

This repository contains a collection of Python-based projects created for learning, practice, and academic purposes.  
Each project focuses on solving real-world problems using core Python concepts and commonly used libraries.

---

## 🚀 Main Project

### Fees Department Management System

A **Python-based desktop application** designed to digitize and manage student fee records efficiently, replacing manual register-based systems.

#### 🔹 Problem Addressed
- Manual data entry in registers is time-consuming and error-prone  
- Searching individual records from physical registers is inefficient  
- Existing solutions often require professional-level training  

#### 🔹 Solution
The application provides an easy-to-use interface for:
- Entering student fee details  
- Fetching and viewing stored records  
- Managing data digitally using a database backend  

---

## 🛠️ Technologies Used
- **Python**
- **Tkinter** – GUI development
- **MySQL** – Database management
- **MySQL Connector**
- **PyInstaller** (used for packaging the application)
- **Flask + Jinja2** – Web portal and API
- **Flask-CORS** – API CORS support

---

## 💻 System Requirements

### Minimum
- Python 3.8+
- MySQL Server 5.7+
- RAM: 2 GB
- OS: Windows 7 (64-bit)
- Display Resolution: 1280×720

### Recommended
- Python 3.10+
- MySQL Server 8.0
- RAM: 4 GB or higher
- OS: Windows 10 (64-bit)

---

## 📷 Output
- Application outputs and execution results are provided as screenshots inside the project folder.

---

## 🌐 Web Portal (New)

The project now includes a web-ready implementation while keeping the original Tkinter desktop app intact.

### Architecture Split
- **UI Layer (Desktop):** `/home/runner/work/ProjectsInPython/ProjectsInPython/Main/Fee_Dep.py.py`
- **Database Access Layer:** `/home/runner/work/ProjectsInPython/ProjectsInPython/web_portal/repository.py`
- **Business Rules Layer:** `/home/runner/work/ProjectsInPython/ProjectsInPython/web_portal/services.py`
- **Web/API Layer:** `/home/runner/work/ProjectsInPython/ProjectsInPython/web_portal/app.py`

### Features Exposed on Web
- Login/Auth
- Add student
- Submit fee
- Get details
- Update student
- Delete student

### Online MySQL Support
Database credentials are now environment-driven (`.env.example`) for managed online MySQL providers.

### Local Run (Web)
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Copy environment file:
   - `cp .env.example .env`
3. Configure online/local MySQL values in `.env`
4. Initialize schema:
   - `python scripts/init_db.py`
5. Start web app:
   - `python wsgi.py`

### Deployment
- **Recommended:** Render / Railway (persistent Python service)
  - Render config included: `/home/runner/work/ProjectsInPython/ProjectsInPython/render.yaml`
- **Optional Vercel setup:** `/home/runner/work/ProjectsInPython/ProjectsInPython/vercel.json`
  - For production, prefer hosting API on Render/Railway and connect Vercel frontend to it.

---

## 📚 Learning Resources Used
- GeeksforGeeks
- Stack Overflow
- Python Official Documentation
- Google & YouTube tutorials

---

## 🎯 Purpose of This Repository
- Practice Python programming
- Build academic and resume-ready projects
- Improve understanding of GUI development and databases
- Maintain a structured project portfolio on GitHub

---

## 👤 Author
**Satyam Vats**

---

## 📌 Note
This repository is continuously updated as new projects and improvements are added.
