from django.urls import path
from . import views

app_name = 'knowledge_base'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # KBCategory
    path('kb_categories/', views.kb_categories_list, name='kb_categories_list'),
    path('kb_categories/add/', views.kb_category_add, name='kb_category_add'),
    path('kb_categories/<uuid:pk>/edit/', views.kb_category_edit, name='kb_category_edit'),
    path('kb_categories/<uuid:pk>/delete/', views.kb_category_delete, name='kb_category_delete'),
    path('kb_categories/<uuid:pk>/toggle/', views.kb_category_toggle_status, name='kb_category_toggle_status'),
    path('kb_categories/bulk/', views.kb_categories_bulk_action, name='kb_categories_bulk_action'),

    # KBArticle
    path('kb_articles/', views.kb_articles_list, name='kb_articles_list'),
    path('kb_articles/add/', views.kb_article_add, name='kb_article_add'),
    path('kb_articles/<uuid:pk>/edit/', views.kb_article_edit, name='kb_article_edit'),
    path('kb_articles/<uuid:pk>/delete/', views.kb_article_delete, name='kb_article_delete'),
    path('kb_articles/bulk/', views.kb_articles_bulk_action, name='kb_articles_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
