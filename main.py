import uvicorn
from fastapi import FastAPI, Depends
from typing import List
from models import CreateUser, SendUser, CreatePatient, SendPatient, CreateMedicalRecord, SendMedicalRecord
from datetime import datetime
from models import SessionLocal, Base, User, Patient, MedicalRecord  # your models
from sqlalchemy.orm import Session

app = FastAPI(title="Simple Medical Records API")

@app.get('/', tags=["Get Methods"])
async def home():
  return "Medical Records API"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=SendUser, tags=["User"])
def create_user(user_in: CreateUser, db: Session = Depends(get_db)):
    user = User(name=user_in.name, role=user_in.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/users', response_model=List[SendUser], tags=["User"])
async def get_users(db: Session = Depends(get_db)):
   return db.query(User).all()

@app.post("/patients/", response_model=SendPatient, tags=["Patient"])
def create_patient(patient_in: CreatePatient, db: Session = Depends(get_db)):
    patient = Patient(name=patient_in.name, age=patient_in.age)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@app.get('/patients', response_model=List[SendPatient], tags=["Patient"])
async def get_patients(db: Session = Depends(get_db)):
   return db.query(Patient).all()


@app.post("/records", response_model=SendMedicalRecord, tags=["Medical Records"])
def create_record(record_in: CreateMedicalRecord, db: Session = Depends(get_db)):
    record = MedicalRecord(patient_id=record_in.patient_id, findings=record_in.findings)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get('/records', response_model=List[SendMedicalRecord], tags=["Medical Records"])
def get_medical_records(db: Session = Depends(get_db)):
    return db.query(MedicalRecord).all()

@app.get("/search/records/", response_model=List[SendMedicalRecord], tags=["Medical Records"])
def search_medical_records(query: str, db: Session = Depends(get_db)):
    records = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.findings.ilike(f"%{query}%"))
        .all()
    )
    return records


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)