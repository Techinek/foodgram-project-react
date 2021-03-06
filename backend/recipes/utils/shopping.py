from django.db.models import F, Sum

from recipes.models import RecipeIngredient


def get_shopping_list(user):
    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_recipe__user=user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')
    ).annotate(total=Sum('amount')).values_list(
        'ingredient__name', 'total', 'ingredient__measurement_unit')
    return ingredients
