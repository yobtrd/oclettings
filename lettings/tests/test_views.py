"""Tests for the lettings application views."""

import pytest
from pytest_django.asserts import assertTemplateUsed

from lettings.models import Address, Letting


@pytest.mark.django_db
def test_letting_index_view(client):
    """Test that the lettings index view is displayed correctly."""
    response = client.get("/lettings/")

    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/index.html")
    assert "lettings_list" in response.context


@pytest.mark.django_db
def test_letting_view(client):
    """Test that a letting detail view is displayed correctly."""
    address = Address.objects.create(
        number=12,
        street="Rue de Paris",
        city="Paris",
        state="FR",
        zip_code=75001,
        country_iso_code="FRA",
    )
    letting = Letting.objects.create(
        title="Super chalet",
        address=address,
    )

    response = client.get(f"/lettings/{letting.id}/")

    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/letting.html")
    assert response.context["title"] == "Super chalet"
    assert response.context["address"] == address


@pytest.mark.django_db
def test_letting_view_returns_404_for_unknown_letting(client):
    """Test that an unknown letting returns a 404 error page."""
    response = client.get("/lettings/999999/")

    assert response.status_code == 404
    assertTemplateUsed(response, "404.html")
