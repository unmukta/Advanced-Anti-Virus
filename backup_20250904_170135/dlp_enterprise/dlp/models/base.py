# dlp_enterprise/dlp/models/base.py
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

class BaseModel:
    \"\"\"Base model with audit fields and soft delete\"\"\"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

Base = declarative_base(cls=BaseModel)
