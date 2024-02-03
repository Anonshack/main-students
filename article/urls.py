from django.urls import path
from.views import art, edit, delete, create, detail

app_name = 'articles'

urlpatterns = [
    path('', art, name='list'),
    path('detail/<slug:slug>/', detail, name='detail'),
    path('delete/<slug:slug>/', delete, name='delete'),
    path('create/', create, name='create'),
    path('edit/<slug:slug>/', edit, name='edit'),
]