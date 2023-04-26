import os

from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView

from utils.pagination import make_pagination

from .models import Recipe

ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 12))
QTY_PAGES_IN_PAGINATION = int(os.environ.get("QTY_PAGES_IN_PAGINATION", 5))


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = "recipes"
    ordering = ["-id"]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pages_obj, pagination_range = make_pagination(
            request=self.request,
            object_list=context.get("recipes"),
            per_page=ITEMS_PER_PAGE,
            qty_pages=QTY_PAGES_IN_PAGINATION,
        )

        context["is_recipe_list"] = True
        context["recipes"] = pages_obj
        context["pagination_range"] = pagination_range

        return context


class RecipeViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id=self.kwargs.get("id"))

        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = context.get("recipes")[0].category.name
        context["page_title"] = f"Category {category_name}"
        return context


class RecipeViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_therm = self.request.GET.get("q", "").strip()

        if not search_therm:
            raise Http404()

        qs = qs.filter(
            Q(title__icontains=search_therm)
            | Q(description__icontains=search_therm),
            is_published=True,
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_therm = self.request.GET.get("q", "").strip()
        context["search_therm"] = f"{search_therm}"
        context["additional_url_query"] = f"&q={search_therm}"
        return context


class RecipeViewDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe_details.html"
