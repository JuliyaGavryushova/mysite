from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewRecipeForm
from .models import Recipe, RecipeCategory, Category

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Добавить рецепт', 'url_name': 'add_recipe'},
]


def index(request):
    recipes = Recipe.objects.all().order_by('?')[:5]
    categorys = Category.objects.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'recipes': recipes,
        'categorys': categorys,
    }
    return render(request, 'recipes/index.html', context=data)


def show_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    data = {
        'title': recipe.title,
        'menu': menu,
        'recipe': recipe,
    }
    return render(request, 'recipes/recipe.html', context=data)


def show_category(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
    cat_all = Category.objects.all()
    recipes_cat = RecipeCategory.objects.filter(category_id=cat_id)
    recipes = [recipe_cat.recipe for recipe_cat in recipes_cat]
    data = {
        'title': category.name,
        'menu': menu,
        'categorys': cat_all,
        'recipes': recipes,
        'cat': recipes_cat
    }
    return render(request, 'recipes/index.html', context=data)


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = NewRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            cooking_steps = form.cleaned_data['cooking_steps']
            cooking_time = form.cleaned_data['cooking_time']
            photo = form.cleaned_data['photo']
            category = form.cleaned_data['category']
            recipe = Recipe(title=title, description=description, cooking_steps=cooking_steps, cooking_time=cooking_time, photo=photo)
            recipe.author = request.user
            recipe.save()
            cat_recipe = RecipeCategory(recipe=recipe, category=category)
            cat_recipe.save()
            return redirect('home')
    else:
        form = NewRecipeForm()
    data = {
        'title': 'Добавление рецепта',
        'menu': menu,
        'form': form
    }
    return render(request, 'recipes/addrecipe.html', context=data)


@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user:
        data = {
            'title': 'Изменение рецепта',
            'menu': menu,
        }
        return render(request, 'recipes/update_del_error.html', context=data, status=403)
    cat_recipe = get_object_or_404(RecipeCategory, recipe=recipe)
    category = RecipeCategory.objects.filter(recipe=recipe).first().category
    if request.method == 'POST':
        form = NewRecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            category = form.cleaned_data['category']
            form.save()
            cat_recipe.category = category
            cat_recipe.save()
            return redirect('home')
    else:
        form = NewRecipeForm(instance=recipe, initial={'category': category})
    data = {
            'title': 'Изменение рецепта',
            'menu': menu,
            'form': form,
            'recipe': recipe,
    }
    return render(request, 'recipes/update_recipe.html', context=data)


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user:
        data = {
            'title': 'Изменение рецепта',
            'menu': menu,
        }
        return render(request, 'recipes/update_del_error.html', context=data, status=403)
    if request.method == 'POST':
        recipe.delete()
    return redirect('home')


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')