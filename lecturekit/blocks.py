"""Elementary blocks: definition, theorem, proof, example, exercise, solution, ..."""

import html
import re
import textwrap

import marimo as mo

from . import numbering
from .config import setting
from .kinds import KINDS


def _name(kind):
    _, full, short = KINDS[kind]
    return short if setting("labels") == "short" else full


_THEN = re.compile(r'<span class="paragraph">(?=\s*(?:<span class="lk-ghost">)?<marimo-tex[^>]*>\|\|\(\\(?:leadsto|Longrightarrow)\|\|\))')

_ARROW = r'(<marimo-tex[^>]*>\|\|\(\\(?:leadsto|Longrightarrow)\|\|\)</marimo-tex>)(?:\s|&nbsp;|\xa0)*'
_AFTER_GHOST = re.compile(r'(<span class="lk-ghost">(?:(?!</span>).)*</span>)' + _ARROW, re.S)
_LEADING = re.compile(r'((?:lk-then|lk-ghost)">\s*)' + _ARROW)

# a ghost line wraps under its own text: ghost, arrow and the rest side by side
_GHOSTED = re.compile(r'<span class="paragraph lk-then">(<span class="lk-ghost">.*?</span><span class="lk-arrow">.*?</span>)((?:(?!<span|</span>).)*)</span>', re.S)


def _arrows(markup):
    """A line that starts with an arrow (⇝ or ⟹) keeps its arrow at the margin, the text hangs after it.
    Each ">" in front of a line in the source moves it under the text of the line above, e.g. "> $\\leadsto$ ..." follows from the line above.
    To line an arrow up under a later arrow of the line above, put the start of that line in front of it,
    hidden: <span class="lk-ghost">$\\leadsto$ &nbsp; $z=2$ &nbsp;</span>$\\Longrightarrow$ ..."""
    markup = _THEN.sub('<span class="paragraph lk-then">', markup)
    markup = _AFTER_GHOST.sub(r'\1<span class="lk-arrow">\2</span>', markup)
    markup = _LEADING.sub(r'\1<span class="lk-arrow">\2</span>', markup)
    return _GHOSTED.sub(r'<span class="paragraph lk-then lk-ghosted">\1<span class="lk-rest">\2</span></span>', markup)


_DISPLAY = re.compile(r'(<marimo-tex[^>]*>\|\|\[.*?\|\|\]</marimo-tex>)', re.S)


def _group(text, k):
    """The {...} group or single token starting at text[k] (after spaces): (inside, end index)."""
    while text[k] in " \n\t":
        k += 1
    if text[k] != "{":
        if text[k] == "\\":
            m = re.match(r"\\[A-Za-z]+|\\.", text[k:])
            return m.group(0), k + len(m.group(0))
        return text[k], k + 1
    j, depth = k + 1, 1
    while depth:
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        j += 1
    return text[k + 1 : j - 1], j


_BRACE = re.compile(r"\\(underbrace|overbrace)(?![A-Za-z])")


def _short(base):
    """A part about one symbol wide (θ, 5, σ²): fewer than three visible characters."""
    if re.search(r"\\(frac|sum|int|prod|left|begin)", base):
        return False
    visible = re.sub(r"\\(mathrm|mathbf|mathcal|vec|hat|bar|tilde)\b", "", base)
    visible = re.sub(r"\\[A-Za-z]+", "x", visible)
    return len(re.sub(r"[{}^_\s]", "", visible)) < 3


def braces(text):
    r"""A brace never changes the spacing of a formula. KaTeX draws a brace at least
    about one em wide, and its label adds width too, so a short part (θ, 5, σ²) gets pushed apart. Every
    \underbrace{B}_{L} / \overbrace{B}^{L} is drawn over a phantom copy of B, centred on B and taking no room;
    the formula keeps exactly the width of B."""
    out, i = [], 0
    while True:
        m = _BRACE.search(text, i)
        if not m:
            return "".join(out) + text[i:]
        base, k = _group(text, m.end())
        script = "_" if m.group(1) == "underbrace" else "^"
        j = k
        while j < len(text) and text[j] in " \n\t":
            j += 1
        label = None
        if j < len(text) and text[j] == script:
            label, k = _group(text, j + 1)
        base = braces(base)
        if label is not None and _short(base):
            # KaTeX draws a brace about two em wide at least: under a single symbol it would run over its
            # neighbours. A short straight arrow points at the symbol instead.
            if script == "_":
                brace = rf"\underset{{\begin{{array}}{{c}}\uparrow\\[2pt]{braces(label)}\end{{array}}}}{{\phantom{{{base}}}\vphantom{{(}}}}"
            else:
                brace = rf"\overset{{\begin{{array}}{{c}}{braces(label)}\\[2pt]\downarrow\end{{array}}}}{{\phantom{{{base}}}}}"
        else:
            brace = rf"\{m.group(1)}{{\phantom{{{base}}}}}" + (rf"{script}{{{braces(label)}}}" if label is not None else "")
        out.append(text[i : m.start()] + rf"{{\mathrlap{{{base}}}\mathclap{{\hphantom{{{base}}}\mathclap{{{brace}}}}}\hphantom{{{base}}}}}")
        i = k


