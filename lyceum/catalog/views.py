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
    queryset = catalog.models.Item.objects.published().only(
        catalog.models.Item.name.field.name,
        catalog.models.Item.text.field.name,
        catalog.models.Item.category.field.name,
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список товаров"
        return context


class ItemDetailView(
    django.views.generic.edit.FormMixin,
    django.views.generic.DetailView,
):
    form_class = rating.forms.RatingForm
    template_name = "catalog/item.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.item_detail_published()

    def get_object(self, queryset=None):
        self.item = super().get_object(queryset)
        self.ratings = rating.models.Rating.objects.filter(item=self.item)
        if self.request.user.is_authenticated:
            self.user_rating = self.ratings.filter(
                user=self.request.user,
            ).first()
        else:
            self.user_rating = None

        return self.item

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            self.ratings = rating.models.Rating.objects.filter(
                item=self.get_object(self.queryset),
            )
            self.user_rating = self.ratings.filter(
                user=self.request.user,
            ).first()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_stats = self.ratings.aggregate(
            Avg(rating.models.Rating.score.field.name),
            Count(rating.models.Rating.score.field.name),
        )
        user_rating = self.user_rating

        context["average_rating"] = rating_stats["score__avg"]
        context["rating_count"] = rating_stats["score__count"]
        context["user_rating"] = user_rating
        context["title"] = self.item
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_rating = self.user_rating
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self):

        return django.shortcuts.reverse(
            "catalog:item-detail",
            kwargs={"pk": self.item.id},
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
            "catalog:item-detail",
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
            F(catalog.models.Item.updated_at.field.name)
            - F(catalog.models.Item.created_at.field.name),
            output_field=DurationField(),
        ),
    ).filter(time_difference__lte=datetime.timedelta(seconds=1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Непроверенное"
        return context


__all__ = ()
