"""Tests for knowledge_base models."""
import pytest
from django.utils import timezone

from knowledge_base.models import KBCategory, KBArticle


@pytest.mark.django_db
class TestKBCategory:
    """KBCategory model tests."""

    def test_create(self, kb_category):
        """Test KBCategory creation."""
        assert kb_category.pk is not None
        assert kb_category.is_deleted is False

    def test_str(self, kb_category):
        """Test string representation."""
        assert str(kb_category) is not None
        assert len(str(kb_category)) > 0

    def test_soft_delete(self, kb_category):
        """Test soft delete."""
        pk = kb_category.pk
        kb_category.is_deleted = True
        kb_category.deleted_at = timezone.now()
        kb_category.save()
        assert not KBCategory.objects.filter(pk=pk).exists()
        assert KBCategory.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, kb_category):
        """Test default queryset excludes deleted."""
        kb_category.is_deleted = True
        kb_category.deleted_at = timezone.now()
        kb_category.save()
        assert KBCategory.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, kb_category):
        """Test toggling is_active."""
        original = kb_category.is_active
        kb_category.is_active = not original
        kb_category.save()
        kb_category.refresh_from_db()
        assert kb_category.is_active != original


@pytest.mark.django_db
class TestKBArticle:
    """KBArticle model tests."""

    def test_create(self, kb_article):
        """Test KBArticle creation."""
        assert kb_article.pk is not None
        assert kb_article.is_deleted is False

    def test_str(self, kb_article):
        """Test string representation."""
        assert str(kb_article) is not None
        assert len(str(kb_article)) > 0

    def test_soft_delete(self, kb_article):
        """Test soft delete."""
        pk = kb_article.pk
        kb_article.is_deleted = True
        kb_article.deleted_at = timezone.now()
        kb_article.save()
        assert not KBArticle.objects.filter(pk=pk).exists()
        assert KBArticle.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, kb_article):
        """Test default queryset excludes deleted."""
        kb_article.is_deleted = True
        kb_article.deleted_at = timezone.now()
        kb_article.save()
        assert KBArticle.objects.filter(hub_id=hub_id).count() == 0