def marks(text):
    r"""\mk{...} (inside math) names what a margin comment refers to. Symbols are not underlined;
    words are marked with <span class='lk-mark'>...</span>."""
    out, i = [], 0
    while True:
        j = text.find(r"\mk{", i)
        if j < 0:
            return "".join(out) + text[i:]
        k, depth = j + 4, 1
        while depth:
            depth += {"{": 1, "}": -1}.get(text[k], 0)
            k += 1
        body = text[j + 4 : k - 1]
        out.append(text[i:j] + "{" + body + "}")
        i = k


def _md(text):
    """Markdown to HTML, with consequence lines (starting with ⇝ or ⟹) indented.
    Each display ($$ ... $$) is wrapped in div.lk-display, so the stylesheet can place it (KaTeX draws inside a shadow root)."""
    return _DISPLAY.sub(r'<div class="lk-display">\1</div>', _arrows(mo.md(braces(marks(textwrap.dedent(text).strip()))).text))


def _mark(item):
    """Extra space above the first output of a new module (see numbering.starts_module)."""
    return '<div class="lk-module-start" aria-hidden="true"></div>' if getattr(item, "new_module", False) else ""


def as_html_all(items):
    """The items one after another; consecutive asides share one grid, so their comments line up in one column."""
    out, run = [], []
    for item in list(items) + [None]:
        if isinstance(item, _Aside):
            run.append(item.html())
            continue
        if run:
            out.append('<div class="lk-asides">' + "".join(run) + "</div>")
            run = []
        if item is not None:
            out.append(as_html(item))
    return "".join(out)


def as_html(item):
    if hasattr(item, "html"):
        return item.html()
    if isinstance(item, str):
        return f'<div class="lk-prose">{_md(item)}</div>'
    return mo.as_html(item).text


class Block:
    def __init__(self, kind, body, title="", label=None, collapsed=None, of=None):
        self.kind, self.cls, self.name = kind, KINDS[kind][0], KINDS[kind][1]
        self.body, self.title, self.label, self.of = body, title, label, of
        self.collapsed = collapsed
        self.number = numbering.claim(kind)
        self.new_module = numbering.starts_module()

    def heading(self):
        name, number = _name(self.kind), self.number
        if self.kind == "solution" and self.of:
            number = numbering.lookup(self.of)[1]
        number = f" {number}" if number else ""
        return f'<span class="lk-label">{html.escape(name)}{number}</span>'

    def content(self):
        parts = list(self.body) if isinstance(self.body, (list, tuple)) else [self.body]
        if self.cls == "argument" and isinstance(parts[-1], _Aside) and isinstance(parts[-1].content, str) and parts[-1].content.rstrip().endswith("$$"):
            # the argument ends with a display that has a margin comment: the end mark sits at the right end of the
            # display's line, never in the comment column
            if r"\square" not in parts[-1].content:
                return self._titled(_end_mark(as_html_all(parts), aside=True))
            return self._titled(as_html_all(parts))
        if self.cls == "argument" and isinstance(parts[-1], str) and parts[-1].rstrip().endswith("$$"):
            # the argument ends with a display: the end mark sits at the right end of the display's line
            last = parts[-1].rstrip()
            close = re.search(r"\n([ \t>]*)\$\$$", last)  # the closing $$ on its own line, with its indentation (and "> " levels)
            multi = close and "\\\\" in last
            if multi:
                # a display of several lines: the end mark goes level with its last line (a \\tag would sit in its middle)
                return self._titled(_end_mark(as_html_all(parts)))
            if close:
                parts[-1] = last[: close.start()] + r" \tag*{$\square$}" + "\n" + close.group(1) + "$$"
            else:
                parts[-1] = last[:-2] + r" \tag*{$\square$}$$"
            return self._titled(as_html_all(parts))
        body = as_html_all(parts)
        if self.cls == "argument":
            # the end mark goes at the end of the last line of text (never into a margin comment of an earlier part)
            qed = '<span class="lk-qed">&#9633;</span>'
            last = as_html(parts[-1])
            if not body.endswith(last):
                last = body
            head = body[: len(body) - len(last)]
            note = last.rfind('<div class="lk-aside-note')
            # the last line has a margin comment: the mark goes at the end of the line itself, not into the comment
            if isinstance(parts[-1], _Aside) and note >= 0:
                end = last.rfind("</span>", 0, last.rfind("</span>", 0, note))  # the close of the line's paragraph
            else:
                end = _paragraph_end(last)
            body = head + (last[:end] + qed + last[end:] if end >= 0 else last + qed)
        return self._titled(body)

    def _titled(self, body):
        if self.title:
            body = f'<div class="lk-title">({_md(self.title)})</div>' + body
        return body

    def _drop(self):
        """When the block opens with a display holding a column vector, its first baseline sits half the vector lower;
        the label moves down with it, so it stays level with the first line."""
        first = (self.body if isinstance(self.body, (list, tuple)) else [self.body])[0]
        text = first.content if isinstance(first, _Aside) else first
        if self.title or not isinstance(text, str) or not text.strip().startswith("$$"):
            return ""
        display = text.strip()[2:].split("$$")[0]
        rows = [m.count(r"\\") + 1 for m in re.findall(r"\\begin\{[bp]matrix\}(.*?)\\end\{[bp]matrix\}", display, re.S)]
        if not rows or max(rows) < 2:
            return ""
        return f' style="--lk-drop: {0.6 * (max(rows) - 1):.2f}em"'

    def html(self):
        css = f"lk-block lk-{self.cls} lk-{self.kind}"
        anchor = f' id="lk-{html.escape(self.label)}"' if self.label else ""
        if self.collapsed:
            return (
                f'<details class="{css}"{anchor}><summary class="lk-head"{self._drop()}>{self.heading()}</summary>'
                f'<div class="lk-body">{self.content()}</div></details>'
            )
        return f'<div class="{css}"{anchor}><div class="lk-head"{self._drop()}>{self.heading()}</div><div class="lk-body">{self.content()}</div></div>'

    def _mime_(self):
        return ("text/html", _mark(self) + self.html())


