# message_routes.py
# Yeh file messages send karne aur chat history dekhne ki APIs handle karti hai

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from groq import Groq

from app.database import get_db
from app.models import Chat, Message, User
from app.schemas import MessageCreate, MessageResponse
from app.auth import get_current_user
from app.config import GROQ_API_KEY

router = APIRouter(prefix="/chats", tags=["Messages"])

# Groq client banate hain
client = Groq(api_key=GROQ_API_KEY)


# ---------- MESSAGE BHEJO AUR AI RESPONSE LO ----------
@router.post("/{chat_id}/messages", response_model=List[MessageResponse])
def send_message(
    chat_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Step 1: Check karo ki chat exist karti hai aur current user ki hai
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    # Step 2: User ka message database mein save karo
    user_message = Message(
        chat_id=chat_id,
        sender="user",
        content=message_data.content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Step 3: Pichli saari messages lo (context ke liye)
    previous_messages = db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.created_at.asc()).all()

    # Step 4: Groq ke liye message history format banao
    groq_messages = [
        {
            "role": "system",
            "content": """Aap Nexa AI hain — ek helpful, smart aur friendly AI assistant. 
            Aap Hindi, English aur Hinglish (Hindi+English mix) teeno mein baat kar sakte hain.
            User jis bhi language mein baat kare, aap usi mein jawab dijiye.
            Hamesha helpful, accurate aur friendly rahein."""
        }
    ]

    # Pichle messages add karo (last 10 messages ka context)
    for msg in previous_messages[-10:]:
        groq_messages.append({
            "role": "user" if msg.sender == "user" else "assistant",
            "content": msg.content
        })

    # Step 5: Groq API ko call karo
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Groq ka fast aur powerful model
            messages=groq_messages,
            max_tokens=1024,
            temperature=0.7  # 0 = strict/factual, 1 = creative
        )

        ai_response_text = completion.choices[0].message.content

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )

    # Step 6: AI ka response database mein save karo
    ai_message = Message(
        chat_id=chat_id,
        sender="ai",
        content=ai_response_text
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    # Step 7: User message aur AI response dono return karo
    return [user_message, ai_message]


# ---------- CHAT KI SAARI MESSAGES DEKHO ----------
@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
def get_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Pehle check karo chat is user ki hai
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    # Saari messages lo latest order mein
    messages = db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.created_at.asc()).all()

    return messages