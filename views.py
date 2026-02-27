"""
Knowledge Base & Wiki Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import KBCategory, KBArticle

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('knowledge_base', 'dashboard')
@htmx_view('knowledge_base/pages/index.html', 'knowledge_base/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_kb_categories': KBCategory.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_kb_articles': KBArticle.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# KBCategory
# ======================================================================

KB_CATEGORY_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'order': 'order',
    'slug': 'slug',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_kb_categories_context(hub_id, per_page=10):
    qs = KBCategory.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'kb_categories': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_kb_categories_list(request, hub_id, per_page=10):
    ctx = _build_kb_categories_context(hub_id, per_page)
    return django_render(request, 'knowledge_base/partials/kb_categories_list.html', ctx)

@login_required
@with_module_nav('knowledge_base', 'articles')
@htmx_view('knowledge_base/pages/kb_categories.html', 'knowledge_base/partials/kb_categories_content.html')
def kb_categories_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = KBCategory.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(slug__icontains=search_query) | Q(description__icontains=search_query))

    order_by = KB_CATEGORY_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'order', 'slug', 'description']
        headers = ['Name', 'Is Active', 'Order', 'Slug', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='kb_categories.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='kb_categories.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'knowledge_base/partials/kb_categories_list.html', {
            'kb_categories': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'kb_categories': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def kb_category_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = request.POST.get('is_active') == 'on'
        obj = KBCategory(hub_id=hub_id)
        obj.name = name
        obj.slug = slug
        obj.description = description
        obj.order = order
        obj.is_active = is_active
        obj.save()
        return _render_kb_categories_list(request, hub_id)
    return django_render(request, 'knowledge_base/partials/panel_kb_category_add.html', {})

@login_required
def kb_category_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(KBCategory, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.slug = request.POST.get('slug', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.order = int(request.POST.get('order', 0) or 0)
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_kb_categories_list(request, hub_id)
    return django_render(request, 'knowledge_base/partials/panel_kb_category_edit.html', {'obj': obj})

@login_required
@require_POST
def kb_category_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(KBCategory, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_kb_categories_list(request, hub_id)

@login_required
@require_POST
def kb_category_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(KBCategory, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_kb_categories_list(request, hub_id)

@login_required
@require_POST
def kb_categories_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = KBCategory.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_kb_categories_list(request, hub_id)


# ======================================================================
# KBArticle
# ======================================================================

KB_ARTICLE_SORT_FIELDS = {
    'title': 'title',
    'category': 'category',
    'is_published': 'is_published',
    'view_count': 'view_count',
    'slug': 'slug',
    'content': 'content',
    'created_at': 'created_at',
}

def _build_kb_articles_context(hub_id, per_page=10):
    qs = KBArticle.objects.filter(hub_id=hub_id, is_deleted=False).order_by('title')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'kb_articles': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'title',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_kb_articles_list(request, hub_id, per_page=10):
    ctx = _build_kb_articles_context(hub_id, per_page)
    return django_render(request, 'knowledge_base/partials/kb_articles_list.html', ctx)

@login_required
@with_module_nav('knowledge_base', 'articles')
@htmx_view('knowledge_base/pages/kb_articles.html', 'knowledge_base/partials/kb_articles_content.html')
def kb_articles_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'title')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = KBArticle.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(title__icontains=search_query) | Q(slug__icontains=search_query) | Q(content__icontains=search_query))

    order_by = KB_ARTICLE_SORT_FIELDS.get(sort_field, 'title')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['title', 'category', 'is_published', 'view_count', 'slug', 'content']
        headers = ['Title', 'KBCategory', 'Is Published', 'View Count', 'Slug', 'Content']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='kb_articles.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='kb_articles.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'knowledge_base/partials/kb_articles_list.html', {
            'kb_articles': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'kb_articles': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def kb_article_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        slug = request.POST.get('slug', '').strip()
        content = request.POST.get('content', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        view_count = int(request.POST.get('view_count', 0) or 0)
        obj = KBArticle(hub_id=hub_id)
        obj.title = title
        obj.slug = slug
        obj.content = content
        obj.is_published = is_published
        obj.view_count = view_count
        obj.save()
        return _render_kb_articles_list(request, hub_id)
    return django_render(request, 'knowledge_base/partials/panel_kb_article_add.html', {})

@login_required
def kb_article_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(KBArticle, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.slug = request.POST.get('slug', '').strip()
        obj.content = request.POST.get('content', '').strip()
        obj.is_published = request.POST.get('is_published') == 'on'
        obj.view_count = int(request.POST.get('view_count', 0) or 0)
        obj.save()
        return _render_kb_articles_list(request, hub_id)
    return django_render(request, 'knowledge_base/partials/panel_kb_article_edit.html', {'obj': obj})

@login_required
@require_POST
def kb_article_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(KBArticle, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_kb_articles_list(request, hub_id)

@login_required
@require_POST
def kb_articles_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = KBArticle.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_kb_articles_list(request, hub_id)


@login_required
@permission_required('knowledge_base.manage_settings')
@with_module_nav('knowledge_base', 'settings')
@htmx_view('knowledge_base/pages/settings.html', 'knowledge_base/partials/settings_content.html')
def settings_view(request):
    return {}

