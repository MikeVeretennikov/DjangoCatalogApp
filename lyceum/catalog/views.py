import datetime

from django.db.models import (
    Avg,
    Count,
    DurationField,
    ExpressionWrapper,
    F,
)
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.views.generic
import django.views.generic.edit


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


class ItemDetailView(
    django.views.generic.edit.FormMixin,
    django.views.generic.DetailView,
):
    model = catalog.models.Item
    form_class = rating.forms.RatingForm
    template_name = "catalog/item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = rating.models.Rating.objects.filter(item=self.object)
        rating_stats = ratings.aggregate(Avg("score"), Count("score"))
        user_rating = ratings.filter(user=self.request.user).first()

        context["average_rating"] = rating_stats["score__avg"]
        context["rating_count"] = rating_stats["score__count"]
        context["user_rating"] = user_rating
        context["title"] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_rating = rating.models.Rating.objects.filter(
            item=self.get_object(self.queryset),
            user=self.request.user,
        ).first()
        if user_rating:
            kwargs["initial"]["score"] = user_rating.score
        else:
            kwargs["initial"]["score"] = 0

        return kwargs

    def form_valid(self, form):
        score = form.cleaned_data["score"]
        rating.models.Rating.objects.update_or_create(
            user=self.request.user,
            item=self.item,
            defaults={"score": score},
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            item = self.get_object(self.queryset)
            return django.shortcuts.render(
                request,
                "catalog/item.html",
                {"item": item, "title": item.name},
            )

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.item = self.get_object(self.queryset)
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self):
        return django.shortcuts.reverse(
            "catalog:default-converter-page",
            kwargs={"pk": self.item.pk},
        )


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
