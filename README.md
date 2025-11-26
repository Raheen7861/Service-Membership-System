# Service Membership API (FastAPI + PostgreSQL)

Simple backend API for a service membership system (gym / coaching / salon style) built with:

- Python 3.9+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Real DB trigger to maintain `members.total_check_ins`

Project Setup

Clone & create virtualenv

```bash
git clone <your-repo-url>.git
cd service-membership-api

python -m venv venv
venv\Scripts\activate     
