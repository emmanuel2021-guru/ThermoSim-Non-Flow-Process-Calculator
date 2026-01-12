from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- CHANGED TO SQLITE FOR PORTABILITY ---
# This creates a file named 'thermosim.db' in the same folder.
# No server installation required.
DATABASE_URL = "sqlite:///./thermosim.db"

# connect_args is needed only for SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Helper function to create tables automatically (Call this in main.py if needed)
def init_db():
    Base.metadata.create_all(bind=engine)