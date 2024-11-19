import django.views.generic
from django.conf import settings
from django.http import (
    FileResponse,
    HttpResponseNotFound,
)


class DownloadDetailView(django.views.generic.TemplateView):
    def get(self, request, path_to_file):
        file_path = settings.MEDIA_ROOT / path_to_file

        if file_path.exists():
            return FileResponse(
                file_path.open("rb"),
                content_type="image",
                as_attachment=True,
            )

        return HttpResponseNotFound()


__all__ = ()
