from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls', namespace="articles")),
    path('', include('blogs.urls', namespace="blogs")),
    path('account/', include('account.urls', namespace="account")),
    path('recipes/', include('recipes.urls', namespace="recipes")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)