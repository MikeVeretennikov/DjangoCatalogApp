import re

from django.conf import settings


@staticmethod
def reverse_russian_words(content):
    return re.sub(r"[А-яёЁ]+", lambda m: m.group()[::-1], content)


class ReverseResponseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.ALLOW_REVERSE:
            return response

        ReverseResponseMiddleware.count += 1
        if ReverseResponseMiddleware.count >= 10:
            ReverseResponseMiddleware.count = 0
            response.content = reverse_russian_words(
                response.content.decode("utf-8")
            ).encode("utf-8")

        return response
