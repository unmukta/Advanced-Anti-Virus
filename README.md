# UbiquiShield 🛡️ (v0.7.0)

**UbiquiShield** is a premium, lightweight, real-time system monitoring and network analysis security suite for your PC. It provides glassmorphic visualizations of system metrics, active processes, and network events, alongside an AI-driven text filtering dashboard and comprehensive audit logger.

All monitoring data and scanning operations are run **strictly locally** on your machine to ensure complete privacy.

---

## ✨ Features

- **📊 Resource Utilization**: Real-time tracking of CPU, RAM, disk, and network speed metrics.
- **🖥️ Process Monitor**: Interactive process table showing active tasks, CPU percentages, and RAM consumption.
- **🌐 Network Shield**: Real-time network throughput chart and an integrated active network scanner (supporting Quick, Comprehensive, and Stealth scans).
- **🧠 AI Threat Filter**: Security playground showcasing AI policy scanning logic for potential threat signatures.
- **📋 Audit Console**: Local audit logging tracking process launches, terminations, network connections, and system starts.

---

## 📂 Project Structure

```text
├── backend/
│   ├── core/
│   │   ├── logger.py       # In-memory audit logging thread & log management
│   │   └── monitor.py      # Non-blocking resource metric tracker
│   ├── main.py             # FastAPI server & route handlers
│   └── run_server.py       # Server runner (uvicorn startup script)
├── frontend/
│   ├── static/
│   │   └── style.css       # Brave-style dark-mode matte style system
│   └── templates/
│       ├── audit.html      # Audit log console webpage
│       ├── network.html    # Network throughput & scanner page
│       ├── overview.html   # Main system overview dashboard
│       ├── system.html     # Performance metrics & process monitor
│       └── threats.html    # Threat center and AI playground
├── requirements.txt        # Minimum Python dependencies list
├── LICENSE                 # MIT License file
├── PRIVACY.md              # Offline local-only operations privacy policy
├── CHANGELOG.md            # Version and changes tracking file
└── README.md               # Project documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/unmukta/Advanced-Anti-Virus.git
   cd Advanced-Anti-Virus
   ```

2. **Initialize a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application**:
   ```bash
   python run_server.py
   ```

5. **Access the dashboard**:
   Open your web browser and navigate to [http://localhost:5050](http://localhost:5050).

---

## 📜 License

This project is open-source and released under the [MIT License](file:///d:/projects/Advanced-Anti-Virus/LICENSE).
