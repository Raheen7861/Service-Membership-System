# Service Membership API (FastAPI + PostgreSQL)

Simple backend API for a service membership system (gym / coaching / salon style) built with:

- Python 3.9+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Real DB trigger to maintain `members.total_check_ins`

Project Setup

Clone & create virtualenv

bash
git clone <your-repo-url>.git
cd service-membership-api

python -m venv venv
venv\Scripts\activate     

Install dependencies
pip install -r requirements.txt

Database Configuration (PostgreSQL)
Create the database manually

Open SQL Shell (psql) and run:
CREATE DATABASE membership_db;

Add your DATABASE_URL in .env
Create a .env file in the project root:
DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost:5432/membership_db

Create Tables & Apply Trigger
Tables
Tables are created automatically at app startup (Base.metadata.create_all).
Just run the app once to generate:
members
plans
subscriptions
attendance

Apply the PostgreSQL trigger
After tables exist, run:
psql -d membership_db -f triggers.sql

Run the Application
Start FastAPI server:
uvicorn app.main:app --reload

API Documentation:
Swagger UI → http://localhost:8000/docs
ReDoc → http://localhost:8000/redoc
