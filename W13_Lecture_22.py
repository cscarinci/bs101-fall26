import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 22 · Integration over surfaces in ℝ³", css_file="lecturekit/style.css")


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
    return Figure, lk, math, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(22, "Integration over surfaces in ℝ³")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points), the curve C and the dome-shaped surface S
    # of the 3D figures

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

    def plane(xlim, ylim, width, names=("$x$", "$y$")):
        """A drawing of a coordinate plane: the two axes as arrows, named at their tips."""
        fig, ax = drawing(xlim, ylim, width)
        lk.arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        lk.arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, names[0], "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, names[1], "black", 10, 12)
        return fig, ax

    def rect_D(s_lim, t_top, ticks_s, ticks_t, s0=None, t0=None):
        """The rectangle D in the (s, t)-plane (t drawn as t / pi), with the segment s = s0 (red) and t = t0 (orange)."""
        a, b = s_lim
        fig, ax = plane((min(a, 0) - 0.7, b + 0.9), (-0.55, t_top + 1.0), 2.6, names=("$s$", "$t$"))
        ax.fill([a, b, b, a], [0, 0, t_top, t_top], color=lk.LIGHT, lw=0, zorder=0)
        ax.plot([a, b, b, a, a], [0, 0, t_top, t_top, 0], color=lk.BLUE, lw=1.8)
        if s0 is not None:
            ax.plot([s0, s0], [0, t_top], color=lk.RED, lw=1.8, zorder=3)
        if t0 is not None:
            ax.plot([a, b], [t0, t0], color=lk.ORANGE, lw=1.8, zorder=3)
        for x, name, c in ticks_s:
            beside(ax, (x, 0), -90, name, c, 12, 14, gap=6)
        for y, name, c in ticks_t:
            beside(ax, (min(a, 0), y), 180, name, c, 20, 14)
        ax.text(b + 0.15, t_top + 0.3, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
        return fig

    _d, _N = np.array([-0.55, 0.83, 0.0]), np.array([0.83, 0.55, 0.0])

    def curve(u):
        """A curve in R^3 with one loop; u runs over [-3.6, 3.6]."""
        u = np.asarray(u, float)
        a, h = 0.7 * (0.5 * u - np.sin(u)), 1.5 - 0.9 * np.cos(u) + 0.08 * u
        e = 0.15 * u
        return 1.3 + a * _d[0] + e * _N[0], 1.5 + a * _d[1] + e * _N[1], h

    def curve_velocity(u):
        return 0.7 * (0.5 - math.cos(u)) * _d + 0.15 * _N + np.array([0.0, 0.0, 0.9 * math.sin(u) + 0.08])

    def dome(x, y):
        """The height of the dome-shaped surface S (a graph over the (x, y)-plane)."""
        return 2.4 - 0.25 * ((x - 1.55) ** 2 + (y - 1.3) ** 2)

    def dome_grid(n=25):
        u, v = np.meshgrid(np.linspace(0.4, 2.7, n), np.linspace(0.3, 2.3, n), indexing="ij")
        return u, v, dome(u, v)

    AXES = [((0, 0, 0), (2.9, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", -20), ((0, 0, 0), (0, 0, 2.8), "z", 90)]
    SPHERE_AXES = [((0, 0, 0), (2.6, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", -20), ((0, 0, 0), (0, 0, 2.6), "z", 90)]
    SPHERE_BOX = ((-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8))  # sphere of radius 2: box 0.9 x radius, as every sphere
    return AXES, SPHERE_AXES, SPHERE_BOX, beside, curve, curve_velocity, dome, dome_grid, drawing, plane, rect_D


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    cs = lk.slider(-1, 1, step=0.25, value=0, label="$s$")
    ct = lk.slider(0, 6.28, step=0.04, value=0.8, label="$t$")
    ss = lk.slider(0, 3.14, step=0.04, value=1.56, label="$s$")
    st = lk.slider(0, 6.28, step=0.04, value=1.04, label="$t$")
    dt = lk.slider(0.1, 1.5, step=0.1, value=1.2, label=r"$\Delta t$")
    dd = lk.slider(0.6, 1.2, step=0.1, value=1.0, label=r"$\Delta s = \Delta t$")
    return cs, ct, dd, dt, ss, st


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"$D\subseteq\mathbb{R}^2$ simple, &nbsp; $\vec{C}=\mathrm{Bd}(D)$ with positive orientation and",
        r"""
        $\vec{F}=\begin{bmatrix} P \\ Q \end{bmatrix}$ &nbsp; $C^1$-smooth

        > $\Longrightarrow$ &nbsp; $\displaystyle\int_{\vec{C}}\vec{F}\cdot d\vec{s}=\iint_D\underbrace{\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)}_{\mathclap{\footnotesize\text{scalar curl}}}dxdy$

        $\leadsto$ &nbsp; can we generalize this to $\mathbb{R}^3$?

        > <span class="lk-tab" style="--lk-tab: 4.2em">Stokes</span>$\longrightarrow$ &nbsp; curved surfaces and their boundary curves

        > <span class="lk-tab" style="--lk-tab: 4.2em">Gauss</span>$\longrightarrow$ &nbsp; bounded 3d regions and their boundary surfaces
        """,
        topic="Green's theorem",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.prose(r"""
        Integration over surfaces in $\mathbb{R}^3$
        """),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 7.3, 7.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: parameterized surfaces
    # section
    lk.section("Integration over surfaces in ℝ³")
    return


@app.cell(hide_code=True)
def _(beside, curve, drawing, lk, np):
    # module: parameterized surfaces
    # recall: paths
    # the interval I on a line with a point t, and the curve C = Im(gamma) with the point gamma(t)
    _fi, _ai = drawing((-0.3, 3.3), (-0.9, 0.9), 2.6)
    lk.arrow(_ai, (-0.2, 0), (3.1, 0), "black", lw=0.9)
    _ai.plot([0.5, 2.6], [0, 0], color=lk.BLUE, lw=3)
    _ai.plot(1.4, 0, "o", color="black", ms=4.5, zorder=6)
    beside(_ai, (1.4, 0), 90, "$t$", "black", 8, 12)
    beside(_ai, (2.3, 0), -90, "$I$", lk.BLUE, 8, 12, gap=6)
    _u0 = 2.3  # the same point as in the tangent-line figure
    _p = curve(_u0)
    _C = lk.turntable(
        30,
        20,
        "the curve C = Im(gamma), with one loop, and the point gamma(t) on it",
        [
            lk.panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), lk.BLUE, 1.8)],
                points=[(tuple(float(c) for c in _p), "#000000")],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(tuple(float(c) for c in _p), r"\gamma(t)", "#000000", -10, 12), (tuple(float(c) for c in curve(-3.0)), r"C = \mathrm{Im}(\gamma)", lk.BLUE, 180, 44)],
                box=((0, 3.0), (0, 3.0), (0, 3.0)),
            )
        ],
        height=lk.H3D,
    )
    lk.recall(
        [
            r"""
            A path (or parameterized curve) in $\mathbb{R}^3$ is a function

            $$
            \gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3, \qquad t \longmapsto \begin{bmatrix} x(t) \\ y(t) \\ z(t) \end{bmatrix}
            $$

            $C=\mathrm{Im}(\gamma)=\gamma(I)\subset\mathbb{R}^3$ is a curve in $\mathbb{R}^3$
            """,
            lk.maps(_fi, r"\gamma", _C),
        ]
    )
    return


@app.cell(hide_code=True)
def _(AXES, dome, lk, np, plane):
    # module: parameterized surfaces
    # definition: parameterized surface
    # the region D with a point (s, t), and the surface S = Phi(D), the graph of a function over D, with Phi(s, t)
    _fd, _ad = plane((-0.5, 3.4), (-0.4, 2.8), 2.6, names=("$s$", "$t$"))
    _s = np.linspace(0.5, 2.6, 100)
    _lo, _hi = 0.5 + 0.12 * np.sin(4 * (_s - 0.5)), 2.1 + 0.12 * np.sin(3.5 * (_s - 0.5) + 1)
    _ad.fill_between(_s, _lo, _hi, color=lk.LIGHT, lw=0, zorder=0)
    for _y in (_lo, _hi):
        _ad.plot(_s, _y, color=lk.BLUE, lw=1.8)
    for _i in (0, -1):
        _ad.plot([_s[_i], _s[_i]], [_lo[_i], _hi[_i]], color=lk.BLUE, lw=1.8)
    _ad.text(2.9, 2.45, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _p = (1.3, 1.2)
    _ad.plot(*_p, "o", color="black", ms=4.5, zorder=6)
    _ad.text(_p[0] + 0.1, _p[1], "$(s, t)$", color="black", fontsize=13, ha="left", va="center")
    _u, _v = np.meshgrid(np.linspace(0.5, 2.6, 25), np.linspace(0, 1, 25), indexing="ij")
    _L, _H = 0.5 + 0.12 * np.sin(4 * (_u - 0.5)), 2.1 + 0.12 * np.sin(3.5 * (_u - 0.5) + 1)
    _x1, _x2 = _u, _L + _v * (_H - _L)
    _rim = [(_s, _y, dome(_s, _y), lk.BLUE, 1.2) for _y in (_lo, _hi)] + [([_s[_i]] * 30, np.linspace(_lo[_i], _hi[_i], 30), dome(_s[_i], np.linspace(_lo[_i], _hi[_i], 30)), lk.BLUE, 1.2) for _i in (0, -1)]
    _q = (_p[0], _p[1], float(dome(*_p)))
    _S = lk.turntable(
        28,
        32,
        "the surface S = Phi(D), the graph of a function over the region D, and the point Phi(s, t), the image of the point (s, t) of D",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_x1, _x2, dome(_x1, _x2), wire=[(0, 4, lk.BLUE, 0.4), (1, 4, lk.BLUE, 0.4)])],
                lines=_rim,
                points=[(_q, "#000000")],
                axes=AXES,
                texts=[(_q, r"\Phi(s, t)", "#000000", 60, 8), ((2.6, float(_lo[-1]), float(dome(2.6, _lo[-1]))), r"S = \mathrm{Im}(\Phi)", lk.BLUE, 230, 10)],
            )
        ],
        height=lk.H3D,
    )
    lk.definition(
        [
            r"""
            A **parameterized surface** in $\mathbb{R}^3$ is a function

            $$
            \Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3, \qquad (s, t) \longmapsto \begin{bmatrix} x(s, t) \\ y(s, t) \\ z(s, t) \end{bmatrix}
            $$

            $S=\mathrm{Im}(\Phi)=\Phi(D)\subset\mathbb{R}^3$ is a surface in $\mathbb{R}^3$
            """,
            lk.maps(_fd, r"\Phi", _S),
        ],
        label="def-surface",
    )
    return


