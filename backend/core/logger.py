# backend/core/logger.py
import psutil
import time
import json
from datetime import datetime
import threading
import socket
import platform

class AuditLogger:
    def __init__(self, max_entries=5000):
        self.logs = []
        self.max_entries = max_entries
        self.running = False
        self.monitor_thread = None
        
        # Track previous states for diff monitoring
        self.previous_processes = set(p.pid for p in psutil.process_iter())
        self.previous_connections = set()
        
        print("AuditLogger initialized in-memory")
    
    def log_event(self, event_type, event_data):
        """Log an event to the in-memory list"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {event_type.upper()}: {json.dumps(event_data)}\n"
            
            self.logs.append(log_entry)
            
            # Prevent memory leaks by capping the list size
            if len(self.logs) > self.max_entries:
                self.logs.pop(0)
                
            print(f"Logged event (in-memory): {event_type}")
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
        """Get logs from the in-memory array"""
        return self.logs[-limit:] if limit else list(self.logs)
    
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
        """Clear all entries in the in-memory logs"""
        try:
            self.logs.clear()
            self.log_event('system', {
                'event': 'audit_logs_cleared',
                'timestamp': datetime.now().isoformat()
            })
            return True
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False

# Create a global instance
audit_logger = AuditLogger()
