# models.py
# Yeh file database ke tables ko Python classes ke roop mein define karti hai

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# ---------- USERS TABLE ----------
class User(Base):
    __tablename__ = "users"  # actual MySQL table ka naam

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship: ek user ke multiple chats ho sakte hain
    chats = relationship("Chat", back_populates="owner", cascade="all, delete")


# ---------- CHATS TABLE ----------
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False, default="New Chat")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship: yeh chat kis user ka hai
    owner = relationship("User", back_populates="chats")

    # Relationship: ek chat ke multiple messages ho sakte hain
    messages = relationship("Message", back_populates="chat", cascade="all, delete")


# ---------- MESSAGES TABLE ----------
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender = Column(Enum("user", "ai"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship: yeh message kis chat ka hai
    chat = relationship("Chat", back_populates="messages")