# File: create_blockchain_table.py
import sys
sys.path.insert(0, 'C:\DLP-System\dlp_enterprise')

from dlp.models.database import engine_postgres

# SQL to create blockchain_audit table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS blockchain_audit (
    id SERIAL PRIMARY KEY,
    transaction_hash VARCHAR(64) UNIQUE NOT NULL,
    data_hash VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    block_number INTEGER,
    previous_hash VARCHAR(64),
    verified BOOLEAN DEFAULT FALSE
);
'''

try:
    with engine_postgres.connect() as conn:
        conn.execute(create_table_sql)
        print('✓ blockchain_audit table created successfully in PostgreSQL')
        
        # Check if table exists
        result = conn.execute('''
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'blockchain_audit'
        ''').scalar()
        
        print(f'✓ Verification: blockchain_audit table exists ({result} instances)')
        
except Exception as e:
    print(f'✗ Error creating table: {e}')
    import traceback
    traceback.print_exc()
