#!/usr/bin/env python3
"""
Convert the downloaded WordPress mirror of st-darmstadt.de into Jekyll content.

- Pages   -> site/<same path>/index.html   (cleaned HTML + front matter)
- Posts   -> site/_posts/YYYY-MM-DD-slug.md (Markdown + front matter); open tasks -> site/_tasks/; only posts
             published on/after --since (default: all posts)
- Images / PDFs referenced by converted content are copied to site/assets/YYYY/MM/...
  (same paths as on the old site, so old image URLs keep working)

Links to content that was not converted (older posts) point to the live old site.

Usage:
    pip install beautifulsoup4 markdownify
    python tools/convert_wp.py --mirror site_mirror/www.st-darmstadt.de --out site
"""
import argparse
import glob
import datetime as dt
import os
import posixpath
import re
import shutil
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from markdownify import MarkdownConverter

OLD_SITE = "https://www.st-darmstadt.de"
OLD_HOSTS = {"www.st-darmstadt.de", "st-darmstadt.de", "estelle.sailingteam.hg.tu-darmstadt.de"}
MONTHS = {m: i + 1 for i, m in enumerate(
    "januar februar märz april mai juni juli august september oktober november dezember".split())}

# Pages that are hand-written in the Jekyll site (not converted)
SKIP_PAGES = {"", "news", "mitmachen/aktuelle-aufgaben", "ueber-uns/boote", "partner"}
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8}
# Sections whose sub-pages get a side navigation (from _data/navigation.yml)
MAX_IMG_WIDTH = 1600


def with_baseurl(text):
    """Prefix root-relative links in content with {{ site.baseurl }} so the site also works from a
    sub-path (GitHub Pages project site). Front matter paths stay plain; templates use relative_url."""
    text = re.sub(r"\]\(/(?!/)", "]({{ site.baseurl }}/", text)
    return re.sub(r'(\s(?:src|href|data-thumb|poster)=")/(?!/)', r"\1{{ site.baseurl }}/", text)


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_german_date(text):
    m = re.search(r"(\d{1,2})\.\s*([A-Za-zäöüÄÖÜ]+)\s+(\d{4})", text)
    if not m:
        return None
    return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))


