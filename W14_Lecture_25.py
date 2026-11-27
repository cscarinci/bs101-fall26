import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 25 · Triple integrals", css_file="lecturekit/style.css")


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
    from lecturekit.blocks import as_html
    return Figure, as_html, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(25, "Triple integrals")
    return


@app.cell(hide_code=True)
def _(Figure, as_html, lk, math, mo, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points), arrowheads along a space curve, a walking
    # figure standing on a curve in 3D, and a row of figures joined by maps that point either way

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

    def plane(xlim, ylim, width, names=("$x$", "$y$"), fontsize=13):
        """A drawing of a coordinate plane: the two axes as arrows, named at their tips."""
        fig, ax = drawing(xlim, ylim, width)
        lk.arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        lk.arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, names[0], "black", 10, 12, fontsize=fontsize)
        beside(ax, (0, ylim[1] - 0.3), 90, names[1], "black", 10, 12, fontsize=fontsize)
        return fig, ax

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

    def maps_both(*parts):
        """Figures in a row joined by maps, as lk.maps; a map name given as ("<", name) points to the left."""
        cells = []
        for i, part in enumerate(parts):
            if i % 2:
                left = isinstance(part, tuple)
                name = part[1] if left else part
                arrow = rf"$\xleftarrow{{\quad {name} \quad}}$" if left else rf"$\xrightarrow{{\quad {name} \quad}}$"
                cells.append(f'<div class="lk-map">{mo.md(arrow).text}</div>')
            else:
                cells.append(f'<div class="lk-map-item">{as_html(part)}</div>')
        return mo.Html(f'<div class="lk-maps">{"".join(cells)}</div>')

    return beside, drawing, heads, maps_both, plane, walker3d


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    pr = lk.slider(0, 2, step=0.05, value=1.25, label="$r$")
    pth = lk.slider(0, 6.28, step=0.04, value=0.8, label=r"$\theta$")
    nb = lk.slider(1, 5, step=1, value=2, label="$N$")
    return nb, pr, pth


