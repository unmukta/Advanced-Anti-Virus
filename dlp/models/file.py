from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import db

class FileScanResult(db.Model):
    __tablename__ = 'file_scan_results'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(Text, nullable=False)
    file_hash = Column(String(64))
    scan_result = Column(String(50))
    threat_level = Column(String(20))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FileScanResult {self.filename}>'
