
# **Module 11 — Secure Calculation Service (FastAPI + SQLAlchemy + Pydantic + CI/CD + Docker)**

### *Advanced Backend Development with Testing, Design Patterns, and Deployment*

---

## **📌 Introduction**

This project builds upon the secure user system developed in Module 10 and extends the application by introducing a fully modeled, validated, and test-driven **Calculation Service**. This module implements a professional-grade backend architecture used in real-world systems, integrating:

* SQLAlchemy ORM models
* Pydantic validation schemas
* Password hashing & secure user handling
* A full calculation engine with a **Factory Design Pattern**
* Unit testing and integration testing
* GitHub Actions CI/CD pipeline
* Docker image build + security scan + deployment to Docker Hub

This README provides a detailed explanation of all implemented features, how to run the system, how to test it locally, how the CI/CD pipeline is structured, and how the calculation model integrates with existing components.

---

# **📂 Project Structure**

```
module-11/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── database_init.py
│   ├── models/
│   │   ├── user.py
│   │   ├── calculation.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── calculation.py
│   │   ├── user.py
│   │   ├── base.py
│   │   └── __init__.py
│   ├── operations/
│   │   ├── user.py
│   │   ├── calculation_ops.py
│   │   └── calculation_factory.py
│   ├── factories/
│   │   └── calculation_factory.py
│   ├── routes/
│       └── (Module 12 will add Calculation endpoints)
│
├── tests/
│   ├── unit/
│   │   ├── test_calculation_factory.py
│   │   ├── test_calculation_schema.py
│   │   ├── test_calculation_model.py
│   │   ├── test_models.py
│   │   ├── test_dependencies.py
│   │   └── test_schemas.py
│   ├── integration/
│   │   ├── test_user_ops.py
│   │   └── test_calculation_db.py
│   └── conftest.py
│
├── dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── .github/workflows/ci.yml
```

This structure mirrors real-world production layouts used in enterprise backends.

---

# **⚙️ Installation, Setup & Running the App**

## **1. Install Dependencies**

```
pip install -r requirements.txt
```

Key dependencies include:

```
fastapi
uvicorn
sqlalchemy
pydantic
passlib[bcrypt]
psycopg2-binary
pytest
pytest-cov
Faker
```

---

# **📦 requirements.txt (for reference)**

```
fastapi
uvicorn
sqlalchemy
alembic
pydantic
passlib[bcrypt]
psycopg2-binary
pytest
pytest-cov
python-multipart
httpx
Faker
```

---

# **🔐 Environment Variables (.env)**

For local development:

```
DATABASE_URL=sqlite:///./test.db
```

For Docker:

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
```

GitHub Actions uses:

```
postgresql+psycopg2://postgres:postgres@localhost:5432/test_db
```

---

# **🧩 SQLAlchemy Models**

## **User Model (enhanced from Module 10)**

Key features:

* UUID primary key
* Hashed passwords using bcrypt
* Unique username + email
* Relationship to `Calculation` model
* `register` method for secure creation

Example snippet:

```python
calculations = relationship("Calculation", back_populates="user")
```

---

# **🧮 Calculation Model (Module 11 Requirement)**

### Fields:

| Field   | Type        | Description                   |
| ------- | ----------- | ----------------------------- |
| id      | UUID        | Primary key                   |
| a       | Float       | First operand                 |
| b       | Float       | Second operand                |
| type    | Enum (text) | add, sub, multiply, divide    |
| result  | Float       | Auto-computed optional result |
| user_id | UUID        | FK to users                   |

### Model Snippet:

```python
user = relationship("User", back_populates="calculations")
```

---

# **📝 Pydantic Schemas**

### **CalculationCreate**

* Accepts: `a`, `b`, `type`, `user_id`
* Validates operation type
* Prevents division by zero
* Normalizes cases for type

Example:

```python
@field_validator("b")
def validate_divisor(cls, v, values):
    if "type" in values and values["type"] == "divide" and v == 0:
        raise ValueError("Cannot divide by zero")
    return v
```

### **CalculationRead**

* Includes `id`, `result`, `user_id`
* Uses `from_attributes=True` for ORM conversion

---

# **🏭 Factory Pattern**

The calculation logic uses:

* AddOperation
* SubOperation
* MultiplyOperation
* DivideOperation

And a **CalculationFactory**:

```python
operation_map = {
    "add": AddOperation,
    "sub": SubOperation,
    "multiply": MultiplyOperation,
    "divide": DivideOperation,
}
```

Example usage:

```python
op = CalculationFactory.create("multiply")
result = op.compute(3, 4)  # 12
```

This modular design allows future extension (e.g., Modulus, Power, SquareRoot).

---

# **🧪 Testing Strategy (Unit + Integration)**

Testing is a major grading criterion for this assignment.
We implemented **full unit tests + integration tests** using:

* SQLite for lightweight local testing
* PostgreSQL (via GitHub Actions) for production-like integration testing

---

# **🧪 UNIT TESTS**

### 1. **Calculation Factory**

* Ensures each operation returns correct results
* Ensures invalid type raises error

```python
def test_factory_add():
    op = CalculationFactory.create("add")
    assert op.compute(3, 2) == 5
