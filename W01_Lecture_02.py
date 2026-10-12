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
    RED, GREEN, BLUE, GREY = "#b3261e", "#2e7d32", "#1b458f", "#888888"

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
        <b>Date</b><span>{date}</span><b>Instructor</b><span>Professor Scarinci</span>
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

    def warning(body):
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, label_offset=(6, 6), label_ha="left", label_va="bottom", **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "->,head_width=0.3,head_length=0.5", "color": color, "lw": 1.4, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=label_offset, ha=label_ha, va=label_va, color=color, fontsize=18)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color="#cfe3f5", lw=0.6)
        ax.set_axisbelow(True)

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, GREEN, GREY, RED, arrow, check, definition, header, plane, theorem, warning


@app.cell(hide_code=True)
def _(header):
    header("Lecture 02", "Week 01", "Lecture 02 · The Euclidean inner product (the dot product)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Points in $n$-space and $n$-vectors (arrows between points):

    $$
    \mathbb{R}^n \ni \vec{x} = (x^1, x^2, \dots, x^n)
    = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}
    $$

    Each entry is a real number; $x^2$ is the *2nd component* of $\vec{x}$.

    | Vector addition | Scalar–vector multiplication |
    |:---:|:---:|
    | $+ : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n$ | $\cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n$ |
    | $\begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} + \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} = \begin{bmatrix} x^1 + y^1 \\ x^2 + y^2 \\ \vdots \\ x^n + y^n \end{bmatrix}$ | $\alpha \cdot \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \alpha x^2 \\ \vdots \\ \alpha x^n \end{bmatrix}$ |
    | componentwise addition | componentwise multiplication |

    These operations allow us to do calculations with vectors the same way as with real numbers!

    **Today:** extra structure on $\mathbb{R}^n$, needed for “measurements”.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 &nbsp; The Euclidean inner product (the dot product)
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given two vectors

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}, \quad
    \vec{y} = \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} \in \mathbb{R}^n
    $$

    we define their **dot product** or **inner product** as the real number

    $$
    \vec{x} \cdot \vec{y} = x^1 y^1 + x^2 y^2 + \dots + x^n y^n \in \mathbb{R}
    $$

    (the sum of products of components).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo, warning):
    mo.vstack(
        [
            mo.md(
                r"""
    This is another extension of multiplication of real numbers, now to pairs of vectors, and taking scalar values:

    $$
    \cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}
    $$
    """
            ),
            warning(
                r"""
    This “$\cdot$” is **not** the same as for scalar–vector multiplication! To avoid confusion, we drop the “$\cdot$” for scalar–vector multiplication and write

    $$
    \alpha \vec{x} = \alpha \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \vdots \\ \alpha x^n \end{bmatrix}
    $$
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
    For all vectors $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and scalars $\alpha, \beta \in \mathbb{R}$:

    1. $\vec{x} \cdot \vec{y} = \vec{y} \cdot \vec{x}$ &nbsp; — *symmetric*
    2. $(\alpha \vec{x} + \beta \vec{y}) \cdot \vec{z} = \alpha\, \vec{x} \cdot \vec{z} + \beta\, \vec{y} \cdot \vec{z}$ and
       $\vec{x} \cdot (\alpha \vec{y} + \beta \vec{z}) = \alpha\, \vec{x} \cdot \vec{y} + \beta\, \vec{x} \cdot \vec{z}$
       &nbsp; — *linear in each of its 2 arguments: bilinear* (this is also a distributivity property)
    3. $\vec{x} \cdot \vec{x} \geq 0$, with “$=$” iff (if and only if) $\vec{x} = \vec{0}$ &nbsp; — *positive definite*
    """,
                "Basic properties",
            ),
            mo.md(r"**Proof.** Exercise (using definitions and properties of real numbers)."),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    The **norm** (length) of a vector $\vec{x}$ is

    $$
    \lVert \vec{x} \rVert := \sqrt{\vec{x} \cdot \vec{x}}
    $$

    This makes sense since $\vec{x} \cdot \vec{x} \geq 0$.

    The **angle** between two vectors $\vec{x}, \vec{y}$ is

    $$
    \theta(\vec{x}, \vec{y}) = \arccos\!\left( \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \right)
    \qquad (\text{must have } \vec{x}, \vec{y} \neq \vec{0})
    $$
    """
            ),
            mo.md(
                r"""
    It is not so clear why this makes sense: $\arccos : [-1, 1] \longrightarrow [0, \pi]$, so we need the quotient to lie in $[-1, 1]$. We come back to this below.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Arc, Figure, GREEN, RED, arrow, math, mo):
    _fig = Figure(figsize=(3.6, 3.0), layout="constrained")
    _ax = _fig.subplots()
    arrow(_ax, (0, 0), (3, 0), RED, r"$\vec{x}$")
    arrow(_ax, (0, 0), (1, math.sqrt(3)), GREEN, r"$\vec{y}$", label_offset=(-8, 6), label_ha="right")
    _ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=0, theta2=60, color="#e65100", lw=1.8))
    _ax.text(0.55, 0.22, r"$\theta = \pi/3$", color="#e65100", fontsize=15)
    _ax.set_xlim(-0.3, 3.6)
    _ax.set_ylim(-0.3, 2.4)
    _ax.set_aspect("equal")
    _ax.set_xticks([0, 1, 3])
    _ax.set_yticks([math.sqrt(3)], [r"$\sqrt{3}$"])
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    for _s in ("left", "bottom"):
        _ax.spines[_s].set_position("zero")

    mo.vstack(
        [
            mo.md(r"**Example.** &nbsp; $\vec{x} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}, \quad \vec{y} = \begin{bmatrix} 1 \\ \sqrt{3} \end{bmatrix}$"),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"""
    $$
    \begin{aligned}
    \lVert \vec{x} \rVert &= \sqrt{(3)^2 + (0)^2} = 3 \\
    \lVert \vec{y} \rVert &= \sqrt{(1)^2 + (\sqrt{3})^2} = 2 \\
    \vec{x} \cdot \vec{y} &= 3 \cdot 1 + 0 \cdot \sqrt{3} = 3 \\
    \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} &= \frac{1}{2} = \cos\!\left(\frac{\pi}{3}\right)
    \end{aligned}
    $$
    """
                    ),
                ],
                justify="start",
                gap=3,
                align="center",
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
    controls = mo.hstack([mo.vstack([x1, x2]), mo.vstack([y1, y2])], justify="start", gap=3)
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
def _(Arc, Figure, GREEN, RED, arrow, controls, dot, math, mo, nonzero, nx, ny, plane, x, y):
    _fig = Figure(figsize=(4.2, 4.2), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 4.5)
    arrow(_ax, (0, 0), tuple(x), RED)
    arrow(_ax, (0, 0), tuple(y), GREEN)
    for _color, _label in ((RED, r"$\vec{x}$"), (GREEN, r"$\vec{y}$")):
        _ax.plot([], [], color=_color, lw=1.4, label=_label)
    _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=12)

    if nonzero:
        _cos = max(-1.0, min(1.0, dot / (nx * ny)))
        _theta = math.acos(_cos)
        _a1 = math.degrees(math.atan2(x[1], x[0]))
        _a2 = math.degrees(math.atan2(y[1], y[0]))
        if (_a2 - _a1) % 360 > 180:
            _a1, _a2 = _a2, _a1
        _ax.add_patch(Arc((0, 0), 1.4, 1.4, theta1=_a1, theta2=_a2, color="#e65100", lw=1.8))
        _angle = (
            rf"| $\dfrac{{\vec{{x}}\cdot\vec{{y}}}}{{\lVert\vec{{x}}\rVert\,\lVert\vec{{y}}\rVert}}$ | ${_cos:.3f}$ |"
            "\n"
            rf"| $\theta(\vec{{x}},\vec{{y}})$ | ${_theta:.3f}$ rad $= {math.degrees(_theta):.1f}^\circ$ |"
        )
    else:
        _angle = r"| $\theta(\vec{x},\vec{y})$ | not defined: one of the vectors is $\vec{0}$ |"

    _values = mo.md(
        "| | |\n|:--|:--|\n"
        rf"| $\vec{{x}}\cdot\vec{{y}}$ | $({x[0]:g})({y[0]:g}) + ({x[1]:g})({y[1]:g}) = {dot:g}$ |"
        "\n"
        rf"| $\lVert\vec{{x}}\rVert$ | ${nx:.3f}$ |"
        "\n"
        rf"| $\lVert\vec{{y}}\rVert$ | ${ny:.3f}$ |"
        "\n" + _angle
    )

    mo.vstack(
        [
            controls,
            _values,
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    For every $\vec{x}, \vec{y} \in \mathbb{R}^n$

    $$
    (\vec{x} \cdot \vec{y})^2 \leq \lVert \vec{x} \rVert^2\, \lVert \vec{y} \rVert^2
    $$

    with “$=$” iff $\vec{x}, \vec{y}$ are proportional.
    """,
                "Cauchy–Schwarz inequality",
            ),
            mo.md(
                r"""
    $$
    \Longrightarrow \quad \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \in [-1, 1] \qquad \forall\, \vec{x}, \vec{y} \neq \vec{0}
    $$

    Our definition of angles really makes sense!

    **Proof.** If $\vec{x} = \vec{0}$ or $\vec{y} = \vec{0}$, then $(\vec{x} \cdot \vec{y})^2 = 0 = \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2$.

    Assume both $\vec{x}, \vec{y} \neq \vec{0}$ and compute $\lVert t\vec{x} + \vec{y} \rVert^2$ for $t \in \mathbb{R}$.

    1. Positive definite implies

        $$
        \lVert t\vec{x} + \vec{y} \rVert^2 \geq 0, \quad \text{with ``$=$'' iff } t\vec{x} + \vec{y} = \vec{0} \quad (\vec{x}, \vec{y} \text{ proportional})
        $$

    2. Bilinearity and symmetry give a quadratic polynomial in $t$:

        $$
        \begin{aligned}
        \lVert t\vec{x} + \vec{y} \rVert^2 &= (t\vec{x} + \vec{y}) \cdot (t\vec{x} + \vec{y}) \\
        &= t^2\, \vec{x} \cdot \vec{x} + t\, \vec{x} \cdot \vec{y} + t\, \vec{y} \cdot \vec{x} + \vec{y} \cdot \vec{y} \\
        &= t^2 \lVert \vec{x} \rVert^2 + 2t\, \vec{x} \cdot \vec{y} + \lVert \vec{y} \rVert^2
        \end{aligned}
        $$

    $$
    \Longrightarrow \quad t^2 \lVert \vec{x} \rVert^2 + 2t\, (\vec{x} \cdot \vec{y}) + \lVert \vec{y} \rVert^2 \geq 0, \quad \text{with equality for some } t \text{ iff } \vec{x}, \vec{y} \text{ are proportional}
    $$

    $$
    \Longrightarrow \quad \text{discriminant:} \quad \big(2 (\vec{x} \cdot \vec{y})\big)^2 - 4 \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2 \leq 0, \quad \text{with ``$=$'' iff } \vec{x}, \vec{y} \text{ are proportional} \qquad \square
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, controls, dot, mo, np, nx, ny):
    _disc = (2 * dot) ** 2 - 4 * nx**2 * ny**2
    _vertex = -dot / nx**2 if nx > 0 else 0.0
    _t = np.sort(np.append(np.linspace(min(-4, _vertex - 2), max(4, _vertex + 2), 400), _vertex))
    _p = _t**2 * nx**2 + 2 * _t * dot + ny**2

    _fig = Figure(figsize=(4.6, 3.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_t, _p, color=BLUE, lw=2.2)
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.grid(True, color="#cfe3f5", lw=0.6)
    _upper = max(30.0, 1.25 * float(_p.min()) + 2)
    _ax.set_ylim(-0.05 * _upper, _upper)
    _ax.set_xlabel("$t$")
    _ax.set_ylabel(r"$\|t\vec{x} + \vec{y}\|^2$")

    _verdict = "yes" if abs(_disc) < 1e-9 else "no"

    mo.vstack(
        [
            controls,
            mo.md(
                "| | |\n|:--|:--|\n"
                rf"| $(\vec{{x}}\cdot\vec{{y}})^2$ | ${dot**2:g}$ |"
                "\n"
                rf"| $\lVert\vec{{x}}\rVert^2\lVert\vec{{y}}\rVert^2$ | ${nx**2 * ny**2:g}$ |"
                "\n"
                rf"| discriminant | ${_disc:g}$ |"
                "\n"
                rf"| $\vec{{x}}, \vec{{y}}$ proportional | {_verdict} |"
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, arrow, controls, mo, np, nx, ny, plane, theorem, x, y):
    _s = x + y
    _ns = float(np.sqrt(_s @ _s))

    _fig = Figure(figsize=(4.2, 4.2), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 8.5)
    _ax.set_xticks(range(-8, 9, 2))
    _ax.set_yticks(range(-8, 9, 2))
    arrow(_ax, (0, 0), tuple(x), RED)
    arrow(_ax, (0, 0), tuple(y), "#1a237e")
    arrow(_ax, tuple(x), tuple(_s), BLUE)
    arrow(_ax, (0, 0), tuple(_s), GREEN)
    for _color, _label in ((RED, r"$\vec{x}$"), (BLUE, r"$\vec{y}$ translated"), ("#1a237e", r"$\vec{y}$"), (GREEN, r"$\vec{x}+\vec{y}$")):
        _ax.plot([], [], color=_color, lw=1.4, label=_label)
    _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=12)

    mo.vstack(
        [
            theorem(
                r"""
    For every $\vec{x}, \vec{y} \in \mathbb{R}^n$

    $$
    \lVert \vec{x} + \vec{y} \rVert \leq \lVert \vec{x} \rVert + \lVert \vec{y} \rVert
    $$
    """,
                "Triangle inequality",
            ),
            mo.md(r"**Proof.** A direct consequence of the Cauchy–Schwarz inequality! Exercise."),
            controls,
            mo.md(
                "| | |\n|:--|:--|\n"
                rf"| $\lVert\vec{{x}}+\vec{{y}}\rVert$ | ${_ns:.3f}$ |"
                "\n"
                rf"| $\lVert\vec{{x}}\rVert+\lVert\vec{{y}}\rVert$ | ${nx:.3f} + {ny:.3f} = {nx + ny:.3f}$ |"
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    $\vec{x}, \vec{y} \in \mathbb{R}^n$ are called **orthogonal** ($\vec{x} \perp \vec{y}$) when

    $$
    \vec{x} \cdot \vec{y} = 0
    $$

    For $\vec{x}, \vec{y} \neq \vec{0}$, this is equivalent to $\theta(\vec{x}, \vec{y}) = \arccos(0) = \frac{\pi}{2} = 90^\circ$.
    """
            ),
            theorem(
                r"""
    In $\mathbb{R}^n$, we can find **at most $n$** non-zero vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$ which are pairwise orthogonal:

    $$
    \vec{e}_i \cdot \vec{e}_j = 0 \qquad \forall\, i \neq j
    $$
    """
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

    This is a specific example of $n$ pairwise orthogonal vectors; many other examples exist!

    Take any other non-zero vector

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \neq \vec{0}
    $$

    Note that

    $$
    \vec{x} \cdot \vec{e}_1 = x^1, \quad \vec{x} \cdot \vec{e}_2 = x^2, \quad \dots, \quad \vec{x} \cdot \vec{e}_n = x^n,
    $$

    so $\vec{x} \perp \vec{e}_i$ iff $x^i = 0$.

    If $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n, \vec{x}$ were pairwise orthogonal, then $\vec{x}$ would have to be the zero vector $\vec{0}$. This contradicts our assumption that $\vec{x} \neq \vec{0}$.

    Here we used the specific vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$; the argument extends to any set of $n$ non-zero pairwise orthogonal vectors (exercise, after Lecture 03). $\square$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
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
    """
            ),
            mo.md(
                r"""
    They have the additional property of having unit length: they are *unit vectors*.

    More importantly: $\vec{x} \cdot \vec{e}_i = x^i \quad \forall\, \vec{x} \in \mathbb{R}^n$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, RED, arrow, mo):
    from mpl_toolkits.mplot3d import proj3d as _proj3d

    _fig = Figure(figsize=(6.4, 2.9), layout="constrained")
    _ax = _fig.add_subplot(1, 2, 1)
    _ax.set_xlim(-0.6, 2)
    _ax.set_ylim(-0.6, 2)
    _ax.set_aspect("equal")
    _ax.axis("off")
    arrow(_ax, (-0.6, 0), (1.9, 0), "black", lw=0.5)
    arrow(_ax, (0, -0.6), (0, 1.9), "black", lw=0.5)
    arrow(_ax, (0, 0), (1, 0), RED)
    arrow(_ax, (0, 0), (0, 1), RED)
    _ax.text(0.8, -0.35, r"$\vec{e}_1$", color=RED, fontsize=17)
    _ax.text(-0.45, 0.8, r"$\vec{e}_2$", color=RED, fontsize=17)
    _ax.set_title(r"$\mathbb{R}^2$")

    _ax3 = _fig.add_subplot(1, 2, 2, projection="3d")
    for _d in ((1.8, 0, 0), (0, 1.8, 0), (0, 0, 1.8)):
        _ax3.quiver(0, 0, 0, *_d, color="black", lw=0.8, arrow_length_ratio=0.06)
    _ax3.set_xlim(0, 1.6)
    _ax3.set_ylim(0, 1.6)
    _ax3.set_zlim(0, 1.6)
    _ax3.view_init(elev=22, azim=28)
    _ax3.set_axis_off()
    _ax3.set_title(r"$\mathbb{R}^3$")
    for _d, _name, _offset, _ha, _va in (
        ((1, 0, 0), r"$\vec{e}_1$", (-8, 8), "right", "bottom"),
        ((0, 1, 0), r"$\vec{e}_2$", (6, 8), "left", "bottom"),
        ((0, 0, 1), r"$\vec{e}_3$", (8, 0), "left", "center"),
    ):
        _ax3.quiver(0, 0, 0, *_d, color=RED, lw=1.6, arrow_length_ratio=0.12)
        _px, _py, _pz = _proj3d.proj_transform(*_d, _ax3.get_proj())
        _ax3.annotate(_name, (_px, _py), xytext=_offset, textcoords="offset points", ha=_ha, va=_va, color=RED, fontsize=17)

    mo.vstack(
        [
            mo.md(
                r"""
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
    The standard basis vectors define the coordinate axes on $\mathbb{R}^n$!

    Coordinates/components of a vector are its dot products with the standard basis vectors!
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
    """
            ),
            mo.md(
                r"""
    **Proof** (for $n = 3$).

    $$
    \begin{aligned}
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix}
    &= \begin{bmatrix} x^1 \\ 0 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ x^2 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ x^3 \end{bmatrix} \\
    &= x^1 \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} + x^3 \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \\
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


if __name__ == "__main__":
    app.run()
