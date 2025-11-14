# app/schemas/calculation.py
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, model_validator

# Supported operation types
VALID_TYPES = {"add", "sub", "multiply", "divide"}


class CalculationBase(BaseModel):
    """
    Shared fields and validation for calculation objects.
    """
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")
    type: str = Field(
        ...,
        description='Type of operation: "add", "sub", "multiply", or "divide".',
    )
    user_id: Optional[UUID] = Field(
        default=None,
        description="Optional ID of the user who owns this calculation.",
    )

    # Allow constructing from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def normalize_and_validate(self):
        """
        Pydantic v2 style validator that:
        - normalizes type to lowercase
        - ensures it's one of the allowed operations
        - prevents division by zero when type == 'divide'
        """
        t = (self.type or "").strip().lower()

        if t not in VALID_TYPES:
            allowed = ", ".join(sorted(VALID_TYPES))
            raise ValueError(f"type must be one of: {allowed}")

        if t == "divide" and self.b == 0:
            raise ValueError("Cannot divide by zero")

        # normalize back onto the object
        self.type = t
        return self


class CalculationCreate(CalculationBase):
    """
    Schema for creating a calculation.
    Client sends: a, b, type, optional user_id.
    The server / factory will compute and persist `result`.
    """
    pass


class CalculationRead(CalculationBase):
    """
    Schema returned to the client when reading a calculation.
    Adjust `id` type (int vs UUID) to match your SQLAlchemy model.
    """
    id: UUID
    result: Optional[float] = Field(
        default=None,
        description="Result of the calculation, if computed/stored.",
    )
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
