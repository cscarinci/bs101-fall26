import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 13 · Higher order derivatives", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(13, "Higher order derivatives")
    return


@app.cell(hide_code=True)
def _(lk):
    # Helpers of this lecture: bare coordinate axes

    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None, at=(0, 0)):
        """A bare pair of coordinate axes crossing at `at`, drawn over the ranges xr and yr."""
        lk.arrow(ax, (xr[0], at[1]), (xr[1], at[1]), "black", lw=0.9)
        lk.arrow(ax, (at[0], yr[0]), (at[0], yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], at[1]), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (at[0], yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    a_taylor = lk.slider(-1.5, 0.7, step=0.1, value=0.5, label="$a$")
    return (a_taylor,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"Chain rule for maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$",
        r"""
        $$
        D(g \circ f)(\vec{x}) = Dg(f(\vec{x})) \cdot Df(\vec{x})
        $$

        > $\leadsto$ &nbsp; assuming $f$ differentiable at $\vec{x} \in \mathbb{R}^n$

        > > <span class='lk-ghost'>assuming </span>$g$ differentiable at $\vec{y} = f(\vec{x}) \in \mathbb{R}^m$
        """,
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"Local maxima and minima of scalar valued functions", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 3.1, 3.2")
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, lk, np):
    # module: motivation
    # recall: local maximum in one variable
    # y = f(x) with two local maxima and a local minimum, the horizontal tangent line at each, and two slanted tangent
    # lines on either side of the maximum at x = a
    def _f(x):
        return 1.25 + 0.55 * np.cos(2.4 * (x - 1)) - 0.05 * (x - 1) ** 2

    def _df(x, h=1e-5):
        return (_f(x + h) - _f(x - h)) / (2 * h)

    _x = np.linspace(-0.25, 4.0, 400)
    _y = _f(_x)
    _ext = [_x[k] for k in range(1, len(_x) - 1) if (_y[k] - _y[k - 1]) * (_y[k + 1] - _y[k]) < 0]
    _a = _ext[0]
    _fig = Figure(figsize=(4.4, 2.4), layout="constrained")
    _ax = _fig.add_axes((0, 0, 1, 1))
    _ax.set_xlim(-0.6, 5.2)
    _ax.set_ylim(-0.35, 2.55)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.55, 4.3), (-0.3, 2.45), "$x$")
    for _e in _ext:
        _ax.plot([_e - 0.5, _e + 0.5], [_f(_e)] * 2, color=lk.GREEN, lw=1.3)
        _ax.plot(_e, _f(_e), "o", color=lk.GREEN, ms=3.5, zorder=5)
    for _t in (_a - 0.42, _a + 0.42):
        _ax.plot([_t - 0.38, _t + 0.38], [_f(_t) - 0.38 * _df(_t), _f(_t) + 0.38 * _df(_t)], color=lk.ORANGE, lw=1.2)
        _ax.plot(_t, _f(_t), "o", color=lk.ORANGE, ms=3, zorder=5)
    _ax.plot(_x, _y, color=lk.RED, lw=1.6)
    _ax.plot([_a, _a], [-0.06, 0.06], color="black", lw=0.9)
    _ax.text(_a, -0.12, "$a$", ha="center", va="top", fontsize=13)
    _ax.text(_a + 0.15, _f(_a) + 0.42, "$y = f(a) + f'(a)(x - a)$", color=lk.GREEN, fontsize=12, ha="left", va="bottom")
    _ax.text(4.05, _f(4.0), "$y = f(x)$", color=lk.RED, fontsize=12, ha="left", va="center")
    lk.recall(
        [
            lk.aside(
                r"if $f : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable and has a <span class='lk-mark'>local maximum</span> at $x = a$",
                "or local minimum",
            ),
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\mk{f'(a) = 0}$",
                r"tangent line to $\mathrm{graph}(f)$ is horizontal at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$",
            ),
            lk.figure(_fig),
            r"Moreover, if $f' : \mathbb{R} \longrightarrow \mathbb{R}$ is also differentiable then",
            lk.aside(
                r"> $f'(a) = 0$ and $f''(a) < 0$ &nbsp; $\Longrightarrow$ &nbsp; local maximum at $x = a$",
                r"$f''(a) > 0$: local minimum",
            ),
            r"""
            > > $\leadsto$ &nbsp; $f'(x)$ is strictly decreasing nearby $x = a$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: motivation
    # prose: why higher order derivatives
    lk.prose(r"$\leadsto$ &nbsp; to discuss local maxima/minima of multivariable functions we need to discuss higher order derivatives")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # section
    lk.section("Higher order derivatives")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # definition: C^2-smooth
    lk.definition(
        [
            r"$f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is called **$C^2$-smooth** at $\vec{x} = \vec{a}$ if all partial derivatives ${\large\tfrac{\partial f}{\partial x^i}}(\vec{x})$ are well-defined around $\vec{x} = \vec{a}$, their partial derivatives ${\large\tfrac{\partial}{\partial x^j} \tfrac{\partial f}{\partial x^i}}(\vec{x})$ are also all well-defined around $\vec{x} = \vec{a}$, and are all continuous at $\vec{x} = \vec{a}$",
            lk.aside(
                r"$$ \frac{\partial}{\partial x^j} \frac{\partial f}{\partial x^i}(\vec{x}) = \mk{\frac{\partial^2 f}{\partial x^j \partial x^i}(\vec{x})} $$",
                r"second order partial derivative<br>of $f$ with respect to $x^i$ and $x^j$",
            ),
        ],
        label="def-c2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # remark: C^2 implies C^1 implies differentiable implies continuous
    lk.remark(
        [
            r"""
            By definition: $f$ $C^2$-smooth at $\vec{x} = \vec{a}$

            > $\Longrightarrow$ &nbsp; $f$ $C^1$-smooth at $\vec{x} = \vec{a}$
            """,
            lk.aside(r"> $\Longrightarrow$ &nbsp; $f$ differentiable at $\vec{x} = \vec{a}$", "opposite directions are NOT true!"),
            r"> $\Longrightarrow$ &nbsp; $f$ continuous at $\vec{x} = \vec{a}$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # definition: Hessian matrix
    lk.definition(
        r"""
        For $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ $C^2$-smooth at $\vec{x} = \vec{a}$

        $$
        Hf(\vec{a}) = \begin{bmatrix}
        {\large\tfrac{\partial^2 f}{\partial x^1 \partial x^1}}(\vec{a}) & {\large\tfrac{\partial^2 f}{\partial x^1 \partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial^2 f}{\partial x^1 \partial x^n}}(\vec{a})\\[6pt]
        {\large\tfrac{\partial^2 f}{\partial x^2 \partial x^1}}(\vec{a}) & {\large\tfrac{\partial^2 f}{\partial x^2 \partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial^2 f}{\partial x^2 \partial x^n}}(\vec{a})\\
        \vdots & \vdots & \ddots & \vdots\\
        {\large\tfrac{\partial^2 f}{\partial x^n \partial x^1}}(\vec{a}) & {\large\tfrac{\partial^2 f}{\partial x^n \partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial^2 f}{\partial x^n \partial x^n}}(\vec{a})
        \end{bmatrix} \in \mathrm{Mat}(n \times n)
        $$

        is called the **Hessian matrix** of $f$ at $\vec{x} = \vec{a}$

        $\leadsto$ &nbsp; $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$ generalizes $f'(a)$

        > $Hf(\vec{a}) \in \mathrm{Mat}(n \times n)$ generalizes $f''(a)$
        """,
        label="def-hessian",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # remark: Hessian is the derivative of the gradient
    lk.remark(
        [
            r"""
            $f$ $C^2$-smooth at $\vec{x} = \vec{a}$

            > $\Longrightarrow$ &nbsp; $\vec{\nabla} f$ $C^1$-smooth at $\vec{x} = \vec{a}$
            """,
            lk.aside(r"> $\leadsto$ &nbsp; $Hf(\vec{a}) = D(\vec{\nabla} f)(\vec{a})$", "Hessian is the derivative<br>of the gradient!"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # theorem: symmetry of second order partial derivatives
    lk.theorem(
        [
            r"$f$ $C^2$-smooth at $\vec{x} = \vec{a}$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\dfrac{\partial^2 f}{\partial x^j \partial x^i}(\vec{a}) = \dfrac{\partial^2 f}{\partial x^i \partial x^j}(\vec{a}) \quad \forall \, i, j = 1, \dots, n$",
                "order of partial derivative<br>does not matter!",
            ),
        ],
        label="thm-symmetry",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: higher order derivatives
    # example: x^1 e^{x^2}, gradient and Hessian
    lk.example(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$

        $\dfrac{\partial f}{\partial x^1}(\vec{x}) = e^{x^2}$, &nbsp; $\dfrac{\partial f}{\partial x^2}(\vec{x}) = x^1 e^{x^2}$ &nbsp; $\leadsto$ &nbsp; $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} e^{x^2} \\ x^1 e^{x^2} \end{bmatrix} \in \mathbb{R}^2$

        > <span class='lk-ghost'>$\dfrac{\partial f}{\partial x^1}(\vec{x}) = e^{x^2}$, &nbsp; $\dfrac{\partial f}{\partial x^2}(\vec{x}) = x^1 e^{x^2}$ &nbsp; </span>$\Longrightarrow$ &nbsp; $\vec{\nabla} f : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$

        $$
        \begin{aligned}
        \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{x}) &= 0 & \qquad \frac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{x}) &= e^{x^2}\\[4pt]
        \frac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{x}) &= e^{x^2} & \qquad \frac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{x}) &= x^1 e^{x^2}
        \end{aligned}
        $$

        $\leadsto$ &nbsp; $Hf(\vec{x}) = \begin{bmatrix} 0 & e^{x^2} \\ e^{x^2} & x^1 e^{x^2} \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$

        $\leadsto$ &nbsp; $D(\vec{\nabla} f)(\vec{x}) = \begin{bmatrix} {\large\tfrac{\partial}{\partial x^1}}(e^{x^2}) & {\large\tfrac{\partial}{\partial x^2}}(e^{x^2}) \\[4pt] {\large\tfrac{\partial}{\partial x^1}}(x^1 e^{x^2}) & {\large\tfrac{\partial}{\partial x^2}}(x^1 e^{x^2}) \end{bmatrix}$
        """,
        label="ex-hessian",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic approximation
    # section
    lk.section("Quadratic approximation")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic approximation
    # recall: affine approximation
    lk.recall(
        [
            r"$f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$ &nbsp; <span class='lk-mark'>affine approximation</span> of $f$ at $\vec{a}$",
                "1st order Taylor approximation",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, a_taylor, lk, math, np):
    # module: quadratic approximation
    # definition: quadratic approximation
    # y = f(x), its 2nd order Taylor approximation (parabola), its tangent line and the line y = f(a), all through
    # the point at x = a; f(x) = e^x and a chosen with the slider
    _a = a_taylor.value
    _fa = math.exp(_a)
    _x = np.linspace(-2.3, 2.4, 300)
    _fig = Figure(figsize=(5.6, 3.4), layout="constrained")
    _ax = _fig.add_axes((0, 0, 1, 1))
    _ax.set_xlim(-2.45, 3.75)  # room on the right for the names at the ends of the tangent line and of y = f(a)
    _ax.set_ylim(-0.85, 5.3)
    _ax.axis("off")
    lk.arrow(_ax, (-2.45, 0), (2.6, 0), "black", lw=0.9)
    lk.arrow(_ax, (-2.3, -0.25), (-2.3, 5.2), "black", lw=0.9)
    _ax.annotate("$x$", (2.6, 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
    _ax.annotate("$y$", (-2.3, 5.2), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)
    with np.errstate(over="ignore"):
        _ax.plot(_x, np.full_like(_x, _fa), color=lk.GREY, lw=1.2, ls=(0, (4, 3)))
        _ax.plot(_x, _fa + _fa * (_x - _a), color=lk.GREEN, lw=1.4)
        _ax.plot(_x, _fa + _fa * (_x - _a) + 0.5 * _fa * (_x - _a) ** 2, color=lk.ORANGE, lw=1.4)
        _ax.plot(_x, np.exp(_x), color=lk.BLUE, lw=1.6)
    _ax.plot(_a, _fa, "o", color="black", ms=4, zorder=4)
    _ax.plot([_a, _a], [-0.08, 0.08], color="black", lw=0.9)
    _ax.text(_a, -0.55, "$a$", ha="center", va="center", fontsize=13)
    # every name stays at one place, or moves with its own line, as a changes
    _ax.text(-1.85, 4.39, "$y = f(a) + f'(a)(x - a)$\n$\\;\\; + \\dfrac{1}{2} f''(a)(x - a)^2$", color=lk.ORANGE, fontsize=12, ha="left", va="bottom")
    _ax.text(0.28, 4.17, "$y = f(x)$", color=lk.BLUE, fontsize=12, ha="left", va="bottom")
    _ax.text(2.48, _fa, "$y = f(a)$", color=lk.GREY, fontsize=12, ha="left", va="center")
    _xe = min(2.4, _a - 1 + 5.2 / _fa)  # where the tangent line leaves the picture: its right end, or the top
    _ax.text(_xe + 0.08, min(_fa + _fa * (_xe - _a), 4.75), "$y = f(a)$\n$\\;\\; + f'(a)(x - a)$", color=lk.GREEN, fontsize=12, ha="left", va="center")
    _ax.set_ylim(-0.85, 5.3)
    lk.definition(
        [
            r"""
            $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ $C^2$-smooth at $\vec{x} = \vec{a}$

            $$
            f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2} (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})
            $$
            """,
            lk.aside(
                r"is the <span class='lk-mark'>**quadratic approximation**</span> of $f$ at $\vec{a}$",
                "2nd order Taylor approximation",
            ),
            lk.interactive(_fig, controls=[a_taylor]),
        ],
        label="def-quadratic",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic approximation
    # theorem: the quadratic approximation is good
    lk.theorem(
        [
            r"The 2nd order Taylor approximation of $f$ at $\vec{a}$ is a good approximation",
            lk.aside(
                r"""
                $$
                \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) - \frac{1}{2} (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}{\mk{\lVert \vec{x} - \vec{a} \rVert^2}} = 0
                $$
                """,
                r"error goes to zero<br>faster than $(\text{distance})^2$",
            ),
        ],
        label="thm-taylor",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic approximation
    # example: quadratic approximation of x^1 e^{x^2} at (1, 0)
    lk.example(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$ at $\vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$

        > $\leadsto$ &nbsp; $f(\vec{a}) = 1$, &nbsp; $Df(\vec{a}) = \begin{bmatrix} 1 & 1 \end{bmatrix}$, &nbsp; $Hf(\vec{a}) = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}$

        $$
        \begin{aligned}
        \Longrightarrow \quad g(\vec{x}) &= 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} + \frac{1}{2} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} \cdot \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix}\\[4pt]
        &= 1 + (x^1 - 1) + x^2 + \frac{1}{2} (x^1 - 1) x^2 + \frac{1}{2} x^2 (x^1 - 1 + x^2)\\[4pt]
        &= 0 + x^1 + x^1 x^2 + \frac{1}{2} (x^2)^2
        \end{aligned}
        $$
        """,
        label="ex-quadratic",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic approximation
    # remark: the same from single variable Taylor
    lk.remark(
        r"""
        From Taylor approximation in single variable calculus

        > $e^t = 1 + t + {\large\tfrac{1}{2}} t^2 + \cdots$ &nbsp; (near $t = 0$)

        > > $\Longrightarrow$ &nbsp; $x^1 e^{x^2} = x^1 \left( 1 + x^2 + {\large\tfrac{1}{2}} (x^2)^2 + \cdots \right)$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # section
    lk.section("Local extrema, critical points, 2nd derivative test")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # definition: local maximum and minimum
    lk.definition(
        [
            r"Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$, a point $\vec{a} \in \mathbb{R}^n$ is",
            lk.aside(
                r"> • &nbsp; <span class='lk-mark'>**local**</span> **maximum** of $f$ if there is an open ball $B$ around $\vec{a}$ such that $f(\vec{x}) \leq f(\vec{a})$ $\forall \, \vec{x} \in B$",
                "only around nearby points",
            ),
            r"> • &nbsp; **local minimum** of $f$ if there is an open ball $B$ around $\vec{a}$ such that $f(\vec{x}) \geq f(\vec{a})$ $\forall \, \vec{x} \in B$",
        ],
        label="def-local-extrema",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # theorem: the derivative vanishes at a local extremum
    lk.theorem(
        [
            lk.aside(r"$f$ differentiable and has local <span class='lk-mark'>maximum</span> at $\vec{x} = \vec{a}$", "(minimum)"),
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the <span class='lk-mark'>zero linear map</span>",
                r"zero linear map: $Df(\vec{a})(\vec{v}) = 0$",
            ),
            r"> $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a}) = \vec{0} \in \mathbb{R}^n$",
        ],
        label="thm-derivative-zero",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # proof
    lk.proof(
        r"""
        For any $\vec{v} \in \mathbb{R}^n$, let $\gamma(t) = \vec{a} + t\vec{v}$ and $g(t) = f \circ \gamma(t)$

        $\vec{a}$ is local max of $f$ &nbsp; $\Longrightarrow$ &nbsp; $0$ is local max of $g$ $\forall \, \vec{v}$

        $0 = g'(0) = (f \circ \gamma)'(0) = Df(\gamma(0))(\gamma'(0)) = Df(\vec{a})(\vec{v})$

        > $\Longrightarrow$ &nbsp; $Df(\vec{a})(\vec{v}) = 0 \quad \forall \, \vec{v} \in \mathbb{R}^n$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # definition: critical point
    lk.definition(r"If $\vec{\nabla} f(\vec{a}) = \vec{0}$ we call $\vec{a}$ a **critical point** of $f$", label="def-critical")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # remark: strategy
    lk.remark(
        [
            r"""
            $f$ differentiable, $\vec{a}$ local extremum

            > $\Longrightarrow$ &nbsp; $\vec{a}$ is critical point
            """,
            lk.gap(),
            r"$\leadsto$ &nbsp; strategy to find maxima/minima is to find critical points",
            lk.aside(
                r"> and decide if they are <span class='lk-mark'>local maxima or local minima</span>",
                "there are also critical points<br>that are not local extrema!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # definition: saddle point
    lk.definition(r"A critical point that is not a local extremum is called a **saddle point**", label="def-saddle")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # theorem: second derivative test with v . Hv
    lk.theorem(
        r"""
        If $f$ is $C^2$-smooth at a critical point $\vec{a}$, let $H = Hf(\vec{a}) \in \mathrm{Mat}(n \times n)$ be the Hessian matrix, then

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 12em">$\vec{a}$ is a local maximum if</span>$\vec{v} \cdot H\vec{v} < 0 \quad \forall \, \vec{v} \neq \vec{0}$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 12em">$\vec{a}$ is a local minimum if</span>$\vec{v} \cdot H\vec{v} > 0 \quad \forall \, \vec{v} \neq \vec{0}$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 12em">$\vec{a}$ is a saddle point if</span>$\vec{u} \cdot H\vec{u} < 0$, $\vec{v} \cdot H\vec{v} > 0$ for some $\vec{u}, \vec{v} \in \mathbb{R}^n$
        """,
        label="thm-hessian-test",
    )
    return


if __name__ == "__main__":
    app.run()
