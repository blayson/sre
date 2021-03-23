

def test_model_email(user):
    assert user.email == 'test@test.com'


def test_model_name(user):
    assert user.name is None

