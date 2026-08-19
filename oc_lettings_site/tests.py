"""Tests for the oc_lettings_site application."""

import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

from oc_lettings_site import views


# Config
###########
def test_environment():
    """Test that tests runs in the test environment."""
    from django.conf import settings

    assert settings.ENVIRONMENT == "test"


# URL
###########
def test_oc_lettings_index_url():
    """Test that the home page URL resolves correctly."""
    path = reverse("index")

    assert path == "/"
    assert resolve(path).view_name == "index"
    assert resolve(path).func == views.index


def test_lettings_root_url():
    """Test that the lettings root URL resolves correctly."""
    path = reverse("lettings:index")

    assert path == "/lettings/"
    assert resolve(path).view_name == "lettings:index"


def test_profiles_root_url():
    """Test that the profiles root URL resolves correctly."""
    path = reverse("profiles:index")

    assert path == "/profiles/"
    assert resolve(path).view_name == "profiles:index"


def test_admin_url():
    """Test that the admin URL resolves correctly."""
    path = reverse("admin:index")

    assert path == "/admin/"
    assert resolve(path).view_name == "admin:index"


# Views
###########
def test_index_view(client):
    """Test that the home page is displayed correctly."""
    response = client.get("/")

    assert response.status_code == 200
    assertTemplateUsed(response, "index.html")


@pytest.mark.django_db
def test_unknown_url_returns_404(client):
    """Test that an unknown URL returns a 404 error page."""
    response = client.get("/this-does-not-exist/")

    assert response.status_code == 404
    assertTemplateUsed(response, "404.html")
