# app/models/calculation.py
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Calculation(Base):
    __tablename__ = "calculations"

    # Allow SQLAlchemy to skip strict typing checks
    __allow_unmapped__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # operands
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)

    # operation type: "add", "sub", "multiply", "divide"
    type = Column(String(20), nullable=False)

    # we choose to store result in the DB (could also be computed on demand)
    result = Column(Float, nullable=True)

    # optional link to a user (foreign key into users.id)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship back to User (optional but nice)
    user: Optional["User"] = relationship("User", back_populates="calculations")

    # --------------------------------------
    # Helper: compute result for this record
    # --------------------------------------
    def compute_result(self) -> float:
        """Compute the result based on (a, b, type). Raises on invalid type or bad input."""
        if self.type == "add":
            return self.a + self.b
        elif self.type == "sub":
            return self.a - self.b
        elif self.type == "multiply":
            return self.a * self.b
        elif self.type == "divide":
            if self.b == 0:
                raise ValueError("Division by zero is not allowed")
            return self.a / self.b
        else:
            raise ValueError(f"Unsupported calculation type: {self.type}")

    def __repr__(self) -> str:  # for debugging/logging
        return (
            f"<Calculation(id={self.id}, type={self.type}, "
            f"a={self.a}, b={self.b}, result={self.result})>"
        )
