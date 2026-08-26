import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/plant_classifier")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True)
    status = Column(String, default = "queued")
    result = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
    