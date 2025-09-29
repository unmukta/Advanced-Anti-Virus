from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
import psutil

# Import the audit logger
from audit_logger import audit_logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Basic routes



# Enhanced network scan with detailed logging

import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan")
async def network_scan(target: str = "192.168.1.0/24", scan_type: str = "quick", ports: str = "1-1000"):
    """Enhanced network scan with detailed logging"""
    import json
    import time
    from datetime import datetime
    
    scan_id = f"scan_{int(time.time())}"
    log_data = {
        "scan_id": scan_id,
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "start_time": datetime.now().isoformat(),
        "results": [],
        "status": "in_progress"
    }
    
    # Log the scan start
    log_network_scan(f"Scan {scan_id} started: Target={target}, Type={scan_type}, Ports={ports}")
    
    # Enhanced results with more details (simulated)
    results = [
        {
            "host": "192.168.1.1",
            "status": "up",
            "hostname": "router.local",
            "open_ports": [80, 443, 22, 53],
            "filtered_ports": [21, 25, 110],
            "closed_ports": [23, 69, 135],
            "services": {
                "80": "HTTP",
                "443": "HTTPS",
                "22": "SSH",
                "53": "DNS"
            },
            "os_guess": "Linux 3.x-4.x",
            "latency": "0.23ms",
            "mac_address": "00:1A:2B:3C:4D:5E",
            "vendor": "Cisco Systems",
            "uptime": "15 days, 3:45:22"
        },
        {
            "host": "192.168.1.2",
            "status": "up",
            "hostname": "pc-01.local",
            "open_ports": [135, 139, 445, 3389, 5357],
            "filtered_ports": [137, 138, 1900],
            "closed_ports": [21, 23, 25, 110],
            "services": {
                "135": "MSRPC",
                "139": "NetBIOS-SSN",
                "445": "Microsoft-DS",
                "3389": "ms-wbt-server",
                "5357": "WS-Discovery"
            },
            "os_guess": "Windows 10",
            "latency": "1.2ms",
            "mac_address": "00:50:56:C0:00:08",
            "vendor": "VMware",
            "uptime": "2 days, 12:30:15"
        },
        {
            "host": "192.168.1.3",
            "status": "down",
            "hostname": "N/A",
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "services": {},
            "os_guess": "N/A",
            "latency": "N/A",
            "mac_address": "N/A",
            "vendor": "N/A",
            "uptime": "N/A"
        }
    ]
    
    # Add results to log
    log_data["results"] = results
    log_data["end_time"] = datetime.now().isoformat()
    log_data["status"] = "completed"
    log_data["hosts_up"] = sum(1 for host in results if host["status"] == "up")
    log_data["hosts_down"] = sum(1 for host in results if host["status"] == "down")
    
    # Save detailed log
    save_detailed_scan_log(log_data)
    
    # Log the scan completion
    log_network_scan(f"Scan {scan_id} completed: {log_data['hosts_up']} hosts up, {log_data['hosts_down']} hosts down")
    
    return {
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "status": "completed",
        "scan_id": scan_id,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "hosts_up": log_data["hosts_up"],
            "hosts_down": log_data["hosts_down"],
            "total_hosts": len(results)
        }
    }

def log_network_scan(message):
    """Log network scan activity"""
    from datetime import datetime
    log_entry = f"[{datetime.now().isoformat()}] {message}\n"
    
    # Append to current log file
    with open("network_scan_logs.txt", "a") as log_file:
        log_file.write(log_entry)
    
    # Also add to in-memory log for API access
    if not hasattr(log_network_scan, 'log_entries'):
        log_network_scan.log_entries = []
    log_network_scan.log_entries.append(log_entry)
    
    # Keep only last 1000 entries in memory
    if len(log_network_scan.log_entries) > 1000:
        log_network_scan.log_entries = log_network_scan.log_entries[-1000:]

