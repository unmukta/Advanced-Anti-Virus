# File: migrate_blockchain_data.py
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your models
sys.path.insert(0, 'C:\DLP-System\dlp_enterprise')
from dlp.models import BlockChainAudit
from dlp.models.database import SQLITE_DB_PATH, POSTGRES_DB_URI

# 1. Create sessions for both databases
# Source: SQLite (the original working database)
sqlite_engine = create_engine(f'sqlite:///{SQLITE_DB_PATH}')
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# Target: PostgreSQL (the new enterprise database)
postgres_engine = create_engine(POSTGRES_DB_URI)
PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# 2. Read all records from SQLite
print("Reading existing Blockchain Audit records from SQLite...")
all_audits = sqlite_session.query(BlockChainAudit).all()
print(f"Found {len(all_audits)} records to migrate.")

# 3. Write them to PostgreSQL, avoiding duplicates
records_migrated = 0
for old_audit in all_audits:
    # Check if this record already exists in PostgreSQL based on a unique field like transaction_hash
    exists = postgres_session.query(BlockChainAudit).filter_by(transaction_hash=old_audit.transaction_hash).first()
    if not exists:
        # Create a new object for PostgreSQL
        new_audit = BlockChainAudit(
            transaction_hash=old_audit.transaction_hash,
            data_hash=old_audit.data_hash,
            timestamp=old_audit.timestamp,
            block_number=old_audit.block_number,
            previous_hash=old_audit.previous_hash,
            verified=old_audit.verified
        )
        postgres_session.add(new_audit)
        records_migrated += 1

# 4. Commit the changes
postgres_session.commit()
print(f"Successfully migrated {records_migrated} new records to PostgreSQL.")

# 5. Verify the counts match (optional but recommended)
sqlite_count = sqlite_session.query(BlockChainAudit).count()
postgres_count = postgres_session.query(BlockChainAudit).count()
print(f"Verification: SQLite has {sqlite_count} records. PostgreSQL has {postgres_count} records.")

sqlite_session.close()
postgres_session.close()
