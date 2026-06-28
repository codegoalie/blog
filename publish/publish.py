#!/usr/bin/env python3
"""Publish Obsidian notes from the vault's Blog/Publish folder to a Hugo blog."""
import os, re, sys, time, shutil, subprocess, datetime, pathlib
import yaml

# ---- config ---------------------------------------------------------------
VAULT_ROOT    = pathlib.Path("/home/chris/vault")
PUBLISH_DIR   = VAULT_ROOT / "Blog" / "Publish"
PUBLISHED_DIR = VAULT_ROOT / "Blog" / "Published"
BLOG_REPO     = pathlib.Path("/home/chris/blog")
CONTENT_DIR   = BLOG_REPO / "content" / "posts"
GIT_BRANCH    = "main"
POST_BASE_URL = "/posts"          # Hugo permalink base for content/posts/<slug>/
# where to look for embedded images (first match wins; whole vault as fallback)
ATTACHMENT_DIRS = [VAULT_ROOT / "Attachments", VAULT_ROOT]
# ---------------------------------------------------------------------------

EMBED    = re.compile(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")          # ![[img.png]]
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")          # [[note|alias]]
CALLOUT  = re.compile(r"^>\s*\[!(\w+)\]\s*(.*)$", re.MULTILINE)     # > [!note] ...
IMG_EXT  = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower().strip())
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-") or "post"


def split_frontmatter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                return (yaml.safe_load(parts[1]) or {}), parts[2].lstrip("\n")
            except yaml.YAMLError:
                pass
    return {}, text


def compute_meta(note_path):
    """Title + slug for a note, using the same rules as process()."""
    fm, _ = split_frontmatter(note_path.read_text(encoding="utf-8"))
    title = fm.get("title") or note_path.stem
    slug  = fm.get("slug") or slugify(title)
    return title, slug


def build_slug_map():
    """Map {note name -> slug} for every published + about-to-be-published note.

    Obsidian wikilinks target a note's filename, so we key by basename; the title
    is added as a secondary key so [[Exact Title]] resolves too. Both the already
    published archive and the current batch are included, so same-batch links
    resolve in either direction regardless of processing order.
    """
    m = {}
    for d in (PUBLISHED_DIR, PUBLISH_DIR):
        if not d.exists():
            continue
        for p in d.glob("*.md"):
            if p.name.startswith("."):
                continue
            try:
                title, slug = compute_meta(p)
            except Exception:
                continue
            m[p.stem.lower()] = slug
            m.setdefault(title.lower(), slug)
    return m


def make_wikilink_sub(slug_map):
    def sub(m):
        raw   = m.group(1).strip()
        alias = (m.group(2) or "").strip()
        target, _, anchor = raw.partition("#")
        target = target.strip()
        # [[#Heading]] -> link within the same post
        if not target and anchor:
            return f"[{alias or anchor}](#{slugify(anchor)})"
        slug = slug_map.get(target.lower())
        display = alias or target
        if slug:
            url = f"{POST_BASE_URL}/{slug}/"
            if anchor:
                url += "#" + slugify(anchor)
            return f"[{display}]({url})"
        return display          # unresolved -> plain text
    return sub


def find_attachment(name):
    for base in ATTACHMENT_DIRS:
        if base.exists():
            for p in base.rglob(name):
                return p
    return None


def process(note_path, wl_sub):
    fm, body = split_frontmatter(note_path.read_text(encoding="utf-8"))

    title = fm.get("title") or note_path.stem
    slug  = fm.get("slug") or slugify(title)
    date  = fm.get("date") or datetime.datetime.fromtimestamp(
        note_path.stat().st_mtime).replace(microsecond=0).isoformat()

    bundle = CONTENT_DIR / slug
    bundle.mkdir(parents=True, exist_ok=True)

    # embeds -> copy image into the page bundle, rewrite the link
    def embed_sub(m):
        target = m.group(1).strip()
        if pathlib.Path(target).suffix.lower() in IMG_EXT:
            src = find_attachment(target)
            if src:
                shutil.copy2(src, bundle / src.name)
                return f"![]({src.name})"
            print(f"  ! image not found: {target}", file=sys.stderr)
            return f"![missing: {target}]()"
        print(f"  ! skipping non-image embed: {target}", file=sys.stderr)
        return f"<!-- embed omitted: {target} -->"
    body = EMBED.sub(embed_sub, body)

    body = WIKILINK.sub(wl_sub, body)          # cross-post links via slug map

    # callouts -> blockquote with a bold label
    def callout_sub(m):
        rest = m.group(2).strip()
        return f"> **{m.group(1).capitalize()}**" + (f" — {rest}" if rest else "")
    body = CALLOUT.sub(callout_sub, body)

    hugo_fm = {"title": title, "date": date, "draft": False}
    for k in ("tags", "categories", "description", "summary"):
        if k in fm:
            hugo_fm[k] = fm[k]

    out = ("---\n"
           + yaml.safe_dump(hugo_fm, sort_keys=False, allow_unicode=True)
           + "---\n\n" + body.strip() + "\n")
    (bundle / "index.md").write_text(out, encoding="utf-8")
    return title, slug


def git(*args):
    subprocess.run(["git", "-C", str(BLOG_REPO), *args], check=True)


def main():
    notes = sorted(p for p in PUBLISH_DIR.glob("*.md") if not p.name.startswith("."))
    if not notes:
        return
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)

    slug_map = build_slug_map()                 # know every post's slug up front
    wl_sub   = make_wikilink_sub(slug_map)

    published = []
    for note in notes:
        # settle: wait until the file size stops changing (avoid half-synced files)
        last = -1
        for _ in range(15):
            size = note.stat().st_size
            if size == last:
                break
            last = size
            time.sleep(1)
        try:
            title, slug = process(note, wl_sub)
        except Exception as e:
            print(f"  ! failed {note.name}: {e}", file=sys.stderr)
            continue
        published.append(title)
        shutil.move(str(note), str(PUBLISHED_DIR / note.name))
        print(f"  + {title} -> posts/{slug}")

    if not published:
        return
    git("add", "-A")
    git("commit", "-m", "Publish: " + ", ".join(published))
    git("pull", "--rebase", "origin", GIT_BRANCH)   # avoid non-fast-forward
    git("push", "origin", GIT_BRANCH)


if __name__ == "__main__":
    main()
