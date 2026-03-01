"""AI tools for the Knowledge Base module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListKBCategories(AssistantTool):
    name = "list_kb_categories"
    description = "List knowledge base categories."
    module_id = "knowledge_base"
    required_permission = "knowledge_base.view_kbcategory"
    parameters = {"type": "object", "properties": {"is_active": {"type": "boolean"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from knowledge_base.models import KBCategory
        qs = KBCategory.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {"categories": [{"id": str(c.id), "name": c.name, "slug": c.slug, "description": c.description, "is_active": c.is_active} for c in qs.order_by('order')]}


@register_tool
class ListKBArticles(AssistantTool):
    name = "list_kb_articles"
    description = "List knowledge base articles."
    module_id = "knowledge_base"
    required_permission = "knowledge_base.view_kbarticle"
    parameters = {
        "type": "object",
        "properties": {"category_id": {"type": "string"}, "is_published": {"type": "boolean"}, "search": {"type": "string"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from knowledge_base.models import KBArticle
        qs = KBArticle.objects.select_related('category').all()
        if args.get('category_id'):
            qs = qs.filter(category_id=args['category_id'])
        if 'is_published' in args:
            qs = qs.filter(is_published=args['is_published'])
        if args.get('search'):
            qs = qs.filter(title__icontains=args['search'])
        limit = args.get('limit', 20)
        return {"articles": [{"id": str(a.id), "title": a.title, "category": a.category.name if a.category else None, "is_published": a.is_published, "view_count": a.view_count} for a in qs[:limit]]}


@register_tool
class CreateKBCategory(AssistantTool):
    name = "create_kb_category"
    description = "Create a knowledge base category."
    module_id = "knowledge_base"
    required_permission = "knowledge_base.add_kbcategory"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "description": {"type": "string"}},
        "required": ["name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from knowledge_base.models import KBCategory
        from django.utils.text import slugify
        c = KBCategory.objects.create(name=args['name'], slug=slugify(args['name']), description=args.get('description', ''))
        return {"id": str(c.id), "name": c.name, "created": True}


@register_tool
class CreateKBArticle(AssistantTool):
    name = "create_kb_article"
    description = "Create a knowledge base article."
    module_id = "knowledge_base"
    required_permission = "knowledge_base.add_kbarticle"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "title": {"type": "string"}, "content": {"type": "string"},
            "category_id": {"type": "string"}, "is_published": {"type": "boolean"},
        },
        "required": ["title", "content"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from knowledge_base.models import KBArticle
        from django.utils.text import slugify
        a = KBArticle.objects.create(title=args['title'], slug=slugify(args['title']), content=args['content'], category_id=args.get('category_id'), is_published=args.get('is_published', False))
        return {"id": str(a.id), "title": a.title, "created": True}
