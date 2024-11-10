import django.forms

import feedback.models


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackAuthorForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False


    class Meta:
        model = feedback.models.FeedbackAuthor
        fields = (
            feedback.models.FeedbackAuthor.name.field.name,
            feedback.models.FeedbackAuthor.mail.field.name,
        )

        labels = {
            feedback.models.FeedbackAuthor.name.field.name: "Имя",
            feedback.models.FeedbackAuthor.mail.field.name: "Почта",
        }

        help_texts = {
            feedback.models.FeedbackAuthor.name.field.name: "Ваше имя",
            feedback.models.FeedbackAuthor.mail.field.name: (
                "Введите вашу почту"
            ),
        }


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class FeedbackFileForm(BootstrapForm):
    class Meta:
        model = feedback.models.FeedbackFile

        fields = (feedback.models.FeedbackFile.file.field.name,)

        labels = {
            feedback.models.FeedbackFile.file.field.name: "Файлы",
        }

        help_texts = {
            feedback.models.FeedbackFile.file.field.name: (
                "При необходимости прикрепите файлы"
            ),
        }

        widgets = {
            feedback.models.FeedbackFile.file.field.name: MultipleFileInput(),
        }


class FeedbackForm(BootstrapForm):
    class Meta:
        model = feedback.models.Feedback
        exclude = (
            feedback.models.Feedback.id.field.name,
            feedback.models.Feedback.created_on.field.name,
            feedback.models.Feedback.status.field.name,
        )

        labels = {
            feedback.models.Feedback.text.field.name: "Текст",
        }


__all__ = []
