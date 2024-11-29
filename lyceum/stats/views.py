from django.contrib.auth import mixins
from django.db.models import Avg, Prefetch
from django.shortcuts import get_object_or_404, render
from django.views import generic



import catalog.models
import rating.models


class UserDetailView(generic.TemplateView):
    template_name = "stats/user_stats.html"

    def get(self, request, pk):
        context = {}
        user_ratings = rating.models.Rating.objects.filter(user_id=pk)

        if user_ratings:
            context["avg_rating"] = user_ratings.aggregate(Avg("score"))[
                "score__avg"
            ]
            context["rating_count"] = user_ratings.count()
            context["max_rating_user"] = user_ratings.order_by(
                "-score",
                "-created_at",
            ).first()
            context["min_rating_user"] = user_ratings.order_by(
                "score",
                "-created_at",
            ).first()
        else:
            context["avg_rating"] = 0
            context["rating_count"] = 0
            context["max_rating_user"] = context["min_rating_user"] = None

        return render(request, "stats/user_stats.html", context)


class ItemDetailView(generic.TemplateView):
    template_name = "stats/item_stats.html"

    def get(self, request, pk):
        context = {}
        item_ratings = rating.models.Rating.objects.filter(item_id=pk)

        item = get_object_or_404(catalog.models.Item, id=pk)
        context["item"] = item

        if item_ratings:
            context["avg_rating"] = item_ratings.aggregate(Avg("score"))[
                "score__avg"
            ]
            context["rating_count"] = item_ratings.count()
            context["max_rating_user"] = (
                item_ratings.order_by("-score", "-created_at").first().user
            )
            context["min_rating_user"] = (
                item_ratings.order_by("score", "-created_at").first().user
            )
        else:
            context["avg_rating"] = 0
            context["rating_count"] = 0
            context["max_rating_user"] = context["min_rating_user"] = None

        return render(request, "stats/item_stats.html", context)


class RatedItemsView(mixins.LoginRequiredMixin, generic.View):
    def get(self, request):
        context = {}
        items = catalog.models.Item.objects.published()
        prefetched_items = (
            items.prefetch_related(
                Prefetch(
                    "rating",
                    queryset=rating.models.Rating.objects.filter(
                        user=request.user,
                    ),
                ),
            )
            .filter(rating__user=request.user)
            .order_by("-rating__score")
        )

        context["items"] = prefetched_items

        return render(request, "stats/rated_items.html", context)


__all__ = ()
