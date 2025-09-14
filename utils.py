import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session
from models import SessionLocal, AuditLog, User
from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
log_action: Logs user actions for HIPAA-compliant auditing purposes.
"""
def log_action(
    db: Session, user_id: int, action: str, target_table: str, target_id: Optional[int]
):
    audit = AuditLog(
        user_id=user_id, action=action, target_table=target_table, target_id=target_id
    )
    db.add(audit)
    db.commit()


security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


"""
authenticate: Basic authentication dependency for FastAPI routes.
"""
def authenticate(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    logging.info("Authenticating user: %s", credentials.username)
    user = db.query(User).filter(User.name == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.id
