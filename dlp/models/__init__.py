# Import available models here for easy access
try:
    from .blockchain import BlockChainAudit
except ImportError:
    pass  # Module doesn't exist yet

try:
    from .file import FileScanResult
except ImportError:
    pass  # Module doesn't exist yet

try:
    from .user import User, Role
except ImportError:
    pass  # Module doesn't exist yet

# Import database instance
from .database import db, SQLALCHEMY_DATABASE_URI, engine_sqlite, engine_postgres

__all__ = [
    'db', 'SQLALCHEMY_DATABASE_URI', 'engine_sqlite', 'engine_postgres'
]

# Add available models to __all__
try:
    BlockChainAudit
    __all__.append('BlockChainAudit')
except NameError:
    pass

try:
    FileScanResult
    __all__.append('FileScanResult')
except NameError:
    pass

try:
    User
    __all__.append('User')
    __all__.append('Role')
except NameError:
    pass
