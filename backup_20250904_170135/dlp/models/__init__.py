# dlp/models/__init__.py
# Base model definitions for Enterprise DLP

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__ = ['Base']
