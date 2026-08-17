import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed

from profiles.models import Profile


@pytest.mark.django_db
def test_profile_index_view(client):
    response = client.get("/profiles/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/index.html")
    assert "profiles_list" in response.context


@pytest.mark.django_db
def test_profile_view(client):
    user = User.objects.create(
        username="Johndoe",
        email="Johndoe@gmail.com",
    )
    profile = Profile.objects.create(
        user=user,
        favorite_city="Oxford",
    )

    response = client.get(f"/profiles/{profile.user.username}/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile.html")
    assert response.context["profile"] == profile
    assert response.context["profile"].user.email == "Johndoe@gmail.com"
    assert response.context["profile"].favorite_city == "Oxford"


@pytest.mark.django_db
def test_profile_view_returns_404_for_unknown_profile(client):
    response = client.get("/profiles/UnknownUser/")

    assert response.status_code == 404
