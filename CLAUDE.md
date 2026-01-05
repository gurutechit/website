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
