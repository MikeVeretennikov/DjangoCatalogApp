import http

import django.db.models
import django.http
import django.shortcuts
import django.views
import django.views.decorators
import django.views.decorators.csrf
import django.views.decorators.http

import catalog.models
import homepage.forms


class HomepageListView(django.views.generic.ListView):
    template_name = "homepage/main.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.on_main()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class CoffeeListView(django.views.generic.TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.profile.coffee_count += 1
            request.user.profile.save()

        return django.http.HttpResponse(
            "Я чайник",
            status=http.HTTPStatus.IM_A_TEAPOT,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Я чайник"
        return context


class EchoView(django.views.generic.FormView):
    form_class = homepage.forms.EchoForm
    template_name = "homepage/echo.html"
    success_url = django.urls.reverse_lazy("homepage:echo-submit-page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Эхо"
        return context


class EchoSubmitView(django.views.generic.TemplateView):
    def get(self, request):
        return django.http.HttpResponse(
            status=http.HTTPStatus.METHOD_NOT_ALLOWED,
        )

    def post(self, request):
        form = homepage.forms.EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return django.http.HttpResponse(text)

        return django.http.HttpResponse(
            status=http.HTTPStatus.METHOD_NOT_ALLOWED,
        )


__all__ = ()