@app.cell(hide_code=True)
def _(SPHERE_AXES, cs, ct, lk, np):
    # module: parameterized surfaces
    # scene (no visible output; the example below shows it)
    # the cylinder S with the images of the segments s = s0 (red: the circle at height s0) and t = t0 (orange: the
    # vertical segment at the angle t0); s and t move with the sliders
    _s0, _a = float(cs.value), float(ct.value)
    _s, _t = np.meshgrid(np.linspace(-1, 1, 9), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _Z = np.linspace(-1, 1, 20)
    lk.turntable(
        30,
        22,
        "the cylinder of radius 2 and height 2 around the z-axis, with the circle at height s and the vertical segment at the angle t",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.cos(_t), 2 * np.sin(_t), _s, wire=[(0, 2, lk.BLUE, 0.4), (1, 9, lk.BLUE, 0.4)], alpha=0.45)],
                lines=[(2 * np.cos(_T), 2 * np.sin(_T), _s0 + 0 * _T, lk.RED, 2.4), (2 * np.cos(_a) + 0 * _Z, 2 * np.sin(_a) + 0 * _Z, _Z, lk.ORANGE, 2.4)],
                axes=SPHERE_AXES,
                texts=[((0, 0, 1), "1", "#000000", 180, 6), ((0, 0, -1), "-1", "#000000", 180, 6), ((2, 0, 0), "2", "#000000", -90, 8), ((0, 2, 0), "2", "#000000", -90, 8), ((-1.41, -1.41, 1), "S", lk.BLUE, 150, 8)],
                box=((-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8)),
            )
        ],
        height=lk.H3D,
        key="L22-cylinder",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(beside, cs, ct, lk, np, rect_D):
    # module: parameterized surfaces
    # example: cylinder
    # D = [-1, 1] x [0, 2 pi] with the segment s = s0 (red) and t = t0 (orange), t drawn as t / pi
    _s0, _t0 = float(cs.value), float(ct.value) / np.pi
    _fd = rect_D((-1, 1), 2, [(-1, "$-1$", "black"), (1, "$1$", "black")], [(2, r"$2\pi$", "black")], s0=_s0, t0=_t0)
    beside(_fd.axes[0], (_s0, 2), 90, "$s$", lk.RED, 8, 12)
    beside(_fd.axes[0], (1, _t0), 0, "$t$", lk.ORANGE, 8, 12)
    lk.example(
        [
            r"""
            $\Phi(s, t) = \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \\ s \end{bmatrix}$, &nbsp; $(s, t) \in [-1, 1] \times [0, 2\pi]$

            > $\Longrightarrow$ &nbsp; $\mathrm{Im}(\Phi) = \lbrace (x, y, z) \mid x^2 + y^2 = 4, \ -1 \le z \le 1 \rbrace$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\mathrm{Im}(\Phi)\;$</span>$=$ cylinder of radius $2$ and height $2$
            """,
            lk.interactive(lk.maps(_fd, r"\Phi", lk.frame("L22-cylinder", lk.H3D)), controls=[cs, ct]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(SPHERE_AXES, SPHERE_BOX, lk, np, ss, st):
    # module: parameterized surfaces
    # scene (no visible output; the example below shows it)
    # the sphere S with the images of the segments s = s0 (red: a circle of latitude, the equator for s0 = pi/2) and
    # t = t0 (orange: a meridian); s and t move with the sliders
    _s0, _a = float(ss.value), float(st.value)
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _U = np.linspace(0, np.pi, 61)
    lk.turntable(
        30,
        22,
        "the sphere of radius 2 around the origin, with the circle of latitude s and the meridian at the angle t",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, lk.BLUE, 0.4), (1, 8, lk.BLUE, 0.4)], alpha=0.45)],
                lines=[(2 * np.sin(_s0) * np.cos(_T), 2 * np.sin(_s0) * np.sin(_T), 2 * np.cos(_s0) + 0 * _T, lk.RED, 2.4), (2 * np.sin(_U) * np.cos(_a), 2 * np.sin(_U) * np.sin(_a), 2 * np.cos(_U), lk.ORANGE, 2.4)],
                axes=SPHERE_AXES,
                texts=[((0, 0, 2), "2", "#000000", 150, 6), ((0, 0, -2), "-2", "#000000", 180, 6), ((0, 2, 0), "2", "#000000", -90, 8), ((0, -2, 0), "-2", "#000000", -90, 8), ((0, -1.41, 1.41), "S", lk.BLUE, 150, 8)],
                box=SPHERE_BOX,
            )
        ],
        height=lk.H3D,
        key="L22-sphere",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, np, rect_D, ss, st):
    # module: parameterized surfaces
    # example: sphere
    # D = [0, pi] x [0, 2 pi] with the segment s = s0 (red) and t = t0 (orange); pi is drawn as 1, and t / pi on the
    # vertical axis
    _s0, _t0 = float(ss.value) / np.pi, float(st.value) / np.pi
    _fd = rect_D((0, 1), 2, [(1, r"$\pi$", "black")], [(2, r"$2\pi$", "black")], s0=_s0, t0=_t0)
    beside(_fd.axes[0], (_s0, 2), 90, "$s$", lk.RED, 8, 12)
    beside(_fd.axes[0], (1, _t0), 0, "$t$", lk.ORANGE, 8, 12)
    lk.example(
        [
            r"""
            $\Phi(s, t) = \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix}$, &nbsp; $(s, t) \in [0, \pi] \times [0, 2\pi]$

            > $\Longrightarrow$ &nbsp; $\mathrm{Im}(\Phi) = \lbrace (x, y, z) \mid x^2 + y^2 + z^2 = 4 \rbrace$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\mathrm{Im}(\Phi)\;$</span>$=$ sphere of radius $2$ around $\vec{0}$
            """,
            lk.interactive(lk.maps(_fd, r"\Phi", lk.frame("L22-sphere", lk.H3D)), controls=[ss, st]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(AXES, dome, lk, np, plane):
    # module: parameterized surfaces
    # example: graph
    # D, a rectangle with a grid, and the graph of f over it, with the same grid, the rectangle D in the (x, y)-plane
    # below it (grey) and the vertical lines from the corners of D up to the graph (grey, dashed)
    _a, _b, _c, _d = 0.4, 2.7, 0.3, 2.3
    _fd, _ad = plane((-0.5, 3.6), (-0.4, 3.0), 2.6, names=("$s$", "$t$"))
    _ad.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=lk.LIGHT, lw=0, zorder=0)
    for _x in np.linspace(_a, _b, 7):
        _ad.plot([_x, _x], [_c, _d], color=lk.BLUE, lw=0.6)
    for _y in np.linspace(_c, _d, 6):
        _ad.plot([_a, _b], [_y, _y], color=lk.BLUE, lw=0.6)
    _ad.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=lk.BLUE, lw=1.8)
    _ad.text(_b + 0.25, _d + 0.25, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _u, _v = np.meshgrid(np.linspace(_a, _b, 25), np.linspace(_c, _d, 21), indexing="ij")
    _corners = [(_a, _c), (_b, _c), (_b, _d), (_a, _d)]
    _z = np.linspace(0, 1, 20)
    _S = lk.turntable(
        28,
        32,
        "the graph S of a function f over the rectangle D, z = f(x, y), above the rectangle D in the (x, y)-plane",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_u, _v, dome(_u, _v), wire=[(0, 4, lk.BLUE, 0.5), (1, 4, lk.BLUE, 0.5)]), lk.patch([(x, y, 0) for x, y in _corners], lk.LIGHT, alpha=0.8)],
                lines=[(x + 0 * _z, y + 0 * _z, dome(x, y) * _z, lk.GREY, 1.0, [4, 3]) for x, y in _corners]
                + [([x for x, _ in _corners + _corners[:1]], [y for _, y in _corners + _corners[:1]], [0] * 5, lk.GREY, 1.2)],
                axes=AXES,
                texts=[((_b, _c, float(dome(_b, _c))), "S", lk.BLUE, 180, 8), ((_b, _d, float(dome(_b, _d))), "z = f(x, y)", lk.BLUE, 0, 10)],
            )
        ],
        height=lk.H3D,
    )
    lk.example(
        [
            r"""
            Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $\Phi(s, t) = \begin{bmatrix} s \\ t \\ f(s, t) \end{bmatrix}$, &nbsp; $(s, t) \in D$

            > $\Longrightarrow$ &nbsp; $\mathrm{Im}(\Phi) = \mathrm{graph}(f) \subset \mathbb{R}^3$
            """,
            lk.maps(_fd, r"\Phi", _S),
        ]
    )
    return


