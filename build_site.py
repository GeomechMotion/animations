
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

MODEL_ORDER = [
    "mc",
    "hss",
    "camclay",
    "norsand",
    "pm4sand",
    "pm4silt",
    "sclay1s",
]

MODEL_NAMES = {
    "mc": "Mohr-Coulomb",
    "hss": "HS-Small",
    "camclay": "Cam-Clay",
    "norsand": "NorSand",
    "pm4sand": "PM4Sand",
    "pm4silt": "PM4Silt",
    "sclay1s": "Creep S-CLAY1S",
}

MODEL_DESCRIPTIONS = {
    "mc": "A linear-elastic perfectly-plastic model.",
    "hss": "A non-linear elastoplastic model with isotropic hardening.",
    "camclay": "A classic critical-state model for clays.",
    "norsand": "A critical-state model for sands.",
    "pm4sand": "A plasticity model for earthquake engineering applications in sands.",
    "pm4silt": "A plasticity model for earthquake engineering applications in silts.",
    "sclay1s": "A viscoplastic anisotropic model for soft soils.",
}


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

    descriptions = {
        "constitutive-models": "Animations illustrating the behavior of different soil constitutive models, focusing on visualizing the complex stress-strain relationships.",
        "plaxis": "Analyses performed with PLAXIS, a leading geotechnical finite element software. See how meshes are generated and deform under different load scenarios.",
        "undergraduate": "A set of animations for undergraduate students, simplifying fundamental geotechnical concepts to make them more accessible.",
    }

    links = []
    for slug, title in CATEGORIES:
        if (VIDEOS_ROOT / slug).exists():
            desc = descriptions.get(slug, "")
            links.append(
                f'''<li><a href="{BASE_URL}/{slug}.html">{title}</a> - {desc}</li>'''
            )

    links.append(
        "<li><b>FLAC (WIP)</b> - Animations made with FLAC are a work in progress. Stay tuned for future updates!</li>"
    )

    links_html = "\n".join(links)
    video_src = f"{BASE_URL}/assets/videos/Load_intro.mp4"
    caption_text = "Pore pressure (top) and magnitude of displacements (bottom) under a load application in the HS-Small model."
    body = f'''
    <div style="background-color: #d4edda; border-color: #c3e6cb; color: #155724; padding: .75rem 1.25rem; margin-bottom: 1rem; border: 1px solid transparent; border-radius: .25rem;">
        The animations presented here were created quickly for conferences and educational purposes, and therefore may contain errors or inaccuracies. If you find one, please don't hesitate to email ntasso@fi.uba.ar.
    </div>

    <div class="flex-container" style="display: flex; align-items: flex-start; gap: 2rem;">
        <div style="flex: 1;">
            <p>This collection of animations has been developed for graduate courses, such as 'Numerical Geotechnics I and II', and for various conferences. The purpose of these short videos is to explain complex topics in geomechanics and numerical modeling in a more visual and intuitive way.</p>
            <p>These animations are intended for educational purposes and are freely available. You are encouraged to use them in your teaching, presentations, or other academic work if you find them helpful for illustrating these concepts.</p>
            
            <p>For more animations and resources on constitutive models, be sure to check out <a href="https://soilmodels.com/soilanim/" target="_blank">SoilAnim</a> by the SoilModels team.</p>

            <hr style="border: 0; border-top: 1px solid #ccc; margin: 2rem 0;">

            <p>The animations are grouped into the following categories:</p>

            <ul>
                {links_html}
            </ul>
        </div>
        <div style="flex-shrink: 0; width: 400px;">
            <video src="{video_src}" style="width: 100%; border-radius: 8px;" autoplay muted loop playsinline></video>
            <p style="font-size: 0.9em; font-style: italic; color: #6c757d; text-align: center; margin-top: 0.5em;">{caption_text}</p>
        </div>
    </div>
'''

    full = template_top + body + template_bottom
    write_html(DOCS_DIR / "index.html", full)


# -----------------------------------------
# PÁGINA DE CATEGORÍA
# -----------------------------------------

