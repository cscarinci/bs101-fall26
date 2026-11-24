import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 6 · Multivariable functions", css_file="lecturekit/style.css")


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
    lk.lecture(6, "Multivariable functions")
    return


@app.cell(hide_code=True)
def _(Figure, lk, np):
    # Helpers of this lecture: bare sketches, the quadrics (x^1)^2 + (x^2)^2 - (x^3)^2 = b

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def quadric(b, zmax, colour, alpha=0.35):
        """The level set (x^1)^2 + (x^2)^2 - (x^3)^2 = b for |x^3| <= zmax: one sheet for b > 0, the cone for b = 0,
        two sheets for b < 0; smooth and see-through in light tones of `colour`, with only the lines that carry meaning
        drawn: the rims at |x^3| = zmax and, for one sheet, the waist (the vertex for the cone)."""
        phi = np.linspace(0, 2 * np.pi, 73)
        if b >= 0:
            z = np.linspace(-zmax, zmax, 25)
            parts = [(np.sqrt(b + z**2), z)]
            wire = [(0, 12, colour, 1.0)]
        else:
            r = np.linspace(0, np.sqrt(zmax**2 + b), 13)
            parts = [(r, s * np.sqrt(r**2 - b)) for s in (1, -1)]
            wire = [(0, 12, colour, 1.0)]
        return [lk.sheet(r[:, None] * np.cos(phi), r[:, None] * np.sin(phi), z[:, None] + 0 * phi, wire=wire, tone=colour, alpha=alpha) for r, z in parts]

    return blank, quadric


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    t_path = lk.slider(-1, 3, step=0.25, value=1.5, label="$t$")
    b_level = lk.slider(-4, 4, step=0.5, value=1, label="$b$")
    return b_level, t_path


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: Euclidean geometry
    lk.recap(
        r"> $\leadsto$ &nbsp; vectors, lines, planes",
        lk.aside(
            r"> $\leadsto$ &nbsp; <span class='lk-mark'>dot products</span> and cross-products (in $\mathbb{R}^3$)",
            "lengths, angles, areas, volumes",
        ),
        topic="Euclidean Geometry",
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Multivariable functions", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.1")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions
    # section
    lk.section("Multivariable functions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions
    # definition: multivariable function
    lk.definition(
        r"""
        A **multivariable function** is a rule

        $$
        f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m
        $$

        that assigns to each element $\vec{x}$ in a set $A \subseteq \mathbb{R}^n$ a unique element $\vec{y} = f(\vec{x})$ in another set $B \subseteq \mathbb{R}^m$
        """,
        label="def-function",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions
    # prose: the three parts of a function
    lk.prose(
        r"""
        $\leadsto$ &nbsp; there are 3 parts to a function

        $$
        \begin{aligned}
        \mathrm{Dom}(f) &= A = \text{set of allowed inputs}\\
        \mathrm{Codom}(f) &= B = \text{set of desired outputs}\\
        \vec{x} &\longmapsto f(\vec{x}) \quad \text{the rule of assignment}
        \end{aligned}
        $$

        $\leadsto$ &nbsp; change any one of these and you have a different function!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions
    # remark: names of special functions
    lk.remark(
        [
            "Sometimes we will call",
            lk.aside(
                r"> • &nbsp; $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mk{\mathbb{R}}$ &nbsp; a **scalar function** on $\mathbb{R}^n$ (or scalar-valued function)",
                "$m = 1$",
            ),
            lk.aside(r"> • &nbsp; $f : A \subseteq \mk{\mathbb{R}} \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; a **path** in $\mathbb{R}^m$", "$n = 1$"),
            lk.aside(
                r"> • &nbsp; $f : A \subseteq \mk{\mathbb{R}^2} \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; a **parameterized surface** in $\mathbb{R}^m$",
                "$n = 2$",
            ),
            r"> • &nbsp; $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; a **map** from $A \subseteq \mathbb{R}^n$ to $B \subseteq \mathbb{R}^m$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions
    # example: lengths, affine parameterizations, linear transformations, with what is variable and what is fixed
    _ub = lambda a, b: r"\underbrace{" + a + r"}_{\begin{array}{c} \scriptstyle " + b.replace("|", r" \\ \scriptstyle ") + r" \end{array}}"
    lk.example(
        r"""
        lengths

        $$
        \begin{aligned}
        \lVert \cdot \rVert : \mathbb{R}^n &\longrightarrow \mathbb{R}\\
        \vec{x} &\longmapsto \sqrt{(x^1)^2 + (x^2)^2 + \dots + (x^n)^2}
        \end{aligned}
        $$

        affine parameterizations

        $$
        \begin{aligned}
        \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^3\\
        """
        + _ub("t", r"\text{variable}")
        + r" &\longmapsto "
        + _ub(r"\begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \\ x^3 + t v^3 \end{bmatrix}", r"\vec{x} \text{ and } \vec{v}|\text{fixed here!}")
        + r"""
        \end{aligned}
        \qquad\qquad
        \begin{aligned}
        \varphi : \mathbb{R}^2 &\longrightarrow \mathbb{R}^3\\
        """
        + _ub("(s, t)", r"\text{variables}")
        + r" &\longmapsto "
        + _ub(r"\begin{bmatrix} x^1 + s u^1 + t v^1 \\ x^2 + s u^2 + t v^2 \\ x^3 + s u^3 + t v^3 \end{bmatrix}", r"\vec{x}, \vec{u} \text{ and } \vec{v}|\text{fixed here!}")
        + r"""
        \end{aligned}
        $$

        linear transformations

        $$
        \begin{aligned}
        T : \mathbb{R}^n &\longrightarrow \mathbb{R}^m\\
        """
        + _ub(r"\begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix}", r"\text{variables}")
        + r" &\longmapsto "
        + _ub(r"\begin{bmatrix} t^1{}_1 x^1 + \dots + t^1{}_n x^n \\ \vdots \\ t^m{}_1 x^1 + \dots + t^m{}_n x^n \end{bmatrix}", r"t^i{}_j \text{ are fixed}")
        + r"""
        \end{aligned}
        $$
        """,
        label="ex-functions",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: image and graph
    # section
    lk.section("Basic properties")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: image and graph
    # definition: image and graph
    lk.definition(
        [
            r"Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$",
            r"> • &nbsp; **image** of $f$ is",
            lk.aside(
                r"$$ \mathrm{Im}(f) = \big\{ \vec{y} \in \mathbb{R}^m \;\big|\; \exists \, \vec{x} \in A, \ f(\vec{x}) = \vec{y} \big\} \mk{{} \subseteq B} $$",
                r"not necessarily equal!<br>$\mathrm{Im}(f) \subseteq \mathrm{Codom}(f)$",
            ),
            r"""
            > • &nbsp; **graph** of $f$ is

            $$
            \mathrm{graph}(f) = \big\{ (\vec{x}, \vec{y}) \in \mathbb{R}^n \times \mathbb{R}^m \;\big|\; \vec{x} \in A, \ \vec{y} = f(\vec{x}) \big\} \subseteq A \times B
            $$
            """,
        ],
        label="def-image-graph",
    )
    return


@app.cell(hide_code=True)
def _(lk, np, t_path):
    # module: image and graph
    # the scene of graph(gamma), a line in R x R^2, with its points (0, x) and (t, gamma(t)) moving with the slider t and,
    # over t, a copy of the (y^1, y^2)-axes: t to the right, y^1 towards the viewer, y^2 up
    _x, _v, _t = (1.0, 2.0), (1.2, 0.4), t_path.value
    _g = (_x[0] + _t * _v[0], _x[1] + _t * _v[1])
    _s = np.array([-1.3, 3.4])
    _copy = [] if _t == 0 else [((-0.5, _t, 0), (5.0, _t, 0), lk.GREY, 1.2), ((0, _t, -0.5), (0, _t, 3.3), lk.GREY, 1.2)]
    lk.turntable(
        -20,
        20,
        "graph of gamma, a line in R x R^2, with its points (0, x) and (t, x + t v), and the axes of {t} x R^2",
        [
            lk.panel(
                1.0,
                lines=[(_x[0] + _s * _v[0], _s, _x[1] + _s * _v[1], "#000000", 1.6)],
                arrows=_copy + [((0, 0, 0), (_x[0], 0, _x[1]), "#000000"), ((0, _t, 0), (_g[0], _t, _g[1]), lk.GREEN)],
                points=[((_x[0], 0, _x[1]), "#000000", 6.0 if _t == 0 else 4.5), ((_g[0], _t, _g[1]), lk.GREEN, 4.5), ((0, _t, 0), lk.GREY, 3.5)],
                axes=[((-0.5, 0, 0), (5.6, 0, 0), "y^1", -120), ((0, -1.5, 0), (0, 4.0, 0), "t", 0), ((0, 0, -0.5), (0, 0, 3.8), "y^2", 90)],
                texts=[((0, 0, 0), "0", "#000000", -45), ((_x[0] + 3.0 * _v[0], 3.0, _x[1] + 3.0 * _v[1]), r"\mathrm{graph}(\gamma)", "#000000", -90, 8),
                       ((_x[0], 0, _x[1]), r"(0, \vec{x})", "#000000", 45, 9), ((_g[0], _t, _g[1]), r"(t, \vec{x} + t\vec{v})", lk.GREEN, 45, 10)],
                box=((-0.3, 5.4), (-1.3, 3.8), (-0.3, 3.6)),
            )
        ],
        height=lk.H3D,
        width=460,
        key="L06-graph-line",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(blank, lk, mo, t_path):
    # module: image and graph
    # example: the affine parameterization of a line, its image and its graph, with the t-line, the map gamma and Im(gamma)
    # in the plane above graph(gamma) in R x R^2, both moving with the slider t
    _x, _v, _t = (1.0, 2.0), (1.2, 0.4), t_path.value
    _g = (_x[0] + _t * _v[0], _x[1] + _t * _v[1])
    _fig, _ax = blank(lk.FULL, 3.0, (-6.6, 6.9), (-0.7, 3.9))

    def _at(s):
        return -5.6 + 0.8 * (s + 1)

    lk.arrow(_ax, (-6.2, 1.5), (-1.9, 1.5), "black", lw=0.9)
    _ax.text(-1.9, 1.32, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    _ax.plot(_at(0), 1.5, "o", color="black", ms=6 if _t == 0 else 4.5, zorder=4)
    _ax.plot(_at(_t), 1.5, "o", color=lk.GREEN, ms=4.5, zorder=4)
    _ax.text(_at(0), 1.32, "$0$", fontsize=12, ha="center", va="top")
    _ax.text(_at(_t), 1.68, "$t$", fontsize=13, ha="center", va="bottom", color=lk.GREEN)
    lk.arrow(_ax, (-1.55, 2.2), (-0.45, 2.2), "black", lw=0.9, connectionstyle="arc3,rad=-0.3")
    _ax.text(-1.0, 2.5, r"$\gamma$", fontsize=13, ha="center", va="bottom")
    lk.arrow(_ax, (-0.4, 0), (5.6, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.4), (0, 3.7), "black", lw=0.9)
    _ax.text(5.6, -0.14, "$y^1$", fontsize=13, ha="right", va="top")
    _ax.text(-0.14, 3.7, "$y^2$", fontsize=13, ha="right", va="top")
    _ax.plot([_x[0] + s * _v[0] for s in (-1.3, 3.4)], [_x[1] + s * _v[1] for s in (-1.3, 3.4)], color="black", lw=1.2)
    lk.arrow(_ax, (0, 0), _v, lk.RED)
    lk.arrow(_ax, (0, 0), _x, "black")
    lk.arrow(_ax, (0, 0), _g, lk.GREEN)
    _ax.plot(*_x, "o", color="black", ms=6 if _t == 0 else 4, zorder=4)
    _ax.plot(*_g, "o", color=lk.GREEN, ms=4, zorder=4)
    _ax.text(_x[0] + 3.4 * _v[0] + 0.1, _x[1] + 3.4 * _v[1], r"$\mathrm{Im}(\gamma)$", fontsize=13, ha="left", va="center")
    _ax.text(_v[0] + 0.1, _v[1] + 0.05, r"$\vec{v}$", color=lk.RED, fontsize=13, ha="left", va="bottom")
    _ax.text(_x[0], _x[1] + 0.35, r"$\vec{x} = \gamma(0)$", fontsize=13, ha="center", va="bottom")
    _ax.text(_g[0] + 0.05, _g[1] - 0.15, r"$\gamma(t) = \vec{x} + t\vec{v}$", color=lk.GREEN, fontsize=13, ha="left", va="top")

    lk.example(
        [
            r"""
            $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ affine parameterization

            > $\gamma(t) = \vec{x} + t\vec{v}$ &nbsp; (with $\vec{v} \neq \vec{0}$)
            """,
            lk.aside(
                r"> > $\leadsto$ &nbsp; $\mathrm{Im}(\gamma) = \big\{ \vec{y} \in \mathbb{R}^2 \;\big|\; \exists \, t \in \mathbb{R}, \ \vec{y} = \gamma(t) \big\}$",
                r"line in $\mathbb{R}^2$ through $\vec{x}$<br>in the direction of $\vec{v}$",
            ),
            lk.aside(
                r"> > $\leadsto$ &nbsp; $\mathrm{graph}(\gamma) = \big\{ (t, \vec{y}) \in \mathbb{R} \times \mathbb{R}^2 \;\big|\; t \in \mathbb{R}, \ \vec{y} = \gamma(t) \big\}$",
                r"subset of $\mathbb{R} \times \mathbb{R}^2 \approx \mathbb{R}^3$",
            ),
            r"$$ (0, \vec{x}) = \begin{bmatrix} 0 \\ x^1 \\ x^2 \end{bmatrix}, \qquad (t, \vec{x} + t\vec{v}) = \begin{bmatrix} t \\ x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix} $$",
            lk.interactive(mo.vstack([_fig, lk.frame("L06-graph-line", lk.H3D, width=460)], align="center", gap=0.5), controls=[t_path]),
        ],
        label="ex-line",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: image and graph
    # remark: image and graph help us visualize
    lk.remark(
        r"""
        $\mathrm{Im}(f)$ and $\mathrm{graph}(f)$ help us visualize $f$ as a set of points (very useful in lower dimensions)

        > $\leadsto$ &nbsp; we might have many functions with same image

        > $\leadsto$ &nbsp; graph essentially determines the function completely! (but it lives in higher dimensions)
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: level sets
    # section
    lk.section("Level sets")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: level sets
    # definition: level set
    lk.definition(
        r"""
        Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$, $\vec{b} \in B$ fixed

        > • &nbsp; **level set** of $f$ with value $\vec{b}$ is

        $$
        f^{-1}(\vec{b}) = \big\{ \vec{x} \in \mathbb{R}^n \;\big|\; \vec{x} \in A \text{ and } f(\vec{x}) = \vec{b} \big\}
        $$
        """,
        label="def-level-set",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: level sets
    # example: the sphere of radius 2 as a level set of the length, with two of its points
    _q = [tuple(2 * np.array(_d) / np.linalg.norm(_d)) for _d in ((0.3, 1.0, 1.7), (0.2, 1.3, 1.5))]
    _th, _ph = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 49), indexing="ij")
    _w = np.linspace(0, 2 * np.pi, 121)
    _fig = lk.turntable(
        28,
        22,
        "the sphere of radius 2 about the origin, the level set of f with value 2, with two of its points x and y",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_th) * np.cos(_ph), 2 * np.sin(_th) * np.sin(_ph), 2 * np.cos(_th), alpha=0.25)],
                lines=[(2 * np.cos(_w), 2 * np.sin(_w), 0 * _w, lk.BLUE, 1.0)],
                outlines=[("sphere", (0, 0, 0), 2.0, lk.BLUE, 1.4)],
                arrows=[((0, 0, 0), _q[0], lk.RED), ((0, 0, 0), _q[1], lk.GREEN)],
                points=[(tuple(2 * _d), "#000000", 2.6) for _d in np.eye(3)],
                axes=[((-1.0, 0, 0), (3.0, 0, 0), "x^1", -120), ((0, -1.0, 0), (0, 3.0, 0), "x^2", 0), ((0, 0, -1.0), (0, 0, 3.0), "x^3", 90)],
                texts=[(tuple(2 * _d), "2", "#000000", _a) for _d, _a in zip(np.eye(3), (120, -60, 150))]
                + [((0, 0, 0), r"\vec{0}", "#000000", -60), (_q[0], r"\vec{x}", lk.RED, 150, 7), (_q[1], r"\vec{y}", lk.GREEN, 20, 7),
                   ((-0.871, 1.452, -1.065), "f^{-1}(2)", lk.BLUE, -40, 8)],
            )
        ],
        height=lk.H3D,
    )
    lk.example(
        [
            r"""
            $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$, &nbsp; $\vec{x} \longmapsto \lVert \vec{x} \rVert$

            fix $r = 2$ &nbsp; $\Longrightarrow$ &nbsp; $f^{-1}(2) = \big\{ \vec{x} \in \mathbb{R}^3 \;\big|\; \lVert \vec{x} \rVert = 2 \big\}$

            <span class='lk-ghost'>fix $r = 2$ &nbsp; $\Longrightarrow$ &nbsp; $f^{-1}(2)$</span> $=$ sphere centered at $\vec{0}$ with radius $r = 2$
            """,
            lk.figure(_fig),
        ],
        label="ex-sphere",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: level sets
    # remark: f^{-1}(b) is not the inverse function
    lk.remark(
        [
            r"""
            Here $f^{-1}(\vec{b})$ is NOT the value of the inverse function of $f$ (we don't even know if $f$ has inverse)

            $f^{-1}(\vec{b})$ is the set of points in the domain of $f$ which gives the value “$\vec{b}$” as an output!

            > $\leadsto$ &nbsp; if $f$ is invertible then, for each $\vec{b} \in B$,
            """,
            lk.aside(
                r"> > $f^{-1}(\vec{b}) = \big\{ \vec{x} \in A \;\big|\; f(\vec{x}) = \vec{b} \big\}$ <span class='lk-mark'>has a single element</span>",
                r"which we call “$f^{-1}(\vec{b})$”",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(blank, lk, np, quadric):
    # module: level sets
    # example: level sets of f in the plane and of g in space
    _fig, _ax = blank(3.4, 3.3, (-3.6, 3.9), (-3.6, 3.8))
    lk.arrow(_ax, (-3.4, 0), (3.5, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -3.4), (0, 3.5), "black", lw=0.9)
    _ax.text(3.5, -0.15, "$x^1$", fontsize=13, ha="right", va="top")
    _ax.text(0.15, 3.5, "$x^2$", fontsize=13, ha="left", va="top")
    _s = np.linspace(-2.9, 2.9, 200)
    for _sign in (1, -1):
        _ax.plot(_s, _sign * _s, color=lk.ORANGE, lw=1.4)
        _ax.plot(_sign * np.sqrt(1 + _s[20:-20] ** 2), _s[20:-20], color=lk.BLUE, lw=1.4)
        _ax.plot(_s[35:-35], _sign * np.sqrt(4 + _s[35:-35] ** 2), color=lk.RED, lw=1.4)
    _ax.text(1.75, 0.95, "$f^{-1}(1)$", color=lk.BLUE, fontsize=12, ha="left", va="center")
    _ax.text(2.9, 2.9, "$f^{-1}(0)$", color=lk.ORANGE, fontsize=12, ha="left", va="bottom")
    _ax.text(-1.9, -2.92, "$f^{-1}(-4)$", color=lk.RED, fontsize=12, ha="center", va="top")

    # g^{-1}(-4) inside the cone g^{-1}(0) inside g^{-1}(1), all cut at |x^3| <= 3
    _fig2 = lk.turntable(
        28,
        22,
        "level sets of g in space: the hyperboloid of one sheet g^{-1}(1) around the cone g^{-1}(0) around the hyperboloid of two sheets g^{-1}(-4)",
        [
            lk.panel(
                1.0,
                surfaces=quadric(1, 3.0, lk.BLUE, 0.3) + quadric(0, 3.0, lk.ORANGE, 0.45) + quadric(-4, 3.0, lk.RED, 0.7),
                axes=[((-1.2, 0, 0), (4.4, 0, 0), "x^1", -120), ((0, -1.2, 0), (0, 4.0, 0), "x^2", 0), ((0, 0, -1.2), (0, 0, 5.0), "x^3", 90)],
                texts=[((0, np.sqrt(10), 3.0), "g^{-1}(1)", lk.BLUE, 0, 8), ((0, -3.0, 3.0), "g^{-1}(0)", lk.ORANGE, 180, 8), ((0, np.sqrt(5), -3.0), "g^{-1}(-4)", lk.RED, -20, 10)],
            )
        ],
        height=lk.H3D,
    )

    lk.example(
        [
            r"""
            $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $\begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \longmapsto (x^1)^2 - (x^2)^2$

            what are the level sets with values $1, 0, -4$?

            $$
            f^{-1}(b) = \left\{ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \;\middle|\; (x^1)^2 - (x^2)^2 = b \right\}
            $$

            > $f^{-1}(0) \iff \lvert x^1 \rvert = \lvert x^2 \rvert$ &nbsp; (a cone)

            > $f^{-1}(1) \iff (x^1)^2 - (x^2)^2 = 1$ &nbsp; (a hyperbola)

            > $f^{-1}(-4) \iff (x^1)^2 - (x^2)^2 = -4$ &nbsp; (also a hyperbola)
            """,
            lk.figure(_fig),
            r"""
            $g : \mathbb{R}^3 \longrightarrow \mathbb{R}$, &nbsp; $\begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \longmapsto (x^1)^2 + (x^2)^2 - (x^3)^2$

            > $g^{-1}(0)$ &nbsp; (cone)

            > $g^{-1}(1)$ &nbsp; (hyperboloid of one sheet)

            > $g^{-1}(-4)$ &nbsp; (hyperboloid of two sheets)
            """,
            lk.figure(_fig2),
        ],
        label="ex-quadrics",
    )
    return


@app.cell(hide_code=True)
def _(b_level, lk, np, quadric):
    # module: level sets
    # the scene of g^{-1}(b) for the slider b, cut at |x^3| <= 3
    _b = b_level.value
    lk.turntable(
        28,
        22,
        "the level set of g with value b in space, cut at |x3| <= 3: a hyperboloid of one sheet for b > 0, the cone for b = 0, a hyperboloid of two sheets for b < 0",
        [
            lk.panel(
                1.0,
                surfaces=quadric(_b, 3.0, lk.BLUE, 0.4),
                axes=[((-1.2, 0, 0), (4.6, 0, 0), "x^1", -120), ((0, -1.2, 0), (0, 4.4, 0), "x^2", 0), ((0, 0, -1.2), (0, 0, 4.0), "x^3", 90)],
                texts=[((0, np.sqrt(max(_b + 9, 0)), 3.0), "g^{-1}(b)", lk.BLUE, 0, 8)],
                box=((-2.8, 2.8), (-2.8, 2.8), (-2.8, 2.8)),
            )
        ],
        height=lk.H3D,
        key="L06-quadric",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(Figure, b_level, lk, mo, np):
    # module: level sets
    # illustration: f^{-1}(b) in the plane beside g^{-1}(b) in space, both moving with the slider b
    _b = b_level.value
    _fig = Figure(figsize=(3.2, 3.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-4, 4)
    _ax.set_ylim(-4, 4)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.grid(True, color=lk.LIGHT, lw=0.6)
    _ax.set_axisbelow(True)
    _ax.set_xticks(range(-4, 5, 2))
    _ax.set_yticks(range(-4, 5, 2))
    _ax.set_xlabel("$x^1$")
    _ax.set_ylabel("$x^2$", rotation=0, labelpad=10)
    _s = np.linspace(-4.2, 4.2, 400)
    for _sign in (1, -1):
        if _b > 0:
            _ax.plot(_sign * np.sqrt(_b + _s**2), _s, color=lk.BLUE, lw=1.4)
        elif _b < 0:
            _ax.plot(_s, _sign * np.sqrt(_s**2 - _b), color=lk.BLUE, lw=1.4)
        else:
            _ax.plot(_s, _sign * _s, color=lk.BLUE, lw=1.4)
    _ax.text(3.9, 3.9, "$f^{-1}(b)$", color=lk.BLUE, fontsize=12, ha="right", va="top")
    _row = mo.Html(
        '<div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 0.5rem 1.5rem;">'
        + '<div style="flex: none;">'
        + mo.as_html(_fig).text
        + "</div>"
        + '<div style="width: 360px; max-width: 100%;">'
        + lk.frame("L06-quadric", lk.H3D).text
        + "</div>"
        + "</div>"
    )
    lk.prose(lk.interactive(_row, controls=[b_level]))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic surfaces
    # definition: affine and quadratic scalar functions
    lk.definition(
        [
            r"""
            For $p : \mathbb{R}^3 \longrightarrow \mathbb{R}$ an **affine scalar function**

            $$
            p\left( \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \right) = a x^1 + b x^2 + c x^3 + d
            $$
            """,
            lk.aside(
                r"> $p^{-1}(r)$ is a <span class='lk-mark'>plane in $\mathbb{R}^3$</span>",
                r"starting point $\begin{bmatrix} {\large\tfrac{r - d}{a}} \\ 0 \\ 0 \end{bmatrix}$ if $a \neq 0$<br>normal vector $\begin{bmatrix} a \\ b \\ c \end{bmatrix}$",
            ),
            lk.gap(),
            r"""
            For $q : \mathbb{R}^3 \longrightarrow \mathbb{R}$ a **quadratic scalar function**

            $$
            \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \longmapsto
            \begin{aligned}
            &a (x^1)^2 + b (x^2)^2 + c (x^3)^2\\
            &+ d \, x^1 x^2 + e \, x^2 x^3 + f \, x^3 x^1\\
            &+ g \, x^1 + h \, x^2 + i \, x^3 + j
            \end{aligned}
            $$

            > $q^{-1}(r)$ is called a **quadratic surface**

            $$
            \begin{array}{lll}
            \bullet & \dfrac{(x^1)^2}{a^2} + \dfrac{(x^2)^2}{b^2} + \dfrac{(x^3)^2}{c^2} = r^2 & \quad \text{ellipsoids}\\[14pt]
            \bullet & \dfrac{(x^1)^2}{a^2} + \dfrac{(x^2)^2}{b^2} - \dfrac{(x^3)^2}{c^2} = \pm r^2 & \quad \text{hyperboloids}\\[14pt]
            \bullet & \dfrac{(x^1)^2}{a^2} + \dfrac{(x^2)^2}{b^2} - \dfrac{x^3}{c} = d & \quad \text{paraboloids}\\[10pt]
            \bullet & \ldots &
            \end{array}
            $$
            """,
        ],
        label="def-affine-quadratic",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quadratic surfaces
    # remark: level sets and graphs
    lk.remark(
        r"""
        Sometimes level sets of a function can be seen as graphs of another function and vice-versa!

        > $\Longrightarrow$ &nbsp; geometry of sets in $\mathbb{R}^n$ or $\mathbb{R}^m$ or $\mathbb{R}^n \times \mathbb{R}^m$ is useful to study properties of various functions!
        """
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
    # exercise: ln(x^2 - (x^1)^2)
    lk.exercise(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \ln\big( x^2 - (x^1)^2 \big)$

        a) Find the largest possible domain and codomain

        b) For those, find the image

        c) Sketch the level sets $f^{-1}(0)$, $f^{-1}(\ln 4)$
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: the map T
    lk.exercise(
        r"""
        Let $T : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ be given by &nbsp; $\begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \longmapsto \begin{bmatrix} x^1 + x^2 \\ (x^1 + x^2)^2 \end{bmatrix}$

        a) Sketch $\mathrm{Im}(T)$

        b) Describe $T^{-1}\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right)$ and $T^{-1}\left( \begin{bmatrix} 1 \\ 2 \end{bmatrix} \right)$
        """,
        label="ex-practice-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: a surface as level set, graph and image
    lk.exercise(
        r"""
        Consider the surface

        $$
        S = \left\{ \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \in \mathbb{R}^3 \;\middle|\; (x^1)^2 + (x^2)^2 - x^3 = 1 \right\}
        $$

        Find

        a) a function $f$ such that $S$ is a level set of $f$

        b) a function $g$ such that $S$ is the graph of $g$

        c) a function $h$ such that $S$ is the image of $h$
        """,
        label="ex-practice-3",
    )
    return


if __name__ == "__main__":
    app.run()
