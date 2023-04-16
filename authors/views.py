import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

from recipes.models import Recipe
from utils.pagination import make_pagination

from .forms import LoginForm, RecipeForm, RegisterForm

ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 12))
QTY_PAGES_IN_PAGINATION = int(os.environ.get("QTY_PAGES_IN_PAGINATION", 5))


def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)

    return render(
        request,
        "authors/pages/register_view.html",
        context={
            "page_title": "Register",
            "form": form,
            "form_action": reverse("authors:register_create"),
        },
    )


def register_create(request):
    if not request.POST:
        raise Http404()

    request.session["register_form_data"] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        del request.session["register_form_data"]

        messages.success(request, "User created successfully")
        return redirect("authors:login")

    return redirect("authors:register")


def login_view(request):
    form = LoginForm()
    return render(
        request,
        "authors/pages/login.html",
        context={
            "page_title": "Login",
            "form": form,
            "form_action": reverse("authors:login_create"),
        },
    )


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )

        if authenticated_user is not None:
            messages.success(request, "Successfully logged in")
            login(request, user=authenticated_user)
            return redirect("recipes:home")

        else:
            messages.error(request, "Invalid username or password")

    else:
        messages.error(request, "Invalid credentials")

    return redirect("authors:login")


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if not request.POST:
        raise Http404()

    if request.POST.get("username") != request.user.username:
        raise Http404()

    logout(request)
    messages.success(request, "Successfully logged out")

    return redirect("authors:login")


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    )

    pages_obj, pagination_range = make_pagination(
        request=request,
        object_list=recipes,
        per_page=ITEMS_PER_PAGE,
        qty_pages=QTY_PAGES_IN_PAGINATION,
    )
    user = request.user.username

    return render(
        request,
        "authors/pages/dashboard.html",
        context={
            "pagination_range": pagination_range,
            "recipes": pages_obj,
            "is_recipe_list": True,
            "page_title": f"Dashboard - {user}",
        },
    )


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        id=id, is_published=False, author=request.user
    ).first()

    if not recipe:
        raise Http404()

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()

        messages.success(request, "Recipe update successfully")
        return redirect("authors:dashboard_recipe_edit", id)

    return render(
        request,
        "authors/pages/dashboard_recipe.html",
        context={
            "page_title": "Recipe edit",
            "form": form,
        },
    )


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_create(request):
    register_recipe_data = request.session.get("register_recipe_data", None)
    # register_recipe_files = request.session.get("register_recipe_files", None)# noqa: 501

    form = RecipeForm(
        register_recipe_data,
        files=request.FILES or None,
    )

    return render(
        request,
        "authors/pages/dashboard_recipe.html",
        context={
            "page_title": "Recipe create",
            "form": form,
            "form_action": reverse("authors:recipe_create"),
        },
    )


@login_required(login_url="authors:login", redirect_field_name="next")
def recipe_create(request):
    if not request.POST:
        raise Http404()

    request.session["register_recipe_data"] = request.POST
    # request.session["register_recipe_files"] = request.FILES
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = slugify(recipe.title)
        recipe.save()

        del request.session["register_recipe_data"]

        messages.success(request, "Recipe create successfully")
        return redirect("authors:dashboard")

    return redirect("authors:dashboard_recipe_create")
