from django.http import HttpResponse


def index(request):
    return HttpResponse("<body>Главная</body>")
