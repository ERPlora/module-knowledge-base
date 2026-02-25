# Knowledge Base & Wiki Module

Internal wiki, articles and knowledge management.

## Features

- Create and organize knowledge base articles with rich text content
- Categorize articles with custom categories and ordering
- Track article view counts for popularity insights
- Publish/unpublish workflow for content review
- Slug-based URLs for SEO-friendly article links

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Knowledge Base & Wiki > Settings**

## Usage

Access via: **Menu > Knowledge Base & Wiki**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/knowledge_base/dashboard/` | Overview of articles and categories |
| Articles | `/m/knowledge_base/articles/` | Browse, create, and edit articles |
| Categories | `/m/knowledge_base/categories/` | Manage article categories |
| Settings | `/m/knowledge_base/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `KBCategory` | Article category with name, slug, description, ordering, and active status |
| `KBArticle` | Knowledge base article with title, slug, content, publish status, view count, and category link |

## Permissions

| Permission | Description |
|------------|-------------|
| `knowledge_base.view_kbarticle` | View knowledge base articles |
| `knowledge_base.add_kbarticle` | Create new articles |
| `knowledge_base.change_kbarticle` | Edit existing articles |
| `knowledge_base.delete_kbarticle` | Delete articles |
| `knowledge_base.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
