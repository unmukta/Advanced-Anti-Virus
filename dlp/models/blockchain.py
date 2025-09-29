from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from .database import db

class BlockChainAudit(db.Model):
    __tablename__ = 'blockchain_audit'
    
    id = Column(Integer, primary_key=True)
    transaction_hash = Column(String(64), unique=True, nullable=False)
    data_hash = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    block_number = Column(Integer)
    previous_hash = Column(String(64))
    verified = Column(Boolean, default=False)
    
    def __repr__(self):
        return f'<BlockChainAudit {self.transaction_hash}>'
