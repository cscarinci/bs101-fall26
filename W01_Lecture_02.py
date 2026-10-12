import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 02 · The Euclidean inner product (the dot product)", css_file="bs101.css")


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
    header("Lecture 02", "Week 01", "Lecture 02 · The Euclidean inner product (the dot product)")
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
    mo.md(r"""
    ## Last time

    - points in $n$-space $\mathbb{R}^n \ni \vec{x} = (x^1, x^2, \dots, x^n)$ = $n$-vectors (arrows between points); each entry is a real number, $x^2$ is the 2nd component of $\vec{x}$
    - vector addition ${+} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n$ and scalar–vector multiplication $\cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n$, both componentwise
    - $\leadsto$ &nbsp; allow us to do calculations with vectors the same way as with real numbers!

    **In this lecture:** extra structure on $\mathbb{R}^n$ (needed for “measurements”)
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, note, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## I.2 &nbsp; The Euclidean inner product (the dot product)

    ### The dot product
    """
            ),
            definition(
                r"""
    Given two vectors

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}, \quad
    \vec{y} = \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} \in \mathbb{R}^n
    $$

    we define their **dot product** or **inner product** as the real number

    $$
    \vec{x} \cdot \vec{y} = \underbrace{x^1 y^1 + x^2 y^2 + \dots + x^n y^n}_{\text{sum of products of components}} \in \mathbb{R}
    $$
    """,
                "Dot product",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; another extension of multiplication of real numbers, now to pairs of vectors, and taking scalar values

    $$
    \cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}
    $$
    """
            ),
            note(
                r"""
    This “$\cdot$” is **not** the same as for scalar–vector multiplication! To avoid confusion, we drop the “$\cdot$” for scalar–vector multiplication and write

    $$
    \alpha \vec{x} = \alpha \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \vdots \\ \alpha x^n \end{bmatrix}
    $$
    """
            ),
            theorem(
                r"""
    For all vectors $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and scalars $\alpha, \beta \in \mathbb{R}$

    1. $\vec{x} \cdot \vec{y} = \vec{y} \cdot \vec{x}$ &nbsp; (**symmetric**)
    2. $(\alpha \vec{x} + \beta \vec{y}) \cdot \vec{z} = \alpha\, \vec{x} \cdot \vec{z} + \beta\, \vec{y} \cdot \vec{z}$ and
       $\vec{x} \cdot (\alpha \vec{y} + \beta \vec{z}) = \alpha\, \vec{x} \cdot \vec{y} + \beta\, \vec{x} \cdot \vec{z}$
       &nbsp; (linear in each of its 2 arguments: **bilinear**; this is also a distributivity property)
    3. $\vec{x} \cdot \vec{x} \geq 0$, with “$=$” if and only if $\vec{x} = \vec{0}$ &nbsp; (**positive definite**)
    """,
                "Basic properties",
            ),
            mo.md(r"**Proof.** Exercise (using definitions and properties of real numbers). $\square$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Arc, BLUE, GREEN, HALF, RED, arrow, blank, definition, math, mo):
    _fig, _ax = blank(HALF, 2.5, (-0.6, 4.0), (-0.55, 2.6))
    arrow(_ax, (-0.4, 0), (3.8, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 2.45), "black", lw=0.9)
    for _t in (1, 3):
        _ax.plot([_t, _t], [-0.05, 0.05], color="black", lw=0.9)
        _ax.text(_t, -0.14, f"${_t}$", fontsize=12, ha="center", va="top")
    _ax.plot([-0.05, 0.05], [math.sqrt(3)] * 2, color="black", lw=0.9)
    _ax.text(-0.14, math.sqrt(3), r"$\sqrt{3}$", fontsize=12, ha="right", va="center")
    _ax.text(-0.14, -0.14, "$0$", fontsize=12, ha="right", va="top")
    arrow(_ax, (0, 0), (3, 0), BLUE)
    arrow(_ax, (0, 0), (1, math.sqrt(3)), RED)
    _ax.text(2.2, 0.14, r"$\vec{x}$", color=BLUE, fontsize=13, ha="center", va="bottom")
    _ax.text(0.38, 1.1, r"$\vec{y}$", color=RED, fontsize=13, ha="right", va="center")
    _ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=0, theta2=60, color=GREEN, lw=1.4))
    _ax.text(0.68, 0.34, r"$\theta = \pi/3$", color=GREEN, fontsize=12, ha="left", va="center")

    mo.vstack(
        [
            mo.md(r"""### Norm and angle"""),
            definition(
                r"""
    The **norm** (length) of a vector $\vec{x}$ is

    $$
    \lVert \vec{x} \rVert := \sqrt{\vec{x} \cdot \vec{x}} \qquad (\text{makes sense since } \vec{x} \cdot \vec{x} \geq 0)
    $$

    The **angle** between two vectors $\vec{x}, \vec{y}$ is

    $$
    \theta(\vec{x}, \vec{y}) = \arccos\!\left( \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \right)
    \qquad (\text{must have } \vec{x}, \vec{y} \neq \vec{0})
    $$
    """,
                "Norm and angle",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; not so clear why this makes sense… &nbsp; ($\arccos : [-1, 1] \longrightarrow [0, \pi]$)

    **Example.** &nbsp; $\vec{x} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}, \quad \vec{y} = \begin{bmatrix} 1 \\ \sqrt{3} \end{bmatrix}$
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \lVert \vec{x} \rVert = \sqrt{(3)^2 + (0)^2} = 3, \qquad
    \lVert \vec{y} \rVert = \sqrt{(1)^2 + (\sqrt{3})^2} = 2, \qquad
    \vec{x} \cdot \vec{y} = 3 \cdot 1 + 0 \cdot \sqrt{3} = 3
    $$

    $$
    \Longrightarrow \quad \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} = \frac{1}{2} = \cos\!\left(\frac{\pi}{3}\right)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    x1 = mo.ui.slider(-4, 4, 0.5, value=3, label="$x^1$", show_value=True)
    x2 = mo.ui.slider(-4, 4, 0.5, value=0, label="$x^2$", show_value=True)
    y1 = mo.ui.slider(-4, 4, 0.5, value=1, label="$y^1$", show_value=True)
    y2 = mo.ui.slider(-4, 4, 0.5, value=2, label="$y^2$", show_value=True)
    controls = mo.hstack([x1, x2, y1, y2], justify="start", gap=2, wrap=True)
    return controls, x1, x2, y1, y2