def save_detailed_scan_log(scan_data):
    """Save detailed scan log to JSON file"""
    import json
    from datetime import datetime
    
    # Create scans directory if it doesn't exist
    import os
    if not os.path.exists("scan_logs"):
        os.makedirs("scan_logs")
    
    # Save with timestamp in filename
    filename = f"scan_logs/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{scan_data['scan_id']}.json"
    with open(filename, "w") as f:
        json.dump(scan_data, f, indent=2)


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan/logs")
async def get_network_scan_logs(limit: int = 100):
    """Get recent network scan logs"""
    if not hasattr(log_network_scan, 'log_entries'):
        return {"logs": []}
    
    logs = log_network_scan.log_entries[-limit:] if limit > 0 else log_network_scan.log_entries
    return {"logs": logs}

@app.get("/api/network/scan/export")
async def export_network_scan_logs():
    """Export network scan logs to a file"""
    from datetime import datetime
    import os
    
    # Create exports directory if it doesn't exist
    if not os.path.exists("scan_exports"):
        os.makedirs("scan_exports")
    
    # Generate filename with timestamp
    filename = f"scan_exports/network_scan_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Write all logs to file
    if hasattr(log_network_scan, 'log_entries'):
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
    
    return {"status": "exported", "filename": filename, "export_time": datetime.now().isoformat()}


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/")
async def root():
    return {"message": "DLP Enterprise System"}

@app.get("/overview")
async def overview(request: Request):
    return templates.TemplateResponse("overview.html", {"request": request})

@app.get("/audit")
async def audit(request: Request):
    return templates.TemplateResponse("audit.html", {"request": request})

@app.get("/network")
async def network_page(request: Request):
    return templates.TemplateResponse("network.html", {"request": request})

# System metrics endpoint
@app.get("/api/system/metrics")
async def get_system_metrics():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_traffic": 0,
        "timestamp": datetime.now().isoformat()
    }

