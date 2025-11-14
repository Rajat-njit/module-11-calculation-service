# tests/integration/test_calculation_db.py

import pytest
from uuid import uuid4

from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import CalculationCreate
from app.operations.calculation_factory import CalculationFactory


def test_create_calculation_in_db(db):
    """Ensure a calculation is inserted into DB and retrieved correctly."""

    # Create user first (FK requirement)
    user = User(
        first_name="Test",
        last_name="User",
        username="calc_user",
        email="calcuser@example.com",
        password_hash=User.hash_password("password123")
    )
    db.add(user)
    db.flush()

    # Build schema
    schema = CalculationCreate(
        a=10,
        b=5,
        type="add",
        user_id=user.id
    )

    # Run factory
    op = CalculationFactory.create(schema.type)
    result = op.compute(schema.a, schema.b)

    # Save to DB
    calc = Calculation(
        a=schema.a,
        b=schema.b,
        type=schema.type,
        result=result,
        user_id=user.id
    )
    db.add(calc)
    db.commit()

    # Retrieve & validate
    saved = db.query(Calculation).filter_by(id=calc.id).first()

    assert saved is not None
    assert saved.a == 10
    assert saved.b == 5
    assert saved.type == "add"
    assert saved.result == 15
    assert saved.user_id == user.id



def test_calculation_invalid_type_rejected(db):
    """Invalid type should cause Pydantic validation error."""

    with pytest.raises(ValueError):
        CalculationCreate(a=3, b=4, type="invalid")



def test_division_by_zero_integration(db):
    """Division by zero should be rejected by schema validator."""
    with pytest.raises(ValueError):
        CalculationCreate(a=10, b=0, type="divide")



def test_calculation_relationship(db):
    """Test User → Calculation relationship works at ORM level."""

    user = User(
        first_name="Alice",
        last_name="RelTest",
        username="reluser",
        email="rel@example.com",
        password_hash=User.hash_password("pw123")
    )
    db.add(user)
    db.flush()

    calc = Calculation(
        a=8, b=2, type="divide", result=4, user_id=user.id
    )
    db.add(calc)
    db.commit()

    # Refresh user
    db.refresh(user)

    assert len(user.calculations) == 1
    assert user.calculations[0].result == 4
    assert user.calculations[0].type == "divide"