```

### 2. **Schemas**

* Valid type
* Invalid type
* Division by zero
* Optional user_id

```python
with pytest.raises(ValueError):
    CalculationCreate(a=5, b=0, type="divide")
```

### 3. **Model Tests**

Check SQLAlchemy fields + relationships:

```python
assert calc.user is not None
```

### 4. **User Tests**

* Password hashing
* Password verification
* repr()

---

# **🔗 Integration Tests**

These run against a real PostgreSQL database in CI:

### 1. **test_user_ops.py**

* Create user
* Fetch user
* Ensure uniqueness constraint

### 2. **test_calculation_db.py**

* Insert calculation
* Ensure auto result
* Ensure FK constraint

---

# **🧪 Running Tests Locally**

This is *required in the grading rubric*.

## **1. Run ONLY Unit Tests**

```
pytest tests/unit -v -s
```

## **2. Run ONLY Integration Tests (SQLite)**

```
pytest tests/integration -v -s
```

## **3. Run Full Suite**

```
pytest -v -s
```

## **4. Run With Coverage**

```
pytest --cov=app --cov-report=term-missing
```

---

# **🐳 Running Tests with Docker (Alternate Method)**

### **Build the image**

```
docker build -t module11-app .
```

### **Run PostgreSQL**

```
docker-compose up -d db
```

### **Run FastAPI container**

```
docker-compose up --build
```

### **Run tests inside container**

```
docker exec -it fastapi_app pytest
```

---

# **📦 Docker Deployment**

## **Dockerfile**

The Dockerfile supports production-grade builds with:

* Python slim base image
* psycopg2 dependencies
* pip optimization
* Uvicorn server

Snippet:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## **docker-compose.yml**

Runs:

* PostgreSQL container
* FastAPI container
* Auto-networking

---

# **🌐 Docker Hub Repository**

Your pushed repository:

### **➡ [https://hub.docker.com/r/rajatpednekar/module11-calculation-service](https://hub.docker.com/r/rajatpednekar/module11-calculation-service)**

Images pushed:

* `latest`
* `${GITHUB_RUN_NUMBER}`

Example:

```
docker pull rajatpednekar/module11-calculation-service:latest
```

---

# **🔄 CI/CD Pipeline (GitHub Actions)**

This is one of the main grading items.

Your final pipeline includes:

### ✔ Automatic testing

### ✔ PostgreSQL container

### ✔ Coverage reporting

### ✔ Docker buildx

### ✔ Docker Hub login

### ✔ Docker push

### ✔ Trivy security scan

### **Snippet (abbreviated):**

```yaml
- name: 🧪 Run Pytest with Coverage
  run: pytest --cov=app --cov-report=xml
```

```yaml
- name: 🏗️ Build and Push
  uses: docker/build-push-action@v5
  with:
    tags: |
      ${{ secrets.DOCKERHUB_USERNAME }}/module11-calculation-service:latest
```

---

# **✨ Key Features Summary (For Professor’s Script)**

### **Secure User Model**

* Fully hashed passwords
* Unique constraints
* Pydantic validation
* SQLAlchemy relationship

### **Calculation System**

* Full CRUD-ready model
* Pydantic validation
* Division by zero checks
* Factory Design Pattern
* Clean, extensible architecture

### **Testing**

* Full unit tests
* Full integration tests
* Faker integration
* Extensive validation tests

### **CI/CD**

* Full pipeline
* Postgres for integration
* Docker Buildx
* Docker Hub Deployment
* Vulnerability scans

### **Docker**

* Fully buildable image
* Production-ready
* Pullable by instructor
* Compose stack with PostgreSQL

---

# **📚 How to Run Tests Locally (Detailed)**

### 1. Start Virtual Environment

```
source venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run tests

```
pytest -v -s
```

### 4. Run integration tests ONLY

```
pytest tests/integration -v
```

### 5. With coverage

```
pytest --cov=app --cov-report=term-missing
```

### 6. Run using Docker Compose

```
docker-compose up --build
```

---

# **📘 Conclusion**

This module demonstrates professional backend engineering practices:

* Clean SQLAlchemy modeling
* Safe password hashing
* Pydantic validation
* Design patterns (Factory)
* Full testing suite
* Dockerized deployment
* CI/CD pipeline with security

---
