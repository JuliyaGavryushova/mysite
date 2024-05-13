from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание')
    cooking_steps = models.TextField(verbose_name='Шаги приготовления')
    cooking_time = models.CharField(max_length=50, verbose_name='Время приготовления')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='recipes', null=True, default=None)
    photo = models.ImageField(upload_to='uploads', default=None, null=True, blank=True, verbose_name='Фото блюда')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Recipe: {self.title}'


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return f'{self.name}'


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['recipe', 'category']
