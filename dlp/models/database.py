from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

# Database configuration
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
SQLITE_DB_PATH = os.path.join(basedir, 'dlp_data.db')

# PostgreSQL configuration - using proper URL format
POSTGRES_DB_URI = 'postgresql://postgres:postgres@localhost:5432/dlp_enterprise'

# Use appropriate database URI
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or POSTGRES_DB_URI

# Create database engines with proper connection strings
# For SQLite, we need to use the proper format
engine_sqlite = create_engine(f'sqlite:///{SQLITE_DB_PATH}', connect_args={'check_same_thread': False})
engine_postgres = create_engine(POSTGRES_DB_URI)
