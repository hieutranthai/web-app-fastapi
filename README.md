# web-app-fastapi
A Python web app using FastAPI with SQLAlchemy and PostGreSQL.

# Step by step setup
- Create a virtual environment using `virtualenv` module in python.
```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
.venv/bin/activate.bat

# Install depdendency packages
pip install -r requirements.txt
```
- Configure variables in `.env` file
- Create postgres docker container
```bash
docker compose -f docker-compose-postgres.yaml up
```
- At `app` directory, run `alembic` migration command
```bash
# Migrate to latest revison which has one admin account setup already
alembic upgrade head

```
- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)
```bash
uvicorn main:app --reload
```