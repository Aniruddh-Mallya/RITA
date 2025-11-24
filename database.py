from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 1. The Connection to Jobs DB---
DATABASE_URL = "sqlite:///./jobs.db"

# We create the "Engine" (The connection to the physical file)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False, "timeout": 15}
)

# We create the "Session" (How we talk to the engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We create the "Base" (The template for our tables)
Base = declarative_base()

# --- 2. The Shared Model (The "Laminated Form") ---
# This ensures api.py and worker.py ALWAYS agree on the table structure
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="QUEUED")
    total_reviews = Column(Integer, default=0)
    completed_reviews = Column(Integer, default=0)
    original_reviews_json = Column(Text, default="[]") 
    results_json = Column(Text, default="[]")
    requirement_type = Column(String, default="UNKNOWN")
    llm_choice = Column(String, default="UNKNOWN")
    prompt_strategy = Column(String, default="UNKNOWN")

# --- 3. Initialization ---
def init_db():
    Base.metadata.create_all(bind=engine)