from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from sqlalchemy import create_engine


engine = create_engine("sqlite:///medi-records.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


"""SQLAlchemy models for the database tables."""


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    hashed_password = Column(String)

    patients = relationship("Patient", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)

    doctor_id = Column(Integer, ForeignKey("users.id"))
    doctor = relationship("User", back_populates="patients")
    records = relationship("MedicalRecord", back_populates="patient")


class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id = Column(Integer, primary_key=True)
    findings = Column(Text)
    date_created = Column(DateTime, default=datetime.now)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="records")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    action = Column(String)
    target_table = Column(String)
    target_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


"""Pydantic models for request and response validation."""


class CreateUser(BaseModel):
    name: str
    password: str
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
