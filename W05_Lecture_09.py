import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 09 • Differentiability and the derivative", css_file="bs101.css")


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
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 09", "Week 05", "Lecture 09 • Differentiability and the derivative")
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
def _(mo):
    last_t = mo.ui.slider(0.4, 5, 0.05, value=3, label=r"$t$", show_value=True)
    return (last_t,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, RED, arrow, blank, last_t, mo, np, vector):
    # the path: three cubic pieces, two units of time each (t in [0, 6]), through the points _K with the velocities _V
    # there (the start, the right end of the arch, the lowest point, the end)
    _K = np.array([(5.05, 1.45), (8.35, 2.6), (6.8, 0.6), (10.55, 1.8)])
    _V = np.array([(0.4, 4.5), (-0.6, -3.0), (4.0, 0.0), (2.0, -1.5)])

    def _gamma(t):
        _u = np.asarray(t, float) / 2
        _i = np.clip(np.floor(_u).astype(int), 0, 2)
        _u = (_u - _i)[..., None]
        _g = (2 * _u**3 - 3 * _u**2 + 1) * _K[_i] + (_u**3 - 2 * _u**2 + _u) * _V[_i] + (3 * _u**2 - 2 * _u**3) * _K[_i + 1] + (_u**3 - _u**2) * _V[_i + 1]
        return _g[..., 0], _g[..., 1]

    _fig, _ax = blank(FULL, 3.5, (-0.2, 11.7), (-0.55, 4.25))
    # the time axis
    arrow(_ax, (0, 1.2), (3.0, 1.2), "black", lw=0.9)
    _a, _t, _h = 0.8, last_t.value, 1e-4
    _near = abs(_t - _a) < 0.9  # t this close to a: no room for the names of t and gamma(t) beside a and gamma(a)
    _ax.plot(0.2 + 0.43 * _t, 1.2, "o", color=RED, ms=4)
    _ax.plot(0.2 + 0.43 * _a, 1.2, "o", color="black", ms=4)
    _ax.text(0.2 + 0.43 * _a, 0.98, "$a$", ha="center", va="top", fontsize=13)
    if abs(_t - _a) >= 0.45:
        _ax.text(0.2 + 0.43 * _t, 0.98, "$t$", ha="center", va="top", fontsize=13)
    arrow(_ax, (3.3, 1.4), (4.0, 1.4), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(3.65, 1.67, r"$\gamma$", fontsize=13, ha="center", va="bottom")
    # the plane with the image of the path
    arrow(_ax, (4.2, 0), (11.5, 0), "black", lw=0.9)
    arrow(_ax, (4.5, -0.3), (4.5, 3.5), "black", lw=0.9)
    _s = np.linspace(0, 6, 600)
    _ax.plot(*_gamma(_s), color=BLUE, lw=1.4)
    _pa, _pt = _gamma(_a), _gamma(_t)
    _va = ((_gamma(_a + _h)[0] - _pa[0]) / _h, (_gamma(_a + _h)[1] - _pa[1]) / _h)
    if _t != _a:
        _q = ((_pt[0] - _pa[0]) / (_t - _a), (_pt[1] - _pa[1]) / (_t - _a))
        arrow(_ax, _pa, (_pa[0] + _q[0], _pa[1] + _q[1]), RED)
    vector(_ax, _pa, (_pa[0] + _va[0], _pa[1] + _va[1]), GREEN, r"$\gamma'(a)$", 0, r=20)
    _ax.plot(*_pa, "o", color="black", ms=4, zorder=4)
    _ax.plot(*_pt, "o", color=RED, ms=4, zorder=4)
    _end = _gamma(6)
    _ax.text(_end[0] + 0.15, _end[1], r"$\mathrm{Im}(\gamma)$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax.text(_pa[0] - 0.08, _pa[1] + 0.1, r"$\gamma(a)$", fontsize=13, ha="right", va="bottom")
    # the red arrow named once, fixed, below gamma(a) inside the arch
    _ax.text(_pa[0] + 0.17, _pa[1] - 0.92, r"$\dfrac{\gamma(t) - \gamma(a)}{t - a}$", color=RED, fontsize=13, ha="center", va="top")
    if not _near:
        # gamma(t) named just past its point, away from gamma(a)
        _d = np.array((_pt[0] - _pa[0], _pt[1] - _pa[1])) / np.hypot(_pt[0] - _pa[0], _pt[1] - _pa[1])
        _ax.annotate(r"$\gamma(t)$", _pt, textcoords="offset points", xytext=(24 * _d[0], 17 * _d[1]), fontsize=13, ha="center", va="center", zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - limits of multivariable functions: &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m, \quad \vec{a} \in \mathbb{R}^n, \quad \vec{b} \in \mathbb{R}^m$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$ &nbsp; if for every $B(\vec{b}, \varepsilon) \subset \mathbb{R}^m$ we can find $B(\vec{a}, \delta) \subset \mathbb{R}^n$ such that $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$
    - $\leadsto$ &nbsp; we can make $f(\vec{x})$ as close as we want to $\vec{b}$ by taking $\vec{x}$ close enough to, but different from, $\vec{a}$
    - recall: path in $\mathbb{R}^2$ &nbsp; ($n = 1$, $m = 2$)

        $$
        \gamma : \mathbb{R} \longrightarrow \mathbb{R}^2, \qquad \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix} \in \mathbb{R}^2 \qquad (\text{position of } \gamma \text{ at time } t)
        $$

        $$
        \leadsto \qquad \gamma'(a) = \underbrace{\lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}}_{\mathclap{\footnotesize \text{displacement per unit of time}}\vphantom{\footnotesize \text{displacement per unit of time}}} = \begin{bmatrix} (\gamma^1)'(a) \\ (\gamma^2)'(a) \end{bmatrix} \qquad (\text{velocity of } \gamma \text{ at time } t = a)
        $$
    """
            ),
            last_t,
            _fig,
            mo.md(r"""**In this lecture:** differentiability and the derivative, for $n = 2$, $m = 1$ &nbsp; $\leadsto$ &nbsp; scalar functions on $\mathbb{R}^2$

            **References:** MT 2.3, 2.6""").style({"display": "block"}),
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
    \Longrightarrow \qquad f(\vec{x}) \approx f(\vec{a}) + m \lVert \vec{x} - \vec{a} \rVert \quad \text{for } \vec{x} \approx \vec{a} \qquad (\text{too restrictive!})
    $$

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 \qquad \Longrightarrow \qquad
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
    _fig, _ax = blank(FULL, 3.4, (-0.7, 9.0), (-0.55, 3.2))
    arrow(_ax, (-0.4, 0), (4.5, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 3.0), "black", lw=0.9)
    _ax.text(4.5, -0.12, "$x^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.12, 3.0, "$x^2$", fontsize=13, ha="right", va="center")
    _a = (1.6, 0.9)
    arrow(_ax, (0.6, _a[1]), (4.0, _a[1]), BLUE)
    arrow(_ax, (_a[0], 0.2), (_a[0], 2.9), RED)
    _ax.text(4.1, _a[1], "$t$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax.text(_a[0], 2.95, "$s$", color=RED, fontsize=13, ha="center", va="bottom")
    # the points and their values, coloured as the line they lie on
    for _pt, _c in ((_a, "black"), ((2.9, _a[1]), BLUE), ((_a[0], 2.2), RED)):
        _ax.plot(*_pt, "o", color=_c, ms=4, zorder=4)
    arrow(_ax, (4.9, 2.0), (5.9, 2.0), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(5.4, 2.32, "$f$", fontsize=13, ha="center", va="bottom")
    # the real line of values
    arrow(_ax, (6.6, -0.4), (6.6, 3.0), "black", lw=0.9)
    for _y, _c in ((2.2, BLUE), (1.3, "black"), (0.5, RED)):
        _ax.plot(6.6, _y, "o", color=_c, ms=4, zorder=4)
    _ax.text(_a[0] - 0.08, _a[1] - 0.08, r"$\vec{a}$", fontsize=13, ha="right", va="top")
    _ax.text(2.9, _a[1] + 0.1, r"$\vec{a} + t\vec{e}_1$", fontsize=13, ha="center", va="bottom")
    _ax.text(_a[0] + 0.1, 2.2, r"$\vec{a} + s\vec{e}_2$", fontsize=13, ha="left", va="center")
    for _y, _c, _name in ((2.2, BLUE, r"$f(\vec{a} + t\vec{e}_1)$"), (1.3, "black", r"$f(\vec{a})$"), (0.5, RED, r"$f(\vec{a} + s\vec{e}_2)$")):
        _ax.text(6.75, _y, _name, fontsize=13, ha="left", va="center")

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
    \leadsto \qquad \frac{\partial f}{\partial x^1}(\vec{a}) = \underbrace{\frac{d}{dt} f(\vec{a} + t\vec{e}_1) \Big|_{t = 0}}_{\mathclap{\footnotesize \begin{matrix}\text{real single variable} \\ \text{differentiation at } t = 0\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{real single variable} \\ \text{differentiation at } t = 0\end{matrix}}}
    \qquad \leadsto \qquad \underbrace{t \longmapsto f(\vec{a} + t\vec{e}_1)}_{\mathclap{\footnotesize \begin{matrix}\text{real single variable} \\ \text{real valued function!}\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{real single variable} \\ \text{real valued function!}\end{matrix}}}
    $$

    Similarly, the partial derivative of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ is

    $$
    \frac{\partial f}{\partial x^2}(\vec{a}) = \lim_{s \to 0} \frac{f(\vec{a} + s\vec{e}_2) - f(\vec{a})}{s}
    $$

    provided that the limit exists.

    $$
    \leadsto \qquad \frac{\partial f}{\partial x^2}(\vec{a}) = \frac{d}{ds} f(\vec{a} + s\vec{e}_2) \Big|_{s = 0}
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
    \Longrightarrow \qquad \frac{\partial}{\partial x^1} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
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
    \Longrightarrow \qquad \frac{\partial}{\partial x^1} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
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
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; to call a function $f$ differentiable at $\vec{x} = \vec{a}$ we want also that all directional derivatives for all $\vec{v} \in \mathbb{R}^2$ be well-defined and that

    $$
    Df(\vec{a})(\vec{v}) = \underbrace{v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})}_{\mathclap{\footnotesize \text{linear combination of partial derivatives}}\vphantom{\footnotesize \text{linear combination of partial derivatives}}}
    $$

    **Remark.** &nbsp; $\dfrac{\partial f}{\partial x^i}(\vec{a}) = Df(\vec{a})(\vec{e}_i)$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **continuous** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ if

    $$
    \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = f(\vec{a})
    $$
    """,
                "Continuity",
            ),
            mo.md(r"""### Differentiability"""),
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
    \Longrightarrow \qquad f(\vec{x}) \approx f(\vec{a}) + \underbrace{Df(\vec{a})(\vec{x} - \vec{a})}_{\mathclap{\footnotesize \text{more flexible than } m \lVert \vec{x} - \vec{a} \rVert}\vphantom{\footnotesize \text{more flexible than } m \lVert \vec{x} - \vec{a} \rVert}} \quad \text{for } \vec{x} \approx \vec{a}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$

    $$
    \begin{aligned}
    \Longrightarrow \qquad Df(\vec{a})(\vec{v}) &= \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t = 0} = \frac{d}{dt} (a^1 + t v^1) \Big|_{t = 0} = v^1 \\
    &= v^1 \underbrace{\frac{\partial f}{\partial x^1}(\vec{a})}_{\mathclap{\footnotesize = 1}\vphantom{\footnotesize = 1}} + v^2 \underbrace{\frac{\partial f}{\partial x^2}(\vec{a})}_{\mathclap{\footnotesize = 0}\vphantom{\footnotesize = 0}} \qquad \forall\, \vec{v}
    \end{aligned}
    $$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 & 0 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}, \quad \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto v^1 \quad (\text{linear in } \vec{v})
    $$

    For the final limit:

    $$
    \frac{f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) - Df(\vec{a})\!\left( \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \end{bmatrix} \right)}{\lVert \vec{x} - \vec{a} \rVert}
    = \frac{x^1 - a^1 - (x^1 - a^1)}{\lVert \vec{x} - \vec{a} \rVert} = 0 \qquad \forall\, \vec{x} \in \mathbb{R}^2 \setminus \{\vec{a}\}
    $$

    $$
    \Longrightarrow \qquad \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$

    $\Longrightarrow$ &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$ is differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \in \mathbb{R}^2$!
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
