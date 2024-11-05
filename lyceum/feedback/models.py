import django.db.models


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(max_length=150, blank=True, null=True)
    text = django.db.models.TextField(max_length=3000)
    created_on = django.db.models.DateTimeField(auto_now_add=True, null=True)
    mail = django.db.models.EmailField(max_length=254)

    class Meta:
        verbose_name = "обратная связь"
        verbose_name = "обратная связь"


__all__ = []
