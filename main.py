import uvicorn
from rag import RAG
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from models import (
    CreateUser,
    SendUser,
    CreatePatient,
    SendPatient,
    CreateMedicalRecord,
    SendMedicalRecord,
)
from models import SessionLocal, Base, User, Patient, MedicalRecord


from utils import get_db, log_action, authenticate, pwd_context

app = FastAPI(title="Simple Medical Records API")

"""Basic home route."""


@app.get("/", tags=["Get Methods"])
async def home():
    return "Medical Records API"


"""User routes for creating users. Passwords are hashed for security."""


@app.post("/users/", response_model=SendUser, tags=["User"])
def create_user(user_in: CreateUser, db: Session = Depends(get_db)):
    hashed_pw = pwd_context.hash(user_in.password)
    user = User(name=user_in.name, role=user_in.role, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


"""List all the users."""


@app.get("/users", response_model=List[SendUser], tags=["User"])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


"""Patient routes for creating and listing patients. Restricted to authenticated users."""


@app.post("/patients/", response_model=SendPatient, tags=["Patient"])
def create_patient(
    patient_in: CreatePatient,
    user_id=Depends(authenticate),
    db: Session = Depends(get_db),
):
    if not user_id:
        return HTTPException(status_code=401, detail="Authentication required")
    patient = Patient(name=patient_in.name, age=patient_in.age, doctor_id=user_id)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


"""List all patients."""


@app.get("/patients", response_model=List[SendPatient], tags=["Patient"])
async def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()


"""
Medical Record routes for creating and listing records. 
Creating records is restricted to authenticated users.
"""


@app.post("/records", response_model=SendMedicalRecord, tags=["Medical Records"])
def create_record(
    record_in: CreateMedicalRecord,
    user_id=Depends(authenticate),
    db: Session = Depends(get_db),
):
    if not user_id:
        return HTTPException(status_code=401, detail="Authentication required")
    patient = db.query(Patient).filter(Patient.id == record_in.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=400, detail="Invalid patient_id: patient does not exist."
        )
    record = MedicalRecord(patient_id=record_in.patient_id, findings=record_in.findings)
    db.add(record)
    db.commit()
    db.refresh(record)
    log_action(
        db,
        user_id=1,
        action="CREATE MedicalRecord",
        target_table="medical_records",
        target_id=record.id,
    )
    return record


"""List all medical records. Lists only the record file names."""


@app.get("/records", response_model=List[SendMedicalRecord], tags=["Medical Records"])
def get_medical_records(db: Session = Depends(get_db)):
    return db.query(MedicalRecord).all()


"""Search medical records by query string in findings. Only shows the record file names."""


@app.get(
    "/search/records/", response_model=List[SendMedicalRecord], tags=["Medical Records"]
)
def search_medical_records(query: str, db: Session = Depends(get_db)):
    records = (
        db.query(MedicalRecord).filter(MedicalRecord.findings.ilike(f"%{query}%")).all()
    )
    return records


"""Get medical records for a specific patient. Restricted to the doctor who owns the patient."""


@app.get(
    "/records/patient/{patient_id}",
    response_model=List[SendMedicalRecord],
    tags=["Medical Records"],
)
def get_records_by_patient(
    patient_id, user_id=Depends(authenticate), db: Session = Depends(get_db)
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id, Patient.doctor_id == user_id)
        .first()
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access records for this patient. Login again with correct user.",
        )

    # Fetch and return medical records for the patient
    records = (
        db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()
    )
    return records


"""RAG route to ask questions about medical records. Requires authentication."""


@app.get("/ask_records", response_model=str, tags=["RAG"])
def ask_records(
    question: str, user_id=Depends(authenticate), db: Session = Depends(get_db)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    rag = RAG()
    rag.create_pinecone_embeddings()
    rag.create_qa_chain()
    response = rag.query(question)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
