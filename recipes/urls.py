from django.urls import path
from .views import recipe_list, recipe_detail, recipe_update, recipe_create, recipe_delete, my_recipes
from .views import tag_list, tag_detail, tag_update, tag_delete, tag_create
from .views import ing_create, ing_update, ing_delete

app_name = 'recipes'

urlpatterns = [
    path('', recipe_list, name='list'),
    path('my/recipes/', my_recipes, name='my_list'),
    path('detail/<slug:slug>/', recipe_detail, name='detail'),
    path('update/<slug:slug>/', recipe_update, name='update'),
    path('create/', recipe_create, name='create'),
    path('delete/<slug:slug>', recipe_delete, name='delete'),

    path('tag/', tag_list, name='tag_list'),
    path('tag/detail/<int:pk>/', tag_detail, name='tag_detail'),
    path('tag/update/<int:pk>/', tag_update, name='tag_update'),
    path('tag/delete/<int:pk>/', tag_delete, name='tag_delete'),
    path('tag/create/', tag_create, name='tag_create'),

    path('detail/<slug:recipe_slug>/create/', ing_create, name='ing_create'),
    path('detail/<slug:recipe_slug>/update/<int:pk>/', ing_update, name='ing_update'),
    path('detail/<slug:recipe_slug>/delete/<int:pk>/', ing_delete, name='ing_delete'),
]