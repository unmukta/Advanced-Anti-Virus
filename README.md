# Advanced Anti-Virus 🛡️

**Advanced Anti-Virus** is a next-generation monitoring and protection system for your PC.  
It provides **real-time insights** into system usage, applications, and network activity, while also maintaining detailed audit logs for security and compliance.

---

## 🚀 Features
- **Process Monitoring**: View all running applications, similar to Task Manager.  
- **Network Traffic Analysis**: Monitor active connections and all open ports.  
- **Audit Logs**:  
  - Tracks system activities like file deletions, downloads, running apps, and network activity.  
  - Export audit logs to `.txt` with precise **timestamps**.  
- **User-Friendly Dashboard** for visibility and control.

---

## 📂 Project Structure
- `app.py` → Main application entry point  
- `templates/` → Web UI and dashboards  
- `audit_logs/` → Saved audit reports  
- `modules/` → Core monitoring modules (process, network, USB, firewall, etc.)

---

## 🛠️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/unmukta/Advanced-Anti-Virus.git
   cd Advanced-Anti-Virus
Create a Python virtual environment:

bash
Copy code
python -m venv venv
venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python app.py
📊 Usage
Access the dashboard in your browser at http://localhost:5000

Monitor system processes, network traffic, and audit logs in real time.

Export logs in .txt format for auditing or investigation.

🏷️ Versioning
Main (Enterprise) → Current active branch

Legacy 0.5.0 → Older stable branch

Legacy 0.1.0 → First prototype branch

## 📜 License

This project is **private property**.  

- ✅ You may **use** it for personal purposes, free of charge.  
- ❌ You may **not modify, redistribute, or sell** this software.  
- All rights are reserved by the project owner.
