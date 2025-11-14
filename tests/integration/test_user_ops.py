# tests/integration/test_user_ops.py
from app.schemas.base import UserCreate
from app.operations.user import create_user, get_user_by_username

def test_create_and_retrieve_user(db):
    data = UserCreate(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        username="alicesmith",
        password="Secure123"
    )

    created = create_user(db, data)
    db.commit()  # commit so it becomes queryable

    fetched = get_user_by_username(db, "alicesmith")

    assert fetched is not None
    assert fetched.email == created.email


def test_user_not_found_returns_none(db):
    assert get_user_by_username(db, "ghost_user") is None
