import django.shortcuts


def description(request):
    template = "about/about.html"
    context = {"title": "О проекте"}
    return django.shortcuts.render(request, template, context)


__all__ = ()
