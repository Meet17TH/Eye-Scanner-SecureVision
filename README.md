# SecureVision — Eye Scanner Demo

A computer vision project built with Python, FastAPI, OpenCV, and SQLite. It detects faces and eyes in uploaded images and includes a browser-based dashboard.

## Features

* Face and eye detection using OpenCV
* FastAPI backend and REST API
* Employee record registration
* SQLite database
* HTML dashboard with camera support
* Interactive API documentation

## Technologies Used

* Python
* FastAPI
* OpenCV
* NumPy
* SQLite
* HTML, CSS, JavaScript

## Installation

**1. Create a virtual environment**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**2. Install dependencies**

```powershell
pip install -r requirements.txt
```

**3. Start the backend**

```powershell
uvicorn main:app --reload --port 8001
```

**4. Open the API**

* API: http://127.0.0.1:8001/
* Swagger documentation: http://127.0.0.1:8001/docs
* Health check: http://127.0.0.1:8001/health

## Dashboard

Open `admin_dashboard.html` in your browser and allow camera access when prompted.

## API Endpoints

* `GET /` — API information
* `GET /health` — health check
* `POST /register` — register an employee record
* `POST /scan` — detect faces and eyes in an image

## Important Note

This is a computer vision demonstration, not a production biometric authentication system. It does not verify a person's identity or liveness. Do not use it for security or access-control decisions.

## Author

**Meet Prajapati**

GitHub: https://github.com/Meet17TH

LinkedIn: https://www.linkedin.com/in/meet-prajapati-cs2026
