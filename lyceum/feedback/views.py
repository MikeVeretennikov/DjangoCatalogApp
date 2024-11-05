import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts


from feedback.forms import FeedbackForm


def feedback(request):
    template = "feedback/feedback.html"
    form = FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"]
        text = form.cleaned_data["text"]
        mail = form.cleaned_data["mail"]

        django.core.mail.send_mail(
            name,
            text,
            django.conf.settings.MAIL,
            [mail],
            fail_silently=False,
        )
        form.save()

        django.contrib.messages.success(request, "Все прошло успешно")
        return django.shortcuts.redirect("feedback:feedback")

    context = {"form": form, "title": "Обратная связь"}

    return django.shortcuts.render(request, template, context)


__all__ = []
