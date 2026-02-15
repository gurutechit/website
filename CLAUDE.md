# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pelican-based static site for www.gurutech.it. Content is written in Markdown or reStructuredText in `content/`, processed by Pelican, and automatically deployed to GitHub Pages via GitHub Actions.

## Build Commands

```bash
# Development
make html                    # Build site to output/
make devserver               # Serve + auto-regenerate on changes (localhost:8000)
make serve                   # Serve output/ without auto-regenerate
make clean                   # Remove generated files

# Production
make publish                 # Build with production settings (publishconf.py)

# Debug
make DEBUG=1 html            # Build with debug output
make RELATIVE=1 html         # Use relative URLs
```

Alternative commands via Poetry/Invoke:
```bash
poetry run invoke livereload  # Live reload development server
poetry run invoke preview     # Build production version locally
```

## Architecture

**Dual Configuration Model**:
- `pelicanconf.py` - Development settings with relative URLs, feeds disabled
- `publishconf.py` - Production settings with absolute URLs (https://www.gurutech.it), feeds enabled

**Content Pipeline**:
1. Source files in `content/` (Markdown/reStructuredText)
2. Pelican processes → generates HTML in `output/`
3. Push to main branch triggers GitHub Actions deployment

**Key Paths**:
- `content/` - Source content (articles, pages, images)
- `content/extra/CNAME` - Custom domain configuration
- `output/` - Generated static site (gitignored)

## Deployment

GitHub Actions (`pelican-deploy.yml`) automatically deploys on push to main when changes occur in:
- `content/`, `pelicanconf.py`, `publishconf.py`, `theme/`, `pyproject.toml`, `poetry.lock`

Manual deployment: `make publish` then use GitHub Actions workflow dispatch.

## Dependencies

Managed via Poetry (Python 3.9+). Install with:
```bash
poetry install
```

## Git Workflow

- Main branch is **protected** - all changes must go through pull requests
- PRs must be **squash merged** (merge commits are disabled)
- Use `gh pr merge --squash` when merging PRs

## Plugins

- **sitemap** - Generates XML sitemap at `sitemap.xml`
- **seo** - Adds Open Graph and Twitter Card meta tags

## Markdown Extensions

Configured in `pelicanconf.py` under `MARKDOWN`:
- **codehilite** - Syntax highlighting (uses Pygments with `highlight` CSS class)
- **extra** - Tables, fenced code blocks, footnotes, attribute lists
- **meta** - Frontmatter metadata parsing

## CI/Testing

Pull requests run automated checks via `.github/workflows/ci.yml`:
- HTML5 validation (`html5validator`)
- Link checking (`htmltest` - config in `.htmltest.yml`)

Run locally:
```bash
poetry run html5validator --root output/
```

## Theme

Custom theme in `theme/` based on `bootstrap2-dark`. Key directories:
- `theme/templates/` - Jinja2 templates
- `theme/static/css/` - Bootstrap dark + Pygments highlighting
- `theme/static/js/` - jQuery, Bootstrap JS

## Content Metadata

Article/page frontmatter fields:
```markdown
Title: Article Title
Date: 2026-02-13
Tags: tag1, tag2
Slug: article-slug
Category: Category Name
Status: draft | published
Lang: en | it
```

## Scripts

Automation scripts in `scripts/`:
- `pelican_automated_install.py` - Automated Pelican setup from JSON config
- `bootstrap-website.sh` - Website initialization
