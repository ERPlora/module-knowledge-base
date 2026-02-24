"""Tests for knowledge_base views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('knowledge_base:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('knowledge_base:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('knowledge_base:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestKBCategoryViews:
    """KBCategory view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('knowledge_base:kb_categories_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('knowledge_base:kb_categories_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('knowledge_base:kb_categories_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('knowledge_base:kb_categories_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('knowledge_base:kb_categories_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('knowledge_base:kb_categories_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('knowledge_base:kb_category_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('knowledge_base:kb_category_add')
        data = {
            'name': 'New Name',
            'slug': 'New Slug',
            'description': 'Test description',
            'order': '5',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, kb_category):
        """Test edit form loads."""
        url = reverse('knowledge_base:kb_category_edit', args=[kb_category.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, kb_category):
        """Test editing via POST."""
        url = reverse('knowledge_base:kb_category_edit', args=[kb_category.pk])
        data = {
            'name': 'Updated Name',
            'slug': 'Updated Slug',
            'description': 'Test description',
            'order': '5',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, kb_category):
        """Test soft delete via POST."""
        url = reverse('knowledge_base:kb_category_delete', args=[kb_category.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        kb_category.refresh_from_db()
        assert kb_category.is_deleted is True

    def test_toggle_status(self, auth_client, kb_category):
        """Test toggle active status."""
        url = reverse('knowledge_base:kb_category_toggle_status', args=[kb_category.pk])
        original = kb_category.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        kb_category.refresh_from_db()
        assert kb_category.is_active != original

    def test_bulk_delete(self, auth_client, kb_category):
        """Test bulk delete."""
        url = reverse('knowledge_base:kb_categories_bulk_action')
        response = auth_client.post(url, {'ids': str(kb_category.pk), 'action': 'delete'})
        assert response.status_code == 200
        kb_category.refresh_from_db()
        assert kb_category.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('knowledge_base:kb_categories_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestKBArticleViews:
    """KBArticle view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('knowledge_base:kb_articles_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('knowledge_base:kb_articles_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('knowledge_base:kb_articles_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('knowledge_base:kb_articles_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('knowledge_base:kb_articles_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('knowledge_base:kb_articles_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('knowledge_base:kb_article_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('knowledge_base:kb_article_add')
        data = {
            'title': 'New Title',
            'slug': 'New Slug',
            'content': 'Test description',
            'is_published': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, kb_article):
        """Test edit form loads."""
        url = reverse('knowledge_base:kb_article_edit', args=[kb_article.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, kb_article):
        """Test editing via POST."""
        url = reverse('knowledge_base:kb_article_edit', args=[kb_article.pk])
        data = {
            'title': 'Updated Title',
            'slug': 'Updated Slug',
            'content': 'Test description',
            'is_published': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, kb_article):
        """Test soft delete via POST."""
        url = reverse('knowledge_base:kb_article_delete', args=[kb_article.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        kb_article.refresh_from_db()
        assert kb_article.is_deleted is True

    def test_bulk_delete(self, auth_client, kb_article):
        """Test bulk delete."""
        url = reverse('knowledge_base:kb_articles_bulk_action')
        response = auth_client.post(url, {'ids': str(kb_article.pk), 'action': 'delete'})
        assert response.status_code == 200
        kb_article.refresh_from_db()
        assert kb_article.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('knowledge_base:kb_articles_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('knowledge_base:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('knowledge_base:settings')
        response = client.get(url)
        assert response.status_code == 302

