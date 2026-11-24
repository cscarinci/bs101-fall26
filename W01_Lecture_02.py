import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 2 · The Euclidean inner product (the dot product)", css_file="lecturekit/style.css")


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
    return Arc, Figure, lk, math, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(2, "The Euclidean inner product (the dot product)")
    return


@app.cell(hide_code=True)
def _(Arc, Figure, lk, math):
    # Helpers of this lecture: bare sketches, coordinate planes, labelled vectors, angle arcs

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def plane(lim, ticks, size=3.0):
        """A figure with one 2D axis styled as a coordinate plane with range [-lim, lim]."""
        fig = Figure(figsize=(size, size), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=lk.LIGHT, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_xticks(ticks, [f"${k}$" for k in ticks])
        ax.set_yticks(ticks, [f"${k}$" for k in ticks])
        return fig, ax

    def vector(ax, tail, tip, color, label=None, away=None, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), with its name beside the tip: beyond the tip,
        or to the side of the arrow away from the direction `away` (no box behind the name)."""
        v = (tip[0] - tail[0], tip[1] - tail[1])
        if v == (0, 0):
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
        else:
            lk.arrow(ax, tail, tip, color, **kw)
        if label:
            d = v if away is None else (-v[1], v[0])
            if away is not None and d[0] * away[0] + d[1] * away[1] > 0:
                d = (-d[0], -d[1])
            r = math.hypot(*d) or 1
            d = (d[0] / r, d[1] / r) if math.hypot(*d) else (0.7, 0.7)
            ax.annotate(label, tip, textcoords="offset points", xytext=(11 * d[0], 11 * d[1]), color=color, fontsize=13,
                        ha="left" if d[0] > 0.3 else "right" if d[0] < -0.3 else "center",
                        va="bottom" if d[1] > 0.3 else "top" if d[1] < -0.3 else "center", zorder=5)

    def angle(ax, p, q, radius, name=r"$\theta$"):
        """The (unsigned) angle between the directions of p and q, as an arc with its name beside its middle."""
        a1, a2 = math.degrees(math.atan2(p[1], p[0])), math.degrees(math.atan2(q[1], q[0]))
        if (a2 - a1) % 360 > 180:
            a1, a2 = a2, a1
        ax.add_patch(Arc((0, 0), 2 * radius, 2 * radius, theta1=a1, theta2=a2, color=lk.GREEN, lw=1.4))
        mid = math.radians(a1 + ((a2 - a1) % 360) / 2)
        ax.text(1.55 * radius * math.cos(mid), 1.55 * radius * math.sin(mid), name, color=lk.GREEN, fontsize=13, ha="center", va="center")

    return angle, blank, plane, vector


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    # One pair of vectors x, y drives the figures of the angle, of the Cauchy–Schwarz polynomial and of the triangle inequality.
    x1 = lk.slider(-4, 4, step=0.5, value=3, label="$x^1$")
    x2 = lk.slider(-4, 4, step=0.5, value=0, label="$x^2$")
    y1 = lk.slider(-4, 4, step=0.5, value=1, label="$y^1$")
    y2 = lk.slider(-4, 4, step=0.5, value=2, label="$y^2$")
    return x1, x2, y1, y2


@app.cell(hide_code=True)
def _(np, x1, x2, y1, y2):
    # the vectors of the sliders
    x = np.array([x1.value, x2.value], dtype=float)
    y = np.array([y1.value, y2.value], dtype=float)
    return x, y


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: points and vectors in R^n, vector addition and scalar-vector multiplication
    lk.recap(
        lk.aside(
            r"> $\displaystyle = \begin{bmatrix} x^1 \\ \mk{x^2} \\ \vdots \\ x^n \end{bmatrix}$ &nbsp; $n$-vectors (arrows between points)",
            r"$x^2$ = real number<br>$\leadsto$ 2nd component of $\vec{x}$",
        ),
        r"""
        $$
        \begin{array}{cc}
        {+} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n & \qquad \cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n\\[2pt]
        \text{vector addition} & \qquad \text{scalar-vector multiplication}\\[10pt]
        \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} + \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} = \begin{bmatrix} x^1 + y^1 \\ x^2 + y^2 \\ \vdots \\ x^n + y^n \end{bmatrix} & \qquad \alpha \cdot \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \alpha x^2 \\ \vdots \\ \alpha x^n \end{bmatrix}\\[4pt]
        \text{componentwise addition} & \qquad \text{componentwise multiplication}
        \end{array}
        $$
        """,
        r"$\leadsto$ &nbsp; allows us to do calculations with vectors the same way as with real numbers!",
        topic=r"$\mathbb{R}^n \ni \vec{x} = (x^1, x^2, \dots, x^n)$ &nbsp; points in $n$-space",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"Extra structure on $\mathbb{R}^n$ (needed for “measurements”)", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 1.2, 1.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: dot product
    # section
    lk.section("The Euclidean inner product (the dot product)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: dot product
    # definition: the dot product
    lk.definition(
        [
            r"Given two vectors $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}, \ \vec{y} = \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} \in \mathbb{R}^n$",
            r"we define their “**dot product**” or “**inner product**” as the real number",
            lk.aside(r"$$ \vec{x} \cdot \vec{y} = x^1 \cdot y^1 + x^2 \cdot y^2 + \dots + x^n \cdot y^n \in \mathbb{R} $$", "sum of products of components"),
        ],
        label="def-dot",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: dot product
    # consequences: a new multiplication, and the dot dropped for scalar-vector multiplication
    lk.prose(
        r"$\leadsto$ &nbsp; another extension of multiplication of real numbers, now to pairs of vectors, and taking scalar values",
        lk.aside(r"$$ \mk{\cdot} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R} $$", "not same as for scalar-vector multiplication!"),
        r"to avoid confusion, we drop “$\cdot$” for scalar-vector multiplication and write: &nbsp; $\alpha \vec{x} = \alpha \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \vdots \\ \alpha x^n \end{bmatrix}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: dot product
    # theorem: basic properties
    lk.theorem(
        [
            r"For all vectors $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and scalars $\alpha, \beta \in \mathbb{R}$",
            lk.aside(r"i) &nbsp; $\vec{x} \cdot \vec{y} = \vec{y} \cdot \vec{x}$", "symmetric"),
            lk.aside(
                r"ii) &nbsp; $\begin{cases} (\alpha \vec{x} + \beta \vec{y}) \cdot \vec{z} = \alpha \vec{x} \cdot \vec{z} + \beta \vec{y} \cdot \vec{z} \\ \vec{x} \cdot (\alpha \vec{y} + \beta \vec{z}) = \alpha \vec{x} \cdot \vec{y} + \beta \vec{x} \cdot \vec{z} \end{cases}$",
                r"linear on each of its 2 arguments<br>$\leadsto$ bilinear<br>(this is also a distributivity property)",
            ),
            lk.aside(r"iii) &nbsp; $\vec{x} \cdot \vec{x} \geq 0$, &nbsp; with “$=$” <span class='lk-mark'>iff</span> $\vec{x} = \vec{0}$", "positive definite<br>iff = if and only if"),
        ],
        title="basic properties",
        label="thm-dot-properties",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: dot product
    # proof
    lk.proof(r"exercise (using definitions and properties of real numbers)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: norm and angle
    # definition: norm and angle
    lk.definition(
        [
            lk.aside(r"The **<span class='lk-mark'>norm</span>** of a vector $\vec{x}$ is", "norm = length"),
            lk.aside(r"$$ \lVert \vec{x} \rVert := \mk{\sqrt{\vec{x} \cdot \vec{x}}} $$", r"makes sense since $\vec{x} \cdot \vec{x} \geq 0$"),
            r"The **angle** between two vectors $\vec{x}, \vec{y}$ is",
            lk.aside(
                r"$$ \theta(\vec{x}, \vec{y}) = \arccos\left( \mk{\frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert \lVert \vec{y} \rVert}} \right) \qquad (\text{must have } \vec{x}, \vec{y} \neq \vec{0}) $$",
                r"not so clear why this makes sense…<br>$\arccos : [-1, 1] \longrightarrow [0, \pi]$",
            ),
        ],
        label="def-norm-angle",
    )
    return


@app.cell(hide_code=True)
def _(angle, lk, plane, vector, x, x1, x2, y, y1, y2):
    # module: norm and angle
    # illustration: the angle between x and y, moving with the sliders
    _fig, _ax = plane(5, range(-4, 5, 2))
    vector(_ax, (0, 0), tuple(x), lk.BLUE, r"$\vec{x}$", away=tuple(y))
    vector(_ax, (0, 0), tuple(y), lk.RED, r"$\vec{y}$", away=tuple(x))
    if x.any() and y.any():
        angle(_ax, x, y, 0.8)
    lk.prose(lk.interactive(_fig, controls=[(x1, x2), (y1, y2)]))
    return


@app.cell(hide_code=True)
def _(Arc, blank, lk, math):
    # module: norm and angle
    # example: x = (3, 0), y = (1, √3), with a sketch
    _fig, _ax = blank(3.0, 1.9, (-0.6, 4.0), (-0.55, 2.4))
    lk.arrow(_ax, (-0.4, 0), (3.8, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.4), (0, 2.3), "black", lw=0.9)
    for _t in (1, 3):
        _ax.plot([_t, _t], [-0.05, 0.05], color="black", lw=0.9)
        _ax.text(_t, -0.14, f"${_t}$", fontsize=12, ha="center", va="top")
    _ax.plot([-0.05, 0.05], [math.sqrt(3)] * 2, color="black", lw=0.9)
    _ax.text(-0.14, math.sqrt(3), r"$\sqrt{3}$", fontsize=12, ha="right", va="center")
    _ax.text(-0.14, -0.14, "$0$", fontsize=12, ha="right", va="top")
    lk.arrow(_ax, (0, 0), (3, 0), lk.BLUE)
    lk.arrow(_ax, (0, 0), (1, math.sqrt(3)), lk.RED)
    _ax.text(2.2, 0.14, r"$\vec{x}$", color=lk.BLUE, fontsize=13, ha="center", va="bottom")
    _ax.text(0.38, 1.1, r"$\vec{y}$", color=lk.RED, fontsize=13, ha="right", va="center")
    _ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=0, theta2=60, color=lk.GREEN, lw=1.4))
    _ax.text(0.68, 0.34, r"$\theta = \pi/3$", color=lk.GREEN, fontsize=12, ha="left", va="center")

    lk.example(
        [
            r"$\vec{x} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}, \quad \vec{y} = \begin{bmatrix} 1 \\ \sqrt{3} \end{bmatrix}$",
            r"""
            $$
            \begin{aligned}
            \lVert \vec{x} \rVert &= \sqrt{(3)^2 + (0)^2} = 3\\[4pt]
            \lVert \vec{y} \rVert &= \sqrt{(1)^2 + (\sqrt{3})^2} = 2\\[4pt]
            \vec{x} \cdot \vec{y} &= 3 \cdot 1 + 0 \cdot \sqrt{3} = 3\\[4pt]
            \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert \lVert \vec{y} \rVert} &= \frac{1}{2} = \cos(\pi/3)
            \end{aligned}
            $$
            """,
            lk.figure(_fig),
        ],
        label="ex-angle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cauchy-schwarz
    # theorem: Cauchy–Schwarz inequality
    lk.theorem(
        [
            r"For every $\vec{x}, \vec{y} \in \mathbb{R}^n$",
            r"$$ (\vec{x} \cdot \vec{y})^2 \leq \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2 $$",
            r"with “$=$” iff $\vec{x}, \vec{y}$ are proportional",
        ],
        title="Cauchy-Schwarz inequality",
        label="thm-cauchy-schwarz",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cauchy-schwarz
    # consequence: the angle makes sense
    lk.prose(
        lk.aside(
            r"$$ \Longrightarrow \quad \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert \lVert \vec{y} \rVert} \in [-1, 1] \quad \forall\, \vec{x}, \vec{y} \neq \vec{0} $$",
            "our definition of angles really makes sense!",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cauchy-schwarz
    # proof
    _g = r"<span class='lk-ghost'>ii) &nbsp; $\lVert t\vec{x} + \vec{y} \rVert^2$</span>"
    lk.proof(
        [
            r"if $\vec{x} = \vec{0}$ or $\vec{y} = \vec{0}$ &nbsp; $\Longrightarrow$ &nbsp; $(\vec{x} \cdot \vec{y})^2 = 0 = \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2$",
            r"assume both $\vec{x}, \vec{y} \neq \vec{0}$ and compute $\lVert t\vec{x} + \vec{y} \rVert^2$ for $t \in \mathbb{R}$",
            r"> i) &nbsp; positive definite implies",
            lk.aside(
                r"$$ \lVert t\vec{x} + \vec{y} \rVert^2 \geq 0, \quad \text{with “$=$” iff } \mk{t\vec{x} + \vec{y} = \vec{0}} $$",
                r"$t\vec{x} + \vec{y} = \vec{0}$: $\vec{x}, \vec{y}$ proportional",
            ),
            r"> ii) &nbsp; $\lVert t\vec{x} + \vec{y} \rVert^2 = (t\vec{x} + \vec{y}) \cdot (t\vec{x} + \vec{y})$",
            r"> " + _g + r" $= t^2 \, \vec{x} \cdot \vec{x} + t \, \vec{x} \cdot \vec{y} + t \, \vec{y} \cdot \vec{x} + \vec{y} \cdot \vec{y}$",
            lk.aside(r"> " + _g + r" $= \mk{t^2 \lVert \vec{x} \rVert^2 + 2t \, \vec{x} \cdot \vec{y} + \lVert \vec{y} \rVert^2}$", r"quadratic polynomial in $t$"),
            r"> > $\Longrightarrow$ &nbsp; $t^2 \lVert \vec{x} \rVert^2 + 2t \, (\vec{x} \cdot \vec{y}) + \lVert \vec{y} \rVert^2 \geq 0$",
            r"> > > $\Longrightarrow$ &nbsp; discriminant: &nbsp; $\big( 2 (\vec{x} \cdot \vec{y}) \big)^2 - 4 \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2 \leq 0$",
            lk.aside(
                r"> > > > $\Longleftrightarrow$ &nbsp; $(\vec{x} \cdot \vec{y})^2 \leq \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2$",
                r"“$=$” iff $\vec{x}, \vec{y}$ proportional",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, np, x, x1, x2, y, y1, y2):
    # module: cauchy-schwarz
    # illustration: the quadratic polynomial t ↦ ‖t x + y‖², moving with the sliders, with its lowest point
    _xx, _yy, _xy = float(x @ x), float(y @ y), float(x @ y)  # exact for the slider values
    _vertex = -_xy / _xx if _xx > 0 else 0.0
    _t = np.sort(np.append(np.linspace(min(-4, _vertex - 2), max(4, _vertex + 2), 400), _vertex))
    _p = _t**2 * _xx + 2 * _t * _xy + _yy
    _fig = Figure(figsize=(3.4, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_t, _p, color=lk.BLUE, lw=1.6)
    _ax.plot(_vertex, float(_p.min()), "o", color=lk.GREEN, ms=5, zorder=4)
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.grid(True, color=lk.LIGHT, lw=0.6)
    _ax.set_axisbelow(True)
    _upper = max(30.0, 1.25 * float(_p.min()) + 2)
    _ax.set_ylim(-0.05 * _upper, _upper)
    _ax.set_xlabel("$t$")
    _ax.set_ylabel(r"$\Vert t\vec{x} + \vec{y} \Vert^2$")  # mathtext has no \lVert
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    lk.prose(lk.interactive(_fig, controls=[(x1, x2), (y1, y2)]))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: triangle inequality
    # theorem: triangle inequality
    lk.theorem(
        [
            r"For every $\vec{x}, \vec{y} \in \mathbb{R}^n$",
            r"$$ \lVert \vec{x} + \vec{y} \rVert \leq \lVert \vec{x} \rVert + \lVert \vec{y} \rVert $$",
        ],
        title="triangle inequality",
        label="thm-triangle",
    )
    return


@app.cell(hide_code=True)
def _(lk, np, plane, vector, x, x1, x2, y, y1, y2):
    # module: triangle inequality
    # consequence and illustration: x, y, x + y and y translated to the tip of x, moving with the sliders
    _s = x + y
    _small = max(abs(x).max(), abs(y).max(), abs(_s).max()) <= 4
    _fig, _ax = plane(4.6, range(-4, 5, 2), size=3.4) if _small else plane(8.6, range(-8, 9, 4), size=3.4)  # the frame follows the vectors
    vector(_ax, tuple(x), tuple(_s), lk.RED, linestyle=(0, (4, 3)))
    vector(_ax, (0, 0), tuple(_s), lk.GREEN, r"$\vec{x} + \vec{y}$")
    vector(_ax, (0, 0), tuple(x), lk.BLUE, r"$\vec{x}$", away=tuple(y))
    vector(_ax, (0, 0), tuple(y), lk.RED, r"$\vec{y}$", away=tuple(x))
    if y.any():
        # "y translated" beside the middle of the dashed copy of y, on the side away from the origin
        _m, _n = x + y / 2, np.array([-y[1], y[0]]) / np.hypot(*y)
        _n = _n if _n @ _m >= 0 else -_n
        _ax.annotate(r"$\vec{y}$ translated", tuple(_m), textcoords="offset points", xytext=tuple(12 * _n), color=lk.RED, fontsize=12,
                     ha="left" if _n[0] > 0.3 else "right" if _n[0] < -0.3 else "center", va="bottom" if _n[1] > 0.3 else "top" if _n[1] < -0.3 else "center")
    lk.prose(
        r"$\leadsto$ &nbsp; proof is direct consequence of the Cauchy-Schwarz! &nbsp; (exercise)",
        lk.interactive(_fig, controls=[(x1, x2), (y1, y2)]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: orthogonality
    # definition: orthogonal vectors
    lk.definition(
        [
            r"$\vec{x}, \vec{y} \in \mathbb{R}^n$ are called **orthogonal** ($\vec{x} \perp \vec{y}$)",
            r"when &nbsp; $\vec{x} \cdot \vec{y} = 0$ &nbsp; $\Longrightarrow$ &nbsp; $\theta(\vec{x}, \vec{y}) = \arccos(0) = \pi/2 = 90^\circ$",
        ],
        label="def-orthogonal",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: orthogonality
    # theorem: at most n pairwise orthogonal vectors
    lk.theorem(
        [
            r"In $\mathbb{R}^n$, we can find at most $n$ non-zero vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$ which are pairwise orthogonal",
            r"$$ \vec{e}_i \cdot \vec{e}_j = 0 \quad \forall\, i \neq j $$",
        ],
        label="thm-at-most-n",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: orthogonality
    # proof
    lk.proof(
        [
            lk.aside(
                r"$\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \ \dots, \ \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}$",
                r"a specific example of $n$ pairwise orthogonal vectors<br>many other examples exist!",
            ),
            r"> $\Longrightarrow$ &nbsp; pairwise orthogonal",
            r"Take any other non-zero vector &nbsp; $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \neq \vec{0}$",
            r"Note that",
            r"$$ \vec{x} \cdot \vec{e}_1 = x^1, \ \ \vec{x} \cdot \vec{e}_2 = x^2, \ \ \dots, \ \ \vec{x} \cdot \vec{e}_n = x^n, $$",
            r"so $\vec{x} \perp \vec{e}_i$ iff $x^i = 0$",
            r"If $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n, \vec{x}$ were pairwise orthogonal then $\vec{x}$ would have to be the zero vector $\vec{0}$.",
            r"This contradicts our assumption that $\vec{x} \neq \vec{0}$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: orthogonality
    # remark after the proof: any orthogonal set works
    lk.prose(
        r"$\leadsto$ &nbsp; here I am using specific vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$ but the argument also works for any set of $n$ non-zero pairwise orthogonal vectors!"
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # definition: orthogonal basis, standard basis vectors
    lk.definition(
        [
            r"A set of $n$ non-zero pairwise orthogonal vectors is called an **orthogonal basis** of $\mathbb{R}^n$.",
            r"The vectors $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \ \dots, \ \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}$ used above",
            lk.aside(
                r"are called the <span class='lk-mark'>**standard basis vectors**</span> of $\mathbb{R}^n$.",
                r"they have the additional property of having unit length<br>$\leadsto$ unit vectors",
            ),
        ],
        label="def-standard-basis",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # consequence
    lk.prose(r"$\leadsto$ &nbsp; more importantly: &nbsp; $\vec{x} \cdot \vec{e}_i = x^i \quad \forall\, \vec{x} \in \mathbb{R}^n$")
    return


@app.cell(hide_code=True)
def _(blank, lk):
    # module: standard basis
    # example: the standard basis of R^2 and R^3, each with its sketch
    _fig, _ax = blank(2.4, 2.1, (-0.7, 2.1), (-0.8, 1.9))
    lk.arrow(_ax, (-0.6, 0), (1.9, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.6), (0, 1.8), "black", lw=0.9)
    lk.arrow(_ax, (0, 0), (1, 0), lk.BLUE)
    lk.arrow(_ax, (0, 0), (0, 1), lk.BLUE)
    _ax.text(0.55, -0.14, r"$\vec{e}_1$", color=lk.BLUE, fontsize=13, ha="center", va="top")
    _ax.text(-0.14, 0.55, r"$\vec{e}_2$", color=lk.BLUE, fontsize=13, ha="right", va="center")

    # each axis is left out from the origin to the tip of e_i, so that the axis never covers the arrow
    _space = lk.turntable(
        30,
        22,
        "the standard basis vectors e1, e2, e3 of R3, along the three coordinate axes",
        [
            lk.panel(
                1.0,
                lines=[([-0.5, 0], [0, 0], [0, 0], "#000000", 1.1), ([0, 0], [-0.6, 0], [0, 0], "#000000", 1.1), ([0, 0], [0, 0], [-0.6, 0], "#000000", 1.1)],
                arrows=[((1, 0, 0), (1.9, 0, 0), "#000000", 1.1), ((0, 1, 0), (0, 1.9, 0), "#000000", 1.1), ((0, 0, 1), (0, 0, 1.9), "#000000", 1.1)]
                + [((0, 0, 0), (1, 0, 0), lk.BLUE), ((0, 0, 0), (0, 1, 0), lk.BLUE), ((0, 0, 0), (0, 0, 1), lk.BLUE)],
                texts=[((0.55, 0, 0), r"\vec{e}_1", lk.BLUE, -60), ((0, 0.55, 0), r"\vec{e}_2", lk.BLUE, -90), ((0, 0, 0.55), r"\vec{e}_3", lk.BLUE, 0)],
            )
        ],
        height=lk.H3D_FLAT,
    )

    lk.example(
        [
            r"$\mathbb{R}^2$ &nbsp; $\leadsto$ &nbsp; $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$",
            r"""
            $$
            \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \quad \Longrightarrow \quad \begin{cases} \vec{x} \cdot \vec{e}_1 = (x^1) \cdot (1) + (x^2) \cdot (0) = x^1 \\ \vec{x} \cdot \vec{e}_2 = (x^1) \cdot (0) + (x^2) \cdot (1) = x^2 \end{cases}
            $$
            """,
            lk.figure(_fig),
            lk.gap(),
            r"$\mathbb{R}^3$ &nbsp; $\leadsto$ &nbsp; $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \ \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$",
            r"""
            $$
            \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \quad \Longrightarrow \quad \begin{cases} \vec{x} \cdot \vec{e}_1 = x^1 \\ \vec{x} \cdot \vec{e}_2 = x^2 \\ \vec{x} \cdot \vec{e}_3 = x^3 \end{cases}
            $$
            """,
            lk.figure(_space),
        ],
        label="ex-standard-basis",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # consequences: coordinate axes and components
    lk.prose(
        r"$\leadsto$ &nbsp; the standard basis vectors define the coordinate axes on $\mathbb{R}^n$!",
        r"$\leadsto$ &nbsp; coordinates / components of a vector are its dot products with the standard basis vectors!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # theorem: components as coefficients
    lk.theorem(
        r"Every $\vec{x} \in \mathbb{R}^n$ is a linear combination of the standard basis vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$, with coefficients $x^1 = \vec{x} \cdot \vec{e}_1, \ x^2 = \vec{x} \cdot \vec{e}_2, \ \dots, \ x^n = \vec{x} \cdot \vec{e}_n$",
        label="thm-components",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard basis
    # proof (for n = 3)
    lk.proof(
        r"""
        $$
        \begin{aligned}
        \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} &= \begin{bmatrix} x^1 \\ 0 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ x^2 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ x^3 \end{bmatrix}\\[6pt]
        &= x^1 \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} + x^3 \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}\\[6pt]
        &= x^1 \vec{e}_1 + x^2 \vec{e}_2 + x^3 \vec{e}_3 \qquad \text{and} \qquad \begin{cases} x^1 = \vec{x} \cdot \vec{e}_1 \\ x^2 = \vec{x} \cdot \vec{e}_2 \\ x^3 = \vec{x} \cdot \vec{e}_3 \end{cases}
        \end{aligned}
        $$
        """,
        title="for $n = 3$",
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
    # exercise: computing with two vectors
    lk.exercise(
        [
            r"Let $\vec{x} = \begin{bmatrix} 1 \\ -2 \\ 2 \end{bmatrix}, \ \vec{y} = \begin{bmatrix} 2 \\ 1 \\ 1 \end{bmatrix}$",
            r"a) Compute $2\vec{x} - \vec{y}$",
            r"b) Compute $\vec{x} \cdot \vec{y}$, $\lVert \vec{x} \rVert$, $\lVert \vec{y} \rVert$",
            r"c) Find the angle between $\vec{x}$ and $\vec{y}$",
        ],
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: orthogonal vectors
    lk.exercise(
        [
            r"Consider $\vec{u} = \begin{bmatrix} 1 \\ 2 \\ -1 \end{bmatrix}, \ \vec{v} = \begin{bmatrix} 2 \\ a \\ 4 \end{bmatrix}$",
            r"a) Find $a \in \mathbb{R}$ so that $\vec{u} \perp \vec{v}$",
            r"b) For this value of $a$, compute $\lVert \vec{u} + \vec{v} \rVert$",
            r"c) Check that $\lVert \vec{u} + \vec{v} \rVert^2 = \lVert \vec{u} \rVert^2 + \lVert \vec{v} \rVert^2$",
        ],
        label="ex-practice-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: an orthogonal basis of R^3
    lk.exercise(
        [
            r"Consider $\vec{u} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \ \vec{v} = \begin{bmatrix} 1 \\ -1 \\ 0 \end{bmatrix}, \ \vec{w} = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$",
            r"a) Show that $\vec{u}, \vec{v}, \vec{w}$ are pairwise orthogonal",
            r"b) Write $\vec{x} = \begin{bmatrix} 3 \\ 1 \\ 4 \end{bmatrix}$ in the form $\vec{x} = a\vec{u} + b\vec{v} + c\vec{w}$",
            r"c) Show that $a = \dfrac{\vec{x} \cdot \vec{u}}{\vec{u} \cdot \vec{u}}, \ b = \dfrac{\vec{x} \cdot \vec{v}}{\vec{v} \cdot \vec{v}}, \ c = \dfrac{\vec{x} \cdot \vec{w}}{\vec{w} \cdot \vec{w}}$",
            r"d) Show that there is no non-zero vector $\vec{y} = \begin{bmatrix} p \\ q \\ r \end{bmatrix}$ orthogonal to $\vec{u}$, $\vec{v}$ and $\vec{w}$ at the same time.",
        ],
        label="ex-practice-3",
    )
    return


if __name__ == "__main__":
    app.run()
