import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.Feedback
        fields = ("name", "text", "mail")

        labels = {
            "name": "Имя",
            "text": "Текст",
            "mail": "Почта",
        }

        help_texts = {
            "name": "Ваше имя",
            "text": "Введите текст обращения",
            "mail": "Введите вашу почту",
        }


__all__ = []
