import os
from pathlib import Path

# -----------------------------------------
# PATHS
# -----------------------------------------

ROOT = Path(__file__).parent
DOCS_DIR = ROOT / "docs"
VIDEOS_ROOT = DOCS_DIR / "assets" / "videos"

# Repo path en GitHub Pages: /animations
BASE_URL = "/animations"

# Categorías principales
CATEGORIES = [
    ("constitutive-models", "Constitutive Models"),
    ("plaxis", "PLAXIS"),
    ("undergraduate", "Undergraduate"),
]

VIDEO_EXTS = {".mp4", ".webm", ".mov", ".m4v", ".gif"}


# -----------------------------------------
# UTILIDADES
# -----------------------------------------


def slug_from_name(name: str) -> str:
    base = os.path.splitext(name)[0]
    base = base.replace(" ", "-")
    base = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in base)
    while "--" in base:
        base = base.replace("--", "-")
    return base.lower() or "page"


def title_from_name(name: str) -> str:
    base = os.path.splitext(name)[0]
    base = base.replace("_", " ").replace("-", " ")
    return " ".join(w.capitalize() for w in base.split())


def list_video_files(folder: Path):
    if not folder.exists():
        return []
    return sorted(
        [
            f
            for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in VIDEO_EXTS
        ],
        key=lambda x: x.name.lower(),
    )


def list_subfolders(folder: Path):
    if not folder.exists():
        return []
    return sorted(
        [d for d in folder.iterdir() if d.is_dir()], key=lambda x: x.name.lower()
    )


def write_html(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_template(name: str) -> str:
    path = DOCS_DIR / name
    return path.read_text(encoding="utf-8")


# -----------------------------------------
# PÁGINA PRINCIPAL (INDEX)
# -----------------------------------------


def make_index_page():
    template_top = read_template("_template_top.html")
    template_bottom = read_template("_template_bottom.html")

    links = []
    for slug, title in CATEGORIES:
        if (VIDEOS_ROOT / slug).exists():
            links.append(f'<li><a href="{BASE_URL}/{slug}.html">{title}</a></li>')

    links_html = "".join(links)
    body = f"""
<h1>GeomechMotion — Numerical Modelling Animations</h1>
<p>Select a category to explore animations:</p>

<ul>
    {links_html}
</ul>
"""

    full = template_top + body + template_bottom
    write_html(DOCS_DIR / "index.html", full)


# -----------------------------------------
# PÁGINA DE CATEGORÍA
# -----------------------------------------


def make_category_page(cat_slug: str, cat_title: str):
    template_top = read_template("_template_top.html")
    template_bottom = read_template("_template_bottom.html")

    cat_dir = VIDEOS_ROOT / cat_slug
    subfolders = list_subfolders(cat_dir)

    if subfolders:
        items = []
        for sub in subfolders:
            sub_slug = slug_from_name(sub.name)
            sub_title = title_from_name(sub.name)
            items.append(
                f'<li><a href="{BASE_URL}/{cat_slug}/{sub_slug}.html">{sub_title}</a></li>'
            )

        items_html = "".join(items)
        body = f"""
<h1>{cat_title}</h1>

<ul>
    {items_html}
</ul>

<p><a href="{BASE_URL}/index.html">Back to home</a></p>
"""
    else:
        videos = list_video_files(cat_dir)
        blocks = []
        for vid in videos:
            title = title_from_name(vid.name)
            # ruta absoluta para GitHub Pages
            src = f"{BASE_URL}/assets/videos/{cat_slug}/{vid.name}"
            blocks.append(
                f"""
<section>
    <video controls>
        <source src="{src}">
    </video>
    <p>Animation: {title}</p>
</section>
"""
            )

        if not blocks:
            blocks.append("<p>No videos available yet.</p>")

        blocks_html = "".join(blocks)
        body = f"""
<h1>{cat_title}</h1>
{blocks_html}
<p><a href="{BASE_URL}/index.html">Back to home</a></p>
"""

    full = template_top + body + template_bottom
    write_html(DOCS_DIR / f"{cat_slug}.html", full)


# -----------------------------------------
# SUBPÁGINA: SUBCARPETA
# -----------------------------------------


def make_subcategory_page(cat_slug: str, cat_title: str, subfolder: Path):
    template_top = read_template("_template_top.html")
    template_bottom = read_template("_template_bottom.html")

    sub_slug = slug_from_name(subfolder.name)
    sub_title = title_from_name(subfolder.name)

    videos = list_video_files(subfolder)
    blocks = []

    for vid in videos:
        title = title_from_name(vid.name)
        src = f"{BASE_URL}/assets/videos/{cat_slug}/{subfolder.name}/{vid.name}"
        blocks.append(
            f"""
<section>
    <video controls>
        <source src="{src}">
    </video>
    <p>Animation: {title}</p>
</section>
"""
        )

    if not blocks:
        blocks.append("<p>No videos available.</p>")

    blocks_html = "".join(blocks)
    body = f"""
<h1>{sub_title}</h1>
<p>Category: {cat_title}</p>

{blocks_html}

<p>
    <a href="{BASE_URL}/{cat_slug}.html">Back to {cat_title}</a> |
    <a href="{BASE_URL}/index.html">Home</a>
</p>
"""

    out_path = DOCS_DIR / cat_slug / f"{sub_slug}.html"
    full = template_top + body + template_bottom
    write_html(out_path, full)


# -----------------------------------------
# MAIN
# -----------------------------------------


def main():
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating site for", BASE_URL)

    # index
    make_index_page()
    print("✔ docs/index.html")

    # categorías y subcarpetas
    for slug, title in CATEGORIES:
        cat_dir = VIDEOS_ROOT / slug
        if not cat_dir.exists():
            continue

        make_category_page(slug, title)
        print(f"✔ docs/{slug}.html")

        for sub in list_subfolders(cat_dir):
            make_subcategory_page(slug, title, sub)
            print(f"  ✔ docs/{slug}/{slug_from_name(sub.name)}.html")

    print("\n🎉 DONE — Site generated.")


if __name__ == "__main__":
    main()
