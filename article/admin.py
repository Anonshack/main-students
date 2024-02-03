from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_deleted', 'modified_date', 'created_date']
    readonly_fields = ['modified_date', 'created_date']
    fields = ['title', 'image', 'content', 'slug', 'modified_date', 'created_date']
    list_display_links = ('title', 'id')
    list_per_page = 10
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('-id',)
    search_fields = ('title',)
    search_help_text = 'Search through title'
    list_filter = ('is_deleted', 'created_date', 'modified_date')
    date_hierarchy = 'created_date'


admin.site.register(Article, ArticleAdmin)