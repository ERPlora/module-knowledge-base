from django.urls import path
from . import views

app_name = 'knowledge_base'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('articles/', views.articles, name='articles'),
    path('categories/', views.categories, name='categories'),
    path('settings/', views.settings, name='settings'),
]
