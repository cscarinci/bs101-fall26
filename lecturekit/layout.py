"""Page structure (lecture header, sections, modules, opening/closing frames) and figures."""

import html
import sys

import marimo as mo

from . import numbering
from .blocks import _mark, _md, as_html, as_html_all, braces, marks
from .config import setting


class _Html:
    def __init__(self, markup):
        self.markup = markup
        self.new_module = numbering.starts_module()

    def html(self):
        return self.markup

    def _mime_(self):
        return ("text/html", _mark(self) + self.markup)


def lecture(number, title, date=""):
    """Lecture header. The number is also the prefix of every block number (Thm 3.2)."""
    meta = " &middot; ".join(html.escape(x) for x in (setting("code"), f"Lecture {number}", date) if x)
    return _Html(
        f'<header class="lk-lecture"><div class="lk-meta">{meta}</div>'
        f'<h1 class="lk-lecture-title">{_inline(title) if "$" in title else html.escape(title)}</h1></header>'
    )


def section(title, label=None):
    """A section heading, unnumbered."""
    numbering.claim("section")
    anchor = f' id="lk-{html.escape(label)}"' if label else ""
    text = _inline(title) if "$" in title else html.escape(title)  # a title may hold mathematics: "on $(M,g)$"
    return _Html(f'<h2 class="lk-section"{anchor}>{text}</h2>')


def module(*items, title=""):
    """A unit of a section: a sequence of blocks, text and figures that is moved around as one cell."""
    head = f'<h3 class="lk-module-title">{html.escape(title)}</h3>' if title else ""
    return _Html(f'<section class="lk-module">{head}{as_html_all(items)}</section>')


def _frame(kind, heading, items):
    return _Html(
        f'<aside class="lk-frame lk-{kind}"><div class="lk-frame-head">{html.escape(heading)}</div>'
        f'{as_html_all(items)}</aside>'
    )


class _Under:
    """The lines under a heading line (e.g. a recap's topic), one level in: lk.under(...)."""

    def __init__(self, items):
        self.items = items

    def html(self):
        return f'<div class="lk-under">{as_html_all(self.items)}</div>'


def under(*items):
    """Items one level in, under the heading line before them (e.g. a second topic in a recap)."""
    return _Under(items)


def recap(*items, title="Last time", topic=None):
    """What last time covered. With `topic`, the topic is the heading line and every item sits one level under it."""
    if topic is not None:
        items = (topic, _Under(items))
    return _frame("recap", title, items)


def goals(*items, title="Goals"):
    return _frame("goals", title, items)


def references(text, title="References"):
    """The references of the lecture: a one-line frame after the goals, its name in the left margin."""
    return _frame("refs", title, (text,))


def summary(*items, title="Summary"):
    return _frame("summary", title, items)


def figure(content, caption="", label=None, width=None):
    """A numbered figure: a matplotlib figure, an image, or any marimo output."""
    number = numbering.claim("figure")
    return _figure(content, caption, label, number, width)


def interactive(content, controls=(), readout=None, caption="", label=None):
    """A numbered figure with one row under it: its controls (sliders, ...) and a readout (e.g. lk.table) side by side.
    `content` may be a list."""
    number = numbering.claim("interactive")
    row = [mo.as_html(c).text for c in controls] + ([as_html(readout)] if readout is not None else [])
    parts = content if isinstance(content, (list, tuple)) else [content]
    body = "".join(as_html(p) for p in parts) + (f'<div class="lk-controls">{"".join(f"<div>{r}</div>" for r in row)}</div>' if row else "")
    return _figure(_Html(body), caption, label, number, None, extra="lk-interactive", live=True)


def _figure(content, caption, label, number, width, extra="", live=False):
    anchor = f' id="lk-{html.escape(label)}"' if label else ""
    # On the website the page first shows a snapshot made at build time; once Python runs in the
    # browser the figure is redrawn with this mark, which hides the "loading" note (style.css).
    if live:
        anchor += f' data-lk-runtime="{sys.platform}"'
    style = f' style="--lk-figure-width:{width}"' if width else ""
    name = f'<span class="lk-label">Fig {number}</span> ' if number else ""
    cap = f'<figcaption>{name}{_md(caption)}</figcaption>' if caption or number else ""
    return _Html(f'<figure class="lk-figure {extra}"{anchor}{style}>{as_html(content)}{cap}</figure>')


def side(left, right):
    """Two columns, e.g. a few lines of text and the figure they describe, side by side. Wraps on narrow screens."""
    return _Html(f'<div class="lk-side"><div>{as_html(left)}</div><div>{as_html(right)}</div></div>')


def gap():
    """Extra space between two parts of one block (e.g. the second field of an example), as between modules."""
    return _Html('<div class="lk-gap" aria-hidden="true"></div>')


def maps(*parts):
    r"""Figures in a row joined by the maps between them, each arrow centred between its two figures:
    lk.maps(fig_D, r"\Phi", fig_S, "f", r"$\mathbb{R}$"). The parts in between are the names of the maps (TeX);
    a figure may also be a short piece of text. On phones the row becomes a column."""
    cells = []
    for i, part in enumerate(parts):
        if i % 2:
            cells.append(f'<div class="lk-map">{_inline(rf"$\xrightarrow{{\quad {part} \quad}}$")}</div>')
        else:
            cells.append(f'<div class="lk-map-item">{_inline(part) if isinstance(part, str) else as_html(part)}</div>')
    return _Html(f'<div class="lk-maps">{"".join(cells)}</div>')


def chain(*parts):
    """Equal things stacked, joined by a turned "=", e.g.
    lk.chain("parameterized surface", "parameterization of a surface"). Never needs a line break."""
    sep = '<div class="lk-chain-sep">' + _inline(r"$\shortparallel$") + "</div>"
    return _Html('<div class="lk-chain">' + sep.join(f"<div>{_inline(p)}</div>" for p in parts) + "</div>")


def _inline(text):
    """Markdown for a piece of a line, without the paragraph wrapper."""
    html = mo.md(braces(marks(text))).text
    return html.replace('<span class="paragraph">', "<span>")


def table(rows):
    """A small readout table: rows of (label, value) Markdown strings, e.g. under a slider."""
    md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
    return _Html(f'<div class="lk-table">{md.text}</div>')


def slider(start=None, stop=None, step=None, value=None, label="", steps=None, show_value=True):
    """A slider in the course style (value shown, full label in LaTeX if wanted). `steps`: its values, instead of
    start, stop and step; with show_value=False the figure shows the value itself, e.g. as a multiple of pi."""
    if steps is not None:
        return mo.ui.slider(steps=steps, value=value, label=label, show_value=show_value)
    return mo.ui.slider(start, stop, step=step, value=value, label=label, show_value=show_value)
