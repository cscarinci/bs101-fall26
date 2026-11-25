import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 24 · Stokes' theorem", css_file="lecturekit/style.css")


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
    lk.lecture(24, "Stokes' theorem")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points, arrowheads along a curve, a walking figure)
    # and the same in 3D (arrowheads along a space curve, a walking figure standing on a curve)

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
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8)

    def plane(xlim, ylim, width, names=("$x$", "$y$")):
        """A drawing of a coordinate plane: the two axes as arrows, named at their tips."""
        fig, ax = drawing(xlim, ylim, width)
        lk.arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        lk.arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, names[0], "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, names[1], "black", 10, 12)
        return fig, ax

    def along(ax, x, y, color, at=(0.5,), lw=1.8):
        """Arrowheads on the curve through the points (x[k], y[k]), at the fractions `at` of its points,
        pointing the way the points run."""
        n = len(x)
        for f in at:
            k = round(f * (n - 1))
            j = max(k - max(n // 40, 1), 0)
            ax.annotate("", xy=(x[k], y[k]), xytext=(x[j], y[j]), zorder=5, arrowprops={"arrowstyle": f"->,head_length={4.5 * lw:g},head_width={2 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0})

    def blob(cx, cy, a=1.5, b=0.95):
        """A closed curve run counter-clockwise about the point (cx, cy): two arrays."""
        s = np.linspace(0, 2 * np.pi, 400)
        r = 1 + 0.1 * np.cos(3 * s) + 0.06 * np.sin(2 * s)
        return cx + a * r * np.cos(s), cy + b * r * np.sin(s)

    def heads(x, y, z, color, at, lw=2.0):
        """Arrowheads on the space curve through the points (x[k], y[k], z[k]), at the fractions `at` of its points,
        pointing the way the points run: short arcs of a 3D figure."""
        n = len(x)
        out = []
        for f in at:
            k = round(f * (n - 1))
            j = max(k - max(n // 30, 2), 0)
            out.append((x[j : k + 1], y[j : k + 1], z[j : k + 1], color, lw))
        return out

    def walker3d(foot, up, ahead, h=0.55, color="#000000", lw=1.3):
        """A walking figure of height h standing at `foot` in the direction `up`, facing `ahead`: lines of a 3D figure."""
        foot, up, ahead = (np.asarray(v, float) for v in (foot, up, ahead))
        up = up / np.linalg.norm(up)
        ahead = ahead - (ahead @ up) * up
        ahead = ahead / np.linalg.norm(ahead)

        def at(u, v):
            return foot + h * (u * ahead + v * up)

        def seg(*pts):
            p = np.array([at(u, v) for u, v in pts])
            return (p[:, 0], p[:, 1], p[:, 2], color, lw)

        s = np.linspace(0, 2 * np.pi, 30)
        head = np.array([at(0.13 * np.cos(a), 0.87 + 0.13 * np.sin(a)) for a in s])
        return [
            (head[:, 0], head[:, 1], head[:, 2], color, lw),
            seg((0, 0.74), (0, 0.36)),
            seg((-0.2, 0.46), (0, 0.62), (0.2, 0.46)),
            seg((-0.16, 0), (0, 0.36), (0.16, 0)),
        ]

    return along, beside, blob, drawing, heads, plane, walker3d


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(r"$\vec{S}$ <span class='lk-mark'>oriented</span> surface", "with a choice of normal direction"),
        lk.aside(
            r"$\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ parameterization of $S$ <span class='lk-mark'>compatible with the orientation</span>",
            r"$\Phi_s(s, t) \times \Phi_t(s, t)$ agrees<br>with normal direction",
        ),
        r"""
        $$
        \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt
        $$
        """,
        topic="Surface integrals of vector fields",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"Stokes' theorem (Green for curved surfaces)",
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 8.2, 8.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: opposite orientation
    # remark: opposite orientation
    lk.remark(
        r"""
        $\vec{S}^{\,op} = S$ with opposite orientation

        > $\Longrightarrow$ &nbsp; $\displaystyle\iint_{\vec{S}^{\,op}} \vec{F} \cdot d\vec{A} = -\iint_{\vec{S}} \vec{F} \cdot d\vec{A}$
        """
    )
    return


@app.cell(hide_code=True)
def _(along, beside, blob, lk, plane):
    # module: Green in R3
    # recall: Green's theorem
    # a region D and its boundary curve C = Bd(D) (red), run counter-clockwise
    _x, _y = blob(2.3, 1.6)
    _fig, _ax = plane((-0.6, 5.0), (-0.5, 3.4), 3.4)
    _ax.fill(_x, _y, color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot(_x, _y, color=lk.RED, lw=1.8)
    along(_ax, _x, _y, lk.RED, at=(0.3, 0.62, 0.95))
    _ax.text(2.3, 1.6, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x[250], _y[250]), 225, r"$\vec{C}$", lk.RED, 14, 18)
    lk.recall(
        [
            r"Green's theorem in $\mathbb{R}^2$",
            r"""
            $$
            \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy
            $$
            """,
            lk.aside(
                r"for $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$ on simple region $D \subseteq \mathbb{R}^2$ with boundary $\mk{\vec{C}} = \mathrm{Bd}(D)$",
                r"$\vec{C}$ positively oriented",
            ),
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(blob, heads, lk, np, walker3d):
    # module: Green in R3
    # remark: Green's theorem in R3
    # the region D in the xy-plane (blue) with the "up" orientation, its boundary C (red, counter-clockwise, with two
    # walking figures standing up), and the curl of F (orange) pointing up at points of D
    _th = np.linspace(0, 2 * np.pi, 400)
    _bx, _by = blob(1.0, 1.1, a=0.85, b=0.7)
    _r, _k = np.meshgrid(np.linspace(0, 1, 12), np.arange(400), indexing="ij")
    _sx, _sy = 1.0 + _r * (_bx[_k] - 1.0), 1.1 + _r * (_by[_k] - 1.1)
    _c = (_bx, _by, 0 * _bx)
    _walk = []
    for _i in (20, 230):
        _t = np.array([_bx[_i + 1] - _bx[_i - 1], _by[_i + 1] - _by[_i - 1], 0.0])
        _walk += walker3d((_bx[_i], _by[_i], 0.0), (0, 0, 1), _t, h=0.45)
    _curl = [((1.0 + _u, 1.1 + _v, 0.0), (1.0 + _u, 1.1 + _v, 0.8), lk.ORANGE, 1.4) for _u, _v in ((-0.5, -0.15), (-0.15, 0.4), (0.0, -0.3), (0.45, 0.1), (0.15, 0.05))]
    _fig = lk.turntable(
        30,
        25,
        "the region D in the xy-plane with the up orientation, its boundary curve C run counter-clockwise with two walking figures, and the curl of F pointing up",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_sx, _sy, 0 * _sx, alpha=0.7)],
                lines=[(*_c, lk.RED, 2.0)] + _walk,
                arcs=heads(*_c, lk.RED, (0.2, 0.55, 0.85)),
                arrows=_curl,
                axes=[((0, 0, 0), (2.3, 0, 0), "x", -150), ((0, 0, 0), (0, 2.3, 0), "y", -20), ((0, 0, 0), (0, 0, 1.3), "z", 90)],
                texts=[((float(_bx[60]), float(_by[60]), 0.0), r"\vec{C}", lk.RED, -90, 12), ((1.0, 1.5, 0.0), r"\vec{D}", lk.BLUE, 0, 0)],
                box=((0, 2.2), (0, 2.2), (0, 1.1)),
            )
        ],
        height=lk.H3D,
        zoom=1.15,
        key="L24-green",
    )
    lk.remark(
        [
            r"""
            $\leadsto$ &nbsp; think of $\mathbb{R}^2 \subset \mathbb{R}^3$ as the $z = 0$ $xy$-plane

            > $\Longrightarrow$ &nbsp; $D \subseteq \mathbb{R}^2 \subset \mathbb{R}^3$ is a flat surface in $\mathbb{R}^3$

            extend $\vec{F}$ to $\mathbb{R}^3$ via $\vec{F}(x, y, z) = \begin{bmatrix} P(x, y) \\ Q(x, y) \\ 0 \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $\vec{\nabla} \times \vec{F} = \begin{bmatrix} 0 \\ 0 \\ {\large\tfrac{\partial Q}{\partial x}} - {\large\tfrac{\partial P}{\partial y}} \end{bmatrix}$

            Green &nbsp; $\leadsto$ &nbsp; $\displaystyle\int_{\vec{C}} \vec{F} \cdot d\vec{s} = \iint_{\vec{D}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A}$

            > with $\vec{D}$ given the “up” orientation and $\vec{C} = \mathrm{Bd}(D)$ the positive orientation.
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: boundary of a surface
    # section
    lk.section("Stokes' theorem")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: boundary of a surface
    # lead-in
    lk.prose(r"$\leadsto$ &nbsp; what is the boundary of a surface in $\mathbb{R}^3$?")
    return


@app.cell(hide_code=True)
def _(along, beside, blob, drawing, heads, lk, np, walker3d):
    # module: boundary of a surface
    # definition: boundary of an oriented surface
    # left: the region D with its boundary C = Bd(D) (red, counter-clockwise); right: the dome S = Phi(D) (blue) with its
    # normal vectors (green) and its boundary Bd(S) = Phi(C) (red), with two walking figures standing up on it
    _x, _y = blob(0.0, 0.0, a=1.3, b=0.8)
    _fd, _ad = drawing((-1.9, 1.9), (-1.9, 1.5), 2.4)
    _ad.fill(_x, _y, color=lk.LIGHT, lw=0, zorder=0)
    _ad.plot(_x, _y, color=lk.RED, lw=1.8)
    along(_ad, _x, _y, lk.RED, at=(0.3, 0.62, 0.95))
    _ad.text(0, 0, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    beside(_ad, (_x[300], _y[300]), -90, r"$\vec{C} = \mathrm{Bd}(D)$", lk.RED, 84, 18, gap=12)

    _bx, _by = blob(0.0, 0.0, a=1.5, b=1.5)
    _r, _k = np.meshgrid(np.linspace(0, 1, 16), np.arange(400), indexing="ij")
    _X, _Y = _r * _bx[_k], _r * _by[_k]
    _Z = 1.6 * np.sqrt(np.clip(1 - _r**2, 0, 1))
    _c = (_bx, _by, 0 * _bx)
    _n = []
    for _rr, _kk in ((0.0, 0), (0.6, 40), (0.6, 170), (0.6, 300), (0.9, 100), (0.9, 230), (0.9, 360)):
        _p = np.array([_rr * _bx[_kk], _rr * _by[_kk], 1.6 * np.sqrt(1 - _rr**2)])
        _g = np.array([_p[0] / 1.5**2, _p[1] / 1.5**2, _p[2] / 1.6**2])
        _n.append((_p, _p + 0.55 * _g / np.linalg.norm(_g), lk.GREEN, 1.3))
    _walk = []
    for _i in (70, 150):
        _t = np.array([_bx[_i + 1] - _bx[_i - 1], _by[_i + 1] - _by[_i - 1], 0.0])
        _walk += walker3d((_bx[_i], _by[_i], 0.0), (0, 0, 1), _t, h=0.5)
    _fs = lk.turntable(
        30,
        18,
        "the dome S, the image of D, with its normal vectors and its boundary Bd(S), the image of C, with two walking figures on it",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_X, _Y, _Z, alpha=0.55)],
                lines=[(*_c, lk.RED, 2.0)] + _walk,
                arcs=heads(*_c, lk.RED, (0.15, 0.5, 0.85)),
                arrows=_n,
                texts=[((0.0, -1.3, 0.8), r"\vec{S}", lk.BLUE, 180, 12), ((float(_bx[330]), float(_by[330]), 0.0), r"\mathrm{Bd}(\vec{S}) = \Phi(\vec{C})", lk.RED, -100, 40)],
                box=((-1.6, 1.6), (-1.6, 1.6), (0, 2.0)),
            )
        ],
        height=lk.H3D,
        zoom=1.25,
        key="L24-boundary",
    )
    lk.definition(
        [
            r"""
            Given $\vec{S}$ an oriented surface and $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ a compatible parameterization, define the **boundary** of $\vec{S}$ as the oriented curve

            $$
            \mathrm{Bd}(\vec{S}) = \Phi(\vec{C})
            $$

            where $\vec{C} = \mathrm{Bd}(D)$ with the positive orientation.
            """,
            lk.figure(lk.maps(_fd, r"\Phi", _fs)),
        ],
        label="def-boundary",
    )
    return


@app.cell(hide_code=True)
def _(along, beside, heads, lk, np, plane):
    # module: boundary of a surface
    # example: graph
    # left: the square D with its boundary C (red, counter-clockwise) and a point (s, t); right: S = graph(f) = Phi(D)
    # (blue) over D (drawn in the xy-plane), the point Phi(s, t) with Phi_s and Phi_t (orange) and Phi_s x Phi_t (green),
    # and the boundary Bd(S) = Phi(C) (red), above the boundary of D (red, faint). f is chosen for the drawing only
    def _f(s, t):
        return 2.3 - 0.25 * ((s - 1.9) ** 2 + (t - 1.7) ** 2) + 0.15 * np.sin(2.2 * s)

    _lo, _hi = 0.5, 2.7
    _p = (1.3, 1.6)
    _fd, _ad = plane((-0.5, 3.4), (-0.5, 3.4), 2.6, names=("$s$", "$t$"))
    _sq = np.array([[_lo, _lo], [_hi, _lo], [_hi, _hi], [_lo, _hi], [_lo, _lo]])
    _ad.fill(_sq[:, 0], _sq[:, 1], color=lk.LIGHT, lw=0, zorder=0)
    _ad.plot(_sq[:, 0], _sq[:, 1], color=lk.RED, lw=1.8)
    for _a, _b in zip(_sq[:-1], _sq[1:]):
        _w = np.linspace(0, 1, 40)
        along(_ad, _a[0] + _w * (_b[0] - _a[0]), _a[1] + _w * (_b[1] - _a[1]), lk.RED)
    _ad.plot(*_p, "o", color="black", ms=4.5, zorder=6)
    beside(_ad, _p, 45, "$(s, t)$", "black", 34, 14, gap=2)
    _ad.text(2.95, 3.0, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    beside(_ad, (1.6, _lo), -90, r"$\vec{C} = \mathrm{Bd}(D)$", lk.RED, 84, 18, gap=6)

    _w = np.linspace(_lo, _hi, 60)
    _edges = [(_w, _lo + 0 * _w), (_hi + 0 * _w, _w), (_w[::-1], _hi + 0 * _w), (_lo + 0 * _w, _w[::-1])]
    _bd = [np.concatenate(_v) for _v in zip(*_edges)]
    _rim = (_bd[0], _bd[1], _f(_bd[0], _bd[1]))
    _floor = (_bd[0], _bd[1], 0 * _bd[0])
    _S, _T = np.meshgrid(np.linspace(_lo, _hi, 25), np.linspace(_lo, _hi, 25), indexing="ij")
    _h = 1e-4
    _fs = (_f(_p[0] + _h, _p[1]) - _f(_p[0] - _h, _p[1])) / (2 * _h)
    _ft = (_f(_p[0], _p[1] + _h) - _f(_p[0], _p[1] - _h)) / (2 * _h)
    _P = np.array([_p[0], _p[1], float(_f(*_p))])
    _vs, _vt, _vn = 1.1 * np.array([1, 0, _fs]), 1.1 * np.array([0, 1, _ft]), 0.9 * np.array([-_fs, -_ft, 1.0])
    _fig = lk.turntable(
        40,
        22,
        "the graph S of f over the square D, with the point Phi(s, t), the tangent vectors Phi_s and Phi_t, the normal Phi_s x Phi_t, and the boundary of S above the boundary of D",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_S, _T, _f(_S, _T), wire=[(0, 6, lk.BLUE, 0.4), (1, 6, lk.BLUE, 0.4)], alpha=0.8), lk.patch([(_lo, _lo, 0), (_hi, _lo, 0), (_hi, _hi, 0), (_lo, _hi, 0)], lk.LIGHT, alpha=0.6)],
                lines=[(*_rim, lk.RED, 2.0), (*_floor, lk.RED, 1.2), ([_p[0]] * 2, [_p[1]] * 2, [0, _P[2]], lk.GREY, 1.0, [4, 3])],
                arcs=heads(*_rim, lk.RED, (0.15, 0.4, 0.65, 0.9)) + heads(*_floor, lk.RED, (0.15, 0.4, 0.65, 0.9), lw=1.2),
                points=[(tuple(_P), "#000000"), ((_p[0], _p[1], 0.0), "#000000", 3.0)],
                arrows=[(_P, _P + _vs, lk.ORANGE), (_P, _P + _vt, lk.ORANGE), (_P, _P + _vn, lk.GREEN)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", -20), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[
                    (tuple(_P + _vs), r"\Phi_s(s, t)", lk.ORANGE, 230, 8),
                    (tuple(_P + _vt), r"\Phi_t(s, t)", lk.ORANGE, -50, 8),
                    (tuple(_P + _vn), r"\Phi_s(s, t) \times \Phi_t(s, t)", lk.GREEN, 0, 8),
                    ((_lo, _lo, float(_f(_lo, _lo))), r"S", lk.BLUE, 150, 10),
                    ((_lo, _hi, float(_f(_lo, _hi))), r"\mathrm{Bd}(\vec{S}) = \Phi(\vec{C})", lk.RED, -90, 18),
                    ((_hi, _lo, 0.0), "D", lk.BLUE, 220, 8),
                ],
                caption=r"S = \mathrm{graph}(f) = \Phi(D)",
                box=((0.3, 2.9), (0.3, 2.9), (0, 3.1)),
            )
        ],
        height=lk.H3D,
        key="L24-graph",
    )
    def _updown():
        # S = graph(f) (blue) with one normal vector (green), up on the left and down on the right, its boundary (red) above
        # the square D (light) with its boundary (red): C on the left, C^op on the right
        def _f(s, t):
            return 1.6 + 0.3 * np.sin(1.4 * s) - 0.25 * (t - 1.0) ** 2

        _lo, _hi = 0.0, 2.0
        _w = np.linspace(_lo, _hi, 60)
        _edges = [(_w, _lo + 0 * _w), (_hi + 0 * _w, _w), (_w[::-1], _hi + 0 * _w), (_lo + 0 * _w, _w[::-1])]
        _bx, _by = (np.concatenate(_v) for _v in zip(*_edges))
        _S, _T = np.meshgrid(np.linspace(_lo, _hi, 21), np.linspace(_lo, _hi, 21), indexing="ij")
        _surf = lk.sheet(_S, _T, _f(_S, _T), wire=[(0, 5, lk.BLUE, 0.4), (1, 5, lk.BLUE, 0.4)], alpha=0.8)
        _floor = lk.patch([(_lo, _lo, 0), (_hi, _lo, 0), (_hi, _hi, 0), (_lo, _hi, 0)], lk.LIGHT, alpha=0.6)
        _top = float(_f(1.0, 1.0))

        def _panel(sign, name, caption):
            x, y = (_bx, _by) if sign > 0 else (_bx[::-1], _by[::-1])
            rim, floor = (x, y, _f(x, y)), (x, y, 0 * x)
            return lk.panel(
                1.0,
                surfaces=[_surf, _floor],
                lines=[(*rim, lk.RED, 2.0), (*floor, lk.RED, 1.6)],
                arcs=heads(*rim, lk.RED, (0.15, 0.4, 0.65, 0.9)) + heads(*floor, lk.RED, (0.15, 0.4, 0.65, 0.9), lw=1.6),
                arrows=[((1.0, 1.0, _top), (1.0, 1.0, _top + 0.8 * sign), lk.GREEN, 1.6)],
                texts=[((_hi, _hi, float(_f(_hi, _hi))), r"\mathrm{Bd}(\vec{S})", lk.RED, 20, 8), ((_hi, _hi, 0.0), name, lk.RED, 20, 8)],
                caption=caption,
                box=((_lo, _hi), (_lo, _hi), (0, 2.4)),
            )

        _fig = lk.turntable(
            35,
            22,
            "the graph S with the up orientation, whose boundary runs above C, and with the down orientation, whose boundary runs above the opposite curve",
            [_panel(1, r"\vec{C}", r"\text{“up”}"), _panel(-1, r"\vec{C}^{\,op}", r"\text{“down”}")],
            height=lk.H3D,
            cols=2,
            key="L24-up-down",
        )
        return _fig

    lk.example(
        [
            r"""
            $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$

            > $\Longrightarrow$ &nbsp; $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$, $(s, t) \longmapsto \Phi(s, t) = \begin{bmatrix} s \\ t \\ f(s, t) \end{bmatrix}$<br>is a parameterization of $S = \mathrm{graph}(f)$
            """,
            lk.figure(lk.maps(_fd, r"\Phi", _fig)),
            lk.aside(
                r"$\Phi_s = \begin{bmatrix} 1 \\ 0 \\ f_s \end{bmatrix}$, $\Phi_t = \begin{bmatrix} 0 \\ 1 \\ f_t \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\Phi_s \times \Phi_t = \begin{bmatrix} -f_s \\ -f_t \\ \mk{1} \end{bmatrix}$",
                "always “up”",
            ),
            lk.gap(),
            r"""
            If $\vec{S} = \mathrm{graph}(f)$ with “up” orientation &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{Bd}(\vec{S}) = \Phi(\vec{C})$

            If $\vec{S} = \mathrm{graph}(f)$ with “down” orientation &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{Bd}(\vec{S}) = \Phi(\vec{C}^{\,op})$
            """,
            lk.figure(_updown()),
        ],
        label="ex-graph",
    )
    return


@app.cell(hide_code=True)
def _(beside, heads, lk, np, plane, walker3d):
    # module: boundary of a surface
    # example: upper hemisphere
    # top: the disk D with its boundary circle C (red); the hemisphere S = Phi(D) (blue) with its boundary circle (red).
    # bottom: the hemisphere with the "out" orientation (normals, green, pointing out; boundary counter-clockwise, walking
    # figures standing up) and with the "in" orientation (normals pointing in; boundary clockwise, figures upside down).
    # R is drawn as 2
    _fd, _ad = drawing((-3.4, 4.6), (-3.2, 3.0), 3.4)
    lk.arrow(_ad, (-2.7, 0), (2.9, 0), "black", lw=0.9)
    lk.arrow(_ad, (0, -2.5), (0, 2.8), "black", lw=0.9)
    beside(_ad, (2.9, 0), 0, "$s$", "black", 10, 12)
    beside(_ad, (0, 2.8), 90, "$t$", "black", 10, 12)
    _a = np.linspace(0, 2 * np.pi, 200)
    _ad.fill(2 * np.cos(_a), 2 * np.sin(_a), color=lk.LIGHT, lw=0, zorder=0)
    _ad.plot(2 * np.cos(_a), 2 * np.sin(_a), color=lk.RED, lw=1.8)
    _ad.text(1.6, 1.75, r"$D = \lbrace s^2 + t^2 \leqslant R^2 \rbrace$", color=lk.BLUE, fontsize=13, ha="left", va="bottom")
    _ad.text(0.6, -2.75, r"$C = \mathrm{Bd}(D) = \lbrace s^2 + t^2 = R^2 \rbrace$", color=lk.RED, fontsize=13, ha="center", va="top")

    _s, _t = np.meshgrid(np.linspace(0, np.pi / 2, 13), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _hemi = lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), alpha=0.35)
    _circ = (2 * np.cos(_a), 2 * np.sin(_a), 0 * _a)
    _axes = [((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", -20), ((0, 0, 0), (0, 0, 2.7), "z", 90)]
    _box = ((-1.8, 1.8), (-1.8, 1.8), (0, 1.8))
    _outline = [("sphere", (0, 0, 0), 2.0, lk.BLUE, 1.2)]
    _fs = lk.turntable(
        30,
        18,
        "the upper hemisphere S of radius R, the image of the disk D, with its boundary circle in the xy-plane",
        [lk.panel(1.0, surfaces=[_hemi], lines=[(*_circ, lk.RED, 2.0)], axes=_axes, texts=[((0.0, 1.41, 1.41), "S", lk.BLUE, 30, 10), ((1.0, 1.73, 0.0), r"\mathrm{Bd}(S)", lk.RED, -60, 12)], box=_box)],
        height=lk.H3D,
        zoom=1.2,
        key="L24-hemisphere",
    )

    _pts = [np.array([np.sin(_u) * np.cos(_v), np.sin(_u) * np.sin(_v), np.cos(_u)]) for _u, _m, _o in ((0.0, 1, 0.0), (np.pi / 4, 6, 0.0), (np.pi / 2.6, 8, 0.4)) for _v in _o + 2 * np.pi * np.arange(_m) / _m]

    def _panel(sign, caption):
        c = _circ if sign > 0 else tuple(v[::-1] for v in _circ)
        walk = []
        for i in (25, 125):
            p = np.array([2 * np.cos(_a[i]), 2 * np.sin(_a[i]), 0.0])
            tang = sign * np.array([-np.sin(_a[i]), np.cos(_a[i]), 0.0])
            walk += walker3d(p + 0.12 * p, (0, 0, sign), tang, h=0.55)
        return lk.panel(
            1.0,
            surfaces=[_hemi],
            lines=[(*c, lk.RED, 2.0)] + walk,
            arcs=heads(*c, lk.RED, (0.2, 0.45, 0.7, 0.95)),
            arrows=[(2 * _p, 2 * _p + 0.6 * sign * _p, lk.GREEN, 1.3) for _p in _pts],
            caption=caption,
            box=((-1.8, 1.8), (-1.8, 1.8), (-0.4, 1.8)),
        )

    _fo = lk.turntable(
        30,
        18,
        "the upper hemisphere with the out orientation, its boundary counter-clockwise with walking figures standing up, and with the in orientation, its boundary clockwise with walking figures upside down",
        [_panel(1, r"\text{“out”}"), _panel(-1, r"\text{“in”}")],
        height=lk.H3D,
        cols=2,
        zoom=1.15,
        key="L24-out-in",
    )
    lk.example(
        [
            r"$f(x, y) = \sqrt{R^2 - x^2 - y^2}$, $D = \lbrace (x, y) \mid x^2 + y^2 \leqslant R^2 \rbrace$",
            lk.figure(lk.maps(_fd, r"\Phi", _fs)),
            r"""
            $\vec{S} = \lbrace x^2 + y^2 \leqslant R^2, \ z = \sqrt{R^2 - x^2 - y^2} \rbrace$ with “out” orientation

            > $\Longrightarrow$ &nbsp; $\mathrm{Bd}(\vec{S}) = \lbrace x^2 + y^2 = R^2, \ z = 0 \rbrace$ counter-clockwise in the $xy$-plane

            $\vec{S} = \lbrace x^2 + y^2 \leqslant R^2, \ z = \sqrt{R^2 - x^2 - y^2} \rbrace$ with “in” orientation

            > $\Longrightarrow$ &nbsp; $\mathrm{Bd}(\vec{S}) = \lbrace x^2 + y^2 = R^2, \ z = 0 \rbrace$ clockwise in the $xy$-plane
            """,
            lk.figure(_fo),
        ],
        label="ex-hemisphere",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: boundary of a surface
    # remark: how to find the orientation of the boundary
    lk.remark(
        r"""
        $\leadsto$ &nbsp; walking along $\mathrm{Bd}(\vec{S})$ standing along the normal of $\vec{S}$, the surface is to your left.

        $\leadsto$ &nbsp; right-hand rule: right thumb along the normal of $\vec{S}$, fingers follow $\mathrm{Bd}(\vec{S})$.
        """
    )
    return


@app.cell(hide_code=True)
def _(beside, heads, lk, np, plane):
    # module: closed surfaces
    # example: sphere
    # left: the rectangle [0, pi] x [0, 2 pi] with its four edges, run counter-clockwise: t = 0 (red), s = pi (green),
    # t = 2 pi (blue), s = 0 (orange); right: their images on the sphere: two meridians, the same curve run both ways (red
    # and blue, drawn a little apart), and the two poles (green, orange). pi is drawn as 1.5, and t / pi on the vertical axis
    _fd, _ad = plane((-0.8, 2.6), (-0.5, 3.0), 2.2, names=("$s$", "$t$"))
    _ad.fill([0, 1.5, 1.5, 0], [0, 0, 2, 2], color=lk.LIGHT, lw=0, zorder=0)
    _w = np.linspace(0, 1, 40)
    for (_a, _b), _col in zip((((0, 0), (1.5, 0)), ((1.5, 0), (1.5, 2)), ((1.5, 2), (0, 2)), ((0, 2), (0, 0))), (lk.RED, lk.GREEN, lk.BLUE, lk.ORANGE)):
        _x, _y = _a[0] + _w * (_b[0] - _a[0]), _a[1] + _w * (_b[1] - _a[1])
        _ad.plot(_x, _y, color=_col, lw=2.0, zorder=3)
        _ad.annotate("", xy=(_x[24], _y[24]), xytext=(_x[18], _y[18]), zorder=4, arrowprops={"arrowstyle": "->,head_length=8,head_width=3.6", "mutation_scale": 1, "color": _col, "lw": 2.0, "shrinkA": 0, "shrinkB": 0})
    beside(_ad, (1.5, 0), -90, r"$\pi$", "black", 12, 14, gap=6)
    beside(_ad, (0, 2), 180, r"$2\pi$", "black", 20, 14)

    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _S = np.linspace(0, np.pi, 80)

    def _meridian(t, run):
        x, y, z = 2 * np.sin(_S) * np.cos(t), 2 * np.sin(_S) * np.sin(t), 2 * np.cos(_S)
        return (x, y, z) if run > 0 else (x[::-1], y[::-1], z[::-1])

    _red, _blue = _meridian(-0.022, 1), _meridian(0.022, -1)
    _fs = lk.turntable(
        38,
        12,
        "the sphere with the images of the four edges: the meridian Phi(s, 0) run from the north pole to the south pole, the same meridian Phi(s, 2 pi) run back, and the two poles",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), alpha=0.3)],
                lines=[(*_red, lk.RED, 2.0), (*_blue, lk.BLUE, 2.0)],
                arcs=heads(*_red, lk.RED, (0.4,)) + heads(*_blue, lk.BLUE, (0.4,)),
                points=[((0, 0, 2.0), lk.ORANGE, 5.5), ((0, 0, -2.0), lk.GREEN, 5.5)],
                outlines=[("sphere", (0, 0, 0), 2.0, lk.BLUE, 1.2)],
                texts=[(tuple(v[60] for v in _red), r"\Phi(s, 0)", lk.RED, 0, 18), (tuple(v[45] for v in _blue), r"\Phi(s, 2\pi)", lk.BLUE, 180, 30)],
                box=((-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8)),
            )
        ],
        height=lk.H3D,
        key="L24-sphere",
    )
    lk.example(
        [
            r"$\vec{S} = \lbrace x^2 + y^2 + z^2 = R^2 \rbrace$ with “out” orientation",
            lk.aside(
                r"$\Phi : [0, \pi] \times [0, 2\pi] \longrightarrow \mathbb{R}^3$, $\Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$",
                "spherical parameterization",
            ),
            r"$\Phi_s \times \Phi_t = R\sin(s) \, \Phi$ &nbsp; $\Longrightarrow$ &nbsp; $\Phi$ is compatible with $\vec{S}$",
            lk.aside(
                r"> $\begin{aligned} \Longrightarrow \quad \mathrm{Bd}(\vec{S}) &= \Phi\big( \mathrm{Bd}([0, \pi] \times [0, 2\pi]) \big) \\ &= \mk{\Phi([0, \pi] \times \lbrace 0 \rbrace) \cup \Phi([0, \pi] \times \lbrace 2\pi \rbrace)} \\ &\phantom{=}\qquad {} \cup {} \mk{\Phi(\lbrace \pi \rbrace \times [0, 2\pi]) \cup \Phi(\lbrace 0 \rbrace \times [0, 2\pi])} \end{aligned}$",
                [(2, "same curve, opposite orientation"), (3, "points")],
                rows=3,
            ),
            lk.figure(lk.maps(_fd, r"\Phi", _fs)),
            r"""
            $\leadsto$ &nbsp; by convention: no points in $\mathrm{Bd}(\vec{S})$, and curves with opposite orientation “cancel”
            """,
            lk.aside(r"> $\Longrightarrow$ &nbsp; $\mathrm{Bd}(\vec{S}) = \emptyset$", "the sphere has no boundary"),
        ],
        label="ex-sphere",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: closed surfaces
    # definition: closed surface
    lk.definition(
        r"$\vec{S} \subset \mathbb{R}^3$ with $\mathrm{Bd}(\vec{S}) = \emptyset$ is called a **closed surface** in $\mathbb{R}^3$.",
        label="def-closed",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Stokes' theorem
    # theorem: Stokes
    lk.theorem(
        r"""
        Given $\vec{S}$ oriented surface and $\vec{F}$ a vector field

        $$
        \int_{\mathrm{Bd}(\vec{S})} \vec{F} \cdot d\vec{s} = \iint_{\vec{S}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A}
        $$
        """,
        title="Stokes' theorem",
        label="thm-stokes",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Stokes' theorem
    # corollary: closed surfaces
    lk.corollary(
        [
            r"In particular, if $\mathrm{Bd}(\vec{S}) = \emptyset$,",
            lk.aside(r"$$\iint_{\mk{\vec{S}}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} = 0$$", "closed surface"),
        ],
        label="cor-closed",
    )
    return


@app.cell(hide_code=True)
def _(heads, lk, np):
    # module: Stokes' theorem
    # example: F = (-y, x, 1) over the upper hemisphere
    # the upper hemisphere oriented up (normals, green) and its boundary circle (red, counter-clockwise). R is drawn as 2
    _s, _t = np.meshgrid(np.linspace(0, np.pi / 2, 13), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _a = np.linspace(0, 2 * np.pi, 200)
    _c = (2 * np.cos(_a), 2 * np.sin(_a), 0 * _a)
    _pts = [np.array([np.sin(_u) * np.cos(_v), np.sin(_u) * np.sin(_v), np.cos(_u)]) for _u, _m, _o in ((0.0, 1, 0.0), (np.pi / 4, 6, 0.0), (np.pi / 2.6, 8, 0.4)) for _v in _o + 2 * np.pi * np.arange(_m) / _m]
    _fig = lk.turntable(
        30,
        18,
        "the upper hemisphere oriented up, with its boundary circle run counter-clockwise",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), alpha=0.35)],
                lines=[(*_c, lk.RED, 2.0)],
                arcs=heads(*_c, lk.RED, (0.2, 0.45, 0.7, 0.95)),
                arrows=[(2 * _p, 2.3 * _p, lk.GREEN, 1.3) for _p in _pts],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", -20), ((0, 0, 0), (0, 0, 2.9), "z", 90)],
                texts=[((-1.0, -1.0, 1.41), r"\vec{S}", lk.BLUE, 150, 14), ((-0.35, -1.97, 0.0), r"\mathrm{Bd}(\vec{S})", lk.RED, 200, 18)],
                box=((-1.8, 1.8), (-1.8, 1.8), (0, 2.2)),
            )
        ],
        height=lk.H3D,
        zoom=1.2,
        key="L24-stokes-example",
    )
    lk.example(
        [
            r"""
            $\vec{F}(x, y, z) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$, $\vec{S} = \lbrace x^2 + y^2 \leqslant R^2, \ z = \sqrt{R^2 - x^2 - y^2} \rbrace$ oriented “up”

            $\vec{\nabla} \times \vec{F} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ -y & x & 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$

            $\Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}$, &nbsp; $(s, t) \in [0, \pi/2] \times [0, 2\pi]$

            $$
            \begin{aligned}
            \Longrightarrow \quad \iint_{\vec{S}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} &= \int_0^{2\pi} \int_0^{\pi/2} \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix} \cdot \big( R\sin(s) \, \Phi(s, t) \big) \, ds \, dt \\
            &= \int_0^{2\pi} \int_0^{\pi/2} 2R^2 \sin(s)\cos(s) \, ds \, dt \\
            &= \int_0^{2\pi} \left( R^2 \sin(s)^2 \Big|_{s=0}^{s=\pi/2} \right) dt = 2\pi R^2
            \end{aligned}
            $$

            $\mathrm{Bd}(\vec{S}) = \gamma([0, 2\pi])$, &nbsp; $\gamma(t) = \begin{bmatrix} R\cos(t) \\ R\sin(t) \\ 0 \end{bmatrix}$

            $$
            \begin{aligned}
            \int_{\mathrm{Bd}(\vec{S})} \vec{F} \cdot d\vec{s} &= \int_0^{2\pi} \begin{bmatrix} -R\sin(t) \\ R\cos(t) \\ 1 \end{bmatrix} \cdot \begin{bmatrix} -R\sin(t) \\ R\cos(t) \\ 0 \end{bmatrix} dt \\
            &= \int_0^{2\pi} R^2 \, dt = 2\pi R^2
            \end{aligned}
            $$
            """,
            lk.figure(_fig),
        ],
        label="ex-stokes",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: same boundary
    # corollary: surfaces with the same boundary
    lk.corollary(
        r"""
        Given $\vec{S}_1$ and $\vec{S}_2$ with $\mathrm{Bd}(\vec{S}_1) = \mathrm{Bd}(\vec{S}_2)$

        > $\Longrightarrow$ &nbsp; $\displaystyle\iint_{\vec{S}_1} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} = \iint_{\vec{S}_2} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A}$
        """,
        label="cor-same-boundary",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: same boundary
    # consequence
    lk.prose(r"$\leadsto$ &nbsp; we get to choose the surface which gives a simpler integral!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curl-free fields
    # corollary: curl-free fields are gradients
    lk.corollary(
        r"""
        If $\vec{F}$ is $C^1$-smooth over all of $\mathbb{R}^3$ and $\vec{\nabla} \times \vec{F} = \vec{0}$

        > $\Longrightarrow$ &nbsp; $\vec{F} = \vec{\nabla} f$ is a gradient

        Moreover, the potential function for $\vec{F}$ is $\displaystyle f(x, y, z) = \int_{\vec{C}} \vec{F} \cdot d\vec{s}$, for any oriented curve $\vec{C}$ from $(0, 0, 0)$ to $(x, y, z)$

        > e.g. &nbsp; $\displaystyle f(x, y, z) = \int_0^1 \vec{F}(tx, ty, tz) \cdot \begin{bmatrix} x \\ y \\ z \end{bmatrix} dt$
        """,
        label="cor-potential",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curl-free fields
    # example: a potential function
    lk.example(
        r"""
        $\vec{F}(x, y, z) = \begin{bmatrix} yz \\ xz \\ xy + 2z \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{\nabla} \times \vec{F} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$

        $$
        \begin{aligned}
        f(x, y, z) &= \int_0^1 \begin{bmatrix} (ty)(tz) \\ (tx)(tz) \\ (tx)(ty) + 2(tz) \end{bmatrix} \cdot \begin{bmatrix} x \\ y \\ z \end{bmatrix} dt \\
        &= \int_0^1 \big( t^2 xyz + t^2 xyz + t^2 xyz + 2tz^2 \big) \, dt = xyz + z^2
        \end{aligned}
        $$

        > $\leadsto$ &nbsp; $\vec{\nabla} f = \vec{F}$
        """,
        label="ex-potential",
    )
    return


if __name__ == "__main__":
    app.run()
