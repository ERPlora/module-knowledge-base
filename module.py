    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'knowledge_base'
    MODULE_NAME = _('Knowledge Base & Wiki')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'library-outline'
    MODULE_DESCRIPTION = _('Internal wiki, articles and knowledge management')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'documents'

    MENU = {
        'label': _('Knowledge Base & Wiki'),
        'icon': 'library-outline',
        'order': 71,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Articles'), 'icon': 'library-outline', 'id': 'articles'},
{'label': _('Categories'), 'icon': 'folder-outline', 'id': 'categories'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'knowledge_base.view_kbarticle',
'knowledge_base.add_kbarticle',
'knowledge_base.change_kbarticle',
'knowledge_base.delete_kbarticle',
'knowledge_base.manage_settings',
    ]
