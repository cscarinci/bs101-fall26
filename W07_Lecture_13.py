import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 13 · Local maxima and minima of scalar valued functions", css_file="bs101.css")


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
            arrowprops={"arrowstyle": "->,head_width=0.3,head_length=0.5", "color": color, "lw": 1.4, "shrinkA": 0, "shrinkB": 0, **kw},
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
    header("Lecture 13", "Week 07", "Lecture 13 · Local maxima and minima of scalar valued functions")
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

    Chain rule for maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$

    $$
    D(g \circ f)(\vec{x}) = Dg(f(\vec{x})) \cdot Df(\vec{x})
    $$

    assuming $f$ differentiable at $\vec{x} \in \mathbb{R}^n$, $g$ differentiable at $\vec{y} = f(\vec{x}) \in \mathbb{R}^m$

    **Today:** Local maxima and minima of scalar valued functions

    **Recall:** if $f : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable and has a local maximum at $x = a$ (or local minimum)

    $$
    \Longrightarrow \quad f'(a) = 0 \qquad \left( \text{tangent line to } \mathrm{graph}(f) \text{ is horizontal at } \begin{bmatrix} a \\ f(a) \end{bmatrix} \right)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    a_ext = mo.ui.slider(-0.4, 4.6, 0.05, value=0.5, label="$a$", show_value=True)
    return (a_ext,)


