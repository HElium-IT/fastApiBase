from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# The “pre ping” feature operates on a per-dialect basis either by invoking a 
# DBAPI-specific “ping” method, or if not available will emit SQL equivalent 
# to “SELECT 1”, catching any errors and detecting the error as a “disconnect” 
# situation. If the ping / error check determines that the connection is not usable,
#  the connection will be immediately recycled, and all other pooled connections older
#  than the current time are invalidated, so that the next time they are checked out,
#  they will also be recycled before use.

# If the database is still not available when “pre ping” runs, then the initial
#  connect will fail and the error for failure to connect will be propagated normally.
#  In the uncommon situation that the database is available for connections, but is
#  not able to respond to a “ping”, the “pre_ping” will try up to three times before
#  giving up, propagating the database error last received.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
