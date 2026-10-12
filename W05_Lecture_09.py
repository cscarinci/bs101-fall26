import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 09 · Differentiability and the derivative", css_file="bs101.css")


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
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 09", "Week 05", "Lecture 09 · Differentiability and the derivative")
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
def _(BLUE, FULL, GREEN, RED, arrow, blank, mo, np, vector):
    def _gamma(t):
        return 5.1 + 2.9 * t, 1.7 + 1.0 * np.sin(3.3 * t) - 0.3 * t

    _fig, _ax = blank(FULL, 2.6, (-0.2, 11.7), (-0.55, 3.65))
    # the time axis
    arrow(_ax, (0, 1.2), (3.0, 1.2), "black", lw=0.9)
    for _x, _name in ((1.0, "$a$"), (1.8, "$t$")):
        _ax.plot(_x, 1.2, "o", color="black", ms=4)
        _ax.text(_x, 0.98, _name, ha="center", va="top", fontsize=13)
    arrow(_ax, (3.3, 1.4), (4.0, 1.4), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(3.65, 1.67, r"$\gamma$", fontsize=13, ha="center", va="bottom")
    # the plane with the image of the path
    arrow(_ax, (4.2, 0), (11.5, 0), "black", lw=0.9)
    arrow(_ax, (4.5, -0.3), (4.5, 3.5), "black", lw=0.9)
    _s = np.linspace(0, 1.9, 300)
    _ax.plot(*_gamma(_s), color=BLUE, lw=1.4)
    _a, _t, _h = 0.3, 0.72, 1e-4
    _pa, _pt = _gamma(_a), _gamma(_t)
    _va = ((_gamma(_a + _h)[0] - _pa[0]) / _h, (_gamma(_a + _h)[1] - _pa[1]) / _h)
    arrow(_ax, _pa, _pt, RED)
    vector(_ax, _pa, (_pa[0] + 0.45 * _va[0], _pa[1] + 0.45 * _va[1]), GREEN, r"$\gamma'(a)$", 0, r=20)
    _ax.plot(*_pa, "o", color="black", ms=4, zorder=4)
    _ax.plot(*_pt, "o", color="black", ms=4, zorder=4)
    _ax.annotate(r"$\gamma(a)$", _pa, textcoords="offset points", xytext=(-8, 4), ha="right", va="bottom", fontsize=13)
    _ax.annotate(r"$\gamma(t)$", _pt, textcoords="offset points", xytext=(7, 5), ha="left", va="bottom", fontsize=13)
    _end = _gamma(1.9)
    _ax.text(_end[0] + 0.15, _end[1], r"$\mathrm{Im}(\gamma)$", fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - limits of multivariable functions: &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m, \quad \vec{a} \in \mathbb{R}^n, \quad \vec{b} \in \mathbb{R}^m$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$ &nbsp; if for every $B(\vec{b}, \varepsilon) \subset \mathbb{R}^m$ we can find $B(\vec{a}, \delta) \subset \mathbb{R}^n$ such that $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$
    - $\leadsto$ &nbsp; we can make $f(\vec{x})$ as close as we want to $\vec{b}$ by taking $\vec{x}$ close enough, but different, to $\vec{a}$
    - recall: path in $\mathbb{R}^2$ &nbsp; ($n = 1$, $m = 2$)

        $$
        \gamma : \mathbb{R} \longrightarrow \mathbb{R}^2, \qquad \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix} \in \mathbb{R}^2 \qquad (\text{position of } \gamma \text{ at time } t)
        $$

        $$
        \leadsto \quad \gamma'(a) = \underbrace{\lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}}_{\text{displacement per unit of time}} = \begin{bmatrix} (\gamma^1)'(a) \\ (\gamma^2)'(a) \end{bmatrix} \qquad (\text{velocity of } \gamma \text{ at time } t = a)
        $$
    """
            ),
            _fig,
            mo.md(r"""**In this lecture:** differentiability and the derivative, for $n = 2$, $m = 1$ &nbsp; $\leadsto$ &nbsp; scalar functions on $\mathbb{R}^2$"""),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## II.4 &nbsp; Differentiability and the derivative

    How do we generalize to scalar functions on $\mathbb{R}^2$?

    $\leadsto$ &nbsp; could try

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\vec{x} - \vec{a}}
    $$

    Makes NO sense: we cannot divide by $\vec{x} - \vec{a} \in \mathbb{R}^2$!

    $\leadsto$ &nbsp; could try instead

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert}
    $$

    This makes sense! But if this limit exists (say equal $m \in \mathbb{R}$)

    $$
    \Longrightarrow \quad f(\vec{x}) \approx f(\vec{a}) + m \lVert \vec{x} - \vec{a} \rVert \quad \text{for } \vec{x} \approx \vec{a} \qquad (\text{too restrictive!})
    $$

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 \quad \Longrightarrow \quad
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert}
    = \lim_{\vec{x} \to \vec{a}} \frac{x^1 - a^1}{\lVert \vec{x} - \vec{a} \rVert} \ \text{ does not exist}
    $$

    It depends on how $\vec{x}$ approaches $\vec{a}$:

    $$
    \frac{x^1 - a^1}{\lVert \vec{x} - \vec{a} \rVert}
    \begin{cases} = 1 & \text{along } \vec{x} = \vec{a} + t\vec{e}_1,\ t \to 0^+ \\ = 0 & \text{along } \vec{x} = \vec{a} + s\vec{e}_2 \end{cases}
    $$

    We should hope to give a definition of derivatives for which this simple function is differentiable!
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, RED, arrow, blank, definition, mo):
    _fig, _ax = blank(FULL, 2.9, (-0.7, 9.0), (-0.55, 3.2))
    arrow(_ax, (-0.4, 0), (4.5, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 3.0), "black", lw=0.9)
    _ax.text(4.5, -0.12, "$x^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.12, 3.0, "$x^2$", fontsize=13, ha="right", va="center")
    _a = (1.6, 0.9)
    arrow(_ax, (0.6, _a[1]), (4.0, _a[1]), BLUE)
    arrow(_ax, (_a[0], 0.2), (_a[0], 2.9), RED)
    _ax.text(4.1, _a[1], "$t$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax.text(_a[0], 2.95, "$s$", color=RED, fontsize=13, ha="center", va="bottom")
    for _pt, _name, _off, _ha, _va in (
        (_a, r"$\vec{a}$", (-6, -6), "right", "top"),
        ((2.9, _a[1]), r"$\vec{a} + t\vec{e}_1$", (0, -7), "center", "top"),
        ((_a[0], 2.2), r"$\vec{a} + s\vec{e}_2$", (8, 0), "left", "center"),
    ):
        _ax.plot(*_pt, "o", color="black", ms=4, zorder=4)
        _ax.annotate(_name, _pt, textcoords="offset points", xytext=_off, ha=_ha, va=_va, fontsize=13)
    arrow(_ax, (4.9, 2.0), (5.9, 2.0), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(5.4, 2.32, "$f$", fontsize=13, ha="center", va="bottom")
    # the real line of values
    arrow(_ax, (6.6, -0.4), (6.6, 3.0), "black", lw=0.9)
    for _y, _name in ((2.2, r"$f(\vec{a} + t\vec{e}_1)$"), (1.3, r"$f(\vec{a})$"), (0.5, r"$f(\vec{a} + s\vec{e}_2)$")):
        _ax.plot(6.6, _y, "o", color="black", ms=4, zorder=4)
        _ax.text(6.8, _y, _name, fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.md(r"""### Partial derivatives"""),
            definition(
                r"""
    Given a function $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, the **partial derivative** of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ is

    $$
    \frac{\partial f}{\partial x^1}(\vec{a}) = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{e}_1) - f(\vec{a})}{t}
    $$

    provided that the limit exists.

    $$
    \leadsto \quad \frac{\partial f}{\partial x^1}(\vec{a}) = \underbrace{\frac{d}{dt} f(\vec{a} + t\vec{e}_1) \Big|_{t = 0}}_{\text{real single variable differentiation at } t = 0}
    \qquad \leadsto \quad \underbrace{t \longmapsto f(\vec{a} + t\vec{e}_1)}_{\text{real single variable real valued function!}}
    $$

    Similarly, the partial derivative of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ is

    $$
    \frac{\partial f}{\partial x^2}(\vec{a}) = \lim_{s \to 0} \frac{f(\vec{a} + s\vec{e}_2) - f(\vec{a})}{s}
    $$

    provided that the limit exists.

    $$
    \leadsto \quad \frac{\partial f}{\partial x^2}(\vec{a}) = \frac{d}{ds} f(\vec{a} + s\vec{e}_2) \Big|_{s = 0}
    $$
    """,
                "Partial derivatives",
            ),
            _fig,
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \sin(x^1)$

    $$
    \begin{aligned}
    \Longrightarrow \quad \frac{\partial}{\partial x^1} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + t \\ a^2 + 0 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t}
    = \lim_{t \to 0} \frac{\sin(a^1 + t) - \sin(a^1)}{t} \\[4pt]
    &= \frac{d}{dt} \sin(a^1 + t) \Big|_{t = 0} = \cos(a^1) \\[8pt]
    \frac{\partial}{\partial x^2} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{s \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + 0 \\ a^2 + s \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{s}
    = \lim_{s \to 0} \frac{\sin(a^1) - \sin(a^1)}{s} = 0
    \end{aligned}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) = (a^1)^2 (a^2)^3$

    $$
    \begin{aligned}
    \Longrightarrow \quad \frac{\partial}{\partial x^1} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{t \to 0} \frac{(a^1 + t)^2 (a^2)^3 - (a^1)^2 (a^2)^3}{t}
    = \lim_{t \to 0} \frac{(a^1 + t)^2 - (a^1)^2}{t}\, (a^2)^3 \\[4pt]
    &= \frac{d}{dt} (a^1 + t)^2 \Big|_{t = 0} \cdot (a^2)^3 = 2 (a^1) \cdot (a^2)^3 \\[8pt]
    \frac{\partial}{\partial x^2} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{s \to 0} \frac{(a^1)^2 (a^2 + s)^3 - (a^1)^2 (a^2)^3}{s}
    = (a^1)^2 \cdot \frac{d}{ds} (a^2 + s)^3 \Big|_{s = 0} = 3 (a^1)^2 (a^2)^2
    \end{aligned}
    $$

    $\leadsto$ &nbsp; the partial derivative in the direction of $\vec{e}_i$ is the usual single variable derivative with respect to $x^i$, assuming $x^j$ is held constant ($j \neq i$)

    $\leadsto$ &nbsp; the existence of partial derivatives will be necessary for the notion of differentiability but will not be sufficient &nbsp; $\leadsto$ &nbsp; $f$ could behave badly in other directions!
    """
            ),
            mo.md(r"""### Directional derivatives"""),
            definition(
                r"""
    Given $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, the **directional derivative** of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$ is

    $$
    Df(\vec{a})(\vec{v}) = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{v}) - f(\vec{a})}{t} = \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t = 0}
    $$

    provided the derivative exists.
    """,
                "Directional derivative",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    angle = mo.ui.slider(0, 355, 5, value=30, label=r"direction of $\vec{v}$ (degrees)", show_value=True)
    return (angle,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, angle, math, mo, np, table, vector):
    _th = math.radians(angle.value)
    _v = (round(math.cos(_th), 12) + 0.0, round(math.sin(_th), 12) + 0.0)
    _a = (1.0, 1.0)

    def _f(x1, x2):
        return x1**2 * x2**3

    _D = 2 * _a[0] * _a[1] ** 3 * _v[0] + 3 * _a[0] ** 2 * _a[1] ** 2 * _v[1]

    def _n(x):
        return f"{round(x, 2) + 0.0:.2f}"

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    # level sets of f, the segment a + t v (t in [-1, 1]) and the direction v
    _g = np.linspace(-0.4, 2.4, 200)
    _X, _Y = np.meshgrid(_g, _g)
    _left.contour(_X, _Y, _f(_X, _Y), levels=[-1, -0.3, 0.1, 0.5, 1, 2, 4, 8, 16], colors=GREY, linewidths=0.6, linestyles="solid")
    _left.plot([_a[0] - _v[0], _a[0] + _v[0]], [_a[1] - _v[1], _a[1] + _v[1]], color=BLUE, lw=1.0, ls=(0, (4, 3)))
    vector(_left, _a, (_a[0] + _v[0], _a[1] + _v[1]), BLUE, r"$\vec{v}$")
    _left.plot(*_a, "o", color="black", ms=4, zorder=4)
    _left.annotate(r"$\vec{a}$", _a, textcoords="offset points", xytext=(14 * _v[1], -14 * _v[0]), ha="center", va="center", fontsize=13, zorder=5, bbox=_box)
    _left.text(-0.33, -0.33, "level sets of $f$", color=GREY, fontsize=12, ha="left", va="bottom", bbox=_box)
    _left.set_xlim(-0.4, 2.4)
    _left.set_ylim(-0.4, 2.4)
    _left.set_aspect("equal")
    _left.set_xticks([0, 1, 2])
    _left.set_yticks([0, 1, 2])
    _left.set_xlabel("$x^1$")
    _left.set_ylabel("$x^2$", rotation=0, labelpad=10)

    # the restriction t -> f(a + t v) and its tangent line at t = 0
    _t = np.linspace(-1, 1, 200)
    _right.axhline(0, color="black", lw=0.8)
    _right.axvline(0, color="black", lw=0.8)
    _right.grid(True, color=LIGHT, lw=0.6)
    _right.set_axisbelow(True)
    _right.plot(_t, _f(_a[0] + _t * _v[0], _a[1] + _t * _v[1]), color=BLUE, lw=1.4)
    _right.plot(_t, 1 + _D * _t, color=GREEN, lw=1.4)
    _right.plot(0, 1, "o", color="black", ms=4, zorder=4)
    _right.set_xlim(-1, 1)
    _right.set_ylim(-3, 16)  # holds every value of f(a + t v) and of the tangent line for unit v
    _right.set_xticks([-1, -0.5, 0, 0.5, 1])
    _right.set_yticks([0, 5, 10, 15])
    _right.set_xlabel("$t$")
    # the two labels sit in the upper corner that the graph leaves free
    _free_left = _f(_a[0] + _v[0], _a[1] + _v[1]) >= _f(_a[0] - _v[0], _a[1] - _v[1])
    _x, _ha = (-0.94, "left") if _free_left else (0.94, "right")
    _right.text(_x, 14.9, r"$f(\vec{a} + t\vec{v})$", color=BLUE, fontsize=12, ha=_ha, va="top", bbox=_box)
    _right.text(_x, 12.9, r"$f(\vec{a}) + t\, Df(\vec{a})(\vec{v})$", color=GREEN, fontsize=12, ha=_ha, va="top", bbox=_box)

    mo.vstack(
        [
            mo.hstack([angle], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(\vec{x})$", r"$(x^1)^2 (x^2)^3$"),
                    (r"$\vec{a}$", r"$\begin{bmatrix} 1 \\ 1 \end{bmatrix}$"),
                    (r"$\vec{v}$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_n(_v[0])} \\ {_n(_v[1])} \end{{bmatrix}}}}$"),
                    (r"$Df(\vec{a})(\vec{v})$", rf"$\textcolor{{{GREEN}}}{{{_n(_D)}}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; to call a function $f$ differentiable at $\vec{x} = \vec{a}$ we want also that all directional derivatives for all $\vec{v} \in \mathbb{R}^2$ be well-defined and that

    $$
    Df(\vec{a})(\vec{v}) = \underbrace{v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})}_{\text{linear combination of partial derivatives}}
    $$

    **Remark.** &nbsp; $\dfrac{\partial f}{\partial x^i}(\vec{a}) = Df(\vec{a})(\vec{e}_i)$

    ### Differentiability
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ if the directional derivative

    $$
    Df(\vec{a})(\vec{v})
    $$

    exists for every $\vec{v} = v^1 \vec{e}_1 + v^2 \vec{e}_2 = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \in \mathbb{R}^2$, satisfies

    $$
    \begin{aligned}
    Df(\vec{a})(\vec{v}) = Df(\vec{a})(v^1 \vec{e}_1 + v^2 \vec{e}_2)
    &= v^1\, Df(\vec{a})(\vec{e}_1) + v^2\, Df(\vec{a})(\vec{e}_2) \qquad (\text{linearity in } \vec{v}) \\
    &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})
    \end{aligned}
    $$

    and

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$
    """,
                "Differentiable function",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; now NOT a limit over real numbers! (Stronger than just existence + linearity of directional derivatives.)

    $$
    \Longrightarrow \quad f(\vec{x}) \approx f(\vec{a}) + \underbrace{Df(\vec{a})(\vec{x} - \vec{a})}_{\text{more flexible than } m \lVert \vec{x} - \vec{a} \rVert} \quad \text{for } \vec{x} \approx \vec{a}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$

    $$
    \begin{aligned}
    \Longrightarrow \quad Df(\vec{a})(\vec{v}) &= \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t = 0} = \frac{d}{dt} (a^1 + t v^1) \Big|_{t = 0} = v^1 \\
    &= v^1 \underbrace{\frac{\partial f}{\partial x^1}(\vec{a})}_{= 1} + v^2 \underbrace{\frac{\partial f}{\partial x^2}(\vec{a})}_{= 0} \qquad \forall\, \vec{v}
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 & 0 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}, \quad \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto v^1 \quad (\text{linear in } \vec{v})
    $$

    For the final limit:

    $$
    \frac{f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) - Df(\vec{a})\!\left( \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \end{bmatrix} \right)}{\lVert \vec{x} - \vec{a} \rVert}
    = \frac{x^1 - a^1 - (x^1 - a^1)}{\lVert \vec{x} - \vec{a} \rVert} = 0 \qquad \forall\, \vec{x} \in \mathbb{R}^2 \setminus \{\vec{a}\}
    $$

    $$
    \Longrightarrow \quad \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$

    $\Longrightarrow$ &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$ is differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \in \mathbb{R}^2$!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - dividing by $\vec{x} - \vec{a}$ makes no sense, and dividing by $\lVert \vec{x} - \vec{a} \rVert$ is too restrictive: already $f(\vec{x}) = x^1$ would not be differentiable
    - partial derivatives $\dfrac{\partial f}{\partial x^i}(\vec{a})$: the usual single variable derivative with respect to $x^i$, with $x^j$ held constant ($j \neq i$)
    - directional derivative $Df(\vec{a})(\vec{v}) = \dfrac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t = 0}$, and $\dfrac{\partial f}{\partial x^i}(\vec{a}) = Df(\vec{a})(\vec{e}_i)$
    - $f$ is differentiable at $\vec{a}$ if $Df(\vec{a})(\vec{v})$ exists and is linear in $\vec{v}$, and $\displaystyle \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0$

    **Next:** properties and interpretations of differentiable functions
    """)
    return


if __name__ == "__main__":
    app.run()
