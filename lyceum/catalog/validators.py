import re

import django.core.exceptions
import django.utils.deconstruct


def validate_perfect_in_text(text):
    if not (
        re.match(
            r".*\b(роскошно|превосходно)\b.*",
            text,
            re.IGNORECASE,
        )
    ):
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть слово 'превосходно' или 'роскошно'",
        )


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.args = args

    def __call__(self, text):
        pattern = r".*\b(" + "|".join(self.args) + r")\b.*"
        if not (
            re.match(
                pattern,
                text,
                re.IGNORECASE,
            )
        ):
            raise django.core.exceptions.ValidationError(
                "В тексте должно быть слово 'превосходно' или 'роскошно'",
            )


def validate_int_from_1_to_32767(num):
    if not (0 < num <= 32767) or type(num) is not int:
        raise django.core.exceptions.ValidationError(
            "Число должно быть от 1 до 32767 включительно",
        )


__all__ = []