@app.cell(hide_code=True)
def _(curve, curve_velocity, lk, np):
    # module: tangent planes
    # tangent line
    # the curve C (blue), the point gamma(t), the velocity vector gamma'(t) (red) and the line through gamma(t) in its
    # direction (green)
    _u0 = 2.3
    _p = np.array([float(c) for c in curve(_u0)])
    _w = curve_velocity(_u0)
    _w = 0.9 * _w / np.linalg.norm(_w)
    _k = np.linspace(-1.3, 1.5, 2)
    _figure = lk.turntable(
        30,
        20,
        "the curve C, the point gamma(t), the velocity vector gamma'(t) at it and the line through gamma(t) in its direction",
        [
            lk.panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), lk.BLUE, 1.8), (_p[0] + _k * _w[0], _p[1] + _k * _w[1], _p[2] + _k * _w[2], lk.GREEN, 1.4)],
                points=[(tuple(_p), "#000000")],
                arrows=[(_p, _p + _w, lk.RED, 2.0)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(tuple(_p), r"\gamma(t)", "#000000", -10, 12), (tuple(_p + _w), r"\gamma'(t)", lk.RED, 120, 10), (tuple(float(c) for c in curve(-3.0)), "C", lk.BLUE, -90, 10)],
                box=((0, 3.0), (0, 3.0), (0, 3.0)),
            )
        ],
        height=lk.H3D,
    )
    lk.prose(
        r"If $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ is differentiable at $t$",
        r"""
        > $\Longrightarrow$ &nbsp; $\gamma'(t) = \begin{bmatrix} x'(t) \\ y'(t) \\ z'(t) \end{bmatrix} \in \mathbb{R}^3$ &nbsp; is the velocity vector of $\gamma$ at $\gamma(t)$
        """,
        lk.aside(
            _figure,
            r"line through $\gamma(t)$ in the direction of $\gamma'(t)$<br>= tangent line to $C$ at $\gamma(t)$ (for $\gamma'(t) \neq \vec{0}$)",
        ),
    )
    return


