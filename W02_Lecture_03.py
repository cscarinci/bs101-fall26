import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 3 · Matrices, linear transformations, and determinants", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Arc, Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(3, "Matrices, linear transformations, and determinants")
    return


@app.cell(hide_code=True)
def _(Arc, Figure, lk, math):
    # Helpers of this lecture: bare sketches, coordinate planes, labelled vectors, turning arcs

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=lk.LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def vector(ax, tail, tip, color, label=None, turn=0, r=15):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip (no box behind the label);
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            lk.arrow(ax, tail, tip, color)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5)

    def turn(ax, p, q, ccw, radius, name=None):
        """Circular arc from the direction of p to the direction of q (counterclockwise when ccw), with a head at its end,
        and `name` beside its middle."""
        t1, t2 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
        span = (t2 - t1) % (2 * math.pi) if ccw else -((t1 - t2) % (2 * math.pi))
        lo, hi = (t1, t1 + span) if ccw else (t1 + span, t1)
        ax.add_patch(Arc((0, 0), 2 * radius, 2 * radius, theta1=math.degrees(lo), theta2=math.degrees(hi), color=lk.GREEN, lw=1.4))
        end = (radius * math.cos(t2), radius * math.sin(t2))
        step = math.copysign(min(0.35 * abs(span), 0.2), span)
        back = (radius * math.cos(t2 - step), radius * math.sin(t2 - step))
        d = (end[0] - back[0], end[1] - back[1])
        n = math.hypot(*d)  # the head follows the chord of the last part of the arc
        lk.arrow(ax, (end[0] - 1e-3 * d[0] / n, end[1] - 1e-3 * d[1] / n), end, lk.GREEN)
        if name:
            mid = t1 + span / 2
            ax.text(1.45 * radius * math.cos(mid), 1.45 * radius * math.sin(mid), name, color=lk.GREEN, fontsize=13, ha="center", va="center")

    return blank, plane, turn, vector


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    ma = lk.slider(-3, 3, step=0.5, value=2, label="$a$")
    mb = lk.slider(-3, 3, step=0.5, value=1, label="$b$")
    mc = lk.slider(-3, 3, step=0.5, value=0.5, label="$c$")
    md = lk.slider(-3, 3, step=0.5, value=1.5, label="$d$")
    return ma, mb, mc, md


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: the dot product, norm and angle
    lk.recap(
        r"$$ \vec{x} \cdot \vec{y} = x^1 y^1 + x^2 y^2 + \dots + x^n y^n $$",
        lk.aside(r"$$ \lVert \vec{x} \rVert = \sqrt{\vec{x} \cdot \vec{x}} $$", "norm / length"),
        lk.aside(r"$$ \theta(\vec{x}, \vec{y}) = \arccos\left( \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert \lVert \vec{y} \rVert} \right) $$", "angle"),
        topic=r"Dot product in $\mathbb{R}^n$ &nbsp; $\cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 1.2, 1.3")
    return


