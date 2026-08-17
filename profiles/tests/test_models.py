import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from profiles.models import Profile


@pytest.mark.django_db
def test_profile_str():
    user = User.objects.create(
        username="Johndoe",
    )
    profile = Profile.objects.create(
        user=user,
        favorite_city="Oxford",
    )

    assert str(profile) == "Johndoe"


@pytest.mark.django_db
def test_profile_favorite_city_max_length():
    user = User.objects.create(
        username="Johndoe",
    )
    profile = Profile.objects.create(
        user=user,
        favorite_city="x" * 65,
    )

    with pytest.raises(ValidationError):
        profile.full_clean()


@pytest.mark.django_db
def test_user_can_only_have_one_profile():
    user = User.objects.create(username="Johndoe")

    Profile.objects.create(
        user=user,
        favorite_city="Oxford",
    )

    second_profile = Profile(
        user=user,
        favorite_city="London",
    )

    with pytest.raises(ValidationError):
        second_profile.full_clean()


@pytest.mark.django_db
def test_deleting_user_deletes_profile():
    user = User.objects.create(
        username="Johndoe",
    )
    profile = Profile.objects.create(
        user=user,
        favorite_city="Oxford",
    )

    profile_id = profile.id

    user.delete()

    assert not Profile.objects.filter(id=profile_id).exists()