@app.cell(hide_code=True)
def _(AXES, dome, dome_grid, lk, np):
    # module: tangent planes
    # tangent plane
    # the surface S, the point Phi(s, t), the tangent vectors Phi_s, Phi_t (blue), a combination a Phi_s + b Phi_t (green),
    # the tangent plane (green, translucent) and the normal vector Phi_s x Phi_t (red)
    _x0, _y0 = 1.3, 1.0
    _q = np.array([_x0, _y0, float(dome(_x0, _y0))])
    _ps = 0.75 * np.array([1.0, 0.0, -0.5 * (_x0 - 1.55)])
    _pt = 0.75 * np.array([0.0, 1.0, -0.5 * (_y0 - 1.3)])
    _n = np.cross(_ps, _pt)
    _n = 0.8 * _n / np.linalg.norm(_n)
    _c = 1.0 * _ps + 0.6 * _pt
    _plane = lk.patch([_q - 1.2 * _ps - 1.0 * _pt, _q + 1.4 * _ps - 1.0 * _pt, _q + 1.4 * _ps + 1.6 * _pt, _q - 1.2 * _ps + 1.6 * _pt], lk.GREEN, alpha=0.18)
    _figure = lk.turntable(
        28,
        32,
        "the surface S, the point Phi(s, t), the tangent vectors Phi_s(s, t) and Phi_t(s, t), a combination a Phi_s + b Phi_t, the tangent plane and the normal vector Phi_s x Phi_t",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(*dome_grid(), wire=[(0, 4, lk.BLUE, 0.4), (1, 4, lk.BLUE, 0.4)], alpha=0.6), _plane],
                points=[(tuple(_q), "#000000")],
                arrows=[(_q, _q + _ps, lk.BLUE, 2.0), (_q, _q + _pt, lk.BLUE, 2.0), (_q, _q + _c, lk.GREEN, 2.0), (_q, _q + _n, lk.RED, 2.0)],
                texts=[
                    (tuple(_q), r"\Phi(s, t)", "#000000", 180, 10),
                    (tuple(_q + _ps), r"\Phi_s(s, t)", lk.BLUE, -120, 10),
                    (tuple(_q + _pt), r"\Phi_t(s, t)", lk.BLUE, 30, 10),
                    (tuple(_q + _c), r"a\Phi_s(s, t) + b\Phi_t(s, t)", lk.GREEN, -60, 10),
                    (tuple(_q + _n), r"\Phi_s(s, t) \times \Phi_t(s, t)", lk.RED, 90, 8),
                    ((2.7, 2.3, float(dome(2.7, 2.3))), "S", lk.BLUE, 0, 8),
                ],
                box=((0.4, 2.7), (0.3, 2.3), (1.4, 3.0)),  # the surface only, no axes: it fills the frame
            )
        ],
        height=lk.H3D,
    )
    lk.prose(
        r"If $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ is differentiable at $(s, t)$",
        r"""
        > $\Longrightarrow$ &nbsp; $D\Phi(s, t) = \begin{bmatrix} \frac{\partial x}{\partial s}(s, t) & \frac{\partial x}{\partial t}(s, t) \\[0.3em] \frac{\partial y}{\partial s}(s, t) & \frac{\partial y}{\partial t}(s, t) \\[0.3em] \frac{\partial z}{\partial s}(s, t) & \frac{\partial z}{\partial t}(s, t) \end{bmatrix} \in \mathrm{Mat}(3 \times 2)$

        > $\Longrightarrow$ &nbsp; $\left\lbrace \begin{aligned}
        \Phi_s(s, t) &= \frac{\partial \Phi}{\partial s}(s, t) = \begin{bmatrix} \frac{\partial x}{\partial s}(s, t) \\[0.3em] \frac{\partial y}{\partial s}(s, t) \\[0.3em] \frac{\partial z}{\partial s}(s, t) \end{bmatrix} \in \mathbb{R}^3 \\[0.6em]
        \Phi_t(s, t) &= \frac{\partial \Phi}{\partial t}(s, t) = \begin{bmatrix} \frac{\partial x}{\partial t}(s, t) \\[0.3em] \frac{\partial y}{\partial t}(s, t) \\[0.3em] \frac{\partial z}{\partial t}(s, t) \end{bmatrix} \in \mathbb{R}^3
        \end{aligned} \right.$ &nbsp; are the tangent vectors of $\Phi$ at $\Phi(s, t)$
        """,
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\mk{\Phi_s(s, t) \times \Phi_t(s, t)}$ is normal to $\Phi_s(s, t)$ and $\Phi_t(s, t)$",
            "normal to the tangent plane",
        ),
        lk.aside(
            _figure,
            r"plane through $\Phi(s, t)$ in the<br>direction of $\Phi_s(s, t)$ and $\Phi_t(s, t)$<br>= tangent plane to $S$ at $\Phi(s, t)$<br>(for $\Phi_s(s, t) \times \Phi_t(s, t) \neq \vec{0}$)",
        ),
    )
    return