# Network stats endpoint
@app.get("/api/network/stats")
async def get_network_stats():
    try:
        import time
        
        # Initialize function attributes if they don't exist
        if not hasattr(get_network_stats, 'prev_time'):
            get_network_stats.prev_time = time.time()
            get_network_stats.prev_bytes_sent = psutil.net_io_counters().bytes_sent
            get_network_stats.prev_bytes_recv = psutil.net_io_counters().bytes_recv
            return {
                "bytes_sent": 0,
                "bytes_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
                "upload_speed": 0,
                "download_speed": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get current stats
        current_time = time.time()
        net_io = psutil.net_io_counters()
        
        # Calculate time difference
        time_diff = current_time - get_network_stats.prev_time
        
        # Calculate speeds in Mbps (not MB/s)
        upload_speed_bps = (net_io.bytes_sent - get_network_stats.prev_bytes_sent) * 8 / time_diff
        download_speed_bps = (net_io.bytes_recv - get_network_stats.prev_bytes_recv) * 8 / time_diff
        
        # Convert to Mbps
        upload_speed_mbps = upload_speed_bps / 1000000
        download_speed_mbps = download_speed_bps / 1000000
        
        # Update previous values
        get_network_stats.prev_time = current_time
        get_network_stats.prev_bytes_sent = net_io.bytes_sent
        get_network_stats.prev_bytes_recv = net_io.bytes_recv
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "upload_speed": round(upload_speed_mbps, 2),
            "download_speed": round(download_speed_mbps, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": "Failed to get network stats: " + str(e)}


# Enhanced network scan with detailed logging

import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan")
async def network_scan(target: str = "192.168.1.0/24", scan_type: str = "quick", ports: str = "1-1000"):
    """Enhanced network scan with detailed logging"""
    import json
    import time
    from datetime import datetime
    
    scan_id = f"scan_{int(time.time())}"
    log_data = {
        "scan_id": scan_id,
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "start_time": datetime.now().isoformat(),
        "results": [],
        "status": "in_progress"
    }
    
    # Log the scan start
    log_network_scan(f"Scan {scan_id} started: Target={target}, Type={scan_type}, Ports={ports}")
    
    # Enhanced results with more details (simulated)
    results = [
        {
            "host": "192.168.1.1",
            "status": "up",
            "hostname": "router.local",
            "open_ports": [80, 443, 22, 53],
            "filtered_ports": [21, 25, 110],
            "closed_ports": [23, 69, 135],
            "services": {
                "80": "HTTP",
                "443": "HTTPS",
                "22": "SSH",
                "53": "DNS"
            },
            "os_guess": "Linux 3.x-4.x",
            "latency": "0.23ms",
            "mac_address": "00:1A:2B:3C:4D:5E",
            "vendor": "Cisco Systems",
            "uptime": "15 days, 3:45:22"
        },
        {
            "host": "192.168.1.2",
            "status": "up",
            "hostname": "pc-01.local",
            "open_ports": [135, 139, 445, 3389, 5357],
            "filtered_ports": [137, 138, 1900],
            "closed_ports": [21, 23, 25, 110],
            "services": {
                "135": "MSRPC",
                "139": "NetBIOS-SSN",
                "445": "Microsoft-DS",
                "3389": "ms-wbt-server",
                "5357": "WS-Discovery"
            },
            "os_guess": "Windows 10",
            "latency": "1.2ms",
            "mac_address": "00:50:56:C0:00:08",
            "vendor": "VMware",
            "uptime": "2 days, 12:30:15"
        },
        {
            "host": "192.168.1.3",
            "status": "down",
            "hostname": "N/A",
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "services": {},
            "os_guess": "N/A",
            "latency": "N/A",
            "mac_address": "N/A",
            "vendor": "N/A",
            "uptime": "N/A"
        }
    ]
    
    # Add results to log
    log_data["results"] = results
    log_data["end_time"] = datetime.now().isoformat()
    log_data["status"] = "completed"
    log_data["hosts_up"] = sum(1 for host in results if host["status"] == "up")
    log_data["hosts_down"] = sum(1 for host in results if host["status"] == "down")
    
    # Save detailed log
    save_detailed_scan_log(log_data)
    
    # Log the scan completion
    log_network_scan(f"Scan {scan_id} completed: {log_data['hosts_up']} hosts up, {log_data['hosts_down']} hosts down")
    
    return {
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "status": "completed",
        "scan_id": scan_id,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "hosts_up": log_data["hosts_up"],
            "hosts_down": log_data["hosts_down"],
            "total_hosts": len(results)
        }
    }

def log_network_scan(message):
    """Log network scan activity"""
    from datetime import datetime
    log_entry = f"[{datetime.now().isoformat()}] {message}\n"
    
    # Append to current log file
    with open("network_scan_logs.txt", "a") as log_file:
        log_file.write(log_entry)
    
    # Also add to in-memory log for API access
    if not hasattr(log_network_scan, 'log_entries'):
        log_network_scan.log_entries = []
    log_network_scan.log_entries.append(log_entry)
    
    # Keep only last 1000 entries in memory
    if len(log_network_scan.log_entries) > 1000:
        log_network_scan.log_entries = log_network_scan.log_entries[-1000:]

def save_detailed_scan_log(scan_data):
    """Save detailed scan log to JSON file"""
    import json
    from datetime import datetime
    
    # Create scans directory if it doesn't exist
    import os
    if not os.path.exists("scan_logs"):
        os.makedirs("scan_logs")
    
    # Save with timestamp in filename
    filename = f"scan_logs/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{scan_data['scan_id']}.json"
    with open(filename, "w") as f:
        json.dump(scan_data, f, indent=2)


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan/logs")
async def get_network_scan_logs(limit: int = 100):
    """Get recent network scan logs"""
    if not hasattr(log_network_scan, 'log_entries'):
        return {"logs": []}
    
    logs = log_network_scan.log_entries[-limit:] if limit > 0 else log_network_scan.log_entries
    return {"logs": logs}

@app.get("/api/network/scan/export")
async def export_network_scan_logs():
    """Export network scan logs to a file"""
    from datetime import datetime
    import os
    
    # Create exports directory if it doesn't exist
    if not os.path.exists("scan_exports"):
        os.makedirs("scan_exports")
    
    # Generate filename with timestamp
    filename = f"scan_exports/network_scan_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Write all logs to file
    if hasattr(log_network_scan, 'log_entries'):
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
    
    return {"status": "exported", "filename": filename, "export_time": datetime.now().isoformat()}


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/audit/logs")
async def get_audit_logs():
    try:
        return {"logs": audit_logger.get_current_logs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get audit logs: {str(e)}")

@app.delete("/api/audit/logs")
async def clear_audit_logs():
    try:
        audit_logger.entries.clear()
        return {"message": "Audit logs cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear audit logs: {str(e)}")

@app.get("/api/audit/export")
async def export_audit_logs():
    try:
        # Simple export implementation
        export_file = "audit_export.txt"
        with open(export_file, 'w') as f:
            for entry in audit_logger.entries:
                f.write(f"{entry['timestamp']} - {entry['type']} - {entry['message']}\n")
        
        return FileResponse(export_file, filename="audit_logs_export.txt")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export audit logs: {str(e)}")

# Startup event
@app.on_event("startup")
async def startup_event():
    audit_logger.start_monitoring()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    audit_logger.stop_monitoring()


# Network stats endpoint with real-time speed calculation
@app.get("/api/network/stats")
async def get_network_stats():
    try:
        import time
        
        # Initialize function attributes if they don't exist
        if not hasattr(get_network_stats, 'prev_time'):
            get_network_stats.prev_time = time.time()
            get_network_stats.prev_bytes_sent = psutil.net_io_counters().bytes_sent
            get_network_stats.prev_bytes_recv = psutil.net_io_counters().bytes_recv
            return {
                "bytes_sent": 0,
                "bytes_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
                "upload_speed": 0,
                "download_speed": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get current stats
        current_time = time.time()
        net_io = psutil.net_io_counters()
        
        # Calculate time difference
        time_diff = current_time - get_network_stats.prev_time
        
        # Calculate speeds in Mbps (not MB/s)
        upload_speed_bps = (net_io.bytes_sent - get_network_stats.prev_bytes_sent) * 8 / time_diff
        download_speed_bps = (net_io.bytes_recv - get_network_stats.prev_bytes_recv) * 8 / time_diff
        
        # Convert to Mbps
        upload_speed_mbps = upload_speed_bps / 1000000
        download_speed_mbps = download_speed_bps / 1000000
        
        # Update previous values
        get_network_stats.prev_time = current_time
        get_network_stats.prev_bytes_sent = net_io.bytes_sent
        get_network_stats.prev_bytes_recv = net_io.bytes_recv
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "upload_speed": round(upload_speed_mbps, 2),
            "download_speed": round(download_speed_mbps, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": "Failed to get network stats: " + str(e)}


# Enhanced network scan with detailed logging

import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan")
async def network_scan(target: str = "192.168.1.0/24", scan_type: str = "quick", ports: str = "1-1000"):
    """Enhanced network scan with detailed logging"""
    import json
    import time
    from datetime import datetime
    
    scan_id = f"scan_{int(time.time())}"
    log_data = {
        "scan_id": scan_id,
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "start_time": datetime.now().isoformat(),
        "results": [],
        "status": "in_progress"
    }
    
    # Log the scan start
    log_network_scan(f"Scan {scan_id} started: Target={target}, Type={scan_type}, Ports={ports}")
    
    # Enhanced results with more details (simulated)
    results = [
        {
            "host": "192.168.1.1",
            "status": "up",
            "hostname": "router.local",
            "open_ports": [80, 443, 22, 53],
            "filtered_ports": [21, 25, 110],
            "closed_ports": [23, 69, 135],
            "services": {
                "80": "HTTP",
                "443": "HTTPS",
                "22": "SSH",
                "53": "DNS"
            },
            "os_guess": "Linux 3.x-4.x",
            "latency": "0.23ms",
            "mac_address": "00:1A:2B:3C:4D:5E",
            "vendor": "Cisco Systems",
            "uptime": "15 days, 3:45:22"
        },
        {
            "host": "192.168.1.2",
            "status": "up",
            "hostname": "pc-01.local",
            "open_ports": [135, 139, 445, 3389, 5357],
            "filtered_ports": [137, 138, 1900],
            "closed_ports": [21, 23, 25, 110],
            "services": {
                "135": "MSRPC",
                "139": "NetBIOS-SSN",
                "445": "Microsoft-DS",
                "3389": "ms-wbt-server",
                "5357": "WS-Discovery"
            },
            "os_guess": "Windows 10",
            "latency": "1.2ms",
            "mac_address": "00:50:56:C0:00:08",
            "vendor": "VMware",
            "uptime": "2 days, 12:30:15"
        },
        {
            "host": "192.168.1.3",
            "status": "down",
            "hostname": "N/A",
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "services": {},
            "os_guess": "N/A",
            "latency": "N/A",
            "mac_address": "N/A",
            "vendor": "N/A",
            "uptime": "N/A"
        }
    ]
    
    # Add results to log
    log_data["results"] = results
    log_data["end_time"] = datetime.now().isoformat()
    log_data["status"] = "completed"
    log_data["hosts_up"] = sum(1 for host in results if host["status"] == "up")
    log_data["hosts_down"] = sum(1 for host in results if host["status"] == "down")
    
    # Save detailed log
    save_detailed_scan_log(log_data)
    
    # Log the scan completion
    log_network_scan(f"Scan {scan_id} completed: {log_data['hosts_up']} hosts up, {log_data['hosts_down']} hosts down")
    
    return {
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "status": "completed",
        "scan_id": scan_id,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "hosts_up": log_data["hosts_up"],
            "hosts_down": log_data["hosts_down"],
            "total_hosts": len(results)
        }
    }

def log_network_scan(message):
    """Log network scan activity"""
    from datetime import datetime
    log_entry = f"[{datetime.now().isoformat()}] {message}\n"
    
    # Append to current log file
    with open("network_scan_logs.txt", "a") as log_file:
        log_file.write(log_entry)
    
    # Also add to in-memory log for API access
    if not hasattr(log_network_scan, 'log_entries'):
        log_network_scan.log_entries = []
    log_network_scan.log_entries.append(log_entry)
    
    # Keep only last 1000 entries in memory
    if len(log_network_scan.log_entries) > 1000:
        log_network_scan.log_entries = log_network_scan.log_entries[-1000:]

def save_detailed_scan_log(scan_data):
    """Save detailed scan log to JSON file"""
    import json
    from datetime import datetime
    
    # Create scans directory if it doesn't exist
    import os
    if not os.path.exists("scan_logs"):
        os.makedirs("scan_logs")
    
    # Save with timestamp in filename
    filename = f"scan_logs/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{scan_data['scan_id']}.json"
    with open(filename, "w") as f:
        json.dump(scan_data, f, indent=2)


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan/logs")
async def get_network_scan_logs(limit: int = 100):
    """Get recent network scan logs"""
    if not hasattr(log_network_scan, 'log_entries'):
        return {"logs": []}
    
    logs = log_network_scan.log_entries[-limit:] if limit > 0 else log_network_scan.log_entries
    return {"logs": logs}

@app.get("/api/network/scan/export")
async def export_network_scan_logs():
    """Export network scan logs to a file"""
    from datetime import datetime
    import os
    
    # Create exports directory if it doesn't exist
    if not os.path.exists("scan_exports"):
        os.makedirs("scan_exports")
    
    # Generate filename with timestamp
    filename = f"scan_exports/network_scan_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Write all logs to file
    if hasattr(log_network_scan, 'log_entries'):
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
    
    return {"status": "exported", "filename": filename, "export_time": datetime.now().isoformat()}


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/stats")
async def get_network_stats():
    try:
        import time
        
        # Initialize function attributes if they don't exist
        if not hasattr(get_network_stats, 'prev_time'):
            get_network_stats.prev_time = time.time()
            get_network_stats.prev_bytes_sent = psutil.net_io_counters().bytes_sent
            get_network_stats.prev_bytes_recv = psutil.net_io_counters().bytes_recv
            return {
                "bytes_sent": 0,
                "bytes_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
                "upload_speed": 0,
                "download_speed": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get current stats
        current_time = time.time()
        net_io = psutil.net_io_counters()
        
        # Calculate time difference
        time_diff = current_time - get_network_stats.prev_time
        
        # Calculate speeds in Mbps (not MB/s)
        upload_speed_bps = (net_io.bytes_sent - get_network_stats.prev_bytes_sent) * 8 / time_diff
        download_speed_bps = (net_io.bytes_recv - get_network_stats.prev_bytes_recv) * 8 / time_diff
        
        # Convert to Mbps
        upload_speed_mbps = upload_speed_bps / 1000000
        download_speed_mbps = download_speed_bps / 1000000
        
        # Update previous values
        get_network_stats.prev_time = current_time
        get_network_stats.prev_bytes_sent = net_io.bytes_sent
        get_network_stats.prev_bytes_recv = net_io.bytes_recv
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "upload_speed": round(upload_speed_mbps, 2),
            "download_speed": round(download_speed_mbps, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": "Failed to get network stats: " + str(e)}



# Enhanced network scan with detailed logging

import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan")
async def network_scan(target: str = "192.168.1.0/24", scan_type: str = "quick", ports: str = "1-1000"):
    """Enhanced network scan with detailed logging"""
    import json
    import time
    from datetime import datetime
    
    scan_id = f"scan_{int(time.time())}"
    log_data = {
        "scan_id": scan_id,
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "start_time": datetime.now().isoformat(),
        "results": [],
        "status": "in_progress"
    }
    
    # Log the scan start
    log_network_scan(f"Scan {scan_id} started: Target={target}, Type={scan_type}, Ports={ports}")
    
    # Enhanced results with more details (simulated)
    results = [
        {
            "host": "192.168.1.1",
            "status": "up",
            "hostname": "router.local",
            "open_ports": [80, 443, 22, 53],
            "filtered_ports": [21, 25, 110],
            "closed_ports": [23, 69, 135],
            "services": {
                "80": "HTTP",
                "443": "HTTPS",
                "22": "SSH",
                "53": "DNS"
            },
            "os_guess": "Linux 3.x-4.x",
            "latency": "0.23ms",
            "mac_address": "00:1A:2B:3C:4D:5E",
            "vendor": "Cisco Systems",
            "uptime": "15 days, 3:45:22"
        },
        {
            "host": "192.168.1.2",
            "status": "up",
            "hostname": "pc-01.local",
            "open_ports": [135, 139, 445, 3389, 5357],
            "filtered_ports": [137, 138, 1900],
            "closed_ports": [21, 23, 25, 110],
            "services": {
                "135": "MSRPC",
                "139": "NetBIOS-SSN",
                "445": "Microsoft-DS",
                "3389": "ms-wbt-server",
                "5357": "WS-Discovery"
            },
            "os_guess": "Windows 10",
            "latency": "1.2ms",
            "mac_address": "00:50:56:C0:00:08",
            "vendor": "VMware",
            "uptime": "2 days, 12:30:15"
        },
        {
            "host": "192.168.1.3",
            "status": "down",
            "hostname": "N/A",
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "services": {},
            "os_guess": "N/A",
            "latency": "N/A",
            "mac_address": "N/A",
            "vendor": "N/A",
            "uptime": "N/A"
        }
    ]
    
    # Add results to log
    log_data["results"] = results
    log_data["end_time"] = datetime.now().isoformat()
    log_data["status"] = "completed"
    log_data["hosts_up"] = sum(1 for host in results if host["status"] == "up")
    log_data["hosts_down"] = sum(1 for host in results if host["status"] == "down")
    
    # Save detailed log
    save_detailed_scan_log(log_data)
    
    # Log the scan completion
    log_network_scan(f"Scan {scan_id} completed: {log_data['hosts_up']} hosts up, {log_data['hosts_down']} hosts down")
    
    return {
        "target": target,
        "scan_type": scan_type,
        "ports": ports,
        "status": "completed",
        "scan_id": scan_id,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "hosts_up": log_data["hosts_up"],
            "hosts_down": log_data["hosts_down"],
            "total_hosts": len(results)
        }
    }

def log_network_scan(message):
    """Log network scan activity"""
    from datetime import datetime
    log_entry = f"[{datetime.now().isoformat()}] {message}\n"
    
    # Append to current log file
    with open("network_scan_logs.txt", "a") as log_file:
        log_file.write(log_entry)
    
    # Also add to in-memory log for API access
    if not hasattr(log_network_scan, 'log_entries'):
        log_network_scan.log_entries = []
    log_network_scan.log_entries.append(log_entry)
    
    # Keep only last 1000 entries in memory
    if len(log_network_scan.log_entries) > 1000:
        log_network_scan.log_entries = log_network_scan.log_entries[-1000:]

def save_detailed_scan_log(scan_data):
    """Save detailed scan log to JSON file"""
    import json
    from datetime import datetime
    
    # Create scans directory if it doesn't exist
    import os
    if not os.path.exists("scan_logs"):
        os.makedirs("scan_logs")
    
    # Save with timestamp in filename
    filename = f"scan_logs/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{scan_data['scan_id']}.json"
    with open(filename, "w") as f:
        json.dump(scan_data, f, indent=2)


import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/api/network/scan/logs")
async def get_network_scan_logs(limit: int = 100):
    """Get recent network scan logs"""
    if not hasattr(log_network_scan, 'log_entries'):
        return {"logs": []}
    
    logs = log_network_scan.log_entries[-limit:] if limit > 0 else log_network_scan.log_entries
    return {"logs": logs}

@app.get("/api/network/scan/export")
async def export_network_scan_logs():
    """Export network scan logs to a file"""
    from datetime import datetime
    import os
    
    # Create exports directory if it doesn't exist
    if not os.path.exists("scan_exports"):
        os.makedirs("scan_exports")
    
    # Generate filename with timestamp
    filename = f"scan_exports/network_scan_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Write all logs to file
    if hasattr(log_network_scan, 'log_entries'):
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
    
    return {"status": "exported", "filename": filename, "export_time": datetime.now().isoformat()}



import aioschedule as schedule
import asyncio


# Auto-export functionality
import asyncio
import aioschedule as schedule
from datetime import datetime
import os

async def auto_export_scan_logs():
    """Automatically export scan logs every hour"""
    if hasattr(log_network_scan, 'log_entries') and log_network_scan.log_entries:
        # Create exports directory if it doesn't exist
        if not os.path.exists("scan_exports"):
            os.makedirs("scan_exports")
        
        # Generate filename with timestamp
        filename = f"scan_exports/auto_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Write all logs to file
        with open(filename, "w") as f:
            f.writelines(log_network_scan.log_entries)
        
        print(f"Auto-export completed: {filename}")

# Schedule auto-export to run every hour
schedule.every().hour.do(lambda: asyncio.create_task(auto_export_scan_logs()))

# Background task to run the scheduler
async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Start the scheduler when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())



