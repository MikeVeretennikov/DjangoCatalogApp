import os

from django.conf import settings
from django.http import HttpResponse


def download_image(request, path):
    file_path = settings.MEDIA_ROOT / path

    if os.path.exists(file_path):

        filename = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
            response["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )
            return response
    else:
        return HttpResponse(status=404)
