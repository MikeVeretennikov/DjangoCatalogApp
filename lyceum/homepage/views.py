import http

import django.db.models
import django.http
import django.shortcuts

import catalog.models
import homepage.forms


def index(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()

    context = {"items": items, "title": "Главная страница"}

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def echo(request):
    template = "homepage/echo.html"

    form = homepage.forms.EchoForm()
    context = {"form": form, "title": "Эхо"}
    return django.shortcuts.render(request, template, context)


def echo_submit(request):
    form = homepage.forms.EchoForm(request.POST)
    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data["text"]
        return django.http.HttpResponse(text)

    return django.http.HttpResponseNotAllowed(["POST"])


__all__ = []
