import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 23 · Surface integrals of vector fields", css_file="lecturekit/style.css")


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
    lk.lecture(23, "Surface integrals of vector fields")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points) and the curve C of the 3D figures

    def drawing(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges;
        the scale never changes with a slider (names are kept inside the ranges)."""
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

    _d, _N = np.array([-0.55, 0.83, 0.0]), np.array([0.83, 0.55, 0.0])

    def curve(u):
        """A curve in R^3 with one loop; u runs over [-3.6, 3.6]. It lies near the vertical plane through (1.3, 1.5, 0)
        in the direction d, so that x, y and z all vary; it leaves that plane slowly in the direction N, so that the
        loop passes over itself and does not cross itself."""
        u = np.asarray(u, float)
        a, h = 0.7 * (0.5 * u - np.sin(u)), 1.5 - 0.9 * np.cos(u) + 0.08 * u
        e = 0.15 * u
        return 1.3 + a * _d[0] + e * _N[0], 1.5 + a * _d[1] + e * _N[1], h

    def curve_velocity(u):
        return 0.7 * (0.5 - math.cos(u)) * _d + 0.15 * _N + np.array([0.0, 0.0, 0.9 * math.sin(u) + 0.08])

    def curve_side(u, sign=1):
        """A unit vector at curve(u), perpendicular to the curve in its plane, on its upper side for sign = 1: names of
        points are put there, in space, so that they turn with the figure."""
        n = np.cross(_N, curve_velocity(u))
        n = n / np.linalg.norm(n)
        return sign * (n if n[2] >= 0 else -n)
    return beside, curve, curve_side, plane, drawing


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    ps = lk.slider(0, 2, step=0.05, value=1.25, label="$s$")
    pt = lk.slider(0, 6.28, step=0.04, value=0.8, label="$t$")
    ss = lk.slider(0, 3.14, step=0.04, value=0.8, label="$s$")
    st = lk.slider(0, 6.28, step=0.04, value=1.04, label="$t$")
    dt = lk.slider(0.1, 1.5, step=0.1, value=1.2, label=r"$\Delta t$")
    return dt, ps, pt, ss, st


@app.cell(hide_code=True)
def _(lk, np, plane):
    # module: recap
    # recap
    # the region D with a point (s, t), and the surface S = Phi(D), the graph of a function over D, with Phi(s, t).
    # D and S are chosen for the drawing only
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

    def _h(x, y):
        return 2.4 - 0.25 * ((x - 1.55) ** 2 + (y - 1.3) ** 2)

    # S = Phi(D) for Phi(s, t) = (s, t, h(s, t)): the graph of h over the same region D, with its wire and rim
    _u, _v = np.meshgrid(np.linspace(0.5, 2.6, 25), np.linspace(0, 1, 25), indexing="ij")
    _L, _H = 0.5 + 0.12 * np.sin(4 * (_u - 0.5)), 2.1 + 0.12 * np.sin(3.5 * (_u - 0.5) + 1)
    _x1, _x2 = _u, _L + _v * (_H - _L)
    _rim = [(_s, _y, _h(_s, _y), lk.BLUE, 1.2) for _y in (_lo, _hi)] + [([_s[_i]] * 30, np.linspace(_lo[_i], _hi[_i], 30), _h(_s[_i], np.linspace(_lo[_i], _hi[_i], 30)), lk.BLUE, 1.2) for _i in (0, -1)]
    _q = (_p[0], _p[1], float(_h(*_p)))
    _surface = lk.turntable(
        28,
        32,
        "the surface S = Phi(D), the graph of a function over the region D, and the point Phi(s, t), the image of the point (s, t) of D",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_x1, _x2, _h(_x1, _x2), wire=[(0, 4, lk.BLUE, 0.5), (1, 4, lk.BLUE, 0.5)])],
                lines=_rim,
                points=[(_q, "#000000")],
                axes=[((0, 0, 0), (2.9, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", -20), ((0, 0, 0), (0, 0, 2.8), "z", 90)],
                texts=[(_q, r"\Phi(s, t)", "#000000", 60, 8), ((2.6, float(_lo[-1]), float(_h(2.6, _lo[-1]))), "S", lk.BLUE, 230, 10)],
            )
        ],
        height=lk.H3D,
        key="L23-surface",
    )

    lk.recap(
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \mk{\Phi} : D \subseteq \mathbb{R}^2 &\longrightarrow \mathbb{R}^3 \\
            (s, t) &\longmapsto \Phi(s, t) = \begin{bmatrix} x(s, t) \\ y(s, t) \\ z(s, t) \end{bmatrix}
            \end{aligned}
            $$
            """,
            r"parameterized surface<br>= parameterization of a surface<br>= $\mathbb{R}^3$-valued 2-variable function",
        ),
        lk.aside(
            r"$$\mk{S} = \mathrm{Im}(\Phi) = \Phi(D) \subset \mathbb{R}^3$$",
            r"2-dimensional surface being parameterized by $\Phi$<br>= subset of $\mathbb{R}^3$",
        ),
        lk.maps(_fd, r"\Phi", _surface, "f", r"$\mathbb{R}$"),
        r"""
        Given $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$

        $$
        \iint\limits_{S = \Phi(D)} f \, dA = \iint_D \underbrace{f(\Phi(s, t)) \, \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert}_{\mathclap{\rule{0pt}{1.3em} \footnotesize \begin{gathered} \text{2-variable scalar valued function over } D \subseteq \mathbb{R}^2 \\ \leadsto \ \text{iterated integrals} \end{gathered}}} \, dsdt \mathllap{\overbrace{\phantom{\lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt}}^{\rule[-0.5em]{0pt}{0.5em} dA}},
        $$
        """,
        lk.aside(
            r"$$\mk{dA} = \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt,$$",
            r"infinitesimal area element of $S$ at $\Phi(s, t)$",
        ),
        r"$$\leadsto \quad \iint_S dA = \text{area of } S.$$",
        lk.aside(
            r"Similar to &nbsp; $\mk{ds} = \lVert \gamma'(t) \rVert \, dt$",
            r"infinitesimal arc-length element of $C$ at $\gamma(t)$",
        ),
        topic="Parameterized surfaces and surface integrals",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.prose(r"""
        Surface integrals of vector fields in $\mathbb{R}^3$ (and examples)
        """),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 7.4, 7.5, 7.6")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # section
    lk.section("Surface integrals of vector fields")
    return


