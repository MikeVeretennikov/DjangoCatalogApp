from django.urls import path

import download.views


app_name = "download"

urlpatterns = [
    path(
        "<path:path_to_file>/",
        download.views.download_image,
        name="download-page",
    ),
]
