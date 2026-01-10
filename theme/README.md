# Theme: bootstrap2-dark (patched)

This theme is based on [bootstrap2-dark](https://github.com/getpelican/pelican-themes/tree/master/bootstrap2-dark) from the pelican-themes repository, with patches applied to fix HTML validation errors and broken links.

## Changes from original

### 1. Duplicate ID Attribute (`id="content"`)

**Files:** `archives.html`, `article.html`

```html
<!-- Before -->
<section id="content">

<!-- After -->
<section class="content-section">
```

**Why mandatory (HTML standard):** The HTML specification requires that `id` attributes be unique within a document. The `base.html` template already contained an element with `id="content"`, causing duplicate IDs in generated pages.

**References:**
- [HTML Living Standard - The id attribute](https://html.spec.whatwg.org/multipage/dom.html#the-id-attribute)

---

### 2. Undefined Jinja2 Variable (`{{ pagename }}`)

**File:** `article.html`

```html
<!-- Before -->
<a href="{{ pagename }}"

<!-- After -->
<a href="{{ SITEURL }}/{{ article.url }}"
```

**Why mandatory (Pelican):** The variable `{{ pagename }}` does not exist in Pelican's template context. This caused the `href` attribute to render as empty, resulting in blank links that failed validation.

**References:**
- [Pelican Theming Documentation - article object](https://docs.getpelican.com/en/stable/themes.html#article)
- [Pelican Template Variables](https://docs.getpelican.com/en/stable/themes.html#templates-and-variables)

---

### 3. Missing `authors.html` Template

**File:** `authors.html` (was empty in original theme)

The original theme had an empty `authors.html`, which generated HTML without `<!DOCTYPE>`, `<html>`, `<head>`, or `<title>` elements.

**Why mandatory (HTML standard):** Every HTML document must have a DOCTYPE declaration and a `<title>` element.

**References:**
- [HTML Living Standard - The DOCTYPE](https://html.spec.whatwg.org/multipage/syntax.html#the-doctype)
- [HTML Living Standard - The title element](https://html.spec.whatwg.org/multipage/semantics.html#the-title-element)

---

### 4. Invalid Nested `<ul>` Elements

**File:** `base.html`

```html
<!-- Before -->
<ul class="nav pull-right">
    <li><a href="{{ SITEURL }}/archives.html">...</a></li>
</ul>

<!-- After (inside parent <ul>) -->
<li class="pull-right"><a href="{{ SITEURL }}/archives.html">...</a></li>
```

**Why mandatory (HTML standard):** A `<ul>` element can only contain `<li>` elements as direct children. The original code had a `<ul>` nested directly inside another `<ul>`.

**References:**
- [HTML Living Standard - The ul element](https://html.spec.whatwg.org/multipage/grouping-content.html#the-ul-element)
- [MDN Web Docs - ul element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul)

---

### 5. Self-closing `<link />` Tags

**File:** `base.html`

```html
<!-- Before (XHTML-style) -->
<link href="..." rel="alternate" />

<!-- After (HTML5-style) -->
<link href="..." rel="alternate">
```

**Why best practice (HTML5):** In HTML5, `<link>` is a void element and should not have a closing tag or trailing slash. While the trailing slash is technically allowed, it's unnecessary and can cause validation warnings.

**References:**
- [HTML Living Standard - Void elements](https://html.spec.whatwg.org/multipage/syntax.html#void-elements)

---

### 6. Dead External Links in Footer

**File:** `base.html`

| Before (dead) | After (working) |
|---------------|-----------------|
| `http://pelican.notmyidea.org/` | `https://getpelican.com/` |
| `http://python.org` | `https://www.python.org` |
| `http://twitter.github.com/bootstrap/` | `https://getbootstrap.com/` |
| `http://fortawesome.github.com/Font-Awesome/` | `https://fontawesome.com/` |

**Why best practice:** These domains no longer exist or have moved. Broken links negatively impact SEO and user experience. Updated to use HTTPS.

---

## Summary

| Fix | Category | Requirement | Pelican-Specific? |
|-----|----------|-------------|-------------------|
| Duplicate `id="content"` | HTML Validity | Mandatory | No |
| `{{ pagename }}` undefined | Template Error | Mandatory | Yes |
| Missing `authors.html` | HTML Validity | Mandatory | Yes |
| Nested `<ul>` elements | HTML Validity | Mandatory | No |
| Self-closing `<link />` | HTML Validity | Best practice | No |
| Dead external links | Link Integrity | Best practice | No |

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
