# Font Awesome Upgrade Patch

This patch upgrades Font Awesome from version 2.0 (2012) to version 6.7.2 (2024).

## Prerequisites

This patch must be applied **after** `bootstrap2-dark.patch`. The base patch fixes HTML validation errors and broken links in the original theme. This patch builds on top of those fixes.

## What this patch does

### Deletes
- `static/css/font-awesome.css` (old FA 2.0 CSS)

### Updates templates
- `templates/article_infos.html`
- `templates/base.html`
- `templates/search_sidebar.html`
- `templates/sidebar.html`
- `templates/taglist.html`
- `templates/tags.html`
- `templates/translations.html`
- `templates/twitter_profile.html`

### Icon class syntax changes

| Old (FA 2.0) | New (FA 6.x) |
|--------------|--------------|
| `icon-calendar` | `fa-solid fa-calendar-days` |
| `icon-user` | `fa-solid fa-user` |
| `icon-folder-open` | `fa-solid fa-folder-open` |
| `icon-folder-close` | `fa-solid fa-folder` |
| `icon-external-link` | `fa-solid fa-arrow-up-right-from-square` |
| `icon-th-list` | `fa-solid fa-list` |
| `icon-search` | `fa-solid fa-magnifying-glass` |
| `icon-tag` | `fa-solid fa-tag` |
| `icon-tags` | `fa-solid fa-tags` |
| `icon-bookmark` | `fa-solid fa-rss` |
| `icon-home` | `fa-solid fa-users` |
| `icon-edit` | `fa-solid fa-language` |
| `icon-twitter-sign` | `fa-brands fa-x-twitter` |
| `icon-{{ name }}-sign` | `fa-brands fa-{{ name }}` |
| `icon-large` | `fa-lg` |

## How to apply

This patch requires two steps:
1. Download Font Awesome 6.7.2 files
2. Apply the template patch

### Step 1: Download Font Awesome 6.7.2

```bash
# Download and extract Font Awesome 6.7.2 Free
cd /tmp
wget https://github.com/FortAwesome/Font-Awesome/releases/download/6.7.2/fontawesome-free-6.7.2-web.zip
unzip fontawesome-free-6.7.2-web.zip

# Copy CSS (rename to fontawesome.min.css)
cp fontawesome-free-6.7.2-web/css/all.min.css /path/to/theme/static/css/fontawesome.min.css

# Copy webfonts
mkdir -p /path/to/theme/static/webfonts
cp fontawesome-free-6.7.2-web/webfonts/* /path/to/theme/static/webfonts/

# Cleanup
rm -rf fontawesome-free-6.7.2-web fontawesome-free-6.7.2-web.zip
```

### Step 2: Apply the template patch

```bash
cd /path/to/project
patch -p1 < theme/bootstrap2-dark-font-awesome.patch
```

This will:
- Delete the old `static/css/font-awesome.css`
- Update all templates to use FA6 class syntax

### Step 3: Delete old font files

```bash
rm -rf /path/to/theme/static/font/
```

## Applying both patches to a fresh theme

```bash
# Clone the pelican-themes repository
git clone --depth 1 --filter=blob:none --sparse https://github.com/getpelican/pelican-themes.git
cd pelican-themes
git sparse-checkout set bootstrap2-dark

# Apply the base patch first
patch -p1 < /path/to/bootstrap2-dark.patch

# Download Font Awesome 6.7.2
wget -qO- https://github.com/FortAwesome/Font-Awesome/releases/download/6.7.2/fontawesome-free-6.7.2-web.zip | unzip -
cp fontawesome-free-6.7.2-web/css/all.min.css bootstrap2-dark/static/css/fontawesome.min.css
mkdir -p bootstrap2-dark/static/webfonts
cp fontawesome-free-6.7.2-web/webfonts/* bootstrap2-dark/static/webfonts/
rm -rf fontawesome-free-6.7.2-web

# Apply the Font Awesome template patch
patch -p1 < /path/to/bootstrap2-dark-font-awesome.patch

# Remove old font files
rm -rf bootstrap2-dark/static/font/
```

## Configuration note

If you use the `SOCIAL` variable in `pelicanconf.py`, the social network names must be **lowercase** to match Font Awesome 6 brand icon names:

```python
# Correct (FA6 compatible)
SOCIAL = (
    ("linkedin", "https://www.linkedin.com/in/..."),
    ("mastodon", "https://mastodon.social/@..."),
    ("github", "https://github.com/..."),
)

# Incorrect (won't render icons)
SOCIAL = (
    ("LinkedIn", "https://..."),
    ("GitHub", "https://..."),
)
```

See https://fontawesome.com/icons?s=brands for available brand icon names.

## Font Awesome resources

- Official website: https://fontawesome.com/
- GitHub releases: https://github.com/FortAwesome/Font-Awesome/releases
- Free icons search: https://fontawesome.com/search?o=r&m=free
