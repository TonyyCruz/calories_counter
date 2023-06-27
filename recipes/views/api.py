from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


@api_view(http_method_names=["get", "post"])
def recipe_api_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
        )


@api_view()
def recipe_api_details(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk,
    )
    serializer = RecipeSerializer(
        instance=recipe,
        many=False,
        context={
            "request": request,
        },
    )
    return Response(serializer.data)

    # HTTP RESPONSE PERSONALIZADO:
    # recipe = Recipe.objects.get_published(pk=pk)

    # if not recipe:
    #     return Response(
    #         {"detail": "Recipe not found."},
    #         status=status.HTTP_404_NOT_FOUND,
    #     )

    # serializer = RecipeSerializer(instance=recipe, many=False)
    # return Response(serializer.data)


@api_view()
def recipe_api_tag(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
