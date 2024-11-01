from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound


def download_image(request, path):
    file_path = settings.MEDIA_ROOT / path

    if file_path.exists():
        return FileResponse(
            file_path.open("rb"),
            content_type="image",
            as_attachment=True,
        )

    return HttpResponseNotFound()


__all__ = []
