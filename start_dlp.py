# File: start_dlp.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def check_dependencies():
    \"\"\"Check if all required dependencies are installed\"\"\"
    try:
        import flask
        import sqlalchemy
        import psycopg2
        import uvicorn
        import fastapi
        print('✓ All required dependencies are installed')
        return True
    except ImportError as e:
        print(f'✗ Missing dependency: {e}')
        return False

def check_databases():
    \"\"\"Check if databases are accessible\"\"\"
    try:
        from dlp.models.database import engine_sqlite, engine_postgres
        
        # Check SQLite
        with engine_sqlite.connect() as conn:
            tables = conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall()
            print(f'✓ SQLite connected. Found {len(tables)} tables.')
        
        # Check PostgreSQL
        with engine_postgres.connect() as conn:
            tables = conn.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\'').fetchall()
            print(f'✓ PostgreSQL connected. Found {len(tables)} tables.')
            
        return True
    except Exception as e:
        print(f'✗ Database error: {e}')
        return False

def main():
    \"\"\"Main function to start the DLP system\"\"\"
    print('Starting DLP Enterprise 3.0...')
    
    # Check dependencies
    if not check_dependencies():
        print('Please install missing dependencies and try again')
        return
    
    # Check databases
    if not check_databases():
        print('Please fix database issues and try again')
        return
    
    # Start the application
    try:
        from main import app
        import uvicorn
        
        print('✓ Starting DLP Enterprise server on http://localhost:5000')
        uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')
        
    except Exception as e:
        print(f'Error starting application: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
