import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 10", css_file="bs101.css")


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

    def arrow(ax, tail, tip, color, label=None, at_tip=False, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 2.2, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=18)

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
    header("Lecture 10", "Week 05", "Lecture 10")
    return


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
def _(mo):
    mo.md(r"""
    ## Last time

    Differentiability and the derivative

    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

    1. has well-defined partial derivatives

        $$
        \begin{aligned}
        \frac{\partial f}{\partial x^1}(\vec{a}) &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + t \\ a^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t = 0} f(\vec{a} + t\vec{e}_1) \\[6pt]
        \frac{\partial f}{\partial x^2}(\vec{a}) &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 \\ a^2 + t \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t = 0} f(\vec{a} + t\vec{e}_2)
        \end{aligned}
        $$

    2. has well-defined directional derivatives $\forall\, \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$

        $$
        Df(\vec{a})(\vec{v}) = \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + t v^1 \\ a^2 + t v^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t = 0} f(\vec{a} + t\vec{v})
        $$

    3. the map $Df(\vec{a}) : \mathbb{R}^2 \longrightarrow \mathbb{R}$, $\vec{v} \longmapsto Df(\vec{a})(\vec{v})$ is linear

        $$
        \begin{aligned}
        \Longrightarrow \quad Df(\vec{a})(\vec{v}) &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a}) \\
        &= \underbrace{\begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\text{matrix of partial derivatives}} \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}
        \end{aligned}
        $$

    4. $Df(\vec{a})(\vec{x} - \vec{a})$ is a linear approximation to $f(\vec{x}) - f(\vec{a})$

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

    It is this approximation that allows us to call $Df(\vec{a})$ the derivative.

    In this case, $Df(\vec{a}) : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **the derivative of $f$ at $\vec{x} = \vec{a}$**.

    **Remark.** &nbsp; 4 $\Longrightarrow$ 3 $\Longrightarrow$ 2 $\Longrightarrow$ 1

    We could define differentiability by requiring only the existence of a linear approximation! Other conditions follow as consequence!

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{cases}
    \dfrac{(x^1)^2 x^2}{\lVert \vec{x} \rVert^2}, & \vec{x} \neq \vec{0} \\[10pt]
    0, & \vec{x} = \vec{0}
    \end{cases}
    $$

    $$
    \begin{aligned}
    Df(\vec{0})(\vec{v}) &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} t v^1 \\ t v^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} 0 \\ 0 \end{bmatrix} \right)}{t} \\[4pt]
    &= \lim_{t \to 0} \frac{\dfrac{t^3 (v^1)^2 v^2}{t^2 \lVert \vec{v} \rVert^2} - 0}{t} = \frac{(v^1)^2 v^2}{\lVert \vec{v} \rVert^2} \qquad (\vec{v} \neq \vec{0})
    \end{aligned}
    $$

    - $Df(\vec{0})(\vec{v})$ defined $\forall\, \vec{v}$, with $Df(\vec{0})(\vec{0}) = 0$
    - not linear!

    $\Longrightarrow$ &nbsp; $f$ is NOT differentiable at $\vec{x} = \vec{0}$!

    **Remark.** Generalization for $n > 2$ (still $m = 1$)

    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \\ \vdots \\ a^n \end{bmatrix}$ if

    - $Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} : \mathbb{R}^n \longrightarrow \mathbb{R}$ &nbsp; (matrix of partial derivatives) is well-defined (in particular, it is linear)

    - $Df(\vec{a})(\vec{x} - \vec{a})$ is a linear approximation to $f(\vec{x}) - f(\vec{a})$

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"**Today:** Properties and interpretations of differentiable functions"),
            theorem(
                r"""
    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a}$ then

    $$
    \lim_{\vec{x} \to \vec{a}} \big( f(\vec{x}) - f(\vec{a}) \big) = 0
    $$

    $f$ is continuous at $\vec{x} = \vec{a}$!
    """
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    f(\vec{x}) - f(\vec{a}) = \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert}\, \lVert \vec{x} - \vec{a} \rVert + Df(\vec{a})(\vec{x} - \vec{a})
    $$

    $$
    \Longrightarrow \quad \lim_{\vec{x} \to \vec{a}} \big( f(\vec{x}) - f(\vec{a}) \big)
    = \underbrace{\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert}\, \lVert \vec{x} - \vec{a} \rVert}_{= \,0 \cdot 0}
    + \underbrace{\lim_{\vec{x} \to \vec{a}} Df(\vec{a})(\vec{x} - \vec{a})}_{= \,0 \ (\text{linear maps are continuous})} \qquad \square
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

    $\Longrightarrow$ &nbsp; $f$ cannot be continuous! &nbsp; $\Longrightarrow$ &nbsp; $f$ cannot be differentiable!
    """
            ),
            theorem(
                r"""
    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ has partial derivatives on an open ball around $\vec{x} = \vec{a}$ and they are continuous at $\vec{x} = \vec{a}$, then $f$ is differentiable at $\vec{x} = \vec{a}$!
    """
            ),
            mo.md(
                r"""
    Gives an easier criterion for differentiability (sufficient, but not necessary!)

    1. compute partial derivatives for all points nearby $\vec{x} = \vec{a}$
    2. check for continuity at $\vec{x} = \vec{a}$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ with continuous partials at $\vec{x} = \vec{a}$ is called **$C^1$-smooth** at $\vec{x} = \vec{a}$.
    """
            ),
            mo.md(
                r"""
    The previous two theorems give

    $$
    C^1\text{-smooth} \quad \Longrightarrow \quad \text{differentiable} \quad \Longrightarrow \quad \text{continuous}
    $$

    **Example.** Any function $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ given by linear combination of products, quotients and compositions of elementary functions (powers, roots, exps, logs, trigs) of $x^i$'s are $C^1$-smooth where the formula and its derivatives are well-defined!

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

    In our course, we will mostly be dealing with this type of functions.

    So checking if and where a function is differentiable will generally be a problem of finding their domains and the domains of their partials.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$

    $$
    Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} : \mathbb{R}^n \longrightarrow \mathbb{R} \qquad (\mathrm{Mat}(1 \times n))
    $$

    is called

    - the **derivative** of $f$ at $\vec{x} = \vec{a}$
    - the **differential** of $f$ at $\vec{x} = \vec{a}$
    - the **Jacobian matrix** of $f$ at $\vec{x} = \vec{a}$
    """
            ),
            definition(
                r"""
    We define the **gradient** of $f$ at $\vec{x} = \vec{a}$ as the vector

    $$
    \nabla f(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] \dfrac{\partial f}{\partial x^2}(\vec{a}) \\ \vdots \\ \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathbb{R}^n \qquad (\mathrm{Mat}(n \times 1) \neq \mathrm{Mat}(1 \times n))
    $$
    """
            ),
            mo.md(
                r"""
    The derivative is the map that calculates directional derivatives &nbsp; $Df(\vec{a}) : \vec{v} \longmapsto Df(\vec{a})(\vec{v})$

    The gradient is a vector! (carrying equivalent information but in a very different way!)

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \lVert \vec{x} \rVert^2 = (x^1)^2 + (x^2)^2, \quad \vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$

    $$
    \Longrightarrow \quad Df(\vec{a}) = \begin{bmatrix} 2 & 2 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}, \qquad
    \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto \begin{bmatrix} 2 & 2 \end{bmatrix} \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} = 2 v^1 + 2 v^2
    $$

    vs

    $$
    \nabla f(\vec{a}) = \begin{bmatrix} 2 \\ 2 \end{bmatrix} = 2\vec{a} \in \mathbb{R}^2
    $$

    **Remark.** $Df(\vec{a})$ and $\nabla f(\vec{a})$ are related via the dot product

    $$
    \begin{aligned}
    Df(\vec{a})(\vec{v}) &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a}) + \dots + v^n \frac{\partial f}{\partial x^n}(\vec{a}) \\
    &= \big( \nabla f(\vec{a}) \big) \cdot \vec{v} \\
    &= \lVert \nabla f(\vec{a}) \rVert\, \lVert \vec{v} \rVert \cos\!\big( \theta(\nabla f(\vec{a}), \vec{v}) \big) \qquad (\nabla f(\vec{a}) \neq \vec{0},\ \vec{v} \neq \vec{0})
    \end{aligned}
    $$
    """
            ),
            theorem(
                r"""
    If $\nabla f(\vec{a}) \neq \vec{0}$, it points in the direction at $\vec{a}$ where $f(\vec{x})$ grows fastest (direction of steepest ascent).

    If $\nabla f(\vec{a}) = \vec{0}$, then $Df(\vec{a})(\vec{v}) = 0$ for every $\vec{v}$.
    """
            ),
            mo.md(
                r"""
    **Proof.** If we keep $\lVert \vec{v} \rVert = 1$, $Df(\vec{a})(\vec{v})$ is largest when $\theta(\nabla f(\vec{a}), \vec{v}) = 0$

    $\Longrightarrow$ &nbsp; $\nabla f(\vec{a})$ points in the direction of largest growth of $f$ at $\vec{x} = \vec{a}$!

    $\Longrightarrow$ &nbsp; $\nabla f(\vec{a})$ is the direction of steepest ascent of $f$ at $\vec{x} = \vec{a}$!

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2, \qquad
    \nabla f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) = \begin{bmatrix} 2 a^1 \\ 2 a^2 \end{bmatrix}
    $$

    For $\vec{a} \neq \vec{0}$, $f(\vec{x})$ increases fastest along the radial direction.

    Direction of steepest descent (fastest decrease) of $f$ at $\vec{a} \neq \vec{0}$

    $$
    \leadsto \quad -\nabla f(\vec{a}) = \begin{bmatrix} -2 a^1 \\ -2 a^2 \end{bmatrix}
    $$

    Directions with no ascent / descent

    $$
    \leadsto \quad \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \ \text{ s.t. } \ \nabla f(\vec{a}) \cdot \vec{v} = 0 \quad \Longleftrightarrow \quad Df(\vec{a})(\vec{v}) = 0
    $$

    $$
    \nabla f(\vec{a}) \cdot \vec{v} = 2 a^1 v^1 + 2 a^2 v^2 = 0 \quad \Longleftrightarrow \quad v^2 = -\frac{a^1}{a^2}\, v^1 \qquad (\text{assuming } a^2 \neq 0)
    $$

    $$
    \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \in \big( \nabla f(\vec{a}) \big)^{\perp} \qquad \text{orthogonal complement of } \nabla f(\vec{a})
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
def _(BLUE, Figure, GREEN, RED, arrow, cross_axes, ga1, ga2, math, mo, np):
    OCHRE = "#9a6b1f"
    _a = (ga1.value, ga2.value)
    _R = math.hypot(*_a)
    _grad = (2 * _a[0], 2 * _a[1])

    _fig = Figure(figsize=(4.8, 4.6), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-4.6, 4.8), (-4.6, 4.8), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    for _r in (0.75, 1.5, 2.25, 3.0, 3.75):
        _ax.plot(_r * np.cos(_th), _r * np.sin(_th), color="#bbbbbb", lw=0.7)
    _ax.plot(_R * np.cos(_th), _R * np.sin(_th), color=RED, lw=1.8)
    if _R > 0:
        _t = (-_a[1] / _R, _a[0] / _R)
        _ax.plot([_a[0] - 1.6 * _t[0], _a[0] + 1.6 * _t[0]], [_a[1] - 1.6 * _t[1], _a[1] + 1.6 * _t[1]], color=BLUE, lw=1.3)
        arrow(_ax, _a, (_a[0] + _grad[0], _a[1] + _grad[1]), OCHRE, r"$\nabla f(\vec{a})$", at_tip=True)
    arrow(_ax, (0, 0), _a, GREEN)
    _ax.plot(*_a, "o", color=GREEN, ms=5)
    _ax.annotate(r"$\vec{a}$", (_a[0] / 2, _a[1] / 2), textcoords="offset points", xytext=(2, -20), color=GREEN, fontsize=15)

    mo.vstack(
        [
            mo.hstack([ga1, ga2], justify="start", gap=3),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        rf"$$\nabla f(\vec{{a}}) = 2\vec{{a}} = \begin{{bmatrix}} {_grad[0]:g} \\ {_grad[1]:g} \end{{bmatrix}}$$"
                        "\n\n"
                        rf"$$f^{{-1}}(R^2) = \left\{{\, \begin{{bmatrix}} x^1 \\ x^2 \end{{bmatrix}} \;\middle|\; (x^1)^2 + (x^2)^2 = R^2 \,\right\}}, \qquad R^2 = {_R**2:.2f}$$"
                        "\n\n"
                        + (
                            r"The blue line shows the directions $\vec{v} \in \big( \nabla f(\vec{a}) \big)^{\perp}$."
                            if _R > 0
                            else r"$Df(\vec{a})(\vec{v}) = 0$ for every $\vec{v}$."
                        )
                    ).style({"max-width": "28rem"}),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
        ]
    )
    return (OCHRE,)


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, arrow, definition, mo, np, theorem):
    _fig = Figure(figsize=(3.4, 2.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-2.2, 2.6)
    _ax.set_ylim(-0.9, 2.1)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _x = np.linspace(-2, 2, 100)
    _ax.plot(_x, -0.12 * _x**2 - 0.15 * _x, color=RED, lw=1.8)
    _n = np.array([0.15, 1.0]) / np.hypot(0.15, 1.0)
    arrow(_ax, (0, 0), tuple(1.6 * _n), BLUE, r"$\nabla f(\vec{a})$", at_tip=True)
    _tv = np.array([1.0, -0.15]) / np.hypot(0.15, 1.0)
    _sq = np.array([0.22 * _tv, 0.22 * _tv + 0.22 * _n, 0.22 * _n])
    _ax.plot(_sq[:, 0], _sq[:, 1], color=BLUE, lw=1)
    _ax.plot(0, 0, "o", color=BLUE, ms=4)
    _ax.text(-0.35, -0.42, r"$\vec{a}$", color=BLUE, fontsize=15)
    _ax.text(1.5, -0.45, r"$f^{-1}(b)$", color=RED, fontsize=14)

    mo.vstack(
        [
            mo.hstack(
                [
                    theorem(
                        r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$ with $f(\vec{a}) = b$ and $\nabla f(\vec{a}) \neq \vec{0}$, then $\nabla f(\vec{a})$ is perpendicular to $f^{-1}(b)$

    $$
    \nabla f(\vec{a}) \perp f^{-1}(b)
    $$
    """
                    ),
                    _fig,
                ],
                widths=[3, 2],
                gap=2,
                align="center",
            ),
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
    """
            ),
            mo.md(
                r"""
    **Remark.** For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ differentiable at $x = a$

    $$
    g(x) = f(a) + f'(a)(x - a)
    $$

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
    \mathrm{graph}(g) = \text{plane in } \mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R} \text{ through } \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} \text{ with normal } \vec{n} = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] \dfrac{\partial f}{\partial x^2}(\vec{a}) \\[8pt] -1 \end{bmatrix}
    $$

    (the **tangent plane** to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$)

    $$
    = \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ y \end{bmatrix} \;\middle|\; y = f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \frac{\partial f}{\partial x^2}(\vec{a})\, (x^2 - a^2),\ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\}
    $$

    $$
    \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \frac{\partial f}{\partial x^2}(\vec{a})\, (x^2 - a^2) - \big( y - f(\vec{a}) \big) = 0
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

    (e) Sketch $f^{-1}(\ln(2))$ and draw $\nabla f(\vec{a})$ at $\vec{a}$.
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
