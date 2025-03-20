"""
Views for the recipe APIs.
"""

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""

    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return serializer class based on action"""
        if self.action == "list":
            return serializers.RecipeSerializer
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # need to add user
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# My implementation
# class TagViewSet(viewsets.ModelViewSet):
#     """View for manage tag APIs"""
#
#     serializer_class = serializers.TagSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     # disable creating
#     http_method_names = ["get", "patch", "put", "delete"]
#
#     def get_queryset(self):
#         """Retrieve recipes for authenticated user"""
#         return self.queryset.filter(user=self.request.user).order_by("-name")
#
#     def perform_create(self, serializer):
#         """Create a new tag"""
#         serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve attributes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
