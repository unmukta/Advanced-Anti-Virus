# core/logger.py
import psutil
import time
import json
from datetime import datetime
import threading
import socket
import platform
import os
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir="audit_logs_history"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.running = False
        self.monitor_thread = None
        self.current_log_file = None
        self._create_new_log_file()
        
        # Track previous states
        self.previous_processes = set(p.pid for p in psutil.process_iter())
        self.previous_connections = set()
        
        print("AuditLogger initialized")
    
    def _create_new_log_file(self):
        """Create a new log file with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = self.log_dir / f"audit_log_{timestamp}.txt"
        
        # Write header to the new log file
        with open(self.current_log_file, 'w') as f:
            f.write(f"UbiquiShield Audit Log - Started at {datetime.now().isoformat()}\n")
            f.write("=" * 80 + "\n\n")
        
        print(f"Created new log file: {self.current_log_file}")
    
    def log_event(self, event_type, event_data):
        """Log an event with timestamp and details"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {event_type.upper()}: {json.dumps(event_data)}\n"
            
            # Append to current log file
            with open(self.current_log_file, 'a') as f:
                f.write(log_entry)
            
            print(f"Logged event: {event_type}")
            return True
        except Exception as e:
            print(f"Error logging event: {e}")
            return False
    
    def monitor_system_activities(self):
        """Continuously monitor and log system activities"""
        print("System activity monitoring started")
        
        while self.running:
            try:
                # Monitor process activity
                current_processes = set()
                for proc in psutil.process_iter(['pid', 'name', 'username']):
                    try:
                        proc_info = proc.info
                        pid = proc_info['pid']
                        current_processes.add(pid)
                        
                        # Log new processes
                        if pid not in self.previous_processes:
                            self.log_event('process', {
                                'action': 'started',
                                'pid': pid,
                                'name': proc_info['name'],
                                'username': proc_info['username']
                            })
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                
                # Log terminated processes
                for pid in self.previous_processes - current_processes:
                    self.log_event('process', {
                        'action': 'terminated',
                        'pid': pid
                    })
                
                self.previous_processes = current_processes
                
                # Monitor network connections
                current_connections = set()
                for conn in psutil.net_connections(kind='inet'):
                    if conn.laddr:
                        conn_id = f"{conn.laddr.ip}:{conn.laddr.port}"
                        if conn.raddr:
                            conn_id += f"-{conn.raddr.ip}:{conn.raddr.port}"
                        current_connections.add(conn_id)
                        
                        # Log new connections
                        if conn_id not in self.previous_connections:
                            try:
                                process_name = psutil.Process(conn.pid).name() if conn.pid else 'N/A'
                                self.log_event('network', {
                                    'action': 'connection_established',
                                    'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                                    'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A',
                                    'status': conn.status,
                                    'pid': conn.pid,
                                    'process_name': process_name
                                })
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
                
                # Log closed connections
                for conn_id in self.previous_connections - current_connections:
                    self.log_event('network', {
                        'action': 'connection_closed',
                        'connection_id': conn_id
                    })
                
                self.previous_connections = current_connections
                
                # Log system metrics periodically
                self.log_event('system', {
                    'cpu_percent': psutil.cpu_percent(),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_percent': psutil.disk_usage('/').percent
                })
                
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def get_current_logs(self, limit=1000):
        """Get logs from the current log file"""
        try:
            with open(self.current_log_file, 'r') as f:
                logs = f.readlines()
            
            # Return the most recent logs, limited by the specified count
            return logs[-limit:] if limit else logs
        except Exception as e:
            print(f"Error reading logs: {e}")
            return []
    
    def start_monitoring(self):
        """Start all monitoring threads"""
        if self.running:
            print("Audit logger is already running")
            return
        
        self.running = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_system_activities)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        self.log_event('system', {
            'event': 'audit_logger_started',
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'timestamp': datetime.now().isoformat()
        })
        
        print("Audit logger monitoring started")
    
    def stop_monitoring(self):
        """Stop all monitoring threads"""
        self.running = False
        
        self.log_event('system', {
            'event': 'audit_logger_stopped',
            'timestamp': datetime.now().isoformat()
        })
        
        print("Audit logger monitoring stopped")

    def clear_current_logs(self):
        """Clear all entries in the current log file"""
        try:
            with open(self.current_log_file, 'w') as f:
                f.write(f"UbiquiShield Audit Log - Started at {datetime.now().isoformat()}\n")
                f.write("=" * 80 + "\n\n")
            return True
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False

# Create a global instance
audit_logger = AuditLogger()

if __name__ == "__main__":
    # Test the logger
    logger = AuditLogger()
    logger.start_monitoring()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.stop_monitoring()
