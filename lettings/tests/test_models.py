"""Tests for the lettings application models."""

import pytest
from django.core.exceptions import ValidationError

from lettings.models import Address, Letting


@pytest.mark.django_db
def test_address_str():
    """Test that an address returns its number and street as a string."""
    address = Address.objects.create(
        number=12,
        street="Rue de Paris",
        city="Paris",
        state="FR",
        zip_code=75001,
        country_iso_code="FRA",
    )

    assert str(address) == "12 Rue de Paris"


def test_address_number_max_value():
    """Test that an address number cannot exceed the maximum value."""
    address = Address(
        number=10000,
        street="Rue de Paris",
        city="Paris",
        state="FR",
        zip_code=75001,
        country_iso_code="FRA",
    )

    with pytest.raises(ValidationError):
        address.full_clean()


@pytest.mark.django_db
def test_letting_str():
    """Test that a letting returns its title as a string."""
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

    assert str(letting) == "Super chalet"
    assert letting.address == address
    assert address.letting == letting


@pytest.mark.django_db
def test_address_can_only_be_used_by_one_letting():
    """Test that an address can only be associated with one letting."""
    address = Address.objects.create(
        number=12,
        street="Rue de Paris",
        city="Paris",
        state="FR",
        zip_code=75001,
        country_iso_code="FRA",
    )

    Letting.objects.create(
        title="Premier chalet",
        address=address,
    )

    second_letting = Letting(
        title="Deuxième chalet",
        address=address,
    )

    with pytest.raises(ValidationError):
        second_letting.full_clean()


@pytest.mark.django_db
def test_deleting_address_deletes_letting():
    """Test that deleting an address also deletes its letting."""
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

    letting_id = letting.id

    address.delete()

    assert not Letting.objects.filter(id=letting_id).exists()


def test_address_verbose_names():
    """Test that the Address model has the correct singular and plural names."""
    assert Address._meta.verbose_name == "Address"
    assert Address._meta.verbose_name_plural == "Addresses"
