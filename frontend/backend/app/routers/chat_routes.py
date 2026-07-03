# chat_routes.py
# Yeh file chat create, rename, delete aur list karne ki APIs handle karti hai

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Chat, User
from app.schemas import ChatCreate, ChatRename, ChatResponse
from app.auth import get_current_user

router = APIRouter(prefix="/chats", tags=["Chats"])


# ---------- NAYI CHAT BANAO ----------
@router.post("/", response_model=ChatResponse)
def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_chat = Chat(
        user_id=current_user.id,
        title=chat_data.title or "New Chat"
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


# ---------- APNI SAARI CHATS DEKHO ----------
@router.get("/", response_model=List[ChatResponse])
def get_all_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = db.query(Chat).filter(
        Chat.user_id == current_user.id
    ).order_by(Chat.created_at.desc()).all()
    return chats


# ---------- EK SPECIFIC CHAT DEKHO ----------
@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return chat


# ---------- CHAT RENAME KARO ----------
@router.put("/{chat_id}/rename", response_model=ChatResponse)
def rename_chat(
    chat_id: int,
    chat_data: ChatRename,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    chat.title = chat_data.title
    db.commit()
    db.refresh(chat)
    return chat


# ---------- CHAT DELETE KARO ----------
@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}