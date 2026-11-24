import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 10 · Properties and interpretations of differentiable functions", css_file="lecturekit/style.css")


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
    lk.lecture(10, "Properties and interpretations of differentiable functions")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math):
    # Helpers of this lecture: a bare sketch, bare coordinate axes, an arrow with its name

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr."""
        lk.arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        lk.arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    def vector(ax, tail, tip, color, label=None, turn=0, r=15):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip; `turn` (degrees)
        rotates the label about the tip. No box behind the label."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            lk.arrow(ax, tail, tip, color)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5)

    return blank, cross_axes, vector


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    ga1 = lk.slider(-1.5, 1.5, step=0.1, value=1, label="$a^1$")
    ga2 = lk.slider(-1.5, 1.5, step=0.1, value=0.6, label="$a^2$")
    return ga1, ga2


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: the four conditions of differentiability for f : R^2 -> R
    lk.recap(
        "Differentiability and the derivative",
        lk.gap(),
        r"""
        $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

        > 1\. &nbsp; has well-defined partial derivatives

        $$
        \begin{aligned}
        \frac{\partial f}{\partial x^1}(\vec{a}) &= \lim_{t \to 0} \frac{f\left( \begin{bmatrix} a^1 + t \\ a^2 \end{bmatrix} \right) - f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t=0} f(\vec{a} + t\vec{e}_1)\\[6pt]
        \frac{\partial f}{\partial x^2}(\vec{a}) &= \lim_{t \to 0} \frac{f\left( \begin{bmatrix} a^1 \\ a^2 + t \end{bmatrix} \right) - f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t=0} f(\vec{a} + t\vec{e}_2)
        \end{aligned}
        $$

        > 2\. &nbsp; has well-defined directional derivatives $\forall \, \vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$

        $$
        Df(\vec{a})(\vec{v}) = \lim_{t \to 0} \frac{f\left( \begin{bmatrix} a^1 + t v^1 \\ a^2 + t v^2 \end{bmatrix} \right) - f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} = \frac{d}{dt} \Big|_{t=0} f(\vec{a} + t\vec{v})
        $$

        > 3\. &nbsp; the map $Df(\vec{a}) : \mathbb{R}^2 \longrightarrow \mathbb{R}$, $\vec{v} \longmapsto Df(\vec{a})(\vec{v})$ is linear

        > > $\Longrightarrow$ &nbsp; $Df(\vec{a})(\vec{v}) = v^1 \dfrac{\partial f}{\partial x^1}(\vec{a}) + v^2 \dfrac{\partial f}{\partial x^2}(\vec{a})$
        """,
        lk.aside(
            r"> > <span class='lk-ghost'>$\Longrightarrow$ &nbsp; $Df(\vec{a})(\vec{v})$</span> $= \mk{\begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \end{bmatrix}} \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$",
            "matrix of partial derivatives",
        ),
        r"> 4\. &nbsp; $Df(\vec{a})(\vec{x} - \vec{a})$ is a linear approximation to $f(\vec{x}) - f(\vec{a})$",
        lk.aside(
            r"""
            $$
            \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
            $$
            """,
            r"it is this approximation that allows<br>us to call $Df(\vec{a})$ the derivative",
        ),
        r"In this case, $Df(\vec{a}) : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **the derivative** of $f$ at $\vec{x} = \vec{a}$",
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Properties and interpretations of differentiable functions", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.3, 2.6")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # remark: the linear approximation implies the other conditions
    lk.remark(
        r"""
        (4) &nbsp; $\Longrightarrow$ &nbsp; (3) &nbsp; $\Longrightarrow$ &nbsp; (2) &nbsp; $\Longrightarrow$ &nbsp; (1)

        > $\leadsto$ &nbsp; we could define differentiability by requiring only the existence of a linear approximation! other conditions follow as consequence!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # example: directional derivatives at 0 that are not linear
    lk.example(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{cases} \dfrac{(x^1)^2 x^2}{\lVert \vec{x} \rVert^2}, & \vec{x} \neq \vec{0}\\[8pt] 0, & \vec{x} = \vec{0} \end{cases}$

        $$
        \begin{aligned}
        Df(\vec{0})(\vec{v}) &= \lim_{t \to 0} \frac{f\left( \begin{bmatrix} t v^1 \\ t v^2 \end{bmatrix} \right) - f\left( \begin{bmatrix} 0 \\ 0 \end{bmatrix} \right)}{t}\\[6pt]
        &= \lim_{t \to 0} \frac{\dfrac{t^3 (v^1)^2 v^2}{t^2 \lVert \vec{v} \rVert^2} - 0}{t} = \frac{(v^1)^2 v^2}{\lVert \vec{v} \rVert^2}
        \end{aligned}
        $$

        > • &nbsp; $Df(\vec{0})(\vec{v})$ defined $\forall \, \vec{v}$

        > • &nbsp; not linear!

        > > $\Longrightarrow$ &nbsp; $f$ is NOT differentiable at $\vec{x} = \vec{0}$!
        """,
        label="ex-not-linear",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # remark: differentiability for n > 2
    lk.remark(
        [
            lk.aside(
                r"""
                Generalization for <span class='lk-mark'>$n > 2$</span>

                > $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \\ \vdots \\ a^n \end{bmatrix}$ if
                """,
                "still $m = 1$",
            ),
            lk.aside(
                r"> > • &nbsp; $Df(\vec{a}) = \mk{\begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix}} : \mathbb{R}^n \longrightarrow \mathbb{R}$",
                "matrix of partial derivatives",
            ),
            lk.aside(
                r"> > <span class='lk-ghost'>• &nbsp; </span>is <span class='lk-mark'>well-defined</span>",
                "in particular, it is linear",
            ),
            r"""
            > > • &nbsp; $Df(\vec{a})(\vec{x} - \vec{a})$ is a linear approximation to $f(\vec{x}) - f(\vec{a})$

            $$
            \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
            $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # section
    lk.section("Differentiability and continuity")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # theorem: differentiable implies continuous
    lk.theorem(
        r"""
        If $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a}$

        > then $\displaystyle\lim_{\vec{x} \to \vec{a}} \big( f(\vec{x}) - f(\vec{a}) \big) = 0$

        $\leadsto$ &nbsp; $f$ is continuous at $\vec{x} = \vec{a}$!
        """,
        label="thm-continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # proof: differentiable implies continuous
    lk.proof(
        [
            r"""
            $f(\vec{x}) - f(\vec{a}) = \dfrac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \, \lVert \vec{x} - \vec{a} \rVert$

            $\phantom{f(\vec{x}) - f(\vec{a}) =} \quad {} + Df(\vec{a})(\vec{x} - \vec{a})$
            """,
            lk.gap(),
            r"""
            $$
            \begin{aligned}
            \Longrightarrow \quad \lim_{\vec{x} \to \vec{a}} \big( f(\vec{x}) - f(\vec{a}) \big) &= \underbrace{\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \, \lVert \vec{x} - \vec{a} \rVert}_{= \, 0 \, \cdot \, 0}\\[22pt]
            &\qquad + \underbrace{\lim_{\vec{x} \to \vec{a}} Df(\vec{a})(\vec{x} - \vec{a})}_{\begin{array}{c} \scriptstyle = \, 0 \\ \scriptstyle \text{(linear maps are continuous)} \end{array}}\\[30pt]
            \end{aligned}
            $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # example: not continuous, so not differentiable
    lk.example(
        [
            r"$f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{cases} \dfrac{(x^1)^2}{\lVert \vec{x} \rVert^2}, & \vec{x} \neq \vec{0}\\[8pt] b, & \vec{x} = \vec{0} \end{cases}$",
            lk.aside(
                r"> is not differentiable at $\vec{x} = \vec{0}$",
                r"no matter the value of $b \in \mathbb{R}$",
            ),
            r"""
            > > $\displaystyle\lim_{t \to 0} f\left( \begin{bmatrix} t \\ 0 \end{bmatrix} \right) = 1$, &nbsp; $\displaystyle\lim_{t \to 0} f\left( \begin{bmatrix} 0 \\ t \end{bmatrix} \right) = 0$

            > > > $\Longrightarrow$ &nbsp; $f$ cannot be continuous!

            > > > $\Longrightarrow$ &nbsp; $f$ cannot be differentiable!
            """,
        ],
        label="ex-not-continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: C1-smooth
    # section
    lk.section(r"$C^1$-smooth functions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: C1-smooth
    # theorem: continuous partial derivatives imply differentiable
    lk.theorem(
        r"""
        If $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ has partial derivatives on an open ball around $\vec{x} = \vec{a}$ and they are continuous at $\vec{x} = \vec{a}$, then $f$ is differentiable at $\vec{x} = \vec{a}$!

        $\leadsto$ &nbsp; gives an easier criterion for differentiability (sufficient, but not necessary!)

        > 1\. &nbsp; compute partial derivatives for all points nearby $\vec{x} = \vec{a}$

        > 2\. &nbsp; check for continuity at $\vec{x} = \vec{a}$
        """,
        label="thm-c1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: C1-smooth
    # definition: C1-smooth
    lk.definition(
        r"""
        $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ with continuous partials at $\vec{x} = \vec{a}$ is called **$C^1$-smooth** at $\vec{x} = \vec{a}$

        $\leadsto$ &nbsp; the previous two theorems give

        > $C^1$-smooth &nbsp; $\Longrightarrow$ &nbsp; differentiable &nbsp; $\Longrightarrow$ &nbsp; continuous
        """,
        label="def-c1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: C1-smooth
    # example: elementary functions are C1-smooth
    lk.example(
        r"Any function $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ given by linear combination of products, quotients and compositions of "
        + lk.gloss("elementary functions", "powers, roots, exponentials,<br>logarithms, trigonometric functions")
        + r" of $x^i$s is $C^1$-smooth where the formula and its derivatives are well-defined!",
        label="ex-elementary",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: C1-smooth
    # example: where a quotient of elementary functions is C1-smooth
    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \dfrac{e^{x^1} + \sqrt{x^2}}{\sin(x^1)}$

            > is $C^1$-smooth for $x^1 \neq n\pi$ and $x^2 > 0$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \frac{\partial f}{\partial x^1} &= \frac{e^{x^1} \sin(x^1) - (e^{x^1} + \sqrt{x^2}) \cos(x^1)}{(\sin(x^1))^2}\\[6pt]
                \frac{\partial f}{\partial x^2} &= \frac{1}{2} \, \frac{1}{\sqrt{x^2} \, \sin(x^1)}
                \end{aligned}
                $$
                """,
                r"both continuous for<br>$x^1 \neq n\pi$, $x^2 > 0$",
            ),
            r"""
            $\leadsto$ &nbsp; in our course, we will mostly be dealing with this type of functions

            $\leadsto$ &nbsp; so checking if and where a function is differentiable will generally be a problem of finding their domains and the domains of their partials
            """,
        ],
        label="ex-quotient",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative and gradient
    # section
    lk.section("The derivative and the gradient")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative and gradient
    # definition: derivative, differential, Jacobian matrix
    lk.definition(
        [
            r"Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$",
            lk.aside(
                r"""
                $$
                Df(\vec{a}) = \mk{\begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix}} : \mathbb{R}^n \longrightarrow \mathbb{R}
                $$
                """,
                r"$\mathrm{Mat}(1 \times n)$",
            ),
            r"""
            is called <span class="lk-tab" style="--lk-tab: 10.5em">the **derivative**</span>of $f$ at $\vec{x} = \vec{a}$

            <span class='lk-ghost'>is called </span><span class="lk-tab" style="--lk-tab: 10.5em">the **differential**</span>of $f$ at $\vec{x} = \vec{a}$

            <span class='lk-ghost'>is called </span><span class="lk-tab" style="--lk-tab: 10.5em">the **Jacobian matrix**</span>of $f$ at $\vec{x} = \vec{a}$
            """,
        ],
        label="def-derivative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative and gradient
    # definition: gradient
    lk.definition(
        [
            r"We define the **gradient** of $f$ at $\vec{x} = \vec{a}$ as the vector",
            lk.aside(
                r"""
                $$
                \vec{\nabla} f(\vec{a}) = \mk{\begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\[4pt] {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \\ \vdots \\ {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix}} \in \mathbb{R}^n
                $$
                """,
                r"$\mathrm{Mat}(n \times 1) \neq \mathrm{Mat}(1 \times n)$",
            ),
            r"$\leadsto$ &nbsp; the derivative is the map that calculates directional derivatives $Df(\vec{a}) : \vec{v} \longmapsto Df(\vec{a})(\vec{v})$",
            lk.aside(
                r"$\leadsto$ &nbsp; the gradient is <span class='lk-mark'>a vector</span>!",
                "carrying equivalent information<br>but in a very different way!",
            ),
        ],
        label="def-gradient",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative and gradient
    # example: derivative versus gradient of the squared norm
    lk.example(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \lVert \vec{x} \rVert^2 = (x^1)^2 + (x^2)^2$, $\vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$

        > $\Longrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} 2 & 2 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $\begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto \underbrace{\begin{bmatrix} 2 & 2 \end{bmatrix} \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}}_{= \, 2v^1 + 2v^2}\rule[-1.6em]{0pt}{0pt}$

        > vs

        > $\vec{\nabla} f(\vec{a}) = \begin{bmatrix} 2 \\ 2 \end{bmatrix} = 2\vec{a} \in \mathbb{R}^2$
        """,
        label="ex-derivative-gradient",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative and gradient
    # remark: derivative and gradient through the dot product
    lk.remark(
        r"""
        $Df(\vec{a})$ and $\vec{\nabla} f(\vec{a})$ are related via the dot product

        $$
        \begin{aligned}
        Df(\vec{a})(\vec{v}) &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a}) + \dots + v^n \frac{\partial f}{\partial x^n}(\vec{a})\\[4pt]
        &= \big( \vec{\nabla} f(\vec{a}) \big) \cdot \vec{v}\\[4pt]
        &= \lVert \vec{\nabla} f(\vec{a}) \rVert \, \lVert \vec{v} \rVert \cos\big( \theta(\vec{\nabla} f(\vec{a}), \vec{v}) \big)
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: steepest ascent
    # section
    lk.section("Steepest ascent")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: steepest ascent
    # theorem: the gradient points in the direction of steepest ascent
    lk.theorem(
        lk.aside(
            r"$\vec{\nabla} f(\vec{a})$ points in the direction at $\vec{a}$ where <span class='lk-mark'>$f(\vec{x})$ grows fastest</span>",
            "direction of steepest ascent",
        ),
        label="thm-steepest",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: steepest ascent
    # proof: the gradient points in the direction of steepest ascent
    lk.proof(
        r"""
        If we keep $\lVert \vec{v} \rVert = 1$, $Df(\vec{a})(\vec{v})$ is largest when $\theta(\vec{\nabla} f(\vec{a}), \vec{v}) = 0$

        > $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a})$ points in the direction of largest growth of $f$ at $\vec{x} = \vec{a}$!

        > $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a})$ is the direction of steepest ascent of $f$ at $\vec{x} = \vec{a}$!
        """
    )
    return


@app.cell(hide_code=True)
def _(blank, cross_axes, ga1, ga2, lk, math, np, vector):
    # module: steepest ascent
    # example: f = (x^1)^2 + (x^2)^2, its gradient 2a, steepest descent and the directions with no ascent / descent
    # figure 1: the level sets f^{-1}(r^2), f^{-1}(R^2), a and the gradient 2a
    _R, _r, _phi = 1.3, 0.45, math.radians(40)
    _fig1, _ax = blank(3.6, 2.6, (-1.75, 3.9), (-1.6, 2.5))
    cross_axes(_ax, (-1.7, 3.5), (-1.55, 2.45), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(_R * np.cos(_th), _R * np.sin(_th), color=lk.BLUE, lw=1.4)
    _ax.plot(_r * np.cos(_th), _r * np.sin(_th), color=lk.RED, lw=1.4)
    _a = (_R * math.cos(_phi), _R * math.sin(_phi))
    lk.arrow(_ax, _a, (2.6 * _a[0], 2.6 * _a[1]), lk.GREEN)
    lk.arrow(_ax, (0, 0), _a, "black")
    _ax.plot(*_a, "o", color="black", ms=3.5, zorder=4)
    _ax.text(0.55, 0.62, r"$\vec{a}$", fontsize=13, ha="right", va="bottom")
    _ax.text(2.0, 1.25, r"$\vec{\nabla} f(\vec{a}) = 2\vec{a}$", color=lk.GREEN, fontsize=13, ha="left", va="top")
    _ax.text(0.95, -0.95, r"$f^{-1}(R^2)$", color=lk.BLUE, fontsize=12, ha="left", va="top")
    _ax.text(0.4, -0.3, r"$f^{-1}(r^2)$", color=lk.RED, fontsize=12, ha="left", va="top")

    # figure 2: a on the level set f^{-1}(R^2), the gradient and a vector v orthogonal to it
    _a = (round(ga1.value, 10) + 0.0, round(ga2.value, 10) + 0.0)
    _Ra = math.hypot(*_a)
    _grad = (2 * _a[0], 2 * _a[1])
    _v = (-_a[1] + 0.0, _a[0])  # one vector orthogonal to the gradient
    _ext = max(abs(_grad[0] + _a[0]), abs(_grad[1] + _a[1]), abs(_a[0] + _v[0]), abs(_a[1] + _v[1]))
    _lim = next(_l for _e, _l in ((0.375, 0.475), (0.75, 0.95), (1.5, 1.9), (3, 3.8), (math.inf, 5.6)) if _ext <= _e)  # the frame follows the drawing
    _fig2, _bx = blank(3.0, 3.0, (-_lim, _lim), (-_lim, _lim))
    for _rr in np.arange(1, 7) * min(1, _lim / 3.8):  # other level sets, as many across the frame at every zoom
        _bx.plot(_rr * np.cos(_th), _rr * np.sin(_th), color=lk.LIGHT, lw=0.8)
    cross_axes(_bx, (-_lim, _lim), (-_lim, _lim), "$x^1$", "$x^2$")
    if _Ra > 0:
        _bx.plot(_Ra * np.cos(_th), _Ra * np.sin(_th), color=lk.BLUE, lw=1.4)
        _t, _u = (-_a[1] / _Ra, _a[0] / _Ra), (_a[0] / _Ra, _a[1] / _Ra)
        _q = min(0.055 * _lim, 0.3 * _Ra)  # right-angle mark between v and the gradient
        _bx.plot([_a[0] + _q * _t[0], _a[0] + _q * (_t[0] + _u[0]), _a[0] + _q * _u[0]], [_a[1] + _q * _t[1], _a[1] + _q * (_t[1] + _u[1]), _a[1] + _q * _u[1]], color=lk.GREY, lw=0.8)
        vector(_bx, _a, (_a[0] + _grad[0], _a[1] + _grad[1]), lk.GREEN)
        _gap = 27 * abs(_u[1]) + 9 * abs(_u[0]) + 3  # its name beside the arrow, near its tip, on its left (the side of v)
        _bx.annotate(r"$\vec{\nabla} f(\vec{a})$", (2.5 * _a[0], 2.5 * _a[1]), textcoords="offset points", xytext=(-_gap * _u[1], _gap * _u[0]), ha="center", va="center", color=lk.GREEN, fontsize=13, zorder=5)
        vector(_bx, _a, (_a[0] + _v[0], _a[1] + _v[1]), lk.RED, r"$\vec{v}$", -35, r=14)  # its name beyond the tip, turned away from the circle
        _crowded = _Ra < 0.13 * _lim  # a very short a: its name would pile up on the others
        vector(_bx, (0, 0), _a, "black", None if _crowded else r"$\vec{a}$", -45, r=16)
        _c, _s = -_u[0], -_u[1]  # the circle's name on the side opposite a, just outside it
        _gap = 23 * abs(_c) + 8 * abs(_s) + 4
        _bx.annotate("$f^{-1}(R^2)$", (_Ra * _c, _Ra * _s), textcoords="offset points", xytext=(_gap * _c, _gap * _s), ha="center", va="center", color=lk.BLUE, fontsize=12, zorder=5)
    else:
        vector(_bx, (0, 0), _a, "black", r"$\vec{a}$", 0)

    lk.example(
        [
            r"$f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$",
            lk.aside(
                r"> $\vec{\nabla} f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) = \mk{\begin{bmatrix} 2a^1 \\ 2a^2 \end{bmatrix}}$",
                r"$f(\vec{x})$ increases fastest<br>along the radial direction",
            ),
            r"""
            > > $f^{-1}(r^2)$: &nbsp; $(x^1)^2 + (x^2)^2 = r^2$, &nbsp; $f^{-1}(R^2)$: &nbsp; $(x^1)^2 + (x^2)^2 = R^2$
            """,
            lk.figure(_fig1),
            lk.gap(),
            lk.aside(
                r"direction of <span class='lk-mark'>steepest descent</span> of $f$ at $\vec{a}$",
                "fastest decrease",
            ),
            r"""
            > $\leadsto$ &nbsp; $-\vec{\nabla} f(\vec{a}) = \begin{bmatrix} -2a^1 \\ -2a^2 \end{bmatrix}$
            """,
            lk.gap(),
            r"""
            directions with no ascent / descent

            > $\leadsto$ &nbsp; $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$ such that $\vec{\nabla} f(\vec{a}) \cdot \vec{v} = 0$ &nbsp; $\Longleftrightarrow$ &nbsp; $Df(\vec{a})(\vec{v}) = 0$

            > > $\vec{\nabla} f(\vec{a}) \cdot \vec{v} = 2a^1 v^1 + 2a^2 v^2 = 0$
            """,
            lk.aside(
                r"> > > $\Longleftrightarrow$ &nbsp; $v^2 = \mk{-{\large\tfrac{a^1}{a^2}} \, v^1}$",
                r"assuming $a^2 \neq 0$",
            ),
            lk.aside(
                r"> > $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \in \mk{\big( \vec{\nabla} f(\vec{a}) \big)^{\perp}}$, &nbsp; $f^{-1}(R^2) = \left\{ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \;\middle|\; (x^1)^2 + (x^2)^2 = R^2 \right\}$",
                r"orthogonal complement of $\vec{\nabla} f(\vec{a})$",
            ),
            lk.interactive(_fig2, controls=[ga1, ga2]),
        ],
        label="ex-steepest",
    )
    return


@app.cell(hide_code=True)
def _(blank, lk, np):
    # module: level sets
    # theorem: the gradient is perpendicular to the level set
    _fig, _ax = blank(3.6, 2.0, (-2.3, 2.9), (-1.05, 1.85))
    _x = np.linspace(-2.1, 2.1, 100)
    _ax.plot(_x, -0.12 * _x**2 - 0.15 * _x, color=lk.BLUE, lw=1.4)
    _n = np.array([0.15, 1.0]) / np.hypot(0.15, 1.0)
    _tv = np.array([1.0, -0.15]) / np.hypot(0.15, 1.0)
    _sq = np.array([0.2 * _tv, 0.2 * _tv + 0.2 * _n, 0.2 * _n])
    _ax.plot(_sq[:, 0], _sq[:, 1], color=lk.GREY, lw=0.8)
    lk.arrow(_ax, (0, 0), tuple(1.4 * _n), lk.GREEN)
    _ax.plot(0, 0, "o", color="black", ms=4, zorder=4)
    _ax.text(0.38, 1.4, r"$\vec{\nabla} f(\vec{a})$", color=lk.GREEN, fontsize=13, ha="left", va="center")
    _ax.text(2.0, -0.55, r"$f^{-1}(b)$", color=lk.BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(-0.08, -0.1, r"$\vec{a}$", fontsize=13, ha="right", va="top")

    lk.theorem(
        [
            r"""
            Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$ with $f(\vec{a}) = b$ and $\vec{\nabla} f(\vec{a}) \neq \vec{0}$, then

            > $\vec{\nabla} f(\vec{a})$ is perpendicular to $f^{-1}(b)$

            > $\vec{\nabla} f(\vec{a}) \perp f^{-1}(b)$
            """,
            lk.figure(_fig),
        ],
        label="thm-level-set",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine approximation
    # section
    lk.section("Affine approximations")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine approximation
    # definition: affine approximation
    lk.definition(
        r"""
        Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$

        > we call $g : \mathbb{R}^n \longrightarrow \mathbb{R}$ given by

        $$
        \begin{aligned}
        g(\vec{x}) &= f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})\\[4pt]
        &= f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})(x^1 - a^1) + \frac{\partial f}{\partial x^2}(\vec{a})(x^2 - a^2) + \dots + \frac{\partial f}{\partial x^n}(\vec{a})(x^n - a^n)
        \end{aligned}
        $$

        > the **affine approximation** of $f$ at $\vec{a}$
        """,
        label="def-affine",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine approximation
    # remark: n = 1, the tangent line
    lk.remark(
        r"""
        For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ differentiable at $x = a$

        > $g(x) = f(a) + f'(a)(x - a)$

        > > $\leadsto$ &nbsp; $\mathrm{graph}(g) =$ tangent line to $\mathrm{graph}(f)$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$

        > > <span class='lk-ghost'>$\leadsto$ &nbsp; $\mathrm{graph}(g)$ </span>$= \left\{ \begin{bmatrix} x \\ y \end{bmatrix} \;\middle|\; y = f(a) + f'(a)(x - a), \ x \in \mathbb{R} \right\}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine approximation
    # theorem: the graph of the affine approximation is the tangent plane
    lk.theorem(
        [
            r"""
            If $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$, then

            > $\mathrm{graph}(g) =$ plane in $\mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R}$ through $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$ with normal $\vec{n} = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\[4pt] {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \\[4pt] -1 \end{bmatrix}$
            """,
            lk.aside(
                r"> <span class='lk-ghost'>$\mathrm{graph}(g)$ </span>$= \left\{ \begin{bmatrix} x^1 \\ x^2 \\ y \end{bmatrix} \;\middle|\; \underbrace{y = f(\vec{a}) + {\large\tfrac{\partial f}{\partial x^1}}(\vec{a})(x^1 - a^1) + {\large\tfrac{\partial f}{\partial x^2}}(\vec{a})(x^2 - a^2)}_{\scriptstyle {\large\tfrac{\partial f}{\partial x^1}}(\vec{a})(x^1 - a^1) + {\large\tfrac{\partial f}{\partial x^2}}(\vec{a})(x^2 - a^2) - (y - f(\vec{a})) \, = \, 0}, \ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \right\}\rule[-2em]{0pt}{0pt}$",
                r"the tangent plane to $\mathrm{graph}(f)$<br>at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$",
            ),
        ],
        label="thm-tangent-plane",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # section
    lk.section("Practice")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: f = ln(x^1 x^2)
    lk.exercise(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \ln(x^1 x^2)$

        a) Compute $\dfrac{\partial f}{\partial x^1}$, $\dfrac{\partial f}{\partial x^2}$

        b) Where is $f$ $C^1$-smooth?

        c) For $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$, write the derivative of $f$ at $\vec{a}$

        <span class='lk-ghost'>c) For $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$, </span>write the gradient of $f$ at $\vec{a}$

        d) Find all $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$ for which $Df(\vec{a})(\vec{v}) = 0$

        e) Sketch $f^{-1}(\ln(2))$ and draw $\vec{\nabla} f(\vec{a})$ at $\vec{a}$
        """,
        label="ex-practice",
    )
    return


if __name__ == "__main__":
    app.run()
