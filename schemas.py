from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRegister(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str

class Horse(BaseModel):
    id: int
    name: str
    discipline: str
    daily_limit: int

class Trainer(BaseModel):
    id: int
    name: str
    surname: str
    specialization: Optional[str] = None

class TrainingTypeMode(str, Enum):
    individual = "individual"
    group = "group"

class TrainingTypeDiscipline(str, Enum):
    Dressage = "Dressage"
    Jumping = "Jumping"
    Recreational = "Recreational"

class TrainingType(BaseModel):
    id: int
    discipline: TrainingTypeDiscipline
    training_mode: TrainingTypeMode

class TrainingStatus(str, Enum):
    open = "open"
    full = "full"
    completed = "completed"
    cancelled = "cancelled"

class Training(BaseModel):
    id: int
    horse_id: int
    trainer_id: int
    training_type_id: int
    date: datetime
    capacity: int
    status: TrainingStatus
    created_at: Optional[datetime] = None

class TrainingCreate(BaseModel):
    horse_id: int
    trainer_id: int
    training_type_id: int
    date: datetime

class TrainingUpdate(BaseModel):
    horse_id: Optional[int] = None
    trainer_id: Optional[int] = None
    training_type_id: Optional[int] = None
    date: Optional[datetime] = None
    capacity: Optional[int] = None
    status: Optional[TrainingStatus] = None

class TrainingParticipant(BaseModel):
    id: int
    training_id: int
    user_id: int

class JoinTraining(BaseModel):
    pass
