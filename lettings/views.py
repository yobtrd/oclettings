import logging

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Letting

logger = logging.getLogger(__name__)


# Aenean leo magna, vestibulum et tincidunt fermentum, consectetur quis velit. Sed non placerat
# massa. Integer est nunc, pulvinar a tempor et, bibendum id arcu. Vestibulum ante ipsum primis in
# faucibus orci luctus et ultrices posuere cubilia curae; Cras eget scelerisque
def index(request):
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


# Cras ultricies dignissim purus, vitae hendrerit ex varius non. In accumsan porta nisl id
# eleifend. Praesent dignissim, odio eu consequat pretium, purus urna vulputate arcu, vitae
# jefficitur lacus usto nec purus. Aenean finibus faucibus lectus at porta. Maecenas auctor,
# est ut luctus congue, dui enim mattis enim, ac condimentum velit libero in magna.
# Suspendisse potenti. In tempus a nisised laoreet. Suspendisse porta dui eget sem accumsan
# interdum. Ut quis urna pellentesque justo mattis ullamcorper ac non tellus. In tristique
# mauris eu velit fermentum, tempus pharetra est luctus. Vivamus consequat aliquam libero, eget
# bibendum lorem. Sed non dolor risus. Mauris condimentum auctor elementum. Donec quis nisi ligula.
# Integer vehicula tincidunt enim, ac lacinia augue pulvinar sit amet.
def letting(request, letting_id):
    try:
        letting = get_object_or_404(Letting, id=letting_id)
    except Http404:
        logger.warning("Letting not found with id %s", letting_id)
        raise

    logger.info("Viewing letting with id %s", letting_id)

    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/letting.html", context)
