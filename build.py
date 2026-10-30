"""Build the BS101 course site: one browser-run page per lecture, plus an index.

Usage:  python build.py        (writes ./site)
Preview: python -m http.server --directory site
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SITE = HERE / "site"

PARTS = [  # (name, first lecture, last lecture)
    ("I. Euclidean Geometry", 1, 5),
    ("II. Differentiation", 6, 13),
    ("III. Applications to Optimization", 14, 16),
    ("IV. Vector fields and line integrals", 17, 19),
    ("V. Multiple integrals", 20, 22),
    ("VI. Surface integrals, Stokes and Gauss", 23, 27),
]

TITLES = {  # lecture number -> title shown on the index
    1: "The Cartesian n-space",
    2: "The Euclidean inner product (the dot product)",
    3: "Matrices, linear transformations, and determinants",
    4: "Determinants, areas and volumes",
    5: "Lines and planes and the cross-product in R³",
    6: "Multivariable functions",
    7: "Local properties of paths",
    8: "Local properties of scalar functions and maps: limits",
    9: "Differentiability and the derivative",
    10: "Properties and interpretations of differentiable functions",
    11: "Affine approximations and the derivative of general maps",
    12: "The chain rule",
    13: "Higher order derivatives",
    14: "Local extrema and the second derivative test",
    15: "Global extrema on closed and bounded domains",
    16: "Method of Lagrange multipliers",
    17: "Differentiation of vector fields",
}

DRAFTS = set()  # lectures kept in the repo but not published

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BS101 Multivariable Calculus</title>
<style>
  body {{ font-family: "Latin Modern Roman", "CMU Serif", Georgia, serif; color: #111; background: #fff;
         max-width: 46rem; margin: 0 auto; padding: 2rem 1rem; font-size: 1.1rem; line-height: 1.5; }}
  .title {{ color: #1b458f; font-weight: 700; font-size: 1.9rem; text-align: center; margin: 1rem 0 .3rem; }}
  .inst {{ color: #1b458f; text-align: center; font-size: 1.2rem; }}
  .meta {{ display: grid; grid-template-columns: auto 1fr auto 1fr; gap: .5rem 1.5rem; margin: 2rem 0;
          padding: 1rem 1.2rem; text-align: right; border-top: 1px solid #1b458f; border-bottom: 1px solid #1b458f; }}
  .meta b {{ text-align: left; }}
  @media (max-width: 600px) {{ .meta {{ grid-template-columns: auto 1fr; }} }}
  h2 {{ font-size: 1.2rem; margin: 1.8rem 0 .4rem; }}
  ul {{ list-style: none; padding: 0; margin: 0; }}
  li {{ padding: .15rem 0; }}
  a {{ color: #1b458f; }}
  .none {{ opacity: .55; font-style: italic; }}
  .license {{ margin-top: 3rem; font-size: .9rem; opacity: .7; }}
</style></head><body>
<div class="title">Multivariable Calculus</div>
<div class="inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
<div class="meta"><b>Document</b><span>Lecture notes</span><b>Course</b><span>BS101-04/05</span>
<b>Lectures</b><span>{count} available</span><b>Instructor</b><span>Professor Scarinci</span></div>
{parts}
<p class="license">&copy; 2026 Carlos Scarinci &middot; <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a> &middot; <a href="https://github.com/cscarinci/bs101-fall26">GitHub</a></p>
</body></html>
"""


NAV_CSS = """<style>
  .bs-nav { position: fixed; left: 1.1rem; bottom: 1.1rem; z-index: 50; display: flex; gap: .35rem;
             font-family: "KaTeX_Main", "Latin Modern Roman", "CMU Serif", Georgia, serif; font-size: .9rem; }
  .bs-nav a { color: #1b458f; text-decoration: none; opacity: .75; padding: .25rem .55rem; border-radius: .3rem;
               background: rgba(255,255,255,.85); border: 1px solid rgba(27,69,143,.25); transition: opacity .15s; }
  .bs-nav a:hover, .bs-nav a:focus-visible { opacity: 1; }
  .bs-nav a:focus-visible { outline: 2px solid #1b458f; outline-offset: 2px; }
  #root { padding-bottom: 3.5rem; }
  .bs-ask { position: fixed; right: 16px; bottom: 16px; z-index: 50; color: #1b458f; text-decoration: none; opacity: .75;
             padding: 3.5px 8px; border-radius: 4.5px; background: rgba(255,255,255,.85); border: 1px solid rgba(27,69,143,.25);
             display: inline-flex; align-items: center; transition: opacity .15s; }
  .bs-ask svg { width: 18px; height: 19.5px; }  /* px, not rem: the same size on the index and in the lectures */
  .bs-ask:hover, .bs-ask:focus-visible { opacity: 1; }
  .bs-ask:focus-visible { outline: 2px solid #1b458f; outline-offset: 2px; }
  @media print { .bs-nav, .bs-ask { display: none; } }
  @media (max-width: 1000px) {  /* narrow screens: a bottom bar instead of floating buttons */
    .bs-nav { left: 0; right: 0; bottom: 0; justify-content: center; padding: .35rem; background: #fff;
               border-top: 1px solid rgba(27,69,143,.25); }
    .bs-nav a { border: none; background: none; }
    .bs-nav:has(~ .bs-ask) { justify-content: flex-start; }
    .bs-nav ~ .bs-ask { right: 9px; bottom: 5px; z-index: 51; border: none; background: none; }
    #root { padding-bottom: 4rem; }
  }
</style>"""


