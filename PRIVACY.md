# Privacy Policy

**UbiquiShield** values your privacy. This policy explains how we handle system and network monitoring data.

---

## 🔒 Offline & Local Operation

UbiquiShield is designed to run **strictly locally** on your computer.

1. **No External Transmission**: 
   All data collected by the monitoring suite (such as running processes, CPU/RAM usage, open network ports, active connection sockets, and network events) is processed strictly in-memory or written to local log files on your hard drive. 
   **None of this information is transmitted over the internet or sent to external servers.**

2. **AI Playground Privacy**:
   The AI Content Scanner Playground analyses text input entirely on your local machine using standard regex pattern rules. No external APIs or web services are called to perform these analyses.

3. **Audit Log Storage**:
   Your audit reports are stored as simple text files in the `audit_logs_history/` directory in the root of the project. You have complete ownership and control over these files and can delete them at any time.

---

## 🛠️ Data Collected & Processed

To provide its monitoring features, UbiquiShield reads:
* **System Resource Metrics**: Total/available CPU, RAM, disk space, and network interface speeds via Python's `psutil` library.
* **Process Metadata**: Process IDs (PIDs), process names, owner usernames, and memory/CPU percentages.
* **Network Status**: Network interface IO counters and active TCP/UDP connection details (local and remote IP addresses, connection state, and associated PIDs).
* **Network Scanner Targets**: If you run a network scan, the scanner targets the IP range you specify (e.g., your local subnet) and probes common ports to display active hosts. This scan is run directly from your machine.

---

## 📜 MIT License Compliance

Since this project is open-source under the MIT license, you are free to audit the source code to verify our privacy architecture. No telemetry, tracking, or network callback code is present.
