from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.db.session import get_db
from app.models import Profile, User
from app.schemas import Token, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        email=user_data.email.lower(),
        username=user_data.username.strip(),
        full_name=user_data.full_name.strip(),
        password_hash=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = Profile(user_id=user.id, branch="", semester="", target_role="", bio="", skills="", interests="")
    db.add(profile)
    db.commit()

    user.profile = profile
    return user


@router.post("/login", response_model=Token)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email.lower()).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
