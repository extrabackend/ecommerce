import pytest

from helpers import load_json_data


@pytest.mark.django_db
class TestUserView:

    @pytest.mark.parametrize('case, status', (
        ('base', 200),
        ('wrong', 400),
    ))
    def test_user_create(self, case, status, client):
        data = load_json_data(f'users/views/{case}/payload.json')
        response = client.post('/users/session/', data=data)
        assert response.status_code == status
