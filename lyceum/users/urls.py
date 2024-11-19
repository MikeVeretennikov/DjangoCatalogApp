from django.contrib.auth import views as auth_views
from django.urls import path

import users.views


app_name = "users"

urlpatterns = [
    path("user_list/", users.views.UserListView.as_view(), name="user-list"),
    path(
        "user_detail/<int:pk>/",
        users.views.UserDetailView.as_view(),
        name="user-detail",
    ),
    path("profile/", users.views.ProfileView.as_view(), name="user-profile"),
    path(
        "signup/",
        users.views.SignupView.as_view(),
        name="signup",
    ),
    path(
        "activate/<str:username>/",
        users.views.ActivateView.as_view(),
        name="activate",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
]

urlpatterns_password_reset = [
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url="done",
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            success_url="done",
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

urlpatterns += urlpatterns_password_reset
