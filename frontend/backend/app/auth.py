# auth.py
# Yeh file password hashing aur JWT token banane/verify karne ka kaam karti hai

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

# bcrypt ka context banate hain password hash karne ke liye
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- PASSWORD FUNCTIONS ----------

def hash_password(password: str) -> str:
    """Plain password ko bcrypt se hash (encrypt) karta hai"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login ke waqt, diya gaya password aur database wala hash match karta hai"""
    return pwd_context.verify(plain_password, hashed_password)


# ---------- JWT TOKEN FUNCTIONS ----------

def create_access_token(data: dict) -> str:
    """Naya JWT token banata hai, jisme user ka data (jaise user_id) encoded hota hai"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    """Token ko verify karta hai aur usme se data nikalta hai. Invalid/expired ho to None deta hai"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
    

# auth.py mein yeh imports upar add karo (file ke top pe)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db

# OAuth2 scheme - yeh batata hai ki token "Authorization: Bearer <token>" header mein aayega
security = HTTPBearer()

# ---------- CURRENT USER DEPENDENCY ----------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    
    payload = verify_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_id = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    from app.models import User
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user