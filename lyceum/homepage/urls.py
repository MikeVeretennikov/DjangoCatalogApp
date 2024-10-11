from django.urls import path

import views


urlpatterns = [path("", views.index), path("coffee/", views.coffee)]