def make_category_page(cat_slug: str, cat_title: str):
    template_top = read_template("_template_top.html")
    template_bottom = read_template("_template_bottom.html")

    cat_dir = VIDEOS_ROOT / cat_slug
    body = f"<h1>{cat_title}</h1>"

    if cat_slug == "constitutive-models":
        video_src = f"{BASE_URL}/assets/videos/ConstModel_intro.mp4"
        caption_text = "Yield surface evolution for different constitutive models under a triaxial stress path."
        
        items = []
        for model_slug in MODEL_ORDER:
            sub_slug = slug_from_name(model_slug)
            sub_title = MODEL_NAMES.get(model_slug.lower())
            sub_desc = MODEL_DESCRIPTIONS.get(model_slug.lower())
            
            if sub_title and sub_desc:
                link = f'<a href="{BASE_URL}/{cat_slug}/{sub_slug}.html">{sub_title}</a>'
                items.append(f"<li>{link} - {sub_desc}</li>")

        items_html = "\n".join(items)
        body += f'''
        <p>In this section, you will find videos intended to explain how different constitutive models work. The available models are:</p>
        <div class="flex-container" style="display: flex; align-items: flex-start; gap: 2rem;">
            <div style="flex: 1;">
                <ul>
                    {items_html}
                </ul>
            </div>
            <div style="flex-shrink: 0; width: 400px;">
                <video src="{video_src}" style="width: 100%; border-radius: 8px;" autoplay muted loop playsinline></video>
                <p style="font-size: 0.9em; font-style: italic; color: #6c757d; text-align: center; margin-top: 0.5em;">{caption_text}</p>
            </div>
        </div>
        '''

    else:
        subfolders = list_subfolders(cat_dir)
        if subfolders:
            items = []
            for sub in subfolders:
                sub_slug = slug_from_name(sub.name)
                sub_title = title_from_name(sub.name)
                items.append(
                    f'''<li><a href="{BASE_URL}/{cat_slug}/{sub_slug}.html">{sub_title}</a></li>'''
                )
            items_html = "".join(items)
            body += f"<ul>{items_html}</ul>"

        else:
            videos = list_video_files(cat_dir)
            blocks = []
            for vid in videos:
                title = title_from_name(vid.name)
                src = f"{BASE_URL}/assets/videos/{cat_slug}/{vid.name}"
                blocks.append(
                    f'''
<section>
    <video controls>
        <source src="{src}">
    </video>
    <p>Animation: {title}</p>
</section>
'''
                )

            if not blocks:
                blocks.append("<p>No videos available yet.</p>")

            blocks_html = "".join(blocks)
            body += blocks_html

    body += f'\n\n<p><a href="{BASE_URL}/index.html">Back to home</a></p>\n'

    full = template_top + body + template_bottom
    write_html(DOCS_DIR / f"{cat_slug}.html", full)


# -----------------------------------------
# SUBPÁGINA: SUBCARPETA
# -----------------------------------------

def make_subcategory_page(cat_slug: str, cat_title: str, subfolder: Path):
    template_top = read_template("_template_top.html")
    template_bottom = read_template("_template_bottom.html")

    sub_slug = slug_from_name(subfolder.name)
    sub_title = MODEL_NAMES.get(subfolder.name.lower(), title_from_name(subfolder.name))
    
    videos = list_video_files(subfolder)
    blocks = []

    mc_captions = {
        "TRX CIDC - MC model.mp4": "Stress path for a Consolidated Isotropically Drained Compression (CIDC) triaxial test, shown in the p-q plane (top left), q-εa plane (top right), deviatoric plane (bottom left), and Mohr's circles (bottom right).",
        "TRX CIUC - MC model.mp4": "Stress path for a Consolidated Isotropically Undrained Compression (CIUC) triaxial test, shown in the p-q plane (top left), q-εa plane (top right), deviatoric plane (bottom left), and Mohr's circles (bottom right)."
    }

    for vid in videos:
        src = f"{BASE_URL}/assets/videos/{cat_slug}/{subfolder.name}/{vid.name}"
        
        video_style = "width: 70%; border-radius: 8px; margin-left: auto; margin-right: auto; display: block;"
        caption_wrapper_style = "width: 70%; margin: auto;"
        caption_p_style = "font-size: 0.9em; font-style: italic; color: #6c757d; text-align: center; margin-top: 0.5em;"
        caption_text = title_from_name(vid.name)

        if cat_slug == "constitutive-models" and sub_slug == "mc":
            caption_text = mc_captions.get(vid.name, caption_text)

        caption_tag = f'''
<div style="{caption_wrapper_style}">
    <p style="{caption_p_style}">{caption_text}</p>
</div>
'''

        blocks.append(
            f'''
<section style="margin-bottom: 2rem;">
    <video controls style="{video_style}">
        <source src="{src}">
    </video>
    {caption_tag}
</section>
'''
        )

    if not blocks:
        blocks.append("<p>No videos available.</p>")

    blocks_html = "".join(blocks)
    
    page_description = ""
    if cat_slug == "constitutive-models":
        description = MODEL_DESCRIPTIONS.get(sub_slug)
        if description:
            page_description = f"<p>{description}</p>"

    body = f'''
<h1>{sub_title}</h1>
{page_description}

{blocks_html}

<p>
    <a href="{BASE_URL}/{cat_slug}.html">Back to {cat_title}</a> |
    <a href="{BASE_URL}/index.html">Home</a>
</p>
'''

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
