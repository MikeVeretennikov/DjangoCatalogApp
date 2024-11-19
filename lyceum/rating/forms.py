from django import forms


class RatingForm(forms.Form):
    score = forms.ChoiceField(
        choices=[
            (1, "Ненависть"),
            (2, "Неприязнь"),
            (3, "Нейтрально"),
            (4, "Обожание"),
            (5, "Любовь"),
        ],
        label="Ваша оценка",
    )


__all__ = ()
