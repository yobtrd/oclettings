from django.urls import resolve, reverse

from profiles import views


def test_profile_index_url():
    path = reverse("profiles:index")

    assert path == "/profiles/"
    assert resolve(path).view_name == "profiles:index"
    assert resolve(path).func == views.index


def test_profile_url():
    path = reverse("profiles:profile", kwargs={"username": "Johndoe"})

    assert path == "/profiles/Johndoe/"
    assert resolve(path).view_name == "profiles:profile"
    assert resolve(path).func == views.profile
