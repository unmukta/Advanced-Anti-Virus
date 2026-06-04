import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import psutil
import time

class ComprehensiveLogger:
    def __init__(self):
        import os
        self.log_dir = Path(os.getenv("DLP_LOG_DIR", "./logs"))
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up comprehensive logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'dlp_system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DLPEnterprise')
        
        # Application tracking
        self.app_log = self.log_dir / 'applications.log'
        self.system_log = self.log_dir / 'system.log'
        self.network_log = self.log_dir / 'network.log'
        self.security_log = self.log_dir / 'security.log'
        self.audit_log = self.log_dir / 'audit.log'
        
        # Track running processes
        self.running_processes = {}
    
    def log_application(self, app_name: str, action: str, details: Dict[str, Any]):
        """Log application events"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'application',
            'application': app_name,
            'action': action,
            'details': details
        }
        self._write_log(self.app_log, entry)
        self.logger.info(f"Application {app_name} {action}: {json.dumps(details)}")
    
    def log_system(self, component: str, event_type: str, details: Dict[str, Any]):
        """Log system events"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'system',
            'component': component,
            'event_type': event_type,
            'details': details
        }
        self._write_log(self.system_log, entry)
        self.logger.info(f"System {component} {event_type}: {json.dumps(details)}")
    
    def log_network(self, event_type: str, source: str, destination: str, details: Dict[str, Any]):
        """Log network events"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'network',
            'event_type': event_type,
            'source': source,
            'destination': destination,
            'details': details
        }
        self._write_log(self.network_log, entry)
        self.logger.info(f"Network {event_type} from {source} to {destination}: {json.dumps(details)}")
    
    def log_security(self, threat_level: str, event_type: str, details: Dict[str, Any]):
        """Log security events"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'security',
            'threat_level': threat_level,
            'event_type': event_type,
            'details': details
        }
        self._write_log(self.security_log, entry)
        self.logger.info(f"Security {threat_level} {event_type}: {json.dumps(details)}")
    
    def log_audit(self, user: str, action: str, details: Dict[str, Any]):
        """Log audit events - everything gets logged here"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'audit',
            'user': user,
            'action': action,
            'details': details
        }
        self._write_log(self.audit_log, entry)
        self.logger.info(f"Audit {user} {action}: {json.dumps(details)}")
    
    def _write_log(self, log_file: Path, entry: Dict[str, Any]):
        """Write log entry to file"""
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write to log file {log_file}: {e}")
    
    def track_processes(self):
        """Track all running processes and log changes"""
        current_processes = {p.pid: p.name() for p in psutil.process_iter(['name'])}
        
        # Check for new processes
        for pid, name in current_processes.items():
            if pid not in self.running_processes:
                self.log_application(
                    name, 
                    'started', 
                    {'pid': pid, 'name': name, 'timestamp': datetime.now().isoformat()}
                )
                self.log_audit(
                    'system',
                    'process_started',
                    {'pid': pid, 'process_name': name}
                )
        
        # Check for stopped processes
        for pid, name in self.running_processes.items():
            if pid not in current_processes:
                self.log_application(
                    name,
                    'stopped',
                    {'pid': pid, 'name': name, 'timestamp': datetime.now().isoformat()}
                )
                self.log_audit(
                    'system',
                    'process_stopped',
                    {'pid': pid, 'process_name': name}
                )
        
        self.running_processes = current_processes
    
    def get_logs(self, log_type: str, limit: int = 1000):
        """Retrieve logs of a specific type"""
        log_file = self.log_dir / f'{log_type}.log'
        logs = []
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    logs.append(json.loads(line.strip()))
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
        except Exception as e:
            self.logger.error(f"Failed to read log file {log_file}: {e}")
        return logs

# Global logger instance
logger = ComprehensiveLogger()
