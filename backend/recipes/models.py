from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .validator_fields.hex_code import HexColorField

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='name', max_length=40, unique=True)
    color = HexColorField(verbose_name='color in hex', unique=True,
                          null=True)
    slug = models.SlugField(verbose_name='relative url', unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    measurement_unit = models.CharField(verbose_name='unit', max_length=50)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [models.UniqueConstraint(fields=('name',
                                                       'measurement_unit'),
                                               name='pair_unique')]
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    name = models.CharField(verbose_name='name', max_length=200, unique=True)
    author = models.ForeignKey(User, verbose_name='author',
                               on_delete=models.CASCADE,
                               related_name='recipes')
    text = models.TextField(verbose_name='recipe description')
    tags = models.ManyToManyField(Tag, verbose_name='tags',
                                  related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='ingredients',
                                         through='RecipeIngredient')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='recipe photo')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='cooking time',
        validators=[MinValueValidator(1, message='Time cannot be none!')])

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='recipe',
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredient, verbose_name='ingredient',
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_recipe')
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, message='Should be at least 1!')],
        verbose_name='amount of ingredient')

    class Meta:
        verbose_name = 'Recipe ingredient'
        verbose_name_plural = 'Recipe ingredients'
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'ingredient'),
                                    name='recipe_ingredient_exists'),
            models.CheckConstraint(check=models.Q(amount__gte=1),
                                   name='amount_gte_1')]

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='recipe',
                               on_delete=models.CASCADE,
                               related_name='in_favorite')
    user = models.ForeignKey(User, verbose_name='user',
                             on_delete=models.CASCADE,
                             related_name='favorite')

    class Meta:
        verbose_name = 'Favourite recipe'
        verbose_name_plural = 'Favourite recipes'
        constraints = [models.UniqueConstraint(fields=('recipe', 'user'),
                                               name='unique_favorite')]
        ordering = ('-id',)

    def __str__(self):
        return f'Recipe {self.recipe} is added to favorites by {self.user}'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='recipe',
                               on_delete=models.CASCADE,
                               related_name='shopping_recipe')
    user = models.ForeignKey(User, verbose_name='user',
                             on_delete=models.CASCADE,
                             related_name='shopping_user')

    class Meta:
        verbose_name = 'Shopping list'
        verbose_name_plural = 'Shopping lists'
        constraints = [models.UniqueConstraint(fields=('recipe', 'user'),
                                               name='shopping_recipe_exists')]
        ordering = ('-id',)

    def __str__(self):
        return f'Recipe {self.recipe} is added by {self.user}'
