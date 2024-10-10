import re

from django.conf import settings


class ReverseResponseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.ALLOW_REVERSE:
            ReverseResponseMiddleware.count += 1

        if settings.ALLOW_REVERSE and ReverseResponseMiddleware.count >= 10:
            content = response.content.decode()
            new_content = reverse_russian_words(content)

            response.content = new_content.encode("utf-8")

            ReverseResponseMiddleware.count = 0

        return response


def reverse_russian_words(sentence):

    def reverse_word(word):
        return word[::-1]

    russian_words_pattern = r"\b[а-яА-ЯёЁ]+\b"

    reversed_sentence = re.sub(
        russian_words_pattern,
        lambda match: reverse_word(match.group()),
        sentence,
    )

    return reversed_sentence
