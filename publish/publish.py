#!/usr/bin/env python3
"""Publish Obsidian notes from the vault's blog/Publish folder to a Hugo blog."""
import re, sys, time, shutil, subprocess, datetime, pathlib
from zoneinfo import ZoneInfo

# ---- config ---------------------------------------------------------------
VAULT_ROOT    = pathlib.Path("/home/chris/Notes")
PUBLISH_DIR   = VAULT_ROOT / "blog" / "Publish"
PUBLISHED_DIR = VAULT_ROOT / "blog" / "Published"
BLOG_REPO     = pathlib.Path("/home/chris/blog")
CONTENT_DIR   = BLOG_REPO / "content" / "posts"
GIT_BRANCH    = "main"
POST_BASE_URL = "/posts"          # Hugo permalink base for content/posts/<slug>/
TIMEZONE      = ZoneInfo("America/New_York")   # for dates derived from file mtime
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


def _scalar(s):
    """Strip surrounding quotes from a frontmatter scalar; everything is a str."""
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _split_inline(s):
    """Split an inline list body (`a, "b, c", d`) on top-level commas."""
    out, cur, quote = [], "", None
    for ch in s:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            cur += ch
        elif ch == ",":
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x for x in out if x.strip()]


def split_frontmatter(text):
    """Parse a note's YAML-ish frontmatter without a third-party YAML library.

    Obsidian frontmatter is simple key/value with string scalars and tag/category
    lists (inline `[a, b]` or block `- item`), which is all we need to read here.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text

    fm, key = {}, None
    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-"):                       # block list item
            item = stripped[1:].strip()
            if key is not None and item:
                fm.setdefault(key, [])
                if isinstance(fm[key], list):
                    fm[key].append(_scalar(item))
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v == "":                                        # opens a block list
            fm[k], key = [], k
        elif v.startswith("[") and v.endswith("]"):        # inline list
            inner = v[1:-1].strip()
            fm[k] = [_scalar(x) for x in _split_inline(inner)] if inner else []
            key = None
        else:
            fm[k] = _scalar(v)
            key = None

    body = "\n".join(lines[end + 1:]).lstrip("\n")
    return fm, body


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


def _toml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_toml_frontmatter(fm):
    """Render Hugo's TOML (`+++`) frontmatter for our fixed set of fields."""
    lines = [
        f"title = {_toml_str(fm['title'])}",
        f"date = {_toml_str(fm['date'])}",
        f"draft = {'true' if fm['draft'] else 'false'}",
    ]
    for k in ("tags", "categories"):
        if k in fm:
            vals = fm[k] if isinstance(fm[k], list) else [fm[k]]
            lines.append(f"{k} = [{', '.join(_toml_str(v) for v in vals)}]")
    for k in ("description", "summary"):
        if k in fm:
            lines.append(f"{k} = {_toml_str(fm[k])}")
    return "\n".join(lines) + "\n"


def process(note_path, wl_sub):
    fm, body = split_frontmatter(note_path.read_text(encoding="utf-8"))

    title = fm.get("title") or note_path.stem
    slug  = fm.get("slug") or slugify(title)
    date  = fm.get("date") or datetime.datetime.fromtimestamp(
        note_path.stat().st_mtime, TIMEZONE).replace(microsecond=0).isoformat()

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

    out = ("+++\n" + render_toml_frontmatter(hugo_fm)
           + "+++\n\n" + body.strip() + "\n")
    (bundle / "index.md").write_text(out, encoding="utf-8")
    return title, slug


def git(*args):
    subprocess.run(["git", "-C", str(BLOG_REPO), *args], check=True)


def has_staged_changes():
    # `git diff --cached --quiet` exits 1 when there is something staged
    return subprocess.run(
        ["git", "-C", str(BLOG_REPO), "diff", "--cached", "--quiet"]
    ).returncode != 0


def main():
    notes = sorted(p for p in PUBLISH_DIR.glob("*.md") if not p.name.startswith("."))
    if not notes:
        return
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)

    slug_map = build_slug_map()                 # know every post's slug up front
    wl_sub   = make_wikilink_sub(slug_map)

    processed = []
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
        processed.append((note, title, slug))

    if not processed:
        return

    # Commit & push first; only archive notes once the push has landed. A failure
    # here raises before the move, so the notes stay in Publish/ and get retried.
    git("add", str(CONTENT_DIR))
    if has_staged_changes():
        titles = ", ".join(title for _, title, _ in processed)
        git("commit", "-m", "Publish: " + titles)
    git("pull", "--rebase", "origin", GIT_BRANCH)   # avoid non-fast-forward;
    git("push", "origin", GIT_BRANCH)               # also flushes prior commits

    for note, title, slug in processed:
        shutil.move(str(note), str(PUBLISHED_DIR / note.name))
        print(f"  + {title} -> posts/{slug}")


if __name__ == "__main__":
    main()
