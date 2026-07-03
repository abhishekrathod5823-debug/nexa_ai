# auth_routes.py
# Yeh file Signup aur Login se related saari APIs handle karti hai

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, Token
from app.auth import hash_password, verify_password, create_access_token

# Router banate hain - yeh ek "mini FastAPI app" hai jo main app mein jud jayega
router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------- SIGNUP API ----------
@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    
    # Step 1: Check karo ki email already registered to nahi
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Step 2: Password ko hash karo
    hashed_pwd = hash_password(user_data.password)
    
    # Step 3: Naya user object banao
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_pwd
    )
    
    # Step 4: Database mein save karo
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Step 5: User ka data return karo (password_hash UserResponse schema mein nahi hai, isliye safe hai)
    return new_user

# ---------- LOGIN API ----------
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    
    # Step 1: Email se user dhundo database mein
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # Step 2: Agar user nahi mila, error do
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Step 3: Password verify karo (plain password vs database hash)
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Step 4: JWT token banao
    access_token = create_access_token(data={"user_id": user.id})
    
    # Step 5: Token return karo
    return {"access_token": access_token, "token_type": "bearer"}