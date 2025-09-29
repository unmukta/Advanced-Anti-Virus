from sqlalchemy import Column, Integer, String, Boolean
from .database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(255))
    
    def __repr__(self):
        return f'<Role {self.name}>'
