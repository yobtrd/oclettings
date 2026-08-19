"""Tests for the profiles application URLs."""

from django.urls import resolve, reverse

from profiles import views


def test_profile_index_url():
    """Test that the profiles index URL resolves correctly."""
    path = reverse("profiles:index")

    assert path == "/profiles/"
    assert resolve(path).view_name == "profiles:index"
    assert resolve(path).func == views.index


def test_profile_url():
    """Test that the profile detail URL resolves correctly."""
    path = reverse("profiles:profile", kwargs={"username": "Johndoe"})

    assert path == "/profiles/Johndoe/"
    assert resolve(path).view_name == "profiles:profile"
    assert resolve(path).func == views.profile