@app.cell(hide_code=True)
def _(Figure, GREEN, RED, a_ext, cross_axes, math, mo, np):
    OCHRE = "#9a6b1f"

    def _f(x):
        return 1.3 + np.sin(1.9 * x - 0.4) + 0.12 * x

    _a = a_ext.value
    _fa = float(_f(_a))
    _d1 = 1.9 * math.cos(1.9 * _a - 0.4) + 0.12
    _d2 = -1.9**2 * math.sin(1.9 * _a - 0.4)

    _fig = Figure(figsize=(7.4, 3.4), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-0.9, 5.4), (-0.5, 3.4))
    _x = np.linspace(-0.7, 5.0, 300)
    _ax.plot(_x, _f(_x), color=RED, lw=1.8)
    _s = np.array([-1.3, 1.3])
    _ax.plot(_a + _s, _fa + _d1 * _s, color=OCHRE, lw=1.5, label="$y = f(a) + f'(a)(x - a)$")
    _ax.plot(_a, _fa, "o", color=OCHRE, ms=5)
    _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), frameon=False, fontsize=12)
    _ax.plot([_a, _a], [-0.06, 0.06], color=GREEN, lw=1.2)
    _ax.text(_a, -0.35, "$a$", color=GREEN, ha="center", fontsize=14)
    _ax.text(4.6, 0.9, "$y = f(x)$", color=RED, fontsize=13)
    _ax.set_clip_on(False)
    _ax.set_ylim(-0.5, 3.4)

    mo.vstack(
        [
            mo.hstack([a_ext], justify="start", gap=3),
            mo.md("| | |\n|:--|:--|\n" + rf"| $f'(a)$ | ${_d1:.2f}$ |" + "\n" + rf"| $f''(a)$ | ${_d2:.2f}$ |"),
            _fig,
        ]
    )
    return (OCHRE,)


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    Moreover, if $f' : \mathbb{R} \longrightarrow \mathbb{R}$ is also differentiable then, at a local maximum $x = a$, $f''(a) \leq 0$

    Conversely, if $f'(a) = 0$ and $f''(a) < 0$ &nbsp; $\Longrightarrow$ &nbsp; $f'(x)$ is strictly decreasing nearby $x = a$ &nbsp; $\Longrightarrow$ &nbsp; $x = a$ is a local maximum

    To discuss local maxima / minima of multivariable functions we need to discuss higher order derivatives.
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is called **$C^2$-smooth** at $\vec{x} = \vec{a}$ if all partial derivatives $\dfrac{\partial f}{\partial x^i}(\vec{x})$ are well-defined around $\vec{x} = \vec{a}$, their partial derivatives $\dfrac{\partial}{\partial x^j} \dfrac{\partial f}{\partial x^i}(\vec{x})$ are also all well-defined around $\vec{x} = \vec{a}$, and are all continuous at $\vec{x} = \vec{a}$

    $$
    \frac{\partial}{\partial x^j} \frac{\partial f}{\partial x^i}(\vec{x}) = \frac{\partial^2 f}{\partial x^j \partial x^i}(\vec{x}) \qquad \text{second order partial derivative of } f \text{ wrt } x^i \text{ and } x^j
    $$
    """
            ),
            mo.md(
                r"""
    **Remark.** By definition: $f$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $\Longrightarrow$ &nbsp; $f$ $C^1$-smooth at $\vec{x} = \vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $f$ differentiable at $\vec{x} = \vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $f$ continuous at $\vec{x} = \vec{a}$

    Opposite directions are NOT true!
    """
            ),
            definition(
                r"""
    For $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $$
    Hf(\vec{a}) = \begin{bmatrix}
    \dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) & \dfrac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^1 \partial x^n}(\vec{a}) \\[10pt]
    \dfrac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{a}) & \dfrac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^2 \partial x^n}(\vec{a}) \\
    \vdots & \vdots & \ddots & \vdots \\
    \dfrac{\partial^2 f}{\partial x^n \partial x^1}(\vec{a}) & \dfrac{\partial^2 f}{\partial x^n \partial x^2}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^n \partial x^n}(\vec{a})
    \end{bmatrix} \in \mathrm{Mat}(n \times n)
    $$

    is called the **Hessian matrix** of $f$ at $\vec{x} = \vec{a}$.
    """
            ),
            mo.md(
                r"""
    $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$ generalizes $f'(a)$

    $Hf(\vec{a}) \in \mathrm{Mat}(n \times n)$ generalizes $f''(a)$

    **Remark.** $f$ $C^2$-smooth at $\vec{x} = \vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{\nabla} f$ $C^1$-smooth at $\vec{x} = \vec{a}$

    $$
    \leadsto \quad Hf(\vec{a}) = D(\vec{\nabla} f)(\vec{a}) \qquad \text{Hessian is the derivative of the gradient!}
    $$
    """
            ),
            theorem(
                r"""
    $f$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $$
    \Longrightarrow \quad \frac{\partial^2 f}{\partial x^j \partial x^i}(\vec{a}) = \frac{\partial^2 f}{\partial x^i \partial x^j}(\vec{a}) \qquad \forall\, i, j = 1, \dots, n
    $$

    Order of partial derivative does not matter!
    """
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$

    $$
    \frac{\partial f}{\partial x^1}(\vec{x}) = e^{x^2}, \qquad \frac{\partial f}{\partial x^2}(\vec{x}) = x^1 e^{x^2}
    \qquad \leadsto \qquad \vec{\nabla} f(\vec{x}) = \begin{bmatrix} e^{x^2} \\ x^1 e^{x^2} \end{bmatrix} \in \mathbb{R}^2
    \qquad \Longrightarrow \quad \vec{\nabla} f : \mathbb{R}^2 \longrightarrow \mathbb{R}^2
    $$

    $$
    \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{x}) = 0, \qquad
    \frac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{x}) = e^{x^2}, \qquad
    \frac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{x}) = e^{x^2}, \qquad
    \frac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{x}) = x^1 e^{x^2}
    $$

    $$
    \leadsto \quad Hf(\vec{x}) = \begin{bmatrix} 0 & e^{x^2} \\ e^{x^2} & x^1 e^{x^2} \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    $$

    $$
    \leadsto \quad D(\vec{\nabla} f)(\vec{x}) = \begin{bmatrix}
    \dfrac{\partial}{\partial x^1}\big( e^{x^2} \big) & \dfrac{\partial}{\partial x^2}\big( e^{x^2} \big) \\[10pt]
    \dfrac{\partial}{\partial x^1}\big( x^1 e^{x^2} \big) & \dfrac{\partial}{\partial x^2}\big( x^1 e^{x^2} \big)
    \end{bmatrix}
    $$

    **Recall:** $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$

    $$
    \Longrightarrow \quad f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \qquad \text{affine approx. of } f \text{ at } \vec{a} \quad (\text{1st order Taylor approx.})
    $$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $$
    f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})
    $$

    is the **quadratic approx.** of $f$ at $\vec{a}$ &nbsp; (2nd order Taylor approx.)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_taylor = mo.ui.slider(-1.5, 1.5, 0.1, value=0.5, label="$a$", show_value=True)
    return (a_taylor,)


@app.cell(hide_code=True)
def _(Figure, GREEN, OCHRE, RED, a_taylor, cross_axes, math, mo, np):
    PURPLE = "#7b3fa0"
    _a = a_taylor.value
    _fa = math.exp(_a)
    _x = np.linspace(-2.6, 2.6, 300)

    _fig = Figure(figsize=(5.4, 4.2), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-2.6, 2.8), (-0.8, 5.2))
    _ax.plot(_x, np.exp(_x), color=RED, lw=2.0, label="$y = f(x)$")
    _ax.plot(_x, _fa + _fa * (_x - _a) + 0.5 * _fa * (_x - _a) ** 2, color=GREEN, lw=1.5, label=r"$y = f(a) + f'(a)(x - a) + \frac{1}{2} f''(a)(x - a)^2$")
    _ax.plot(_x, _fa + _fa * (_x - _a), color=OCHRE, lw=1.3, label="$y = f(a) + f'(a)(x - a)$")
    _ax.plot(_x, np.full_like(_x, _fa), color=PURPLE, lw=1.3, label="$y = f(a)$")
    _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False, fontsize=11)
    _ax.plot(_a, _fa, "o", color="black", ms=5)
    _ax.plot([_a, _a], [-0.08, 0.08], color="black", lw=1.2)
    _ax.text(_a, -0.5, "$a$", ha="center", fontsize=14)
    _ax.set_ylim(-0.8, 5.2)

    mo.vstack(
        [
            mo.hstack([a_taylor], justify="start", gap=3),
            mo.md("| | |\n|:--|:--|\n" + r"| $f(x)$ | $e^x$ |" + "\n" + rf"| $f(a) = f'(a) = f''(a)$ | ${_fa:.3f}$ |"),
            mo.center(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    The 2nd order Taylor approx. of $f$ at $\vec{a}$ is a good approximation

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) - \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert^2} = 0
    $$

    (error goes to zero faster than $(\text{dist})^2$)
    """
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$ at $\vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$

    $$
    \leadsto \quad f(\vec{a}) = 1, \qquad Df(\vec{a}) = \begin{bmatrix} 1 & 1 \end{bmatrix}, \qquad Hf(\vec{a}) = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad g(\vec{x}) &= 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} + \frac{1}{2} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} \cdot \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} \\[4pt]
    &= 1 + (x^1 - 1) + x^2 + \frac{1}{2} (x^1 - 1) x^2 + \frac{1}{2} x^2 (x^1 - 1 + x^2) \\[4pt]
    &= 0 + x^1 + x^1 x^2 + \frac{1}{2} (x^2)^2
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    qx1 = mo.ui.slider(0, 2, 0.05, value=1.1, label="$x^1$", show_value=True)
    qx2 = mo.ui.slider(-1, 1, 0.05, value=-0.1, label="$x^2$", show_value=True)
    return qx1, qx2


