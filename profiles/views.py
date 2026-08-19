import logging

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Profile

logger = logging.getLogger(__name__)


# Sed placerat quam in pulvinar commodo. Nullam laoreet consectetur ex, sed consequat
# libero pulvinar eget. Fusc faucibus, urna quis auctor pharetra, massa dolor cursus neque,
# quis dictum lacus d
def index(request):
    profiles_list = Profile.objects.all()
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


# Aliquam sed metus eget nisi tincidunt ornare accumsan eget lac
# laoreet neque quis, pellentesque dui. Nullam facilisis pharetra vulputate. Sed tincidunt, dolor
# id facilisis fringilla, eros leo tristique lacus, it. Nam aliquam dignissim congue.
# Pellentesque habitant morbi tristique senectus et netus et males
def profile(request, username):
    try:
        profile = get_object_or_404(Profile, user__username=username)
    except Http404:
        logger.warning("Profile not found for username %s", username)
        raise

    logger.info("Viewing profile for user %s", username)

    context = {"profile": profile}
    return render(request, "profiles/profile.html", context)
