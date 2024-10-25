from django.http import HttpResponse
import django.shortcuts
import django.urls


def item_list(request):
    template = "catalog/item_list.html"
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


def item_detail(request, elem):
    template = "catalog/item.html"
    context = {}

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def regex_endpoint(request, number):
    return HttpResponse(f"<body>{number}</body>")


__all__ = []