def nav_html(number, numbers):
    """Subtle previous / index / next links for the page of lecture `number`."""
    links = []
    if number - 1 in numbers:
        links.append(f'<a href="../Lecture_{number - 1:02d}/" title="Lecture {number - 1:02d}">&larr; {number - 1:02d}</a>')
    links.append('<a href="../" title="All lectures">Index</a>')
    if number + 1 in numbers:
        links.append(f'<a href="../Lecture_{number + 1:02d}/" title="Lecture {number + 1:02d}">{number + 1:02d} &rarr;</a>')
    return NAV_CSS + '<nav class="bs-nav">' + "".join(links) + "</nav>" + ask_html()


BUBBLE = (  # outline speech bubble, drawn in the link colour
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M4 5.5h16a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1h-9l-4.5 3.5v-3.5H4a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1z"/></svg>'
)


def ask_html():
    """Bottom-right icon button linking to the questions and comments form."""
    if not QUESTIONS:
        return ""
    return f'<a class="bs-ask" href="{QUESTIONS}" target="_blank" rel="noopener" title="{ASK_TEXT}" aria-label="{ASK_TEXT}">{BUBBLE}</a>'


# python build.py --snapshot: run each notebook during the build and embed its outputs, so the page shows
# the header and figures at once while the browser is still loading Python (needs numpy and matplotlib)
SNAPSHOT = ["--execute", "--no-sandbox"] if "--snapshot" in sys.argv else []

# page-view counting with GoatCounter (goatcounter.com): the site code chosen at sign-up; "" turns it off
GOATCOUNTER = "cscarinci"

# share link of the course's Microsoft Forms form for questions and comments; "" hides the links to it
QUESTIONS = (
    "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=LRqY0sLhfEau6kPCST8vRN-nk1Q9k4xFlhx6m6mvuZJUQk5JUE8wN1hHSzJRVEtZWkhPWVlFTFZLTi4u&r703d5ae20f8c4e00ab89e285392ca2b6="
    "%22BS101%20-%20Multivariable%20Calculus%22"
)
ASK_TEXT = "Questions, comments, or suggestions?"
COUNTER = (
    f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    if GOATCOUNTER
    else ""
)


def main():
    notebooks = {}
    for path in sorted(HERE.glob("W*_Lecture_*.py")):
        number = int(re.search(r"Lecture_(\d+)", path.stem).group(1))
        if number not in DRAFTS:
            notebooks[number] = path

    for number, path in notebooks.items():
        print(f"exporting {path.name}")
        subprocess.run(
            ["marimo", "export", "html-wasm", str(path), "-o", str(SITE / f"Lecture_{number:02d}"), "--mode", "run", "-f", *SNAPSHOT],
            check=True,
            cwd=HERE,
        )

    for number in notebooks:  # previous / next navigation, injected into each exported page
        page = SITE / f"Lecture_{number:02d}" / "index.html"
        html = re.sub(r'<nav class="bs-nav">.*?</nav>(<a class="bs-ask".*?</a>)?', "", page.read_text(encoding="utf-8"), flags=re.S)
        html = html.replace("</body>", nav_html(number, notebooks) + "</body>", 1)
        html = re.sub(r"<script data-goatcounter=.*?</script>", "", html, flags=re.S).replace("</head>", COUNTER + "</head>", 1)
        page.write_text(html, encoding="utf-8")

    covered = {n for _, first, last in PARTS for n in range(first, last + 1)}
    for number in sorted(set(notebooks) - covered):
        print(f"warning: lecture {number:02d} is outside every part in PARTS and will not appear on the index")

    sections = []
    for name, first, last in PARTS:
        items = [
            f'<li><a href="Lecture_{n:02d}/">Lecture {n:02d}</a> &mdash; {TITLES.get(n, "")}</li>'
            for n in range(first, last + 1)
            if n in notebooks
        ]
        body = "<ul>" + "".join(items) + "</ul>" if items else '<div class="none">not yet available</div>'
        sections.append(f"<h2>{name}</h2>{body}")

    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(PAGE.format(count=len(notebooks), parts="\n".join(sections)).replace("</body>", NAV_CSS + ask_html() + "</body>", 1).replace("</head>", COUNTER + "</head>", 1), encoding="utf-8")
    (SITE / ".nojekyll").write_text("")
    print(f"wrote {SITE / 'index.html'}")


if __name__ == "__main__":
    main()
