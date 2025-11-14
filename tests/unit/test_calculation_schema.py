import pytest
from uuid import uuid4
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead
)


def test_valid_calculation_schema():
    calc = CalculationCreate(a=10, b=5, type="add")
    assert calc.a == 10
    assert calc.b == 5
    assert calc.type == "add"


def test_invalid_type_rejected():
    with pytest.raises(ValueError):
        CalculationCreate(a=10, b=5, type="invalidtype")


def test_division_by_zero_rejected():
    with pytest.raises(ValueError):
        CalculationCreate(a=10, b=0, type="divide")


def test_optional_user_id():
    user_id = uuid4()
    calc = CalculationCreate(a=5, b=2, type="multiply", user_id=user_id)
    assert calc.user_id == user_id
