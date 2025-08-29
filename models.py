from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from sqlalchemy import create_engine


engine = create_engine("sqlite:///medi-records.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

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
    patient = relationship("Patient", back_populates="records")


Base.metadata.create_all(bind=engine)


class CreateUser(BaseModel):
    name: str
    role: Optional[str] = "doctor"


class SendUser(BaseModel):
    id: int
    name: str
    role: str


class CreatePatient(BaseModel):
    name: str
    age: int


class SendPatient(BaseModel):
    id: int
    name: str
    age: int


class CreateMedicalRecord(BaseModel):
    patient_id: int
    findings: str


class SendMedicalRecord(BaseModel):
    id: int
    patient_id: int
    findings: str
    date_created: datetime