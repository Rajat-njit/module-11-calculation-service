import pytest
from app.operations.calculation_factory import CalculationFactory


def test_factory_add():
    op = CalculationFactory.create("add")
    assert op.compute(3, 2) == 5


def test_factory_sub():
    op = CalculationFactory.create("sub")
    assert op.compute(5, 2) == 3


def test_factory_multiply():
    op = CalculationFactory.create("multiply")
    assert op.compute(3, 4) == 12


def test_factory_divide():
    op = CalculationFactory.create("divide")
    assert op.compute(10, 2) == 5


def test_factory_invalid_type():
    with pytest.raises(ValueError):
        CalculationFactory.create("invalid")
