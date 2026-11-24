import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 7 · Local properties of paths", css_file="lecturekit/style.css")


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
    lk.lecture(7, "Local properties of paths")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: bare sketches, coordinate axes, the unit circle with an angle

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def angle_mark(ax, angle, name, color):
        """The angle `angle` (radians, from the first axis) as an arc about the origin, which spirals outwards after a
        full turn; its `name` sits in the widest quadrant the last turn sweeps, so that it never lies on an axis."""
        th = np.linspace(0, angle, max(2, int(40 * angle)))
        r = 0.3 + 0.2 * np.maximum(th - 2 * np.pi, 0) / (2 * np.pi)
        ax.plot(r * np.cos(th), r * np.sin(th), color=color, lw=1.0)
        if angle < 0.5:
            return
        lo = max(0.0, angle - 2 * np.pi)
        a, b = max(((max(lo, k * np.pi / 2), min(angle, (k + 1) * np.pi / 2)) for k in range(8)), key=lambda p: p[1] - p[0])
        m = (a + b) / 2
        d = 0.5 + 0.2 * max(m - 2 * np.pi, 0) / (2 * np.pi)
        ax.text(d * np.cos(m), d * np.sin(m), name, color=color, fontsize=12, ha="center", va="center")

    def circle_axes(ax, lim):
        """The y^1 and y^2 axes and the unit circle."""
        lk.arrow(ax, (-lim, 0), (lim + 0.05, 0), "black", lw=0.9)
        lk.arrow(ax, (0, -lim), (0, lim + 0.05), "black", lw=0.9)
        ax.text(lim + 0.1, -0.08, "$y^1$", fontsize=13, ha="center", va="top")
        ax.text(-0.1, lim + 0.05, "$y^2$", fontsize=13, ha="right", va="center")
        th = np.linspace(0, 2 * math.pi, 361)
        ax.plot(np.cos(th), np.sin(th), color=lk.BLUE, lw=1.5)

    return angle_mark, blank, circle_axes


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    t_circle = lk.slider(0, 12.5, step=0.1, value=0.7, label="$t$")
    a_circle = lk.slider(0, 6.25, step=0.05, value=0.5, label="$a$")
    a_parabola = lk.slider(-1.4, 1.4, step=0.1, value=0.7, label="$a$")
    return a_circle, a_parabola, t_circle


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: multivariable functions and their global properties
    lk.recap(
        r"> $\leadsto$ &nbsp; global properties (image, graph, level sets)",
        topic=r"Multivariable functions $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"Local properties of paths $\gamma : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}^m$", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: paths
    # section
    lk.section("Paths")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: paths
    # definition: path
    lk.definition(
        r"""
        A **path** in $\mathbb{R}^m$ is a function

        $$
        \begin{aligned}
        \gamma : A \subseteq \mathbb{R} &\longrightarrow \mathbb{R}^m \\
        t &\longmapsto \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix}
        \end{aligned}
        $$
        """,
        label="def-path",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: paths
    # remark: the components are single variable functions
    lk.remark(
        r"""
        Each component $\gamma^i : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}$ is a usual single variable real valued function!

        > $\Longrightarrow$ &nbsp; paths are ordered lists of single variable scalar functions, like vectors were ordered lists of scalars!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: paths
    # example: affine parameterization of a line
    lk.example(
        [
            r"""
            $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ an affine parameterization of a line

            $$
            \gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
            $$
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $\mk{\gamma^1(t) = x^1 + t v^1, \ \ \gamma^2(t) = x^2 + t v^2}$",
                "pair of affine single variable functions",
            ),
        ],
        label="ex-line",
    )
    return


