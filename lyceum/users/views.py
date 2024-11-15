from datetime import timedelta

import django.conf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone


import users.forms


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)

    if request.method == "POST":

        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        activation_link = (
            f"http://127.0.0.1:8000/auth/activate/{user.username}/"
        )

        send_mail(
            subject="Активация",
            message=activation_link,
            from_email=django.conf.settings.MAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        return render(request, "users/activation_sent.html", {"form": form})

    return render(request, "users/signup.html", {"form": form})


def activate(request, username):
    user = User.objects.get(username=username)

    if user.date_joined + timedelta(hours=12) > timezone.now():
        user.is_active = True
        user.save()

        return render(
            request,
            "users/activation_success.html",
            {"title": "Успешная активация"},
        )

    return render(
        request,
        "users/activation_expired.html",
        {"title": "Ссылка просрочена"},
    )


def user_list(request):
    users = User.objects.filter(is_active=True).all()

    return render(
        request,
        "users/user_list.html",
        {"users": users, "title": "Список пользователей"},
    )


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    return render(
        request,
        "users/user_detail.html",
        {"user": user, "title": user.username},
    )


@login_required
def profile(request):
    user_form = users.forms.UserForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )

    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect("users:user-profile")

    return render(
        request,
        "users/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "title": "Профиль",
        },
    )


__all__ = []
