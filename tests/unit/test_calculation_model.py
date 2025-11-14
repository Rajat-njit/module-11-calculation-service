from app.models.calculation import Calculation


def test_model_fields_basic():
    calc = Calculation(a=4, b=2, type="add", result=6)
    assert calc.a == 4
    assert calc.b == 2
    assert calc.type == "add"
    assert calc.result == 6


def test_model_relationship_to_user(db_session, test_user):
    # create calculation linked to a user
    calc = Calculation(
        a=10, b=5, type="sub", result=5, user_id=test_user.id
    )
    db_session.add(calc)
    db_session.commit()

    assert calc.user_id == test_user.id
    assert calc.user.username == test_user.username

    # user should have 1 calculation in its list
    assert len(test_user.calculations) == 1