class Hidden:
    def html(self):
        return ""

    def _mime_(self):
        return ("text/html", "")


def _paragraph_end(html_text):
    """Where the last paragraph of `html_text` closes (the position of its closing </span>), or -1.

    The end mark □ goes there, at the end of the last line of text, also when that line sits in a quote (> ...)."""
    k = html_text.rfind('<span class="paragraph')
    if k < 0:
        return html_text.rfind("</span></span>")
    depth = 0
    for m in re.finditer(r"<span\b|</span>", html_text[k:]):
        depth += 1 if m.group(0) != "</span>" else -1
        if depth == 0:
            return k + m.start()
    return -1


def _end_mark(body, aside=False):
    """Put the end mark □ in the last display of `body`, at its right edge, level with its last line.
    `aside`: the display has a margin comment after it, so the mark goes inside the display, not after the comment."""
    k = body.rfind('<div class="lk-display">')
    end = body.find("</div>", k) if aside else body.rfind("</div>")
    if k < 0 or end < k:
        return body + '<span class="lk-qed">&#9633;</span>'
    return body[:end] + '<span class="lk-qed lk-qed-end">&#9633;</span>' + body[end:]


def _maker(kind):
    cls = KINDS[kind][0]

    def make(body, title="", label=None, collapsed=None, **kw):
        if cls == "argument" and collapsed is None:
            collapsed = setting("proofs") == "collapsed"
        if cls == "solution":
            mode = setting("solutions")
            if mode == "hidden":
                numbering.claim(kind)
                return Hidden()
            if collapsed is None:
                collapsed = mode == "collapsed"
        return Block(kind, body, title, label, collapsed, **kw)

    make.__name__ = kind
    make.__doc__ = f"{KINDS[kind][1]} block ({cls})."
    return make


for _kind in KINDS:
    globals()[_kind] = _maker(_kind)


def prose(*parts):
    """Running text between blocks: no label, no frame. Several parts (text, lk.side, ...) are stacked."""
    return _Prose(parts)


class _Prose:
    def __init__(self, parts):
        self.parts = parts
        self.new_module = numbering.starts_module()

    def html(self):
        if len(self.parts) == 1 and not isinstance(self.parts[0], _Aside):
            return as_html(self.parts[0])
        return '<div class="lk-prose-group">' + as_html_all(self.parts) + "</div>"

    def _mime_(self):
        return ("text/html", _mark(self) + self.html())


