from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class KBCategory(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.SlugField(max_length=100, verbose_name=_('Slug'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'knowledge_base_kbcategory'

    def __str__(self):
        return self.name


class KBArticle(HubBaseModel):
    category = models.ForeignKey('KBCategory', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'))
    content = models.TextField(verbose_name=_('Content'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is Published'))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_('View Count'))

    class Meta(HubBaseModel.Meta):
        db_table = 'knowledge_base_kbarticle'

    def __str__(self):
        return self.title

