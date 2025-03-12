"""
Views for the recipe APIs.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
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
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # need to add user
        serializer.save(user=self.request.user)


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


class TagViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Manage tags in the database"""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve tags for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")
