# Simple Medical Records API

This project is a basic medical records management system built with FastAPI and SQLAlchemy. It provides a simple API for managing users, patients, and their medical records using a SQLite database.

## Features

- FastAPI-based REST API
- SQLite database for storage
- SQLAlchemy ORM models for Users, Patients, and Medical Records

## Project Structure

- `main.py` - Main application file containing API endpoints and database models
- `medi-records.db` - SQLite database file (created automatically)

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd medical-records-system
   ```

2. Install the dependencies
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application
   ```sh
   python main.py
   ```

The API will be available at http://localhost:8000.

