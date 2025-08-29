from fastapi import FastAPI

from datetime import datetime

app = FastAPI(title="Simple Medical Records API")

@app.get('/', tags=["Get Methods"])
async def home():
  return "Home"

@app.post('/users', tags=["User"])
async def create_user():
  return "Create User"

@app.get('/users', tags=["User"])
async def get_users():
  return "Get Users"

@app.post('/patients', tags=["Patient"])
async def create_patient():
  return "Create Patient"

@app.get('/patients', tags=["Patient"])
async def get_patients():
  return "Get Patients"

@app.post('/records', tags=["Medical Records"])
async def create_medical_record():
  return "Create Medical Record"

@app.get('/records', tags=["Medical Records"])
async def get_medical_records():
  return "Get Medical Records"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)