from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipesViewSet, TagViewSet

app_name = 'recipes'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path(r'', include(router.urls)),
]
