import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 17 · Differentiation of vector fields", css_file="lecturekit/style.css")


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
    lk.lecture(17, "Differentiation of vector fields")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: bare axes, names kept clear of arrows, and the fields. Every field is drawn with each arrow
    # at 1/2 of its vector, so that the arrows of F and H do not run into each other.
    K = 0.5

    def panel(ax, xl, yl=None):
        """A bare axis over xl x yl (a square [-xl, xl]^2 when xl is a number)."""
        if not isinstance(xl, tuple):
            xl = (-xl, xl)
        ax.set_xlim(*xl)
        ax.set_ylim(*(yl or xl))
        ax.set_aspect("equal")
        ax.axis("off")

    def plane(xlim, ylim, width=3.6):
        """A figure with one bare axis filling it, its height set by the ranges."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        panel(ax, xlim, ylim)
        return fig, ax

    def per_pt(ax):
        """Data units per point on an axis of fixed place and equal aspect."""
        x0, x1 = ax.get_xlim()
        return (x1 - x0) / (ax.figure.get_figwidth() * 72 * ax.get_position().width)

    def cross_axes(ax, xr, yr, xlabel="$x$", ylabel="$y$"):
        """Coordinate axes through the origin; returns the boxes their names take (data coordinates)."""
        lk.arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        lk.arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        u, boxes = per_pt(ax), []
        ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        boxes.append((xr[1] - 14 * u, -24 * u, xr[1] + 2 * u, -2 * u))
        ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)
        boxes.append((2 * u, yr[1] - 18 * u, 18 * u, yr[1] + 2 * u))
        return boxes

    def beside(ax, at, angle, text, color, w, h, gap=4, fontsize=13):
        """A name centred beside the point `at`, in the direction `angle` (degrees), clear of a w x h box (points)."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        d = w / 2 * abs(c) + h / 2 * abs(s) + gap
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "none", "edgecolor": "none"})
        u = per_pt(ax)
        cx, cy = at[0] + d * c * u, at[1] + d * s * u
        return (cx - (w / 2 + 2) * u, cy - (h / 2 + 2) * u, cx + (w / 2 + 2) * u, cy + (h / 2 + 2) * u)

    def label(ax, at, text, color, w, h, fontsize=12, ha="center"):
        """A name at one place `at`; returns its box in data coordinates."""
        ax.text(*at, text, color=color, fontsize=fontsize, ha=ha, va="center", zorder=8, linespacing=1.15)
        u = per_pt(ax)
        x0 = at[0] - (w / 2 if ha == "center" else (w if ha == "right" else 0)) * u
        return (x0 - 2 * u, at[1] - (h / 2 + 2) * u, x0 + (w + 2) * u, at[1] + (h / 2 + 2) * u)

    def clear_of(boxes, p, q):
        """True when the segment from p to q stays out of every box."""
        for b in boxes:
            for i in range(21):
                x, y = p[0] + (q[0] - p[0]) * i / 20, p[1] + (q[1] - p[1]) * i / 20
                if b[0] <= x <= b[2] and b[1] <= y <= b[3]:
                    return False
        return True

    def farrow(ax, tail, tip, color, lw=1.1, zorder=3):
        """A field arrow: solid shaft with a small open head."""
        ax.annotate("", xy=tip, xytext=tail, zorder=zorder, arrowprops={"arrowstyle": "->,head_length=0.35,head_width=0.22", "mutation_scale": 11, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0})

    def vfield(ax, F, color, pts, k=K, skip=(), avoid=(), cross=()):
        """The vectors k F(p) drawn from the points p; points in `skip`, arrows under a name in `avoid` and arrows that touch
        one of the curves in `cross` are left out."""
        for p in pts:
            if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 1e-9 for q in skip):
                continue
            v = F(*p)
            tip = (p[0] + k * v[0], p[1] + k * v[1])
            near = False
            for xs, ys in cross:
                for i in range(21):
                    qx, qy = p[0] + (tip[0] - p[0]) * i / 20, p[1] + (tip[1] - p[1]) * i / 20
                    if np.min(np.hypot(np.asarray(xs) - qx, np.asarray(ys) - qy)) < 0.08:
                        near = True
                        break
                if near:
                    break
            if not near and clear_of(avoid, p, tip):
                farrow(ax, p, tip, color)

    def chevron(ax, at, angle, color, size=4.5, lw=1.0):
        """A small open head at `at`, pointing in the direction `angle` (radians): a direction mark on a flow line."""
        u = per_pt(ax) * size
        for s in (1, -1):
            b = angle + math.pi + s * 0.55
            ax.plot([at[0] + u * math.cos(b), at[0]], [at[1] + u * math.sin(b), at[1]], color=color, lw=lw, solid_capstyle="round", zorder=2)

    def disc_patch(c, rho, n=2000):
        """The boundary of the disc of radius rho about c, as two arrays."""
        s = np.linspace(0, 2 * math.pi, n, endpoint=False)
        return c[0] + rho * np.cos(s), c[1] + rho * np.sin(s)

    def patch(ax, xs, ys):
        """A filled patch with its outline."""
        ax.fill(xs, ys, color=lk.LIGHT, alpha=0.9, lw=0, zorder=4)
        ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=lk.BLUE, lw=1.3, zorder=5)

    # the fields of the lecture
    def rot(x, y):
        return (-y, x)

    def unit_rot(x, y):
        r = math.hypot(x, y)
        return (-y / r, x / r)

    def rad(x, y):
        return (x, y)

    def unit_rad(x, y):
        r = math.hypot(x, y)
        return (x / r, y / r)

    # base points: five circles about the origin (r = 1/2, 1, ..., 5/2), eight points each, circles 1 and 2 on the axes and
    # diagonals, circles 1/2, 3/2, 5/2 halfway between, so that each circle shows the same pattern scaled
    RINGS = [(0.5 * (_k + 1) * math.cos(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0)), 0.5 * (_k + 1) * math.sin(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0))) for _k in range(5) for _j in range(8)]
    # for the unit fields: rings of radius 1/2, 1, ..., 5/2 with 6, 9, 12, 15, 18 points
    RINGS_UNIT = [(0.5 * _k * np.cos(2 * np.pi * _j / (3 * _k + 3)), 0.5 * _k * np.sin(2 * np.pi * _j / (3 * _k + 3))) for _k in range(1, 6) for _j in range(3 * _k + 3)]
    return K, RINGS, RINGS_UNIT, beside, chevron, cross_axes, disc_patch, farrow, label, panel, patch, rad, rot, plane, unit_rad, unit_rot, vfield


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    lt = lk.slider(-3, 3, step=0.05, value=0.6, label="$t$")
    ct = lk.slider(0, 6.28, step=0.02, value=1.0, label="$t$")
    rt = lk.slider(-1.5, 1, step=0.02, value=0, label="$t$")
    ft = lk.slider(0, 6.28, step=0.02, value=1.0, label="$t$")
    ht = lk.slider(-1, 1, step=0.02, value=0.5, label="$t$")
    gt = lk.slider(0, 4, step=0.05, value=1.5, label="$t$")
    return ct, ft, gt, ht, lt, rt


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(r"mostly for $n = 1$", "paths"),
        lk.aside(r'<span class="lk-ghost">mostly for </span>$m = 1$', "scalar valued"),
        title="So far",
        topic=r"Differentiation of $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"Differentiation of vector fields $(n = m)$", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 4.3, 4.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # section
    lk.section("Differentiation of vector fields $(n = m)$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # remark: notation
    lk.remark(
        r"""
        For the rest of the course we work mostly with $n = 1, 2, 3$ &nbsp; $\leadsto$ &nbsp; we simplify the notation

        > $$
        > \begin{alignedat}{3}
        > &\text{in } \mathbb{R} \text{ we were already writing} \quad && t \in \mathbb{R}\\[10pt]
        > &\text{in } \mathbb{R}^2 \text{ we will write} && \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} x \\ y \end{bmatrix} \quad && \leadsto \; x^1 = x, \quad x^2 = y\\[10pt]
        > &\text{in } \mathbb{R}^3 \text{ we will write} && \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} = \begin{bmatrix} x \\ y \\ z \end{bmatrix} && \leadsto \; x^1 = x, \quad x^2 = y, \quad x^3 = z
        > \end{alignedat}
        > $$

        > > $\leadsto$ &nbsp; no more indices!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # definition: vector field
    lk.definition(
        r"""
        A **vector field** in $\mathbb{R}^2$ is a map

        $$
        \vec{F} : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^2, \qquad \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix} \longmapsto \vec{F}(\vec{x}) = \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \end{bmatrix}.
        $$

        > $\leadsto$ &nbsp; $P : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ and $Q : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ are called the **components** of $\vec{F}$
        """,
        label="def-vector-field",
    )
    return


@app.cell(hide_code=True)
def _(Figure, K, RINGS, RINGS_UNIT, beside, cross_axes, farrow, label, lk, math, mo, panel, rad, rot, plane, unit_rad, unit_rot, vfield):
    # module: vector fields
    # example: rotation, unit rotation, radial and unit radial vector fields
    # Fig 1 four points with their vectors F(x) at true length, then the whole field (arrows at 1/2) with one point x
    # and its vector F(x)
    _fa, _a = plane((-3.3, 3.1), (-2.8, 2.8), width=3.3)
    cross_axes(_a, (-2.6, 2.4), (-2.7, 2.7))
    for _p, _pn, _pa, _vn, _va in (
        ((1.0, 0.0), r"$\genfrac{[}{]}{0}{0}{1}{0}$", -60, r"$\vec{F}\left(\genfrac{[}{]}{0}{0}{1}{0}\right) = \genfrac{[}{]}{0}{0}{0}{1}$", 0),
        ((0.0, 2.0), r"$\genfrac{[}{]}{0}{0}{0}{2}$", 0, r"$\genfrac{[}{]}{0}{0}{-2}{0}$", 180),
        ((-1.0, 1.0), r"$\genfrac{[}{]}{0}{0}{-1}{1}$", 45, r"$\genfrac{[}{]}{0}{0}{-1}{-1}$", -120),
        ((-1.0, -1.0), r"$\genfrac{[}{]}{0}{0}{-1}{-1}$", 180, r"$\genfrac{[}{]}{0}{0}{1}{-1}$", 0),
    ):
        _v = rot(*_p)
        _tip = (_p[0] + _v[0], _p[1] + _v[1])
        farrow(_a, _p, _tip, lk.GREEN, lw=1.3)
        _a.plot(*_p, "o", color="black", ms=3, zorder=7)
        beside(_a, _p, _pa, _pn, "black", 26, 28, gap=3, fontsize=11)
        beside(_a, _tip, _va, _vn, lk.GREEN, 74 if "vec" in _vn else 32, 28, gap=3, fontsize=11)
    _fb, _b = plane((-3.6, 3.6), (-3.6, 3.6), width=3.2)
    _xv = (1.5 * math.cos(math.radians(30)), 1.5 * math.sin(math.radians(30)))
    _names = [label(_b, (0.6, 3.25), "rotation vector field", lk.GREEN, 120, 16, fontsize=12, ha="left")]
    _names += cross_axes(_b, (-3.5, 3.5), (-3.5, 3.5))
    _names.append(beside(_b, (_xv[0] + K * rot(*_xv)[0] / 2, _xv[1] + K * rot(*_xv)[1] / 2), 20, r"$\vec{F}(\vec{x})$", lk.BLUE, 30, 16, gap=4))
    vfield(_b, rot, lk.GREEN, RINGS, skip=[_xv], avoid=_names)
    farrow(_b, _xv, (_xv[0] + K * rot(*_xv)[0], _xv[1] + K * rot(*_xv)[1]), lk.BLUE, lw=1.6, zorder=6)
    _b.plot(*_xv, "o", color=lk.BLUE, ms=3, zorder=7)
    beside(_b, _xv, -40, r"$\vec{x}$", "black", 10, 12, gap=2)
    _rotation = mo.hstack([_fa, mo.md(r"$\leadsto$"), _fb], justify="center", align="center", gap=1.5)

    # Fig 2: the unit rotation field, all arrows of length 1/2; x on the radius-2 ring and G(x) its arrow
    fig_unit_rot, _g = plane((-3.5, 3.5), (-3.5, 3.5), width=3.2)
    _xg = RINGS_UNIT[27 + 2]
    _u = unit_rot(*_xg)
    _tip = (_xg[0] + K * _u[0], _xg[1] + K * _u[1])
    _names = [
        beside(_g, ((_xg[0] + _tip[0]) / 2, (_xg[1] + _tip[1]) / 2), 45, r"$\vec{G}(\vec{x})$", lk.BLUE, 34, 16, gap=4),
        beside(_g, _xg, -45, r"$\vec{x}$", "black", 10, 12, gap=2),
        label(_g, (-3.45, -3.05), "unit rotation\nvector field", lk.GREEN, 90, 34, fontsize=12, ha="left"),
    ]
    _names += cross_axes(_g, (-3.4, 3.4), (-3.4, 3.4))
    vfield(_g, unit_rot, lk.GREEN, RINGS_UNIT, skip=[_xg], avoid=_names[2:])
    farrow(_g, _xg, _tip, lk.BLUE, lw=1.6, zorder=6)
    _g.plot(*_xg, "o", color=lk.BLUE, ms=3, zorder=7)

    # Fig 3: the radial field H and the unit radial field I at the same points, side by side
    fig_radial = Figure(figsize=(6.8, 3.2))
    _left = fig_radial.add_axes((0, 0, 3.2 / 6.8, 1))
    _right = fig_radial.add_axes((3.6 / 6.8, 0, 3.2 / 6.8, 1))
    for _ax, _F, _lim, _name in ((_left, rad, 4.2, "radial\nvector field"), (_right, unit_rad, 3.5, "unit radial\nvector field")):
        panel(_ax, _lim)
        _names = [label(_ax, (-_lim + 0.05, -_lim + 0.35), _name, lk.GREEN, 84, 34, fontsize=12, ha="left")]
        _names += cross_axes(_ax, (-_lim + 0.1, _lim - 0.1), (-_lim + 0.1, _lim - 0.1))
        vfield(_ax, _F, lk.GREEN, RINGS, avoid=_names)

    lk.example(
        [
            r"""
            $\vec{F} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$, &nbsp; $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \end{bmatrix}$
            """,
            lk.figure(_rotation),
        ],
        label="ex-fields",
    )
    return fig_radial, fig_unit_rot


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # remark: length of the rotation field
    lk.remark(
        r"""
        $\lVert \vec{F}(\vec{x}) \rVert^2 = (-y)^2 + (x)^2 = \lVert \vec{x} \rVert^2$

        > $\Longrightarrow$ &nbsp; vectors are getting bigger away from $\vec{0}$
        """
    )
    return


@app.cell(hide_code=True)
def _(fig_radial, fig_unit_rot, lk):
    # module: vector fields
    # example: unit rotation, radial and unit radial vector fields
    lk.example(
        [
            r"""
            $\vec{G}(\vec{x}) = \begin{cases} \dfrac{1}{\lVert \vec{x} \rVert} \vec{F}(\vec{x}), & \vec{x} \neq \vec{0},\\[8pt] \vec{0}, & \vec{x} = \vec{0} \end{cases}$

            > $\Longrightarrow$ &nbsp; $\lVert \vec{G}(\vec{x}) \rVert^2 = \begin{cases} \dfrac{1}{\lVert \vec{x} \rVert^2} \lVert \vec{F}(\vec{x}) \rVert^2 = 1, & \vec{x} \neq \vec{0},\\[8pt] 0, & \vec{x} = \vec{0} \end{cases}$
            """,
            lk.figure(fig_unit_rot),
            lk.gap(),
            r"""
            $\vec{H}(\vec{x}) = \begin{bmatrix} x \\ y \end{bmatrix} = \vec{x}$ &emsp;&emsp; $\vec{I}(\vec{x}) = \begin{cases} \dfrac{\vec{x}}{\lVert \vec{x} \rVert}, & \vec{x} \neq \vec{0},\\[8pt] \vec{0}, & \vec{x} = \vec{0} \end{cases}$
            """,
            lk.figure(fig_radial),
        ],
        label="ex-fields-unit",
    )
    return


@app.cell(hide_code=True)
def _(K, farrow, label, lk, lt, mo, np, plane, vfield):
    # module: flow lines
    # definition: flow line
    # a generic vector field, its base points the points of gamma moved up and down (rows parallel to gamma); the flow line
    # gamma in red, with the field's arrows along it; gamma(t) moves with the slider, its velocity in blue
    def _p(x):
        return x**3 / 14 - x / 3

    def _F(x, y):
        return (1.0, 3 * x * x / 14 - 1 / 3)

    _k = 0.6
    _fig, _ax = plane((-3.4, 3.8), (-2.0, 4.2), width=3.8)
    _t = round(lt.value, 10)
    _g = (_t, _p(_t))
    _names = [
        label(_ax, (1.85, -1.75), r"$\vec{F}(\gamma(t))$", lk.BLUE, 60, 18, fontsize=13),
        label(_ax, (-3.22, -0.55), r"$\gamma$", lk.RED, 10, 14, fontsize=13),
    ]
    _grid = [(_x, _p(_x) + _c) for _x in np.arange(-3.0, 3.01, 0.75) for _c in (-0.75, 0.75, 1.5, 2.25)]
    vfield(_ax, _F, lk.GREEN, _grid, k=_k, avoid=_names)
    _s = np.linspace(-3.3, 3.3, 400)
    _ys = _p(_s)
    _m = np.abs(_ys) < 3.3
    _ax.plot(_s[_m], _ys[_m], color=lk.RED, lw=1.6, zorder=4)
    vfield(_ax, _F, lk.GREEN, [(_x, _p(_x)) for _x in np.arange(-3.0, 3.01, 0.75)], k=_k)
    farrow(_ax, _g, (_g[0] + _k * _F(*_g)[0], _g[1] + _k * _F(*_g)[1]), lk.BLUE, lw=2.0, zorder=6)
    _ax.plot(*_g, "o", color=lk.BLUE, ms=3.3, zorder=7)
    _ax.annotate(r"$\gamma(t)$", _g, textcoords="offset points", xytext=(-4, 9), ha="right", va="bottom", fontsize=12, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "none", "edgecolor": "none"})
    lk.module(
        lk.definition(
            [
                r"""
                Given a vector field $\vec{F} : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^2$, a path $\gamma : (-\varepsilon, \varepsilon) \subseteq \mathbb{R} \longrightarrow D \subseteq \mathbb{R}^2$<br>is called a **flow line** of the vector field $\vec{F}$ if
                """,
                lk.aside(
                    r"$$\gamma'(t) = \vec{F}(\gamma(t)) \qquad \forall t \in (-\varepsilon, \varepsilon).$$",
                    r"at every $t$, the velocity of $\gamma$<br>agrees with $\vec{F}$ at $\gamma(t)$",
                ),
            ],
            label="def-flow-line",
        ),
        lk.prose(lk.interactive(_fig, controls=[lt])),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: flow lines
    # remark: a system of ODEs
    lk.remark(
        r"""
        $\gamma'(t) = \vec{F}(\gamma(t))$ is nothing but a 1st order system of ODEs!

        > $\leadsto$ &nbsp; write $\gamma(t) = \begin{bmatrix} x(t) \\ y(t) \end{bmatrix}$, &nbsp; $\vec{F}(\gamma(t)) = \begin{bmatrix} P(x(t), y(t)) \\ Q(x(t), y(t)) \end{bmatrix}$

        > > $\gamma'(t) = \vec{F}(\gamma(t))$ &nbsp; $\Longleftrightarrow$ &nbsp; $\begin{cases} x'(t) = P(x(t), y(t))\\ y'(t) = Q(x(t), y(t)) \end{cases}$
        """
    )
    return


@app.cell(hide_code=True)
def _(K, RINGS, beside, cross_axes, ct, farrow, label, lk, math, np, rot, plane, vfield):
    # module: flow lines
    # example: circular paths
    # the flow line of F(x) = (-y, x) through x0 = (2, 0): it turns by the angle t, once round for t up to 2 pi; the field
    # drawn as in the first example (arrows at 1/2); gamma'(t) = F(gamma(t)) at the same scale
    _t = round(ct.value, 10)
    _fig, _ax = plane((-3.6, 3.6), (-3.6, 3.6))
    _x0 = (2.0, 0.0)
    _g = (2 * math.cos(_t), 2 * math.sin(_t))
    _names = [
        label(_ax, (-2.95, -1.3), r"$\gamma$", lk.RED, 10, 14, fontsize=13),
        label(_ax, (2.2, 2.95), r"$\gamma'(t) = \vec{F}(\gamma(t))$", lk.BLUE, 100, 18, fontsize=13),
    ]
    _names += cross_axes(_ax, (-3.5, 3.5), (-3.5, 3.5))
    _names.append(beside(_ax, _g, math.degrees(_t) - 30, r"$\gamma(t)$", "black", 26, 16))
    _names.append(beside(_ax, _x0, 32, r"$\vec{x}_0 = \gamma(0)$", "black", 62, 16, gap=3, fontsize=12))
    vfield(_ax, rot, lk.GREEN, RINGS, avoid=_names)
    _s = np.linspace(0, 2 * math.pi, 300)
    _ax.plot(2 * np.cos(_s), 2 * np.sin(_s), color=lk.RED, lw=1.6, zorder=3)
    farrow(_ax, _g, (_g[0] + K * rot(*_g)[0], _g[1] + K * rot(*_g)[1]), lk.BLUE, lw=2.0, zorder=6)
    _ax.plot(*_x0, "o", color=lk.BLUE, ms=3.3, zorder=7)
    _ax.plot(*_g, "o", color=lk.BLUE, ms=3.3, zorder=7)
    lk.example(
        [
            r"""
            $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; find flow lines by solving $\begin{bmatrix} x'(t) \\ y'(t) \end{bmatrix} = \begin{bmatrix} -y(t) \\ x(t) \end{bmatrix}$
            """,
            lk.aside(
                r"""
                > $\Longrightarrow$ &nbsp; $\gamma(t) = \begin{bmatrix} x_0 \cos(t) - y_0 \sin(t) \\ x_0 \sin(t) + y_0 \cos(t) \end{bmatrix}$ for $\gamma(0) = \begin{bmatrix} x_0 \\ y_0 \end{bmatrix}$
                """,
                "circular paths!",
            ),
            lk.interactive(_fig, controls=[ct]),
        ],
        label="ex-circular",
    )
    return


@app.cell(hide_code=True)
def _(K, RINGS, beside, cross_axes, farrow, label, lk, math, rad, rt, plane, vfield):
    # module: flow lines
    # example: radial paths
    # the flow line of H(x) = x through x0 = (1, 1), a ray: sigma(t) = e^t x0 moves in towards 0 for t < 0 and out for
    # t > 0; the field drawn as in the first example (arrows at 1/2), sigma'(t) = H(sigma(t)) at the same scale
    _t = round(rt.value, 10)
    _fig, _ax = plane((-4.4, 4.4), (-4.4, 4.4))
    _x0 = (1.0, 1.0)
    _sg = (math.exp(_t), math.exp(_t))
    _tip = (_sg[0] + K * rad(*_sg)[0], _sg[1] + K * rad(*_sg)[1])
    _names = [
        label(_ax, (3.75, 4.15), r"$\sigma$", lk.RED, 10, 14, fontsize=13),
        label(_ax, (-4.25, 3.1), r"$\sigma'(t) = \vec{H}(\sigma(t))$", lk.BLUE, 100, 18, fontsize=13, ha="left"),
    ]
    _names += cross_axes(_ax, (-4.3, 4.3), (-4.3, 4.3))
    _names.append(beside(_ax, _sg, 120, r"$\sigma(t)$", "black", 26, 16))
    _names.append(beside(_ax, _x0, -20, r"$\vec{x}_0 = \sigma(0)$", "black", 62, 16, gap=3, fontsize=12))
    vfield(_ax, rad, lk.GREEN, RINGS, avoid=_names)
    _ax.plot([0, 4.25], [0, 4.25], color=lk.RED, lw=1.6, zorder=3)
    farrow(_ax, _sg, _tip, lk.BLUE, lw=2.0, zorder=6)
    _ax.plot(*_x0, "o", color=lk.BLUE, ms=3.3, zorder=7)
    _ax.plot(*_sg, "o", color=lk.BLUE, ms=3.3, zorder=7)
    lk.example(
        [
            r"""
            $\vec{H}(\vec{x}) = \vec{x}$ &nbsp; $\leadsto$ &nbsp; $\sigma'(t) = \sigma(t)$
            """,
            lk.aside(
                r"""
                > $\leadsto$ &nbsp; $\begin{bmatrix} x'(t) \\ y'(t) \end{bmatrix} = \begin{bmatrix} x(t) \\ y(t) \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\sigma(t) = \begin{bmatrix} x_0 e^t \\ y_0 e^t \end{bmatrix}$
                """,
                "radial paths",
            ),
            lk.interactive(_fig, controls=[rt]),
        ],
        label="ex-radial",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: divergence
    # lead-in
    lk.prose(r"$\leadsto$ &nbsp; differentiation of vector fields?")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: divergence
    # definition: divergence
    lk.definition(
        [
            r"""
            Given $\vec{F}(\vec{x}) = \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \end{bmatrix}$ differentiable

            > $\Longrightarrow$ &nbsp; $D\vec{F}(\vec{x}) = \begin{bmatrix} {\large\tfrac{\partial P}{\partial x}}(\vec{x}) & {\large\tfrac{\partial P}{\partial y}}(\vec{x})\\[4pt] {\large\tfrac{\partial Q}{\partial x}}(\vec{x}) & {\large\tfrac{\partial Q}{\partial y}}(\vec{x}) \end{bmatrix}$ is well-defined

            The **divergence** of $\vec{F}$ is the scalar function

            $$
            \begin{aligned}
            \mathrm{div}(\vec{F})(\vec{x}) &= \vec{\nabla} \cdot \vec{F}(\vec{x})\\
            &= \underbrace{\frac{\partial P}{\partial x\vphantom{y}}}_{\mathllap{\footnotesize \begin{array}{c} \text{partial derivative of 1st component} \\ \text{with respect to 1st variable} \end{array}\kern-1.2em}}(\vec{x}) + \underbrace{\frac{\partial Q}{\partial y}}_{\mathrlap{\kern-1.2em \footnotesize \begin{array}{c} \text{partial derivative of 2nd component} \\ \text{with respect to 2nd variable} \end{array}}}(\vec{x}) = \mathrm{tr}\big( D\vec{F}(\vec{x}) \big).
            \end{aligned}
            $$
            """,
        ],
        label="def-divergence",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: divergence
    # consequence: nabla notation
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; $\vec{\nabla} \cdot \vec{F}(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \end{bmatrix}$",
            "useful abuse of notation!",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: divergence
    # question: what div tells
    lk.prose(
        r"""
        What does $\mathrm{div}(\vec{F})$ tell us about $\vec{F}$?

        > $\leadsto$ &nbsp; $\mathrm{div}(\vec{F})(\vec{x})$ = rate of expansion of “area at $\vec{x}$” under the flow of $\vec{F}$
        """
    )
    return


@app.cell(hide_code=True)
def _(RINGS, beside, chevron, cross_axes, disc_patch, ft, label, lk, math, np, patch, rot, plane, vfield):
    # module: divergence
    # example: div of the rotation vector field
    # the flow of F(x) = (-y, x) turns every point of the disc around x0 by the angle t: the moved patch is the image of the
    # disc; the two flow circles pass through the field's own points (radius 1 and 2)
    _rc, _a, _rho = 1.5, math.radians(50), 0.5
    _t = round(ft.value, 10)
    _fig, _ax = plane((-3.5, 3.5), (-3.5, 3.5))
    _x0 = (_rc * math.cos(_a), _rc * math.sin(_a))
    _names = [label(_ax, (2.3, -3.2), r"flow lines of $\vec{F}$", lk.RED, 100, 18, fontsize=13)]
    _names += cross_axes(_ax, (-3.4, 3.4), (-3.4, 3.4))
    vfield(_ax, rot, lk.GREEN, RINGS, avoid=_names)
    _s = np.linspace(0, 2 * math.pi, 300)
    for _rr in (1.0, 2.0):
        _ax.plot(_rr * np.cos(_s), _rr * np.sin(_s), color=lk.RED, lw=1.3, zorder=3)
        for _hh in (math.radians(-110), math.radians(70)):
            chevron(_ax, (_rr * math.cos(_hh), _rr * math.sin(_hh)), _hh + math.pi / 2, lk.RED, lw=1.2)
    _bx, _by = disc_patch(_x0, _rho)
    _c, _sn = math.cos(_t), math.sin(_t)
    _mx, _my = _c * _bx - _sn * _by, _sn * _bx + _c * _by
    patch(_ax, _bx, _by)
    patch(_ax, _mx, _my)
    _ax.plot(*_x0, "o", color=lk.BLUE, ms=3, zorder=7)
    _ax.plot(_rc * math.cos(_a + _t), _rc * math.sin(_a + _t), "o", color=lk.BLUE, ms=3, zorder=7)
    beside(_ax, (_x0[0] * (1 + (_rho + 0.02) / _rc), _x0[1] * (1 + (_rho + 0.02) / _rc)), math.degrees(_a), r"$\vec{x}_0$", "black", 16, 14, gap=2)
    _f = _a + _t + (_rho + 0.04) / _rc
    beside(_ax, (_rc * math.cos(_f), _rc * math.sin(_f)), math.degrees(_f) + 90, r"$\gamma(t)$", "black", 26, 16, gap=2)
    lk.example(
        [
            r"""
            $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \end{bmatrix}$ (rotation vector field)

            > $\Longrightarrow$ &nbsp; $\mathrm{div}(\vec{F})(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \begin{bmatrix} -y \\ x \end{bmatrix} = {\large\tfrac{\partial}{\partial x}}(-y) + {\large\tfrac{\partial}{\partial y}}(x) = 0$
            """,
            lk.aside(lk.interactive(_fig, controls=[ft]), r"“flow of $\vec{F}$” does not compress/expand<br>the area around any point $\vec{x}_0$"),
        ],
        label="ex-div-rotation",
    )
    return


@app.cell(hide_code=True)
def _(RINGS, beside, chevron, cross_axes, disc_patch, ht, lk, math, np, patch, rad, plane, vfield):
    # module: divergence
    # example: div of the radial vector field
    # the flow of H(x) = x moves every point of the disc around x0 to e^t times itself: the moved patch is the image of the
    # disc; eight rays (flow lines) along the axes and diagonals, the field arrows on them left out
    _rc, _a, _rho = 1.0, math.radians(67.5), 0.35
    _t = round(ht.value, 10)
    _e = math.exp(_t)
    _fig, _ax = plane((-4.0, 4.0), (-4.0, 4.0))
    _x0 = (_rc * math.cos(_a), _rc * math.sin(_a))
    _sg = (_e * _x0[0], _e * _x0[1])
    _names = cross_axes(_ax, (-3.9, 3.9), (-3.9, 3.9))
    _rays = [(np.linspace(0, 3.9, 80) * math.cos(math.radians(45 * _j)), np.linspace(0, 3.9, 80) * math.sin(math.radians(45 * _j))) for _j in range(8)]
    vfield(_ax, rad, lk.GREEN, RINGS, avoid=_names, cross=_rays)
    for _j in range(8):
        _an = math.radians(45 * _j)
        _ax.plot([0, 3.9 * math.cos(_an)], [0, 3.9 * math.sin(_an)], color=lk.RED, lw=1.6, zorder=3)
        chevron(_ax, (0.45 * 3.9 * math.cos(_an), 0.45 * 3.9 * math.sin(_an)), _an, lk.RED, lw=1.2)
    _bx, _by = disc_patch(_x0, _rho)
    patch(_ax, _bx, _by)
    patch(_ax, _e * _bx, _e * _by)
    _ax.plot(*_x0, "o", color=lk.BLUE, ms=3, zorder=7)
    _ax.plot(*_sg, "o", color=lk.BLUE, ms=3, zorder=7)
    _q = (_x0[0] + (_rho + 0.04) * math.cos(math.radians(-45)), _x0[1] + (_rho + 0.04) * math.sin(math.radians(-45)))
    beside(_ax, _q, -45, r"$\vec{x}_0$", "black", 16, 14, gap=2)
    _fo = 1 + (_rho + 0.02) / _rc
    beside(_ax, (_fo * _sg[0], _fo * _sg[1]), math.degrees(_a), r"$\sigma(t)$", "black", 26, 16, gap=2)
    lk.example(
        [
            r"""
            $\vec{H}(\vec{x}) = \begin{bmatrix} x \\ y \end{bmatrix}$ (radial vector field)

            > $\Longrightarrow$ &nbsp; $\mathrm{div}(\vec{H})(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \begin{bmatrix} x \\ y \end{bmatrix} = {\large\tfrac{\partial}{\partial x}}(x) + {\large\tfrac{\partial}{\partial y}}(y) = 2 > 0$
            """,
            lk.aside(lk.interactive(_fig, controls=[ht]), r"“flow of $\vec{H}$” expands<br>the area around each $\vec{x}$"),
        ],
        label="ex-div-radial",
    )
    return


@app.cell(hide_code=True)
def _(K, RINGS_UNIT, beside, chevron, cross_axes, disc_patch, gt, lk, math, np, patch, plane, unit_rot, vfield):
    # module: divergence
    # example: div of the unit rotation vector field
    # the flow of G: every point moves at unit speed on its circle, so a point at distance r from the origin turns by the
    # angle t / r; the moved patch is the image of the disc around x0
    _rc, _a, _rho = 1.5, math.radians(50), 0.5
    _t = round(gt.value, 10)
    _fig, _ax = plane((-3.1, 3.1), (-3.1, 3.1))
    _x0 = (_rc * math.cos(_a), _rc * math.sin(_a))
    _names = cross_axes(_ax, (-3.0, 3.0), (-3.0, 3.0))
    vfield(_ax, unit_rot, lk.GREEN, RINGS_UNIT, avoid=_names)
    _s = np.linspace(0, 2 * math.pi, 300)
    for _rr in (_rc - _rho, _rc + _rho):
        _ax.plot(_rr * np.cos(_s), _rr * np.sin(_s), color=lk.RED, lw=1.6, zorder=3)
        for _hh in (math.radians(-110), math.radians(170)):
            chevron(_ax, (_rr * math.cos(_hh), _rr * math.sin(_hh)), _hh + math.pi / 2, lk.RED, lw=1.2)
    _bx, _by = disc_patch(_x0, _rho, n=4000)
    _ang = _t / np.hypot(_bx, _by)
    _mx, _my = np.cos(_ang) * _bx - np.sin(_ang) * _by, np.sin(_ang) * _bx + np.cos(_ang) * _by
    patch(_ax, _bx, _by)
    patch(_ax, _mx, _my)
    _ax.plot(*_x0, "o", color=lk.BLUE, ms=3, zorder=7)
    _ax.plot(_rc * math.cos(_a + _t / _rc), _rc * math.sin(_a + _t / _rc), "o", color=lk.BLUE, ms=3, zorder=7)
    _b = _a - (_rho + 0.04) / _rc
    beside(_ax, (_rc * math.cos(_b), _rc * math.sin(_b)), math.degrees(_b) - 90, r"$\vec{x}_0$", "black", 16, 14, gap=2)
    lk.example(
        [
            lk.aside(
                r"$\vec{G}(\vec{x}) = \begin{cases} \dfrac{1}{\lVert \vec{x} \rVert} \begin{bmatrix} -y \\ x \end{bmatrix}, & \vec{x} \neq \vec{0}\\[8pt] \mk{\vec{0}}, & \vec{x} = \vec{0} \end{cases}$",
                "not differentiable",
                at="last",
            ),
            lk.aside(
                r"> $\mathrm{div}(\vec{G})(\vec{x}) = \dfrac{\partial}{\partial x} \left( \dfrac{-y}{\sqrt{x^2 + y^2}} \right) + \dfrac{\partial}{\partial y} \left( \dfrac{x}{\sqrt{x^2 + y^2}} \right)$",
                r"for $\vec{x} \neq \vec{0}$",
            ),
            r'> <span class="lk-ghost">$\mathrm{div}(\vec{G})(\vec{x})$ </span>$= \dfrac{xy}{(x^2 + y^2)^{3/2}} - \dfrac{xy}{(x^2 + y^2)^{3/2}} = 0$',
            lk.interactive(_fig, controls=[gt]),
        ],
        label="ex-div-unit-rotation",
    )
    return


if __name__ == "__main__":
    app.run()