@app.cell(hide_code=True)
def _(lk, np, ps, pt):
    # module: area element of the disk
    # scene (no visible output; the example below shows it)
    # the disk S of radius R in the xy-plane; the circle of radius s (red, the image of the segment s = s0 of D), the
    # radius at the angle t (orange, the image of the segment t = t0), the point Phi(s, t) (black) and the angle t.
    # s and t move with the sliders. R is drawn as 2
    _s0, _t0 = float(ps.value), float(pt.value)
    _r, _a = np.meshgrid(np.linspace(0, 2, 9), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _g = np.linspace(0, 1, 30)
    _e = np.array([np.cos(_t0), np.sin(_t0), 0.0])
    _P = _s0 * _e
    _lines = [
        (_s0 * np.cos(_T), _s0 * np.sin(_T), 0 * _T, lk.RED, 2.2),
        (2 * _e[0] * _g, 2 * _e[1] * _g, 0 * _g, lk.ORANGE, 2.2),
    ]
    _o = np.array([np.cos(_t0 + 2.2), np.sin(_t0 + 2.2), 0.0])
    _arcs, _texts = [], [((-1.45, -1.45, 0.0), "S", lk.BLUE, 200, 10), ((2.0, 0.0, 0.0), "R", "#000000", 0, 10), (tuple(_P), r"\Phi(s, t)", "#000000", -30, 8)]
    if _s0 > 0.3:
        _texts.append((tuple(_s0 * _o), "s", lk.RED, 90, 8))
    if 0.05 < _t0 < 6.24:
        _V = np.linspace(0, _t0, 60)
        _ra = 0.6 if abs(_s0 - 0.6) > 0.25 else 1.1
        _arcs.append((_ra * np.cos(_V), _ra * np.sin(_V), 0 * _V, lk.ORANGE, 1.6))
        _texts.append(((_ra * 1.35 * np.cos(_t0 / 2), _ra * 1.35 * np.sin(_t0 / 2), 0.0), "t", lk.ORANGE, 0, 0))
    lk.turntable(
        30,
        35,
        "the disk S of radius R in the xy-plane, with the circle of radius s, the radius at the angle t, the point Phi(s, t) and the angle t",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_r * np.cos(_a), _r * np.sin(_a), 0 * _r, wire=[(0, 4, lk.BLUE, 0.4)], alpha=0.6)],
                lines=_lines,
                arcs=_arcs,
                points=[(tuple(_P), "#000000")],
                axes=[((0, 0, 0), (2.6, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", -20), ((0, 0, 0), (0, 0, 1.3), "z", 90)],
                texts=_texts,
                box=((-1.7, 1.7), (-1.7, 1.7), (-0.2, 0.5)),
            )
        ],
        height=lk.H3D,
        key="L23-disk",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, np, plane, ps, pt):
    # module: area element of the disk
    # example: polar parameterization of the disk
    # D with the segment s = s0 (red), the segment t = t0 (orange) and the point (s0, t0); R is drawn as 2, and t / pi on
    # the vertical axis
    _s0, _t0 = float(ps.value), float(pt.value)
    _fd, _ad = plane((-0.7, 3.0), (-0.55, 3.1), 2.6, names=("$s$", "$t$"))
    _ad.fill([0, 2, 2, 0], [0, 0, 2, 2], color=lk.LIGHT, lw=0, zorder=0)
    _ad.plot([0, 2, 2, 0, 0], [0, 0, 2, 2, 0], color=lk.BLUE, lw=1.8)
    _ad.plot([_s0, _s0], [0, 2], color=lk.RED, lw=1.8, zorder=3)
    _ad.plot([0, 2], [_t0 / np.pi, _t0 / np.pi], color=lk.ORANGE, lw=1.8, zorder=3)
    _ad.plot(_s0, _t0 / np.pi, "o", color="black", ms=4.5, zorder=6)
    beside(_ad, (_s0, _t0 / np.pi), 45, "$(s, t)$", "black", 34, 14, gap=2)
    beside(_ad, (2, 0), -90, "$R$", "black", 12, 14, gap=6)
    beside(_ad, (0, 2), 180, r"$2\pi$", "black", 20, 14)
    beside(_ad, (_s0, 0), -90, "$s$", lk.RED, 8, 12, gap=6)
    beside(_ad, (0, _t0 / np.pi), 180, "$t$", lk.ORANGE, 8, 12)
    _ad.text(2.12, 2.32, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    lk.example(
        [
            r"""
            $\Phi(s, t) = \begin{bmatrix} s\cos(t) \\ s\sin(t) \\ 0 \end{bmatrix}$, &nbsp; $(s, t) \in [0, R] \times [0, 2\pi]$
            """,
            lk.interactive(lk.maps(_fd, r"\Phi", lk.frame("L23-disk", lk.H3D)), controls=[ps, pt]),
            r"""
            > $\Longrightarrow$ &nbsp; on $xy$-plane &nbsp; $\left\{ \begin{aligned} s &= \text{distance from origin} \\ t &= \text{angle from } x\text{-axis} \end{aligned} \right.$

            $\Phi_s(s, t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ 0 \end{bmatrix}$, &nbsp; $\Phi_t(s, t) = \begin{bmatrix} -s\sin(t) \\ s\cos(t) \\ 0 \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $\Phi_s(s, t) \times \Phi_t(s, t) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \cos(t) & \sin(t) & 0 \\ -s\sin(t) & s\cos(t) & 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ s \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $\lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert = \sqrt{s^2} = s$

            $$
            \begin{aligned}
            \iint\limits_{S = \Phi(D)} dA &= \iint_D \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt \\
            &= \int_0^{2\pi} \left( \int_0^R s \, ds \right) dt = \int_0^{2\pi} \frac{R^2}{2} \, dt = \pi R^2
            \end{aligned}
            $$
            """,
            lk.aside(r"$\leadsto$ &nbsp; $\mk{dA} = s \, dsdt$", "area element for the polar parameterization"),
        ],
        title="polar parameterization of the disk",
    )
    return


@app.cell(hide_code=True)
def _(lk, np, ss, st):
    # module: area element of the sphere
    # scene (no visible output; the example below shows it)
    # the segment s = s0 of D (red) is mapped to a circle of latitude, the segment t = t0 (orange) to a meridian, the point
    # (s0, t0) to Phi(s0, t0) (black); grey guides from the origin to Phi(s0, t0) and to its projection onto the xy-plane,
    # and from there up to Phi(s0, t0); the angle s at the z-axis (red) and the angle t in the xy-plane (orange). s0 and t0
    # move with the sliders. R is drawn as 2; the sphere is translucent, so that the guides and the angles inside it show
    _s0, _t0 = float(ss.value), float(st.value)
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _S = np.linspace(0, np.pi, 61)
    _P = 2 * np.array([np.sin(_s0) * np.cos(_t0), np.sin(_s0) * np.sin(_t0), np.cos(_s0)])
    _g = np.linspace(0, 1, 30)
    _guides = [
        (_P[0] * _g, _P[1] * _g, _P[2] * _g, lk.GREY, 1.0, [4, 3]),
        (_P[0] * _g, _P[1] * _g, 0 * _g, lk.GREY, 1.0, [4, 3]),
        (_P[0] + 0 * _g, _P[1] + 0 * _g, _P[2] * _g, lk.GREY, 1.0, [4, 3]),
    ]
    _arcs, _texts = [], [((0, -1.41, 1.41), "S", lk.BLUE, 150, 8), (tuple(1.15 * _P), r"\Phi(s, t)", "#000000", -40, 12)]
    if _s0 > 0.05:
        _U = np.linspace(0, _s0, 40)
        _arcs.append((0.8 * np.sin(_U) * np.cos(_t0), 0.8 * np.sin(_U) * np.sin(_t0), 0.8 * np.cos(_U), lk.RED, 2.0))
        _texts.append(((1.15 * np.sin(_s0 / 2) * np.cos(_t0), 1.15 * np.sin(_s0 / 2) * np.sin(_t0), 1.15 * np.cos(_s0 / 2)), "s", lk.RED, 0, 0))
    if 0.05 < _t0 < 6.24:
        _V = np.linspace(0, _t0, 60)
        _arcs.append((0.8 * np.cos(_V), 0.8 * np.sin(_V), 0 * _V, lk.ORANGE, 2.0))
        _texts.append(((1.15 * np.cos(_t0 / 2), 1.15 * np.sin(_t0 / 2), 0), "t", lk.ORANGE, 0, 0))
    lk.turntable(
        30,
        22,
        "the sphere of radius R around the origin, with the circle of latitude s, the meridian at the angle t, the point Phi(s, t) and the angles s and t",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, lk.BLUE, 0.4), (1, 8, lk.BLUE, 0.4)], alpha=0.4)],
                lines=[
                    (2 * np.sin(_s0) * np.cos(_T), 2 * np.sin(_s0) * np.sin(_T), 2 * np.cos(_s0) + 0 * _T, lk.RED, 2.4),
                    (2 * np.sin(_S) * np.cos(_t0), 2 * np.sin(_S) * np.sin(_t0), 2 * np.cos(_S), lk.ORANGE, 2.4),
                ]
                + _guides
                + _arcs,  # the angles s and t: plain arcs without heads, as the angle in the 2D figures
                points=[(tuple(_P), "#000000")],
                axes=[((0, 0, 0), (2.5, 0, 0), "x", -150), ((0, 0, 0), (0, 2.5, 0), "y", -20), ((0, 0, 0), (0, 0, 2.5), "z", 90)],
                texts=_texts,
                box=((-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8))  # sphere of radius 2: box 0.9 x radius, as every sphere,
            )
        ],
        height=lk.H3D,
        key="L23-sphere",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, np, plane, ss, st):
    # module: area element of the sphere
    # example: spherical parameterization of the sphere
    # D with the segment s = s0 (red), the segment t = t0 (orange) and the point (s0, t0); pi is drawn as 1.5, and t / pi
    # on the vertical axis
    _s0, _t0 = float(ss.value), float(st.value)
    _x0, _y0 = 1.5 * _s0 / np.pi, _t0 / np.pi
    _fd, _ax = plane((-0.7, 2.9), (-0.55, 3.1), 2.6, names=("$s$", "$t$"))
    _ax.fill([0, 1.5, 1.5, 0], [0, 0, 2, 2], color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot([0, 1.5, 1.5, 0, 0], [0, 0, 2, 2, 0], color=lk.BLUE, lw=1.8)
    _ax.plot([_x0] * 2, [0, 2], color=lk.RED, lw=1.8, zorder=3)
    _ax.plot([0, 1.5], [_y0, _y0], color=lk.ORANGE, lw=1.8, zorder=3)
    _ax.plot(_x0, _y0, "o", color="black", ms=4.5, zorder=6)
    beside(_ax, (_x0, _y0), 45, "$(s, t)$", "black", 34, 14, gap=2)
    beside(_ax, (1.5, 0), -90, r"$\pi$", "black", 12, 14, gap=6)
    beside(_ax, (0, 2), 180, r"$2\pi$", "black", 20, 14)
    beside(_ax, (_x0, 0), -90, "$s$", lk.RED, 8, 12, gap=6)
    beside(_ax, (0, _y0), 180, "$t$", lk.ORANGE, 8, 12)
    _ax.text(1.62, 2.32, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    lk.example(
        [
            r"""
            $\Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$, &nbsp; $(s, t) \in [0, \pi] \times [0, 2\pi]$
            """,
            lk.interactive(lk.maps(_fd, r"\Phi", lk.frame("L23-sphere", lk.H3D)), controls=[ss, st]),
            r"""
            $\left\{ \begin{aligned} s &= \text{angle with } z\text{-axis} \\ t &= \text{angle with } x\text{-axis of the projection} \\ &\phantom{=}\ \text{onto the } xy\text{-plane} \end{aligned} \right.$

            $$
            \begin{aligned}
            \iint_S dA &= \iint_D \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt \\
            &= \int_0^{2\pi} \int_0^{\pi} R^2 \sin(s) \, ds \, dt = 4\pi R^2
            \end{aligned}
            $$
            """,
            lk.aside(r"$\leadsto$ &nbsp; $\mk{dA} = R^2 \sin(s) \, dsdt$", "area element for the spherical parameterization"),
            lk.aside(r"$f(x, y, z) = \mk{z}$", "“height from the equator”"),
            r"""
            $$
            \begin{aligned}
            \iint_S f \, dA &= \int_0^{2\pi} \left( \int_0^{\pi} R\cos(s) \cdot R^2 \sin(s) \, ds \right) dt \\
            &= \int_0^{2\pi} \left( R^3 \, \frac{\sin(s)^2}{2} \bigg|_{s=0}^{s=\pi} \right) dt = 0
            \end{aligned}
            $$
            """,
        ],
        title="spherical parameterization of the sphere",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: surface element
    # lead-in
    lk.prose(r"What about surface integrals of vector fields?")
    return


@app.cell(hide_code=True)
def _(curve, curve_side, dt, lk, np):
    # module: surface element
    # scene (no visible output; the recall below shows it)
    # the curve C (red) with the points gamma(t) and gamma(t + Delta t) (blue) and the vector from one to the other (blue),
    # about gamma'(t) Delta t; Delta t moves with the slider. The names of the points sit in space on either side of the
    # curve; the vector is named at its middle, on the side away from the curve
    _u0, _h = 2.0, float(dt.value)
    _p, _q = np.array(curve(_u0)), np.array(curve(_u0 + _h))
    _m = (_p + _q) / 2
    lk.turntable(
        30,
        20,
        "the curve C with the points gamma(t) and gamma(t + Delta t) and the vector from the first to the second, about gamma'(t) Delta t",
        [
            lk.panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), lk.RED, 1.8)],
                points=[(tuple(_p), lk.BLUE, 4.0), (tuple(_q), lk.BLUE, 4.0)],
                arrows=[(_p, _q, lk.BLUE, 1.6)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[
                    (tuple(_p), r"\gamma(t)", "#000000", -150, 12),
                    (tuple(_q), r"\gamma(t + \Delta t)", "#000000", -60, 14),
                    (tuple(_m), r"\Delta\vec{s} \approx \gamma'(t) \, \Delta t", lk.BLUE, 150, 16),
                ],
                box=((0, 3.0), (0, 3.0), (0, 3.0)),
            )
        ],
        height=lk.H3D,
        key="L23-secant",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(dt, lk):
    # module: surface element
    # recall: curves
    lk.recall(
        [
            r"For curves $C \subset \mathbb{R}^3$ with a parameterization $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$",
            # the two lines share their columns (=, ⇝), so they line up
            lk.aside(r"$$\hphantom{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}\mathllap{\int_C f \, ds} = \mathrlap{\int_I f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt}\hphantom{\int_I f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt} \qquad \leadsto \quad \mathrlap{ds = \lVert \gamma'(t) \rVert \, dt}\hphantom{ds = \lVert \gamma'(t) \rVert \, dt}$$", ""),
            lk.aside(r"$$\hphantom{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}\mathllap{\int_{\mk{\vec{C}}} \vec{F} \cdot d\vec{s}} = \mathrlap{\int_I \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt}\hphantom{\int_I f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt} \qquad \leadsto \quad \mathrlap{\mk{d\vec{s}} = \gamma'(t) \, dt}\hphantom{ds = \lVert \gamma'(t) \rVert \, dt}$$", r"infinitesimal line element<br>($\vec{C}$ oriented)"),
            lk.interactive(lk.frame("L23-secant", lk.H3D), controls=[dt]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: surface element
    # text: surfaces
    # figure: a graph S (chosen for the drawing only), Phi(s, t) = (s, t, f(s, t)), the point Phi(s, t) (black) with its
    # tangent vectors Phi_s and Phi_t (orange), the two coordinate curves through it (grey) with the points Phi(s + Delta s, t)
    # and Phi(s, t + Delta t) (black), and the normal, about Phi_s x Phi_t Delta s Delta t (red). Each name sits beside the
    # tip of its vector, on the far side, or beside its point away from the vectors
    def _f(x1, x2):
        return 2.4 - 0.2 * ((x1 - 1.9) ** 2 + (x2 - 1.7) ** 2)

    _a = (1.3, 1.6)
    _d1, _d2 = -0.4 * (_a[0] - 1.9), -0.4 * (_a[1] - 1.7)
    _fa = float(_f(*_a))
    _lo, _hi, _vv, _D = 0.5, 3.1, 1.5, 0.7
    _x1, _x2 = np.meshgrid(np.linspace(_lo, _hi, 25), np.linspace(_lo, _hi, 25), indexing="ij")
    _w = np.linspace(_lo, _hi, 25)
    _rim = [(_c + 0 * _w, _w) for _c in (_lo, _hi)] + [(_w, _c + 0 * _w) for _c in (_lo, _hi)]
    _W = np.linspace(_lo, _hi, 105)
    _P = np.array([_a[0], _a[1], _fa])
    _fs, _ft = np.array([_vv, 0, _vv * _d1]), np.array([0, _vv, _vv * _d2])
    _n = np.array([-_d1, -_d2, 1.0])
    _Ps = (_a[0] + _D, _a[1], float(_f(_a[0] + _D, _a[1])))
    _Pt = (_a[0], _a[1] + _D, float(_f(_a[0], _a[1] + _D)))
    _figure = lk.figure(
        lk.turntable(
            50,
            30,
            "a surface S with the point Phi(s, t), its tangent vectors Phi_s and Phi_t, the points Phi(s + Delta s, t) and Phi(s, t + Delta t) on the coordinate curves through it, and the normal vector, about Phi_s x Phi_t Delta s Delta t",
            [
                lk.panel(
                    1.0,
                    surfaces=[lk.sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, lk.BLUE, 0.5), (1, 4, lk.BLUE, 0.5)])],
                    lines=[(_c1, _c2, _f(_c1, _c2), lk.BLUE, 1.2) for _c1, _c2 in _rim]
                    + [
                        (_W, _a[1] + 0 * _W, _f(_W, _a[1]), lk.GREY, 2.0, None, 0.1),
                        (_a[0] + 0 * _W, _W, _f(_a[0], _W), lk.GREY, 2.0, None, 0.1),
                    ],
                    points=[(tuple(_P), "#000000"), (_Ps, "#000000"), (_Pt, "#000000")],
                    arrows=[(_P, _P + _fs, lk.ORANGE), (_P, _P + _ft, lk.ORANGE), (_P, _P + _n, lk.RED)],
                    texts=[
                        ((_hi, _lo, _f(_hi, _lo)), "S", lk.BLUE, 200, 8),
                        (tuple(_P), r"\Phi(s, t)", "#000000", 30, 10),
                        (tuple(_P + _n), r"\Delta\vec{A} \approx \Phi_s(s, t) \times \Phi_t(s, t) \, \Delta s \, \Delta t", lk.RED, 45, 8),
                        (tuple(_P + _fs), r"\Phi_s(s, t)", lk.ORANGE, 150, 8),
                        (tuple(_P + _ft), r"\Phi_t(s, t)", lk.ORANGE, 40, 10),
                        (_Ps, r"\Phi(s + \Delta s, t)", "#000000", -120, 14),
                        (_Pt, r"\Phi(s, t + \Delta t)", "#000000", -95, 16),
                    ],
                    axes=[((0, 0, 0), (3.4, 0, 0), "x", -150), ((0, 0, 0), (0, 3.4, 0), "y", -20), ((0, 0, 0), (0, 0, _fa + 1.3), "z", 90)],
                    box=((0, 3.4), (0, 3.4), (0, _fa + 1.3)),
                )
            ],
            height=lk.H3D,
            key="L23-surface-element",
        )
    )
    lk.prose(
        r"Similarly, for a surface $S \subset \mathbb{R}^3$ with a parameterization $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$",
        # the f-lines and the F-lines share their columns (=, ⇝), so they line up
        lk.aside(r"$$\hphantom{\iint_{\vec{S}} \vec{F} \cdot d\vec{A}}\mathllap{\iint_S f \, dA} = \mathrlap{\iint_D f(\Phi(s, t)) \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt},\hphantom{\iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt}$$", ""),
        lk.aside(r"$$\leadsto \quad \mathrlap{dA = \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt},\hphantom{dA = \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt}$$", ""),
        lk.aside(r"$$\hphantom{\iint_{\vec{S}} \vec{F} \cdot d\vec{A}}\mathllap{\iint_{\mk{\vec{S}}} \vec{F} \cdot d\vec{A}} = \mathrlap{\iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt},\hphantom{\iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt}$$", r"$\vec{S}$ oriented"),
        lk.aside(r"$$\leadsto \quad \mathrlap{\mk{d\vec{A}} = \Phi_s(s, t) \times \Phi_t(s, t) \, dsdt}.\hphantom{dA = \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt}$$", "infinitesimal surface element<br>(oriented area element)"),
        _figure,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: orientation
    # definition: orientation
    lk.definition(
        r"""
        An **orientation** of a surface $S$ is a continuous choice of the *direction* of the normal vectors at each point of $S$.
        """,
        label="def-orientation",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: orientation
    # example: disk
    # the disk with the normal vectors n pointing up, and with -n pointing down (red), every vector of length 1/2, at the
    # centre of the disk and on two circles
    _r, _a = np.meshgrid(np.linspace(0, 1, 9), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _disk = lk.sheet(_r * np.cos(_a), _r * np.sin(_a), 0 * _r, wire=[(0, 8, lk.BLUE, 0.6)], alpha=0.85)
    _dp = [np.zeros(3)] + [np.array([_q * np.cos(_v), _q * np.sin(_v), 0.0]) for _q, _m, _o in ((0.45, 6, 0.0), (0.85, 10, 0.3)) for _v in _o + 2 * np.pi * np.arange(_m) / _m]
    _axes = [((0, 0, 0), (1.35, 0, 0), "x", -150), ((0, 0, 0), (0, 1.35, 0), "y", -20), ((0, 0, 0), (0, 0, 0.8), "z", 90)]
    _box = ((-1.0, 1.0), (-1.0, 1.0), (-0.2, 0.5))
    lk.example(
        [
            r"""
            $S$ = disk on the $xy$-plane
            """,
            lk.aside(r'> $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 6.4em">$\hphantom{-}\mk{\vec{n}} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$</span>at each point gives one orientation', "pointing “up”"),
            lk.aside(r'> $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 6.4em">$\mk{-\vec{n}} = \begin{bmatrix} 0 \\ 0 \\ -1 \end{bmatrix}$</span>gives another', "pointing “down”"),
            r"> $\leadsto$ &nbsp; these are the only options",
            lk.figure(
                lk.turntable(
                    30,
                    24,
                    "the disk with the normal vectors n pointing up, and the disk with the normal vectors -n pointing down",
                    [
                        lk.panel(1.0, surfaces=[_disk], axes=_axes, arrows=[(_p, _p + np.array([0, 0, 0.5]), lk.RED, 1.3) for _p in _dp], caption=r"\vec{n}", box=_box),
                        lk.panel(1.0, surfaces=[_disk], axes=_axes, arrows=[(_p, _p - np.array([0, 0, 0.5]), lk.RED, 1.3) for _p in _dp], caption=r"-\vec{n}", box=_box),
                    ],
                    height=lk.H3D_FLAT,
                    cols=2,
                    key="L23-disk-orientations",
                )
            ),
        ],
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: orientation
    # example: sphere
    # the sphere with the normal vectors n pointing out, and with -n pointing in (red), every vector of length 1/2, at
    # points on three circles of latitude and the poles. The sphere is translucent, so that the vectors pointing in show
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _sphere = lk.sheet(np.sin(_s) * np.cos(_t), np.sin(_s) * np.sin(_t), np.cos(_s), wire=[(0, 6, lk.BLUE, 0.4), (1, 9, lk.BLUE, 0.4)], alpha=0.45)
    _sp = [np.array([0, 0, 1.0]), np.array([0, 0, -1.0])] + [
        np.array([np.sin(_u) * np.cos(_v), np.sin(_u) * np.sin(_v), np.cos(_u)]) for _u, _m, _o in ((np.pi / 4, 6, 0.0), (np.pi / 2, 8, 0.4), (3 * np.pi / 4, 6, 0.5)) for _v in _o + 2 * np.pi * np.arange(_m) / _m
    ]
    _axes = [((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 1.8, 0), "y", -20), ((0, 0, 0), (0, 0, 1.8), "z", 90)]
    _box = ((-0.9, 0.9), (-0.9, 0.9), (-0.9, 0.9))
    lk.example(
        [
            r"""
            $S$ = sphere
            """,
            lk.aside(r'> $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 7em">$\hphantom{-}\mk{\vec{n}} = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$</span>gives one orientation', "pointing “out”"),
            lk.aside(r'> $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 7em">$\mk{-\vec{n}} = \begin{bmatrix} -x \\ -y \\ -z \end{bmatrix}$</span>gives another', "pointing “in”"),
            lk.figure(
                lk.turntable(
                    30,
                    24,
                    "the sphere with the normal vectors n pointing out, and the sphere with the normal vectors -n pointing in",
                    [
                        lk.panel(1.0, surfaces=[_sphere], axes=_axes, arrows=[(_p, 1.5 * _p, lk.RED, 1.3) for _p in _sp], caption=r"\vec{n}", box=_box),
                        lk.panel(1.0, surfaces=[_sphere], axes=_axes, arrows=[(_p, 0.5 * _p, lk.RED, 1.3) for _p in _sp], caption=r"-\vec{n}", box=_box),
                    ],
                    height=lk.H3D,
                    cols=2,
                    key="L23-sphere-orientations",
                )
            ),
        ],
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: flux
    # definition: flux
    lk.definition(
        r"""
        Given an oriented surface $\vec{S}$, and a parameterization $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ such that $\Phi_s(s, t) \times \Phi_t(s, t)$ agrees with the orientation, the **flux** of $\vec{F} : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ across $\vec{S}$ is

        $$
        \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt.
        $$
        """,
        label="def-flux",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: flux
    # the sphere of the two flux examples, drawn with a vector field on it
    # the vector fields F(x, y, z) = (x, y, 0) and G(x, y, z) = (x, y, z) on the sphere (green, every arrow at 1/2 of its
    # vector, at the same points: five circles of latitude, eight per circle, every other circle turned by half a step, and
    # the poles, where F is 0). R is drawn as 2
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _pts = [
        2 * np.array([np.sin(_u) * np.cos(_v), np.sin(_u) * np.sin(_v), np.cos(_u)])
        for _i, _u in enumerate(np.pi * np.arange(1, 6) / 6)
        for _v in (_i % 2) * np.pi / 8 + 2 * np.pi * np.arange(8) / 8
    ] + [np.array([0, 0, 2.0]), np.array([0, 0, -2.0])]
    _sphere = lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, lk.BLUE, 0.4), (1, 8, lk.BLUE, 0.4)], alpha=0.85)
    _axes = [((0, 0, 0), (3.6, 0, 0), "x", -150), ((0, 0, 0), (0, 3.6, 0), "y", -20), ((0, 0, 0), (0, 0, 3.4), "z", 90)]
    _box = ((-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8))

    def flux_panel(name, arrows):
        return lk.panel(1.0, surfaces=[_sphere], arrows=arrows, axes=_axes, caption=name, box=_box)

    flux_F = [(_p, _p + 0.5 * np.array([_p[0], _p[1], 0.0]), lk.GREEN, 1.3) for _p in _pts if abs(_p[2]) < 1.99]
    flux_G = [(_p, 1.5 * _p, lk.GREEN, 1.3) for _p in _pts]
    return flux_F, flux_G, flux_panel


@app.cell(hide_code=True)
def _(flux_F, flux_panel, lk):
    # module: flux
    # example: flux of F across the sphere
    lk.example(
        [
            r"$\vec{S}$ = sphere of radius $R$ oriented outward, &nbsp; $\Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$",
            lk.aside(r"$\mk{\vec{F}}(x, y, z) = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$", r"radial vector field along each $z = \text{constant}$ plane"),
            r"""
            $\Phi_s(s, t) \times \Phi_t(s, t) = R\sin(s) \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$, &nbsp; $\vec{F}(\Phi(s, t)) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ 0 \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $\vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) = R^3 \sin(s)^3 \cos(t)^2 + R^3 \sin(s)^3 \sin(t)^2$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big)\;$</span>$= R^3 \sin(s)^3$

            > $\Longrightarrow$ &nbsp; $\displaystyle\iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \int_0^{2\pi} \left( \int_0^{\pi} R^3 \sin(s)^3 \, ds \right) dt = \frac{8\pi R^3}{3}$
            """,
            lk.figure(lk.turntable(30, 22, "the sphere of radius R with the vector field F(x, y, z) = (x, y, 0) on it", [flux_panel(r"\vec{F}", flux_F)], height=lk.H3D, key="L23-flux-F")),
        ],
    )
    return


@app.cell(hide_code=True)
def _(flux_G, flux_panel, lk):
    # module: flux
    # example: flux of G across the sphere, oriented inward
    lk.example(
        [
            r"$\vec{S}$ = sphere of radius $R$ oriented inward, &nbsp; $\Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$",
            r"$\vec{G}(x, y, z) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$",
            lk.aside(
                r"$\Phi_t(s, t) \times \Phi_s(s, t) = -R\sin(s) \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$",
                "agrees with the inward orientation",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $\vec{G}(\Phi(s, t)) \cdot \big( \Phi_t(s, t) \times \Phi_s(s, t) \big) = -R^3 \sin(s) \big( \sin(s)^2 + \cos(s)^2 \big)$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\vec{G}(\Phi(s, t)) \cdot \big( \Phi_t(s, t) \times \Phi_s(s, t) \big)\;$</span>$= -R^3 \sin(s)$

            > $\Longrightarrow$ &nbsp; $\displaystyle\iint_{\vec{S}} \vec{G} \cdot d\vec{A} = -4\pi R^3$
            """,
            lk.figure(lk.turntable(30, 22, "the sphere of radius R with the vector field G(x, y, z) = (x, y, z) on it", [flux_panel(r"\vec{G}", flux_G)], height=lk.H3D, key="L23-flux-G")),
        ],
    )
    return


if __name__ == "__main__":
    app.run()
