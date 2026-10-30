import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 08 • Local properties of scalar functions and maps: limits", css_file="bs101.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a result made from them (sum, multiple, angle, tangent vector, gradient)
    #   ORANGE (ochre) a third object, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS101 &bull; {running}</div>
      <div class="bs-title">Multivariable Calculus</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>BS101-04/05</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def proposition(body, title=""):
        return _statement("Proposition", title, body)

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def postulate(body, title=""):
        return _statement("Postulate", title, body)

    def note(body):
        """Editorial note of the notebook (not part of the lecture)."""
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        One line weight for every figure; the head is open and sized in points from the line width,
        so arrows look alike across lectures at any axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={3 * lw:g},head_width={1.3 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        from matplotlib.figure import Figure as _Figure

        fig = _Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        import numpy as _np

        rng = _np.random.default_rng(seed)
        t = _np.linspace(0, 2 * _np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * _np.cos(k * t + rng.uniform(0, 2 * _np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * _np.cos(t), cy + ry * r * _np.sin(t)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 08", "Week 04", "Lecture 08 • Local properties of scalar functions and maps: limits")
    return


@app.cell(hide_code=True)
def _(arrow, math):
    def vector(ax, tail, tip, color, label=None, turn=0, r=15, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip on a white box;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            arrow(ax, tail, tip, color, **kw)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    return (vector,)


@app.cell(hide_code=True)
def _(arrow):
    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, cross_axes, math, mo, np):
    _fig = Figure(figsize=(FULL, 3.6), layout="constrained")
    _sub, _sub2 = _fig.subfigures(1, 2)
    _ax, _ax2 = _sub.subplots(), _sub2.subplots()

    cross_axes(_ax, (-1.9, 1.9), (-0.6, 2.4))
    _t = np.linspace(-1.5, 1.5, 200)
    _ax.plot(_t, _t**2, color=BLUE, lw=1.4)
    _ax.plot(0, 0, "o", color="black", ms=6, mfc="white", mew=1.2, zorder=4)
    _ax.plot(0, 1, "o", color="black", ms=5, zorder=4)
    _ax.plot(-1.2, 1.44, "o", color=BLUE, ms=5, zorder=4)
    _ax.text(1.3, 1.3, r"$\mathrm{Im}(\gamma)$", color=BLUE, fontsize=13, ha="left", va="top")
    _ax.text(-1.3, 1.3, r"$\genfrac{[}{]}{0}{0}{t}{t^2}$", fontsize=13, ha="right", va="top")
    _ax.text(0.1, 1, r"$\genfrac{[}{]}{0}{0}{0}{1}$", fontsize=13, ha="left", va="center")
    _ax.text(0.1, -0.1, "not continuous", fontsize=12, ha="left", va="top")

    cross_axes(_ax2, (-1.6, 1.9), (-1.5, 1.7))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax2.plot(np.cos(_th), np.sin(_th), color=BLUE, lw=1.4)
    _ax2.plot(1, 0, "o", color=GREEN, ms=5, zorder=4)
    _ax2.plot(0, 1, "o", color="black", ms=5, zorder=4)
    _ax2.plot(math.cos(0.7), math.sin(0.7), "o", color=BLUE, ms=5, zorder=4)
    _ax2.text(-0.8, -0.8, r"$\mathrm{Im}(\sigma)$", color=BLUE, fontsize=13, ha="right", va="top")
    _ax2.text(1.12 * math.cos(0.7), 1.12 * math.sin(0.7), r"$\genfrac{[}{]}{0}{0}{\cos(t)}{\sin(t)}$", fontsize=13, ha="left", va="bottom")
    _ax2.text(-0.1, 1.08, r"$\genfrac{[}{]}{0}{0}{0}{1}$", fontsize=13, ha="right", va="bottom")
    _ax2.text(1.08, -0.08, r"$\lim_{t \to 0} \sigma(t)$", fontsize=13, ha="left", va="top")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - local properties of paths $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, &nbsp; $\gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix}$ (components)
    - $\leadsto$ &nbsp; limits are taken component by component

        $$
        \lim_{t \to a} \gamma(t) = \lim_{t \to a} \begin{bmatrix} \gamma^1(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix} = \begin{bmatrix} \lim_{t \to a} \gamma^1(t) \\ \vdots \\ \lim_{t \to a} \gamma^m(t) \end{bmatrix}
        $$

    - $\leadsto$ &nbsp; $\gamma$ continuous at $t = a$ if $\displaystyle \lim_{t \to a} \gamma(t) = \gamma(a)$ &nbsp; ($\gamma(a)$ is the position of $\gamma$ at $t = a$: $\gamma$ does not jump between positions at $t = a$)
    - $\leadsto$ &nbsp; $\gamma$ differentiable at $t = a$ if $\displaystyle \lim_{t \to a} \dfrac{\gamma(t) - \gamma(a)}{t - a}$ exists &nbsp; ($\gamma'(a)$, the velocity of $\gamma$ at $t = a$)
    - **Example.**

        $$
        \gamma(t) = \begin{cases}
        \begin{bmatrix} t \\ t^2 \end{bmatrix}, & t \neq 0 \\[12pt]
        \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0
        \end{cases}
        \qquad \qquad
        \sigma(t) = \begin{cases}
        \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, & t \neq 0 \\[12pt]
        \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0
        \end{cases}
        $$
    """
            ),
            _fig,
            mo.md(
                r"""
    - $\displaystyle \lim_{t \to 0} \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} \cos(2\pi) \\ \sin(2\pi) \end{bmatrix} = \begin{bmatrix} \cos(4\pi) \\ \sin(4\pi) \end{bmatrix}$ &nbsp; (also in $\mathrm{Im}(\sigma)$)
    - $\leadsto$ &nbsp; discontinuity is a “jump” in the parameterization of the image, not necessarily a hole in $\mathrm{Im}(\sigma)$
    - $\leadsto$ &nbsp; discontinuity is a hole in $\mathrm{graph}(\gamma)$!

    **In this lecture:** local properties of scalar functions and maps

    **References:** MT 2.2
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, LIGHT, RED, arrow, blank, definition, mo, np):
    _fig, _ax = blank(HALF + 1.5, 2.9, (-0.4, 3.8), (-0.4, 3.0))
    arrow(_ax, (-0.3, 0), (3.7, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.3), (0, 2.9), "black", lw=0.9)
    _a, _d = (2.1, 1.5), 1.15
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=LIGHT, lw=0)
    _ax.plot(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _x = (1.35, 2.05)
    _r = (_a[0] + _d * np.cos(-0.26), _a[1] + _d * np.sin(-0.26))
    _ax.plot([_a[0], _r[0]], [_a[1], _r[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    arrow(_ax, (0, 0), _a, "black")
    arrow(_ax, (0, 0), _x, RED)
    arrow(_ax, _a, _x, GREEN)
    _ax.text(_a[0] / 2 + 0.08, _a[1] / 2 - 0.08, r"$\vec{a}$", fontsize=13, ha="left", va="top")
    _ax.text(_x[0] / 2 - 0.08, _x[1] / 2 + 0.05, r"$\vec{x}$", color=RED, fontsize=13, ha="right", va="bottom")
    _ax.text((_a[0] + _x[0]) / 2 + 0.05, (_a[1] + _x[1]) / 2 + 0.1, r"$\vec{x} - \vec{a}$", color=GREEN, fontsize=13, ha="left", va="bottom")
    _ax.text((_a[0] + _r[0]) / 2 - 0.02, (_a[1] + _r[1]) / 2 - 0.06, r"$\delta$", color=GREY, fontsize=13, ha="right", va="top")
    _ax.text(_a[0] + _d * np.cos(2.3) - 0.05, _a[1] + _d * np.sin(2.3) + 0.05, r"$B(\vec{a}, \delta)$", color=BLUE, fontsize=13, ha="right", va="bottom")

    mo.vstack(
        [
            mo.md(
                r"""
    ## II.3 &nbsp; Local properties of scalar functions and maps: limits

    **Remark.** Given $f, g : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\lambda : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$, we can define

    - $(f + g) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $(f + g)(\vec{x}) = f(\vec{x}) + g(\vec{x})$
    - $(\lambda f) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $(\lambda f)(\vec{x}) = \lambda(\vec{x}) f(\vec{x})$
    - $(f \cdot g) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $(f \cdot g)(\vec{x}) = f(\vec{x}) \cdot g(\vec{x})$

    If $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ and $g : B \subseteq \mathbb{R}^m \longrightarrow C \subseteq \mathbb{R}^p$

    - $(g \circ f) : A \subseteq \mathbb{R}^n \longrightarrow C \subseteq \mathbb{R}^p$ &nbsp; $\leadsto$ &nbsp; $(g \circ f)(\vec{x}) = g(f(\vec{x}))$

    ### Limits
    """
            ),
            definition(
                r"""
    Given $\vec{a} \in \mathbb{R}^n$ and $\delta > 0$

    $$
    B(\vec{a}, \delta) = \big\{\, \vec{x} \in \mathbb{R}^n \;\big|\; \lVert \vec{x} - \vec{a} \rVert < \delta \,\big\}
    $$

    (the distance of $\vec{x}$ from $\vec{a}$ is smaller than $\delta$) is the **open ball** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$.
    """,
                "Open ball",
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** The “boundary” is not included! Only “interior” points are part of $B(\vec{a}, \delta)$.

    - $\leadsto$ &nbsp; $S(\vec{a}, \delta) = \big\{\, \vec{x} \in \mathbb{R}^n \;\big|\; \lVert \vec{x} - \vec{a} \rVert = \delta \,\big\}$ &nbsp; **sphere** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$
    - $\leadsto$ &nbsp; $\overline{B(\vec{a}, \delta)} = B(\vec{a}, \delta) \cup S(\vec{a}, \delta)$ &nbsp; **closed ball** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$ &nbsp; ($\lVert \vec{x} - \vec{a} \rVert \leq \delta$)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, np):
    # ---- Interactive 3D figures ------------------------------------------
    # Drawn in the browser on canvases, in the style of the static figures: orthographic views of
    # R^3 = R^2 x R (x^1 towards the viewer, x^2 to the right, y up), surfaces drawn back to front.
    # Dragging turns the view at a fixed scale (all panels of a figure together) and a double click restores
    # it; a figure redrawn by a slider keeps its view. Names sit beside the objects they name. Typesetting is done
    # by KaTeX.
    import html as _html
    import json as _json

    _PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" onload="window.typeset && typeset()"></script>
    <style>
      html, body { margin: 0; padding: 0; background: transparent; overflow: hidden;
                   font-family: KaTeX_Main, "Latin Modern Roman", Georgia, serif; }
      #o { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 4px 16px; }
      #g { position: relative; flex: 1 1 300px; min-width: 240px; max-width: __MAXW__px; display: grid;
           grid-template-columns: repeat(__COLS__, minmax(0, 1fr)); gap: 6px 14px; touch-action: none; cursor: grab;
           user-select: none; -webkit-user-select: none; }
      @media (max-width: 520px) { #g { grid-template-columns: minmax(0, 1fr); } }
      #g.drag { cursor: grabbing; }
      .p { position: relative; }
      .p canvas { display: block; width: 100%; }
      .cap { text-align: center; font-size: 14px; }
      .lab { position: absolute; left: 0; top: 0; white-space: nowrap; line-height: 1.1; pointer-events: none; font-size: 15px; }
      .katex { font-size: 1em; }
      #lg { flex: 0 0 auto; border: 1px solid #c8c8c8; border-radius: 4px; padding: 4px 10px; background: #fff; font-size: 14px; }
      #lg:empty { display: none; }
      .it { display: flex; align-items: center; gap: 8px; margin: 4px 0; white-space: nowrap; }
      .it svg { flex: 0 0 24px; }
      #hint { position: absolute; right: 0; bottom: 0; color: #888; opacity: 0.7; font: 15px Georgia, serif; }
    </style></head><body>
    <div id="o"><div id="g" role="img" aria-label="__ALT__"><div id="hint">&#10227;</div></div><div id="lg"></div></div>
    <script>
    (function () {
      const S = __SCENE__;
      const RAD = Math.PI / 180, L = [0.3, -0.4, 0.87];
      const lit = [247, 251, 255], dark = [201, 223, 244], lit2 = [219, 235, 251], dark2 = [163, 194, 230];
      const rgb = (a, b, k) => "rgb(" + [0, 1, 2].map((i) => Math.round(a[i] + (b[i] - a[i]) * k)).join(",") + ")";
      const texs = [];
      const tex = (el, t) => { el.dataset.tex = t; el.textContent = t.replace(/\\[a-z]+\{?|[{}$^_]/gi, ""); texs.push(el); };
      const dot3 = (u, p) => u[0] * p[0] + u[1] * p[1] + u[2] * p[2];

      class Scene {
        constructor(spec, host) {
          const ys = (this.ys = spec.ys);
          this.box = document.createElement("div");
          this.box.className = "p";
          this.cv = document.createElement("canvas");
          this.box.appendChild(this.cv);
          this.g = this.cv.getContext("2d");
          host.appendChild(this.box);
          if (spec.caption) {
            const c = document.createElement("div");
            c.className = "cap";
            tex(c, spec.caption);
            this.box.appendChild(c);
          }
          const pts = (this.pts = []), quads = (this.quads = []), segs = (this.segs = []);
          this.dots = []; this.heads = []; this.labs = [];
          const add = (x, y, z) => (pts.push(x, y, z), pts.length / 3 - 1);
          for (const s of spec.surfaces) {
            const base = pts.length / 3, n = s.n, m = s.m, id = (i, j) => base + i * m + j;
            for (const v of s.v) pts.push(v);
            const P = (k) => [pts[3 * k], pts[3 * k + 1], pts[3 * k + 2]];
            const inTint = (x1, x2) => s.tint && x1 > s.tint[0] && x1 <= s.tint[1] && x2 > s.tint[2] && x2 <= s.tint[3];
            const sLit = s.tone ? s.tone.map((c) => Math.round(0.06 * c + 0.94 * 255)) : lit;
            const sDark = s.tone ? s.tone.map((c) => Math.round(0.3 * c + 0.7 * 255)) : dark;
            for (let i = 0; i < n - 1; i++) for (let j = 0; j < m - 1; j++) {
              const q = [id(i, j), id(i + 1, j), id(i + 1, j + 1), id(i, j + 1)];
              const v = q.map(P);
              if (v.some((p) => p.some(isNaN))) continue;
              const deep = inTint((v[0][0] + v[2][0]) / 2, (v[0][1] + v[2][1]) / 2);
              let col = s.flat;
              if (!col) {
                const a = [0, 1, 2].map((t) => v[2][t] - v[0][t]), b = [0, 1, 2].map((t) => v[3][t] - v[1][t]);
                const nn = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
                const len = Math.hypot(...nn) || 1;
                const k = Math.min(1, Math.abs((nn[0] * L[0] + nn[1] * L[1] + nn[2] * L[2]) / len) / 1.0034);
                col = deep ? rgb(dark2, lit2, k) : rgb(sDark, sLit, k);
              }
              quads.push([q, col, deep ? 1 : s.alpha]);
            }
            for (const [axis, every, c, lw] of s.wire || []) {
              const rows = axis === 0 ? n : m, cols = axis === 0 ? m : n;
              for (let r = 0; r < rows; r++) {
                if (r % every !== 0 && r !== rows - 1) continue;
                for (let t = 0; t < cols - 1; t++) {
                  const a = axis === 0 ? id(r, t) : id(t, r), b = axis === 0 ? id(r, t + 1) : id(t + 1, r);
                  const pa = P(a), pb = P(b);
                  if (pa.concat(pb).some(isNaN)) continue;
                  if (s.clear && inTint((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)) continue;
                  segs.push({ a, b, c, lw, line: null });
                }
              }
            }
          }
          this.lines = spec.lines.map((ln) => {
            const idx = [];
            for (let k = 0; k < ln.p.length; k += 3) idx.push(add(ln.p[k], ln.p[k + 1], ln.p[k + 2]));
            const line = { idx, dash: ln.d, cum: new Float64Array(idx.length) };
            for (let k = 0; k < idx.length - 1; k++)
              if (![ln.p[3 * k], ln.p[3 * k + 3]].some(isNaN)) segs.push({ a: idx[k], b: idx[k + 1], c: ln.c, lw: ln.w, line, k, e: ln.e || 0, flat: ln.b });
            return line;
          });
          for (const d of spec.points) this.dots.push({ i: add(...d.p), c: d.c, r: d.r, h: d.h });
          for (const h of spec.heads) this.heads.push({ i: add(...h.p), j: add(...h.q), c: h.c, w: h.w, d: h.d });
          // the centre of the scene and the radius of a ball holding it, heights at their drawing scale
          let src = pts;
          if (spec.box) {
            src = [];
            for (const p of [0, 1]) for (const q of [0, 1]) for (const t of [0, 1]) src.push(spec.box[0][p], spec.box[1][q], spec.box[2][t]);
          }
          const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
          for (let k = 0; k < src.length; k++) {
            const t = k % 3, v = src[k] * (t === 2 ? ys : 1);
            if (!isNaN(v)) { lo[t] = Math.min(lo[t], v); hi[t] = Math.max(hi[t], v); }
          }
          const C = [0, 1, 2].map((t) => (lo[t] + hi[t]) / 2);
          let R = 0;
          for (let k = 0; k < src.length; k += 3) {
            const d = Math.hypot(src[k] - C[0], src[k + 1] - C[1], src[k + 2] * ys - C[2]);
            if (!isNaN(d)) R = Math.max(R, d);
          }
          C[2] /= ys;
          this.C = C;
          this.R = R;
          for (const l of spec.labels) {
            const el = document.createElement("div");
            el.className = "lab";
            el.style.color = l.c;
            tex(el, l.t);
            this.box.appendChild(el);
            this.labs.push({ el, i: add(...l.p), a: l.a * RAD, r: l.r });
          }
          const M = pts.length / 3;
          this.X = new Float64Array(M); this.Y = new Float64Array(M); this.Z = new Float64Array(M);
        }

        size(W, H, R) {
          this.W = W; this.H = H;
          this.sc = 0.94 * Math.min(W, H) / (2 * R);
          const dpr = window.devicePixelRatio || 1;
          this.cv.width = Math.round(W * dpr);
          this.cv.height = Math.round(H * dpr);
          this.cv.style.height = H + "px";
          this.g.setTransform(dpr, 0, 0, dpr, 0, 0);
        }

        draw(az, el) {
          const { g, pts, X, Y, Z, W, H, sc, ys } = this;
          if (!W) return;
          const a = az * RAD, e = el * RAD;
          const r = [-Math.sin(a), Math.cos(a), 0];
          const u = [-Math.sin(e) * Math.cos(a), -Math.sin(e) * Math.sin(a), Math.cos(e) * ys];
          const d = [Math.cos(e) * Math.cos(a), Math.cos(e) * Math.sin(a), Math.sin(e) * ys];
          const tx = W / 2 - dot3(r, this.C) * sc, ty = H / 2 + dot3(u, this.C) * sc;
          for (let k = 0; k < X.length; k++) {
            const x = pts[3 * k], y = pts[3 * k + 1], z = pts[3 * k + 2];
            X[k] = (x * r[0] + y * r[1] + z * r[2]) * sc + tx;
            Y[k] = ty - (x * u[0] + y * u[1] + z * u[2]) * sc;
            Z[k] = x * d[0] + y * d[1] + z * d[2];
          }
          for (const ln of this.lines) {  // screen length along each line, so that dashes run on across segments
            ln.cum[0] = 0;
            for (let k = 1; k < ln.idx.length; k++) {
              const p = ln.idx[k - 1], q = ln.idx[k];
              ln.cum[k] = ln.cum[k - 1] + (isNaN(X[p] + X[q]) ? 0 : Math.hypot(X[q] - X[p], Y[q] - Y[p]));
            }
          }
          const items = [], bias = S.bias;
          for (const q of this.quads) items.push([(Z[q[0][0]] + Z[q[0][1]] + Z[q[0][2]] + Z[q[0][3]]) / 4, 0, q]);
          for (const s of this.segs) items.push([(Z[s.a] + Z[s.b]) / 2 + bias + (s.e || 0), 1, s]);
          for (const h of this.heads) items.push([Z[h.i] + bias, 2, h]);
          for (const p of this.dots) items.push([Z[p.i] + 2 * bias, 3, p]);
          items.sort((p, q) => p[0] - q[0]);
          g.clearRect(0, 0, W, H);
          g.lineJoin = "round";
          for (let n = 0; n < items.length; n++) {
            const [, kind, o] = items[n];
            if (kind === 0) {
              const q = o[0];
              g.beginPath();
              g.moveTo(X[q[0]], Y[q[0]]);
              for (let t = 1; t < 4; t++) g.lineTo(X[q[t]], Y[q[t]]);
              g.closePath();
              g.fillStyle = g.strokeStyle = o[1];
              g.globalAlpha = o[2];
              g.fill();
              if (o[2] === 1) { g.lineWidth = 0.6; g.setLineDash([]); g.stroke(); }
              g.globalAlpha = 1;
            } else if (kind === 1) {
              if (o.done) { o.done = false; continue; }
              let p0 = o, p1 = o;
              if (o.flat) {  // the pieces of a straight line up to the next surface go in one stroke, so no seams show
                let grew = true;
                while (grew) {
                  grew = false;
                  for (let m = n + 1; m < items.length && items[m][1] !== 0; m++) {
                    const q = items[m][2];
                    if (items[m][1] !== 1 || q.line !== o.line || q.done) continue;
                    if (q.k === p1.k + 1) { p1 = q; q.done = true; grew = true; }
                    else if (q.k === p0.k - 1) { p0 = q; q.done = true; grew = true; }
                  }
                }
              }
              g.beginPath();
              g.moveTo(X[p0.a], Y[p0.a]);
              g.lineTo(X[p1.b], Y[p1.b]);
              g.strokeStyle = o.c;
              g.lineWidth = o.lw;
              const dash = o.line && o.line.dash;
              g.lineCap = dash || o.flat ? "butt" : "round";
              g.setLineDash(dash || []);
              g.lineDashOffset = dash ? -o.line.cum[p0.k] : 0;
              g.stroke();
            } else if (kind === 2) {
              let vx = X[o.i] - X[o.j], vy = Y[o.i] - Y[o.j];
              const len = Math.hypot(vx, vy) || 1;
              vx /= len; vy /= len;
              const hl = Math.max(3.5 * o.w, 6), hw = Math.max(1.5 * o.w, 2.6), bx = X[o.i] - hl * vx, by = Y[o.i] - hl * vy;  // open head, as on the page
              g.strokeStyle = o.c;
              g.lineWidth = o.w;
              g.setLineDash([]);
              g.lineCap = "round";
              if (!o.d) { g.beginPath(); g.moveTo(X[o.j], Y[o.j]); g.lineTo(X[o.i], Y[o.i]); g.stroke(); }
              g.beginPath();
              g.moveTo(bx - hw * vy, by + hw * vx);
              g.lineTo(X[o.i], Y[o.i]);
              g.lineTo(bx + hw * vy, by - hw * vx);
              g.stroke();
            } else {
              g.beginPath();
              g.arc(X[o.i], Y[o.i], o.r, 0, 2 * Math.PI);
              g.setLineDash([]);
              g.fillStyle = o.h ? "#fff" : o.c;
              g.fill();
              g.strokeStyle = o.h ? o.c : "#fff";
              g.lineWidth = o.h ? 1.5 : 1;
              g.stroke();
            }
          }
          for (const l of this.labs) {  // beside its point, on the side given by its direction
            const c = Math.cos(l.a), s = Math.sin(l.a);
            const hx = c > 0.35 ? 0 : c < -0.35 ? -100 : -50, vy = s > 0.35 ? -100 : s < -0.35 ? 0 : -50;
            l.el.style.transform = `translate(${X[l.i] + l.r * c}px, ${Y[l.i] - l.r * s}px) translate(${hx}%, ${vy}%)`;
          }
        }
      }

      const grid = document.getElementById("g"), out = document.getElementById("o");
      const scenes = S.panels.map((p) => new Scene(p, grid));
      const Rmax = Math.max(...scenes.map((s) => s.R));
      const lg = document.getElementById("lg");
      for (const e of S.legend) {
        const it = document.createElement("div"), t = document.createElement("span");
        it.className = "it";
        const dash = e.d ? ` stroke-dasharray="${e.d.join(" ")}"` : "";
        it.innerHTML = {
          dot: `<svg width="24" height="14"><circle cx="12" cy="7" r="4.2" fill="${e.c}"/></svg>`,
          ring: `<svg width="24" height="14"><circle cx="12" cy="7" r="3.8" fill="#fff" stroke="${e.c}" stroke-width="1.5"/></svg>`,
          line: `<svg width="24" height="14"><line x1="1" y1="7" x2="23" y2="7" stroke="${e.c}" stroke-width="${e.w || 2}"${dash}/></svg>`,
          area: `<svg width="24" height="14"><rect x="2" y="1.5" width="20" height="11" fill="${e.c}" fill-opacity="${e.o || 1}" stroke="${e.e || e.c}" stroke-width="1.2"/></svg>`,
        }[e.k];
        tex(t, e.t);
        it.appendChild(t);
        lg.appendChild(it);
      }

      // the view, shared by all panels and kept by the page when a slider redraws the figure
      let store = {};
      try { store = window.parent.__bs3d || (window.parent.__bs3d = {}); } catch (e) {}
      let view = S.key && store[S.key] ? { ...store[S.key] } : { az: S.az, el: S.el };
      const keep = () => { if (S.key) store[S.key] = { ...view }; };

      function fit() {  // square-ish canvases holding their balls, so that the scale never changes while turning
        for (const s of scenes) {
          const W = s.box.clientWidth;
          s.size(W, Math.min(S.h, W), S.shared ? Rmax : s.R);
        }
        if (window.frameElement) window.frameElement.style.height = out.offsetHeight + "px";
      }
      const draw = () => { for (const s of scenes) s.draw(view.az, view.el); };
      window.typeset = () => {
        for (const el of texs) try { katex.render(el.dataset.tex, el, { throwOnError: false }); } catch (e) {}
        fit();
        draw();
      };

      let pending = false;
      const redraw = () => { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; draw(); }); } };
      let grab = null;
      grid.addEventListener("pointerdown", (e) => { grab = { x: e.clientX, y: e.clientY, ...view }; grid.setPointerCapture(e.pointerId); grid.classList.add("drag"); });
      grid.addEventListener("pointermove", (e) => {
        if (!grab) return;
        view = { az: grab.az - (e.clientX - grab.x) * 0.45, el: Math.max(-89, Math.min(89, grab.el + (e.clientY - grab.y) * 0.45)) };
        keep();
        redraw();
      });
      const drop = () => { grab = null; grid.classList.remove("drag"); };
      grid.addEventListener("pointerup", drop);
      grid.addEventListener("pointercancel", drop);
      grid.addEventListener("dblclick", () => { view = { az: S.az, el: S.el }; if (S.key) delete store[S.key]; redraw(); });
      new ResizeObserver(() => { fit(); draw(); }).observe(out);
      if (window.katex) window.typeset();
    })();
    </script></body></html>"""

    def _flat(*xyz):
        return np.round(np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in xyz)), -1).ravel(), 3).tolist()

    def sheet(x1, x2, y, wire=(), tint=None, clear=False, flat=None, alpha=1.0, tone=None):
        """A surface through the grid points (x1, x2, y) (2D arrays). `wire` lists grid lines to draw, as
        (axis, every, colour, width): every `every`-th row (axis 0) or column (axis 1), and the last one.
        Faces whose centre lies in tint = (x^1 lo, x^1 hi, x^2 lo, x^2 hi) (lo excluded) take deeper tones and
        stay opaque, without wire there when `clear`; the other faces have the opacity `alpha`.
        `flat` is one colour instead of the shading, and `tone` (a colour such as RED) shades the surface in
        light tones of that colour instead of the light blue ones."""
        n, m = np.shape(x1)
        rgb = [int(tone[k : k + 2], 16) for k in (1, 3, 5)] if tone else None
        return {"n": n, "m": m, "v": _flat(x1, x2, y), "wire": [list(t) for t in wire], "tint": tint, "clear": clear, "flat": flat, "alpha": alpha, "tone": rgb}

    def patch(corners, colour, alpha=1.0, n=6):
        """The flat parallelogram (or quadrilateral) with the four `corners` (in order), one colour, opacity `alpha`;
        cut into n x n faces, so that it is drawn in the right order among other surfaces."""
        c = [np.asarray(q, float) for q in corners]
        s, t = np.meshgrid(np.linspace(0, 1, n + 1), np.linspace(0, 1, n + 1), indexing="ij")
        p = (1 - s)[..., None] * (1 - t)[..., None] * c[0] + s[..., None] * (1 - t)[..., None] * c[1] + (s * t)[..., None] * c[2] + ((1 - s) * t)[..., None] * c[3]
        return sheet(p[..., 0], p[..., 1], p[..., 2], flat=colour, alpha=alpha)

    def panel(ys, surfaces=(), lines=(), points=(), axes=(), arrows=(), arcs=(), texts=(), caption=None, box=None):
        """One drawing of a 3D figure, with heights at the scale `ys`.
        lines: (x1, x2, y, colour, width[, dash, depth offset]); points: ((x^1, x^2, y), colour[, radius, hollow]);
        axes: (tail, tip, TeX label, direction of the label in degrees), drawn black;
        arrows: (tail, tip, colour[, width, dash]), vectors with a head in their colour;
        arcs: (x1, x2, y, colour[, width]), curves ending in a head, such as a turning arrow;
        texts: ((x^1, x^2, y), TeX, colour, direction[, distance]), names of points and objects and tick values,
        each beside its point; caption: TeX below the drawing;
        box: ((x^1 lo, hi), (x^2 lo, hi), (y lo, hi)) to size the drawing by, instead of its own points."""
        p = {"ys": ys, "surfaces": list(surfaces), "lines": [], "points": [], "heads": [], "labels": [], "caption": caption, "box": box}
        for ln in lines:
            p["lines"].append({"p": _flat(*ln[:3]), "c": ln[3], "w": ln[4], "d": ln[5] if len(ln) > 5 else None, "e": ln[6] if len(ln) > 6 else 0})
        for tail, tip, label, d in axes:
            a, b = np.asarray(tail, float), np.asarray(tip, float)
            seg = a + np.linspace(0, 0.96, 60)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": "#000000", "w": 1.1, "d": None, "b": 1})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": "#000000", "w": 1.1})
            p["labels"].append({"p": b.tolist(), "t": label, "c": "#000000", "a": d, "r": 5})
        for q in points:
            p["points"].append({"p": [float(c) for c in q[0]], "c": q[1], "r": q[2] if len(q) > 2 else 4.0, "h": bool(q[3]) if len(q) > 3 else False})
        for ar in arrows:
            a, b = np.asarray(ar[0], float), np.asarray(ar[1], float)
            seg = a + np.linspace(0, 0.96, 40)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8, "d": ar[4] if len(ar) > 4 else None, "e": 0, "b": 1})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8, "d": ar[4] if len(ar) > 4 else None})
        for arc in arcs:
            c = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in arc[:3])), -1)
            p["lines"].append({"p": _flat(*c[:-1].T), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8, "d": None, "e": 0})
            p["heads"].append({"p": c[-1].tolist(), "q": c[max(0, len(c) - 4)].tolist(), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8})
        for tx in texts:
            p["labels"].append({"p": [float(c) for c in tx[0]], "t": tx[1], "c": tx[2], "a": tx[3], "r": tx[4] if len(tx) > 4 else 5})
        return p

    def turntable(az, el, alt, panels, legend=(), height=360, width=None, cols=1, key=None, shared=True, bias=0.03):
        """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
        from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
        at most `width` wide, with a legend box beside them (below them on narrow screens). `key` names the view
        so that it survives a redraw; with `shared`, all panels have one scale.
        legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area"."""
        scene = {"az": az, "el": el, "h": height, "bias": bias, "panels": list(panels), "legend": [], "key": key, "shared": shared}
        for e in legend:
            item = {"k": e[0], "c": e[1], "t": e[2]}
            if len(e) > 3:
                item["e" if e[0] == "area" else "w"] = e[3]
            if len(e) > 4:
                item["o" if e[0] == "area" else "d"] = e[4]
            scene["legend"].append(item)
        page = (_PAGE.replace("__MAXW__", str(width or cols * height + (cols - 1) * 14)).replace("__COLS__", str(cols))
                .replace("__ALT__", _html.escape(alt)).replace("__SCENE__", _json.dumps(scene, separators=(",", ":"))))
        return mo.Html(f'<iframe srcdoc="{_html.escape(page)}" title="{_html.escape(alt)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>')

    return panel, patch, sheet, turntable


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, arrow, blank, definition, mo, np, panel, sheet, turntable):
    # R^n: the ball about a (blue), fixed, and the map
    _fig, _ax = blank(3.9, 3.4, (-0.5, 5.1), (-0.6, 3.6))
    _th = np.linspace(0, 2 * np.pi, 200)
    arrow(_ax, (-0.4, 0), (3.4, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.5), (0, 3.0), "black", lw=0.9)
    _ax.text(-0.15, 3.05, r"$\mathbb{R}^n$", fontsize=13, ha="right", va="center")
    _ax.fill(1.5 + 0.85 * np.cos(_th), 1.75 + 0.85 * np.sin(_th), color=LIGHT, lw=0)
    _ax.plot(1.5 + 0.85 * np.cos(_th), 1.75 + 0.85 * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _ax.plot(1.5, 1.75, "o", color="black", ms=5, zorder=4)
    _ax.text(1.5, 0.82, r"$B(\vec{a}, \delta)$", color=BLUE, fontsize=13, ha="center", va="top")
    _ax.text(1.6, 1.75, r"$\vec{a}$", fontsize=13, ha="left", va="center")
    arrow(_ax, (3.7, 2.2), (5.0, 2.2), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(4.35, 2.55, "$f$", fontsize=13, ha="center", va="bottom")

    # R^m, turning: the ball about b, see-through as the L06 sphere (light red, a few grey circles), b, and the image of
    # the punctured ball (green), a small flat disk inside the ball, upper left of b
    _c, _r = np.array((0.5, 1.9, 1.7)), 1.1
    _b = _c + (0.0, 0.25, 0.12)
    _u, _w = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 49), indexing="ij")
    _ball = sheet(_c[0] + _r * np.sin(_u) * np.cos(_w), _c[1] + _r * np.sin(_u) * np.sin(_w), _c[2] + _r * np.cos(_u),
                  wire=[(0, 12, GREY, 1.0), (1, 12, GREY, 0.5)], flat="#f4e4e1", alpha=0.5)
    _g = _c + (0.0, -0.35, 0.42)  # about halfway between the centre and the surface
    _s2, _w2 = np.meshgrid(np.linspace(0, 1, 4), np.linspace(0, 2 * np.pi, 37), indexing="ij")  # a flat disk, light green, a thin green rim
    _d1, _d2 = _g[0] + 0.3 * _s2 * np.cos(_w2), _g[1] + 0.3 * _s2 * np.sin(_w2)
    _image = [sheet(_d1, _d2, np.full_like(_d1, _g[2]), flat="#bcd5c2", alpha=0.95)]
    _ball3d = turntable(
        25,
        20,
        "the ball about b in R^m, the point b, and the image of the punctured ball about a, a small region inside the ball",
        [
            panel(
                1.0,
                surfaces=[_ball] + _image,
                lines=[(_d1[-1], _d2[-1], np.full(37, _g[2]), GREEN, 1.0)],
                points=[(tuple(_b), RED, 4.0)],
                axes=[((0, 0, 0), (2.2, 0, 0), "", 0), ((0, 0, 0), (0, 3.6, 0), "", 0), ((0, 0, 0), (0, 0, 3.3), r"\mathbb{R}^m", 150)],
                texts=[(tuple(_c + (0, _r, 0)), r"B(\vec{b}, \varepsilon)", RED, 0, 8), (tuple(_b), r"\vec{b}", "#000000", 0, 6),
                       (tuple(_c + (0, 0, _r)), r"f(B(\vec{a}, \delta) \setminus \{\vec{a}\})", GREEN, 90, 8)],
            )
        ],
        height=300,
        key="lecture-08-limit",
    )
    _both = mo.Html(
        '<div style="display: flex; flex-wrap: nowrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'  # always on one line (the instructor)
        f'<div style="flex: 1.3 1 300px; min-width: 0;">{mo.as_html(_fig).text}</div>'
        f'<div style="flex: 1 1 260px; min-width: 240px;">{_ball3d.text}</div></div>'
    )

    mo.vstack(
        [
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\vec{a} \in \mathbb{R}^n$, $\vec{b} \in \mathbb{R}^m$, we say

    $$
    \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}
    $$

    (the limit of $f(\vec{x})$ as $\vec{x}$ approaches $\vec{a}$ exists and is equal to $\vec{b}$) if for every choice of $\varepsilon > 0$ we can make $f(\vec{x})$ $\varepsilon$-close to $\vec{b}$ by finding $\delta > 0$ and taking $\vec{x}$ $\delta$-close to $\vec{a}$ (different from $\vec{a}$).
    """,
                "Limit",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; for every $\varepsilon > 0$, we can find $\delta > 0$ such that $\vec{x} \in B(\vec{a}, \delta) \setminus \{\vec{a}\}$ guarantees that $f(\vec{x}) \in B(\vec{b}, \varepsilon)$

    $$
    \Longleftrightarrow \qquad f\big( B(\vec{a}, \delta) \setminus \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)
    $$
    """
            ),
            _both,
            mo.md(
                r"""
    Choose $B(\vec{b}, \varepsilon)$. Can we find $B(\vec{a}, \delta)$ such that $f\big( B(\vec{a}, \delta) \setminus \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$?

    If yes for every $\varepsilon > 0$ &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$!

    **Example.** $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$

    $$
    f(\vec{x}) = \begin{cases}
    \dfrac{2 (x^1)^2}{\lVert \vec{x} \rVert}, & \vec{x} \neq \vec{0} \\[10pt]
    5, & \vec{x} = \vec{0}
    \end{cases}
    $$

    Claim: $\displaystyle \lim_{\vec{x} \to \vec{0}} f(\vec{x}) = 0$

    **Proof.** To show this

    1. choose $\varepsilon > 0$ (let's say $\varepsilon = 1$)
    2. look for $\delta > 0$ such that

        $$
        \underbrace{0 < \lVert \vec{x} - \vec{0} \rVert < \delta}_{\footnotesize \begin{matrix}\text{whenever } \vec{x} \text{ is} \\ \delta\text{-close to } \vec{a} = \vec{0}\end{matrix}} \qquad \underbrace{\Longrightarrow}_{\footnotesize \begin{matrix}\text{we} \\ \text{guarantee}\end{matrix}} \qquad \underbrace{\lvert f(\vec{x}) - 0 \rvert < \varepsilon = 1}_{\footnotesize \begin{matrix}f(\vec{x}) \text{ is } 1\text{-close} \\ \text{to } b = 0\end{matrix}}
        $$

        ($1$-close: as close as we want it)

    For $\vec{x} \neq \vec{0}$

    $$
    \lvert f(\vec{x}) - 0 \rvert = \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} \leq \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} + \frac{2 (x^2)^2}{\lVert \vec{x} \rVert} = 2\, \frac{\lVert \vec{x} \rVert^2}{\lVert \vec{x} \rVert} = 2 \lVert \vec{x} \rVert
    $$

    $$
    \Longrightarrow \qquad \lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert = 2 \lVert \vec{x} - \vec{0} \rVert
    $$

    $\Longrightarrow$ &nbsp; whenever we make $0 < \lVert \vec{x} - \vec{0} \rVert < \dfrac{1}{2} = \delta$ (for $\varepsilon = 1$) we guarantee that $\lvert f(\vec{x}) - 0 \rvert < 1$!

    Now repeat the argument for every $\varepsilon > 0$ &nbsp; ($\varepsilon = \dfrac{1}{2} \leadsto \delta = \dfrac{1}{4}$, &nbsp; $\varepsilon = \dfrac{1}{3} \leadsto \delta = \dfrac{1}{6}$, &nbsp; …)

    $\therefore$ &nbsp; if $0 < \lVert \vec{x} - \vec{0} \rVert < \dfrac{\varepsilon}{2} = \delta$

    $$
    \Longrightarrow \qquad \lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert < 2 \cdot \frac{\varepsilon}{2} = \varepsilon \tag*{$\square$}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    eps = mo.ui.slider(0.1, 2, 0.1, value=1, label=r"$\varepsilon$", show_value=True)
    return (eps,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, LIGHT, RED, arrow, cross_axes, eps, mo, np):
    _e = eps.value
    _d = _e / 2
    _fig = Figure(figsize=(FULL, 3.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 0.8])

    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.fill(_d * np.cos(_th), _d * np.sin(_th), color=LIGHT, lw=0, zorder=0)
    _left.plot(_d * np.cos(_th), _d * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _left.plot(0, 0, "o", color="black", ms=5, mfc="white", mew=1.1, zorder=4)

    _right.set_xlim(-1.0, 1.9)
    _right.set_ylim(-2.6, 5.9)
    _right.axis("off")
    arrow(_right, (0, -2.6), (0, 5.85), "black", lw=0.9)
    _right.text(-0.2, 5.75, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    # tick labels at their ticks; below 0.6 the labels of +-eps sit just above and below them, and below 0.3 the 0 is not written
    _near = _e < 0.6
    for _y, _name, _va in ((_e, r"$\varepsilon$", "bottom" if _near else "center"), (-_e, r"$-\varepsilon$", "top" if _near else "center"), (0, "$0$", "center"), (5, "$5$", "center")):
        _right.plot([-0.07, 0.07], [_y, _y], color="black", lw=0.9)
        if _y != 0 or _e >= 0.3:
            _right.text(-0.2, _y, _name, ha="right", va=_va, fontsize=12)
    # the interval B(0, eps) and the image of the punctured ball, drawn beside the axis
    _right.plot([0.3, 0.3], [-_e, _e], color=RED, lw=1.4)
    _right.plot([0.3, 0.3], [-_e, _e], "o", color=RED, ms=5, mfc="white", mew=1.1, zorder=4)
    _right.plot([0.6, 0.6], [0, _e], color=GREEN, lw=1.4)
    _right.plot(0.6, 0, "o", color=GREEN, ms=5, zorder=4)
    _right.plot(0.6, _e, "o", color=GREEN, ms=5, mfc="white", mew=1.1, zorder=4)
    _right.plot(0, 5, "o", color="black", ms=5, zorder=4)
    _left.text(_d * 0.71 + 0.05, _d * 0.71 + 0.05, r"$B(\vec{0}, \delta) \setminus \{\vec{0}\}$", color=BLUE, fontsize=13, ha="left", va="bottom")
    _left.text(-0.06, -0.06, r"$\vec{0}$", fontsize=13, ha="right", va="top")
    _right.text(0.22, -_e - 0.15, r"$B(0, \varepsilon)$", color=RED, fontsize=13, ha="left", va="top")
    _right.text(0.5, _e + 0.15, r"$f(B(\vec{0}, \delta) \setminus \{\vec{0}\})$", color=GREEN, fontsize=13, ha="left", va="bottom")
    _right.text(0.12, 5, r"$f(\vec{0})$", fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.hstack([eps], justify="start", gap=2, wrap=True),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, LIGHT, ORANGE, RED, arrow, blank, blob, mo, np, theorem):
    _tint = (0.18, 0.49, 0.2, 0.18)
    _fig, _ax = blank(FULL, 3.3, (-0.3, 9.1), (-0.15, 3.05))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(1.2 + 0.8 * np.cos(_th), 1.5 + 0.8 * np.sin(_th), color=LIGHT, lw=0)
    _ax.plot(1.2 + 0.8 * np.cos(_th), 1.5 + 0.8 * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _ax.plot([1.2, 1.2 + 0.8 * 0.82], [1.5, 1.5 + 0.8 * 0.57], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot(1.2, 1.5, "o", color="black", ms=5, zorder=4)
    arrow(_ax, (2.5, 2.0), (3.8, 2.0), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(3.15, 2.33, "$f$", fontsize=13, ha="center", va="bottom")
    for _c, _col in ((5.5, RED), (7.7, ORANGE)):
        _ax.plot(_c + 1.1 * np.cos(_th), 1.5 + 1.1 * np.sin(_th), color=_col, lw=1.2, ls=(0, (4, 3)))
        _ax.plot([_c, _c + 1.1], [1.5, 1.5], color=GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.plot(_c, 1.5, "o", color=_col, ms=5, zorder=4)
    _bx, _by = blob(5.15, 2.05, 0.4, 0.26, seed=3)
    _ax.fill(_bx, _by, color=_tint, lw=0)
    _ax.plot(_bx, _by, color=GREEN, lw=1.2)
    _ax.text(1.2, 0.62, r"$B(\vec{a}, \delta)$", color=BLUE, fontsize=13, ha="center", va="top")
    _ax.text(1.1, 1.5, r"$\vec{a}$", fontsize=13, ha="right", va="center")
    _ax.text(1.48, 1.8, r"$\delta$", color=GREY, fontsize=13, ha="right", va="bottom")
    for _c, _col, _i in ((5.5, RED, 1), (7.7, ORANGE, 2)):
        _ax.text(_c + 0.55, 1.55, r"$\varepsilon$", color=GREY, fontsize=13, ha="center", va="bottom")
        _ax.text(_c, 1.42, rf"$\vec{{b}}_{_i}$", fontsize=13, ha="center", va="top")
        _ax.text(_c, 0.32, rf"$B(\vec{{b}}_{_i}, \varepsilon)$", color=_col, fontsize=13, ha="center", va="top")
    _ax.text(5.15, 2.68, r"$f(B(\vec{a}, \delta) \setminus \{\vec{a}\})$", color=GREEN, fontsize=13, ha="center", va="bottom")

    mo.vstack(
        [
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ and $\vec{a} \in \mathbb{R}^n$

    If $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1 \in \mathbb{R}^m$ and $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_2 \in \mathbb{R}^m$ then $\vec{b}_1 = \vec{b}_2$.
    """,
                "Uniqueness of limits",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; limits are unique! (when they exist)

    **Proof.** Given $\vec{b}_1 \neq \vec{b}_2 \in \mathbb{R}^m$ let $\varepsilon = \dfrac{\lVert \vec{b}_2 - \vec{b}_1 \rVert}{2}$

    $$
    \Longrightarrow \qquad B(\vec{b}_1, \varepsilon) \cap B(\vec{b}_2, \varepsilon) = \emptyset
    $$

    (remember: the sphere is not part of the ball; to be more precise we need to use the triangle inequality)
    """
            ),
            _fig,
            mo.md(
                r"""
    $\Longrightarrow$ &nbsp; if $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1$, then there is a $\delta_1 > 0$ such that

    $$
    f\big( B(\vec{a}, \delta_1) \setminus \{\vec{a}\} \big) \subset B(\vec{b}_1, \varepsilon)
    $$

    $\Longrightarrow$ &nbsp; for any $\delta_2 < \delta_1$

    $$
    f\big( B(\vec{a}, \delta_2) \setminus \{\vec{a}\} \big) \not\subset B(\vec{b}_2, \varepsilon)
    \qquad \Longrightarrow \qquad \lim_{\vec{x} \to \vec{a}} f(\vec{x}) \neq \vec{b}_2 \tag*{$\square$}
    $$

    **Example.**

    $$
    f(\vec{x}) = \frac{(x^1)^2}{\lVert \vec{x} \rVert^2} = \frac{(x^1)^2}{(x^1)^2 + (x^2)^2}
    $$

    Claim: $\displaystyle \lim_{\vec{x} \to \vec{0}} f(\vec{x})$ **does not exist**! (it is not well-defined)

    **Proof.** Let's consider two different ways $\vec{x}$ can approach $\vec{0}$

    1. along $\vec{x} = t\vec{e}_1 = \begin{bmatrix} t \\ 0 \end{bmatrix}$ for $t \neq 0$ (since $\vec{x} \neq \vec{0}$)

        $$
        f(t\vec{e}_1) = \frac{t^2}{t^2 + 0^2} = 1 \qquad (\text{constant})
        $$

        For any chosen $\varepsilon > 0$

        $$
        0 < \lVert t\vec{e}_1 - \vec{0} \rVert < \delta \qquad \Longrightarrow \qquad \lVert f(t\vec{e}_1) - 1 \rVert = 0 < \varepsilon
        $$

        for every $\delta > 0$! (since $f(t\vec{e}_1) = 1$ is constant)

        $$
        \therefore \quad \lim_{\substack{\vec{x} \to \vec{0} \\ \vec{x} = t\vec{e}_1}} f(\vec{x}) = 1
        $$

    2. along $\vec{x} = s\vec{e}_2 = \begin{bmatrix} 0 \\ s \end{bmatrix}$ for $s \neq 0$

        $$
        f(s\vec{e}_2) = \frac{0^2}{0^2 + s^2} = 0 \qquad \forall\, s \neq 0
        $$

        For any $\varepsilon > 0$

        $$
        0 < \lVert s\vec{e}_2 - \vec{0} \rVert < \delta \qquad \Longrightarrow \qquad \lVert f(s\vec{e}_2) - 0 \rVert = 0 < \varepsilon
        $$

        for every $\delta > 0$!

        $$
        \therefore \quad \lim_{\substack{\vec{x} \to \vec{0} \\ \vec{x} = s\vec{e}_2}} f(\vec{x}) = 0
        $$

    Two possible values for the limit &nbsp; $\Longrightarrow$ &nbsp; limit is not well-defined! <span class=qed>$\square$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    theta = mo.ui.slider(0, 180, 5, value=0, label=r"$\theta$", show_value=True)
    return (theta,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, arrow, cross_axes, math, mo, np, table, theta):
    _a = math.radians(theta.value)
    _c, _s = math.cos(_a) + 0.0, math.sin(_a) + 0.0
    _c, _s = (0.0 if abs(_c) < 1e-12 else _c), (0.0 if abs(_s) < 1e-12 else _s)
    _val = _c**2

    def _r(x):
        return f"{round(2 * x) / 2 + 0.0:g}" if abs(2 * x - round(2 * x)) < 1e-9 else f"{x:.2f}"

    _fig = Figure(figsize=(FULL, 3.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 0.8])
    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.plot(0.8 * np.cos(_th), 0.8 * np.sin(_th), color=GREY, lw=1.0, ls=(0, (4, 3)))
    _left.plot([-1.1 * _c, 1.1 * _c], [-1.1 * _s, 1.1 * _s], color=BLUE, lw=1.4, zorder=3.5)
    _left.plot(0, 0, "o", color="black", ms=5, mfc="white", mew=1.1, zorder=4)

    _right.set_xlim(-1.2, 1.4)
    _right.set_ylim(-0.5, 1.6)
    _right.axis("off")
    arrow(_right, (0, -0.5), (0, 1.58), "black", lw=0.9)
    _right.text(-0.15, 1.55, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    for _y in (0, 1):
        _right.plot([-0.05, 0.05], [_y, _y], color="black", lw=0.9)
        _right.text(-0.15, _y, f"${_y}$", ha="right", va="center", fontsize=12)
    _right.plot(0, _val, "o", color=GREEN, ms=5, zorder=4)
    _m = math.radians(45 if abs(theta.value - 135) < abs(theta.value - 45) else 135)  # the side the line is not on
    _left.text(0.9 * math.cos(_m), 0.9 * math.sin(_m), r"$B(\vec{0}, \delta)$", color=GREY, fontsize=13, ha="left" if math.cos(_m) > 0 else "right", va="bottom")
    _left.text(0.06 if 0 < theta.value < 90 else -0.06, -0.06, r"$\vec{0}$", fontsize=13, ha="left" if 0 < theta.value < 90 else "right", va="top")
    _right.text(0.1, _val, r"$f(\vec{x})$", color=GREEN, fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.hstack([theta], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(t\vec{u})$ for $\vec{u} = \begin{bmatrix} \cos\theta \\ \sin\theta \end{bmatrix}$", rf"${_r(_val)}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\lambda : \mathbb{R}^n \longrightarrow \mathbb{R}$

    if $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1$, &nbsp; $\displaystyle \lim_{\vec{x} \to \vec{a}} g(\vec{x}) = \vec{b}_2$, &nbsp; $\displaystyle \lim_{\vec{x} \to \vec{a}} \lambda(\vec{x}) = \beta$

    - $\displaystyle \lim_{\vec{x} \to \vec{a}} (f + g)(\vec{x}) = \vec{b}_1 + \vec{b}_2$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} (\lambda f)(\vec{x}) = \beta\, \vec{b}_1$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} (f \cdot g)(\vec{x}) = \vec{b}_1 \cdot \vec{b}_2$
    """,
        "Limits of sums and products",
    )
    return


if __name__ == "__main__":
    app.run()
