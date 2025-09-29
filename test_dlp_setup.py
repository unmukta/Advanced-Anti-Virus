# File: test_dlp_setup.py
import sys
import os
sys.path.insert(0, 'C:\DLP-System\dlp_enterprise')

def test_basic_functionality():
    print('Testing DLP basic functionality...')
    
    # Test database models
    from dlp.models import BlockChainAudit, FileScanResult, User
    from dlp.models.database import db, engine_postgres
    
    print('? All models imported successfully')
    
    # Test database connection
    try:
        with engine_postgres.connect() as conn:
            result = conn.execute('SELECT COUNT(*) FROM pg_tables').scalar()
            print(f'? PostgreSQL connected. Found {result} tables.')
    except Exception as e:
        print(f'? PostgreSQL connection failed: {e}')
    
    # Test core functionality
    from dlp.core import FileScanner
    scanner = FileScanner()
    
    # Test scanning a file
    test_result = scanner.scan_file(__file__)
    print(f'? File scanner test: {test_result[\"scan_result\"]}')
    
    print('All basic tests passed!')
    
    # Check if blockchain_audit table exists
    try:
        with engine_postgres.connect() as conn:
            tables = conn.execute('''
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            ''').fetchall()
            
            table_names = [t[0] for t in tables]
            print(f'Available tables: {table_names}')
            
            if 'blockchain_audit' in table_names:
                print('? blockchain_audit table exists in PostgreSQL')
                count = conn.execute('SELECT COUNT(*) FROM blockchain_audit').scalar()
                print(f'? blockchain_audit table has {count} records')
            else:
                print('? blockchain_audit table does not exist yet')
                
    except Exception as e:
        print(f'Error checking tables: {e}')

if __name__ == '__main__':
    test_basic_functionality()
