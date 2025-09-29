import hashlib
import os
from datetime import datetime

class FileScanner:
    def __init__(self):
        self.scan_history = []

    def scan_file(self, filepath):
        """Scan a file for potential threats"""
        if not os.path.exists(filepath):
            return {"status": "error", "message": "File not found"}

        file_info = {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'size': os.path.getsize(filepath),
            'modified': datetime.fromtimestamp(os.path.getmtime(filepath)),
            'file_hash': self.calculate_hash(filepath)
        }
        
        # Basic threat detection logic
        threat_result = self.detect_threats(filepath)
        file_info.update(threat_result)
        
        self.scan_history.append(file_info)
        return file_info
    
    def calculate_hash(self, filepath, algorithm='sha256'):
        """Calculate file hash"""
        hash_func = getattr(hashlib, algorithm)()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def detect_threats(self, filepath):
        """Basic threat detection"""
        # This would be enhanced with actual DLP logic
        filename = os.path.basename(filepath).lower()
        
        # Simple pattern matching
        suspicious_patterns = ['.exe', '.dll', '.bat', '.cmd', '.ps1', '.vbs']
        for pattern in suspicious_patterns:
            if filename.endswith(pattern):
                return {
                    'scan_result': 'suspicious',
                    'threat_level': 'medium',
                    'details': f'Executable file type: {pattern}'
                }
        
        return {
            'scan_result': 'clean',
            'threat_level': 'low',
            'details': 'No obvious threats detected'
        }
    
    def get_scan_history(self):
        """Get scan history"""
        return self.scan_history
