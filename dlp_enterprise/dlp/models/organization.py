# dlp_enterprise/dlp/models/organization.py
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Organization(Base):
    __tablename__ = 'organizations'
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    tenant_id = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    users = relationship(\"User\", back_populates=\"organization\")
    policies = relationship(\"Policy\", back_populates=\"organization\")
    incidents = relationship(\"Incident\", back_populates=\"organization\")
