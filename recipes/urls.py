from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('addrecipe/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/update/', views.update_recipe, name='update_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/', views.show_recipe, name='recipe'),
    path('category/<int:cat_id>', views.show_category, name='category'),
]
