"""Tests for the lettings application URLs."""

from django.urls import resolve, reverse

from lettings import views


def test_letting_index_url():
    """Test that the lettings index URL resolves correctly."""
    path = reverse("lettings:index")

    assert path == "/lettings/"
    assert resolve(path).view_name == "lettings:index"
    assert resolve(path).func == views.index


def test_letting_url():
    """Test that the letting detail URL resolves correctly."""
    path = reverse("lettings:letting", kwargs={"letting_id": 42})

    assert path == "/lettings/42/"
    assert resolve(path).view_name == "lettings:letting"
    assert resolve(path).func == views.letting
