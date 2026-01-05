# Gurutech Website

Source code for [www.gurutech.it](https://www.gurutech.it), built with [Pelican](https://getpelican.com/) and automatically deployed to GitHub Pages.

## Publishing New Content

1. Create a new branch:
   ```bash
   git checkout -b add-new-article
   ```

2. Add your content file in `content/` (Markdown or reStructuredText):
   ```bash
   # Example: content/my-article.md
   ```
   ```markdown
   Title: My Article Title
   Date: 2026-01-05
   Category: Blog

   Your article content goes here.
   ```

3. Preview locally (optional):
   ```bash
   poetry install
   make devserver
   # Open http://localhost:8000
   ```

4. Commit and push:
   ```bash
   git add content/my-article.md
   git commit -m "Add new article"
   git push origin add-new-article
   ```

5. Open a pull request on GitHub. Once merged to `main`, the site is automatically deployed.
