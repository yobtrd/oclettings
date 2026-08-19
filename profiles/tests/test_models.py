"""Tests for the profiles application models."""

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from profiles.models import Profile


@pytest.mark.django_db
def test_profile_str():
    """Test that a profile returns its username as a string."""
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
    """Test that a profile favorite city cannot exceed the maximum length."""
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
    """Test that a user can only be associated with one profile."""
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
    """Test that deleting a user also deletes its profile."""
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
