from app.operations.calculation_ops import (
    AddOperation,
    SubOperation,
    MultiplyOperation,
    DivideOperation,
)

class CalculationFactory:
    """Factory to return the correct operation class based on type."""

    operation_map = {
        "add": AddOperation,
        "sub": SubOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
    }

    @classmethod
    def create(cls, calc_type: str):
        """
        Returns the correct operation CLASS.
        Tests expect only (type) -> class, not instantiation.
        """
        op_class = cls.operation_map.get(calc_type.lower())
        if not op_class:
            raise ValueError(f"Invalid calculation type: {calc_type}")
        return op_class
