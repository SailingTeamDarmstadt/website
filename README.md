# Sailing Team Darmstadt – Website

Static website built with [Jekyll](https://jekyllrb.com/), migrated from the old WordPress site.

## Run locally

```bash
bundle install          # once
bundle exec jekyll serve  # → http://localhost:4000
```

## Writing a news post

Create `_posts/YYYY-MM-DD-my-title.md`:

```markdown
---
title: "Testfahrt am Langener Waldsee"
image: /assets/2026/11/testfahrt.jpg   # optional cover image
author: "Vorname Nachname"                    # optional
---

Text in **Markdown** …

![Bildbeschreibung]({{ site.baseurl }}/assets/2026/11/foto.jpg)
```

- Open tasks for *Mitmachen → Aktuelle Aufgaben* live in `_tasks/` instead of `_posts/`
  (same file naming and front matter); they don't appear in the news.
- Image galleries: `<div class="gallery">` with `<img>` tags inside.
- YouTube video (loads only on click, GDPR friendly): `<div class="video" data-youtube="VIDEO_ID"></div>`

### Pinning a post

Add `pinned: true` to a post's front matter to pin it. Pinned posts

- appear in an "Angepinnt" section at the top of the News page (and still under their year),
- are shown first in "Neues aus dem Team" on the start page (max. 3 cards in total),
- get an "Angepinnt" badge on their card.

Remove the line (or set `pinned: false`) to unpin. Re-running the converter keeps the flag.

## Publishing (GitHub Pages)

Every push to `main` builds the site with GitHub Actions (`.github/workflows/pages.yml`) and deploys it to
GitHub Pages. The workflow sets `baseurl` to the Pages sub-path (`/website`), so **links and images in content
must start with `{{ site.baseurl }}`**, e.g.

```markdown
![Bildbeschreibung]({{ site.baseurl }}/assets/2026/11/foto.jpg)
[Mitmachen]({{ site.baseurl }}/mitmachen/)
```

Front matter paths (`image:`, `thumbnail:`) stay plain (`/assets/...`); the templates add the base URL.
With a custom domain (e.g. www.st-darmstadt.de) the base URL is empty and the links work unchanged.

## Boats

Each boat is `ueber-uns/boote/<slug>/index.html` with `layout: boat`. Its data is in the front matter
(`boat_name`, `number`, `order`, `since`, `image`, `goal`, `specs`, `gallery`, `partners`) and the text
goes below the front matter. The overview page `/ueber-uns/boote/` lists every boat automatically, sorted by `order`.
Spec lines written as `Label: Wert` are shown as a two-column row.

## Structure

| Path | Content |
|---|---|
| `index.html` | Homepage |
| `_posts/` | News (Markdown) |
| `_tasks/` | Aktuelle Aufgaben (Markdown) |
| `ueber-uns/`, `partner/`, `mitmachen/`, `kontakt/`, … | Pages (HTML with front matter) |
| `_data/navigation.yml` | Main menu + side navigation |
| `_layouts/`, `_includes/` | Templates |
| `assets/css/main.css` | All styles (colors as CSS variables at the top) |
| `assets/YYYY/MM/` | Images & files migrated from WordPress (former `wp-content/uploads/`) |

## Migration

Content was generated from the WordPress mirror with `tools/convert_wp.py`.
All posts (2008 until today) and every referenced image/file have been migrated; the site is
self-contained and needs neither the old WordPress server nor the mirror to run.
`tools/convert_wp.py` was the one-time migration script (it needs the downloaded WordPress mirror and would
re-create deleted posts) – edit the Markdown files directly instead. `tools/recolor_logo.py` recolors the logo PNG.