@app.cell(hide_code=True)
def _(np, x1, x2, y1, y2):
    x = np.array([x1.value, x2.value], dtype=float)
    y = np.array([y1.value, y2.value], dtype=float)
    dot = float(x @ y)
    nx = float(np.sqrt(x @ x))
    ny = float(np.sqrt(y @ y))
    nonzero = nx > 0 and ny > 0
    return dot, nonzero, nx, ny, x, y


@app.cell(hide_code=True)
def _(Arc, BLUE, Figure, GREEN, HALF, RED, controls, dot, math, mo, nonzero, nx, ny, plane, table, vector, x, y):
    _fig = Figure(figsize=(HALF, HALF), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 6)
    _ax.set_xticks(range(-4, 5, 2))
    _ax.set_yticks(range(-4, 5, 2))
    _side = -1 if x[0] * y[1] - x[1] * y[0] < 0 else 1  # labels go on the outer side of each arrow
    vector(_ax, (0, 0), tuple(x), BLUE, r"$\vec{x}$", -75 * _side)
    vector(_ax, (0, 0), tuple(y), RED, r"$\vec{y}$", 75 * _side)

    _need = r"need $\vec{x}, \vec{y} \neq \vec{0}$"
    if nonzero:
        _cos = max(-1.0, min(1.0, dot / (nx * ny)))  # guards arccos against rounding only
        _theta = math.acos(_cos)
        _a1 = math.degrees(math.atan2(x[1], x[0]))
        _a2 = math.degrees(math.atan2(y[1], y[0]))
        if (_a2 - _a1) % 360 > 180:
            _a1, _a2 = _a2, _a1
        _ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=_a1, theta2=_a2, color=GREEN, lw=1.4))
        _quotient = rf"${_cos:.3f}$"
        _angle = rf"$\textcolor{{{GREEN}}}{{{_theta:.3f} \text{{ rad}} = {math.degrees(_theta):.1f}^\circ}}$"
    else:
        _quotient = _angle = _need

    mo.vstack(
        [
            controls,
            table(
                [
                    (r"$\vec{x}\cdot\vec{y}$", rf"$\textcolor{{{BLUE}}}{{({x[0]:g})}}\textcolor{{{RED}}}{{({y[0]:g})}} + \textcolor{{{BLUE}}}{{({x[1]:g})}}\textcolor{{{RED}}}{{({y[1]:g})}} = {dot:g}$"),
                    (r"$\lVert\vec{x}\rVert$", rf"$\textcolor{{{BLUE}}}{{{nx:.3f}}}$"),
                    (r"$\lVert\vec{y}\rVert$", rf"$\textcolor{{{RED}}}{{{ny:.3f}}}$"),
                    (r"$\dfrac{\vec{x}\cdot\vec{y}}{\lVert\vec{x}\rVert\,\lVert\vec{y}\rVert}$", _quotient),
                    (r"$\theta(\vec{x},\vec{y})$", _angle),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### The Cauchy–Schwarz inequality"""),
            theorem(
                r"""
    For every $\vec{x}, \vec{y} \in \mathbb{R}^n$

    $$
    (\vec{x} \cdot \vec{y})^2 \leq \lVert \vec{x} \rVert^2\, \lVert \vec{y} \rVert^2
    $$

    with “$=$” if and only if $\vec{x}, \vec{y}$ are proportional.
    """,
                "Cauchy–Schwarz inequality",
            ),
            mo.md(
                r"""
    $$
    \Longrightarrow \quad \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \in [-1, 1] \qquad \forall\, \vec{x}, \vec{y} \neq \vec{0}
    $$

    $\leadsto$ &nbsp; our definition of angles really makes sense!

    **Proof.** If $\vec{x} = \vec{0}$ or $\vec{y} = \vec{0}$ &nbsp; $\Longrightarrow$ &nbsp; $(\vec{x} \cdot \vec{y})^2 = 0 = \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2$

    Assume both $\vec{x}, \vec{y} \neq \vec{0}$ and compute $\lVert t\vec{x} + \vec{y} \rVert^2$ for $t \in \mathbb{R}$

    1. positive definite implies

        $$
        \lVert t\vec{x} + \vec{y} \rVert^2 \geq 0, \quad \text{with ``$=$'' if and only if } \underbrace{t\vec{x} + \vec{y} = \vec{0}}_{\vec{x},\, \vec{y} \text{ proportional}}
        $$

    2. bilinearity and symmetry give

        $$
        \begin{aligned}
        \lVert t\vec{x} + \vec{y} \rVert^2 &= (t\vec{x} + \vec{y}) \cdot (t\vec{x} + \vec{y}) = t^2\, \vec{x} \cdot \vec{x} + t\, \vec{x} \cdot \vec{y} + t\, \vec{y} \cdot \vec{x} + \vec{y} \cdot \vec{y} \\
        &= \underbrace{t^2 \lVert \vec{x} \rVert^2 + 2t\, \vec{x} \cdot \vec{y} + \lVert \vec{y} \rVert^2}_{\text{quadratic polynomial in } t}
        \end{aligned}
        $$

    $$
    \Longrightarrow \quad t^2 \lVert \vec{x} \rVert^2 + 2t\, (\vec{x} \cdot \vec{y}) + \lVert \vec{y} \rVert^2 \geq 0
    $$

    with “$=$” for some $t$ if and only if $\vec{x}, \vec{y}$ are proportional

    $$
    \Longrightarrow \quad \text{discriminant:} \quad \big(2 (\vec{x} \cdot \vec{y})\big)^2 - 4 \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2 \leq 0
    $$

    with “$=$” if and only if $\vec{x}, \vec{y}$ are proportional. $\square$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, controls, dot, mo, np, nx, ny, table):
    _disc = (2 * dot) ** 2 - 4 * nx**2 * ny**2
    _vertex = -dot / nx**2 if nx > 0 else 0.0
    _t = np.sort(np.append(np.linspace(min(-4, _vertex - 2), max(4, _vertex + 2), 400), _vertex))
    _p = _t**2 * nx**2 + 2 * _t * dot + ny**2

    _fig = Figure(figsize=(HALF, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_t, _p, color=BLUE)
    _ax.plot(_vertex, float(_p.min()), "o", color="black", ms=4, zorder=4)
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.grid(True, color=LIGHT, lw=0.6)
    _ax.set_axisbelow(True)
    _upper = max(30.0, 1.25 * float(_p.min()) + 2)
    _ax.set_ylim(-0.05 * _upper, _upper)
    _ax.set_xlabel("$t$")
    _ax.set_ylabel(r"$\|t\vec{x} + \vec{y}\|^2$")

    mo.vstack(
        [
            controls,
            table(
                [
                    (r"$(\vec{x}\cdot\vec{y})^2$", rf"${dot**2:g}$"),
                    (r"$\lVert\vec{x}\rVert^2\lVert\vec{y}\rVert^2$", rf"${nx**2 * ny**2:g}$"),
                    (r"discriminant $\big(2 (\vec{x} \cdot \vec{y})\big)^2 - 4 \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2$", rf"${_disc:g}$"),
                    (r"minimum of $\lVert t\vec{x} + \vec{y} \rVert^2$", rf"${float(_p.min()) + 0.0:.3f}$"),
                    (r"$\vec{x}, \vec{y}$ proportional", "yes" if abs(_disc) < 1e-9 else "no"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, RED, controls, mo, np, nx, ny, plane, table, theorem, vector, x, y):
    _s = x + y
    _ns = float(np.sqrt(_s @ _s))

    _fig = Figure(figsize=(HALF, HALF), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 11.5)
    _ax.set_xticks(range(-8, 9, 4))
    _ax.set_yticks(range(-8, 9, 4))
    vector(_ax, tuple(x), tuple(_s), RED, linestyle=(0, (4, 3)))  # y translated to the tip of x
    vector(_ax, (0, 0), tuple(_s), GREEN, r"$\vec{x}+\vec{y}$", 0, r=24)
    _side = -1 if x[0] * y[1] - x[1] * y[0] < 0 else 1  # labels go on the outer side of each arrow
    vector(_ax, (0, 0), tuple(x), BLUE, r"$\vec{x}$", -75 * _side)
    vector(_ax, (0, 0), tuple(y), RED, r"$\vec{y}$", 75 * _side)

    mo.vstack(
        [
            mo.md(r"""### The triangle inequality"""),
            theorem(
                r"""
    For every $\vec{x}, \vec{y} \in \mathbb{R}^n$

    $$
    \lVert \vec{x} + \vec{y} \rVert \leq \lVert \vec{x} \rVert + \lVert \vec{y} \rVert
    $$
    """,
                "Triangle inequality",
            ),
            mo.md(r"**Proof.** Direct consequence of the Cauchy–Schwarz inequality! Exercise. $\square$"),
            controls,
            table(
                [
                    (r"$\lVert\vec{x}+\vec{y}\rVert$", rf"$\textcolor{{{GREEN}}}{{{_ns:.3f}}}$"),
                    (r"$\lVert\vec{x}\rVert+\lVert\vec{y}\rVert$", rf"$\textcolor{{{BLUE}}}{{{nx:.3f}}} + \textcolor{{{RED}}}{{{ny:.3f}}} = {nx + ny:.3f}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Orthogonal vectors"""),
            definition(
                r"""
    $\vec{x}, \vec{y} \in \mathbb{R}^n$ are called **orthogonal** ($\vec{x} \perp \vec{y}$) when

    $$
    \vec{x} \cdot \vec{y} = 0 \qquad \Longrightarrow \qquad \theta(\vec{x}, \vec{y}) = \arccos(0) = \frac{\pi}{2} = 90^\circ \quad (\text{for } \vec{x}, \vec{y} \neq \vec{0})
    $$
    """,
                "Orthogonal vectors",
            ),
            theorem(
                r"""
    In $\mathbb{R}^n$, we can find **at most $n$** non-zero vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$ which are pairwise orthogonal

    $$
    \vec{e}_i \cdot \vec{e}_j = 0 \qquad \forall\, i \neq j
    $$
    """,
                "Pairwise orthogonal vectors",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}
    \quad \Longrightarrow \quad \text{pairwise orthogonal}
    $$

    (a specific example of $n$ pairwise orthogonal vectors; many other examples exist!)

    Take any other non-zero vector

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \neq \vec{0}
    $$

    Note that

    $$
    \vec{x} \cdot \vec{e}_1 = x^1, \quad \vec{x} \cdot \vec{e}_2 = x^2, \quad \dots, \quad \vec{x} \cdot \vec{e}_n = x^n,
    $$

    so $\vec{x} \perp \vec{e}_i$ if and only if $x^i = 0$.

    If $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n, \vec{x}$ were pairwise orthogonal, then $\vec{x}$ would have to be the zero vector $\vec{0}$. This contradicts our assumption that $\vec{x} \neq \vec{0}$.

    $\leadsto$ &nbsp; here we used the specific vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$, but the argument extends to any set of $n$ non-zero pairwise orthogonal vectors (exercise, after Lecture 03). $\square$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, arrow, definition, mo):
    def _pr(x1, x2, x3):
        """Oblique projection of R^3, as on the board: x^2 to the right, x^3 up, x^1 towards the viewer."""
        return x2 - 0.45 * x1, x3 - 0.4 * x1

    _fig = Figure(figsize=(FULL, 2.3), layout="constrained")
    _a2, _a3 = _fig.subplots(1, 2)
    for _ax in (_a2, _a3):
        _ax.set_xlim(-1.5, 2.3)
        _ax.set_ylim(-1.0, 2.1)
        _ax.set_aspect("equal")
        _ax.axis("off")
    arrow(_a2, (-0.6, 0), (1.9, 0), "black", lw=0.9)
    arrow(_a2, (0, -0.6), (0, 1.9), "black", lw=0.9)
    arrow(_a2, (0, 0), (1, 0), BLUE)
    arrow(_a2, (0, 0), (0, 1), BLUE)
    _a2.text(0.55, -0.14, r"$\vec{e}_1$", color=BLUE, fontsize=13, ha="center", va="top")
    _a2.text(-0.14, 0.55, r"$\vec{e}_2$", color=BLUE, fontsize=13, ha="right", va="center")
    _a2.text(-1.4, 1.75, r"$\mathbb{R}^2$", fontsize=13)

    arrow(_a3, _pr(-0.5, 0, 0), _pr(1.9, 0, 0), "black", lw=0.9)
    arrow(_a3, (-0.6, 0), (1.9, 0), "black", lw=0.9)
    arrow(_a3, (0, -0.6), (0, 1.9), "black", lw=0.9)
    arrow(_a3, (0, 0), _pr(1, 0, 0), BLUE)
    arrow(_a3, (0, 0), (1, 0), BLUE)
    arrow(_a3, (0, 0), (0, 1), BLUE)
    _e1 = _pr(1, 0, 0)
    _a3.text(_e1[0] - 0.12, _e1[1] + 0.12, r"$\vec{e}_1$", color=BLUE, fontsize=13, ha="right", va="bottom")
    _a3.text(0.6, -0.14, r"$\vec{e}_2$", color=BLUE, fontsize=13, ha="center", va="top")
    _a3.text(0.14, 0.6, r"$\vec{e}_3$", color=BLUE, fontsize=13, ha="left", va="center")
    _a3.text(-1.4, 1.75, r"$\mathbb{R}^3$", fontsize=13)

    mo.vstack(
        [
            mo.md(r"""### The standard basis"""),
            definition(
                r"""
    A set of $n$ non-zero pairwise orthogonal vectors is called an **orthogonal basis** of $\mathbb{R}^n$.

    The vectors

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}
    $$

    used above are called the **standard basis vectors** of $\mathbb{R}^n$.
    """,
                "Orthogonal basis and standard basis",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; they have the additional property of having unit length (**unit vectors**)

    $\leadsto$ &nbsp; more importantly: &nbsp; $\vec{x} \cdot \vec{e}_i = x^i \quad \forall\, \vec{x} \in \mathbb{R}^n$

    **Example.**

    $$
    \mathbb{R}^2: \quad \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \; \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \; \Longrightarrow \;
    \begin{cases}
    \vec{x} \cdot \vec{e}_1 = (x^1)(1) + (x^2)(0) = x^1 \\
    \vec{x} \cdot \vec{e}_2 = (x^1)(0) + (x^2)(1) = x^2
    \end{cases}
    $$

    $$
    \mathbb{R}^3: \quad \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \; \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \; \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}
    \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \; \Longrightarrow \;
    \begin{cases}
    \vec{x} \cdot \vec{e}_1 = x^1 \\
    \vec{x} \cdot \vec{e}_2 = x^2 \\
    \vec{x} \cdot \vec{e}_3 = x^3
    \end{cases}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; the standard basis vectors define the coordinate axes on $\mathbb{R}^n$!

    $\leadsto$ &nbsp; coordinates/components of a vector are its dot products with the standard basis vectors!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Every $\vec{x} \in \mathbb{R}^n$ is a linear combination of the standard basis vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$, with coefficients

    $$
    x^1 = \vec{x} \cdot \vec{e}_1, \quad x^2 = \vec{x} \cdot \vec{e}_2, \quad \dots, \quad x^n = \vec{x} \cdot \vec{e}_n
    $$
    """,
                "Components in the standard basis",
            ),
            mo.md(
                r"""
    **Proof** (for $n = 3$).

    $$
    \begin{aligned}
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix}
    &= \begin{bmatrix} x^1 \\ 0 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ x^2 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ x^3 \end{bmatrix}
    = x^1 \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} + x^3 \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \\
    &= x^1 \vec{e}_1 + x^2 \vec{e}_2 + x^3 \vec{e}_3
    \qquad \text{and} \qquad
    \begin{cases}
    x^1 = \vec{x} \cdot \vec{e}_1 \\
    x^2 = \vec{x} \cdot \vec{e}_2 \\
    x^3 = \vec{x} \cdot \vec{e}_3
    \end{cases}
    \qquad \square
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    p1_dot, p1_nx, p2_a, p3_a, p3_b, p3_c = (_field() for _ in range(6))
    return p1_dot, p1_nx, p2_a, p3_a, p3_b, p3_c


@app.cell(hide_code=True)
def _(check, mo, p1_dot, p1_nx, p2_a, p3_a, p3_b, p3_c):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $\vec{x} = \begin{bmatrix} 1 \\ -2 \\ 2 \end{bmatrix}, \; \vec{y} = \begin{bmatrix} 2 \\ 1 \\ 1 \end{bmatrix}$.

    (a) Compute $2\vec{x} - \vec{y}$.

    (b) Compute $\vec{x} \cdot \vec{y}$, $\lVert \vec{x} \rVert$, $\lVert \vec{y} \rVert$.
    """
            ),
            _ask(r"$\vec{x} \cdot \vec{y} =$", p1_dot, 2),
            _ask(r"$\lVert \vec{x} \rVert =$", p1_nx, 3),
            mo.md(
                r"""
    (c) Find the angle between $\vec{x}$ and $\vec{y}$.

    ### Question 2

    Consider $\vec{u} = \begin{bmatrix} 1 \\ 2 \\ -1 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 2 \\ a \\ 4 \end{bmatrix}$.

    (a) Find $a \in \mathbb{R}$ so that $\vec{u} \perp \vec{v}$.
    """
            ),
            _ask(r"$a =$", p2_a, 1),
            mo.md(
                r"""
    (b) For this value of $a$, compute $\lVert \vec{u} + \vec{v} \rVert$.

    (c) Check that $\lVert \vec{u} + \vec{v} \rVert^2 = \lVert \vec{u} \rVert^2 + \lVert \vec{v} \rVert^2$.

    ### Question 3

    Consider $\vec{u} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 1 \\ -1 \\ 0 \end{bmatrix}, \; \vec{w} = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$.

    (a) Show that $\vec{u}, \vec{v}, \vec{w}$ are pairwise orthogonal.

    (b) Write $\vec{x} = \begin{bmatrix} 3 \\ 1 \\ 4 \end{bmatrix}$ in the form $\vec{x} = a\vec{u} + b\vec{v} + c\vec{w}$.
    """
            ),
            _ask(r"$a =$", p3_a, 2),
            _ask(r"$b =$", p3_b, 1),
            _ask(r"$c =$", p3_c, 2),
            mo.md(
                r"""
    (c) Show that $a = \dfrac{\vec{x} \cdot \vec{u}}{\vec{u} \cdot \vec{u}}, \quad b = \dfrac{\vec{x} \cdot \vec{v}}{\vec{v} \cdot \vec{v}}, \quad c = \dfrac{\vec{x} \cdot \vec{w}}{\vec{w} \cdot \vec{w}}$.

    (d) Show that there is no non-zero vector $\vec{y} = \begin{bmatrix} p \\ q \\ r \end{bmatrix}$ orthogonal to $\vec{u}$, $\vec{v}$ and $\vec{w}$ at the same time.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - the dot product $\vec{x} \cdot \vec{y} = x^1 y^1 + \dots + x^n y^n \in \mathbb{R}$ is symmetric, bilinear and positive definite
    - it defines the norm $\lVert \vec{x} \rVert = \sqrt{\vec{x} \cdot \vec{x}}$ and the angle $\theta(\vec{x}, \vec{y})$, which makes sense by the Cauchy–Schwarz inequality $(\vec{x} \cdot \vec{y})^2 \leq \lVert \vec{x} \rVert^2\, \lVert \vec{y} \rVert^2$
    - triangle inequality: $\lVert \vec{x} + \vec{y} \rVert \leq \lVert \vec{x} \rVert + \lVert \vec{y} \rVert$
    - $\vec{x} \perp \vec{y}$ when $\vec{x} \cdot \vec{y} = 0$; in $\mathbb{R}^n$ there are at most $n$ non-zero pairwise orthogonal vectors
    - the standard basis vectors $\vec{e}_1, \dots, \vec{e}_n$ give $\vec{x} = x^1 \vec{e}_1 + \dots + x^n \vec{e}_n$ with $x^i = \vec{x} \cdot \vec{e}_i$

    **Next:** matrices, linear transformations, and determinants
    """)
    return


if __name__ == "__main__":
    app.run()
