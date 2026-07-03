# schemas.py
# Yeh file define karti hai ki API requests/responses mein data kaisa dikhna chahiye

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ---------- USER SCHEMAS ----------

# Jab user signup karega, yeh data aayega
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Jab user login karega, yeh data aayega
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Jab hum user ka data response mein bhejenge (password kabhi nahi bhejenge)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy model ko Pydantic schema mein convert karne ke liye


# ---------- TOKEN SCHEMA ----------

# Login successful hone par yeh response jayega
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- CHAT SCHEMAS ----------

class ChatCreate(BaseModel):
    title: Optional[str] = "New Chat"


class ChatRename(BaseModel):
    title: str


class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- MESSAGE SCHEMAS ----------

class MessageCreate(BaseModel):
    content: str  # user jo message type karega


class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True