def gloss(text, comment, pen="red"):
    """A floating comment on a word or formula, set in the margin without moving the text.

    Use inside any text: f"... {lk.gloss('$x^2$', 'never negative')} ..."; pen="green" for the second colour.
    """
    return f'<span class="lk-gloss lk-gloss-{pen}">{text}<span class="lk-gloss-note">{comment}</span></span>'


def aside(content, comment, at=None, rows=None):
    """A whole line or display with a comment about it in the margin, level with it (below it on narrower screens).

    lk.aside(r"$$ dA = ... $$", "infinitesimal area element"). For a comment on one word or symbol in a line, use gloss.
    The comment may be text or e.g. lk.chain(...).
    at="last": the comment is about the last line of a computation (one aligned display): level with that line.
    at="middle": about the middle line of a three-line computation.
    at=k, rows=n: about line k (counted from 1; 2.5 is between lines 2 and 3) of an n-line computation.
    Several comments on one computation: comment=[(k, "..."), (k2, "...")] with rows=n, each level with its line."""
    return _Aside(content, comment, at, rows)


def _note(comment):
    """The inside of a margin comment, and whether it was broken by hand into lines."""
    if isinstance(comment, str) and "<br>" in comment:
        # a comment broken by hand: one line each; a line "= ..." (another name) or "⟹ ..." (a consequence) is indented
        rows = [r.strip() for r in comment.split("<br>")]
        follows = ("=", "$=", "$\\Longrightarrow", "$\\leadsto", "⟹", "⇝")  # another name, or a consequence of the line above
        # a condition "(for ...)" right after a line "= ..." belongs to it: aligned with the text after its "="
        eq = [r.startswith(follows) for r in rows]
        cond = [k > 0 and eq[k - 1] and r.startswith("(") for k, r in enumerate(rows)]

        def row(k, r):
            if cond[k]:
                return f'<div class="lk-note-eq">{_md("<span class=\'lk-ghost\'>=&nbsp;</span>" + r)}</div>'
            return f'<div class="{"lk-note-eq" if eq[k] else "lk-note-row"}">{_md(r)}</div>'

        return "".join(row(k, r) for k, r in enumerate(rows)), True
    return (comment.html() if hasattr(comment, "html") else _md(comment)), False


class _Aside:
    def __init__(self, content, comment, at=None, rows=None):
        self.content, self.comment, self.at, self.rows = content, comment, at, rows
        self.new_module = numbering.starts_module()

    def html(self):
        # a display or a figure: centred on the page as any display, its comment in the comment column
        display = not isinstance(self.content, str) or self.content.strip().startswith(("$$", '<span class="lk-vconn"'))
        cls = "lk-aside lk-aside-display" if display else "lk-aside"
        if self.rows:
            # comments level with given lines of an n-line computation: the free height of the column is shared out
            # so that each comment's centre falls on its line (lines of about equal height)
            pairs = self.comment if isinstance(self.comment, (list, tuple)) else [(self.at, self.comment)]
            spots = [(k - 0.5) / self.rows for k, _ in pairs]
            grow = [spots[0]] + [b - a for a, b in zip(spots, spots[1:])] + [1 - spots[-1]]
            parts = []
            for g, (_, c) in zip(grow, pairs):
                inner, broken = _note(c)
                parts.append(f'<div class="lk-note-gap" style="flex-grow:{g:.4f}"></div>')
                parts.append(f'<div class="lk-note-one{" lk-note-lines" if broken else ""}">{inner}</div>')
            parts.append(f'<div class="lk-note-gap" style="flex-grow:{grow[-1]:.4f}"></div>')
            return f'<div class="{cls}">{as_html(self.content)}<div class="lk-aside-note lk-note-rows">{"".join(parts)}</div></div>'
        note, broken = _note(self.comment)
        lines = " lk-note-lines" if broken else ""
        lines += f" lk-note-{self.at}" if self.at in ("last", "middle") else ""
        return f'<div class="{cls}">{as_html(self.content)}<div class="lk-aside-note{lines}">{note}</div></div>'

    def _mime_(self):
        return ("text/html", _mark(self) + '<div class="lk-asides">' + self.html() + "</div>")


def ref(label):
    """Cross-reference as Markdown, e.g. f"By {ref('ivt')}, ..." gives "By Theorem 3.2, ..."."""
    kind, number = numbering.lookup(label)
    if kind is None:
        return f"**??{label}??**"
    name = {"section": "§", "figure": "Fig", "interactive": "Fig"}.get(kind) or _name(kind)
    return f'<a class="lk-ref" href="#lk-{label}">{name} {number}</a>'