class Converter:
    def __init__(self, mirror, out, since):
        self.mirror = os.path.abspath(mirror)
        self.out = os.path.abspath(out)
        self.since = since
        self.copied = set()
        self.post_urls = set()   # site paths of posts we convert, e.g. /2025/09/slug/

    # ------------------------------------------------------------ URL helpers
    def mirror_rel(self, ref, page_file):
        """Resolve a reference found in page_file to a path relative to the mirror
        root (e.g. 'ueber-uns/index.html'), or None if it points elsewhere."""
        p = urlparse(ref)
        if p.scheme in ("http", "https"):
            if p.netloc not in OLD_HOSTS:
                return None
            return unquote(p.path).lstrip("/")
        if p.scheme or ref.startswith("#"):
            return None
        page_dir = os.path.dirname(os.path.relpath(page_file, self.mirror))
        return posixpath.normpath(posixpath.join(page_dir, unquote(p.path)))

    def site_link(self, ref, page_file):
        """Map a link to its URL on the new site."""
        rel = self.mirror_rel(ref, page_file)
        if rel is None:
            return ref
        frag = "#" + urlparse(ref).fragment if urlparse(ref).fragment else ""
        if rel.startswith("wp-content/"):
            return self.copy_asset(rel) or OLD_SITE + "/" + rel
        if rel.endswith("index.html"):
            rel = rel[: -len("index.html")]
        url = "/" + rel.strip("/") + ("/" if rel.strip("/") else "")
        url = url.replace("//", "/")
        if re.match(r"^/\d{4}/", url) and url not in self.post_urls:
            return OLD_SITE + url + frag     # older post that wasn't converted
        return url + frag

    def copy_asset(self, rel):
        src = os.path.join(self.mirror, rel)
        if not os.path.isfile(src):
            # Original not mirrored: fall back to the largest resized variant (name-WxH.ext)
            base, ext = os.path.splitext(src)
            variants = []
            for v in glob.glob(glob.escape(base) + "-*x*" + ext):
                m = re.search(r"-(\d+)x(\d+)" + re.escape(ext) + "$", v)
                if m:
                    variants.append((int(m.group(1)), v))
            if not variants:
                return None
            src = max(variants)[1]
            rel = os.path.relpath(src, self.mirror)
        out_rel = self.asset_path(rel)
        if rel not in self.copied:
            dst = os.path.join(self.out, out_rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            self.copied.add(rel)
        return "/" + out_rel

    @staticmethod
    def asset_path(rel):
        """WordPress upload path -> path in the new site: wp-content/uploads/2025/10/x.jpg -> assets/2025/10/x.jpg"""
        for prefix in ("wp-content/uploads/", "wp-content/"):
            if rel.startswith(prefix):
                return "assets/" + rel[len(prefix):]
        return rel

    def video_thumb(self, wrapper, yid, page_file):
        """Copy the preview image cached by wp-youtube-lyte to /assets/video-thumbs/<id>.jpg."""
        img = wrapper.find("img", src=re.compile(r"lyteCache_"))
        rel = self.mirror_rel(img["src"], page_file) if img else None
        src = os.path.join(self.mirror, rel) if rel else None
        if not src or not os.path.isfile(src):
            return None
        dst = os.path.join(self.out, "assets", "video-thumbs", f"{yid}.jpg")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return f"/assets/video-thumbs/{yid}.jpg"

    def best_image(self, img, page_file):
        """Pick a reasonably sized local file from src/srcset."""
        candidates = []
        for item in (img.get("srcset") or "").split(","):
            bits = item.strip().split()
            if len(bits) == 2 and bits[1].endswith("w"):
                candidates.append((int(bits[1][:-1]), bits[0]))
        candidates.sort()
        chosen = None
        fitting = [c for c in candidates if c[0] <= MAX_IMG_WIDTH]
        if fitting:
            chosen = fitting[-1][1]
        for ref in filter(None, [chosen, img.get("src"), img.get("data-src")] + [c[1] for c in candidates]):
            rel = self.mirror_rel(ref, page_file)
            if rel and rel.startswith("wp-content/"):
                url = self.copy_asset(rel)
                if url:
                    return url
        src = img.get("src")
        return src if src and src.startswith("http") else None

    # -------------------------------------------------------------- cleaning
    def clean(self, root, page_file):
        soup = root
        for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
            c.extract()
        for sel in ["script", "style", "form", ".vc_empty_space", ".social-share",
                    ".single-share-title", ".vc_separator", ".lyte_disclaimer"]:
            for el in soup.select(sel):
                el.decompose()

        # YouTube (wp-youtube-lyte) -> privacy friendly click-to-load placeholder
        for el in soup.select(".lyte-wrapper"):
            vid = el.find(id=re.compile(r"^WYL_"))
            if vid:
                yid = vid["id"][4:]
                thumb = self.video_thumb(el, yid, page_file)
                extra = f' data-thumb="{thumb}"' if thumb else ""
                el.replace_with(self.new(soup, f'<div class="video" data-youtube="{yid}"{extra}></div>'))
            else:
                el.decompose()
        for el in soup.find_all("noscript"):
            el.decompose()

        # Self-hosted videos (<video src=...mp4>) -> copied file with native player
        for el in soup.find_all("video"):
            src = el.get("src") or (el.find("source") or {}).get("src")
            url = self.site_link(src, page_file) if src else None
            if url and url.startswith("/assets/"):
                el.replace_with(self.new(soup, f'<div class="video-file"><video controls preload="metadata" playsinline src="{url}"></video></div>'))
            else:
                el.decompose()
        for el in soup.select(".lL"):
            el.decompose()

        # Ultimate Addons "info list" (icon + heading + text) -> simple cards
        for ul in soup.select("ul.smile_icon_list"):
            items = []
            for li in ul.select("li.icon_list_item"):
                h = li.select_one(".info-list-heading")
                d = li.select_one(".icon_description_text")
                items.append(f"<div class=\"info-item\"><h3>{h.decode_contents() if h else ''}</h3>"
                             f"{d.decode_contents() if d else ''}</div>")
            wrap = ul.find_parent(class_="smile_icon_list_wrap") or ul
            wrap.replace_with(self.new(soup, '<div class="info-list">' + "".join(items) + "</div>"))

        # Carousels / sliders / galleries -> grid of images
        for sel in [".ult-carousel-wrapper", ".wpb_gallery", ".wp-block-gallery"]:
            for el in soup.select(sel):
                imgs = el.find_all("img")
                html = "".join(str(i) for i in imgs)
                logos = sel == ".ult-carousel-wrapper"
                if len(imgs) == 1 and not logos:      # a one-image "gallery" is just an image
                    el.replace_with(self.new(soup, f"<p>{html}</p>"))
                    continue
                el.replace_with(self.new(soup, f'<div class="{"logo-grid" if logos else "gallery"}">{html}</div>'))

        # Buttons
        for el in soup.select(".vc_btn3-container"):
            a = el.find("a")
            if a:
                a.attrs = {"href": a.get("href", "#"), "class": "btn"}
                el.replace_with(a)

        # WPBakery rows: multi-column rows become a CSS grid, single columns are unwrapped
        for row in soup.select(".vc_row"):
            cols = row.find_all(class_="wpb_column", recursive=False)
            if len(cols) > 1:
                only_images = all(not c.get_text(strip=True) and c.find("img") for c in cols)
                row.attrs = {"class": "logo-grid" if only_images else f"cols cols-{len(cols)}"}
                for c in cols:
                    c.attrs = {"class": "col"}
            else:
                row.unwrap()

        # Images
        for img in soup.find_all("img"):
            src = self.best_image(img, page_file)
            if not src or "lyteCache" in src:
                img.decompose()
                continue
            align = "right" if "alignright" in img.get("class", []) else "left" if "alignleft" in img.get("class", []) else None
            img.attrs = {"src": src, "alt": img.get("alt", ""), "loading": "lazy"}
            if align:
                img["class"] = "align" + align

        # Links
        for a in soup.find_all("a", href=True):
            href = self.site_link(a["href"].strip(), page_file)
            keep_cls = a.get("class") == "btn"
            a.attrs = {"href": href}
            if keep_cls:
                a["class"] = "btn"
            if href.startswith("http") and not any(h in href for h in OLD_HOSTS):
                a["target"] = "_blank"
                a["rel"] = "noopener"

        # Strip presentational attributes / wrappers
        keep_classes = {"video", "video-file", "info-list", "info-item", "gallery", "logo-grid", "cols", "col",
                        "btn", "alignright", "alignleft"} | {f"cols-{i}" for i in range(2, 7)}
        for el in soup.find_all(True):
            classes = el.get("class") or []
            if isinstance(classes, str):
                classes = classes.split()
            classes = [c for c in classes if c in keep_classes]
            attrs = {k: v for k, v in el.attrs.items() if k in ("href", "src", "alt", "loading", "target", "rel",
                                                                "data-youtube", "data-thumb", "controls", "preload", "playsinline", "colspan", "rowspan")}
            if classes:
                attrs["class"] = " ".join(classes)
            el.attrs = attrs
        for el in soup.find_all(["div", "span", "figure", "main", "article", "section"]):
            if not el.attrs and el.name in ("div", "span", "main", "article", "section"):
                el.unwrap()
        for el in soup.find_all("figure"):
            if not el.find("figcaption"):
                el.unwrap()
        for el in soup.find_all(["p", "h1", "h2", "h3", "h4", "li", "strong", "em"]):
            if not el.get_text(strip=True) and not el.find(["img", "iframe", "br"]):
                el.decompose()
        # Lists that only wrap another list (ul > li > ul) -> flatten
        for li in soup.find_all("li"):
            kids = [c for c in li.contents if not (isinstance(c, NavigableString) and not c.strip())]
            if len(kids) == 1 and getattr(kids[0], "name", None) in ("ul", "ol"):
                outer = li.parent
                li.unwrap()
                kids[0].unwrap()
                if outer and outer.name in ("ul", "ol") and outer.find_parent(["ul", "ol"]):
                    outer.unwrap()
        # Logo grids: drop column wrappers and merge consecutive grids into one
        for grid in soup.select(".logo-grid"):
            for col in grid.select(".col"):
                col.unwrap()
        for grid in soup.select(".logo-grid"):
            nxt = grid.find_next_sibling()
            while nxt is not None and "logo-grid" in (nxt.get("class") or []):
                for child in list(nxt.contents):
                    grid.append(child)
                nxt.decompose()
                nxt = grid.find_next_sibling()
        # demote h1 (layout renders the title)
        for h in soup.find_all("h1"):
            h.name = "h2"
        return soup

    @staticmethod
    def new(soup, html):
        return BeautifulSoup(html, "html.parser")

    # ------------------------------------------------------------------ pages
    def page_title(self, soup):
        t = soup.title.get_text() if soup.title else ""
        return re.split(r"\s+[–|-]\s+Sailing Team Darmstadt", t)[0].strip()

    def convert_page(self, rel_dir, path):
        soup = BeautifulSoup(open(path, encoding="utf-8"), "html.parser")
        content = soup.select_one("#main .col-md-9") or soup.select_one("#main")
        if content is None:
            print("  ! no content:", rel_dir)
            return
        for el in content.select("aside, .sidebar"):
            el.decompose()
        content = self.clean(content, path)
        self.drop_empty_cols(content)
        title = self.page_title(soup)
        # Drop a leading heading identical to the title
        first = content.find(["h2", "h3"])
        if first and first.get_text(strip=True) == title:
            first.decompose()
        html = self.pretty(content.decode_contents())
        url = "/" + rel_dir + "/"
        out = os.path.join(self.out, rel_dir, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"---\nlayout: page\ntitle: {yaml_str(title)}\npermalink: {url}\n---\n{with_baseurl(html)}\n")
        print(f"  page  {url}  ({title})")

    @staticmethod
    def drop_empty_cols(soup):
        for row in soup.select(".cols"):
            for col in row.find_all(class_="col", recursive=False):
                if not col.get_text(strip=True) and not col.find(["img", "iframe", "div"]):
                    col.decompose()
            cols = row.find_all(class_="col", recursive=False)
            if len(cols) <= 1:
                for c in cols:
                    c.unwrap()
                row.unwrap()
            else:
                row["class"] = f"cols cols-{len(cols)}"
        # A row that only holds buttons belongs to the columns above it
        # (otherwise the buttons end up together at the bottom on mobile)
        for row in soup.select(".cols"):
            cols = row.find_all(class_="col", recursive=False)
            only_buttons = cols and all(c.find("a", class_="btn") and
                                        not c.get_text(strip=True).replace(c.find("a").get_text(strip=True), "")
                                        for c in cols)
            prev = row.find_previous_sibling()
            prev_cols = prev.find_all(class_="col", recursive=False) if prev is not None and "cols" in (prev.get("class") or "") else []
            if only_buttons and len(prev_cols) == len(cols):
                for target, col in zip(prev_cols, cols):
                    for child in list(col.contents):
                        target.append(child)
                row.decompose()

    # ------------------------------------------------------------------ boats
    @staticmethod
    def lines_of(el):
        """Text lines of a spec block (list items or <br>-separated lines)."""
        if el.find("li"):
            return [" ".join(li.get_text(" ", strip=True).split()) for li in el.find_all("li")]
        for br in el.find_all("br"):
            br.replace_with("\n")
        lines = el.get_text().split("\n")
        return [" ".join(l.split()).lstrip("›").strip() for l in lines if l.strip()]

    def load_content(self, path):
        soup = BeautifulSoup(open(path, encoding="utf-8"), "html.parser")
        content = soup.select_one("#main .col-md-9") or soup.select_one("#main")
        for el in content.select("aside, .sidebar"):
            el.decompose()
        return soup, self.clean(content, path)

    def parse_boat_overview(self):
        """The old overview page has per-boat 'Features' and 'Ziel' – keep them."""
        path = os.path.join(self.mirror, "ueber-uns/boote/index.html")
        if not os.path.exists(path):
            return {}
        _, content = self.load_content(path)
        info = {}
        for h2 in content.find_all("h2"):
            link = h2.find_previous("a", href=re.compile(r"^/ueber-uns/boote/[^/]+/$"))
            lst = h2.find_next(class_="info-list")
            if not link or not lst:
                continue
            data = {}
            img = link.find("img")
            if img:
                data["card_image"] = img["src"]
            for item in lst.select(".info-item"):
                h = item.find("h3")
                key = h.get_text(strip=True)
                h.decompose()
                data[key] = self.lines_of(item)
            info[link["href"]] = data
        return info

    def convert_boat(self, rel_dir, path, overview):
        soup, content = self.load_content(path)
        title = self.page_title(soup)
        m = re.match(r"(Prototyp\s+([IVX]+))\s*[–-]\s*[„\"](.+?)[“\"]", title)
        number, order, name = (m.group(1), ROMAN.get(m.group(2), 0), m.group(3)) if m else ("", 0, title)
        h4 = content.find("h4")
        since = h4.get_text(strip=True) if h4 else ""
        if h4:
            h4.decompose()
        specs = []
        for item in content.select(".info-item"):
            h = item.find("h3")
            key = h.get_text(strip=True) if h else ""
            if h:
                h.decompose()
            specs.append((key, self.lines_of(item)))
        gallery = [img["src"] for g in content.select(".gallery") for img in g.find_all("img")]
        partners = [img["src"] for g in content.select(".logo-grid") for img in g.find_all("img")]
        partners_link = None
        for a in content.find_all("a", href=re.compile(r"^/partner/")):
            partners_link = a["href"]
            (a.find_parent("p") or a).decompose()
        for el in content.select(".gallery, .logo-grid, .info-list"):
            el.decompose()
        # any remaining loose images go into the gallery
        for img in content.find_all("img"):
            gallery.append(img["src"])
            img.decompose()
        intro = "\n".join(str(p) for p in content.find_all("p") if p.get_text(strip=True))

        url = "/" + rel_dir + "/"
        extra = overview.get(url, {})
        fm = ["layout: boat", f"title: {yaml_str(title)}", f"boat_name: {yaml_str(name)}",
              f"number: {yaml_str(number)}", f"order: {order}", f"since: {yaml_str(since)}",
              f"permalink: {url}"]
        hero = extra.get("card_image") or (gallery[0] if gallery else None)
        if hero:
            fm.append(f"image: {hero}")

        def ylist(key, values):
            if values:
                fm.append(f"{key}:")
                fm.extend(f"  - {yaml_str(v)}" for v in values)

        ylist("goal", extra.get("Ziel"))
        ylist("features", extra.get("Features"))
        if specs:
            fm.append("specs:")
            for key, items in specs:
                fm.append(f"  - title: {yaml_str(key)}")
                fm.append("    items:")
                fm.extend(f"      - {yaml_str(v)}" for v in items)
        ylist("gallery", gallery)
        ylist("partners", partners)
        if partners_link:
            fm.append(f"partners_link: {partners_link}")
        out = os.path.join(self.out, rel_dir, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        # Keep hand-set flags (e.g. "pinned: true") when the post is regenerated
        if os.path.exists(out):
            old_fm = open(out, encoding="utf-8").read().split("---")[1]
            fm += [l for l in old_fm.splitlines() if l.startswith("pinned:")]
        with open(out, "w", encoding="utf-8") as f:
            f.write("---\n" + "\n".join(fm) + "\n---\n" + with_baseurl(intro) + "\n")
        print(f"  boat  {url}  ({title})")

    @staticmethod
    def pretty(html):
        html = re.sub(r"\n\s*\n+", "\n", html)
        html = re.sub(r">\s+<", ">\n<", html)
        return html.strip()

    # ------------------------------------------------------------------ posts
    def collect_authors(self):
        """Post listings show 'By <author>'; single posts don't."""
        authors = {}
        listing_files = [os.path.join(self.mirror, "mitmachen/aktuelle-aufgaben/index.html"),
                         os.path.join(self.mirror, "news/index.html")]
        for f in listing_files:
            if not os.path.exists(f):
                continue
            soup = BeautifulSoup(open(f, encoding="utf-8"), "html.parser")
            for span in soup.select(".author-name"):
                title_link = span.find_previous(["h2", "h3"])
                a = title_link.find("a", href=True) if title_link else None
                name = span.get_text(" ", strip=True).removeprefix("By").strip()
                if a and name:
                    authors.setdefault(self.site_link(a["href"], f), name)
        return authors

    def find_posts(self):
        posts = []
        for year in sorted(os.listdir(self.mirror)):
            if not re.fullmatch(r"\d{4}", year):
                continue
            for root, _, files in os.walk(os.path.join(self.mirror, year)):
                if "index.html" in files:
                    rel = os.path.relpath(root, self.mirror)
                    if re.fullmatch(r"\d{4}/\d{2}/[^/]+", rel) and "/page/" not in rel:
                        posts.append((rel, os.path.join(root, "index.html")))
        return posts

    def convert_post(self, rel, path, authors):
        soup = BeautifulSoup(open(path, encoding="utf-8"), "html.parser")
        art = soup.find("article")
        content = art.select_one(".entry-content")
        heading = content.select_one(".heading")
        title = heading.select_one(".title").get_text(strip=True)
        date = parse_german_date(heading.select_one(".date").get_text())
        heading.decompose()
        cats = [c[len("category-"):] for c in art.get("class", []) if c.startswith("category-")]
        cats = [c for c in cats if c not in ("uncategorized", "not-for-landingpage")]
        media = soup.select_one(".media-con img")
        image = self.best_image(media, path) if media else None

        content = self.clean(content, path)
        md = PostMarkdown(heading_style="ATX", bullets="-", escape_underscores=False).convert_soup(content)
        md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"

        slug = rel.split("/")[-1]
        url = f"/{rel}/"
        fm = [f"title: {yaml_str(title)}", f"date: {date.isoformat()}", f"permalink: {url}"]
        is_task = "tasks" in cats            # open tasks go to their own collection
        cats = [c for c in cats if c != "tasks"]
        if cats:
            fm.append(f"categories: [{', '.join(cats)}]")
        if authors.get(url):
            fm.append(f"author: {yaml_str(authors[url])}")
        if image:
            fm.append(f"image: {image}")
        else:
            # No featured image: use the first picture in the text as thumbnail for cards
            first = content.find("img", src=re.compile(r"^/assets/\d{4}/"))
            video = content.find(attrs={"data-thumb": True})
            if first:
                fm.append(f"thumbnail: {first['src']}")
            elif video:
                fm.append(f"thumbnail: {video['data-thumb']}")
        # Teaser text: first paragraph that is long enough to be meaningful
        for para in content.find_all("p"):
            text = " ".join(para.get_text(" ", strip=True).split())
            if len(text) >= 60:
                fm.append(f"excerpt: {yaml_str(text[:300])}")
                break
        out = os.path.join(self.out, "_tasks" if is_task else "_posts", f"{date.isoformat()}-{slug}.md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        # Keep hand-set flags (e.g. "pinned: true") when the post is regenerated
        if os.path.exists(out):
            old_fm = open(out, encoding="utf-8").read().split("---")[1]
            fm += [l for l in old_fm.splitlines() if l.startswith("pinned:")]
        with open(out, "w", encoding="utf-8") as f:
            f.write("---\n" + "\n".join(fm) + "\n---\n\n" + with_baseurl(md))
        print(f"  post  {url}  ({title})")

    # -------------------------------------------------------------------- run
    def run(self):
        # Decide which posts are converted first, so links between them stay internal
        posts = []
        for rel, path in self.find_posts():
            soup = BeautifulSoup(open(path, encoding="utf-8"), "html.parser")
            d = soup.select_one(".single-blog .date")
            date = parse_german_date(d.get_text()) if d else None
            if date and date >= self.since:
                posts.append((rel, path))
                self.post_urls.add(f"/{rel}/")
        authors = self.collect_authors()

        print(f"Converting {len(posts)} posts since {self.since}:")
        for rel, path in posts:
            self.convert_post(rel, path, authors)

        overview = self.parse_boat_overview()
        print("Converting pages:")
        for root, _, files in os.walk(self.mirror):
            rel = os.path.relpath(root, self.mirror).replace(os.sep, "/")
            rel = "" if rel == "." else rel
            if "index.html" not in files or rel in SKIP_PAGES:
                continue
            if re.match(r"^(\d{4}|news|wp-|page)", rel):
                continue
            if rel.startswith("ueber-uns/boote/"):
                self.convert_boat(rel, os.path.join(root, "index.html"), overview)
            else:
                self.convert_page(rel, os.path.join(root, "index.html"))
        self.copy_asset("wp-content/uploads/2019/04/Sailingteam_Faltblatt.pdf")  # sidebar download
        print(f"Copied {len(self.copied)} images/files.")


class PostMarkdown(MarkdownConverter):
    """Keep layout blocks (galleries, videos, columns) as raw HTML inside Markdown."""
    RAW = {"gallery", "video", "video-file", "logo-grid", "cols", "info-list"}

    def convert_div(self, el, text, *args, **kwargs):
        cls = el.get("class") or []
        if isinstance(cls, str):
            cls = cls.split()
        if set(cls) & self.RAW:
            return "\n\n" + str(el) + "\n\n"
        return text

    def convert_img(self, el, text, *args, **kwargs):
        cls = el.get("class")
        if cls:
            return str(el)
        return super().convert_img(el, text, *args, **kwargs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mirror", default="site_mirror/www.st-darmstadt.de")
    ap.add_argument("--out", default="site")
    ap.add_argument("--since", default="1900-01-01", help="Only convert posts on/after this date")
    args = ap.parse_args()
    Converter(args.mirror, args.out, dt.date.fromisoformat(args.since)).run()


if __name__ == "__main__":
    main()
