"""
Knowledge Base & Wiki Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('knowledge_base', 'dashboard')
@htmx_view('knowledge_base/pages/dashboard.html', 'knowledge_base/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('knowledge_base', 'articles')
@htmx_view('knowledge_base/pages/articles.html', 'knowledge_base/partials/articles_content.html')
def articles(request):
    """Articles view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('knowledge_base', 'categories')
@htmx_view('knowledge_base/pages/categories.html', 'knowledge_base/partials/categories_content.html')
def categories(request):
    """Categories view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('knowledge_base', 'settings')
@htmx_view('knowledge_base/pages/settings.html', 'knowledge_base/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

