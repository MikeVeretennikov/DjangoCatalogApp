import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts


from feedback.forms import FeedbackForm


def feedback(request):
    template = "feedback/feedback.html"
    form = FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        name = form.cleaned_data.get("name")
        text = form.cleaned_data.get("text")
        mail = form.cleaned_data.get("text")
        django.core.mail.send_mail(
            name,
            text,
            django.conf.settings.MAIL,
            [mail],
            fail_silently=False,
        )

        django.contrib.messages.success(request, "Все прошло успешно")
        return django.shortcuts.redirect("feedback:feedback")

    context = {"form": form, "title": "Обратная связь"}

    return django.shortcuts.render(request, template, context)


__all__ = []
