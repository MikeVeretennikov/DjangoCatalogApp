import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts


import feedback.forms
import feedback.models


class FeedbackView(django.views.generic.edit.View):
    def get(self, request):
        feedback_author = feedback.forms.FeedbackAuthorForm(
            request.POST or None)
        feedback_form = feedback.forms.FeedbackForm(request.POST or None)
        files_form = feedback.forms.FeedbackFileForm(request.POST or None)

        context = {
            "feedback_form": feedback_form,
            "feedback_author": feedback_author,
            "files_form": files_form,
        }

        return django.shortcuts.render(request,
                                       "feedback/feedback.html",
                                       context)

    def post(self, request):
        feedback_author = feedback.forms.FeedbackAuthorForm(
            request.POST or None)
        feedback_form = feedback.forms.FeedbackForm(request.POST or None)
        files_form = feedback.forms.FeedbackFileForm(request.POST or None)

        forms = (
            feedback_author,
            feedback_form,
            files_form,
        )

        if all(form.is_valid() for form in forms):
            name = feedback_author.cleaned_data["name"]
            text = feedback_form.cleaned_data["text"]
            mail = feedback_author.cleaned_data["mail"]

            django.core.mail.send_mail(
                name,
                text,
                django.conf.settings.MAIL,
                [mail],
                fail_silently=False,
            )

            feedback_item = feedback_form.save()

            author = feedback_author.save(commit=False)
            author.feedback = feedback_item
            author.save()

            for file in request.FILES.getlist(
                "file",
            ):

                feedback_file = feedback.models.FeedbackFile(
                    file=file,
                    feedback=feedback_item,
                )
                feedback_file.save()

            django.contrib.messages.success(request, "Все прошло успешно")

            return django.shortcuts.redirect("feedback:feedback")

        context = {
            "feedback_form": feedback_form,
            "feedback_author": feedback_author,
            "files_form": files_form,
        }

        return django.shortcuts.render(request,
                                       "feedback/feedback.html",
                                       context)


__all__ = ()
