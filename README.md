# SecureVision — Eye Scanner Demo

A small FastAPI + OpenCV demo that detects faces and eyes in uploaded images. It includes a simple HTML camera interface and stores basic employee records in SQLite.

> **Important limitation:** this is an image-detection demo, not a production biometric authentication system. It does not identify a person, compare iris templates, or prove liveness. Do not use it to make access-control or security decisions.

## Requirements

- Python 3.10 or newer
- A webcam for the browser interface (optional when testing the API with an uploaded image)

## Run locally

From the repository root:

### Windows PowerShell

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload --port 8001
```

### macOS / Linux

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8001
```

Open `http://127.0.0.1:8001/` for the health message and `http://127.0.0.1:8001/docs` for interactive API testing.

## Frontend

Open `frontend/admin_dashboard.html` in a browser and allow camera access. The page sends captured images to the local API at `http://127.0.0.1:8001`. For hosting, update the API URL and configure HTTPS/CORS appropriately.

## API endpoints

- `GET /` — service information
- `GET /health` — health check
- `POST /register` — multipart form fields `name`, `employee_id`, and image field `file`
- `POST /scan` — image field `file`; returns face/eye detection results

## Privacy and security

- Do not upload real biometric images, database files, `.env` files, passwords, or credentials to a public repository.
- The local SQLite database is ignored by Git.
- Before any real deployment, add authentication, authorization, rate limiting, consent and retention controls, and a properly evaluated biometric verification system.