@app.cell(hide_code=True)
def _(math, mo, qx1, qx2):
    _x1, _x2 = qx1.value, qx2.value
    _f = _x1 * math.exp(_x2)
    _g1 = 1 + (_x1 - 1) + _x2
    _g2 = _x1 + _x1 * _x2 + 0.5 * _x2**2
    mo.vstack(
        [
            mo.hstack([qx1, qx2], justify="start", gap=3),
            mo.md(
                "| | value | error |\n|:--|--:|--:|\n"
                rf"| $f(\vec{{x}})$ | ${_f:.4f}$ | |"
                "\n"
                rf"| 1st order Taylor approx. | ${_g1:.4f}$ | ${_f - _g1:.4f}$ |"
                "\n"
                rf"| 2nd order Taylor approx. | ${_g2:.4f}$ | ${_f - _g2:.4f}$ |"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** From Taylor approx. in single variable calculus

    $$
    e^t = 1 + t + \frac{1}{2} t^2 + \cdots \quad (\text{near } t = 0)
    \qquad \Longrightarrow \qquad x^1 e^{x^2} = x^1 \left( 1 + x^2 + \frac{1}{2} (x^2)^2 + \cdots \right)
    $$

    ## Local extrema, critical points, 2nd derivative test
    """
            ),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$, a point $\vec{a} \in \mathbb{R}^n$ is

    - **local maximum** of $f$ if there is an open ball $B$ around $\vec{a}$ such that $f(\vec{x}) \leq f(\vec{a}) \quad \forall\, \vec{x} \in B$
    - **local minimum** of $f$ if there is an open ball $B$ around $\vec{a}$ such that $f(\vec{x}) \geq f(\vec{a}) \quad \forall\, \vec{x} \in B$

    (local: only around nearby points)
    """
            ),
            theorem(
                r"""
    $f$ differentiable and has local maximum (minimum) at $\vec{x} = \vec{a}$

    $\Longrightarrow$ &nbsp; $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the zero linear map &nbsp; ($Df(\vec{a})(\vec{v}) = 0$)

    $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a}) = \vec{0} \in \mathbb{R}^n$
    """
            ),
            mo.md(
                r"""
    **Proof.** For any $\vec{v} \in \mathbb{R}^n$, let $\gamma(t) = \vec{a} + t\vec{v}$ and $g(t) = f \circ \gamma(t)$

    $\vec{a}$ is local max of $f$ &nbsp; $\Longrightarrow$ &nbsp; $0$ is local max of $g$ &nbsp; $\forall\, \vec{v}$

    $$
    0 = g'(0) = (f \circ \gamma)'(0) = Df(\gamma(0))(\gamma'(0)) = Df(\vec{a})(\vec{v})
    $$

    $$
    \Longrightarrow \quad Df(\vec{a})(\vec{v}) = 0 \quad \forall\, \vec{v} \in \mathbb{R}^n \qquad \square
    $$
    """
            ),
            definition(
                r"""
    If $\vec{\nabla} f(\vec{a}) = \vec{0}$ we call $\vec{a}$ a **critical point** of $f$.
    """
            ),
            mo.md(
                r"""
    **Remark.** $f$ differentiable, $\vec{a}$ local extremum &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is critical point

    Strategy to find maxima / minima is to find critical points and decide if they are local maxima or local minima.

    There are also critical points that are not local extrema!
    """
            ),
            definition(
                r"""
    A critical point that is not a local extremum is called a **saddle point**.
    """
            ),
            theorem(
                r"""
    If $f$ is $C^2$-smooth at a critical point $\vec{a}$, let $H = Hf(\vec{a}) \in \mathrm{Mat}(n \times n)$ be the Hessian matrix, then

    - $\vec{a}$ is a local maximum if

        $$
        \vec{v} \cdot H\vec{v} < 0 \qquad \forall\, \vec{v} \in \mathbb{R}^n \setminus \{\vec{0}\}
        $$

    - $\vec{a}$ is a local minimum if

        $$
        \vec{v} \cdot H\vec{v} > 0 \qquad \forall\, \vec{v} \in \mathbb{R}^n \setminus \{\vec{0}\}
        $$

    - $\vec{a}$ is a saddle point if

        $$
        \vec{u} \cdot H\vec{u} < 0, \quad \vec{v} \cdot H\vec{v} > 0 \qquad \text{for some } \vec{u}, \vec{v} \in \mathbb{R}^n
        $$
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