@app.cell(hide_code=True)
def _(SPHERE_AXES, SPHERE_BOX, lk, np):
    # module: tangent planes
    # example: tangent plane of the sphere
    # the sphere S of radius 2, the point (0, 2, 0), the tangent plane y = 2 there (green, translucent) and the vectors
    # Phi_s, Phi_t and Phi_s x Phi_t at s = t = pi/2 (blue, blue, red)
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _q = np.array([0.0, 2.0, 0.0])
    _plane = lk.patch([(-1.4, 2, -1.4), (1.4, 2, -1.4), (1.4, 2, 1.4), (-1.4, 2, 1.4)], lk.GREEN, alpha=0.2)
    _figure = lk.turntable(
        30,
        18,
        "the sphere of radius 2, the point (0, 2, 0), the tangent plane y = 2 at it and the vectors Phi_s, Phi_t and their cross product there",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, lk.BLUE, 0.4), (1, 8, lk.BLUE, 0.4)], alpha=0.45), _plane],
                lines=[(2 * np.cos(_T), 2 * np.sin(_T), 0 * _T, lk.BLUE, 1.2)],
                points=[(tuple(_q), "#000000")],
                arrows=[(_q, _q + (0, 0, -1.2), lk.BLUE, 2.0), (_q, _q + (-1.2, 0, 0), lk.BLUE, 2.0), (_q, _q + (0, 1.6, 0), lk.RED, 2.0)],
                axes=[((0, 0, 0), (2.6, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", -20), ((0, 0, 0), (0, 0, 2.6), "z", 90)],
                texts=[
                    (tuple(_q + (0, 0, -1.2)), r"\Phi_s(\tfrac{\pi}{2}, \tfrac{\pi}{2})", lk.BLUE, -90, 8),
                    (tuple(_q + (-1.2, 0, 0)), r"\Phi_t(\tfrac{\pi}{2}, \tfrac{\pi}{2})", lk.BLUE, 30, 10),
                    (tuple(_q + (0, 1.6, 0)), r"\Phi_s(\tfrac{\pi}{2}, \tfrac{\pi}{2}) \times \Phi_t(\tfrac{\pi}{2}, \tfrac{\pi}{2})", lk.RED, 0, 8),
                    ((0, -1.41, 1.41), "S", lk.BLUE, 150, 8),
                ],
                box=SPHERE_BOX,
            )
        ],
        height=lk.H3D,
    )
    lk.example(
        [
            r"""
            $\Phi(s, t) = \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix}$, &nbsp; $(s, t) \in [0, \pi] \times [0, 2\pi]$

            > $\Phi_s(s, t) = \begin{bmatrix} 2\cos(s)\cos(t) \\ 2\cos(s)\sin(t) \\ -2\sin(s) \end{bmatrix}$, &nbsp; $\Phi_t(s, t) = \begin{bmatrix} -2\sin(s)\sin(t) \\ 2\sin(s)\cos(t) \\ 0 \end{bmatrix}$

            > > $\leadsto$ &nbsp; $\Phi_s(s, t) \times \Phi_t(s, t) = 2\sin(s) \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix} = 2\sin(s) \, \Phi(s, t)$

            at $s = \frac{\pi}{2}$, $t = \frac{\pi}{2}$

            > $\leadsto$ &nbsp; $\Phi(\tfrac{\pi}{2}, \tfrac{\pi}{2}) = \begin{bmatrix} 0 \\ 2 \\ 0 \end{bmatrix} \in S$, &nbsp; $\Phi_s(\tfrac{\pi}{2}, \tfrac{\pi}{2}) = \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix}$, &nbsp; $\Phi_t(\tfrac{\pi}{2}, \tfrac{\pi}{2}) = \begin{bmatrix} -2 \\ 0 \\ 0 \end{bmatrix}$

            > > $\Longrightarrow$ &nbsp; tangent plane to $S$ at the point $(0, 2, 0)$ is

            $$
            \begin{aligned}
            P &= \left\lbrace \begin{bmatrix} 0 \\ 2 \\ 0 \end{bmatrix} + a \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix} + b \begin{bmatrix} -2 \\ 0 \\ 0 \end{bmatrix} \;\middle|\; a, b \in \mathbb{R} \right\rbrace \\[0.4em]
            &= \left\lbrace \begin{bmatrix} x \\ y \\ z \end{bmatrix} \;\middle|\; y = 2, \ x, z \in \mathbb{R} \right\rbrace
            \end{aligned}
            $$

            $\leadsto$ &nbsp; normal vectors to $P$ at $(0, 2, 0)$ are proportional to &nbsp; $\vec{n} = \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix} \times \begin{bmatrix} -2 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 4 \\ 0 \end{bmatrix}$
            """,
            _figure,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent planes
    # remark: poles
    lk.remark(
        [
            r"At $s = 0$ and $s = \pi$, &nbsp; $2\sin(s) \, \Phi(s, t) = \vec{0}$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; cannot describe tangent plane to $S$ at <span class='lk-mark'>$(0, 0, 2)$ and $(0, 0, -2)$</span> using $\Phi$…",
                r"not regular points for $\Phi$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent planes
    # remark: boundary
    lk.remark(
        r"""
        To be precise $\Phi_s(s, t)$ and $\Phi_t(s, t)$ are not really well-defined along $s = 0, \pi$ and $t = 0, 2\pi$…

        $\leadsto$ &nbsp; but we can extend $\Phi_s(s, t) \times \Phi_t(s, t)$ continuously to the boundary of $[0, \pi] \times [0, 2\pi]$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent planes
    # definition: regular point
    lk.definition(
        r"""
        $\Phi(s, t) \in S$ is called a **regular point** for $\Phi$ if

        $$
        \Phi_s(s, t) \times \Phi_t(s, t) \neq \vec{0}
        $$
        """,
        label="def-regular",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent planes
    # example: graph
    lk.example(
        [
        r"""
        $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable

        > $\Longrightarrow$ &nbsp; $\Phi(s, t) = \begin{bmatrix} s \\ t \\ f(s, t) \end{bmatrix}$ &nbsp; parameterization of $\mathrm{graph}(f)$
        """,
        lk.aside(
        r"""
        $$
        \begin{aligned}
        \Longrightarrow \quad \Phi_s(s, t) \times \Phi_t(s, t) &= \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 0 & \frac{\partial f}{\partial s}(s, t) \\[0.3em] 0 & 1 & \frac{\partial f}{\partial t}(s, t) \end{bmatrix} \\[0.4em]
        &= \begin{bmatrix} -\frac{\partial f}{\partial s}(s, t) \\[0.3em] -\frac{\partial f}{\partial t}(s, t) \\[0.3em] \mk{1} \end{bmatrix} \neq \vec{0}\,!
        \end{aligned}
        $$
        """,
        r"$1 \neq 0$",
        at="last",
        ),
        r"""
        $\Longrightarrow$ &nbsp; all points of $S = \mathrm{graph}(f)$ are regular for $\Phi$
        """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(curve, dt, lk, np):
    # module: area element
    # scene (no visible output; the recall below shows it)
    # the curve C (blue) with the points gamma(t) and gamma(t + Delta t) (red) and the vector from one to the other (red);
    # Delta t moves with the slider
    _u0, _h = 2.0, float(dt.value)
    _p, _q = np.array(curve(_u0)), np.array(curve(_u0 + _h))
    lk.turntable(
        30,
        20,
        "the curve C with the points gamma(t) and gamma(t + Delta t) and the vector from the first to the second",
        [
            lk.panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), lk.BLUE, 1.8)],
                points=[(tuple(_p), lk.RED, 4.0), (tuple(_q), lk.RED, 4.0)],
                arrows=[(_p, _q, lk.RED, 1.6)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(tuple(_p), r"\gamma(t)", lk.RED, -150, 12), (tuple(_q), r"\gamma(t + \Delta t)", lk.RED, -60, 14)],
                box=((0, 3.0), (0, 3.0), (0, 3.0)),
            )
        ],
        height=lk.H3D,
        key="L22-secant",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(dt, lk):
    # module: area element
    # recall: line elements
    lk.recall(
        [
            # the two integrals share their columns (=), and so do ds and d\vec{s}
            r"$$\hphantom{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}\mathllap{\int_C f \, ds} = \mathrlap{\int_I f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt}\hphantom{\int_I \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt}$$",
            lk.aside(r"$$\hphantom{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}\mathllap{\int_{\mk{\vec{C}}} \vec{F} \cdot d\vec{s}} = \int_I \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt$$", "oriented curve"),
            lk.gap(),
            lk.aside(
                r"$$\mathllap{\mk{ds}} = \mathrlap{\lVert \gamma'(t) \rVert \, dt = \lim_{\Delta t \to 0} \left\lVert \frac{\gamma(t + \Delta t) - \gamma(t)}{\Delta t} \right\rVert dt}\hphantom{\lVert \gamma'(t) \rVert \, dt = \lim_{\Delta t \to 0} \left\lVert \frac{\gamma(t + \Delta t) - \gamma(t)}{\Delta t} \right\rVert dt}$$",
                "infinitesimal length element",
            ),
            lk.aside(
                r"$$\mathllap{\mk{d\vec{s}}} = \mathrlap{\gamma'(t) \, dt = \lim_{\Delta t \to 0} \frac{\gamma(t + \Delta t) - \gamma(t)}{\Delta t} \, dt}\hphantom{\lVert \gamma'(t) \rVert \, dt = \lim_{\Delta t \to 0} \left\lVert \frac{\gamma(t + \Delta t) - \gamma(t)}{\Delta t} \right\rVert dt}$$",
                "infinitesimal line element",
            ),
            lk.interactive(lk.frame("L22-secant", lk.H3D), controls=[dt]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(dd, lk, np):
    # module: area element
    # scene (no visible output; the lines below show it)
    # the image on S of the small square: the patch (tinted), its corners, the vectors u and v along its sides from
    # Phi(s, t) (green) and u x v (red); Delta s = Delta t moves with the slider
    _x0, _y0, _dx, _dy = 0.8, 0.6, 1.3 * float(dd.value), 1.2 * float(dd.value)
    # a bowl-shaped surface here (not the dome): its chords u and v then lie above it, in sight
    _f = lambda x, y: 1.4 + 0.25 * ((x - 1.55) ** 2 + (y - 1.3) ** 2)
    _P = lambda x, y: np.array([x, y, float(_f(x, y))])
    _o, _a1, _b1, _ab = _P(_x0, _y0), _P(_x0 + _dx, _y0), _P(_x0, _y0 + _dy), _P(_x0 + _dx, _y0 + _dy)
    _u, _v = _a1 - _o, _b1 - _o
    _n = np.cross(_u, _v)
    _n = 0.9 * _n / np.linalg.norm(_n)
    _gu, _gv = np.meshgrid(np.linspace(0.4, 2.7, 24), np.linspace(0.3, 2.3, 21), indexing="ij")
    lk.turntable(
        -35,
        38,
        "the surface S with the image of the small square: a curved patch with corners Phi(s, t), Phi(s + Delta s, t), Phi(s, t + Delta t), Phi(s + Delta s, t + Delta t), the vectors u and v along its sides and u x v",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_gu, _gv, _f(_gu, _gv), wire=[(0, 4, lk.BLUE, 0.4), (1, 4, lk.BLUE, 0.4)], tint=(_x0, _x0 + _dx + 0.01, _y0, _y0 + _dy + 0.01))],
                points=[(tuple(c), "#000000", 3.5) for c in (_o, _a1, _b1, _ab)],
                arrows=[(_o, _a1, lk.GREEN, 2.0), (_o, _b1, lk.GREEN, 2.0), (_o, _o + _n, lk.RED, 1.8)],
                box=((0.4, 2.7), (0.3, 3.1), (1.3, 2.6)),  # the surface only, no axes: it fills the frame
                texts=[
                    (tuple(_o), r"\Phi(s, t)", "#000000", -150, 10),
                    (tuple(_a1), r"\Phi(s + \Delta s, t) = \Phi(s, t) + \vec{u}", "#000000", -60, 10),
                    (tuple(_b1), r"\Phi(s, t + \Delta t) = \Phi(s, t) + \vec{v}", "#000000", 35, 10),
                    (tuple(_ab), r"\Phi(s + \Delta s, t + \Delta t)", "#000000", 0, 10),
                    (tuple((_o + _a1) / 2), r"\vec{u}", lk.GREEN, -150, 6),
                    (tuple((_o + _b1) / 2), r"\vec{v}", lk.GREEN, 140, 10),
                    (tuple(_o + _n), r"\vec{u} \times \vec{v}", lk.RED, 150, 8),
                    ((2.7, 2.3, float(_f(2.7, 2.3))), "S", lk.BLUE, 0, 8),
                ],
            )
        ],
        height=lk.H3D,
        key="L22-patch",
        apart=True,
    )
    return



@app.cell(hide_code=True)
def _(beside, dd, lk, plane):
    # module: area element
    # similarly: area elements
    # the square [s, s + Delta s] x [t, t + Delta t] (blue, its two sides from (s, t) red), and its image on S (scene above)
    _b, _c = 1.2 + 1.4 * float(dd.value), 0.7 + 1.3 * float(dd.value)
    _fd, _ad = plane((-0.4, 4.0), (-0.4, 3.0), 2.6, names=("$s$", "$t$"))
    _ad.fill([1.2, _b, _b, 1.2], [0.7, 0.7, _c, _c], color=lk.LIGHT, lw=0, zorder=0)
    _ad.plot([1.2, _b, _b, 1.2, 1.2], [0.7, 0.7, _c, _c, 0.7], color=lk.BLUE, lw=1.6)
    lk.arrow(_ad, (1.2, 0.7), (_b, 0.7), lk.RED, lw=1.8)
    lk.arrow(_ad, (1.2, 0.7), (1.2, _c), lk.RED, lw=1.8)
    for _p, _n, _a in (((1.2, 0.7), "$(s, t)$", -110), ((_b, 0.7), r"$(s + \Delta s, t)$", -70), ((1.2, _c), r"$(s, t + \Delta t)$", 110), ((_b, _c), r"$(s + \Delta s, t + \Delta t)$", 70)):
        _ad.plot(*_p, "o", color="black", ms=4, zorder=6)
        beside(_ad, _p, _a, _n, "black", 60 if "Delta" in _n else 30, 14, gap=0, fontsize=11)
    lk.prose(
        "Similarly,",
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \mk{dA} &= \lim_{\substack{\Delta s \to 0 \\ \Delta t \to 0}} \left\lVert \frac{\big(\Phi(s + \Delta s, t) - \Phi(s, t)\big) \times \big(\Phi(s, t + \Delta t) - \Phi(s, t)\big)}{\Delta s \, \Delta t} \right\rVert dsdt \\
            &= \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt
            \end{aligned}
            $$
            """,
            "infinitesimal area element",
        ),
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \mk{d\vec{A}} &= \lim_{\substack{\Delta s \to 0 \\ \Delta t \to 0}} \frac{\big(\Phi(s + \Delta s, t) - \Phi(s, t)\big) \times \big(\Phi(s, t + \Delta t) - \Phi(s, t)\big)}{\Delta s \, \Delta t} \, dsdt \\
            &= \Phi_s(s, t) \times \Phi_t(s, t) \, dsdt
            \end{aligned}
            $$
            """,
            "infinitesimal surface element",
        ),
        lk.aside(lk.interactive(lk.maps(_fd, r"\Phi", lk.frame("L22-patch", lk.H3D)), controls=[dd]), r"$A \approx \lVert \vec{u} \times \vec{v} \rVert$"),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: surface integrals
    # definition: surface integral and flux
    lk.definition(
        [
            r"""
            The **surface integral** of $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ over $S$ is

            $$
            \iint_S f \, dA = \iint_D f(\Phi(s, t)) \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt
            $$

            The **flux** of $\vec{F} : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ across $\vec{S}$ is
            """,
            lk.aside(
                r"$$\iint_{\mk{\vec{S}}} \vec{F} \cdot d\vec{A} = \iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt$$",
                r"$\vec{S}$ oriented surface (next time!)",
            ),
        ],
        label="def-surface-integral",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: surface integrals
    # example: sphere
    lk.example(
        [
            r"""
            $S = \Phi([0, \pi] \times [0, 2\pi])$, &nbsp; $\Phi(s, t) = \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix}$

            $f(x, y, z) = 1$, &nbsp; $\vec{F}(x, y, z) = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$
            """,
            lk.aside(
            r"""
            $$
            \begin{aligned}
            \iint_S f \, dA &= \iint_{[0, \pi] \times [0, 2\pi]} 1 \, \lVert \overbrace{\Phi_s(s, t) \times \Phi_t(s, t)}^{\mathclap{\footnotesize 2\sin(s) \, \Phi(s, t)}} \rVert \, dsdt \\
            &= \int_0^{2\pi} \left( \int_0^{\pi} 1 \, \lvert 4\sin(s) \rvert \, ds \right) dt = \int_0^{2\pi} \big( -4\cos(s) \big) \Big|_{s=0}^{s=\pi} \, dt \\
            &= 2\pi \big( 4 - (-4) \big) = \mk{16\pi}
            \end{aligned}
            $$
            """,
            r"$= 4\pi r^2$, with $r = 2$",
            at="last",
            ),
            r"""
            $$
            \begin{aligned}
            \iint_{\vec{S}} \vec{F} \cdot d\vec{A} &= \iint_{[0, \pi] \times [0, 2\pi]} \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} \cdot \left( 2\sin(s) \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix} \right) dsdt \\
            &= \int_0^{\pi} \int_0^{2\pi} 4(\sin(s))^2 \cos(t) \, dt \, ds \\
            &= \int_0^{\pi} 4(\sin(s))^2 \big( \sin(t) \big) \Big|_{t=0}^{t=2\pi} \, ds = 0
            \end{aligned}
            $$
            """,
        ]
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
    # exercise: cone
    lk.exercise(
        r"""
        $$
        \Phi(s, t) = \begin{bmatrix} s\cos(t) \\ s\sin(t) \\ s \end{bmatrix}, \qquad (s, t) \in [-2, 2] \times [0, 2\pi]
        $$

        a) describe $S = \mathrm{Im}(\Phi)$ with an equation in $x, y, z$

        b) sketch $S = \mathrm{Im}(\Phi)$

        c) find the tangent plane to $S$ at $\Phi(1, \frac{\pi}{2})$
        """,
        label="ex-cone",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: cone, integrals
    lk.exercise(
        r"""
        For the same $S$ as above

        a) calculate the surface integral of $f(x, y, z) = z^2$

        b) calculate the flux of

        $$
        \vec{F}(x, y, z) = \begin{bmatrix} -y \\ x \\ z \end{bmatrix}
        $$
        """,
        label="ex-cone-integrals",
    )
    return


if __name__ == "__main__":
    app.run()
