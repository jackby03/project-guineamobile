from src.users.domain.user import User


def test_set_password():
    user = User(name="Test User", email="test@example.com")
    password = "securepassword123"
    user.set_password(password)

    assert user.hashed_password is not None
    assert user.verify_password(password) is True


def test_verify_password_correct():
    user = User(name="Test User", email="test@example.com")
    password = "securepassword123"
    user.set_password(password)

    assert user.verify_password(password) is True


def test_verify_password_incorrect():
    user = User(name="Test User", email="test@example.com")
    password = "securepassword123"
    user.set_password(password)

    assert user.verify_password("wrongpassword") is False


def test_user_repr():
    user = User(user_id=1, name="Test User", email="test@example.com")
    expected_repr = "UserMode(id=1, email='test@example.com', name='Test User')"

    assert repr(user) == expected_repr
