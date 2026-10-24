import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 08 · Local properties of scalar functions and maps: limits", css_file="bs101.css")


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
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#1b458f", "#b3261e", "#2e7d32", "#e65100", "#888888", "#cfe3f5"
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
        One head size and one line weight for every figure, so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>,head_width=0.15,head_length=0.35", "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "correct" if abs(float(s) - answer) < 1e-6 else "try again"
        except ValueError:
            return "enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 08", "Week 04", "Lecture 08 · Local properties of scalar functions and maps: limits")
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

    def legend_box(fig, entries, loc="outside right center", ncols=1):
        """A legend box for the figure, so that no label covers the drawing: entries (kind, colour, label[, style])
        with kind "dot", "ring", "line" (style: line style) or "area" (style: edge colour)."""
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch

        handles = []
        for kind, c, _label, *style in entries:
            if kind == "dot":
                handles.append(Line2D([], [], ls="none", marker="o", ms=6, color=c))
            elif kind == "ring":
                handles.append(Line2D([], [], ls="none", marker="o", ms=6, mfc="white", mec=c, mew=1.3))
            elif kind == "line":
                handles.append(Line2D([], [], color=c, lw=1.6, ls=style[0] if style else "-"))
            else:
                handles.append(Patch(facecolor=c, edgecolor=style[0] if style else c, lw=1.0))
        fig.legend(handles, [e[2] for e in entries], loc=loc, ncols=ncols, fontsize=12, frameon=True, fancybox=False, edgecolor="#c8c8c8")

    return cross_axes, legend_box


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, cross_axes, legend_box, math, mo, np):
    _fig = Figure(figsize=(FULL, 3.6), layout="constrained")
    _sub, _sub2 = _fig.subfigures(1, 2)
    _ax, _ax2 = _sub.subplots(), _sub2.subplots()

    cross_axes(_ax, (-1.9, 1.9), (-0.6, 2.4))
    _t = np.linspace(-1.5, 1.5, 200)
    _ax.plot(_t, _t**2, color=BLUE, lw=1.4)
    _ax.plot(0, 0, "o", color="black", ms=6, mfc="white", mew=1.2, zorder=4)
    _ax.plot(0, 1, "o", color="black", ms=5, zorder=4)
    _ax.plot(-1.2, 1.44, "o", color=BLUE, ms=5, zorder=4)
    legend_box(
        _sub,
        [("line", BLUE, r"$\mathrm{Im}(\gamma)$"), ("dot", BLUE, r"$\genfrac{[}{]}{0}{0}{t}{t^2}$"), ("dot", "black", r"$\genfrac{[}{]}{0}{0}{0}{1}$"), ("ring", "black", "not continuous")],
        loc="outside lower center",
        ncols=2,
    )

    cross_axes(_ax2, (-1.6, 1.9), (-1.5, 1.7))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax2.plot(np.cos(_th), np.sin(_th), color=BLUE, lw=1.4)
    _ax2.plot(1, 0, "o", color=GREEN, ms=5, zorder=4)
    _ax2.plot(0, 1, "o", color="black", ms=5, zorder=4)
    _ax2.plot(math.cos(0.7), math.sin(0.7), "o", color=BLUE, ms=5, zorder=4)
    legend_box(
        _sub2,
        [("line", BLUE, r"$\mathrm{Im}(\sigma)$"), ("dot", BLUE, r"$\genfrac{[}{]}{0}{0}{\cos(t)}{\sin(t)}$"), ("dot", "black", r"$\genfrac{[}{]}{0}{0}{0}{1}$"), ("dot", GREEN, r"$\lim_{t \to 0} \sigma(t)$")],
        loc="outside lower center",
        ncols=2,
    )

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
    - $\leadsto$ &nbsp; $\gamma$ differentiable at $t = a$ if $\displaystyle \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}$ exists &nbsp; ($\gamma'(a)$, the velocity of $\gamma$ at $t = a$)
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
def _(BLUE, GREEN, GREY, HALF, LIGHT, RED, arrow, blank, definition, legend_box, mo, np):
    _fig, _ax = blank(HALF + 1.5, 2.9, (-0.4, 3.8), (-0.4, 3.0))
    arrow(_ax, (-0.3, 0), (3.7, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.3), (0, 2.9), "black", lw=0.9)
    _a, _d = (2.1, 1.5), 1.15
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=LIGHT, lw=0)
    _ax.plot(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _x = (1.35, 2.05)
    _r = (_a[0] + _d * np.cos(-0.5), _a[1] + _d * np.sin(-0.5))
    _ax.plot([_a[0], _r[0]], [_a[1], _r[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    arrow(_ax, (0, 0), _a, "black")
    arrow(_ax, (0, 0), _x, RED)
    arrow(_ax, _a, _x, GREEN)
    legend_box(
        _fig,
        [("line", "black", r"$\vec{a}$"), ("line", RED, r"$\vec{x}$"), ("line", GREEN, r"$\vec{x} - \vec{a}$"), ("line", GREY, r"$\delta$", (0, (4, 3))), ("area", LIGHT, r"$B(\vec{a}, \delta)$", BLUE)],
    )

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
def _(BLUE, FULL, GREEN, LIGHT, RED, arrow, blank, blob, definition, legend_box, mo, np):
    # the ball about a (blue), the image of the punctured ball (green) and the ball about b (red), as in the next figures
    _tint = (0.18, 0.49, 0.2, 0.18)
    _fig, _ax = blank(FULL, 3.4, (-0.5, 10.1), (-0.6, 3.35))
    _th = np.linspace(0, 2 * np.pi, 200)
    # domain
    arrow(_ax, (-0.4, 0), (3.4, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.5), (0, 3.0), "black", lw=0.9)
    _ax.text(-0.15, 3.05, r"$\mathbb{R}^n$", fontsize=13, ha="right", va="center")
    _ax.fill(1.5 + 0.85 * np.cos(_th), 1.75 + 0.85 * np.sin(_th), color=LIGHT, lw=0)
    _ax.plot(1.5 + 0.85 * np.cos(_th), 1.75 + 0.85 * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _ax.plot(1.5, 1.75, "o", color="black", ms=5, zorder=4)
    # the map
    arrow(_ax, (3.7, 2.2), (5.0, 2.2), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(4.35, 2.55, "$f$", fontsize=13, ha="center", va="bottom")
    # codomain
    _o = (6.0, 0.0)
    arrow(_ax, (_o[0] - 0.4, _o[1]), (_o[0] + 3.8, _o[1]), "black", lw=0.9)
    arrow(_ax, (_o[0], _o[1] - 0.5), (_o[0], 3.0), "black", lw=0.9)
    _ax.text(_o[0] - 0.15, 3.05, r"$\mathbb{R}^m$", fontsize=13, ha="right", va="center")
    _c, _r = (7.9, 1.9), 1.2
    _ax.plot(_c[0] + _r * np.cos(_th), _c[1] + _r * np.sin(_th), color=RED, lw=1.2, ls=(0, (4, 3)))
    _bx, _by = blob(7.45, 2.35, 0.48, 0.3, seed=3)
    _ax.fill(_bx, _by, color=_tint, lw=0)
    _ax.plot(_bx, _by, color=GREEN, lw=1.2)
    _ax.plot(8.2, 1.65, "o", color=RED, ms=5, zorder=4)
    legend_box(
        _fig,
        [
            ("area", LIGHT, r"$B(\vec{a}, \delta)$", BLUE),
            ("dot", "black", r"$\vec{a}$"),
            ("line", RED, r"$B(\vec{b}, \varepsilon)$", (0, (4, 3))),
            ("dot", RED, r"$\vec{b}$"),
            ("area", _tint, r"$f(B(\vec{a}, \delta) \setminus \{\vec{a}\})$", GREEN),
        ],
        loc="outside lower center",
        ncols=3,
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
            _fig,
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
        \underbrace{0 < \lVert \vec{x} - \vec{0} \rVert < \delta}_{\text{whenever } \vec{x} \text{ is } \delta\text{-close to } \vec{a} = \vec{0}} \qquad \underbrace{\Longrightarrow}_{\text{we guarantee}} \qquad \underbrace{\lvert f(\vec{x}) - 0 \rvert < \varepsilon = 1}_{f(\vec{x}) \text{ is } 1\text{-close to } b = 0}
        $$

        ($1$-close: as close as we want it)

    For $\vec{x} \neq \vec{0}$

    $$
    \lvert f(\vec{x}) - 0 \rvert = \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} \leq \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} + \frac{2 (x^2)^2}{\lVert \vec{x} \rVert} = 2\, \frac{\lVert \vec{x} \rVert^2}{\lVert \vec{x} \rVert} = 2 \lVert \vec{x} \rVert
    $$

    $$
    \Longrightarrow \qquad \lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert = 2 \lVert \vec{x} - \vec{0} \rVert
    $$

    $\Longrightarrow$ &nbsp; whenever we make $0 < \lVert \vec{x} - \vec{0} \rVert < \tfrac{1}{2} = \delta$ (for $\varepsilon = 1$) we guarantee that $\lvert f(\vec{x}) - 0 \rvert < 1$!

    Now repeat the argument for every $\varepsilon > 0$ &nbsp; ($\varepsilon = \tfrac{1}{2} \leadsto \delta = \tfrac{1}{4}$, &nbsp; $\varepsilon = \tfrac{1}{3} \leadsto \delta = \tfrac{1}{6}$, &nbsp; …)

    $\therefore$ &nbsp; if $0 < \lVert \vec{x} - \vec{0} \rVert < \tfrac{\varepsilon}{2} = \delta$

    $$
    \Longrightarrow \qquad \lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert < 2 \cdot \tfrac{\varepsilon}{2} = \varepsilon \qquad \square
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
def _(BLUE, FULL, Figure, GREEN, LIGHT, RED, arrow, cross_axes, eps, legend_box, mo, np, table):
    _e = eps.value
    _d = _e / 2
    _fig = Figure(figsize=(FULL, 3.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 0.8])

    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.fill(_d * np.cos(_th), _d * np.sin(_th), color=LIGHT, lw=0, zorder=0)
    _left.plot(_d * np.cos(_th), _d * np.sin(_th), color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _left.plot(0, 0, "o", color="black", ms=5, mfc="white", mew=1.1, zorder=4)

    _right.set_xlim(-1.0, 1.4)
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
    legend_box(
        _fig,
        [
            ("area", LIGHT, r"$B(\vec{0}, \delta) \setminus \{\vec{0}\}$", BLUE),
            ("ring", "black", r"$\vec{0}$"),
            ("dot", "black", r"$f(\vec{0})$"),
            ("line", GREEN, r"$f(B(\vec{0}, \delta) \setminus \{\vec{0}\})$"),
            ("line", RED, r"$B(0, \varepsilon)$"),
        ],
        loc="outside lower center",
        ncols=3,
    )

    mo.vstack(
        [
            mo.hstack([eps], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\delta = \varepsilon / 2$", rf"${_d:g}$"),
                    (r"$f\big( B(\vec{0}, \delta) \setminus \{\vec{0}\} \big)$", rf"$\textcolor{{{GREEN}}}{{[0,\, {_e:g})}}$"),
                    (r"$B(0, \varepsilon)$", rf"$\textcolor{{{RED}}}{{({-_e:g},\, {_e:g})}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, LIGHT, ORANGE, RED, arrow, blank, blob, legend_box, mo, np, theorem):
    _tint = (0.18, 0.49, 0.2, 0.18)
    _fig, _ax = blank(FULL, 3.3, (-0.3, 9.1), (0.2, 2.75))
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
    legend_box(
        _fig,
        [
            ("area", LIGHT, r"$B(\vec{a}, \delta)$", BLUE),
            ("dot", "black", r"$\vec{a}$"),
            ("line", GREY, r"$\delta$, $\varepsilon$", (0, (4, 3))),
            ("area", _tint, r"$f(B(\vec{a}, \delta) \setminus \{\vec{a}\})$", GREEN),
            ("line", RED, r"$B(\vec{b}_1, \varepsilon)$", (0, (4, 3))),
            ("dot", RED, r"$\vec{b}_1$"),
            ("line", ORANGE, r"$B(\vec{b}_2, \varepsilon)$", (0, (4, 3))),
            ("dot", ORANGE, r"$\vec{b}_2$"),
        ],
        loc="outside lower center",
        ncols=4,
    )

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
    \qquad \Longrightarrow \qquad \lim_{\vec{x} \to \vec{a}} f(\vec{x}) \neq \vec{b}_2 \qquad \square
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

    Two possible values for the limit &nbsp; $\Longrightarrow$ &nbsp; limit is not well-defined! $\square$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    theta = mo.ui.slider(0, 180, 5, value=0, label=r"direction (degrees from $\vec{e}_1$)", show_value=True)
    return (theta,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, arrow, cross_axes, legend_box, math, mo, np, table, theta):
    _a = math.radians(theta.value)
    _c, _s = math.cos(_a) + 0.0, math.sin(_a) + 0.0
    _c, _s = (0.0 if abs(_c) < 1e-12 else _c), (0.0 if abs(_s) < 1e-12 else _s)
    _val = _c**2

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
    legend_box(
        _fig,
        [
            ("line", GREY, r"$B(\vec{0}, \delta)$", (0, (4, 3))),
            ("line", BLUE, rf"$\vec{{x}} = t \genfrac{{[}}{{]}}{{0}}{{0}}{{{_c:.2f}}}{{{_s:.2f}}}, \ t \neq 0$"),
            ("ring", "black", r"$\vec{0}$"),
            ("dot", GREEN, rf"$f(\vec{{x}}) = {_val:.2f}$"),
        ],
        loc="outside lower center",
        ncols=2,
    )

    mo.vstack(
        [
            mo.hstack([theta], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"direction", rf"$\textcolor{{{BLUE}}}{{\vec{{x}} = t \begin{{bmatrix}} {_c:.2f} \\ {_s:.2f} \end{{bmatrix}}, \ t \neq 0}}$"),
                    (r"$f(\vec{x})$ along this line", rf"$\textcolor{{{GREEN}}}{{{_val:.2f}}}$"),
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - the open ball $B(\vec{a}, \delta) = \{\, \vec{x} \in \mathbb{R}^n \mid \lVert \vec{x} - \vec{a} \rVert < \delta \,\}$ does not include its “boundary”, the sphere $S(\vec{a}, \delta)$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$ if for every $\varepsilon > 0$ we can find $\delta > 0$ such that $f\big( B(\vec{a}, \delta) \setminus \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$
    - limits are unique (when they exist)
    - two different ways of approaching $\vec{a}$ with two different values &nbsp; $\Longrightarrow$ &nbsp; the limit does not exist
    - limits of $f + g$, $\lambda f$ and $f \cdot g$ are the sum, the scalar multiple and the dot product of the limits
    """)
    return


if __name__ == "__main__":
    app.run()