@app.cell(hide_code=True)
def _(blank, lk):
    # module: orthogonal frames
    # in-class practice Q3: decomposition along a pairwise orthogonal frame, with the sketch of the orthogonal projection
    # of x onto the u direction
    _fig, _ax = blank(2.6, 1.5, (-0.3, 3.6), (-0.5, 2.2))
    _ax.plot([2, 2], [0, 1.8], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    lk.arrow(_ax, (0, 0), (3, 0), lk.RED)
    lk.arrow(_ax, (0, 0), (2, 0), lk.GREEN)
    lk.arrow(_ax, (0, 0), (2, 1.8), lk.BLUE)
    _ax.text(2.08, 1.88, r"$\vec{x}$", color=lk.BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(3.1, 0, r"$\vec{u}$", color=lk.RED, fontsize=13, ha="left", va="center")
    _ax.text(1.0, -0.14, r"$a\vec{u}$", color=lk.GREEN, fontsize=13, ha="center", va="top")

    lk.prose(
        "in-class practice Q3:",
        r"> Given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$ pairwise orthogonal we can write $\vec{x} \in \mathbb{R}^3$ as",
        r"$$ \vec{x} = a\vec{u} + b\vec{v} + c\vec{w}, $$",
        r"> where &nbsp; $a = \dfrac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}, \quad b = \dfrac{\vec{x} \cdot \vec{v}}{\lVert \vec{v} \rVert^2}, \quad c = \dfrac{\vec{x} \cdot \vec{w}}{\lVert \vec{w} \rVert^2}$",
        lk.aside(
            lk.figure(_fig),
            r"$a\vec{u} = \dfrac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2} \vec{u} = \mathrm{proj}_{\vec{u}}(\vec{x})$<br>orthogonal projection of $\vec{x}$ onto the $\vec{u}$ direction",
        ),
        lk.aside(r"$\therefore$ &nbsp; $\mk{\vec{u}, \vec{v}, \vec{w}}$ pairwise orthogonal (orthogonal frame)", "all non-zero"),
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\vec{x} = \mathrm{proj}_{\vec{u}}(\vec{x}) + \mathrm{proj}_{\vec{v}}(\vec{x}) + \mathrm{proj}_{\vec{w}}(\vec{x})$",
            r"any vector in $\mathbb{R}^3$ decomposes as the sum of<br>orthogonal projections onto an orthogonal frame!",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # section
    lk.section("The standard basis")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # definition: the standard basis of R^n
    lk.definition(
        [
            r"$\mathbb{R}^n$ has a preferred orthogonal frame",
            lk.aside(
                r"$$ \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad \dots, \quad \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}. $$",
                r"standard basis vectors of $\mathbb{R}^n$",
            ),
        ],
        label="def-standard-basis",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # consequences: orthonormality
    lk.prose(
        r"$\leadsto$ &nbsp; $\vec{e}_i \cdot \vec{e}_j = 0$ if $i \neq j$",
        lk.aside(r"$\leadsto$ &nbsp; $\vec{e}_i \cdot \vec{e}_i = 1$", "unit length vectors"),
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: standard basis
    # components as projections, with x in R^3, the standard basis and the projections x^i e_i onto the axes
    _p = (1.4, 2.0, 1.7)
    _s = np.linspace(0, 1, 40)
    _feet = [(_p[0], 0, 0), (0, _p[1], 0), (0, 0, _p[2])]
    # x drops to the x^1 x^2 plane, then to the x^1 and x^2 axes; and across to the x^3 axis
    _guides = [(_p, (_p[0], _p[1], 0)), ((_p[0], _p[1], 0), _feet[0]), ((_p[0], _p[1], 0), _feet[1]), (_p, _feet[2])]
    # each axis is left out from the origin to the foot of x^i e_i, so that the axis never covers the arrows; the shafts of
    # the x^i e_i lie behind the e_i
    _fig = lk.turntable(
        30,
        22,
        "the vector x in R3 with the standard basis vectors e1, e2, e3 and its projections x1 e1, x2 e2, x3 e3 onto the three axes",
        [
            lk.panel(
                1.0,
                lines=[
                    ([-0.5, 0], [0, 0], [0, 0], "#000000", 1.1),
                    ([0, 0], [-0.5, 0], [0, 0], "#000000", 1.1),
                    ([0, 0], [0, 0], [-0.5, 0], "#000000", 1.1),
                ]
                + [(0.96 * _f[0] * _s, 0.96 * _f[1] * _s, 0.96 * _f[2] * _s, lk.GREEN, 1.8, None, -0.2) for _f in _feet]
                + [(_a[0] + (_b[0] - _a[0]) * _s, _a[1] + (_b[1] - _a[1]) * _s, _a[2] + (_b[2] - _a[2]) * _s, lk.GREY, 1.0, [4, 3]) for _a, _b in _guides],
                arrows=[((_p[0], 0, 0), (2.1, 0, 0), "#000000", 1.1), ((0, _p[1], 0), (0, 2.7, 0), "#000000", 1.1), ((0, 0, _p[2]), (0, 0, 2.2), "#000000", 1.1)]
                + [(tuple(0.9 * c for c in _f), _f, lk.GREEN) for _f in _feet]
                + [((0, 0, 0), (1, 0, 0), lk.GREY), ((0, 0, 0), (0, 1, 0), lk.GREY), ((0, 0, 0), (0, 0, 1), lk.GREY), ((0, 0, 0), _p, lk.BLUE)],
                texts=[((0.55, 0, 0), r"\vec{e}_1", lk.GREY, -60), ((0, 0.55, 0), r"\vec{e}_2", lk.GREY, -90), ((0, 0, 0.55), r"\vec{e}_3", lk.GREY, 0),
                       (_p, r"\vec{x}", lk.BLUE, 20, 7), (_feet[0], r"x^1 \vec{e}_1", lk.GREEN, 160, 9), (_feet[1], r"x^2 \vec{e}_2", lk.GREEN, -90, 8),
                       ((0, 0, 0.8 * _p[2]), r"x^3 \vec{e}_3", lk.GREEN, 180, 8)],
            )
        ],
        height=lk.H3D_FLAT,
    )
    _ub = lambda body, label: r"\underbrace{" + body + r"}_{\scriptstyle " + label + "}"
    lk.prose(
        r"""
        Given

        $$
        \begin{aligned}
        \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} &= x^1 \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix} + \dots + x^n \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}\\[6pt]
        &= """
        + _ub(r"x^1 \vec{e}_1", r"\mathrm{proj}_{\vec{e}_1}(\vec{x})")
        + " + "
        + _ub(r"x^2 \vec{e}_2", r"\mathrm{proj}_{\vec{e}_2}(\vec{x})")
        + r" + \dots + "
        + _ub(r"x^n \vec{e}_n", r"\mathrm{proj}_{\vec{e}_n}(\vec{x})")
        + r"""\\[6pt]
        &= (\vec{x} \cdot \vec{e}_1) \, \vec{e}_1 + (\vec{x} \cdot \vec{e}_2) \, \vec{e}_2 + \dots + (\vec{x} \cdot \vec{e}_n) \, \vec{e}_n
        \end{aligned}
        $$
        """,
        lk.figure(_fig),
        r"$\leadsto$ &nbsp; any vector is a unique linear combination of the standard basis vectors",
        r"$\leadsto$ &nbsp; the component $x^i$ of $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}$ is the signed length of its projection along $\vec{e}_i$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matrices
    # section
    lk.section("Matrices")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matrices
    # definition: m x n matrix
    lk.definition(
        [
            r"Given $m, n \in \mathbb{Z}_{>0}$, an $m \times n$ **matrix** is an array of numbers with $m$ rows and $n$ columns",
            lk.aside(
                r"$$ A = \begin{bmatrix} A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\ A^2{}_1 & A^2{}_2 & \cdots & A^2{}_n \\ \vdots & & & \\ A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n \end{bmatrix}, \qquad \mk{A^i{}_j} \in \mathbb{R} \quad \forall \ \begin{matrix} i = 1, \dots, m \\ j = 1, \dots, n \end{matrix}, $$",
                r"(ij) component of the matrix $A$<br>superscript $i$ denotes the row<br>subscript $j$ denotes the column",
            ),
            lk.aside(r"$$ A \in \mathrm{Mat}(\mk{m} \times \mk{n}). $$", "$m$ = rows, $n$ = columns"),
        ],
        label="def-matrix",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matrices
    # motivation: why matrices
    lk.prose(
        "Why are we interested in matrices?",
        lk.aside(
            r"> $\leadsto$ &nbsp; generalization of <span class='lk-mark'>vectors</span> (addition and multiplication extend to matrices!)",
            r"$n \times 1$ matrices",
        ),
        r"> $\leadsto$ &nbsp; will give the simplest examples of multivariable functions!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matrices
    # definition: addition and multiplication by a scalar
    lk.definition(
        [
            r"Given $A \in \mathrm{Mat}(m \times n)$, $B \in \mathrm{Mat}(m \times n)$, $\alpha \in \mathbb{R}$",
            r"> $\leadsto$ &nbsp; $A + B \in \mathrm{Mat}(m \times n)$ has components",
            lk.aside(r"$$ (A + B)^i{}_j = A^i{}_j + B^i{}_j $$", "componentwise addition"),
            r"> $\leadsto$ &nbsp; $\alpha A \in \mathrm{Mat}(m \times n)$ has components",
            lk.aside(r"$$ (\alpha A)^i{}_j = \alpha A^i{}_j $$", "componentwise multiplication (by a scalar)"),
        ],
        label="def-sum",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matrices
    # example: sum and multiple
    lk.example(
        r"""
        $A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}, \ B = \begin{bmatrix} 6 & 4 & 2 \\ 5 & 3 & 1 \end{bmatrix} \in \mathrm{Mat}(2 \times 3)$

        > $\leadsto$ &nbsp; $A + B = \begin{bmatrix} 7 & 6 & 5 \\ 9 & 8 & 7 \end{bmatrix}, \quad 3A = \begin{bmatrix} 3 & 6 & 9 \\ 12 & 15 & 18 \end{bmatrix}$
        """,
        label="ex-sum",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication
    # section
    lk.section("Matrix multiplication")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication
    # definition: matrix product
    lk.definition(
        [
            r"Given $A \in \mathrm{Mat}(m \times p)$, $B \in \mathrm{Mat}(p \times n)$",
            r"> $\leadsto$ &nbsp; $AB \in \mathrm{Mat}(m \times n)$ has components",
            lk.aside(r"$$ (AB)^i{}_j = A^i{}_1 B^1{}_j + A^i{}_2 B^2{}_j + \dots + A^i{}_p B^p{}_j $$", "sum of products of corresponding components"),
        ],
        label="def-product",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication
    # example: a 2 x 3 times a 3 x 2 matrix
    lk.example(
        [
            r"$A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times \mk{3})$",
            lk.aside(r"$B = \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix} \in \mathrm{Mat}(\mk{3} \times 2)$", "must be the same in order to define $AB$"),
            r"""
            $$
            \begin{aligned}
            AB = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix} &= \begin{bmatrix} 1 \times 1 + 2 \times 0 + 3 \times 2 & 1 \times 0 + 2 \times 3 + 3 \times 0 \\ 4 \times 1 + 5 \times 0 + 6 \times 2 & 4 \times 0 + 5 \times 3 + 6 \times 0 \end{bmatrix}\\[6pt]
            &= \begin{bmatrix} 7 & 6 \\ 16 & 15 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
            \end{aligned}
            $$
            """,
        ],
        label="ex-product",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication
    # remark: when products are defined, and non-commutativity
    lk.remark(
        [
            "Most times we cannot multiply two matrices",
            r"> $A \in \mathrm{Mat}(m \times q)$, $B \in \mathrm{Mat}(p \times n)$",
            r"""
            > > $\leadsto$ &nbsp; $AB$ can only be defined if $p = q$

            > > > $\Longrightarrow$ &nbsp; $AB \in \mathrm{Mat}(m \times n)$

            > > $\leadsto$ &nbsp; $BA$ can only be defined if $m = n$

            > > > $\Longrightarrow$ &nbsp; $BA \in \mathrm{Mat}(p \times q)$
            """,
            r"> > $\leadsto$ &nbsp; $p = q$ and $m = n$",
            lk.aside(r"> > > $\not\Longrightarrow$ &nbsp; $\mk{AB} = \mk{BA}$", r"$AB \in \mathrm{Mat}(n \times n)$, $BA \in \mathrm{Mat}(p \times p)$"),
            r"""
            > > $\leadsto$ &nbsp; $p = q = m = n$

            > > > $\not\Longrightarrow$ &nbsp; $AB = BA$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication
    # example: two square matrices that do not commute
    lk.example(
        [
            r"$A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}, \ B = \begin{bmatrix} 5 & 0 \\ 1 & 1 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$",
            lk.aside(
                r"$$ \Longrightarrow \quad AB = \begin{bmatrix} 11 & 1 \\ 3 & 3 \end{bmatrix} \mathrel{\mk{\neq}} BA = \begin{bmatrix} 10 & 5 \\ 2 & 4 \end{bmatrix} $$",
                "matrix multiplication is non-commutative<br>even for square matrices",
            ),
        ],
        label="ex-noncommutative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # section
    lk.section("Linear transformations")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # remark: matrices transform vectors
    lk.remark(
        r"""
        matrix multiplication can “transform” vectors into other vectors

        > $A \in \mathrm{Mat}(m \times n)$ and $\vec{x} \in \mathbb{R}^n \approx \mathrm{Mat}(n \times 1)$

        > > $\Longrightarrow$ &nbsp; $A\vec{x} \in \mathrm{Mat}(m \times 1) \approx \mathbb{R}^m$

        > > $\Longrightarrow$ &nbsp; $A : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is a multivariable function!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # example: a 2 x 3 matrix acting on a vector of R^3
    lk.example(
        r"""
        $A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \quad \vec{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \in \mathbb{R}^3 = \mathrm{Mat}(3 \times 1)$

        $$
        \Longrightarrow \quad A\vec{x} = \begin{bmatrix} 1 + 4 + 9 \\ 4 + 10 + 18 \end{bmatrix} = \begin{bmatrix} 14 \\ 32 \end{bmatrix} \in \mathbb{R}^2 = \mathrm{Mat}(2 \times 1)
        $$
        """,
        label="ex-Ax",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # motivation: matrix functions are linear
    lk.prose(r"$\leadsto$ &nbsp; matrix multiplication always defines linear functions! (very special property)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # definition: linear function
    lk.definition(
        r"""
        A function $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called **linear** if $\forall \, \vec{x}, \vec{y} \in \mathbb{R}^n$ and $\forall \, \alpha, \beta \in \mathbb{R}$

        $$
        f(\alpha \vec{x} + \beta \vec{y}) = \alpha f(\vec{x}) + \beta f(\vec{y}).
        $$
        """,
        label="def-linear",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # theorem: matrices and linear functions
    lk.theorem(
        r"Every function defined by an $m \times n$ matrix via matrix multiplication is linear. Conversely, every linear function $\mathbb{R}^n \longrightarrow \mathbb{R}^m$ is defined by an $m \times n$ matrix!",
        label="thm-linear",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # proof: columns, A x as a combination of the columns, linearity; then the converse through the standard basis
    _col = lambda k: r"\begin{bmatrix} A^1{}_" + k + r" \\ A^2{}_" + k + r" \\ \vdots \\ A^m{}_" + k + r" \end{bmatrix}"
    lk.proof(
        [
            lk.aside(
                r"$$ A = \begin{bmatrix} A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\ \vdots & \vdots & & \vdots \\ A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n \end{bmatrix} = \begin{bmatrix} \mk{\vec{A}_1} & \mk{\vec{A}_2} & \cdots & \mk{\vec{A}_n} \end{bmatrix} \in \mathrm{Mat}(m \times n) $$",
                r"$n$ $m$-vectors<br>$\leadsto$ column vectors of $A$",
            ),
            r"""
            $$
            \begin{aligned}
            \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \in \mathbb{R}^n \quad \Longrightarrow \quad A\vec{x} &= \begin{bmatrix} A^1{}_1 x^1 + A^1{}_2 x^2 + \dots + A^1{}_n x^n \\ A^2{}_1 x^1 + A^2{}_2 x^2 + \dots + A^2{}_n x^n \\ \vdots \\ A^m{}_1 x^1 + A^m{}_2 x^2 + \dots + A^m{}_n x^n \end{bmatrix}\\[6pt]
            &= x^1 """
            + _col("1")
            + " + x^2 "
            + _col("2")
            + r" + \dots + x^n "
            + _col("n")
            + r"""\\[6pt]
            &= x^1 \vec{A}_1 + x^2 \vec{A}_2 + \dots + x^n \vec{A}_n
            \end{aligned}
            $$
            """,
            r"""
            $$
            \begin{aligned}
            A(\alpha \vec{x} + \beta \vec{y}) &= (\alpha x^1 + \beta y^1) \vec{A}_1 + \dots + (\alpha x^n + \beta y^n) \vec{A}_n\\
            &= \alpha A\vec{x} + \beta A\vec{y}
            \end{aligned}
            $$
            """,
            lk.gap(),
            "For the converse direction",
            r"> $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ linear",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \Longrightarrow \quad f(\vec{x}) &= f(x^1 \mk{\vec{e}_1} + x^2 \mk{\vec{e}_2} + \dots + x^n \mk{\vec{e}_n}), \quad \forall \, \vec{x} \in \mathbb{R}^n\\
                &= x^1 f(\vec{e}_1) + x^2 f(\vec{e}_2) + \dots + x^n f(\vec{e}_n)\\
                &= A\vec{x}, \quad \text{where} \quad A = \begin{bmatrix} \mk{f(\vec{e}_1)} & \mk{f(\vec{e}_2)} & \cdots & \mk{f(\vec{e}_n)} \end{bmatrix} \in \mathrm{Mat}(m \times n).
                \end{aligned}
                $$
                """,
                [(1, r"$\vec{e}_i$: standard basis of $\mathbb{R}^n$"), (3, r"$\vec{A}_i = f(\vec{e}_i) \in \mathbb{R}^m$")],
                rows=3,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # consequences: why linear functions matter
    lk.prose(
        r"$\leadsto$ &nbsp; linear functions (or linear transformations) are the simplest non-trivial examples of multivariable functions",
        r"$\leadsto$ &nbsp; later, we will introduce derivatives of more general multivariable functions as their best linear approximations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linear
    # remark: products are compositions
    lk.remark(
        [
            "Matrix multiplication is the same as composition of linear transformations",
            r"""
            $$
            \begin{aligned}
            A &\in \mathrm{Mat}(m \times p) &&\leftrightsquigarrow \quad A : \mathbb{R}^p \longrightarrow \mathbb{R}^m\\
            B &\in \mathrm{Mat}(p \times n) &&\leftrightsquigarrow \quad B : \mathbb{R}^n \longrightarrow \mathbb{R}^p\\
            AB &\in \mathrm{Mat}(m \times n) &&\leftrightsquigarrow \quad A \circ B : \mathbb{R}^n \longrightarrow \mathbb{R}^m.
            \end{aligned}
            $$
            """,
            r"> $\leadsto$ &nbsp; another way to see that matrix multiplication is non-commutative!",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: determinants
    # section
    lk.section(r"Determinants of $2 \times 2$ matrices")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: determinants
    # definition: determinant of a 2 x 2 matrix
    lk.definition(
        lk.aside(
            r"For $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$, the **determinant** of $A$ is $\det(A) = ad - bc \in \mathbb{R}$.",
            r"$A \in \mathrm{Mat}(2 \times 2) \ \leftrightsquigarrow \ A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear",
        ),
        label="def-det",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, ma, math, mb, mc, md, plane, turn, vector):
    # module: determinants
    # signed area, with the parallelogram defined by the columns A1 = A e1, A2 = A e2 and the angle theta turning from A1
    # to A2, moving with the sliders a, b, c, d
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c + 0.0
    _fig = Figure(figsize=(3.4, 3.4), layout="constrained")
    _ax = _fig.subplots()
    _small = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_a + _b), abs(_c + _d)) <= 3
    plane(_ax, 4.4 if _small else 7.6)  # the frame follows the parallelogram: nothing is clipped
    _ticks = range(-4, 5, 2) if _small else range(-6, 7, 3)
    _ax.set_xticks(_ticks, [f"${_k}$" for _k in _ticks])
    _ax.set_yticks(_ticks, [f"${_k}$" for _k in _ticks])
    _ax.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=lk.LIGHT, lw=0)
    _ax.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_ax, (0, 0), (_a, _c), lk.BLUE, r"$\vec{A}_1 = A\vec{e}_1$", turn=-55, r=30)
    vector(_ax, (0, 0), (_b, _d), lk.RED, r"$\vec{A}_2 = A\vec{e}_2$", turn=35, r=30)
    if _det != 0:
        _r = 0.6 * min(math.hypot(_a, _c), math.hypot(_b, _d), 2.0)
        turn(_ax, (_a, _c), (_b, _d), _det > 0, max(_r, 0.3), r"$\theta$")

    # the margin comment follows the sign of det A (the sliders can turn the columns clockwise)
    if _det > 0:
        _note = r"$\sin\theta > 0$<br>$\Longrightarrow$ $\det A > 0$"
    elif _det < 0:
        _note = r"$\sin\theta < 0$<br>$\Longrightarrow$ $\det A < 0$"
    else:
        _note = r"$\theta = 0$ or $\pi$<br>$\Longrightarrow$ $\det A = 0$"
    lk.prose(
        r"$\leadsto$ &nbsp; the determinant is a fundamental property of a square matrix (also for $n > 2$)",
        r"$\leadsto$ &nbsp; it measures the “signed area” of the parallelogram defined by the columns of $A$",
        lk.aside(lk.interactive(_fig, controls=[ma, mb, mc, md]), _note),
        r"""
        $$
        \begin{aligned}
        \det A &= \text{signed area} = \lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \sin\big(\theta(\vec{A}_1, \vec{A}_2)\big)\\[10pt]
        (\det A)^2 &= \text{area}^2 = (\text{base} \times \text{height})^2\\
        &= \lVert \vec{A}_1 \rVert^2 \lVert \vec{A}_2 \rVert^2 \sin\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2\\
        &= \lVert \vec{A}_1 \rVert^2 \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2\\
        &= (ad - bc)^2
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: determinants
    # consequences: invertibility and the inverse
    lk.prose(
        r"$\leadsto$ &nbsp; it also determines whether or not $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ is invertible!",
        r"> > $\exists \, A^{-1} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ such that $A \circ A^{-1}(\vec{x}) = A^{-1} \circ A(\vec{x}) = \vec{x} \quad \forall \, \vec{x} \in \mathbb{R}^2$",
        r"> > > $\iff$ &nbsp; $\det(A) \neq 0$",
        lk.gap(),
        r"$\leadsto$ &nbsp; in fact, for $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ with $\det(A) = ad - bc \neq 0$, the inverse is",
        r"$$ A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} $$",
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
    # exercise: matrix of a linear map
    lk.exercise(
        r"""
        Let $f : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ be linear, with

        $$
        f\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right) = \begin{bmatrix} 3 \\ 1 \end{bmatrix} \quad \text{and} \quad f\left( \begin{bmatrix} 1 \\ -1 \end{bmatrix} \right) = \begin{bmatrix} 1 \\ 3 \end{bmatrix}.
        $$

        Find the matrix representation of $f$.

        Then compute $f\left( \begin{bmatrix} 2 \\ -1 \end{bmatrix} \right)$.
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: AB and BA
    lk.exercise(
        r"""
        Let $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix}$.

        Compute $AB$ and $BA$.

        Then find all vectors $\vec{x} \in \mathbb{R}^2$ such that $AB\vec{x} = BA\vec{x}$.

        Conclude that

        > $AB \neq BA$ does not imply $AB\vec{x} \neq BA\vec{x} \quad \forall \, \vec{x} \in \mathbb{R}^2$.
        """,
        label="ex-practice-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: invertibility and area
    lk.exercise(
        r"""
        For $t \in \mathbb{R}$, consider

        $$
        C_t = \begin{bmatrix} t & 1 \\ 2 & t - 1 \end{bmatrix}.
        $$

        For which values of $t$ is $C_t$ invertible?

        Let $Q = [0, 1] \times [0, 1] \subseteq \mathbb{R}^2$ be the unit square in $\mathbb{R}^2$.

        Draw $C_t(Q)$ and compute its area for $t = -2$, $t = 0$, $t = 2$.
        """,
        label="ex-practice-3",
    )
    return


if __name__ == "__main__":
    app.run()
