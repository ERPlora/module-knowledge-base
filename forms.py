from django import forms
from django.utils.translation import gettext_lazy as _

from .models import KBCategory, KBArticle

class KBCategoryForm(forms.ModelForm):
    class Meta:
        model = KBCategory
        fields = ['name', 'slug', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'slug': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'order': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class KBArticleForm(forms.ModelForm):
    class Meta:
        model = KBArticle
        fields = ['category', 'title', 'slug', 'content', 'is_published', 'view_count']
        widgets = {
            'category': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'title': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'slug': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'content': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_published': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'view_count': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