@app.cell(hide_code=True)
def _(lk, math, np, t_circle):
    # module: paths
    # the scene of the helix, graph(gamma) = {(t, cos t, sin t)}, with its point (t, gamma(t)) moving with the slider t: t
    # to the right at a quarter of its length, so that two turns fit, y^1 towards the viewer
    _t = t_circle.value
    _p = (math.cos(_t), math.sin(_t))
    _c = 0.25
    _s = np.linspace(-0.8, 13.0, 900)
    _ticks = [(_k * math.pi, _name) for _k, _name in ((1, r"\pi"), (2, r"2\pi"), (3, r"3\pi"), (4, r"4\pi"))]
    lk.turntable(
        30,
        18,
        "graph of gamma, a helix in R x R^2 with the t-axis to the right, and its point (t, gamma(t))",
        [
            lk.panel(
                1.0,
                lines=[(np.cos(_s), _c * _s, np.sin(_s), lk.BLUE, 2.0)],
                points=[((_p[0], _c * _t, _p[1]), "#000000")] + [((0, _c * _k, 0), "#000000", 2.2) for _k, _ in _ticks],
                axes=[((0, -0.5, 0), (0, _c * 13.8, 0), "t", 0), ((-1.2, 0, 0), (1.5, 0, 0), "y^1", -120), ((0, 0, -1.2), (0, 0, 1.4), "y^2", 90)],
                texts=[((0, _c * _k, 0), _name, "#000000", -90) for _k, _name in _ticks]
                + [((0, _c * 2.5 * math.pi, 1), r"\mathrm{graph}(\gamma)", lk.BLUE, 90, 6),
                   ((_p[0], _c * _t, _p[1]), r"\begin{bmatrix} t \\ \gamma(t) \end{bmatrix}", "#000000", math.degrees(math.atan2(46 * _p[1] - 14 * _p[0], -26 * _p[0])), 7)],
                box=((-1.6, 1.6), (-0.5, 3.5), (-1.3, 1.5)),
            )
        ],
        height=lk.H3D,
        width=460,
        key="L07-helix",
        apart=True,
        zoom=1.3,
    )
    return


