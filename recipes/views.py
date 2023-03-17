import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

from .models import Category, Recipe

ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 12))
QTY_PAGES_IN_PAGINATION = int(os.environ.get("QTY_PAGES_IN_PAGINATION", 5))


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by("-id")

    pages_obj, pagination_range = make_pagination(
        request=request,
        object_list=recipes,
        per_page=ITEMS_PER_PAGE,
        qty_pages=QTY_PAGES_IN_PAGINATION,
    )

    return render(
        request,
        "recipes/pages/home.html",
        context={
            "pagination_range": pagination_range,
            "recipes": pages_obj,
            "is_recipe_list": True,
            "page_title": "Recipes",
        })


def recipe_details(request, id):
    recipe = get_object_or_404(
        Recipe.objects.filter(
            id=id,
            is_published=True,
        ))
    return render(
        request,
        "recipes/pages/recipe_details.html",
        context={
            "recipe": recipe,
            "page_title": recipe.title,
        })


def category(request, id):
    category = get_object_or_404(Category, id=id)
    recipes = get_list_or_404(
        Recipe.objects.filter(
            is_published=True,
            category__id=id
        ).order_by("-id")
    )
    pages_obj, pagination_range = make_pagination(
        request,
        recipes,
        ITEMS_PER_PAGE,
        qty_pages=QTY_PAGES_IN_PAGINATION,
    )

    return render(
        request,
        "recipes/pages/category.html",
        context={
            "pagination_range": pagination_range,
            "recipes": pages_obj,
            "is_recipe_list": True,
            "page_title": category.name,
        })


def search(request):
    search_therm = request.GET.get("q", "").strip()
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_therm)
        | Q(description__icontains=search_therm),
        is_published=True,
    ).order_by("-id")

    if not search_therm:
        raise Http404()

    pages_obj, pagination_range = make_pagination(
        request,
        recipes,
        ITEMS_PER_PAGE,
        qty_pages=QTY_PAGES_IN_PAGINATION,
    )

    return render(
        request,
        "recipes/pages/search.html",
        context={
            "pagination_range": pagination_range,
            "recipes": pages_obj,
            "page_title": f'Search: "{search_therm}"',
            "is_recipe_list": True,
            "additional_url_query": f"&q={search_therm}",
        }
    )
