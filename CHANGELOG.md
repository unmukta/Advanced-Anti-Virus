# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-06-04

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
- Updated `get_metrics.ps1` script to use new `core.monitor` module path.
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

