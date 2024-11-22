from datetime import timedelta

from django.utils import timezone

from users.models import User

__all__ = ()


def birthday_context_processor(request):
    user_offset = request.COOKIES.get("user_offset")

    current_time_utc = timezone.now()
    if user_offset:
        try:
            hours_offset = float(user_offset)
            user_time = current_time_utc + timedelta(hours=hours_offset)
        except ValueError:
            user_time = current_time_utc
    else:
        user_time = current_time_utc

    current_date = user_time.date()
    birthday_people = (
        User.objects.filter(
            profile__birthday__day=current_date.day,
            profile__birthday__month=current_date.month,
        )
        .select_related("profile")
        .only(
            "email",
            "first_name",
            "profile__birthday",
        )
    )
    return {
        "birthday_people": birthday_people,
    }
