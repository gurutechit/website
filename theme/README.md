# Theme: bootstrap2-dark (patched)

This theme is based on [bootstrap2-dark](https://github.com/getpelican/pelican-themes/tree/master/bootstrap2-dark) from the pelican-themes repository, with patches applied to fix HTML validation errors and broken links.

## Changes from original

- `authors.html` - Added missing template (original was empty)
- `article.html` - Fixed duplicate `id="content"`, replaced undefined `{{ pagename }}` variable
- `archives.html` - Fixed duplicate `id="content"`
- `base.html` - Fixed invalid nested `<ul>` elements, removed stray `</link>` end tags, updated dead external links in footer

## Reapplying the patch

If you need to apply these fixes to a fresh copy of the original theme:

```bash
# Clone the pelican-themes repository (or just the bootstrap2-dark theme)
git clone --depth 1 --filter=blob:none --sparse https://github.com/getpelican/pelican-themes.git
cd pelican-themes
git sparse-checkout set bootstrap2-dark

# Apply the patch
patch -p1 < /path/to/bootstrap2-dark.patch
```

## Original theme

- Repository: https://github.com/getpelican/pelican-themes
- Theme path: `bootstrap2-dark/`
