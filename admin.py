from django.contrib import admin

from .models import KBCategory, KBArticle

@admin.register(KBCategory)
class KBCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'order', 'is_active']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(KBArticle)
class KBArticleAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'slug', 'content', 'is_published']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

