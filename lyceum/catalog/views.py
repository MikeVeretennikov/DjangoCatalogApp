import datetime

from django.db.models import (
    Avg,
    DurationField,
    ExpressionWrapper,
    F,
)
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.views.generic


import catalog.managers
import catalog.models
import rating.forms
import rating.models


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список товаров"
        return context


class ItemDetailView(django.views.generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.published()

    def get(self, request, pk):

        item = django.shortcuts.get_object_or_404(catalog.models.Item, id=pk)

        ratings = rating.models.Rating.objects.filter(item=item)
        average_rating = ratings.aggregate(Avg("score"))["score__avg"] or 0
        rating_count = ratings.count()
        user_rating = None

        if request.user.is_authenticated:
            user_rating = ratings.filter(user=request.user).first()

        default_score = 5

        if user_rating:
            form = rating.forms.RatingForm({"score": user_rating.score})
        else:
            form = rating.forms.RatingForm({"score": default_score})

        context = {
            "item": item,
            "average_rating": average_rating,
            "rating_count": rating_count,
            "user_rating": user_rating,
            "form": form,
        }
        return django.shortcuts.render(request, "catalog/item.html", context)

    def post(self, request, pk):
        item = django.shortcuts.get_object_or_404(catalog.models.Item, id=pk)
        form = rating.forms.RatingForm(request.POST or None)

        if form.is_valid():
            score = form.cleaned_data["score"]
            rating.models.Rating.objects.update_or_create(
                user=request.user,
                item=item,
                defaults={"score": score},
            )
            return django.shortcuts.redirect(
                "catalog:default-converter-page",
                pk=pk,
            )

        # Если форма не валидна, возвращаем на страницу с ошибками
        ratings = rating.models.Rating.objects.filter(item=item)
        user_rating = ratings.filter(user=request.user).first()
        average_rating = ratings.aggregate(Avg("score"))["score__avg"] or 0
        rating_count = ratings.count()

        context = {
            "item": item,
            "average_rating": average_rating,
            "rating_count": rating_count,
            "user_rating": user_rating,
            "form": form,
        }
        return django.shortcuts.render(request, "catalog/item.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Товар детально"
        return context


class RatingDeleteView(django.views.generic.DeleteView):
    def post(self, request, pk):

        item = django.shortcuts.get_object_or_404(catalog.models.Item, id=pk)

        if request.user.is_authenticated and request.method == "POST":
            rating.models.Rating.objects.filter(
                item=item,
                user=request.user,
            ).delete()

        return django.shortcuts.redirect(
            "catalog:default-converter-page",
            pk=pk,
        )


class FridayItemDetailView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    item_published = catalog.models.Item.objects.published()
    queryset = item_published.filter(updated_at__week_day=6).order_by(
        "-updated_at",
    )[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пятница"
        return context


class NewItemListView(django.views.generic.ListView):
    template_name = "homepage/main.html"
    context_object_name = "items"
    week_ago = django.utils.timezone.now() - datetime.timedelta(weeks=1)
    item_published = catalog.models.Item.objects.published()
    queryset = item_published.filter(created_at__gte=week_ago).order_by("?")[
        :5
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новинки"
        return context


class UnverifiedItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    item_published = catalog.models.Item.objects.published()
    queryset = item_published.annotate(
        time_difference=ExpressionWrapper(
            F("updated_at") - F("created_at"),
            output_field=DurationField(),
        ),
    ).filter(time_difference__lte=datetime.timedelta(seconds=1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Непроверенное"
        return context


__all__ = ()
