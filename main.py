"""SecureVision eye-detection demo API.

This project detects faces/eyes in uploaded images. It is not a production-grade
biometric identity verification system.
"""
from __future__ import annotations

import os
from typing import Annotated

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eye_security.db")
engine_options = {"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    employee_id = Column(String(80), unique=True, index=True, nullable=False)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureVision Eye Scanner Demo", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


def analyze_image(image_bytes: bytes) -> dict:
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty")
    if len(image_bytes) > 8 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image must be 8 MB or smaller")

    encoded = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Upload a valid JPEG or PNG image")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    eye_count = 0
    for x, y, w, h in faces:
        face_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))
        eye_count += len(eyes)

    return {
        "faces_detected": int(len(faces)),
        "eyes_detected": int(eye_count),
        "image_width": int(frame.shape[1]),
        "image_height": int(frame.shape[0]),
        "note": "Detection demo only; this does not verify a person's identity or liveness.",
    }


@app.get("/")
def home():
    return {"message": "SecureVision Eye Scanner Demo API is running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register")
def register(
    name: Annotated[str, Form()],
    employee_id: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
):
    if not name.strip() or not employee_id.strip():
        raise HTTPException(status_code=422, detail="Name and employee ID are required")
    if file.content_type not in {"image/jpeg", "image/png", "image/jpg"}:
        raise HTTPException(status_code=415, detail="Upload a JPEG or PNG image")
    image_bytes = file.file.read(8 * 1024 * 1024 + 1)
    result = analyze_image(image_bytes)
    if result["faces_detected"] < 1:
        raise HTTPException(status_code=422, detail="No face detected. Try a clearer, well-lit image.")

    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id.strip()).first()
        if employee:
            employee.name = name.strip()
            message = "Employee record updated"
        else:
            db.add(Employee(name=name.strip(), employee_id=employee_id.strip()))
            message = "Employee record registered"
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Employee ID already exists")
    finally:
        db.close()

    return {"status": message, "employee_id": employee_id.strip(), **result}


@app.post("/scan")
def scan(file: Annotated[UploadFile, File()]):
    if file.content_type not in {"image/jpeg", "image/png", "image/jpg"}:
        raise HTTPException(status_code=415, detail="Upload a JPEG or PNG image")
    result = analyze_image(file.file.read(8 * 1024 * 1024 + 1))
    if result["faces_detected"] < 1:
        return {"status": "No face detected", **result}
    if result["eyes_detected"] < 1:
        return {"status": "Face detected, but no eyes were detected", **result}
    return {"status": "Face and eyes detected", **result}
