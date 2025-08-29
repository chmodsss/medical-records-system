from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Simple Medical Records API")

@app.get('/', tags=["Get Methods"])
async def home():
  return "Home"

Base = declarative_base()
engine = create_engine("sqlite:///medi-records.db", echo=True)

@app.route("/")
def read_root():
    return {"message": "Welcome to the Simple Medical Records API"}


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    records = relationship("MedicalRecord", back_populates="patient")

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id = Column(Integer, primary_key=True)
    findings = Column(Text)
    date_created = Column(DateTime, default=datetime.now)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    patient = relationship("Patient", back_populates="records")


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)