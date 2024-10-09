from django.conf import settings


class ReverseResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        response = self.get_response(request)
        if settings.ALLOW_REVERSE:
            self.count += 1

        if self.count == 10:
            content = response.content.decode().split("<body>", 1)[1]
            content = content.split("</body>")[0]
            new_content = reverse_all_russian_words(content)
            response.content = "<body>" + new_content + "</body>"
            self.count = 0

        return response


def reverse_all_russian_words(str):
    words = str.split()
    new_words = []
    for word in words:
        new_words.append(word[::-1])

    return " ".join(new_words)
