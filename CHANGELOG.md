# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.7.0] - 2026-06-04

### Added
- Implemented real-time activity updates on the Overview page by fetching actual system audit logs instead of simulated metrics messages.
- Implemented real-time network activity events feed on the Network page by dynamically filtering network audit log events.
- Added process filtering (search bar) and multi-column sorting (PID, Name, CPU, Memory) in the Active Processes table on the System page.

### Changed
- Optimised system metrics collector to use non-blocking CPU monitoring, removing blocking calls that stalled the main FastAPI server thread.
- Strengthened backend robustness by adding graceful fallback handling for `psutil.AccessDenied` errors during network socket tracking when not running as admin.
- Isolated background thread CPU monitoring using a small interval to ensure thread safety and baseline accuracy for the main thread.
- Updated project documentation (`README.md`, `CHANGELOG.md`, `PRIVACY.md`) and package version metadata to align with version `0.7.0` and the restructured directory tree.

---

## [0.6.0] - 2026-06-04

### Added
- Created `LICENSE` file containing the standard MIT License.
- Created `CHANGELOG.md` to track development changes.
- Created `PRIVACY.md` detailing strictly local, private data handling.
- Implemented **UbiquiShield** dark-mode glassmorphic theme system in `static/style.css` using HSL-tailored variables and smooth transitions.
- Restructured core modules: created `core/monitor.py` (system stats) and `core/logger.py` (audit logger).

### Changed
- Rebranded application from "DLP Enterprise 3.0" to **UbiquiShield**.
- Rewrote `.gitignore` and `requirements.txt` to streamline development and minimize dependencies.
- Refactored `main.py` to route to restructured core modules and cleaned metadata.
- Updated all webpage templates (`overview.html`, `network.html`, `system.html`, `threats.html`, `audit.html`) to link with the new stylesheet, use uniform nav-menus, and fix duplication bugs.

### Removed
- Removed obsolete `dlp/` directory and components (unused SQLAlchemy models, routers).
- Removed unused `dlp_enterprise/` directory and PostgreSQL database dependencies.
- Removed unused `alembic/` migration scripts and `alembic.ini` configuration.
- Removed redundant `enterprise_venv/` virtual environment.
- Deleted obsolete templates, scripts, and logs (`test_dlp_setup.py`, `create_blockchain_table.py`, `migrate_blockchain_data.py`, `network_pro.js`, etc.).

## v0.6.0 2025-09-30

## Highlights
- New **Beta version** with full monitoring suite.
- **Process Monitoring** – Track all running applications.
- **Network Traffic Analysis** – Inspect connections and open ports.
- **Audit Logs** – Record activities like delete, download, running apps, network events.
- Export **audit logs in .txt format** with timestamps.
-  **task manager + network monitor + logging system** combined  

