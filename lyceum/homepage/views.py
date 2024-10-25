import http

import django.shortcuts


def index(request):
    template = "homepage/main.html"
    context = [
        {
            "id": 1,
            "name": "Кубик рубика",
            "description": "Хороший тренажер мозга",
            "image": "rubic.jpg",
        },
        {
            "id": 2,
            "name": "Клавиатура",
            "description": "Бюджетная механическая клавиатура",
            "image": "keyboard.jpg",
        },
        {
            "id": 3,
            "name": "Боржоми",
            "description": "Поздно Вася пить боржоми когда почки отказали",
            "image": "borjomi.jpg",
        },
    ]
    return django.shortcuts.render(
        request,
        template,
        context={"content": context},
    )


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


__all__ = []
