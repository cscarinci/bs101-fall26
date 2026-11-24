import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 20 · Double integrals", css_file="lecturekit/style.css")


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
    lk.lecture(20, "Double integrals")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points), intervals marked on an axis, and the
    # region D of the examples (between the parabola y = x^2 and the line y = 1)

    def drawing(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def beside(ax, at, angle, text, color, w, h, gap=4, fontsize=13):
        """Name centred beside the point `at`, in the direction `angle` (degrees), far enough for a
        w x h box (points) to clear it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        d = w / 2 * abs(c) + h / 2 * abs(s) + gap
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "none", "edgecolor": "none"})

    def plane(xlim, ylim, width):
        """A drawing of the xy-plane: the two axes as arrows, named at their tips."""
        fig, ax = drawing(xlim, ylim, width)
        lk.arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        lk.arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, "$x$", "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, "$y$", "black", 10, 12)
        return fig, ax

    def bracket(ax, lo, hi, color, vertical=False, h=0.09):
        """The interval [lo, hi] of the x axis (of the y axis if `vertical`), drawn over the axis between two square brackets."""

        def line(u, v):
            ax.plot(*((v, u) if vertical else (u, v)), color=color, lw=1.6, solid_capstyle="butt", zorder=4)

        line([lo, hi], [0, 0])
        for e, d in ((lo, 1), (hi, -1)):
            line([e + d * 0.6 * h, e, e, e + d * 0.6 * h], [h, h, -h, -h])

    def parabola():
        """The region D of the examples, between the parabola y = x^2 and the line y = 1."""
        fig, ax = plane((-1.8, 2.25), (-0.5, 2.05), 4.2)
        s, d = np.linspace(-1.28, 1.28, 200), np.linspace(-1, 1, 200)
        ax.fill_between(d, d**2, 1, color=lk.LIGHT, lw=0, zorder=0)
        ax.plot(s, s**2, color=lk.RED, lw=1.8)
        ax.plot([-1.5, 1.5], [1, 1], color=lk.ORANGE, lw=1.8)
        beside(ax, (1.28, 1.28**2), 0, "$y = x^2$", lk.RED, 46, 16)
        beside(ax, (1.5, 1), 0, "$y = 1$", lk.ORANGE, 36, 16)
        ax.text(-0.5, 0.72, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=1)
        return fig, ax

    return beside, bracket, drawing, parabola, plane


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    sy = lk.slider(0.6, 2.6, step=0.05, value=1.6, label="$y$")
    xs = lk.slider(-1.0, 1.0, step=0.02, value=0.5, label="$x$")
    ys = lk.slider(0.0, 1.0, step=0.02, value=0.5, label="$y$")
    n1 = lk.slider(1, 24, step=1, value=6, label="$N$")
    n2 = lk.slider(1, 8, step=1, value=3, label="$N$")
    return n1, n2, sy, xs, ys


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ or $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$

        $C = \gamma([a, b]) \subset D$ parameterized by $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$

        path integral of $f$ over $C$

        $$
        \hphantom{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}\mathllap{\int_C f \, ds} = \mathrlap{\int_a^b \underbrace{f(\gamma(t))}_{\footnotesize f} \, \underbrace{\lVert \gamma'(t) \rVert \, dt}_{\footnotesize ds}}\hphantom{\int_a^b f(\gamma(t)) \, \lVert \gamma'(t) \rVert \, dt}
        $$

        line integral of $\vec{F}$ over $\vec{C}$ (oriented from $\gamma(a)$ to $\gamma(b)$)

        $$
        \hphantom{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}\mathllap{\int_{\vec{C}} \vec{F} \cdot d\vec{s}} = \mathrlap{\int_a^b \underbrace{\vec{F}(\gamma(t))}_{\footnotesize \vec{F}} \cdot \underbrace{\gamma'(t) \, dt}_{\footnotesize d\vec{s}}}\hphantom{\int_a^b f(\gamma(t)) \, \lVert \gamma'(t) \rVert \, dt}
        $$

        $\leadsto$ &nbsp; independent of parameterization: given a change of variables

        > $t = \varphi(\tilde{t}) \in [a, b]$ for $\tilde{t} \in [c, d]$, $\varphi'(\tilde{t}) \neq 0$

        $$
        \begin{aligned}
        \int_c^d f(\gamma(\varphi(\tilde{t}))) \, \lVert \gamma'(\varphi(\tilde{t})) \, \varphi'(\tilde{t}) \rVert \, d\tilde{t} &= \int_a^b f(\gamma(t)) \, \lVert \gamma'(t) \rVert \, dt\\[6pt]
        \int_c^d \vec{F}(\gamma(\varphi(\tilde{t}))) \cdot \gamma'(\varphi(\tilde{t})) \, \varphi'(\tilde{t}) \, d\tilde{t} &= \pm \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt
        \end{aligned}
        $$

        $$
        \begin{array}{lll}
        {+} & \text{if } \varphi'(\tilde{t}) > 0 & (\varphi \text{ preserves orientation})\\
        {-} & \text{if } \varphi'(\tilde{t}) < 0 & (\varphi \text{ reverses orientation})
        \end{array}
        $$
        """,
        lk.gap(),
        r"""
        If $\vec{F} = \vec{\nabla} f$, then

        $$
        \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt = \overset{\begin{array}{c}\footnotesize\text{end}\\[-2pt]\downarrow\end{array}}{f(\gamma(b))} - \overset{\begin{array}{c}\footnotesize\text{start}\\[-2pt]\downarrow\end{array}}{f(\gamma(a))}
        $$

        only depends on the (oriented) end points of $\vec{C}$

        (in particular, $\int_{\vec{C}} \vec{F} \cdot d\vec{s} = 0$ over closed curves!)

        $\leadsto$ &nbsp; in this case, we call $\vec{F} = \vec{\nabla} f$ a **conservative vector field** and $f$ a **potential function** for $\vec{F}$
        """,
        title="Last time",
        topic="Integration of functions and vector fields along 1-dimensional curves in $\\mathbb{R}^3$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"Multivariable integrals in $\mathbb{R}^n$ ($n = 2$)",
        lk.aside(
            r"> $\leadsto$ &nbsp; to be able to define integrals of vector fields <span class='lk-mark'>over surfaces in $\mathbb{R}^3$</span>",
            "in a few weeks …",
        ),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 5.1, 5.2, 5.3, 5.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: double integrals
    # section
    lk.section("Double integrals")
    return


@app.cell(hide_code=True)
def _(beside, drawing, lk, n1, np):
    # module: double integrals
    # recall: Riemann sums
    # the interval [a, b] cut into N intervals [a_i, b_i]: the left end points a_1, ..., a_N named above the axis, the
    # right end points b_1, ..., b_N below it, and one point t_i (blue) chosen in each interval
    _fig, _ax = drawing((-0.7, 6.3), (-0.95, 0.7), 5.0)
    lk.arrow(_ax, (-0.5, 0), (6.1, 0), "black", lw=0.9)
    for _e, _d in ((0, 1), (5, -1)):
        _ax.plot([_e + 0.08 * _d, _e, _e, _e + 0.08 * _d], [0.16, 0.16, -0.16, -0.16], color="black", lw=1.6, zorder=4)
    for _e in (1, 2, 3, 4):
        _ax.plot([_e, _e], [-0.07, 0.07], color="black", lw=1.0)
    for _e, _name in ((0, "$a_1$"), (1, "$a_2$"), (2, "$a_3$"), (3, r"$\cdots$"), (4, "$a_N$"), (5, "$b$")):
        beside(_ax, (_e, 0.16), 90, _name, "black", 24, 16)
    for _e, _name in ((0, "$a$"), (1, "$b_1$"), (2, "$b_2$"), (3, r"$\cdots$"), (4, "$b_{N-1}$"), (5, "$b_N$")):
        beside(_ax, (_e, -0.5), -90, _name, "black", 24, 16, gap=0)
    for _e, _name in ((0.45, "$t_1$"), (1.6, "$t_2$"), (4.55, "$t_N$")):
        _ax.plot(_e, 0, "o", color=lk.BLUE, ms=4.5, zorder=6)
        beside(_ax, (_e, 0), -90, _name, lk.BLUE, 16, 14)

    # the Riemann sum as N rectangles of height f(t_i) (t_i chosen in [a_i, b_i], blue) and base Delta t; below the t axis
    # the rectangles count negatively (red); N moves with the slider
    _a, _b, _n = 0.4, 5.4, int(n1.value)

    def _g(t):
        return 0.9 + 1.1 * np.sin(1.2 * t)

    _dt = (_b - _a) / _n
    _ti = _a + _dt * (np.arange(_n) + np.random.default_rng(10).uniform(0.15, 0.85, _n))  # t_i anywhere in [a_i, b_i]
    _rf, _rx = drawing((-0.5, 6.4), (-0.9, 2.55), 4.6)
    lk.arrow(_rx, (-0.3, 0), (6.2, 0), "black", lw=0.9)
    lk.arrow(_rx, (0, -0.8), (0, 2.45), "black", lw=0.9)
    beside(_rx, (6.2, 0), 0, "$t$", "black", 10, 12)
    for _k in range(_n):
        _h = float(_g(_ti[_k]))
        _c = lk.BLUE if _h >= 0 else lk.RED
        _rx.fill([_a + _k * _dt, _a + (_k + 1) * _dt, _a + (_k + 1) * _dt, _a + _k * _dt], [0, 0, _h, _h], color=_c, alpha=0.18, lw=0, zorder=1)
        _rx.plot([_a + _k * _dt, _a + _k * _dt, _a + (_k + 1) * _dt, _a + (_k + 1) * _dt], [0, _h, _h, 0], color=_c, lw=0.9, zorder=2)
    _rx.plot(_ti, 0 * _ti, "o", color=lk.BLUE, ms=3.5, zorder=6)
    _t = np.linspace(_a - 0.15, _b + 0.15, 300)
    _rx.plot(_t, _g(_t), color="black", lw=1.6, zorder=5)
    beside(_rx, (_b + 0.15, float(_g(_b + 0.15))), 0, r"$\mathrm{graph}(f)$", "black", 62, 16)
    for _e, _name in ((_a, "$a$"), (_b, "$b$")):
        beside(_rx, (_e, 0), -90 if float(_g(_e)) >= 0 else 90, _name, "black", 10, 14, gap=6)
    lk.recall(
        [
            r"""
            For $f : [a, b] \longrightarrow \mathbb{R}$

            $$
            \int_a^b f(t) \, dt = \lim_{N \to \infty} \sum_{i=1}^N f(t_i) \, \Delta t
            $$

            where, for each $N \in \mathbb{N}_{>0}$,

            > • divide $[a, b] = \bigcup_{i=1}^N [a_i, b_i]$, with

            $$
            a = a_1, \ b_1 = a_2, \ \ldots, \ b_{N-1} = a_N, \ b_N = b, \quad b_i - a_i = \frac{b - a}{N} = \Delta t
            $$

            > • choose $t_i \in [a_i, b_i]$

            > $\Longrightarrow$ &nbsp; $\displaystyle\sum_{i=1}^N \underbrace{f(t_i)}_{\footnotesize \rule{0pt}{1.15em}\mathllap{\text{height}\kern-1.1em}} \, \underbrace{\Delta t}_{\footnotesize \mathrlap{\kern-0.5em\text{base}}} \ \approx$ &nbsp; signed area between $\mathrm{graph}(f)$ and $t$ axis
            """,
            lk.figure(_fig),
            lk.interactive(_rf, controls=[n1]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(beside, bracket, lk, mo, n2, np, plane):
    # module: double integrals
    # prose: Riemann sums in R^2
    # the rectangle R = [a, b] x [c, d], with [a, b] marked on the x axis and [c, d] on the y axis, cut into N x N
    # small rectangles [a_i, b_i] x [c_j, d_j] with the chosen point (x_i, y_j) (blue) in each; N moves with the slider
    # of the boxes beside it
    _a, _b, _c, _d, _n = 1.0, 3.4, 0.8, 2.2, int(n2.value)
    _fig, _ax = plane((-0.7, 4.6), (-0.6, 3.1), 3.6)
    _ax.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=lk.LIGHT, lw=0, zorder=0)
    for _k in range(1, _n):
        _ax.plot([_a + _k * (_b - _a) / _n] * 2, [_c, _d], color=lk.BLUE, lw=0.7, zorder=1)
        _ax.plot([_a, _b], [_c + _k * (_d - _c) / _n] * 2, color=lk.BLUE, lw=0.7, zorder=1)
    # the chosen points: anywhere in their small rectangles (the same choice as for the boxes beside)
    _u, _v = np.random.default_rng(20).uniform(0.15, 0.85, (2, _n, _n))
    _px = _a + (_b - _a) / _n * (np.arange(_n)[:, None] + _u)
    _py = _c + (_d - _c) / _n * (np.arange(_n)[None, :] + _v)
    _ax.plot(_px.ravel(), _py.ravel(), "o", color=lk.BLUE, ms=3, zorder=6)
    _ax.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=lk.BLUE, lw=1.8)
    for _e in (_a, _b):
        _ax.plot([_e, _e], [0, _d], "--", color=lk.GREY, lw=0.9, zorder=1)
    for _e in (_c, _d):
        _ax.plot([0, _b], [_e, _e], "--", color=lk.GREY, lw=0.9, zorder=1)
    bracket(_ax, _a, _b, "black")
    bracket(_ax, _c, _d, "black", vertical=True)
    for _e, _name in ((_a, "$a$"), (_b, "$b$")):
        beside(_ax, (_e, 0), -90, _name, "black", 10, 14, gap=7)
    for _e, _name in ((_c, "$c$"), (_d, "$d$")):
        beside(_ax, (0, _e), 180, _name, "black", 10, 14, gap=7)
    beside(_ax, (_b, (_c + _d) / 2), 0, "$R$", lk.BLUE, 12, 14, gap=6)
    lk.prose(
        r"""
        How do we integrate functions in $\mathbb{R}^2$?

        Suppose $f : R = [a, b] \times [c, d] \longrightarrow \mathbb{R}$

        > • divide $[a, b] = \bigcup_{i=1}^N [a_i, b_i]$ and $[c, d] = \bigcup_{j=1}^N [c_j, d_j]$

        $$
        \begin{aligned}
        a = a_1, \ b_1 = a_2, \ \ldots, \ b_{N-1} = a_N, \ b_N = b, &\quad b_i - a_i = \frac{b - a}{N} = \Delta x\\
        c = c_1, \ d_1 = c_2, \ \ldots, \ d_{N-1} = c_N, \ d_N = d, &\quad d_j - c_j = \frac{d - c}{N} = \Delta y
        \end{aligned}
        $$

        > • choose $(x_i, y_j) \in [a_i, b_i] \times [c_j, d_j]$

        $$
        \iint_R f(x, y) \, dxdy = \lim_{N \to \infty} \sum_{j=1}^N \sum_{i=1}^N f(x_i, y_j) \, \Delta x \, \Delta y
        $$

        if limit exists for every choice $(x_i, y_j)$ and is independent of that choice!

        > $\Longrightarrow$ &nbsp; $\displaystyle\iint_R f(x, y) \, dxdy =$ &nbsp; signed volume between $\mathrm{graph}(f)$ and $xy$-plane
        """,
        lk.interactive(mo.hstack([_fig, lk.frame("L20-boxes", lk.H3D)], justify="center", align="center", gap=2), controls=[n2]),
    )
    return


@app.cell(hide_code=True)
def _(lk, n2, np):
    # module: double integrals
    # scene (no visible output; the prose above shows it)
    # the double Riemann sum as N x N boxes over the small rectangles [a_i, b_i] x [c_j, d_j] of R, each of height
    # f(x_i, y_j) at the chosen point (x_i, y_j); no labels (the sketch of R beside it names a, b, c, d); N moves with the slider
    _a, _b, _c, _d, _n = 0.6, 2.4, 0.6, 2.6, int(n2.value)

    def _f(x, y):
        return 1.3 + 0.25 * np.sin(1.6 * x) + 0.2 * y

    _dx, _dy = (_b - _a) / _n, (_d - _c) / _n
    _u, _v = np.random.default_rng(20).uniform(0.15, 0.85, (2, _n, _n))  # the chosen points (x_i, y_j), as in the sketch of R
    _faces, _edges = [], []
    for _i in range(_n):
        for _j in range(_n):
            _x0, _x1, _y0, _y1 = _a + _i * _dx, _a + (_i + 1) * _dx, _c + _j * _dy, _c + (_j + 1) * _dy
            _h = float(_f(_x0 + _u[_i, _j] * _dx, _y0 + _v[_i, _j] * _dy))
            _faces.append(lk.patch([(_x0, _y0, _h), (_x1, _y0, _h), (_x1, _y1, _h), (_x0, _y1, _h)], lk.LIGHT, 1.0, n=1))
            for _p, _q in (((_x0, _y0), (_x1, _y0)), ((_x1, _y0), (_x1, _y1)), ((_x1, _y1), (_x0, _y1)), ((_x0, _y1), (_x0, _y0))):
                _faces.append(lk.patch([(*_p, 0), (*_q, 0), (*_q, _h), (*_p, _h)], lk.LIGHT, 1.0, n=1))
                _edges.append(([_p[0], _q[0]], [_p[1], _q[1]], [_h, _h], lk.BLUE, 0.9))
                _edges.append(([_p[0], _p[0]], [_p[1], _p[1]], [0, _h], lk.BLUE, 0.9))
    lk.turntable(
        35,
        25,
        "the rectangle R = [a, b] x [c, d] cut into N x N small rectangles, with a box of height f(x_i, y_j) over each, under the graph z = f(x, y)",
        [
            lk.panel(
                1.0,
                surfaces=_faces,
                lines=_edges,
                axes=[((0, 0, 0), (2.9, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 2.3), "z", 90)],
                box=((0, 2.9), (0, 3.0), (0, 2.3)),
            )
        ],
        height=lk.H3D,
        key="L20-boxes",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: double integrals
    # theorem: continuous functions are integrable
    lk.theorem(
        r"""
        If $f : R \subset \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous, then $\iint_R f(x, y) \, dxdy$ is well-defined!
        """,
        label="thm-integrable",
    )
    return


@app.cell(hide_code=True)
def _(lk, np, sy):
    # module: double integrals
    # scene (no visible output; the proof below shows it)
    # the solid between the rectangle R = [a, b] x [c, d] of the xy-plane and the graph z = f(x, y); its slice at y
    # (green) has the area A(y), and y moves with the slider
    _a, _b, _c, _d = 0.6, 2.4, 0.6, 2.6

    def _f(x, y):
        return 1.3 + 0.25 * np.sin(1.6 * x) + 0.2 * y

    _y = round(sy.value, 10)
    _x1, _x2 = np.meshgrid(np.linspace(_a, _b, 19), np.linspace(_c, _d, 21), indexing="ij")
    _u, _v = np.meshgrid(np.linspace(0, 1, 19), np.linspace(0, 1, 9), indexing="ij")
    _xs, _ys = _a + (_b - _a) * _u, _c + (_d - _c) * _u
    _walls = [lk.sheet(_xs, _q + 0 * _u, _v * _f(_xs, _q), flat=lk.LIGHT, alpha=0.45) for _q in (_c, _d)]
    _walls += [lk.sheet(_q + 0 * _u, _ys, _v * _f(_q, _ys), flat=lk.LIGHT, alpha=0.45) for _q in (_a, _b)]
    _top = lk.sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 6, lk.BLUE, 0.5), (1, 5, lk.BLUE, 0.5)], alpha=0.75)
    _slice = lk.sheet(_xs, _y + 0 * _u, _v * _f(_xs, _y), flat="#a8c6ae", alpha=0.9)
    _s, _t = np.linspace(_a, _b, 60), np.linspace(_c, _d, 60)
    _edges = [(_s, _q + 0 * _s, _f(_s, _q), lk.BLUE, 1.2) for _q in (_c, _d)] + [(_q + 0 * _t, _t, _f(_q, _t), lk.BLUE, 1.2) for _q in (_a, _b)]
    _edges += [(_s, _q + 0 * _s, 0 * _s, lk.BLUE, 1.2) for _q in (_c, _d)] + [(_q + 0 * _t, _t, 0 * _t, lk.BLUE, 1.2) for _q in (_a, _b)]
    _edges += [([_p, _p], [_q, _q], [0, float(_f(_p, _q))], lk.BLUE, 1.2) for _p in (_a, _b) for _q in (_c, _d)]
    _cut = [(_s, _y + 0 * _s, _f(_s, _y), lk.GREEN, 2.2), (_s, _y + 0 * _s, 0 * _s, lk.GREEN, 2.2)]
    _cut += [([_p, _p], [_y, _y], [0, float(_f(_p, _y))], lk.GREEN, 2.2) for _p in (_a, _b)]
    _guides = [([_p, _p], [0, _c], [0, 0], lk.GREY, 1.0, [4, 3]) for _p in (_a, _b)] + [([0, _a], [_q, _q], [0, 0], lk.GREY, 1.0, [4, 3]) for _q in (_c, _d)]
    _guides += [([0, _a], [_y, _y], [0, 0], lk.GREEN, 1.0, [4, 3])]
    lk.turntable(
        35,
        25,
        "the solid between the rectangle R = [a, b] x [c, d] and the graph z = f(x, y), with its slice at y, of area A(y)",
        [
            lk.panel(
                1.0,
                surfaces=_walls + [_top, _slice],
                lines=_edges + _cut + _guides,
                points=[((0, _y, 0), lk.GREEN, 4.0)],
                axes=[((0, 0, 0), (3.1, 0, 0), "x", -150), ((0, 0, 0), (0, 3.2, 0), "y", 0), ((0, 0, 0), (0, 0, 2.6), "z", 90)],
                texts=[
                    ((_a, 0, 0), "a", "#000000", -60, 8),
                    ((_b, 0, 0), "b", "#000000", -60, 8),
                    ((0, _c, 0), "c", "#000000", -90, 8),
                    ((0, _d, 0), "d", "#000000", -90, 8),
                    ((0, _y, 0), "y", lk.GREEN, -90, 8),
                    (((_a + _b) / 2, _y, float(_f((_a + _b) / 2, _y)) / 2), "A(y)", lk.GREEN, 0, 0),
                    ((_a, _d, float(_f(_a, _d))), "z = f(x, y)", lk.BLUE, 45, 6),
                ],
                box=((0, 3.1), (0, 3.2), (0, 2.6)),
            )
        ],
        height=lk.H3D,
        key="L20-volume",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, sy):
    # module: double integrals
    # proof sketch
    lk.sketch(
        [
            r"""
            $$
            \text{area} = A(y) = \int_a^b f(x, y) \, dx \qquad \text{vol} = \int_c^d A(y) \, dy
            $$

            $f(x, y)$ continuous &nbsp; $\Longrightarrow$ &nbsp; $A(y)$ continuous &nbsp; $\Longrightarrow$ &nbsp; integrable
            """,
            lk.interactive(lk.frame("L20-volume", lk.H3D), controls=[sy]),
        ],
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: double integrals
    # theorem: Fubini
    lk.theorem(
        [
            lk.aside(
                r"If $f : R = [a, b] \times [c, d] \longrightarrow \mathbb{R}$ <span class='lk-mark'>continuous</span>",
                "also works if discontinuities<br>are not too bad!",
            ),
            r"""
            $$
            \begin{aligned}
            \iint_R f(x, y) \, dxdy &= \int_c^d \left( \int_a^b f(x, y) \, dx \right) dy\\
            &= \int_a^b \left( \int_c^d f(x, y) \, dy \right) dx
            \end{aligned}
            $$
            """,
        ],
        title="Fubini",
        label="thm-fubini",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: double integrals
    # example: x^2 + y over a rectangle
    lk.example(
        r"""
        $f(x, y) = x^2 + y$, $R = [0, 2] \times [0, 3]$

        $$
        \begin{aligned}
        \int_0^3 \left( \int_0^2 (x^2 + y) \, dx \right) dy &= \int_0^3 \left( \frac{x^3}{3} + xy \right) \Bigg|_{x=0}^{x=2} dy\\
        &= \int_0^3 \left( \frac{8}{3} + 2y \right) dy = 8 + 9 = 17\\[10pt]
        \int_0^2 \left( \int_0^3 (x^2 + y) \, dy \right) dx &= \int_0^2 \left( x^2 y + \frac{y^2}{2} \right) \Bigg|_{y=0}^{y=3} dx\\
        &= \int_0^2 \left( 3x^2 + \frac{9}{2} \right) dx = 8 + 9 = 17
        \end{aligned}
        $$

        > $\Longrightarrow$ &nbsp; $\displaystyle\iint_R f(x, y) \, dxdy = 17$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: double integrals
    # consequence: order of integration, and more general regions
    lk.prose(
        r"""
        $\leadsto$ &nbsp; double integrals *over rectangles* = iterated integrals over intervals<br>are independent of the order of integration!
        """,
        lk.aside(
            r"$\leadsto$ &nbsp; how about <span class='lk-mark'>more general regions</span>?",
            "how to describe them?<br>how to integrate over them?",
        ),
    )
    return


@app.cell(hide_code=True)
def _(beside, bracket, lk, mo, np, plane):
    # module: simple regions
    # definition: y-simple and x-simple
    # left: a y-simple region D between the graphs y = phi_1(x) (red) and y = phi_2(x) (orange) over [a, b]; over the
    # point x (green), y runs from phi_1(x) to phi_2(x). Right: an x-simple region D between x = psi_1(y) (red) and
    # x = psi_2(y) (orange) over [c, d]; at the height y (green), x runs from psi_1(y) to psi_2(y)
    _s = np.linspace(0.7, 3.2, 200)
    _lo, _hi = 0.8 + 0.18 * np.sin(4 * _s), 2.2 + 0.2 * np.sin(3 * _s)
    _k = 85
    _left, _ax = plane((-1.3, 5.05), (-0.8, 3.75), 3.3)
    _ax.fill_between(_s, _lo, _hi, color=lk.LIGHT, lw=0, zorder=0)
    for _e in (0, -1):
        _ax.plot([_s[_e], _s[_e]], [_lo[_e], _hi[_e]], "--", color=lk.GREY, lw=1.0)
    for _g, _c in ((_lo, lk.RED), (_hi, lk.ORANGE)):
        _ax.plot(_s, _g, color=_c, lw=1.8)
        _ax.plot(_s[[0, -1]], _g[[0, -1]], "o", color=_c, ms=4.5, zorder=6)
    bracket(_ax, _s[0], _s[-1], "black")
    beside(_ax, (_s[0], 0), -90, "$a$", "black", 10, 14, gap=7)
    beside(_ax, (_s[-1], 0), -90, "$b$", "black", 10, 14, gap=7)
    _ax.plot([_s[_k], _s[_k]], [_lo[_k], _hi[_k]], color=lk.GREEN, lw=1.8)
    _ax.plot([0, 0], [_lo[_k], _hi[_k]], color=lk.GREEN, lw=1.8, zorder=5)
    for _p in ((_s[_k], _lo[_k]), (_s[_k], _hi[_k]), (_s[_k], 0), (0, _lo[_k]), (0, _hi[_k])):
        _ax.plot(*_p, "o", color=lk.GREEN, ms=4.5, zorder=7)
    beside(_ax, (_s[_k], 0), -90, "$x$", lk.GREEN, 10, 14, gap=7)
    beside(_ax, (0, _lo[_k]), 180, r"$\varphi_1(x)$", lk.GREEN, 40, 16)
    beside(_ax, (0, _hi[_k]), 180, r"$\varphi_2(x)$", lk.GREEN, 40, 16)
    beside(_ax, (_s[-1], _lo[-1]), 0, r"$y = \varphi_1(x)$", lk.RED, 72, 16, gap=6)
    beside(_ax, (_s[-1], _hi[-1]), 0, r"$y = \varphi_2(x)$", lk.ORANGE, 72, 16, gap=6)
    _ax.text((_s[0] + _s[-1]) / 2, 3.4, "$y$-simple region $D$", color=lk.BLUE, fontsize=13, ha="center", va="center")

    _t = np.linspace(0.6, 2.9, 200)
    _l, _r = 1.5 + 0.18 * np.sin(4 * _t), 2.9 + 0.2 * np.sin(3 * _t)
    _right, _ax = plane((-0.9, 5.45), (-0.8, 3.75), 3.3)
    _ax.fill_betweenx(_t, _l, _r, color=lk.LIGHT, lw=0, zorder=0)
    for _e in (0, -1):
        _ax.plot([_l[_e], _r[_e]], [_t[_e], _t[_e]], "--", color=lk.GREY, lw=1.0)
    for _g, _c in ((_l, lk.RED), (_r, lk.ORANGE)):
        _ax.plot(_g, _t, color=_c, lw=1.8)
        _ax.plot(_g[[0, -1]], _t[[0, -1]], "o", color=_c, ms=4.5, zorder=6)
    bracket(_ax, _t[0], _t[-1], "black", vertical=True)
    beside(_ax, (0, _t[0]), 180, "$c$", "black", 10, 14, gap=7)
    beside(_ax, (0, _t[-1]), 180, "$d$", "black", 10, 14, gap=7)
    _ax.plot([_l[_k], _r[_k]], [_t[_k], _t[_k]], color=lk.GREEN, lw=1.8)
    _ax.plot([_l[_k], _r[_k]], [0, 0], color=lk.GREEN, lw=1.8, zorder=5)
    for _p in ((_l[_k], _t[_k]), (_r[_k], _t[_k]), (0, _t[_k]), (_l[_k], 0), (_r[_k], 0)):
        _ax.plot(*_p, "o", color=lk.GREEN, ms=4.5, zorder=7)
    beside(_ax, (0, _t[_k]), 180, "$y$", lk.GREEN, 10, 14, gap=7)
    beside(_ax, (_l[_k], 0), -90, r"$\psi_1(y)$", lk.GREEN, 40, 16)
    beside(_ax, (_r[_k], 0), -90, r"$\psi_2(y)$", lk.GREEN, 40, 16)
    beside(_ax, (_l[-1], _t[-1]), 100, r"$x = \psi_1(y)$", lk.RED, 72, 16, gap=6)
    beside(_ax, (_r[150], _t[150]), 0, r"$x = \psi_2(y)$", lk.ORANGE, 72, 16, gap=6)
    _ax.text(5.4, 3.4, "$x$-simple region $D$", color=lk.BLUE, fontsize=13, ha="right", va="center")
    lk.definition(
        [
            r"""
            A region $D \subseteq \mathbb{R}^2$ is called **$y$-simple** if

            $$
            D = \left\lbrace (x, y) \in \mathbb{R}^2 \mid a \le x \le b, \ \varphi_1(x) \le y \le \varphi_2(x) \right\rbrace
            $$

            for continuous functions $\varphi_1, \varphi_2 : [a, b] \longrightarrow \mathbb{R}$
            """,
            lk.gap(),
            r"""
            Similarly, $D \subseteq \mathbb{R}^2$ is called **$x$-simple** if

            $$
            D = \left\lbrace (x, y) \in \mathbb{R}^2 \mid c \le y \le d, \ \psi_1(y) \le x \le \psi_2(y) \right\rbrace
            $$

            for continuous functions $\psi_1, \psi_2 : [c, d] \longrightarrow \mathbb{R}$
            """,
            lk.figure(mo.hstack([_left, _right], justify="center", gap=4)),
        ],
        label="def-simple",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # prose: integration over simple regions
    lk.prose(
        r"""
        Integration over $y$-simple / $x$-simple regions:

        Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ continuous over $D$ $y$-simple

        > $\leadsto$ &nbsp; take $R = [a, b] \times [\overbrace{c}^{\footnotesize\min\limits_{[a, b]}(\varphi_1)}, \underbrace{d}_{\footnotesize\max\limits_{[a, b]}(\varphi_2)}] \supseteq D$

        > $\leadsto$ &nbsp; define $f^* : R \longrightarrow \mathbb{R}$ via
        """,
        lk.aside(
            r"""
            > > $\mk{f^*(x, y)} = \begin{cases}
            f(x, y) & \text{if } (x, y) \in D\\
            0 & \text{if } (x, y) \notin D
            \end{cases}$
            """,
            "discontinuous, but<br>Fubini still works!",
        ),
        r"""
        $$
        \begin{aligned}
        \leadsto \quad \iint_D f(x, y) \, dxdy &= \iint_R f^*(x, y) \, dxdy\\[4pt]
        &= \int_a^b \left( \int_c^d f^*(x, y) \, dy \right) dx = \int_a^b \left( \int_{\varphi_1(x)}^{\varphi_2(x)} f(x, y) \, dy \right) dx
        \end{aligned}
        $$

        Similarly, if $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ continuous over $D$ $x$-simple

        $$
        \iint_D f(x, y) \, dxdy = \int_c^d \left( \int_{\psi_1(y)}^{\psi_2(y)} f(x, y) \, dx \right) dy
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, parabola, xs):
    # module: simple regions
    # example: the region under y = 1 over the parabola, as a y-simple region
    # over the point x (green), y runs from x^2 to 1; x moves with the slider
    _x = round(xs.value, 10)
    _fig, _ax = parabola()
    _ax.plot([_x, _x], [0, _x**2], ":", color=lk.GREY, lw=0.9)
    _ax.plot([_x, _x], [_x**2, 1], color=lk.GREEN, lw=1.8)
    for _y in (0, _x**2, 1):
        _ax.plot(_x, _y, "o", color=lk.GREEN, ms=4.5, zorder=6)
    beside(_ax, (_x, 0), -90, "$x$", lk.GREEN, 10, 14, gap=6)
    lk.example(
        [
            r"""
            $D = \left\lbrace (x, y) \mid x^2 \le y \le 1 \right\rbrace$

            $\phantom{D} = \left\lbrace (x, y) \mid -1 \le x \le 1, \ x^2 \le y \le 1 \right\rbrace$

            > $\leadsto$ &nbsp; $y$-simple!

            $$
            \begin{aligned}
            \Longrightarrow \quad \iint_D (xy - 2y) \, dxdy &= \int_{-1}^1 \left( \int_{x^2}^1 (xy - 2y) \, dy \right) dx\\
            &= \int_{-1}^1 \left( x \, \frac{y^2}{2} - y^2 \, \Bigg|_{y=x^2}^{y=1} \right) dx\\
            &= \int_{-1}^1 \left( \frac{x}{2} - 1 - \frac{x^5}{2} + x^4 \right) dx\\
            &= \left( \frac{x^2}{4} - x - \frac{x^6}{12} + \frac{x^5}{5} \right) \Bigg|_{x=-1}^{x=1} = -2 + \frac{2}{5} = -8/5
            \end{aligned}
            $$
            """,
            lk.interactive(_fig, controls=[xs]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, math, parabola, ys):
    # module: simple regions
    # example: the same region as an x-simple region
    # at the height y (green), x runs from -sqrt(y) to sqrt(y); y moves with the slider
    _y = round(ys.value, 10)
    _r = math.sqrt(_y)
    _fig, _ax = parabola()
    _ax.plot([-_r, _r], [_y, _y], color=lk.GREEN, lw=1.8)
    for _x in (-_r, 0, _r):
        _ax.plot(_x, _y, "o", color=lk.GREEN, ms=4.5, zorder=6)
    beside(_ax, (-_r, _y), 180, "$y$", lk.GREEN, 10, 14, gap=6)
    lk.example(
        [
            r"""
            Is $D$ $x$-simple? Yes!

            > $D = \left\lbrace (x, y) \mid 0 \le y \le 1, \ -\sqrt{y} \le x \le \sqrt{y} \right\rbrace$

            $$
            \begin{aligned}
            \Longrightarrow \quad \iint_D (xy - 2y) \, dxdy &= \int_0^1 \left( \int_{-\sqrt{y}}^{\sqrt{y}} (xy - 2y) \, dx \right) dy\\
            &= \int_0^1 \left( \frac{x^2 y}{2} - 2xy \, \Bigg|_{x=-\sqrt{y}}^{x=\sqrt{y}} \right) dy\\
            &= \int_0^1 -4 \sqrt{y} \, y \, dy\\
            &= \int_0^1 -4 (y)^{3/2} \, dy = -4 \, \frac{2}{5} \, y^{5/2} \, \Bigg|_{y=0}^{y=1} = -8/5
            \end{aligned}
            $$
            """,
            lk.interactive(_fig, controls=[ys]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # consequence: simple regions
    lk.prose(r"$\leadsto$ &nbsp; $D$ is called **simple** if it is both $y$-simple and $x$-simple")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # theorem: mean value
    lk.theorem(
        r"""
        If $D$ is $y$-simple or $x$-simple and $f : D \longrightarrow \mathbb{R}$ is continuous,<br>then there exists $(x_0, y_0) \in D$ such that

        $$
        \iint_D f(x, y) \, dxdy = f(x_0, y_0) \underbrace{\iint_D dxdy}_{\footnotesize \text{area of } D}
        $$
        """,
        label="thm-mean-value",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # consequence: average
    lk.prose(r"$\leadsto$ &nbsp; $f(x_0, y_0)$ is the average of $f$ over $D$")
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
    # exercise: triangle
    lk.exercise(
        r"""
        $D$ is the triangle with corners $(0, 0)$, $(2, 0)$, $(1, 1)$

        a) Describe $D$ as a $y$-simple region

        b) Describe $D$ as an $x$-simple region

        c) Compute $\displaystyle \iint_D y \, dxdy$.
        """,
        label="ex-triangle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: change the order
    lk.exercise(
        r"Compute $\displaystyle \int_0^1 \left( \int_y^1 \frac{\sin(x)}{x} \, dx \right) dy$.",
        label="ex-order",
    )
    return


if __name__ == "__main__":
    app.run()
