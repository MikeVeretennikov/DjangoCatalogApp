from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

app_name = "lyceum"

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("catalog/", include("catalog.urls")),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
    path("statistics/", include("stats.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        path(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
