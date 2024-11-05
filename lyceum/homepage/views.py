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


@django.views.decorators.csrf.csrf_protect
@django.views.decorators.http.require_GET
def echo(request):

    template = "homepage/echo.html"

    form = homepage.forms.EchoForm()
    context = {"form": form, "title": "Эхо"}
    return django.shortcuts.render(request, template, context)


@django.views.decorators.csrf.csrf_protect
@django.views.decorators.http.require_POST
def echo_submit(request):
    form = homepage.forms.EchoForm(request.POST)
    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data["text"]
        return django.http.HttpResponse(text)

    return django.http.HttpResponseNotAllowed()


__all__ = []
