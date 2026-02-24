from django.contrib import admin

from .models import KBCategory, KBArticle

@admin.register(KBCategory)
class KBCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(KBArticle)
class KBArticleAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'slug', 'is_published', 'created_at']
    search_fields = ['title', 'slug', 'content']
    readonly_fields = ['created_at', 'updated_at']

