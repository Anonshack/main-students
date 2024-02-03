from django.urls import path
from.views import bl

app_name = 'blogs'

urlpatterns = [
    path('', bl, name='list')
]