@app.cell(hide_code=True)
def _(heads, lk, np, walker3d):
    # module: recap
    # recap
    # an oriented dome S (blue) with its normal vectors (green) pointing in, and its boundary curve C = Bd(S) (red), run
    # clockwise seen from above, with a walking figure standing along the normal
    _a = np.linspace(0, 2 * np.pi, 400)
    _bx, _by = 1.6 * np.cos(_a) * (1 + 0.08 * np.cos(3 * _a)), 1.2 * np.sin(_a) * (1 + 0.08 * np.cos(3 * _a))
    _r, _k = np.meshgrid(np.linspace(0, 1, 16), np.arange(400), indexing="ij")
    _X, _Y, _Z = _r * _bx[_k], _r * _by[_k], 1.5 * np.sqrt(np.clip(1 - _r**2, 0, 1))
    _c = (_bx[::-1], _by[::-1], 0 * _bx)
    _n = []
    for _rr, _kk in ((0.0, 0), (0.6, 40), (0.6, 170), (0.6, 300), (0.85, 100), (0.85, 230), (0.85, 360)):
        _p = np.array([_rr * _bx[_kk], _rr * _by[_kk], 1.5 * np.sqrt(1 - _rr**2)])
        _g = np.array([_p[0] / 1.6**2, _p[1] / 1.2**2, _p[2] / 1.5**2])
        _n.append((_p, _p - 0.5 * _g / np.linalg.norm(_g), lk.GREEN, 1.3))
    _i = 333
    _ahead = np.array([_bx[_i - 1] - _bx[_i + 1], _by[_i - 1] - _by[_i + 1], 0.0])
    _walk = walker3d((_bx[_i], _by[_i], 0.0), np.cross(_ahead, (0, 0, 1)), (0, 0, 1), h=0.6)
    _fig = lk.turntable(
        30,
        26,
        "a dome S with its normal vectors pointing in, and its boundary curve C run clockwise seen from above, with a walking figure standing along the normal",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_X, _Y, _Z, alpha=0.5)],
                lines=[(*_c, lk.RED, 2.0)] + _walk,
                arcs=heads(*_c, lk.RED, (0.2, 0.45, 0.7, 0.95)),
                arrows=_n,
                texts=[((0.0, -1.0, 1.0), r"\vec{S}", lk.BLUE, 180, 12), ((0.0, 1.2, 0.0), r"\vec{C} = \mathrm{Bd}(\vec{S})", lk.RED, -20, 14)],
                box=((-1.7, 1.7), (-1.7, 1.7), (-0.6, 1.6)),
            )
        ],
        height=lk.H3D,
        zoom=1.2,
        key="L25-recap",
    )
    lk.recap(
        r"""
        $\vec{S}$ oriented surface

        $\vec{C} = \mathrm{Bd}(\vec{S})$ boundary curve with positive orientation

        $$
        \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \iint_{\vec{S}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A}
        $$
        """,
        lk.figure(_fig),
        topic="Stokes' theorem",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Why is Stokes' theorem useful?

        Change of coordinates in $\mathbb{R}^2$

        Triple integrals over simple 3d regions
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 8.2, 6.2, 5.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Stokes
    # lead-in
    lk.prose(r"$\leadsto$ &nbsp; why is this useful?")
    return


@app.cell(hide_code=True)
def _(heads, lk, np):
    # module: Stokes
    # example: the curl of F across half an ellipsoid
    # the upper half S of the ellipsoid x^2 + y^2 + z^2/4 = 1 (blue), the unit disk D in the xy-plane (green) and their
    # common boundary, the unit circle C (red), run counter-clockwise seen from above
    _s, _t = np.meshgrid(np.linspace(0, np.pi / 2, 17), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _r, _q = np.meshgrid(np.linspace(0, 1, 9), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _a = np.linspace(0, 2 * np.pi, 200)
    _c = (np.cos(_a), np.sin(_a), 0 * _a)
    _fig = lk.turntable(
        30,
        18,
        "the upper half S of the ellipsoid x^2 + y^2 + z^2/4 = 1, the unit disk D in the xy-plane, and their common boundary circle C run counter-clockwise",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(np.sin(_s) * np.cos(_t), np.sin(_s) * np.sin(_t), 2 * np.cos(_s), alpha=0.35), lk.sheet(_r * np.cos(_q), _r * np.sin(_q), 0 * _r, alpha=0.8, tone=lk.GREEN)],
                lines=[(*_c, lk.RED, 2.0)],
                arcs=heads(*_c, lk.RED, (0.2, 0.45, 0.7, 0.95)),
                axes=[((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 1.8, 0), "y", -20), ((0, 0, 0), (0, 0, 2.5), "z", 90)],
                texts=[((0, 0, 2.0), "2", "#000000", 150, 8), ((0, 1.0, 0), "1", "#000000", -60, 8), ((1.0, 0, 0), "1", "#000000", -150, 8), ((0.0, 0.75, 1.3), "S", lk.BLUE, 30, 12), ((0.5, -0.4, 0.0), "D", lk.GREEN, 0, 0), ((0.0, -1.0, 0.0), r"\vec{C}", lk.RED, 200, 12)],
                box=((-1.1, 1.1), (-1.1, 1.1), (0, 2.1)),
            )
        ],
        height=lk.H3D,
        key="L25-ellipsoid",
    )
    lk.example(
        [
            r"$\vec{F}(x, y, z) = \begin{bmatrix} e^{x^2} - y \\ x + z\cos(y) \\ xyz \end{bmatrix}$",
            lk.aside(r"$\mk{S} = \lbrace x^2 + y^2 + {\large\tfrac{z^2}{4}} = 1, \ z \geqslant 0 \rbrace$", "ellipsoid"),
            lk.aside(
                r"$\displaystyle\iint_{\mk{\vec{S}}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} = \ ?$ &nbsp; $\leadsto$ &nbsp; $\vec{\nabla} \times \vec{F} = \begin{bmatrix} xz - \cos(y) \\ -yz \\ 2 \end{bmatrix}$",
                "orient up",
            ),
            r"""
            > $\leadsto$ &nbsp; $\vec{S} = \Phi(D)$, $\Phi(x, y) = \begin{bmatrix} x \\ y \\ 2\sqrt{1 - x^2 - y^2} \end{bmatrix}$ with $D = \lbrace (x, y) \mid x^2 + y^2 \leqslant 1 \rbrace$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \iint_{\vec{S}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} &= \iint_D \cdots \\
                &= \int_{\vec{C}} \vec{F} \cdot d\vec{s}
                \end{aligned}
                $$
                """,
                [(1, "very messy!"), (2, r"$\leadsto$ use Stokes!")],
                rows=2,
            ),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \int_{\mk{\vec{C}}} \vec{F} \cdot d\vec{s} &= \int_0^{2\pi} \underbrace{\vec{F}\left( \begin{bmatrix} \cos(t) \\ \sin(t) \\ 0 \end{bmatrix} \right)}_{\text{still messy}\ldots} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 0 \end{bmatrix} dt \\[6pt]
                &= \iint_{\mk{\vec{D}}} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} \\
                &= \iint_D \begin{bmatrix} xz - \cos(y) \\ -yz \\ 2 \end{bmatrix} \cdot \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} dxdy \\
                &= 2 \iint_D dxdy = 2 \int_{-1}^{1} \left( \int_{-\sqrt{1 - x^2}}^{\sqrt{1 - x^2}} dy \right) dx = \mk{2\pi}
                \end{aligned}
                $$
                """,
                [(1, "circle on $xy$-plane<br>counter-clockwise"), (2, r"disk on $xy$-plane<br>$\leadsto$ use Stokes again!"), (4, "2 times the area of disk of radius 1")],
                rows=4,
            ),
            lk.figure(_fig),
        ],
        label="ex-ellipsoid",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: change of coordinates
    # section
    lk.section(r"Change of coordinates in $\mathbb{R}^2$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: change of coordinates
    # lead-in
    lk.prose(r"$\leadsto$ &nbsp; easier to integrate over a disk!")
    return


@app.cell(hide_code=True)
def _(lk, np, pr, pth):
    # module: change of coordinates
    # scene (no visible output; the prose below shows it)
    # the disk S of radius R in the xy-plane with its normal n (orange); the circle of radius r (red, the image of the
    # segment r = r0), the radius at the angle theta (orange, the image of the segment theta = theta0) and the point
    # (s, t, 0) = (r cos theta, r sin theta, 0) (black). r and theta move with the sliders. R is drawn as 2
    _r0, _t0 = float(pr.value), float(pth.value)
    _rr, _aa = np.meshgrid(np.linspace(0, 2, 9), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _g = np.linspace(0, 1, 30)
    _e = np.array([np.cos(_t0), np.sin(_t0), 0.0])
    _P = _r0 * _e
    lk.turntable(
        30,
        35,
        "the disk S of radius R in the xy-plane with its upward normal, the circle of radius r, the radius at the angle theta and the point (r cos theta, r sin theta, 0)",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(_rr * np.cos(_aa), _rr * np.sin(_aa), 0 * _rr, wire=[(0, 4, lk.BLUE, 0.4)], alpha=0.6)],
                lines=[(_r0 * np.cos(_T), _r0 * np.sin(_T), 0 * _T, lk.RED, 2.2), (2 * _e[0] * _g, 2 * _e[1] * _g, 0 * _g, lk.ORANGE, 2.2)],
                points=[(tuple(_P), "#000000")],
                arrows=[((0, 0, 0), (0, 0, 1.0), lk.GREEN, 1.6)],
                axes=[((0, 0, 0), (2.6, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", -20), ((0, 0, 0), (0, 0, 1.6), "z", 90)],
                texts=[
                    ((-1.45, -1.45, 0.0), r"\vec{S} \subset \mathbb{R}^3", lk.BLUE, 220, 10),
                    ((0, 0, 1.0), r"\vec{n}", lk.GREEN, 180, 8),
                ],
                caption=r"\begin{bmatrix} s \\ t \\ 0 \end{bmatrix} = \begin{bmatrix} r\cos\theta \\ r\sin\theta \\ 0 \end{bmatrix}",
                box=((-1.7, 1.7), (-1.7, 1.7), (-0.2, 1.0)),
            )
        ],
        height=lk.H3D,
        key="L25-disk",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, maps_both, np, plane, pr, pth):
    # module: change of coordinates
    # text: two parameterizations of the disk
    # left: the disk D in the (s, t)-plane with the point (s, t); right: the rectangle [0, R] x [0, 2 pi] in the
    # (r, theta)-plane with the segment r = r0 (red), the segment theta = theta0 (orange) and the point (r, theta). R is
    # drawn as 2, and theta / pi on the vertical axis
    _r0, _t0 = float(pr.value), float(pth.value)
    _a = np.linspace(0, 2 * np.pi, 200)
    _fd, _ad = plane((-2.8, 3.2), (-2.8, 3.2), 2.8, names=("$s$", "$t$"), fontsize=17)
    _ad.fill(2 * np.cos(_a), 2 * np.sin(_a), color=lk.LIGHT, lw=0, zorder=0)
    _ad.plot(2 * np.cos(_a), 2 * np.sin(_a), color=lk.BLUE, lw=1.8)
    _p = (_r0 * np.cos(_t0), _r0 * np.sin(_t0))
    _ad.plot(*_p, "o", color="black", ms=4.5, zorder=6)
    beside(_ad, _p, 45, "$(s, t)$", "black", 46, 18, gap=2, fontsize=17)
    beside(_ad, (2, 0), -60, "$R$", "black", 16, 18, gap=4, fontsize=17)
    beside(_ad, (-2, 0), -120, "$-R$", "black", 26, 18, gap=4, fontsize=17)
    beside(_ad, (0, 2), 30, "$R$", "black", 16, 18, gap=4, fontsize=17)
    beside(_ad, (0, -2), -30, "$-R$", "black", 26, 18, gap=4, fontsize=17)
    _ad.text(-2.2, 2.3, r"$D \subset \mathbb{R}^2$", color=lk.BLUE, fontsize=17, ha="center", va="center")

    _fr, _ar = plane((-0.7, 3.0), (-0.55, 3.1), 2.8, names=("$r$", r"$\theta$"), fontsize=17)
    _ar.fill([0, 2, 2, 0], [0, 0, 2, 2], color=lk.LIGHT, lw=0, zorder=0)
    _ar.plot([0, 2, 2, 0, 0], [0, 0, 2, 2, 0], color=lk.BLUE, lw=1.8)
    _ar.plot([_r0, _r0], [0, 2], color=lk.RED, lw=1.8, zorder=3)
    _ar.plot([0, 2], [_t0 / np.pi, _t0 / np.pi], color=lk.ORANGE, lw=1.8, zorder=3)
    _ar.plot(_r0, _t0 / np.pi, "o", color="black", ms=4.5, zorder=6)
    beside(_ar, (_r0, _t0 / np.pi), 45, r"$(r, \theta)$", "black", 46, 18, gap=2, fontsize=17)
    beside(_ar, (2, 0), -90, "$R$", "black", 16, 18, gap=6, fontsize=17)
    beside(_ar, (0, 2), 180, r"$2\pi$", "black", 26, 18, fontsize=17)
    lk.prose(
        r"""
        $\vec{S} = \lbrace (x, y, z) \mid x^2 + y^2 \leqslant R^2, \ z = 0 \rbrace \subset \mathbb{R}^3$ oriented up, has two natural parameterizations

        $$
        \begin{aligned}
        \Phi(s, t) &= \begin{bmatrix} s \\ t \\ 0 \end{bmatrix} \quad \text{for } s^2 + t^2 \leqslant R^2 \\
        \Psi(r, \theta) &= \begin{bmatrix} r\cos\theta \\ r\sin\theta \\ 0 \end{bmatrix} \quad \text{for } 0 \leqslant r \leqslant R, \ 0 \leqslant \theta \leqslant 2\pi
        \end{aligned}
        $$
        """,
        lk.interactive(maps_both(_fd, r"\Phi", lk.frame("L25-disk", lk.H3D), ("<", r"\Psi"), _fr), controls=[pr, pth]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: change of coordinates
    # text: both parameterizations are compatible with the orientation
    lk.prose(
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \Phi_s \times \Phi_t &= \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} \times \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \\[4pt]
            \Psi_r \times \Psi_\theta &= \begin{bmatrix} \cos\theta \\ \sin\theta \\ 0 \end{bmatrix} \times \begin{bmatrix} -r\sin\theta \\ r\cos\theta \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ r \end{bmatrix}
            \end{aligned}
            $$
            """,
            "compatible with up orientation",
            at=1.5,
            rows=2,
        ),
        r"""
        Let $\vec{F}(x, y, z) = \begin{bmatrix} f(x, y, z) \\ g(x, y, z) \\ h(x, y, z) \end{bmatrix}$

        $$
        \begin{aligned}
        \iint_{\vec{S}} \vec{F} \cdot d\vec{A} &= \iint_D \vec{F}(s, t, 0) \cdot \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} dsdt \\
        &= \int_{-R}^{R} \int_{-\sqrt{R^2 - t^2}}^{\sqrt{R^2 - t^2}} h(s, t, 0) \, dsdt \\
        &= \iint_{[0, R] \times [0, 2\pi]} \vec{F}(r\cos\theta, r\sin\theta, 0) \cdot \begin{bmatrix} 0 \\ 0 \\ r \end{bmatrix} drd\theta \\
        &= \int_0^{2\pi} \int_0^R h(r\cos\theta, r\sin\theta, 0) \, r \, drd\theta
        \end{aligned}
        $$

        > $\Longrightarrow$ &nbsp; for any $h : \mathbb{R}^2 \longrightarrow \mathbb{R}$

        $$
        \int_{-R}^{R} \int_{-\sqrt{R^2 - y^2}}^{\sqrt{R^2 - y^2}} h(x, y) \, dxdy = \int_0^{2\pi} \int_0^R h(r\cos\theta, r\sin\theta) \, r \, drd\theta
        $$

        > $\Longrightarrow$ &nbsp; $\displaystyle\int_{-R}^{R} \int_{-\sqrt{R^2 - y^2}}^{\sqrt{R^2 - y^2}} dxdy = \int_0^{2\pi} \int_0^R r \, drd\theta = 2\pi \, \frac{R^2}{2} = \pi R^2$
        """,
    )
    return


