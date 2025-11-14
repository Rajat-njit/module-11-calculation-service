# app/models/user.py
from datetime import datetime
import uuid
from typing import Dict, Any

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship

from passlib.context import CryptContext

from app.database import Base
from app.schemas.base import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ---------------------------------------------------------
    # 🔗 Relationship: User → Calculations (1-to-many)
    # ---------------------------------------------------------
    calculations = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ---------------------------------------------------------
    # Password helpers
    # ---------------------------------------------------------
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Securely hash a password. bcrypt supports only 72 UTF-8 bytes.
        This implementation safely trims long or non-ASCII inputs
        to avoid ValueError: "password longer than 72 bytes".
        """
        encoded = password.encode("utf-8", errors="ignore")[:72]
        safe_pw = encoded.decode("utf-8", errors="ignore")
        return pwd_context.hash(safe_pw)

    def verify_password(self, plain_password: str) -> bool:
        """Verify plaintext password against the stored hash."""
        encoded = plain_password.encode("utf-8", errors="ignore")[:72]
        safe_pw = encoded.decode("utf-8", errors="ignore")
        return pwd_context.verify(safe_pw, self.password_hash)

    # ---------------------------------------------------------
    # Registration helper
    # ---------------------------------------------------------
    @classmethod
    def register(cls, db, user_data: Dict[str, Any]) -> "User":
        """
        Create and return a validated, hashed User object.
        Uses Pydantic (UserCreate) for input validation.
        """
        validated = UserCreate.model_validate(user_data)

        # uniqueness check
        existing = db.query(cls).filter(
            (cls.email == validated.email) | (cls.username == validated.username)
        ).first()
        if existing:
            raise ValueError("Username or email already exists.")

        new_user = cls(
            first_name=validated.first_name,
            last_name=validated.last_name,
            email=validated.email,
            username=validated.username,
            password_hash=cls.hash_password(validated.password),
        )

        db.add(new_user)
        db.flush()  # generate id before commit
        return new_user

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
