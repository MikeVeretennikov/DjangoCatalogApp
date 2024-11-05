import django.forms


class EchoForm(django.forms.Form):
    text = django.forms.CharField(
        widget=django.forms.Textarea,
        label="Ваш текст",
    )


__all__ = []