@app.cell(hide_code=True)
def _(heads, lk, np):
    # module: change of coordinates
    # example: a curve on a cylinder and a plane
    # the cylinder x^2 + y^2 = 1 (red tone), the plane y + z = 2 (blue tone), their intersection C (green, counter-clockwise
    # seen from above), the piece S_3 of the plane inside the cylinder (orange tone) with its normal n (orange)
    _a = np.linspace(0, 2 * np.pi, 200)
    _c = (np.cos(_a), np.sin(_a), 2 - np.sin(_a))
    _z, _q = np.meshgrid(np.linspace(-0.3, 3.4, 12), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _r, _qq = np.meshgrid(np.linspace(0, 1, 9), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _px, _py = np.meshgrid(np.linspace(-1.6, 1.6, 9), np.linspace(-1.6, 1.6, 9), indexing="ij")
    _fig = lk.turntable(
        35,
        15,
        "the cylinder x^2 + y^2 = 1 and the plane y + z = 2, their intersection C run counter-clockwise seen from above, and the piece S_3 of the plane inside the cylinder with its normal n",
        [
            lk.panel(
                1.0,
                surfaces=[
                    lk.sheet(np.cos(_q), np.sin(_q), _z, alpha=0.2, tone=lk.RED),
                    lk.sheet(_px, _py, 2 - _py, alpha=0.2),
                    lk.sheet(_r * np.cos(_qq), _r * np.sin(_qq), 2 - _r * np.sin(_qq), alpha=0.75, tone=lk.ORANGE),
                ],
                lines=[(*_c, lk.GREEN, 2.2)],
                arcs=heads(*_c, lk.GREEN, (0.2, 0.45, 0.7, 0.95)),
                arrows=[((0, 0, 2.0), (0, 0.7, 2.7), lk.ORANGE, 1.6)],
                axes=[((0, 0, 0), (2.2, 0, 0), "x", -150), ((0, 0, 0), (0, 2.2, 0), "y", -20), ((0, 0, 0), (0, 0, 3.6), "z", 90)],
                texts=[
                    ((0, 0.7, 2.7), r"\vec{n}", lk.ORANGE, 90, 8),
                    ((0.3, 0.4, 1.6), r"\vec{S}_3", lk.ORANGE, 0, 0),
                    ((0.0, -1.0, 3.0), r"\vec{C} = S_1 \cap S_2", lk.GREEN, 150, 14),
                    ((-1.6, 1.6, 0.4), "y + z = 2", lk.BLUE, 90, 10),
                    ((np.cos(-0.5), np.sin(-0.5), -0.3), "x^2 + y^2 = 1", lk.RED, -60, 10),
                ],
                box=((-1.4, 1.4), (-1.4, 1.4), (-0.3, 3.4)),
            )
        ],
        height=lk.H3D,
        key="L25-cylinder",
    )
    lk.example(
        [
            r"$\vec{F} = \begin{bmatrix} -y^3 \\ x^3 \\ -z^3 \end{bmatrix}$, $C = \lbrace (x, y, z) \mid \overbrace{x^2 + y^2 = 1}^{S_1}, \ \overbrace{y + z = 2}^{S_2} \rbrace$",
            lk.aside(r"$\displaystyle\int_{\mk{\vec{C}}} \vec{F} \cdot d\vec{s} = \ ?$", "say, counter-clockwise<br>seen from above"),
            r"""
            Stokes &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle\int_{\vec{C}} \vec{F} \cdot d\vec{s} = \iint_{\vec{S}_3} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A}$

            $\vec{\nabla} \times \vec{F} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ -y^3 & x^3 & -z^3 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 3(x^2 + y^2) \end{bmatrix}$

            $S_3$ = piece of the plane inside the cylinder

            $$
            S_3 = \lbrace (x, y, z) \mid \underbrace{x^2 + y^2 \leqslant 1}_{B(0, 1) \subset \mathbb{R}^2}, \ \underbrace{y + z = 2}_{z = 2 - y = f(x, y)} \rbrace
            $$

            $$
            \begin{aligned}
            \Longrightarrow \quad \iint_{\vec{S}_3} (\vec{\nabla} \times \vec{F}) \cdot d\vec{A} &= \iint_{B(0, 1)} \begin{bmatrix} 0 \\ 0 \\ 3(x^2 + y^2) \end{bmatrix} \cdot \begin{bmatrix} -f_x \\ -f_y \\ 1 \end{bmatrix} dxdy \\
            &= \iint_{B(0, 1)} 3(x^2 + y^2) \, dxdy \\
            &= \iint_{[0, 1] \times [0, 2\pi]} 3\big( (r\cos\theta)^2 + (r\sin\theta)^2 \big) \, r \, drd\theta \\
            &= \int_0^{2\pi} \int_0^1 3r^2 \, r \, drd\theta = 2\pi \cdot \frac{3}{4} = \frac{3\pi}{2}
            \end{aligned}
            $$
            """,
            lk.figure(_fig),
        ],
        label="ex-cylinder",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: triple integrals
    # section
    lk.section("Triple integrals over simple 3d regions")
    return


@app.cell(hide_code=True)
def _(lk, nb, np):
    # module: triple integrals
    # scene (no visible output; the prose below shows it)
    # the box B = [a, b] x [c, d] x [p, q] (blue edges) cut into N^3 smaller boxes of the same size (grey), with a chosen
    # point in each (blue), anywhere in its box; the side lengths b - a, d - c, q - p beside the edges. N moves with the slider
    _a, _b, _c, _d, _p, _q, _n = 0.3, 2.1, 0.3, 2.5, 0.0, 1.6, int(nb.value)
    _lines = []
    for _u in np.linspace(_a, _b, _n + 1):
        for _v in np.linspace(_c, _d, _n + 1):
            _lines.append(([_u, _u], [_v, _v], [_p, _q], lk.GREY, 0.6))
    for _u in np.linspace(_a, _b, _n + 1):
        for _w in np.linspace(_p, _q, _n + 1):
            _lines.append(([_u, _u], [_c, _d], [_w, _w], lk.GREY, 0.6))
    for _v in np.linspace(_c, _d, _n + 1):
        for _w in np.linspace(_p, _q, _n + 1):
            _lines.append(([_a, _b], [_v, _v], [_w, _w], lk.GREY, 0.6))
    for _u in (_a, _b):
        for _v in (_c, _d):
            _lines.append(([_u, _u], [_v, _v], [_p, _q], lk.BLUE, 1.6))
        for _w in (_p, _q):
            _lines.append(([_u, _u], [_c, _d], [_w, _w], lk.BLUE, 1.6))
    for _v in (_c, _d):
        for _w in (_p, _q):
            _lines.append(([_a, _b], [_v, _v], [_w, _w], lk.BLUE, 1.6))
    _h = np.array([_b - _a, _d - _c, _q - _p]) / _n
    _u = np.random.default_rng(30).uniform(0.15, 0.85, (_n, _n, _n, 3))
    _pts = [((_a + (_i + _u[_i, _j, _k, 0]) * _h[0], _c + (_j + _u[_i, _j, _k, 1]) * _h[1], _p + (_k + _u[_i, _j, _k, 2]) * _h[2]), lk.BLUE, 2.6) for _i in range(_n) for _j in range(_n) for _k in range(_n)]
    lk.turntable(
        35,
        22,
        "the box B cut into N^3 smaller boxes of the same size, with a chosen point in each",
        [
            lk.panel(
                1.0,
                lines=_lines,
                points=_pts,
                texts=[(((_a + _b) / 2, _c, _q), "b - a", "#000000", 150, 12), ((_b, (_c + _d) / 2, _p), "d - c", "#000000", -90, 10), ((_a, _d, (_p + _q) / 2), "q - p", "#000000", 0, 14)],
                box=((0.2, 2.2), (0.2, 2.6), (0, 1.7)),
            )
        ],
        height=lk.H3D,
        key="L25-box",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, nb):
    # module: triple integrals
    # text: how to define the triple integral
    lk.prose(
        r"""
        $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ and $B = [a, b] \times [c, d] \times [p, q] \subset \mathbb{R}^3$

        how do we define $\displaystyle\iiint_B f \, dV$?

        $\leadsto$ &nbsp; divide into $N^3$ smaller boxes (of same size)

        $\leadsto$ &nbsp; pick points in each box and evaluate $f$

        $\leadsto$ &nbsp; multiply the value and the volume of the boxes

        $\leadsto$ &nbsp; take the sum and then the $\lim$ $N \to \infty$

        > if well defined, that is $\displaystyle\iiint_B f \, dV$
        """,
        lk.interactive(lk.frame("L25-box", lk.H3D), controls=[nb]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: triple integrals
    # theorem: Fubini in 3d
    lk.theorem(
        r"""
        If $f : B \subset \mathbb{R}^3 \longrightarrow \mathbb{R}$ is continuous

        $$
        \begin{aligned}
        \iiint_B f \, dV &= \int_p^q \left[ \int_c^d \left( \int_a^b f(x, y, z) \, dx \right) dy \right] dz \\
        &= \int_a^b \left[ \int_p^q \left( \int_c^d f(x, y, z) \, dy \right) dz \right] dx \\
        &= \text{any other order!}
        \end{aligned}
        $$
        """,
        title="Fubini in 3d",
        label="thm-fubini-3d",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: triple integrals
    # example: f = x + z over a box
    lk.example(
        r"""
        $f(x, y, z) = x + z$, $B = [0, 1] \times [0, 1] \times [0, 2]$

        $$
        \begin{aligned}
        \Longrightarrow \quad \iiint_B f \, dV &= \int_0^2 \left[ \int_0^1 \left( \int_0^1 (x + z) \, dx \right) dy \right] dz \\
        &= \int_0^2 \left[ \int_0^1 \left( \tfrac{1}{2} + z \right) dy \right] dz = \int_0^2 \left( \tfrac{1}{2} + z \right) dz = 3
        \end{aligned}
        $$
        """,
        label="ex-box",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # definition: z-simple region
    lk.definition(
        r"""
        A region $W \subseteq \mathbb{R}^3$ is called **$z$-simple** if

        $$
        W = \lbrace (x, y, z) \mid (x, y) \in D, \ \eta_1(x, y) \leqslant z \leqslant \eta_2(x, y) \rbrace
        $$

        for $\eta_1, \eta_2 : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ continuous functions over a simple region $D \subseteq \mathbb{R}^2$.
        """,
        label="def-z-simple",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: simple regions
    # example: tetrahedron
    # the tetrahedron W with corners (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1) (blue faces), and its base D, the triangle in
    # the xy-plane (red edges)
    _O, _X, _Y, _Z = (np.array(v, float) for v in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))
    _faces = [lk.patch([_X, _Y, _Z, _Z], lk.LIGHT, 0.6), lk.patch([_O, _X, _Z, _Z], lk.LIGHT, 0.6), lk.patch([_O, _Y, _Z, _Z], lk.LIGHT, 0.6)]
    _edges = [([_p[0], _q[0]], [_p[1], _q[1]], [_p[2], _q[2]], lk.BLUE, 1.6) for _p, _q in ((_X, _Z), (_Y, _Z), (_O, _Z))]
    _base = [([_p[0], _q[0]], [_p[1], _q[1]], [0, 0], lk.RED, 2.0) for _p, _q in ((_O, _X), (_X, _Y), (_Y, _O))]
    _fig = lk.turntable(
        35,
        22,
        "the tetrahedron W with corners at the origin and at (1, 0, 0), (0, 1, 0), (0, 0, 1), and its base D, a triangle in the xy-plane",
        [
            lk.panel(
                1.0,
                surfaces=[lk.patch([_O, _X, _Y, _Y], lk.RED, 0.15)] + _faces,
                lines=_edges + _base,
                axes=[((0, 0, 0), (1.5, 0, 0), "x", -150), ((0, 0, 0), (0, 1.5, 0), "y", -20), ((0, 0, 0), (0, 0, 1.4), "z", 90)],
                texts=[((1, 0, 0), "1", "#000000", -60, 8), ((0, 1, 0), "1", "#000000", -60, 8), ((0, 0, 1), "1", "#000000", 180, 8), ((0.55, 0.55, 0.0), "D", lk.RED, -60, 10), ((0.3, 0.3, 0.4), "W", lk.BLUE, 30, 10)],
                box=((0, 1.4), (0, 1.4), (0, 1.3)),
            )
        ],
        height=lk.H3D,
        key="L25-tetrahedron",
    )
    lk.example(
        [
            lk.aside(r"$\mk{W} = \lbrace (x, y, z) \mid x, y, z \geqslant 0, \ x + y + z \leqslant 1 \rbrace$", "tetrahedron"),
            r"""
            > $\eta_1(x, y) = 0$

            > $\eta_2(x, y) = 1 - x - y$

            > $$
            > \begin{aligned}
            > D &= \lbrace (x, y) \mid x, y \geqslant 0, \ x + y \leqslant 1 \rbrace \\
            > &= \lbrace (x, y) \mid x \in [0, 1], \ 0 \leqslant y \leqslant 1 - x \rbrace \\
            > &= \lbrace (x, y) \mid y \in [0, 1], \ 0 \leqslant x \leqslant 1 - y \rbrace
            > \end{aligned}
            > $$
            """,
            lk.figure(_fig),
        ],
        label="ex-tetrahedron",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # definition: triple integral over a z-simple region
    lk.definition(
        r"""
        Given $W \subseteq \mathbb{R}^3$ a $z$-simple region and $f : W \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ a continuous function

        $$
        \begin{aligned}
        \iiint_W f \, dV &= \iint_D \left( \int_{\eta_1(x, y)}^{\eta_2(x, y)} f(x, y, z) \, dz \right) dxdy \\
        &= \int_a^b \left[ \int_{\varphi_1(x)}^{\varphi_2(x)} \left( \int_{\eta_1(x, y)}^{\eta_2(x, y)} f(x, y, z) \, dz \right) dy \right] dx
        \end{aligned}
        $$
        """,
        label="def-triple-integral",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # remark: y-simple and x-simple regions
    lk.remark(r"Similar definitions for $y$-simple and $x$-simple regions in $\mathbb{R}^3$ and for integrals over them.")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: simple regions
    # example: volume of the tetrahedron
    lk.example(
        r"""
        Volume of $W$:

        $$
        \begin{aligned}
        \iiint_W dV &= \int_0^1 \left[ \int_0^{1 - x} \left( \int_0^{1 - x - y} dz \right) dy \right] dx \\
        &= \int_0^1 \left[ \int_0^{1 - x} (1 - x - y) \, dy \right] dx \\
        &= \int_0^1 \left[ (1 - x)^2 - \frac{(1 - x)^2}{2} \right] dx = \frac{1}{6}
        \end{aligned}
        $$

        > $\leadsto$ &nbsp; six tetrahedra fit inside one cube
        """,
        label="ex-volume",
    )
    return


if __name__ == "__main__":
    app.run()
