from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("homepage.urls"), name="index-page"),
    path("about/", include("about.urls"), name="about-project"),
    path("catalog/", include("catalog.urls"), name="catalog-of-goods"),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
