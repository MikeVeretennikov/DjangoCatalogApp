import http

from django.http import HttpResponse


def index(request):
    return HttpResponse("<body>Главная</body>")


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
