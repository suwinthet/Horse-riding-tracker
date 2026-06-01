from fastapi import FastAPI, Depends, HTTPException, status
import sqlite3
from typing import List
from database import get_db, init_db
import schemas
import auth
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Horse Training Planner API", lifespan=lifespan)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserRegister, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (name, surname, email, password_hash) VALUES (?, ?, ?, ?)",
            (user.name, user.surname, user.email, hashed_password)
        )
        db.commit()
        return {"detail": "User created"}
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=schemas.AuthResponse)
def login(user: schemas.UserLogin, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (user.email,))
    db_user = cursor.fetchone()
    
    if not db_user or not auth.verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    access_token = auth.create_access_token(
        data={"sub": str(db_user["id"])},
        expires_delta=auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"token": access_token}

@app.get("/api/horses", response_model=List[schemas.Horse])
def get_horses(db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM horses")
    return [dict(row) for row in cursor.fetchall()]

@app.get("/api/trainers", response_model=List[schemas.Trainer])
def get_trainers(db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trainers")
    return [dict(row) for row in cursor.fetchall()]

@app.get("/api/training-types", response_model=List[schemas.TrainingType])
def get_training_types(db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM training_types")
    return [dict(row) for row in cursor.fetchall()]

@app.get("/api/trainings", response_model=List[schemas.Training])
def get_trainings(db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trainings")
    return [dict(row) for row in cursor.fetchall()]

@app.post("/api/trainings", status_code=status.HTTP_201_CREATED)
def create_training(training: schemas.TrainingCreate, db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    try:
        # Check foreign keys
        cursor.execute("SELECT id FROM horses WHERE id = ?", (training.horse_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Horse not found")
        
        cursor.execute("SELECT id FROM trainers WHERE id = ?", (training.trainer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Trainer not found")
            
        cursor.execute("SELECT id FROM training_types WHERE id = ?", (training.training_type_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Training type not found")
            
        # Optional: check date format/value (Pydantic already validated it's a valid datetime string)
        
        cursor.execute(
            "INSERT INTO trainings (horse_id, trainer_id, training_type_id, date) VALUES (?, ?, ?, ?)",
            (training.horse_id, training.trainer_id, training.training_type_id, training.date.isoformat())
        )
        db.commit()
        return {"detail": "Training created"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Validation error")

@app.put("/api/trainings/{id}", response_model=schemas.Training)
def update_training(id: int, training: schemas.TrainingUpdate, db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trainings WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Training not found")
    
    update_data = training.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Invalid input")
        
    set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
    values = tuple(val.isoformat() if isinstance(val, datetime) else val for val in update_data.values()) + (id,)
    
    try:
        cursor.execute(f"UPDATE trainings SET {set_clause} WHERE id = ?", values)
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Validation error / Invalid input")
        
    cursor.execute("SELECT * FROM trainings WHERE id = ?", (id,))
    return dict(cursor.fetchone())

@app.delete("/api/trainings/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training(id: int, db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trainings WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Training not found")
        
    cursor.execute("DELETE FROM trainings WHERE id = ?", (id,))
    db.commit()

@app.post("/api/trainings/{id}/join", status_code=status.HTTP_201_CREATED)
def join_training(id: int, join_req: schemas.JoinTraining, db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trainings WHERE id = ?", (id,))
    training = cursor.fetchone()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
        
    if training["status"] != "open":
        raise HTTPException(status_code=400, detail="Training is full or invalid request")
        
    cursor.execute("SELECT COUNT(*) as count FROM training_participants WHERE training_id = ?", (id,))
    participants_count = cursor.fetchone()["count"]
    
    if participants_count >= training["capacity"]:
        # Update status to full
        cursor.execute("UPDATE trainings SET status = 'full' WHERE id = ?", (id,))
        db.commit()
        raise HTTPException(status_code=400, detail="Training is full")
        
    # Check if already joined
    cursor.execute("SELECT * FROM training_participants WHERE training_id = ? AND user_id = ?", (id, current_user))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Already joined")
        
    cursor.execute("INSERT INTO training_participants (training_id, user_id) VALUES (?, ?)", (id, current_user))
    
    if participants_count + 1 >= training["capacity"]:
        cursor.execute("UPDATE trainings SET status = 'full' WHERE id = ?", (id,))
        
    db.commit()
    return {"detail": "Successfully joined"}

@app.get("/api/trainings/{id}/participants", response_model=List[schemas.TrainingParticipant])
def get_participants(id: int, db: sqlite3.Connection = Depends(get_db), current_user=Depends(auth.get_current_user)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trainings WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Training not found")
        
    cursor.execute("SELECT * FROM training_participants WHERE training_id = ?", (id,))
    return [dict(row) for row in cursor.fetchall()]
