import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 10 · Properties and interpretations of differentiable functions", css_file="bs101.css")


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
    header("Lecture 10", "Week 05", "Lecture 10 · Properties and interpretations of differentiable functions")
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
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-2, -6), fontsize=12, ha="right", va="top")
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(6, -2), fontsize=12, ha="left", va="top")

    return (cross_axes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - differentiability and the derivative: $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ if
    - (1) it has well-defined partial derivatives

        $$
        \begin{aligned}
        \frac{\partial f}{\partial x^1}(\vec{a}) &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + t \\ a^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t = 0} f(\vec{a} + t\vec{e}_1) \\[6pt]
        \frac{\partial f}{\partial x^2}(\vec{a}) &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 \\ a^2 + t \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t = 0} f(\vec{a} + t\vec{e}_2)
        \end{aligned}
        $$

    - (2) it has well-defined directional derivatives $\forall\, \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$

        $$
        Df(\vec{a})(\vec{v}) = \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + t v^1 \\ a^2 + t v^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t = 0} f(\vec{a} + t\vec{v})
        $$

    - (3) the map $Df(\vec{a}) : \mathbb{R}^2 \longrightarrow \mathbb{R}$, $\vec{v} \longmapsto Df(\vec{a})(\vec{v})$ is linear

        $$
        \Longrightarrow \qquad Df(\vec{a})(\vec{v}) = v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})
        = \underbrace{\begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\text{matrix of partial derivatives}} \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}
        $$

    - (4) $Df(\vec{a})(\vec{x} - \vec{a})$ is a linear approximation to $f(\vec{x}) - f(\vec{a})$ &nbsp; (it is this approximation that allows us to call $Df(\vec{a})$ the derivative)

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

        in this case, $Df(\vec{a}) : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **the derivative of $f$ at $\vec{x} = \vec{a}$**

    - (4) $\Longrightarrow$ (3) $\Longrightarrow$ (2) $\Longrightarrow$ (1) &nbsp; $\leadsto$ &nbsp; we could define differentiability by requiring only the existence of a linear approximation: other conditions follow as consequence!
    - example: $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \dfrac{(x^1)^2 x^2}{\lVert \vec{x} \rVert^2}$ for $\vec{x} \neq \vec{0}$, &nbsp; $f(\vec{0}) = 0$

        $$
        Df(\vec{0})(\vec{v}) = \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} t v^1 \\ t v^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} 0 \\ 0 \end{bmatrix} \right)}{t}
        = \lim_{t \to 0} \frac{\dfrac{t^3 (v^1)^2 v^2}{t^2 \lVert \vec{v} \rVert^2} - 0}{t} = \frac{(v^1)^2 v^2}{\lVert \vec{v} \rVert^2} \qquad (\vec{v} \neq \vec{0})
        $$

        $Df(\vec{0})(\vec{v})$ defined $\forall\, \vec{v}$, but not linear &nbsp; $\Longrightarrow$ &nbsp; $f$ is NOT differentiable at $\vec{x} = \vec{0}$!

    - generalization for $n > 2$ (still $m = 1$): $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a}$ if the matrix of partial derivatives is well-defined (in particular, it is linear) and $Df(\vec{a})(\vec{x} - \vec{a})$ is a linear approximation to $f(\vec{x}) - f(\vec{a})$

        $$
        Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} : \mathbb{R}^n \longrightarrow \mathbb{R},
        \qquad
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

    **In this lecture:** properties and interpretations of differentiable functions
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.5 &nbsp; Properties and interpretations of differentiable functions

    ### Differentiability and continuity
    """
            ),
            theorem(
                r"""
    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a}$ then

    $$
    \lim_{\vec{x} \to \vec{a}} \big( f(\vec{x}) - f(\vec{a}) \big) = 0
    $$

    $\leadsto$ &nbsp; $f$ is continuous at $\vec{x} = \vec{a}$!
    """,
                "Differentiable implies continuous",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    f(\vec{x}) - f(\vec{a}) = \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert}\, \lVert \vec{x} - \vec{a} \rVert + Df(\vec{a})(\vec{x} - \vec{a})
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad \lim_{\vec{x} \to \vec{a}} \big( f(\vec{x}) - f(\vec{a}) \big)
    &= \underbrace{\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert}\, \lVert \vec{x} - \vec{a} \rVert}_{= \,0 \cdot 0}
    {} + \underbrace{\lim_{\vec{x} \to \vec{a}} Df(\vec{a})(\vec{x} - \vec{a})}_{= \,0 \ (\text{linear maps are continuous})} \\
    &= 0 \qquad \square
    \end{aligned}
    $$

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{cases}
    \dfrac{(x^1)^2}{\lVert \vec{x} \rVert^2}, & \vec{x} \neq \vec{0} \\[10pt]
    b, & \vec{x} = \vec{0}
    \end{cases}
    $$

    is not differentiable at $\vec{x} = \vec{0}$ (no matter the value of $b \in \mathbb{R}$)

    $$
    \lim_{t \to 0} f\!\left( \begin{bmatrix} t \\ 0 \end{bmatrix} \right) = 1, \qquad \lim_{t \to 0} f\!\left( \begin{bmatrix} 0 \\ t \end{bmatrix} \right) = 0
    $$

    $\Longrightarrow$ &nbsp; $f$ cannot be continuous &nbsp; $\Longrightarrow$ &nbsp; $f$ cannot be differentiable!

    ### $C^1$-smooth functions
    """
            ),
            theorem(
                r"""
    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ has partial derivatives on an open ball around $\vec{x} = \vec{a}$ and they are continuous at $\vec{x} = \vec{a}$, then $f$ is differentiable at $\vec{x} = \vec{a}$!
    """,
                "Continuous partials imply differentiable",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; gives an easier criterion for differentiability (sufficient, but not necessary!)

    1. compute partial derivatives for all points nearby $\vec{x} = \vec{a}$
    2. check for continuity at $\vec{x} = \vec{a}$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ whose partial derivatives are well-defined around $\vec{x} = \vec{a}$ and continuous at $\vec{x} = \vec{a}$ is called **$C^1$-smooth** at $\vec{x} = \vec{a}$.
    """,
                "$C^1$-smooth",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; the previous two theorems give

    $$
    C^1\text{-smooth} \qquad \Longrightarrow \qquad \text{differentiable} \qquad \Longrightarrow \qquad \text{continuous}
    $$

    **Example.** Any function $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ given by linear combination of products, quotients and compositions of elementary functions (powers, roots, exponentials, logarithms, trigonometric functions) of $x^i$'s is $C^1$-smooth where the formula and its derivatives are well-defined!

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \frac{e^{x^1} + \sqrt{x^2}}{\sin(x^1)}
    $$

    is $C^1$-smooth for $x^1 \neq n\pi$ and $x^2 > 0$

    $$
    \frac{\partial f}{\partial x^1} = \frac{e^{x^1} \sin(x^1) - \big( e^{x^1} + \sqrt{x^2} \big) \cos(x^1)}{\big( \sin(x^1) \big)^2},
    \qquad
    \frac{\partial f}{\partial x^2} = \frac{1}{2} \frac{1}{\sqrt{x^2}\, \sin(x^1)}
    $$

    both continuous for $x^1 \neq n\pi$, $x^2 > 0$.

    $\leadsto$ &nbsp; in our course, we will mostly be dealing with this type of functions

    $\leadsto$ &nbsp; so checking if and where a function is differentiable will generally be a problem of finding their domains and the domains of their partials
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### The derivative and the gradient"""),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$

    $$
    Df(\vec{a}) = \underbrace{\begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix}}_{\mathrm{Mat}(1 \times n)} : \mathbb{R}^n \longrightarrow \mathbb{R}
    $$

    is called

    - the **derivative** of $f$ at $\vec{x} = \vec{a}$
    - the **differential** of $f$ at $\vec{x} = \vec{a}$
    - the **Jacobian matrix** of $f$ at $\vec{x} = \vec{a}$
    """,
                "Derivative, differential, Jacobian matrix",
            ),
            definition(
                r"""
    We define the **gradient** of $f$ at $\vec{x} = \vec{a}$ as the vector

    $$
    \vec{\nabla} f(\vec{a}) = \underbrace{\begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] \dfrac{\partial f}{\partial x^2}(\vec{a}) \\ \vdots \\ \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix}}_{\mathrm{Mat}(n \times 1) \,\neq\, \mathrm{Mat}(1 \times n)} \in \mathbb{R}^n
    $$
    """,
                "Gradient",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; the derivative is the map that calculates directional derivatives &nbsp; $Df(\vec{a}) : \vec{v} \longmapsto Df(\vec{a})(\vec{v})$

    $\leadsto$ &nbsp; the gradient is **a vector** (carrying equivalent information but in a very different way!)

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \lVert \vec{x} \rVert^2 = (x^1)^2 + (x^2)^2, \quad \vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} 2 & 2 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}, \qquad
    \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto \begin{bmatrix} 2 & 2 \end{bmatrix} \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} = 2 v^1 + 2 v^2
    $$

    versus

    $$
    \vec{\nabla} f(\vec{a}) = \begin{bmatrix} 2 \\ 2 \end{bmatrix} = 2\vec{a} \in \mathbb{R}^2
    $$

    **Remark.** $Df(\vec{a})$ and $\vec{\nabla} f(\vec{a})$ are related via the dot product

    $$
    \begin{aligned}
    Df(\vec{a})(\vec{v}) &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a}) + \dots + v^n \frac{\partial f}{\partial x^n}(\vec{a}) = \big( \vec{\nabla} f(\vec{a}) \big) \cdot \vec{v} \\
    &= \lVert \vec{\nabla} f(\vec{a}) \rVert\, \lVert \vec{v} \rVert \cos\!\big( \theta(\vec{\nabla} f(\vec{a}), \vec{v}) \big) \qquad (\vec{\nabla} f(\vec{a}) \neq \vec{0},\ \vec{v} \neq \vec{0})
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, HALF, RED, arrow, blank, cross_axes, math, mo, np, theorem):
    _R, _r, _phi = 2.4, 0.8, math.radians(30)
    _fig, _ax = blank(HALF, 2.55, (-2.95, 6.95), (-2.95, 4.05))
    cross_axes(_ax, (-2.9, 6.9), (-2.9, 4.0), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(_R * np.cos(_th), _R * np.sin(_th), color=BLUE, lw=1.4)
    _ax.plot(_r * np.cos(_th), _r * np.sin(_th), color=RED, lw=1.4)
    _a = (_R * math.cos(_phi), _R * math.sin(_phi))
    arrow(_ax, _a, (3 * _a[0], 3 * _a[1]), GREEN)
    arrow(_ax, (0, 0), _a, BLUE)
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _ax.text(1.3, 0.75, r"$\vec{a}$", color=BLUE, fontsize=13, ha="left", va="top", bbox=_box)
    _ax.text(4.5, 2.1, r"$\vec{\nabla} f(\vec{a}) = 2\vec{a}$", color=GREEN, fontsize=13, ha="left", va="top")
    _ax.text(-1.75, 1.9, r"$f^{-1}(R^2)$", color=BLUE, fontsize=12, ha="right", va="bottom")
    _ax.text(-0.95, -1.2, r"$f^{-1}(r^2)$", color=RED, fontsize=12, ha="center", va="center")

    mo.vstack(
        [
            mo.md(r"""### Steepest ascent"""),
            theorem(
                r"""
    If $\vec{\nabla} f(\vec{a}) \neq \vec{0}$, it points in the direction at $\vec{a}$ where $f(\vec{x})$ grows fastest (direction of steepest ascent).

    If $\vec{\nabla} f(\vec{a}) = \vec{0}$, then $Df(\vec{a})(\vec{v}) = 0$ for every $\vec{v}$.
    """,
                "Direction of steepest ascent",
            ),
            mo.md(
                r"""
    **Proof.** If we keep $\lVert \vec{v} \rVert = 1$, $Df(\vec{a})(\vec{v})$ is largest when $\theta(\vec{\nabla} f(\vec{a}), \vec{v}) = 0$

    $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a})$ points in the direction of largest growth of $f$ at $\vec{x} = \vec{a}$

    $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a})$ is the direction of steepest ascent of $f$ at $\vec{x} = \vec{a}$! $\square$

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2, \qquad
    \vec{\nabla} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) = \begin{bmatrix} 2 a^1 \\ 2 a^2 \end{bmatrix}
    $$

    with level sets $f^{-1}(r^2)$: &nbsp; $(x^1)^2 + (x^2)^2 = r^2$ &nbsp; and &nbsp; $f^{-1}(R^2)$: &nbsp; $(x^1)^2 + (x^2)^2 = R^2$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; $f(\vec{x})$ increases fastest along the radial direction

    Direction of **steepest descent** (fastest decrease) of $f$ at $\vec{a}$

    $$
    \leadsto \qquad -\vec{\nabla} f(\vec{a}) = \begin{bmatrix} -2 a^1 \\ -2 a^2 \end{bmatrix}
    $$

    Directions with no ascent / descent

    $$
    \leadsto \qquad \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \ \text{ such that } \ \vec{\nabla} f(\vec{a}) \cdot \vec{v} = 0 \qquad \Longleftrightarrow \qquad Df(\vec{a})(\vec{v}) = 0
    $$

    $$
    \vec{\nabla} f(\vec{a}) \cdot \vec{v} = 2 a^1 v^1 + 2 a^2 v^2 = 0 \qquad \Longleftrightarrow \qquad v^2 = -\frac{a^1}{a^2}\, v^1 \qquad (\text{assuming } a^2 \neq 0)
    $$

    $$
    \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \in \underbrace{\big( \vec{\nabla} f(\vec{a}) \big)^{\perp}}_{\text{orthogonal complement of } \vec{\nabla} f(\vec{a})},
    \qquad
    f^{-1}(R^2) = \left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \;\middle|\; (x^1)^2 + (x^2)^2 = R^2 \,\right\}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ga1 = mo.ui.slider(-1.5, 1.5, 0.1, value=1, label="$a^1$", show_value=True)
    ga2 = mo.ui.slider(-1.5, 1.5, 0.1, value=0.6, label="$a^2$", show_value=True)
    return ga1, ga2


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, HALF, LIGHT, ORANGE, cross_axes, ga1, ga2, math, mo, np, table, vector):
    _a = (round(ga1.value, 10) + 0.0, round(ga2.value, 10) + 0.0)
    _R = math.hypot(*_a)
    _grad = (2 * _a[0], 2 * _a[1])
    _v = (-_a[1] + 0.0, _a[0])  # one vector orthogonal to the gradient
    _lim = 3.8 if max(abs(_grad[0] + _a[0]), abs(_grad[1] + _a[1])) <= 3 else 5.6  # the frame follows the gradient: nothing is clipped

    _fig = Figure(figsize=(HALF, HALF), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-_lim, _lim)
    _ax.set_ylim(-_lim, _lim)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _th = np.linspace(0, 2 * np.pi, 200)
    for _r in (1, 2, 3, 4, 5):
        _ax.plot(_r * np.cos(_th), _r * np.sin(_th), color=LIGHT, lw=0.8)
    cross_axes(_ax, (-_lim, _lim), (-_lim, _lim), "$x^1$", "$x^2$")
    if _R > 0:
        _d = math.atan2(_a[1], _a[0])
        _ax.plot(_R * np.cos(_th), _R * np.sin(_th), color=BLUE, lw=1.4)
        _t = (-_a[1] / _R, _a[0] / _R)
        _ax.plot([_a[0] - 2.2 * _t[0], _a[0] + 2.2 * _t[0]], [_a[1] - 2.2 * _t[1], _a[1] + 2.2 * _t[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
        vector(_ax, _a, (_a[0] + _grad[0], _a[1] + _grad[1]), GREEN, r"$\vec{\nabla} f(\vec{a})$", 0, r=22)
        vector(_ax, _a, (_a[0] + _v[0], _a[1] + _v[1]), ORANGE, r"$\vec{v}$", 45, r=16)
        vector(_ax, (0, 0), _a, BLUE, r"$\vec{a}$", -45, r=16)
        _q = _d - math.radians(135)
        _ax.annotate(r"$f^{-1}(R^2)$", (_R * math.cos(_q), _R * math.sin(_q)), textcoords="offset points", xytext=(30 * math.cos(_q), 16 * math.sin(_q)), ha="center", va="center", color=BLUE, fontsize=12, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})
        _perp = rf"$\textcolor{{{ORANGE}}}{{\begin{{bmatrix}} {_v[0]:g} \\ {_v[1]:g} \end{{bmatrix}}}}$"
        _dot = rf"$({_grad[0]:g})({_v[0]:g}) + ({_grad[1]:g})({_v[1]:g}) = 0$"
    else:
        vector(_ax, (0, 0), _a, BLUE, r"$\vec{a}$", 0)
        _perp = _dot = r"need $\vec{\nabla} f(\vec{a}) \neq \vec{0}$"

    mo.vstack(
        [
            mo.hstack([ga1, ga2], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{a}$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_a[0]:g} \\ {_a[1]:g} \end{{bmatrix}}}}$"),
                    (r"$f(\vec{a}) = R^2$", rf"$\textcolor{{{BLUE}}}{{{_R**2:.2f}}}$"),
                    (r"$\vec{\nabla} f(\vec{a}) = 2\vec{a}$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_grad[0]:g} \\ {_grad[1]:g} \end{{bmatrix}}}}$"),
                    (r"$\vec{v} = \begin{bmatrix} -a^2 \\ a^1 \end{bmatrix} \in \big( \vec{\nabla} f(\vec{a}) \big)^{\perp}$", _perp),
                    (r"$\vec{\nabla} f(\vec{a}) \cdot \vec{v}$", _dot),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, arrow, blank, definition, mo, np, theorem):
    _fig, _ax = blank(HALF, 2.0, (-2.3, 2.9), (-1.05, 1.85))
    _x = np.linspace(-2.1, 2.1, 100)
    _ax.plot(_x, -0.12 * _x**2 - 0.15 * _x, color=BLUE, lw=1.4)
    _n = np.array([0.15, 1.0]) / np.hypot(0.15, 1.0)
    _tv = np.array([1.0, -0.15]) / np.hypot(0.15, 1.0)
    _sq = np.array([0.2 * _tv, 0.2 * _tv + 0.2 * _n, 0.2 * _n])
    _ax.plot(_sq[:, 0], _sq[:, 1], color=GREY, lw=0.8)
    arrow(_ax, (0, 0), tuple(1.4 * _n), GREEN)
    _ax.plot(0, 0, "o", color="black", ms=4, zorder=4)
    _ax.text(-0.08, -0.14, r"$\vec{a}$", fontsize=13, ha="center", va="top")
    _ax.text(0.38, 1.4, r"$\vec{\nabla} f(\vec{a})$", color=GREEN, fontsize=13, ha="left", va="center")
    _ax.text(2.0, -0.55, r"$f^{-1}(b)$", color=BLUE, fontsize=13, ha="left", va="bottom")

    mo.vstack(
        [
            mo.md(r"""### The gradient and level sets"""),
            theorem(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$ with $f(\vec{a}) = b$ and $\vec{\nabla} f(\vec{a}) \neq \vec{0}$, then $\vec{\nabla} f(\vec{a})$ is perpendicular to $f^{-1}(b)$

    $$
    \vec{\nabla} f(\vec{a}) \perp f^{-1}(b)
    $$
    """,
                "Gradient is perpendicular to level sets",
            ),
            _fig,
            mo.md(r"""### The affine approximation"""),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$ we call $g : \mathbb{R}^n \longrightarrow \mathbb{R}$ given by

    $$
    \begin{aligned}
    g(\vec{x}) &= f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \\
    &= f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \frac{\partial f}{\partial x^2}(\vec{a})\, (x^2 - a^2) + \dots + \frac{\partial f}{\partial x^n}(\vec{a})\, (x^n - a^n)
    \end{aligned}
    $$

    the **affine approximation** of $f$ at $\vec{a}$.
    """,
                "Affine approximation",
            ),
            mo.md(
                r"""
    **Remark.** For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ differentiable at $x = a$: &nbsp; $g(x) = f(a) + f'(a)(x - a)$

    $$
    \leadsto \quad \mathrm{graph}(g) = \text{tangent line to } \mathrm{graph}(f) \text{ at } \begin{bmatrix} a \\ f(a) \end{bmatrix}
    = \left\{\, \begin{bmatrix} x \\ y \end{bmatrix} \;\middle|\; y = f(a) + f'(a)(x - a),\ x \in \mathbb{R} \,\right\}
    $$
    """
            ),
            theorem(
                r"""
    If $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$, then

    $$
    \begin{aligned}
    \mathrm{graph}(g) &= \text{plane in } \mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R} \text{ through } \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} \text{ with normal } \vec{n} = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] \dfrac{\partial f}{\partial x^2}(\vec{a}) \\[8pt] -1 \end{bmatrix} \\[4pt]
    &= \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ y \end{bmatrix} \;\middle|\; y = f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \frac{\partial f}{\partial x^2}(\vec{a})\, (x^2 - a^2),\ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\}
    \end{aligned}
    $$

    (the **tangent plane** to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$)

    $$
    \leadsto \qquad \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \frac{\partial f}{\partial x^2}(\vec{a})\, (x^2 - a^2) - \big( y - f(\vec{a}) \big) = 0
    $$
    """,
                "Tangent plane",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q_d1, q_d2 = _field(), _field()
    return q_d1, q_d2


@app.cell(hide_code=True)
def _(check, mo, q_d1, q_d2):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \ln(x^1 x^2)
    $$

    (a) Compute $\dfrac{\partial f}{\partial x^1}$, $\dfrac{\partial f}{\partial x^2}$.

    (b) Where is $f$ $C^1$-smooth?

    (c) For $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$, write the derivative of $f$ at $\vec{a}$; write the gradient of $f$ at $\vec{a}$.
    """
            ),
            _ask(r"$\dfrac{\partial f}{\partial x^1}(\vec{a}) =$", q_d1, 1),
            _ask(r"$\dfrac{\partial f}{\partial x^2}(\vec{a}) =$", q_d2, 0.5),
            mo.md(
                r"""
    (d) Find all $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$ for which $Df(\vec{a})(\vec{v}) = 0$.

    (e) Sketch $f^{-1}(\ln(2))$ and draw $\vec{\nabla} f(\vec{a})$ at $\vec{a}$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - differentiable at $\vec{x} = \vec{a}$ $\Longrightarrow$ continuous at $\vec{x} = \vec{a}$; continuous partials at $\vec{x} = \vec{a}$ ($C^1$-smooth) $\Longrightarrow$ differentiable at $\vec{x} = \vec{a}$ (sufficient, but not necessary)
    - the derivative $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$ is the map that calculates directional derivatives; the gradient $\vec{\nabla} f(\vec{a}) \in \mathbb{R}^n$ is a vector, and $Df(\vec{a})(\vec{v}) = \vec{\nabla} f(\vec{a}) \cdot \vec{v}$
    - if $\vec{\nabla} f(\vec{a}) \neq \vec{0}$: $\vec{\nabla} f(\vec{a})$ is the direction of steepest ascent, $-\vec{\nabla} f(\vec{a})$ of steepest descent, and $\big( \vec{\nabla} f(\vec{a}) \big)^{\perp}$ the directions with no ascent / descent
    - $\vec{\nabla} f(\vec{a}) \perp f^{-1}(b)$ for $b = f(\vec{a})$
    - the affine approximation $g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$: for $n = 2$, $\mathrm{graph}(g)$ is the tangent plane to $\mathrm{graph}(f)$

    **Next:** affine approximations and the derivative of general maps
    """)
    return


if __name__ == "__main__":
    app.run()
