import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt
from sqlmodel import Session, select
from src.config import Settings
from src.models.user import User, UserCreate

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hash using bcrypt directly"""
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generate a password hash using bcrypt directly"""
    password_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    settings = Settings()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
    return encoded_jwt

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Retrieve a user by their email address"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user_in: UserCreate) -> User:
    """Create a new user in the database"""
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
