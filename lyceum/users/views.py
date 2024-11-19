from datetime import timedelta

import django.conf
import django.contrib.auth.mixins
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone

import users.forms
import users.models


class SignupView(django.views.generic.FormView):
    model = users.models.User
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = django.urls.reverse_lazy("homepage:index-page")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        if not user.is_active:
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

        return super().form_valid(form)


class ActivateView(django.views.generic.TemplateView):
    def get(self, request, username):
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


class UserListView(django.views.generic.ListView):
    template_name = "users/user_list.html"
    context_object_name = "users"
    queryset = (
        User.objects.filter(is_active=True)
        .select_related("profile")
        .only(
            "username",
            "first_name",
            "last_name",
            "email",
            "profile__birthday",
            "profile__image",
            "profile__coffee_count",
        )
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список пользователей"
        return context


class UserDetailView(django.views.generic.DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user"
    queryset = User.objects.only(
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пользователь детально"
        return context


class ProfileView(
    django.views.generic.DetailView,
    django.views.generic.edit.ModelFormMixin,
    django.contrib.auth.mixins.LoginRequiredMixin,
):
    model = users.models.User
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Профиль"
        return context

    def get(self, request):
        user_form = users.forms.UserForm(
            request.POST or None,
            instance=request.user,
        )
        profile_form = users.forms.ProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=request.user.profile,
        )

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    def post(self, request):
        user_form = users.forms.UserForm(
            request.POST or None,
            instance=request.user,
        )
        profile_form = users.forms.ProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )


__all__ = ()
