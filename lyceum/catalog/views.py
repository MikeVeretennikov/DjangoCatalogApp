from django.http import HttpResponse, HttpResponseNotFound
import django.shortcuts


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
    if elem > len(context):
        return HttpResponseNotFound()
    return django.shortcuts.render(
        request,
        template,
        context={"item": context[elem - 1]},
    )


def regex_endpoint(request, number):
    return HttpResponse(f"<body>{number}</body>")
