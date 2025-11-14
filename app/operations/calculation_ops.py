class AddOperation:
    @staticmethod
    def compute(a, b):
        return a + b


class SubOperation:
    @staticmethod
    def compute(a, b):
        return a - b


class MultiplyOperation:
    @staticmethod
    def compute(a, b):
        return a * b


class DivideOperation:
    @staticmethod
    def compute(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
