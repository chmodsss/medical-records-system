# Simple Medical Records API

This project is a basic medical records management system built with FastAPI and SQLAlchemy. It provides a simple API for managing users, patients, and their medical records using a SQLite database. It also supports retrieval-augmented generation (RAG) for querying patient records using LLMs and vector search (Pinecone/FAISS).

## Tech Stack

- **Backend Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** SQLite
- **Authentication:** HTTP Basic Auth
- **Vector Search:** Pinecone, FAISS
- **LLM Integration:** OpenAI (via LangChain)
- **PDF/Text Parsing:** pdfminer.six
- **Environment Management:** python-dotenv
- **Password Hashing:** passlib[bcrypt]
- **API Server:** Uvicorn

## Features

- FastAPI-based REST API
- SQLite database for storage
- SQLAlchemy ORM models for Users, Patients, and Medical Records
- User authentication with HTTP Basic Auth
- Audit logging of user actions
- RAG (Retrieval-Augmented Generation) endpoint for querying patient records using LLMs and vector search (Pinecone/FAISS)
- PDF and text document ingestion for vector search

## Project Structure

- [`main.py`](main.py) - Main application file containing API endpoints
- [`models.py`](models.py) - SQLAlchemy ORM models and Pydantic schemas
- [`utils.py`](utils.py) - Utility functions for authentication, logging, and DB session management
- [`rag.py`](rag.py) - RAG logic for document loading, embedding, and querying with Pinecone/FAISS
- [`medi-records.db`](medi-records.db) - SQLite database file (created automatically)
- [`patient_records/`](patient_records/) - Directory containing sample patient PDF files
- `.env` - Environment variables for API keys and config

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic
- pdfminer.six
- pinecone
- langchain-pinecone
- python-jose
- passlib[bcrypt]
- dotenv

See [`requirements.txt`](requirements.txt) for the full list.

## Installation

1. **Open the folder:**
   ```sh
   cd medical-records-system
   ```

2. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy or edit the `.env` file with your OpenAI and Pinecone API keys.

4. **Add patient records:**
   - Place PDF or text files in the `patient_records/` directory.

5. **Run the application:**
   ```sh
   python main.py
   ```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Endpoints

- `POST /users/` - Create a new user
- `GET /users` - List all users
- `POST /patients/` - Create a new patient (requires authentication)
- `GET /patients` - List all patients
- `POST /records` - Create a new medical record (requires authentication)
- `GET /records` - List all medical records
- `GET /records/patient/{patient_id}` - Get records for a specific patient (requires authentication)
- `GET /search/records/?query=...` - Search medical records by findings
- `GET /ask_records?question=...` - Query patient records using RAG (requires authentication)

## Notes

- Authentication is required for creating patients, records, and for RAG queries. Use HTTP Basic Auth.
- The RAG endpoint uses Pinecone for vector search and OpenAI for embeddings/LLM. Ensure your API keys are set in `.env`.
- The database and tables are created automatically on first run.

## Project Description & Explanation

This project implements a simple yet extensible medical records management API using FastAPI and SQLAlchemy. The API is designed to securely manage users, patients, and their associated medical records, with additional support for advanced querying using Retrieval-Augmented Generation (RAG) powered by LLMs and vector search.

### Key Concepts and Flow

- **User Management:**  
  Users can be created with hashed passwords for security. User roles can be specified, and all user-related actions are logged for auditing. Users can be `doctor`, `nurse` or `admin`.

- **Authentication:**  
  Most endpoints that modify or access sensitive data require HTTP Basic Authentication. Only authenticated users can create patients, add medical records, or use the RAG endpoint.

- **Patient Management:**  
  Authenticated users (doctors) can create and list patients. Each patient is associated with a doctor (user).

- **Medical Records:**  
  Authenticated users can create medical records for their patients. Each record is linked to a patient and contains findings or notes. Users can list all records, search records by findings, or retrieve records for a specific patient (restricted to the doctor who owns the patient). Each patient can have multiple records.

- **Audit Logging:**  
  Actions such as creating medical records are logged for traceability, including the user, action, and target record.

- **RAG (Retrieval-Augmented Generation):**  
  The `/ask_records` endpoint allows authenticated users to ask questions about patient records using LLMs and vector search (Pinecone/FAISS). This enables advanced, context-aware querying of unstructured medical data.

- **Search Functionality:**  
  Users can search medical records by keywords in the findings, making it easy to locate relevant records.

- **Security:**  
  Passwords are securely hashed, and access to sensitive endpoints is restricted to authenticated users. Authorization checks ensure that users can only access records for their own patients.

