from django.urls import path

import feedback.views


app_name = "feedback"

urlpatterns = [
    path("", feedback.views.FeedbackView.as_view(), name="feedback"),
]