@app.cell(hide_code=True)
def _(angle_mark, blank, circle_axes, lk, math, mo, t_circle):
    # module: paths
    # example: gamma(t) = (cos t, sin t), its image and its graph, with the unit circle beside the helix, both moving
    # with the slider t
    _t = t_circle.value
    _p = (math.cos(_t), math.sin(_t))
    _fig, _ax = blank(3.4, 3.1, (-1.6, 2.1), (-1.75, 1.75))
    circle_axes(_ax, 1.5)
    angle_mark(_ax, _t, "$t$", lk.GREEN)
    lk.arrow(_ax, (0, 0), _p, "black")
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    _ax.text(1.12 * _p[0] if abs(_p[0]) >= 0.35 else 0.1, 1.12 * _p[1] if abs(_p[1]) >= 0.35 else 0.1, r"$\genfrac{[}{]}{0}{0}{\cos(t)}{\sin(t)}$", fontsize=12,
             ha="left" if _p[0] > -0.35 else "right", va="bottom" if _p[1] > -0.35 else "top")
    # the equation of the circle beside it, lower left (lower right when the point is there)
    _d = -1 if not (_p[0] < -0.2 and _p[1] < -0.2) else 1
    _ax.text(0.74 * _d, -0.74, r"$(y^1)^2 + (y^2)^2 = 1$", color=lk.BLUE, fontsize=12, ha="right" if _d < 0 else "left", va="top")

    lk.example(
        [
            r"""
            $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$, &nbsp; $t \longmapsto \gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}$

            > $\leadsto$ &nbsp; $\gamma^1 : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $t \longmapsto \cos(t)$ &nbsp; is the cosine function

            > $\leadsto$ &nbsp; $\gamma^2 : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $t \longmapsto \sin(t)$ &nbsp; is the sine function

            $$
            \begin{aligned}
            \mathrm{Im}(\gamma) &= \left\{ \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; \exists \, t \in \mathbb{R}, \ y^1 = \gamma^1(t), \ y^2 = \gamma^2(t) \right\} \\
            &= \left\{ \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; t \in \mathbb{R} \right\}
            \end{aligned}
            $$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \mathrm{graph}(\gamma) &= \left\{ \begin{bmatrix} t \\ y^1 \\ y^2 \end{bmatrix} \in \mathbb{R} \times \mathbb{R}^2 = \mathbb{R}^3 \;\middle|\; t \in \mathbb{R}, \ y^1 = \gamma^1(t), \ y^2 = \gamma^2(t) \right\} \\
                &= \left\{ \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix} \in \mathbb{R}^3 \;\middle|\; t \in \mathbb{R} \right\}
                \end{aligned}
                $$
                """,
                "helix",
                at="last",
            ),
            lk.interactive(mo.hstack([_fig, lk.frame("L07-helix", lk.H3D, width=460)], justify="center", align="center", gap=1), controls=[t_circle]),
        ],
        label="ex-circle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: operations
    # remark: vector operations extended to paths
    _ub = lambda a, b: r"\underbrace{" + a + r"}_{\begin{array}{c} \scriptstyle \text{" + b.replace("|", r"} \\ \scriptstyle \text{") + r"} \end{array}}"
    lk.remark(
        [
            r"We can extend vector operations to paths",
            r"> Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^m$, and $\lambda : \mathbb{R} \longrightarrow \mathbb{R}$",
            "> • &nbsp; $" + _ub(r"(\gamma + \sigma)(t)", "addition|of paths") + r" \quad = \quad " + _ub(r"\gamma(t) + \sigma(t)", "addition|of vectors")
            + r"$ &nbsp; $\leadsto$ &nbsp; $\gamma + \sigma : \mathbb{R} \longrightarrow \mathbb{R}^m$ $\rule[-2.2em]{0pt}{0pt}$",
            "> • &nbsp; $" + _ub(r"(\lambda \gamma)(t)", "multiplication of|scalar function|and a path") + r" \quad = \quad "
            + _ub(r"\lambda(t) \, \gamma(t)", "multiplication|of scalar|and vector")
            + r"$ &nbsp; $\leadsto$ &nbsp; $\lambda \gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ $\rule[-3em]{0pt}{0pt}$",
            "> • &nbsp; $" + _ub(r"(\gamma \cdot \sigma)(t)", "dot product|of paths") + r" \quad = \quad " + _ub(r"\gamma(t) \cdot \sigma(t)", "dot product|of vectors")
            + r"$ &nbsp; $\leadsto$ &nbsp; $\gamma \cdot \sigma : \mathbb{R} \longrightarrow \mathbb{R}$ $\rule[-2.2em]{0pt}{0pt}$",
            lk.aside(
                "> • &nbsp; $" + _ub(r"(\gamma \times \sigma)(t)", r"cross-product of|paths in }\mathbb{R}^3\text{") + r" \quad = \quad "
                + _ub(r"\gamma(t) \times \sigma(t)", r"cross-product of|vectors in }\mathbb{R}^3\text{")
                + r"$ &nbsp; $\leadsto$ &nbsp; $\gamma \times \sigma : \mathbb{R} \longrightarrow \mathbb{R}^3$ $\rule[-2.2em]{0pt}{0pt}$",
                "if&nbsp;$m = 3$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: operations
    # example: the operations for a circle, an affine path and cos
    lk.example(
        r"""
        $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$, &nbsp; $\sigma(t) = \begin{bmatrix} at + b \\ ct + d \end{bmatrix}$, &nbsp; $\lambda(t) = \cos(t)$

        > $\leadsto$ &nbsp; $(\gamma + \sigma)(t) = \begin{bmatrix} \cos(t) + at + b \\ \sin(t) + ct + d \end{bmatrix}$

        > $\leadsto$ &nbsp; $(\gamma \cdot \sigma)(t) = \cos(t)(at + b) + \sin(t)(ct + d)$

        > $\leadsto$ &nbsp; $\lVert \gamma \rVert^2(t) = (\gamma \cdot \gamma)(t) = \cos(t)^2 + \sin(t)^2 = 1$

        > $\leadsto$ &nbsp; $(\lambda \gamma)(t) = \begin{bmatrix} \cos(t)^2 \\ \cos(t) \sin(t) \end{bmatrix}$
        """,
        label="ex-operations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # section
    lk.section("Limits")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # motivation: the question behind limits
    lk.motivation(r"How does a path behave as we “approach” a certain input?")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # definition: limit of a path
    lk.definition(
        [
            r"Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $a \in \mathbb{R}$ and $\vec{b} \in \mathbb{R}^m$, we say",
            lk.aside(
                r"$$ \lim_{t \to a} \gamma(t) \mk{{} = \vec{b}} $$",
                r"the limit of $\gamma$ as $t$ approaches $a$<br>is equal to $\vec{b}$",
            ),
            r"if we can make",
            lk.aside(r"> $\gamma(t)$ <span class='lk-mark'>**arbitrarily**</span> close to $\vec{b}$", "as close as we want"),
            r"by taking",
            lk.aside(
                r"> $t$ <span class='lk-mark'>**sufficiently**</span> close to $a$ &nbsp; (but <span class='lk-mark'>different from $a$</span>)",
                r"sufficiently: as close as we need<br>different from $a$: we don't even need $\gamma$<br>to be defined at $t = a$ to talk about limits",
            ),
        ],
        label="def-limit",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # prose: the definition with epsilon and delta
    lk.prose(
        r"""
        Choose how close to $\vec{b}$ you would like

        > $\leadsto$ &nbsp; want $\lVert \gamma(t) - \vec{b} \rVert < \varepsilon$, for $\varepsilon > 0$.

        Can we achieve this, by taking $t$ close enough to $a$?

        > $\leadsto$ &nbsp; can we find $\delta > 0$ such that

        $$
        0 < \lvert t - a \rvert < \delta \quad \Longrightarrow \quad \lVert \gamma(t) - \vec{b} \rVert < \varepsilon \ ?
        $$

        Can we do this for every $\varepsilon > 0$?

        > If yes, then $\displaystyle\lim_{t \to a} \gamma(t) = \vec{b}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # theorem: limits componentwise
    lk.theorem(
        r"""
        Limit of paths can be calculated componentwise

        $$
        \lim_{t \to a} \gamma(t) = \vec{b} \quad \Longleftrightarrow \quad \lim_{t \to a} \gamma^i(t) = b^i \quad \forall \, i = 1, 2, \ldots, m
        $$
        """,
        label="thm-limit-components",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # example: the limit of (cos t, sin t) at pi/2
    lk.example(
        r"""
        $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$ &emsp;&emsp; $\displaystyle\lim_{t \to \pi/2} \gamma(t) = \begin{bmatrix} \displaystyle\lim_{t \to \pi/2} \cos(t) \\[8pt] \displaystyle\lim_{t \to \pi/2} \sin(t) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$
        """,
        label="ex-limit-circle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # remark: uniqueness
    lk.remark(r"Limits are unique, provided they exist!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # section
    lk.section("Continuity")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # definition: continuous path
    lk.definition(
        r"""
        A path $\gamma$ is **continuous** at $t = a$ if

        $$
        \lim_{t \to a} \gamma(t) = \gamma(a)
        $$

        > $\gamma$ is continuous in $(a_1, a_2) \subset \mathbb{R}$ if it is continuous at every $t \in (a_1, a_2)$
        """,
        label="def-continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuity
    # theorem: continuity componentwise
    lk.theorem(
        r"""
        A path is continuous iff all of its components are continuous

        $$
        \lim_{t \to a} \gamma(t) = \gamma(a) \quad \Longleftrightarrow \quad \lim_{t \to a} \gamma^i(t) = \gamma^i(a) \quad \forall \, i = 1, 2, \ldots, m
        $$
        """,
        label="thm-continuous-components",
    )
    return


@app.cell(hide_code=True)
def _(lk, math, np):
    # module: continuity
    # example: the circle with a jump at t = 0, with the helix cut at t = 0: its limit point (0, (1, 0)) is not
    # (0, gamma(0)) = (0, (0, 1))
    _c = 0.25
    _ticks = [(_k * math.pi, _name) for _k, _name in ((-1, r"-\pi"), (1, r"\pi"), (2, r"2\pi"))]
    _lines = [(np.cos(_s), _c * _s, np.sin(_s), lk.BLUE, 2.0) for _s in (np.linspace(-4.2, -0.1, 300), np.linspace(0.1, 8.6, 600))]
    _fig = lk.turntable(
        30,
        18,
        "graph of gamma, a helix in R x R^2 with a gap at t = 0, the limit point (0, (1, 0)) and the point (0, gamma(0)) = (0, (0, 1))",
        [
            lk.panel(
                1.0,
                lines=_lines,
                points=[((1, 0, 0), "#000000", 4.5, True), ((0, 0, 1), "#000000")] + [((0, _c * _k, 0), "#000000", 2.2) for _k, _ in _ticks],
                axes=[((0, _c * -4.8, 0), (0, _c * 9.2, 0), "t", 0), ((-1.2, 0, 0), (1.5, 0, 0), "y^1", -120), ((0, 0, -1.2), (0, 0, 1.4), "y^2", 90)],
                texts=[((0, _c * _k, 0), _name, "#000000", 90 if _k < 0 else -90) for _k, _name in _ticks]
                + [((0, _c * 2.5 * math.pi, 1), r"\mathrm{graph}(\gamma)", lk.BLUE, 90, 6),
                   ((1, 0, 0), r"\lim_{t \to 0} \begin{bmatrix} 0 \\ \gamma(t) \end{bmatrix}", "#000000", 162, 25),
                   ((0, 0, 1), r"\begin{bmatrix} 0 \\ \gamma(0) \end{bmatrix}", "#000000", 35, 8)],
            )
        ],
        height=lk.H3D,
        width=480,
        zoom=1.2,
    )
    lk.example(
        [
            r"$\gamma(t) = \begin{cases} \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, & t \neq 0 \\[12pt] \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0 \end{cases}$",
            lk.figure(_fig),
        ],
        label="ex-jump",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # section
    lk.section("Differentiability")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # definition: derivative of a path
    lk.definition(
        r"""
        A path $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is **differentiable** at $t = a$

        > if $\displaystyle\lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}$ exists.

        > > $\leadsto$ &nbsp; if it exists we call it the **derivative** of $\gamma$ at $t = a$ and denote it $\gamma'(a)$
        """,
        label="def-derivative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # prose: velocity and position
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; we also call $\gamma'(a)$ the **velocity** of the path $\gamma$ at $t = a$",
            r"$\gamma(a)$ is the position of $\gamma$ at $t = a$",
        )
    )
    return


@app.cell(hide_code=True)
def _(a_circle, angle_mark, blank, circle_axes, lk, math):
    # module: differentiability
    # example: the derivative of (cos t, sin t), with the circle, gamma(a) and gamma'(a) moving with the slider a
    _a = a_circle.value
    _p = (math.cos(_a), math.sin(_a))
    _v = (-math.sin(_a), math.cos(_a))
    _tip = (_p[0] + _v[0], _p[1] + _v[1])
    _fig, _ax = blank(3.4, 3.4, (-2.0, 2.25), (-2.1, 2.15))
    circle_axes(_ax, 1.9)
    angle_mark(_ax, _a, "$a$", lk.GREEN)
    lk.arrow(_ax, (0, 0), _p, "black")
    lk.arrow(_ax, _p, _tip, lk.GREEN)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    # gamma(a) just outside the circle, gamma'(a) beyond its tip, Im(gamma) where neither is
    _ax.text(1.15 * _p[0] if abs(_p[0]) >= 0.35 else 0.1, 1.15 * _p[1] if abs(_p[1]) >= 0.35 else 0.1, r"$\gamma(a)$", fontsize=13,
             ha="left" if _p[0] > -0.35 else "right", va="bottom" if _p[1] > -0.35 else "top")
    _cross = _v[0] < -0.35 and 0 < _tip[0] < 0.9  # beyond the tip the name would cross the y^2-axis: right of the tip instead
    _ax.annotate(r"$\gamma'(a)$", _tip, textcoords="offset points", xytext=(5 if _cross else 5 * _v[0], 5 * _v[1]), color=lk.GREEN, fontsize=13,
                 ha="left" if _v[0] > 0.35 or _cross else "right" if _v[0] < -0.35 else "center", va="bottom" if _v[1] > 0.35 else "top" if _v[1] < -0.35 else "center")
    _m = math.radians(next(_d for _d in (225, 315, 135, 45) if min(abs((math.degrees(_a) + _k - _d + 180) % 360 - 180) for _k in (0, 45)) >= 50))
    _ax.text(1.08 * math.cos(_m), 1.08 * math.sin(_m), r"$\mathrm{Im}(\gamma)$", color=lk.BLUE, fontsize=13, ha="left" if math.cos(_m) > 0 else "right", va="bottom" if math.sin(_m) > 0 else "top")

    lk.example(
        [
            r"""
            $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

            $$
            \begin{aligned}
            \gamma'(a) &= \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} = \lim_{t \to a} \begin{bmatrix} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix} \\[6pt]
            &= \begin{bmatrix} \displaystyle\lim_{t \to a} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \displaystyle\lim_{t \to a} \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix}
            = \begin{bmatrix} \dfrac{d}{dt} \cos(t) \Big|_{t = a} \\[10pt] \dfrac{d}{dt} \sin(t) \Big|_{t = a} \end{bmatrix} = \begin{bmatrix} -\sin(a) \\ \cos(a) \end{bmatrix}
            \end{aligned}
            $$
            """,
            lk.interactive(_fig, controls=[a_circle]),
        ],
        label="ex-velocity-circle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # theorem: derivatives componentwise
    lk.theorem(
        r"""
        Derivatives of paths can be computed componentwise

        $$
        \gamma'(a) = \vec{v} \quad \Longleftrightarrow \quad \frac{d}{dt} \gamma^i(t) \Big|_{t = a} = v^i \quad \forall \, i = 1, 2, \ldots, m
        $$
        """,
        label="thm-derivative-components",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent line
    # definition: tangent line
    lk.definition(
        r"""
        If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is differentiable at $t = a$ with velocity vector $\gamma'(a) \neq \vec{0}$, we call the line through $\vec{x} = \gamma(a)$ in the direction of $\vec{v} = \gamma'(a)$ the **tangent line** to $\gamma$ at $t = a$

        $$
        T_a\gamma = \big\{ \vec{y} = \gamma(a) + s \, \gamma'(a) \;\big|\; s \in \mathbb{R} \big\}
        $$
        """,
        label="def-tangent-line",
    )
    return


@app.cell(hide_code=True)
def _(a_parabola, blank, lk, np):
    # module: tangent line
    # example: the parabola (t^2, t) with gamma(a), gamma'(a) and the tangent line moving with the slider a
    _a = a_parabola.value
    _p, _v = (_a**2, _a), (2 * _a, 1.0)
    _tip = (_p[0] + _v[0], _p[1] + _v[1])
    _fig, _ax = blank(4.6, 3.7, (-2.2, 4.9), (-2.7, 3.0))  # the drawing cut at y^1 = -2 and y^1 = 4
    lk.arrow(_ax, (-2.0, 0), (4.6, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -2.6), (0, 2.8), "black", lw=0.9)
    _ax.text(4.65, -0.1, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.12, 2.8, "$y^2$", fontsize=13, ha="right", va="center")
    _t = np.linspace(-2, 2, 300)
    _ax.plot(_t**2, _t, color=lk.BLUE, lw=1.5)
    _cut = (4 - _a**2) / _v[0] if _a != 0 else None  # the s at which the line reaches y^1 = 4
    _s = np.array(sorted([(-2 - _a**2) / _v[0], _cut]) if _a != 0 else [-12.0, 12.0])  # and y^1 = -2
    _ax.plot(_p[0] + _s * _v[0], _p[1] + _s * _v[1], color=lk.RED, lw=1.0 if _a != 0 else 2.0, zorder=2 if _a != 0 else 3)  # at a = 0 on the y^2-axis: wider, over it
    lk.arrow(_ax, _p, _tip, lk.GREEN)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    _n = np.array((-1.0, 2 * _a)) / np.hypot(1.0, 2 * _a)  # normal to the line, away from the curve
    _va = "bottom" if _n[1] > 0.35 else "top" if _n[1] < -0.35 else "center"
    _end = _p + (min(_cut, 2.4 - _a) if _a > 0 else max(_cut, -2.3 - _a) if _a < 0 else -2.4) * np.array(_v)
    _ax.annotate(r"$T_a\gamma$", _end, textcoords="offset points", xytext=(6 * _n[0], 6 * _n[1]), color=lk.RED, fontsize=13, ha="right", va=_va, zorder=5)
    _ax.annotate(r"$\gamma'(a)$", _tip, textcoords="offset points", xytext=(6 * _n[0], 6 * _n[1]), color=lk.GREEN, fontsize=13, ha="right", va=_va, zorder=5)
    if abs(_a) >= 0.5:  # inside the curve, below (above) the point
        _ax.annotate(r"$\gamma(a)$", _p, textcoords="offset points", xytext=(6, -6 if _a > 0 else 6), fontsize=13, ha="left", va="top" if _a > 0 else "bottom", zorder=5)
    else:  # near the vertex: left of the y^2-axis
        _ax.annotate(r"$\gamma(a)$", (-0.1, _a), textcoords="offset points", xytext=(0, 3 if _a >= 0 else -3), fontsize=13, ha="right", va="bottom" if _a >= 0 else "top", zorder=5)
    _ax.text(4, -2 if _a >= 0 else 2, r"$\mathrm{Im}(\gamma)$", color=lk.BLUE, fontsize=13, ha="right", va="top" if _a >= 0 else "bottom")  # at the end of the branch the line does not reach

    lk.example(
        [
            r"""
            $\gamma(t) = \begin{bmatrix} t^2 \\ t \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; $\gamma'(t) = \begin{bmatrix} 2t \\ 1 \end{bmatrix}$

            $$
            T_a\gamma = \left\{ \vec{y} = \begin{bmatrix} a^2 \\ a \end{bmatrix} + s \begin{bmatrix} 2a \\ 1 \end{bmatrix} \;\middle|\; s \in \mathbb{R} \right\}
            $$
            """,
            lk.interactive(_fig, controls=[a_parabola]),
        ],
        label="ex-tangent-parabola",
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
    # exercise: limit and continuity of (t, sin(t)/t)
    lk.exercise(
        r"""
        Let $\gamma(t) = \begin{cases} \begin{bmatrix} t \\ \dfrac{\sin(t)}{t} \end{bmatrix}, & t \neq 0 \\[14pt] \begin{bmatrix} a \\ b \end{bmatrix}, & t = 0 \end{cases}$

        a) find $\displaystyle\lim_{t \to 0} \gamma(t)$

        b) find $a, b \in \mathbb{R}$ such that $\gamma$ is continuous at $t = 0$
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: the helix on a cylinder and its tangent line
    lk.exercise(
        r"""
        Consider $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^3$, &nbsp; $\sigma(t) = \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix}$

        and $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$, &nbsp; $f(\vec{x}) = (x^2)^2 + (x^3)^2$

        a) show that $\mathrm{Im}(\sigma) \subseteq f^{-1}(1)$

        b) compute $\sigma'(t)$, and find an affine parameterization of the tangent line to $\sigma$ at $t = 0$

        c) is the entire tangent line contained in $f^{-1}(1)$? &nbsp; Justify your answers!
        """,
        label="ex-practice-2",
    )
    return


if __name__ == "__main__":
    app.run()
