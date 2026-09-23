import pytest

from .models import Document
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(username="test")
    yield user
    user.delete()

@pytest.mark.django_db
class TestDocuments:
    def test_get_document(self, user):
        doc = Document.objects.create(
            title="django",
            description="django usecase",
            user=user
        )
        
        c = APIClient()
        c.force_authenticate(user=user)
        result = c.get("/api/documents/")
        res = result.json()
        result.status_code == 200
        assert res[0]["title"] == "django"
