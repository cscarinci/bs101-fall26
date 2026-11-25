import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 15 · Global extrema on closed and bounded domains", css_file="lecturekit/style.css")


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
    lk.lecture(15, "Global extrema on closed and bounded domains")
    return


@app.cell(hide_code=True)
def _(lk, math):
    # Helpers of this lecture: bare coordinate axes and names beside points

    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr."""
        lk.arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        lk.arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    def tip_label(ax, at, angle, text, color, r=7, fontsize=13):
        """A name next to the point `at`, pushed away from it in the direction `angle` (degrees);
        anchored on the side facing the point, so that long names never run back over it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ha = "left" if c > 0.35 else "right" if c < -0.35 else "center"
        va = "bottom" if s > 0.35 else "top" if s < -0.35 else "center"
        ax.annotate(text, at, textcoords="offset points", xytext=(r * c, r * s), ha=ha, va=va, color=color, fontsize=fontsize, zorder=6)

    BOX = {"boxstyle": "round,pad=0.1", "facecolor": "none", "edgecolor": "none"}  # no background: labels sit on fills too
    return BOX, cross_axes, tip_label


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    ga1 = lk.slider(0.05, 1, step=0.05, value=0.55, label="$a^1$")
    ga2 = lk.slider(0.05, 1, step=0.05, value=0.75, label="$a^2$")
    gx = lk.slider(0.05, 1, step=0.05, value=0.35, label=r"$\vec{x}$", show_value=False)
    bp1 = lk.slider(-0.3, 1.3, step=0.05, value=0.6, label="$p^1$")
    bp2 = lk.slider(-0.3, 1.3, step=0.05, value=0.8, label="$p^2$")
    br = lk.slider(0.05, 0.4, step=0.05, value=0.2, label="$r$")
    st = lk.slider(0, 24, step=1, value=4, label="$k$")
    pt = lk.slider(-1, 1, step=0.05, value=-0.6, label="$t$")
    return bp1, bp2, br, ga1, ga2, gx, pt, st


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        "Local extrema via 2nd derivative test",
        lk.gap(),
        r"If $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is $C^2$-smooth at a critical point $\vec{x} = \vec{a}$ &nbsp; $\big( \vec{\nabla} f(\vec{a}) = \vec{0} \big)$",
        lk.aside(
            r"> • &nbsp; if $Hf(\vec{a})$ is <span class='lk-mark'>negative definite</span>, then $\vec{a}$ is local max",
            r"$\det Hf(\vec{a}) > 0$ and $\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) < 0$",
        ),
        lk.aside(
            r"> • &nbsp; if $Hf(\vec{a})$ is <span class='lk-mark'>positive definite</span>, then $\vec{a}$ is local min",
            r"$\det Hf(\vec{a}) > 0$ and $\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) > 0$",
        ),
        lk.aside(
            r"> • &nbsp; if $Hf(\vec{a})$ is <span class='lk-mark'>indefinite</span>, then $\vec{a}$ is a saddle point",
            r"$\det Hf(\vec{a}) < 0$",
        ),
        lk.aside(
            r"> • &nbsp; if $Hf(\vec{a})$ is <span class='lk-mark'>degenerate</span>, we <span class='lk-mark'>need more info</span>",
            r"$\det Hf(\vec{a}) = 0$",
        ),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: recap
    # figure scene: graph of the example
    def _f(x1, x2):
        return x1**2 * np.exp(-(x1**2)) + x2**2

    _L, _W = 2.2, 0.7
    _u1, _u2 = np.meshgrid(np.linspace(-_L, _L, 89), np.linspace(-_W, _W, 29), indexing="ij")
    _s1, _s2 = np.linspace(-_L, _L, 177), np.linspace(-_W, _W, 57)
    _edges = [(_s1, np.full_like(_s1, _k), _f(_s1, _k), lk.BLUE, 1.4) for _k in (-_W, _W)]
    _edges += [(np.full_like(_s2, _k), _s2, _f(_k, _s2), lk.BLUE, 1.4) for _k in (-_L, _L)]
    lk.turntable(
        -70,
        42,
        "graph of f with its two saddle points and its global minimum",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_u1, _u2, _f(_u1, _u2), wire=[(0, 8, lk.BLUE, 0.6), (1, 4, lk.BLUE, 0.6)])],
                lines=_edges + [(_s1, 0 * _s1, _f(_s1, 0), lk.BLUE, 2.0)],
                points=[((-1, 0, _f(-1, 0)), lk.ORANGE), ((1, 0, _f(1, 0)), lk.ORANGE), ((0, 0, 0), lk.GREEN)],
                axes=[((-2.35, 0, 0), (2.6, 0, 0), "x^1", -60), ((0, 0, 0), (0, 1.6, 0), "x^2", 0), ((0, 0, 0), (0, 0, 1.15), "y", 90)],
                texts=[((-1, 0, _f(-1, 0)), r"\vec{a}", "black", 90, 7), ((1, 0, _f(1, 0)), r"\vec{b}", "black", 90, 7), ((0, 0, 0), r"\vec{0}", "black", 30, 12)],                box=((-2.3, 2.3), (-0.75, 0.75), (0, 0.9)),
            )
        ],
        height=lk.H3D,
        width=500,
        key="L15-hess",
        apart=True,
        zoom=1.5,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # example: second derivative test
    lk.example(
        [
            r"""
            $f\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 e^{-(x^1)^2} + (x^2)^2$

            > $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 e^{-(x^1)^2} - 2(x^1)^3 e^{-(x^1)^2} \\ 2x^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$

            > > $\Longleftrightarrow$ &nbsp; $x^2 = 0$, &nbsp; $x^1 \big( 1 - (x^1)^2 \big) e^{-(x^1)^2} = 0$

            > > $\Longleftrightarrow$ &nbsp; $x^2 = 0$, &nbsp; $x^1 \in \{ -1, 0, 1 \}$

            > $Hf(\vec{x}) = \begin{bmatrix} \big( 4(x^1)^4 - 10(x^1)^2 + 2 \big) e^{-(x^1)^2} & 0 \\ 0 & 2 \end{bmatrix}$
            """,
            lk.aside(
                r"> at $\vec{a} = \begin{bmatrix} -1 \\ 0 \end{bmatrix}$ and $\vec{b} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$: &nbsp; $Hf(\vec{a}) = Hf(\vec{b}) = \begin{bmatrix} -4e^{-1} & 0 \\ 0 & 2 \end{bmatrix}$",
                r"indefinite $\Longrightarrow$ saddle",
            ),
            lk.aside(
                r"> at $\vec{0} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$: &nbsp; $Hf(\vec{0}) = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}$",
                r"positive definite $\Longrightarrow$ minimum",
            ),
            r"""
            $\leadsto$ &nbsp; global minimum: &nbsp; $f(\vec{0}) = 0 < f(\vec{x}) \quad \forall \, \vec{x} \neq \vec{0}$
            """,
            lk.figure(lk.frame("L15-hess", lk.H3D, width=500)),
        ],
        label="ex-hessian",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Global extrema", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 3.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: global extrema
    # section
    lk.section("Global extrema on closed and bounded domains")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: global extrema
    # definition: global maximum and minimum
    lk.definition(
        r"""
        Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, a point $\vec{a} \in D$ is

        > • &nbsp; a **global maximum** of $f$ if

        $$
        f(\vec{x}) \leqslant f(\vec{a}) \qquad \forall \, \vec{x} \in D
        $$

        > • &nbsp; a **global minimum** of $f$ if

        $$
        f(\vec{x}) \geqslant f(\vec{a}) \qquad \forall \, \vec{x} \in D
        $$
        """,
        label="def-global",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: global extrema
    # prose: the domain matters
    lk.prose(r"$\leadsto$ &nbsp; to determine global extrema, we also need to look at properties of the domain of $f$!")
    return


@app.cell(hide_code=True)
def _(ga1, ga2, gx, lk, np):
    # module: global extrema
    # figure scene: graph of g over D = (0, 1] x (0, 1], with the graph of f over the plane in a faint tone
    def _f(x1, x2):
        return x1**2 + x2**2

    _a = (round(ga1.value, 10), round(ga2.value, 10))
    _e = (_a[0] / max(_a), _a[1] / max(_a))
    _x = (gx.value * _e[0], gx.value * _e[1])
    _R = 1.5
    _r, _p = np.meshgrid(np.linspace(0, _R, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _b1, _b2 = np.meshgrid(np.linspace(0, 1, 11), np.linspace(0, 1, 11), indexing="ij")
    _s = np.linspace(0, 1, 41)
    _z, _o = 0 * _s, 1 + 0 * _s
    _phi = np.linspace(0, 2 * np.pi, 241)
    _dash, _faint = [4, 3], "#c4c4c4"
    _lines = [(_R * np.cos(_phi), _R * np.sin(_phi), _R**2 + 0 * _phi, _faint, 1.0)]
    for _k in (0.25, 0.5, 0.75):
        _lines += [(_k + _z, _s, _f(_k, _s), lk.BLUE, 0.8), (_s, _k + _z, _f(_s, _k), lk.BLUE, 0.8)]
    _lines += [(_o, _s, _f(1, _s), lk.BLUE, 1.6), (_s, _o, _f(_s, 1), lk.BLUE, 1.6)]
    _lines += [(_z, _s, _f(0, _s), lk.BLUE, 1.6, _dash), (_s, _z, _f(_s, 0), lk.BLUE, 1.6, _dash)]
    # D in the plane: its edges on the axes dashed, on white bands drawn over the axes
    _lines += [(_o, _s, _z, lk.BLUE, 1.6), (_s, _o, _z, lk.BLUE, 1.6)]
    _lines += [(_z, _s, _z, "#ffffff", 4.5, None, 0.01), (_s, _z, _z, "#ffffff", 4.5, None, 0.01)]
    _lines += [(_z, _s, _z, lk.BLUE, 1.6, _dash, 0.02), (_s, _z, _z, lk.BLUE, 1.6, _dash, 0.02)]
    # the line from 0 through a in D and on the graph, with a and x below their values
    _lines += [(_s * _e[0], _s * _e[1], 0 * _s, lk.GREY, 1.2, _dash, 0.02), (_s * _e[0], _s * _e[1], _f(_s * _e[0], _s * _e[1]), lk.GREY, 1.6, _dash, 0.02)]
    for _q in (_a, _x):
        _lines += [(_q[0] + 0 * _s, _q[1] + 0 * _s, _s * _f(*_q), lk.GREY, 0.8, [1, 2])]
    _open = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1)]
    lk.turntable(
        20,
        23,
        "graph of g over D, with the graph of f over the plane in a faint tone, and the global maximum of g",
        [
            lk.panel(
                0.55,
                surfaces=[
                    lk.sheet(_r * np.cos(_p), _r * np.sin(_p), _f(_r * np.cos(_p), _r * np.sin(_p)), wire=[(0, 4, _faint, 0.5), (1, 8, _faint, 0.5)], tint=(0, 1, 0, 1), clear=True, alpha=0.3),
                    lk.sheet(_b1, _b2, 0 * _b1, flat=lk.LIGHT),
                ],
                lines=_lines,
                points=[(_q, lk.BLUE, 3.6, True) for _q in _open] + [((1, 1, 0), lk.BLUE, 3.6), ((1, 1, 2), lk.RED)]
                + [((*_a, 0), lk.RED, 4.5), ((*_a, _f(*_a)), lk.RED, 4.5), ((*_x, 0), lk.ORANGE, 4.5), ((*_x, _f(*_x)), lk.ORANGE, 4.5)],
                axes=[((0, 0, 0), (1.75, 0, 0), "x^1", -150), ((0, 0, 0), (0, 1.75, 0), "x^2", -30), ((0, 0, 0), (0, 0, 2.6), "y", 90)],
                texts=[
                    ((0.5, 1, _f(0.5, 1)), r"y = g(\vec{x})", lk.BLUE, 40, 10),
                    ((_R * np.cos(-2.1), _R * np.sin(-2.1), _R**2), r"y = f(\vec{x})", "#6b6b6b", 150, 6),
                    ((1, 0.5, 0), "D", lk.BLUE, -120, 6),
                    ((1, 1, 2), r"g\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right) = 2", "black", 100, 10),
                ],
            )
        ],
        height=lk.H3D,
        width=420,
        key="L15-g",
        apart=True,
        zoom=1.3,
    )
    return


@app.cell(hide_code=True)
def _(BOX, Figure, cross_axes, ga1, ga2, gx, lk, mo, tip_label):
    # module: global extrema
    # example: f over the plane, g over (0, 1] x (0, 1]
    # D = (0, 1] x (0, 1] with its edges on the axes dashed, a in D, the line from 0 through a, and x on it
    _fig = Figure(figsize=(lk.HALF - 0.6, 2.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.2, 1.45)
    _ax.set_ylim(-0.2, 1.35)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.15, 1.4), (-0.15, 1.3), "$x^1$", "$x^2$")
    _ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot([1, 1, 0], [0, 1, 1], color=lk.BLUE, lw=1.4, zorder=4)
    _ax.plot([0, 0, 1], [1, 0, 0], color="white", lw=4, zorder=4)
    _ax.plot([0, 0, 1], [1, 0, 0], color=lk.BLUE, lw=1.4, ls=(0, (3, 2)), zorder=5)
    for _c in ((0, 0), (1, 0), (0, 1)):
        _ax.plot(*_c, "o", ms=5, mfc="white", mec=lk.BLUE, mew=1.2, zorder=6)
    _ax.plot(1, 1, "o", ms=5, color=lk.BLUE, zorder=6)
    _a = (round(ga1.value, 10), round(ga2.value, 10))
    _e = (_a[0] / max(_a), _a[1] / max(_a))
    _x = (gx.value * _e[0], gx.value * _e[1])
    _ax.plot([0, _e[0]], [0, _e[1]], color=lk.GREY, lw=0.9, ls=(0, (4, 3)), zorder=1)
    _ax.plot(*_a, "o", color=lk.RED, ms=5, zorder=6)
    _ax.plot(*_x, "o", color=lk.ORANGE, ms=5, zorder=6)
    _ax.text(1, -0.05, "$1$", ha="center", va="top", fontsize=12, bbox=BOX)
    _ax.text(-0.05, 1, "$1$", ha="right", va="center", fontsize=12, bbox=BOX)
    _ax.text(1.1, 0.5, "$D$", ha="left", va="center", color=lk.BLUE, fontsize=13)
    tip_label(_ax, _a, 0, r"$\vec{a}$", "black", r=5)
    tip_label(_ax, _x, 180, r"$\vec{x}$", "black", r=5)
    lk.example(
        [
            r"""
            $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $f\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 + (x^2)^2$

            > $\Longrightarrow$ &nbsp; $\begin{bmatrix} 0 \\ 0 \end{bmatrix}$ is global minimum and there is no global maximum
            """,
            lk.gap(),
            r"""
            $g : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $g\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 + (x^2)^2$ &nbsp; for $D = \Big\{ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\Big|\; 0 < x^1 \leqslant 1, \ 0 < x^2 \leqslant 1 \Big\}$

            > $\Longrightarrow$ &nbsp; there is no global minimum

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp;</span>$\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ is the global maximum!
            """,
            lk.gap(),
            r"""
            Starting from any $\vec{a} \in D$,

            > • &nbsp; can make $g(\vec{x}) < g(\vec{a})$ moving towards $\vec{0}$, but never reach $g(\vec{x}) = 0$ since $\vec{0} \notin D$

            > > $\Longrightarrow$ &nbsp; no $\vec{a} \in D$ can be a minimum!

            > • &nbsp; can make $g(\vec{x}) > g(\vec{a})$ moving away from $\vec{0}$, unless $a^1 = 1$ or $a^2 = 1$

            > • &nbsp; if $a^2 = 1$, can make $g(\vec{x}) > g(\vec{a})$ moving right, unless $a^1 = 1$

            > > $\Longrightarrow$ &nbsp; $\vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix} \in D$ is the maximum!
            """,
            lk.interactive(mo.Html('<div class="lk-pair">' f'<div>{mo.as_html(_fig).text}</div><div class="lk-pair-3d">{lk.frame("L15-g", lk.H3D, width=420).text}</div></div>'), controls=[ga1, ga2, gx]),
        ],
        label="ex-f-g",
    )
    return


@app.cell(hide_code=True)
def _(BOX, Figure, cross_axes, lk, np):
    # module: domains
    # definition: bounded and unbounded
    # left: the rectangle 0 <= x^1 <= a, 0 <= x^2 <= b inside B(0, r); right: the strip a <= x^2 <= b leaves every
    # ball
    _th = np.linspace(0, 2 * np.pi, 241)
    _fig = Figure(figsize=(lk.FULL - 0.6, 2.5), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax in (_left, _right):
        _ax.set_xlim(-2.3, 2.3)
        _ax.set_ylim(-1.6, 2.0)
        _ax.set_aspect("equal")
        _ax.axis("off")
    _a, _b, _r = 1.2, 0.8, 1.55
    _left.fill(_r * np.cos(_th), _r * np.sin(_th), color=lk.RED, alpha=0.06, lw=0)
    _left.plot(_r * np.cos(_th), _r * np.sin(_th), color=lk.RED, lw=1.2)
    _left.fill([0, _a, _a, 0], [0, 0, _b, _b], color=lk.LIGHT, lw=0)
    _left.plot([0, _a, _a, 0, 0], [0, 0, _b, _b, 0], color=lk.BLUE, lw=1.4)
    cross_axes(_left, (-2.0, 2.2), (-1.5, 1.95), "$x^1$", "$x^2$")
    _left.text(_a, -0.06, "$a$", ha="center", va="top", fontsize=12, bbox=BOX)
    _left.text(-0.06, _b, "$b$", ha="right", va="center", fontsize=12, bbox=BOX)
    _left.text(_a / 2, _b / 2, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _left.text(_r * np.cos(-0.7) + 0.05, _r * np.sin(-0.7) - 0.05, r"$B(\vec{0}, r)$", color=lk.RED, fontsize=12, ha="left", va="top")
    _a, _b, _r = 0.4, 1.0, 1.3
    _right.fill([-2.3, 2.3, 2.3, -2.3], [_a, _a, _b, _b], color=lk.LIGHT, lw=0)
    for _h in (_a, _b):
        _right.plot([-2.3, 2.3], [_h, _h], color=lk.BLUE, lw=1.4)
    _right.fill(_r * np.cos(_th), _r * np.sin(_th), color=lk.RED, alpha=0.06, lw=0)
    _right.plot(_r * np.cos(_th), _r * np.sin(_th), color=lk.RED, lw=1.2)
    cross_axes(_right, (-2.25, 2.25), (-1.5, 1.95), "$x^1$", "$x^2$")
    _right.text(-0.06, _a, "$a$", ha="right", va="top", fontsize=12, bbox=BOX)
    _right.text(-0.06, _b, "$b$", ha="right", va="bottom", fontsize=12, bbox=BOX)
    _right.text(-2.0, (_a + _b) / 2 - 0.08, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _right.text(_r * np.cos(-0.7) + 0.05, _r * np.sin(-0.7) - 0.05, r"$B(\vec{0}, r)$", color=lk.RED, fontsize=12, ha="left", va="top")
    lk.module(
        lk.definition(
            r"""
            $D \subseteq \mathbb{R}^2$ is called **bounded** if “we cannot take its points to infinity”

            > $\Longleftrightarrow$ &nbsp; it is contained in some ball of finite radius

            > $\Longleftrightarrow$ &nbsp; there exists $B(\vec{0}, r) \supseteq D$

            $D \subseteq \mathbb{R}^2$ is **unbounded** if it cannot be contained in any ball of finite radius
            """,
            label="def-bounded",
        ),
        lk.example(
            [
                r"""
            $D = \{ 0 \leqslant x^1 \leqslant a, \ 0 \leqslant x^2 \leqslant b \}$ is bounded: &nbsp; $B(\vec{0}, r) \supseteq D$ for $r^2 > a^2 + b^2$

            $D = \{ -\infty < x^1 < +\infty, \ a \leqslant x^2 \leqslant b \}$ is unbounded
            """,
                lk.figure(_fig),
            ],
            label="ex-bounded",
        ),
    )
    return


@app.cell(hide_code=True)
def _(Figure, bp1, bp2, br, cross_axes, lk, math, np, tip_label):
    # module: domains
    # definition: boundary
    # the quarter disc D (edges on the axes in D, solid; the arc not in D, dashed) and a ball B(p, r) that the sliders
    # move
    _p = (round(bp1.value, 10) + 0.0, round(bp2.value, 10) + 0.0)
    _r = round(br.value, 10)
    _eps = 1e-9
    _q = (max(_p[0], 0.0), max(_p[1], 0.0))
    _n = math.hypot(*_q)
    if _n > 1:
        _q = (_q[0] / _n, _q[1] / _n)
    _to_D = math.hypot(_p[0] - _q[0], _p[1] - _q[1])
    _in_D = _p[0] > -_eps and _p[1] > -_eps and math.hypot(*_p) < 1 - _eps
    _to_out = min(_p[0], _p[1], 1 - math.hypot(*_p)) if _in_D else 0.0
    _meets_D = _to_D < _r - _eps
    _meets_out = not (_in_D and _r <= _to_out + _eps)
    _on_Bd = _to_D < _eps and not (_in_D and _to_out > _eps)

    def _yes(b):
        return "yes" if b else "no"

    _fig = Figure(figsize=(lk.HALF + 0.4, 2.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.75, 2.3)
    _ax.set_ylim(-0.75, 2.0)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _th = np.linspace(0, np.pi / 2, 120)
    _ax.fill(np.r_[0, np.cos(_th)], np.r_[0, np.sin(_th)], color=lk.LIGHT, lw=0, zorder=0)
    cross_axes(_ax, (-0.7, 2.25), (-0.7, 1.95), "$x^1$", "$x^2$")
    _ax.plot([0, 0, 1], [1, 0, 0], color=lk.BLUE, lw=1.6, zorder=5)
    _ax.plot(np.cos(_th), np.sin(_th), color=lk.BLUE, lw=1.6, ls=(0, (4, 2)), zorder=5)
    for _e in ((1, 0), (0, 1)):
        _ax.plot(*_e, "o", ms=5, mfc="white", mec=lk.BLUE, mew=1.2, zorder=5)
    _c = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_p[0] + _r * np.cos(_c), _p[1] + _r * np.sin(_c), color=lk.RED, alpha=0.12, lw=0, zorder=6)
    _ax.plot(_p[0] + _r * np.cos(_c), _p[1] + _r * np.sin(_c), color=lk.RED, lw=1.2, zorder=6)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=7)
    tip_label(_ax, (_p[0] + _r * math.sqrt(0.5), _p[1] + _r * math.sqrt(0.5)), 45, r"$B(\vec{p}, r)$", lk.RED, r=2, fontsize=12)
    tip_label(_ax, _p, 225, r"$\vec{p}$", "black", r=3, fontsize=12)
    lk.module(
        lk.definition(
            r"""
            Given $D \subseteq \mathbb{R}^2$, the **boundary** of $D$ is the set $\mathrm{Bd}(D)$ of points $\vec{a} \in \mathbb{R}^2$ such that

            > any ball centered at $\vec{a}$ contains both points in $D$ *and* points not in $D$
            """,
            label="def-boundary",
        ),
        lk.example(
            [
                r"""
                $D = \{ -\infty < x^1 < +\infty, \ a \leqslant x^2 \leqslant b \}$

                > $\Longrightarrow$ &nbsp; $\mathrm{Bd}(D) = \{ x^2 = a \} \cup \{ x^2 = b \}$

                $D = \{ x^1 \geqslant 0, \ x^2 \geqslant 0, \ (x^1)^2 + (x^2)^2 < 1 \}$

                > $\Longrightarrow$ &nbsp; $\mathrm{Bd}(D) = \{ x^1 \geqslant 0, \ x^2 \geqslant 0, \ (x^1)^2 + (x^2)^2 = 1 \} \cup \{ 0 \leqslant x^1 \leqslant 1, \ x^2 = 0 \} \cup \{ x^1 = 0, \ 0 \leqslant x^2 \leqslant 1 \}$
                """,
                lk.interactive(
                    _fig,
                    controls=[bp1, bp2, br],
                    readout=lk.table(
                        [
                            (r"$B(\vec{p}, r)$ contains points in $D$", _yes(_meets_D)),
                            (r"$B(\vec{p}, r)$ contains points not in $D$", _yes(_meets_out)),
                            (r"$\vec{p} \in D$", _yes(_in_D)),
                            (r"$\vec{p} \in \mathrm{Bd}(D)$", _yes(_on_Bd)),
                        ]
                    ),
                ),
            ],
            label="ex-boundary",
        ),
    )
    return


@app.cell(hide_code=True)
def _(BOX, Figure, cross_axes, lk, np):
    # module: domains
    # definition: closed
    # the open rectangle, which misses its corner (a, c) of the boundary, and the closed rectangle
    _a, _b, _c, _d = 0.5, 1.7, 0.45, 1.3
    _fig = Figure(figsize=(lk.FULL - 0.6, 2.2), layout="constrained")
    _panels = _fig.subplots(1, 2)
    for _ax, _closed in zip(_panels, (False, True)):
        _ax.set_xlim(-0.3, 2.3)
        _ax.set_ylim(-0.3, 1.65)
        _ax.set_aspect("equal")
        _ax.axis("off")
        cross_axes(_ax, (-0.2, 2.25), (-0.2, 1.6), "$x^1$", "$x^2$")
        _ax.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=lk.LIGHT, lw=0)
        _ax.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=lk.BLUE, lw=1.4, ls="-" if _closed else (0, (3, 2)))
        for _x in (_a, _b):
            for _y in (_c, _d):
                if _closed:
                    _ax.plot(_x, _y, "o", ms=5, color=lk.BLUE, zorder=3)
                else:
                    _ax.plot(_x, _y, "o", ms=5, mfc="white", mec=lk.BLUE, mew=1.2, zorder=3)
        for _x, _name in ((_a, "$a$"), (_b, "$b$")):
            _ax.text(_x, -0.05, _name, ha="center", va="top", fontsize=12, bbox=BOX)
        for _y, _name in ((_c, "$c$"), (_d, "$d$")):
            _ax.text(-0.05, _y, _name, ha="right", va="center", fontsize=12, bbox=BOX)
        _ax.text((_a + _b) / 2, (_c + _d) / 2, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _t = np.linspace(0, 2 * np.pi, 120)
    _panels[0].fill(_a + 0.16 * np.cos(_t), _c + 0.16 * np.sin(_t), color=lk.RED, alpha=0.12, lw=0, zorder=2)
    _panels[0].plot(_a + 0.16 * np.cos(_t), _c + 0.16 * np.sin(_t), color=lk.RED, lw=1.0, zorder=2)
    lk.module(
        lk.definition(
            r"A set $D \subseteq \mathbb{R}^2$ is called **closed** if it contains all of its boundary &nbsp; $\mathrm{Bd}(D) \subset D$",
            label="def-closed",
        ),
        lk.example(
            [
                r"""
            $D = \{ a < x^1 < b, \ c < x^2 < d \}$ is not closed!

            > $\begin{bmatrix} a \\ c \end{bmatrix} \in \mathrm{Bd}(D)$, but $\begin{bmatrix} a \\ c \end{bmatrix} \notin D$ &nbsp; (one missing point is enough!)

            $D = \{ a \leqslant x^1 \leqslant b, \ c \leqslant x^2 \leqslant d \}$ is closed!
            """,
                lk.figure(_fig),
            ],
            label="ex-closed",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: existence
    # theorem: extreme value theorem
    lk.theorem(
        r"""
        If $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a closed and bounded domain $D$,<br>then $f$ must have both points of global maximum and global minimum!
        """,
        label="thm-extreme-value",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: existence
    # prose: might not admit
    lk.prose(r"$\leadsto$ &nbsp; functions defined on unbounded domains or on non-closed domains might not admit any global extrema!")
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, lk):
    # module: existence
    # remark: f, g, h
    # h on the closed square, with its global extrema at the corners
    _fig = Figure(figsize=(lk.HALF - 0.4, 2.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.35, 1.75)
    _ax.set_ylim(-0.35, 1.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.2, 1.5), (-0.2, 1.4), "$x^1$", "$x^2$")
    _ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color=lk.LIGHT, lw=0)
    _ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=lk.BLUE, lw=1.4, zorder=4)
    for _c in ((1, 0), (0, 1)):
        _ax.plot(*_c, "o", ms=5, color=lk.BLUE, zorder=5)
    _ax.plot(0, 0, "o", color=lk.GREEN, ms=6, zorder=5)
    _ax.plot(1, 1, "o", color=lk.RED, ms=6, zorder=5)
    _ax.text(0.5, 0.5, r"$\bar{D}$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _ax.text(0.06, -0.06, r"$h\left(\genfrac{[}{]}{0}{0}{0}{0}\right) = 0$", color="black", fontsize=12, ha="left", va="top")
    _ax.text(1.06, 1.04, r"$h\left(\genfrac{[}{]}{0}{0}{1}{1}\right) = 2$", color="black", fontsize=12, ha="left", va="bottom")
    lk.remark(
        [
            r"""
            $f\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 + (x^2)^2$ over $\mathbb{R}^2$ has no global maximum because $\mathbb{R}^2$ is unbounded

            $g\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 + (x^2)^2$ over $D = (0, 1] \times (0, 1]$ has no global minimum because $D$ is not closed

            $h\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 + (x^2)^2$ over $\bar{D} = [0, 1] \times [0, 1]$ has both global extrema!
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: existence
    # prose: where can the global extrema be?
    lk.prose(
        r"""
        Suppose $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a closed bounded domain $D$.

        How can we find the global extrema?
        """,
        lk.gap(),
        r"""
        If $\vec{a} \in D$ is global extremum:

        > • &nbsp; $\vec{a} \in \mathrm{Bd}(D) \subset D$

        or

        > • &nbsp; $\vec{a} \notin \mathrm{Bd}(D) \subset D$

        > > $\Longrightarrow$ &nbsp; there is some open ball $B(\vec{a}, r)$ which only contains points of $D$

        > > $\Longrightarrow$ &nbsp; there exists $B(\vec{a}, r) \subset D$ with
        """,
        lk.aside(r"> > > $f(\vec{x}) \leqslant f(\vec{a}) \quad \forall \, \vec{x} \in B(\vec{a}, r)$", r"$\vec{a}$ is local maximum"),
        r"> > or",
        lk.aside(r"> > > $f(\vec{x}) \geqslant f(\vec{a}) \quad \forall \, \vec{x} \in B(\vec{a}, r)$", r"$\vec{a}$ is local minimum"),
        r"$\Longrightarrow$ &nbsp; for differentiable functions defined over closed and bounded domains we get a well-defined strategy to find global extrema!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: strategy
    # section
    lk.section("Strategy to find global extrema")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: strategy
    # prose: strategy
    lk.prose(
        lk.aside(r"1\. &nbsp; find critical points on the <span class='lk-mark'>interior</span> $D - \mathrm{Bd}(D)$", "not on the boundary"),
        lk.aside(
            r"2\. &nbsp; find <span class='lk-mark'>global extrema in $\mathrm{Bd}(D)$</span>",
            r"optimization problem in lower dimension<br>$\Longrightarrow$ easier once the boundary is parameterized",
        ),
        r"3\. &nbsp; compare the values of all candidate points",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: strategy
    # figure scene: graph of f over the disc
    def _f(x1, x2):
        return x1**2 + x2**2 - 2 * x1

    _r, _p = np.meshgrid(np.linspace(0, 2, 21), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _q, _w = np.meshgrid(np.linspace(2, 2.6, 7), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _t = np.linspace(0, 2 * np.pi, 241)
    _c1, _c2 = 2 * np.cos(_t), 2 * np.sin(_t)
    _faint = "#c4c4c4"
    lk.turntable(
        -75,
        48,
        "graph of f over the disc D, the same rule outside D in a faint tone, f restricted to the boundary of D, and the three candidates",
        [
            lk.panel(
                0.3,
                surfaces=[
                    lk.sheet(_r * np.cos(_p), _r * np.sin(_p), _f(_r * np.cos(_p), _r * np.sin(_p)), wire=[(0, 5, lk.BLUE, 0.6), (1, 8, lk.BLUE, 0.6)]),
                    lk.sheet(_q * np.cos(_w), _q * np.sin(_w), _f(_q * np.cos(_w), _q * np.sin(_w)), wire=[(0, 6, _faint, 0.5), (1, 8, _faint, 0.5)], alpha=0.3),
                ],
                lines=[(_c1, _c2, _f(_c1, _c2), lk.BLUE, 2.2), (_c1, _c2, 0 * _t, lk.BLUE, 1.0, [4, 3])],
                points=[((1, 0, -1), lk.GREEN), ((2, 0, 0), lk.ORANGE), ((-2, 0, 8), lk.RED)],
                axes=[((0, 0, 0), (2.9, 0, 0), "x^1", -30), ((0, 0, 0), (0, 2.9, 0), "x^2", 30), ((0, 0, 0), (0, 0, 9), "y", 90)],
                texts=[
                    ((1, 0, -1), r"f(\vec{a}) = -1", "black", -90, 7),
                    ((2, 0, 0), r"f(\vec{b}) = 0", "black", 50, 8),
                    ((-2, 0, 8), r"f(\vec{c}) = 8", "black", 180, 7),
                    ((0, -2, 0), r"\mathrm{Bd}(D)", lk.BLUE, -90, 6),
                    ((2**0.5, 2**0.5, _f(2**0.5, 2**0.5)), r"f \text{ restricted to } \mathrm{Bd}(D)", lk.BLUE, -10, 6),
                    ((-0.5, 1.2, _f(-0.5, 1.2)), r"y = f(\vec{x})", lk.BLUE, 180, 4),
                ],
            )
        ],
        height=lk.H3D,
        width=500,
        key="L15-disc",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(BOX, Figure, cross_axes, lk, math, np, st, tip_label):
    # module: strategy
    # example: f on the disc of radius 2
    # left: D with the level sets of f (circles about a), the candidates and the point gamma(t) of Bd(D);
    # right: g(t) = f on Bd(D), with the value of f at the interior candidate
    _t = st.value * math.pi / 12
    _pt = (2 * math.cos(_t), 2 * math.sin(_t))

    def _g(t):
        return 4 - 4 * np.cos(t)

    _fig = Figure(figsize=(lk.FULL, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1, 1.35])
    _left.set_xlim(-2.85, 3.2)
    _left.set_ylim(-2.65, 3.0)
    _left.set_aspect("equal")
    _left.axis("off")
    _th = np.linspace(0, 2 * np.pi, 241)
    _left.fill(2 * np.cos(_th), 2 * np.sin(_th), color=lk.LIGHT, lw=0, zorder=0)
    _disc = _left.fill(2 * np.cos(_th), 2 * np.sin(_th), color="none", lw=0)[0]
    for _c in range(9):
        (_ring,) = _left.plot(1 + math.sqrt(_c + 1) * np.cos(_th), math.sqrt(_c + 1) * np.sin(_th), color=lk.GREY, lw=0.6, zorder=1)
        _ring.set_clip_path(_disc)
    _left.plot(2 * np.cos(_th), 2 * np.sin(_th), color=lk.BLUE, lw=1.4, zorder=2)
    cross_axes(_left, (-2.5, 3.15), (-2.4, 2.95), "$x^1$", "$x^2$")
    for _p, _col in (((1, 0), lk.GREEN), ((2, 0), lk.ORANGE), ((-2, 0), lk.RED)):
        _left.plot(*_p, "o", color=_col, ms=6, zorder=5)
    _left.plot(*_pt, "o", color="black", ms=6, zorder=6)
    for _p, _name, _ang in (((1, 0), r"$\vec{a}$", -90), ((2, 0), r"$\vec{b}$", 135), ((-2, 0), r"$\vec{c}$", 45)):
        tip_label(_left, _p, _ang, _name, "black", r=5)
    _cc, _ss = math.cos(_t), math.sin(_t)
    _d = 24 / 2 * abs(_cc) + 14 / 2 * abs(_ss) + 4
    _left.annotate(r"$\gamma(t)$", _pt, textcoords="offset points", xytext=(_d * _cc, _d * _ss), ha="center", va="center", fontsize=12, zorder=6, bbox=BOX)
    _right.set_xlim(-0.6, 7.6)
    _right.set_ylim(-1.8, 9.2)
    _right.set_aspect(0.55)
    _right.axis("off")
    cross_axes(_right, (-0.4, 7.2), (-1.6, 9.1), "$t$", "$y$")
    _s = np.linspace(0, 2 * math.pi, 300)
    _right.plot(_s, _g(_s), color=lk.BLUE, lw=1.6)
    _right.plot([0, 2 * math.pi], [-1, -1], color=lk.GREEN, lw=1.0, ls=(0, (4, 3)))
    for _x, _name in ((math.pi, r"$\pi$"), (2 * math.pi, r"$2\pi$")):
        _right.plot([_x, _x], [-0.15, 0.15], color="black", lw=0.9)
        _right.text(_x, 0.35, _name, ha="center", va="bottom", fontsize=12, bbox=BOX)
    for _x, _col in ((0, lk.ORANGE), (math.pi, lk.RED), (2 * math.pi, lk.ORANGE)):
        _right.plot(_x, _g(_x), "o", color=_col, ms=6, zorder=5)
    _right.text(7.5, 7.9, r"$y = g(t) = 4 - 4\cos(t)$", color=lk.BLUE, fontsize=12, ha="right", va="center")
    _right.plot(_t, _g(_t), "o", color="black", ms=6, zorder=6)
    _right.text(math.pi, -1.25, r"$y = f(\vec{a}) = -1$", color=lk.GREEN, fontsize=12, ha="center", va="top")
    lk.example(
        [
            r"""
            $f\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^2 + (x^2)^2 - 2x^1$ &nbsp; on &nbsp; $D = \{ (x^1)^2 + (x^2)^2 \leqslant 4 \}$
            """,
            lk.aside(
                r"> $\mathrm{Bd}(D) = \{ (x^1)^2 + (x^2)^2 = 4 \} = \mk{\Big\{ \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \;\Big|\; t \in [0, 2\pi] \Big\}}$",
                r"parameterization of $\mathrm{Bd}(D)$",
            ),
            r"""
            > $D - \mathrm{Bd}(D) = \{ (x^1)^2 + (x^2)^2 < 4 \}$
            """,
            lk.gap(),
            "1\\. &nbsp; Critical points in $D - \\mathrm{Bd}(D)$",
            lk.aside(
                r"> $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 - 2 \\ 2x^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$ &nbsp; $\Longleftrightarrow$ &nbsp; $\begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \mk{\vec{a}}$",
                "interior candidate for global extremum",
            ),
            lk.gap(),
            r"""
            2\. &nbsp; Restrict $f$ to $\mathrm{Bd}(D)$

            > $f\Big( \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \Big) = 4 - 4\cos(t) = g(t)$

            > > $\leadsto$ &nbsp; $g'(t) = 4\sin(t) = 0$ &nbsp; $\Longleftrightarrow$ &nbsp; $t = 0$ or $t = \pi$
            """,
            lk.aside(
                r"> > > $\Longrightarrow$ &nbsp; $\begin{cases} \mk{\vec{b}} = \begin{bmatrix} 2\cos(0) \\ 2\sin(0) \end{bmatrix} = \begin{bmatrix} 2 \\ 0 \end{bmatrix} \\[14pt] \mk{\vec{c}} = \begin{bmatrix} 2\cos(\pi) \\ 2\sin(\pi) \end{bmatrix} = \begin{bmatrix} -2 \\ 0 \end{bmatrix} \end{cases}$",
                "boundary candidates",
            ),
            lk.gap(),
            r"""
            3\. &nbsp; Compare

            > $\underbrace{f(\vec{a}) = -1}_{\text{min}}$, &emsp; $f(\vec{b}) = 0$, &emsp; $\underbrace{f(\vec{c}) = 8}_{\text{max}}$
            """,
            lk.interactive(_fig, controls=[st]),
            lk.figure(lk.frame("L15-disc", lk.H3D, width=500)),
        ],
        label="ex-disc",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: candidates
    # figure scene: graph of f over D with the candidates
    # graph(f) over D, the same rule over a box around D and the saddle at [2; 0] (light grey), D in the plane, the
    # boundary pieces lifted onto the graph, and the candidates (named in the 2D sketch beside it)
    def _f(x1, x2):
        return x2 * (x1 - 2)

    _s = np.linspace(-1, 1, 41)
    _S, _U = np.meshgrid(_s, np.linspace(0, 1, 11), indexing="ij")
    _d1, _d2 = _S, _S**2 + _U * (1 - _S**2)  # D = {(x^1)^2 <= x^2 <= 1}

    def _strip(x1, lo, hi, n=12):
        w = np.linspace(0, 1, n)[None, :]
        return x1[:, None] + 0 * w, lo + w * (hi - lo)

    # the box x^1 in [-1.3, 2.4], x^2 in [-0.4, 1.3] around D and [2; 0], in four pieces outside D
    _pieces = []
    for _x, _y in (
        _strip(np.linspace(-1.3, -1, 4), -0.4, 1.3),
        _strip(np.linspace(1, 2.4, 15), -0.4, 1.3),
        _strip(_s, -0.4, (_s**2)[:, None], 6),
        _strip(_s, 1.0, 1.3, 4),
    ):
        _pieces.append(lk.sheet(_x, _y, _f(_x, _y), tone=lk.GREY, alpha=0.45))
    # the edges: the border of the box lifted onto the graph, and the boundary of D lifted (the two pieces, below)
    _e = np.linspace(0, 1, 60)
    _border = []
    for _p, _q in (((-1.3, -0.4), (2.4, -0.4)), ((2.4, -0.4), (2.4, 1.3)), ((2.4, 1.3), (-1.3, 1.3)), ((-1.3, 1.3), (-1.3, -0.4))):
        _bx, _by = _p[0] + _e * (_q[0] - _p[0]), _p[1] + _e * (_q[1] - _p[1])
        _border.append((_bx, _by, _f(_bx, _by), "#8a8a8a", 1.0))
    # one mesh over the whole graph: the lines x^1 = const and x^2 = const (every 0.25), grey outside D, blue over D;
    # without it the saddle-shaped graph reads as a plane
    def _piece(x1, x2, colour):
        return (x1, x2, _f(x1, x2), colour, 0.5)

    _mesh = []
    for _k in np.arange(-1.25, 2.4, 0.25):
        if -1 < _k < 1:
            _lo, _hi = _k**2, 1.0
            _mesh += [_piece(_k + 0 * _e, -0.4 + _e * (_lo + 0.4), "#c8c8c8"), _piece(_k + 0 * _e, _lo + _e * (_hi - _lo), lk.BLUE), _piece(_k + 0 * _e, 1 + 0.3 * _e, "#c8c8c8")]
        else:
            _mesh += [_piece(_k + 0 * _e, -0.4 + 1.7 * _e, "#c8c8c8")]
    for _k in np.arange(-0.25, 1.3, 0.25):
        if 0 < _k < 1:
            _w = _k**0.5
            _mesh += [_piece(-1.3 + _e * (1.3 - _w), _k + 0 * _e, "#c8c8c8"), _piece(-_w + 2 * _w * _e, _k + 0 * _e, lk.BLUE), _piece(_w + _e * (2.4 - _w), _k + 0 * _e, "#c8c8c8")]
        elif abs(_k - 1) > 1e-9:
            _mesh += [_piece(-1.3 + 3.7 * _e, _k + 0 * _e, "#c8c8c8")]
    _a, _b, _c = (0, 0, 0), (-1, 1, -3), (1, 1, -1)
    _drops = [((-1, 1, 0), (-1, 1, -3)), ((1, 1, 0), (1, 1, -1))]
    lk.turntable(
        75,
        22,
        "graph of f over D and, in light grey, over a box around D with the saddle point at [2; 0]; D in the plane with its boundary dashed; f along the parabola and along the segment of the boundary of D; and the candidates a, b, c",
        [
            lk.panel(
                0.5,
                surfaces=[lk.sheet(_d1, _d2, 0 * _d1, flat="#c6d8ee", alpha=0.9), lk.sheet(_d1, _d2, _f(_d1, _d2))] + _pieces,
                lines=[(_s, _s**2, _f(_s, _s**2), lk.RED, 2.4, None, 0.4), (_s, 1 + 0 * _s, _f(_s, 1), lk.ORANGE, 2.4, None, 0.4)]
                + [(_s, _s**2, 0 * _s, lk.BLUE, 1.2, [4, 3], 0.2), (_s, 1 + 0 * _s, 0 * _s, lk.BLUE, 1.2, [4, 3], 0.2)]
                + [(np.linspace(_p[0], _q[0], 20), np.linspace(_p[1], _q[1], 20), np.linspace(_p[2], _q[2], 20), "#555555", 1.3, [1, 3], 0.3) for _p, _q in _drops]
                + _border + _mesh,
                points=[(_a, "#000000"), (_b, "#000000"), (_c, "#000000"), ((2, 0, 0), "#000000")],
                axes=[((0, 0, 0), (2.7, 0, 0), "x^1", -120), ((0, 0, 0), (0, 0.85, 0), "x^2", 0), ((0, 0, 0), (0, 0, 1.8), "y", 90)],
                texts=[
                    ((2, 0, 0), r"\begin{matrix} \vec{\nabla} f\left( \begin{bmatrix} 2 \\ 0 \end{bmatrix} \right) = \vec{0}, \\ \text{not a candidate} \end{matrix}", "#000000", 90, 50),
                    ((0.55, 0.75, 0), "D", lk.BLUE, 90, 0),
                    ((0.75, 0.5625, -0.703), r"f(\gamma(t))", lk.RED, 160, 18),
                    ((0, 1, -2), r"f(\sigma(t))", lk.ORANGE, -100, 60),
                    ((-1.15, 0.5, -1.65), r"y = f(\vec{x})", "#000000", 150, 22),
                ],
                box=((-1.2, 2.2), (-0.3, 1.2), (-2.9, 1.1)),
            )
        ],
        height=lk.H3D,
        width=500,
        key="L15-ex",
        apart=True,
    )

    return


@app.cell(hide_code=True)
def _(BOX, Figure, cross_axes, lk, math, mo, np, pt, tip_label):
    # module: candidates
    # example: global extrema of x^2 (x^1 - 2) on D, parts a) to d)
    # a) D between the parabola x^2 = (x^1)^2 and the line x^2 = 1, and the critical point of f outside D
    _fa = Figure(figsize=(lk.HALF + 0.4, 2.2), layout="constrained")
    _aa = _fa.subplots()
    _aa.set_xlim(-1.75, 3.7)
    _aa.set_ylim(-0.5, 1.85)
    _aa.set_aspect("equal")
    _aa.axis("off")
    _s = np.linspace(-1, 1, 201)
    _aa.fill_between(_s, _s**2, 1, color=lk.LIGHT, lw=0, zorder=0)
    _p = np.linspace(-1.3, 1.3, 201)
    _aa.plot(_p, _p**2, color=lk.RED, lw=1.4, zorder=3)
    _aa.plot([-1.55, 1.55], [1, 1], color=lk.ORANGE, lw=1.4, zorder=3)
    cross_axes(_aa, (-1.6, 2.6), (-0.3, 1.8), "$x^1$", "$x^2$")
    for _x, _name in ((-1, "$-1$"), (1, "$1$")):
        _aa.text(_x, -0.07, _name, ha="center", va="top", fontsize=12, bbox=BOX)
    _aa.text(2, -0.16, "$2$", ha="center", va="top", fontsize=12, bbox=BOX)
    _aa.text(-0.06, 1.04, "$1$", ha="right", va="bottom", fontsize=12, bbox=BOX)
    _aa.text(-0.5, 0.62, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _aa.text(1.42, 1.69, "$x^2 = (x^1)^2$", color=lk.RED, fontsize=12, ha="left", va="center")
    _aa.text(1.6, 1.0, "$x^2 = 1$", color=lk.ORANGE, fontsize=12, ha="left", va="center")
    _aa.plot(2, 0, "o", color="black", ms=5, zorder=5)
    _aa.annotate(r"$\genfrac{[}{]}{0}{0}{2}{0}$ not a candidate!", (2, 0), textcoords="offset points", xytext=(-3, 5), ha="left", va="bottom", fontsize=12, zorder=6)
    # b) the parabola gamma(t) = (t, t^2) and the segment sigma(t) = (t, 1), -1 <= t <= 1, with D faintly
    _t = round(pt.value, 10) + 0.0
    _fb = Figure(figsize=(lk.FULL, 2.3), layout="constrained")
    _left, _right = _fb.subplots(1, 2)
    for _ax in (_left, _right):
        _ax.set_xlim(-1.8, 1.8)
        _ax.set_ylim(-0.45, 1.6)
        _ax.set_aspect("equal")
        _ax.axis("off")
        _d = np.linspace(-1, 1, 201)
        _ax.fill_between(_d, _d**2, 1, color=lk.LIGHT, lw=0, zorder=0)
        cross_axes(_ax, (-1.5, 1.5), (-0.3, 1.5))
        for _x, _name in ((-1, "$-1$"), (1, "$1$")):
            _ax.text(_x, -0.07, _name, ha="center", va="top", fontsize=12, bbox=BOX)
    _s = np.linspace(-1, 1, 201)
    _left.plot(_s, _s**2, color=lk.RED, lw=1.6, zorder=3)
    _left.text(-0.06, 1.06, "$1$", ha="right", va="bottom", fontsize=12, bbox=BOX)
    for _e, _name, _ang in ((-1, r"$\gamma(-1)$", 180), (1, r"$\gamma(1)$", 0)):
        _left.plot(_e, 1, "o", color=lk.RED, ms=5, zorder=4)
        tip_label(_left, (_e, 1), _ang, _name, "black", r=4, fontsize=12)
    _left.plot(_t, _t**2, "o", color="black", ms=5, zorder=5)
    # the name of gamma(t) inside the parabola, along its normal (it turns with t and never jumps)
    _c, _n = -2 * _t / math.hypot(2 * _t, 1), 1 / math.hypot(2 * _t, 1)
    _r = 26 / 2 * abs(_c) + 14 / 2 * abs(_n) + 4
    _left.annotate(r"$\gamma(t)$", (_t, _t**2), textcoords="offset points", xytext=(_r * _c, _r * _n), ha="center", va="center", fontsize=12, zorder=6)
    _right.plot([-1, 1], [1, 1], color=lk.ORANGE, lw=1.6, zorder=3)
    _right.text(-0.06, 1.06, "$1$", ha="right", va="bottom", fontsize=12, bbox=BOX)
    for _e, _name, _ang in ((-1, r"$\sigma(-1)$", 180), (1, r"$\sigma(1)$", 0)):
        _right.plot(_e, 1, "o", color=lk.ORANGE, ms=5, zorder=4)
        tip_label(_right, (_e, 1), _ang, _name, "black", r=5, fontsize=12)
    _right.plot(_t, 1, "o", color="black", ms=5, zorder=5)
    _right.annotate(r"$\sigma(t)$", (_t, 1), textcoords="offset points", xytext=(0, -5), ha="center", va="top", fontsize=12, zorder=6)
    # f along the two pieces as functions of t, with the candidate values
    _fd = Figure(figsize=(lk.HALF + 0.6, 3.6), layout="constrained")
    _ad = _fd.subplots()
    _ad.set_xlim(-1.6, 2.35)
    _ad.set_ylim(-3.75, 0.75)
    _ad.axis("off")
    cross_axes(_ad, (-1.35, 1.45), (-3.5, 0.65), "$t$", "$y$")
    _s = np.linspace(-1, 1, 201)
    _ad.plot(_s, _s**2 * (_s - 2), color=lk.RED, lw=1.6, zorder=3)
    _ad.plot(_s, _s - 2, color=lk.ORANGE, lw=1.6, zorder=3)
    for _y in (-1, -3):
        _ad.plot([-0.04, 0.04], [_y, _y], color="black", lw=0.9)
        _ad.text(0.07, _y, f"${_y}$", ha="left", va="center", fontsize=11, bbox=BOX)
    for _x in (-1, 1):
        _ad.plot([_x, _x], [-0.06, 0.06], color="black", lw=0.9)
        _ad.text(_x, 0.12, f"${_x}$", ha="center", va="bottom", fontsize=11, bbox=BOX)
    _ad.text(1.08, -0.55, r"$y = f \circ \gamma(t)$", color=lk.RED, fontsize=12, ha="left", va="center")
    _ad.text(0.2, -2.15, r"$y = f \circ \sigma(t)$", color=lk.ORANGE, fontsize=12, ha="left", va="top")
    for _p, _name, _ang in (((0, 0), r"$f(\vec{a}) = 0$", 135), ((-1, -3), r"$f(\vec{b}) = -3$", -60), ((1, -1), r"$f(\vec{c}) = -1$", -40)):
        _ad.plot(*_p, "o", color="black", ms=5, zorder=5)
        tip_label(_ad, _p, _ang, _name, "black", r=5, fontsize=12)
    lk.example(
        [
            r"""
            $f(\vec{x}) = x^2 (x^1 - 2)$ on $D = \Big\{ \vec{x} \;\Big|\; \overbrace{(x^1)^2 \leqslant \mathrlap{\underbrace{\phantom{x^2 \leqslant 1}}_{D_2}} x^2}^{D_1} \leqslant 1 \Big\} = D_1 \cap D_2$
            """,
            lk.gap(),
            r"""
            a) &nbsp; Critical points in $D - \mathrm{Bd}(D)$

            > $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} x^2 \\ x^1 - 2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$ &nbsp; $\Longleftrightarrow$ &nbsp; $x^1 = 2, \ x^2 = 0$

            > > $\leadsto$ &nbsp; $\begin{bmatrix} 2 \\ 0 \end{bmatrix} \notin D - \mathrm{Bd}(D)$
            """,
            lk.figure(_fa),
            lk.gap(),
        r"""
        b) &nbsp; Parameterization of $\mathrm{Bd}(D)$

        > parabola: &nbsp; $\gamma(t) = \begin{bmatrix} t \\ t^2 \end{bmatrix}$, &nbsp; $-1 \leqslant t \leqslant 1$

        > straight segment: &nbsp; $\sigma(t) = \begin{bmatrix} t \\ 1 \end{bmatrix}$, &nbsp; $-1 \leqslant t \leqslant 1$
        """,
            lk.interactive(_fb, controls=[pt]),
            lk.gap(),
        r"""
        c) &nbsp; Global extrema of $f \circ \gamma$ and $f \circ \sigma$

        > $f \circ \gamma(t) = t^2 (t - 2)$, &nbsp; $t \in [-1, 1]$<br>
        > $f \circ \sigma(t) = t - 2$, &nbsp; $t \in [-1, 1]$

        > > $\Longrightarrow$ &nbsp; $t \in (-1, 1)$ &nbsp; or &nbsp; $t = -1$ or $1$

        > • &nbsp; critical points in $(-1, 1)$
        """,
        lk.aside(
            r"""
            > > $\leadsto$ &nbsp; $(f \circ \gamma)'(t) = 3t^2 - 4t = 0$ &nbsp; $\Longleftrightarrow$ &nbsp; $t = 0$ &nbsp; or &nbsp; $t = {\large\tfrac{4}{3}} > 1$

            > > <span class="lk-ghost">$\leadsto$ &nbsp;</span>$\vec{a} = \gamma(0) = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \in \mathrm{Bd}(D)$
            """,
            "one candidate",
            at="last",
        ),
        lk.aside(
            r"> > $\leadsto$ &nbsp; $(f \circ \sigma)'(t) = 1 \neq 0$ &nbsp; $\forall t \in (-1, 1)$",
            "no candidates",
        ),
        r"> • &nbsp; corner points",
        lk.aside(
            r"""
            > > $\gamma(-1) = \sigma(-1) = \begin{bmatrix} -1 \\ 1 \end{bmatrix} = \vec{b} \in \mathrm{Bd}(D)$

            > > $\gamma(1) = \sigma(1) = \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \vec{c} \in \mathrm{Bd}(D)$
            """,
            "two candidates",
        ),
        lk.gap(),
        r"""
        d) &nbsp; Compare

        > $\underbrace{f(\vec{a}) = 0}_{\footnotesize \text{global max}}$, &emsp; $\underbrace{f(\vec{b}) = -3}_{\footnotesize \text{global min}}$, &emsp; $f(\vec{c}) = -1$
        """,
            lk.figure(mo.Html('<div class="lk-pair">' f'<div class="lk-pair-3d">{lk.frame("L15-ex", lk.H3D, width=500).text}</div><div>{mo.as_html(_fd).text}</div></div>')),
        ],
        label="ex-candidates",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # section
    lk.section("Practice")
    return


@app.cell(hide_code=True)
def _(BOX, Figure, cross_axes, lk):
    # module: practice
    # exercise: global extrema on a rectangle
    # D = [0, 2] x [0, 3]
    _fig = Figure(figsize=(lk.HALF - 0.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.6, 3.1)
    _ax.set_ylim(-0.6, 3.75)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.4, 3.0), (-0.4, 3.7), "$x^1$", "$x^2$")
    _ax.fill([0, 2, 2, 0], [0, 0, 3, 3], color=lk.LIGHT, lw=0)
    _ax.plot([0, 2, 2, 0, 0], [0, 0, 3, 3, 0], color=lk.BLUE, lw=1.4)
    for _c in ((0, 0), (2, 0), (2, 3), (0, 3)):
        _ax.plot(*_c, "o", ms=4, color=lk.BLUE, zorder=3)
    _ax.text(2, -0.1, "$2$", ha="center", va="top", fontsize=12, bbox=BOX)
    _ax.text(-0.1, 3, "$3$", ha="right", va="center", fontsize=12, bbox=BOX)
    _ax.text(1, 1.5, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    lk.exercise(
        [
            r"""
            $f\Big( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \Big) = (x^1)^3 + (x^2)^2 - 3x^1 - 2x^2$

            a) find all critical points in $\mathbb{R}^2$

            b) decide their type (via 2nd derivative test)

            c) find the global maximum and global minimum over $D = [0, 2] \times [0, 3] = \{ 0 \leqslant x^1 \leqslant 2, \ 0 \leqslant x^2 \leqslant 3 \}$

            > $\leadsto$ &nbsp; parameterize the boundary with 4 different line segments
            """,
            lk.figure(_fig),
        ],
        label="ex-rectangle",
    )
    return


if __name__ == "__main__":
    app.run()
