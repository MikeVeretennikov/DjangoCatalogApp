import os

from django.conf import settings
from django.http import HttpResponse


def download_image(request, path):
    file_path = settings.MEDIA_ROOT / path

    if file_path.exists():
        filename = os.path.basename(file_path)
        response = HttpResponse(file_path.open("rb"), content_type="image")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse(status=404)
