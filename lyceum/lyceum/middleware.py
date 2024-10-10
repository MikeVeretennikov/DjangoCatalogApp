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
            content = response.content.decode().split("<body>", 1)[1]
            content = content.split("</body>")[0]
            new_content = reverse_all_russian_words(content)
            response.content = "<body>" + new_content + "</body>"

            ReverseResponseMiddleware.count = 0

        return response


def reverse_all_russian_words(str):
    words = str.split()
    new_words = []
    for word in words:
        new_words.append(word[::-1])

    return " ".join(new_words)
