import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 11 · Affine approximations and the derivative of general maps", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc, FancyArrowPatch

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Arc, FancyArrowPatch, Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(11, "Affine approximations and the derivative of general maps")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math):
    # Helpers of this lecture: a bare sketch, bare coordinate axes, a label beside a point

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr."""
        lk.arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        lk.arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    def tip_label(ax, at, angle, text, color, r=7, fontsize=13):
        """Label next to the point `at`, pushed away from it in the direction `angle` (degrees); the text is anchored
        on the side facing the point, so that long labels never run back over it. No box behind it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ha = "left" if c > 0.35 else "right" if c < -0.35 else "center"
        va = "bottom" if s > 0.35 else "top" if s < -0.35 else "center"
        ax.annotate(text, at, textcoords="offset points", xytext=(r * c, r * s), ha=ha, va=va, color=color, fontsize=fontsize, zorder=5)

    def right_angle(ax, at, d1, d2, size=0.22, color="black"):
        """A small right-angle mark at `at` between the unit directions d1 and d2."""
        p1 = (at[0] + size * d1[0], at[1] + size * d1[1])
        p2 = (p1[0] + size * d2[0], p1[1] + size * d2[1])
        p3 = (at[0] + size * d2[0], at[1] + size * d2[1])
        ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=color, lw=0.8)

    return blank, cross_axes, right_angle, tip_label


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    phi = lk.slider(0, 355, step=5, value=40, label=r"$\varphi$")
    a_line = lk.slider(0.4, 1.9, step=0.1, value=1.5, label="$a$")
    pa1 = lk.slider(1, 2.5, step=0.25, value=2, label="$a^1$")
    pk = lk.slider(0, 12, step=1, value=4, label=r"$a^2 = k\pi / 12$")
    return a_line, pa1, phi, pk


@app.cell(hide_code=True)
def _(blank, cross_axes, lk, math, np, phi, right_angle, tip_label):
    # module: recap
    # recap: the derivative and the gradient, with the level sets of f = (x^1)^2/9 + (x^2)^2/4
    _p = math.radians(phi.value)
    _a = (3 * math.cos(_p), 2 * math.sin(_p))
    _grad = (2 * _a[0] / 9, 2 * _a[1] / 4)
    _tip = (_a[0] + _grad[0], _a[1] + _grad[1])
    _dir = math.degrees(math.atan2(_grad[1], _grad[0]))
    _gl = math.hypot(*_grad)
    _n = (_grad[0] / _gl, _grad[1] / _gl)
    _t = (-_n[1], _n[0])

    _fig, _ax = blank(4.0, 2.6, (-4.4, 4.9), (-2.9, 3.1))
    cross_axes(_ax, (-4.2, 4.8), (-2.8, 3.0), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(3 * np.cos(_th), 2 * np.sin(_th), color=lk.BLUE, lw=1.4)
    # the semi-axes, written inside the ellipse so that the name of the level set outside never meets them
    for _x, _txt in ((3, "$3r$"), (-3, "$-3r$")):
        _ax.annotate(_txt, (_x, 0), textcoords="offset points", xytext=(-3 if _x > 0 else 3, -3), ha="right" if _x > 0 else "left", va="top", fontsize=11)
    for _y, _txt in ((2, "$2r$"), (-2, "$-2r$")):
        _ax.annotate(_txt, (0, _y), textcoords="offset points", xytext=(4, -3 if _y > 0 else 3), ha="left", va="top" if _y > 0 else "bottom", fontsize=11)
    _q = _p + math.pi + 0.6  # the name of the level set sits on the ellipse, away from a and its gradient
    tip_label(_ax, (3 * math.cos(_q), 2 * math.sin(_q)), math.degrees(math.atan2(math.sin(_q) / 2, math.cos(_q) / 3)), "$f^{-1}(r^2)$", lk.BLUE)
    lk.arrow(_ax, (0, 0), _a, "black")
    tip_label(_ax, (_a[0] / 2, _a[1] / 2), math.degrees(_p) + 90, r"$\vec{a}$", "black")
    lk.arrow(_ax, _a, _tip, lk.GREEN)
    right_angle(_ax, _a, _n, _t, size=0.2)
    tip_label(_ax, _tip, _dir + 40, r"$\vec{\nabla} f(\vec{a})$", lk.GREEN)
    _ax.plot(*_a, "o", color="black", ms=4, zorder=4)

    lk.recap(
        "The derivative and the gradient",
        lk.gap(),
        r"""
        $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$

        > $\Longleftrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) & \cdots & {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)$ defines a good affine approximation for $f$ at $\vec{a}$ in the sense that

        > > $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0$
        """,
        lk.gap(),
        lk.aside(
            r"$Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the <span class='lk-mark'>**derivative**</span> of $f$ at $\vec{a}$",
            "linear function taking vectors<br>to directional derivatives",
        ),
        lk.aside(
            r"$\vec{\nabla} f(\vec{a}) = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\ \vdots \\ {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix} \in \mathbb{R}^n$ is the <span class='lk-mark'>**gradient**</span> of $f$ at $\vec{a}$",
            "vector pointing in some direction<br>with some length",
        ),
        lk.gap(),
        r"Theorem: $\vec{\nabla} f(\vec{a})$ points in the direction of steepest ascent of $f$ at $\vec{a}$, and it is perpendicular to the level set of $f$ "
        + lk.gloss(r"through $\vec{a}$", r"containing $\vec{a}$"),
        lk.gap(),
        r"""
        Example: $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = {\large\tfrac{(x^1)^2}{9}} + {\large\tfrac{(x^2)^2}{4}}$

        > $\leadsto$ &nbsp; level sets $f^{-1}(r^2) = \underbrace{\left\{ \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; {\large\tfrac{(x^1)^2}{9r^2}} + {\large\tfrac{(x^2)^2}{4r^2}} = 1 \right\}}_{\footnotesize \begin{array}{c} \text{horizontal ellipse centered at } \vec{0} \\ \text{with semi-axes } 3r \text{ and } 2r \end{array}}$
        """,
        lk.gap(),
        lk.gap(),
        r"""
        > $\vec{\nabla} f(\vec{a}) = \begin{bmatrix} {\large\tfrac{2}{9}} a^1 \\[4pt] {\large\tfrac{2}{4}} a^2 \end{bmatrix}$
        """,
        lk.interactive(_fig, controls=[phi]),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        "Affine approximations and their graphs",
        r"Derivative for general maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$",
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine approximations
    # section
    lk.section("Affine approximations")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine approximations
    # definition: affine approximation
    lk.definition(
        [
            r"Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, the **affine approximation** of $f$ at $\vec{a}$ is the "
            + lk.gloss("affine function", "linear plus constant")
            + r" $g : \mathbb{R}^n \longrightarrow \mathbb{R}$",
            r"""
            $$
            \begin{aligned}
            g(\vec{x}) &= f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})\\
            &= f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})(x^1 - a^1) + \dots + \frac{\partial f}{\partial x^n}(\vec{a})(x^n - a^n)
            \end{aligned}
            $$
            """,
        ],
        label="def-affine",
    )
    return


@app.cell(hide_code=True)
def _(a_line, blank, cross_axes, lk, math, np, right_angle, tip_label):
    # module: affine approximations
    # remark: n = 1, the tangent line, its velocity vector and its normal
    _a = a_line.value
    _fa = 4 * _a * math.exp(-_a)
    _d = 4 * (1 - _a) * math.exp(-_a)
    _slope = math.degrees(math.atan2(_d, 1))
    _l = math.hypot(1, _d)

    _fig, _ax = blank(4.6, 2.4, (-1.75, 6.6), (-0.6, 3.45))
    cross_axes(_ax, (-1.7, 6.2), (-0.5, 3.0), "$x$", "$y$")
    _x = np.linspace(-0.1, 5.1, 300)
    _ax.plot(_x, 4 * _x * np.exp(-_x), color=lk.BLUE, lw=1.4)
    _ax.text(5.2, 0.2, "$y = f(x)$", color=lk.BLUE, fontsize=13, ha="left", va="bottom")
    # the tangent line, as far as it stays inside the frame
    _s = np.linspace(-1.7, 4.9, 400)
    _t = _fa + _d * (_s - _a)
    _in = (_t > -0.5) & (_t < 3.0)
    _ax.plot(_s[_in], _t[_in], color=lk.GREEN, lw=1.0)
    lk.arrow(_ax, (0, 0), (_a, _fa), "black")
    lk.arrow(_ax, (_a, _fa), (_a + 1, _fa + _d), lk.ORANGE)
    lk.arrow(_ax, (_a, _fa), (_a - _d, _fa + 1), lk.RED)
    right_angle(_ax, (_a, _fa), (1 / _l, _d / _l), (-_d / _l, 1 / _l), size=0.2)
    tip_label(_ax, (_a - _d, _fa + 1), _slope + 90, r"$\vec{n}$", lk.RED)
    _ax.plot(_a, _fa, "o", color="black", ms=4, zorder=4)
    tip_label(_ax, (_a + 1, _fa + _d), _slope + (90 if _a < 2 else -90), r"$\genfrac{[}{]}{0}{0}{1}{f'(a)}$", lk.ORANGE)  # the velocity vector of the line, on the side away from the curve
    _ax.text(6.2, 3.05, "$y = f(a) + f'(a)(x - a)$", color=lk.GREEN, fontsize=13, ha="right", va="bottom")  # one place, above where the line is cut
    _ax.annotate(r"$\genfrac{[}{]}{0}{0}{a}{f(a)}$", (0.6 * _a, 0.6 * _fa), textcoords="offset points", xytext=(10, 3), ha="left", va="top", fontsize=13, zorder=5)  # under its arrow, slides with it

    lk.remark(
        [
            r"""
            For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $g : \mathbb{R} \longrightarrow \mathbb{R}$

            $$
            g(x) = f(a) + f'(a)(x - a)
            $$

            is the affine function whose graph is the tangent line to the graph of $f$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$
            """,
            lk.gap(),
            r"> $y = f(x)$ &nbsp; $\leadsto$ &nbsp; $\begin{bmatrix} x \\ f(x) \end{bmatrix}$",
            lk.aside(
                r"> $y = f(a) + f'(a)(x - a)$ &nbsp; $\leadsto$ &nbsp; $\begin{bmatrix} a \\ f(a) \end{bmatrix} + (x - a) \mk{\begin{bmatrix} 1 \\ f'(a) \end{bmatrix}}$",
                "velocity vector of the tangent line",
            ),
            lk.aside(
                r"> $\mk{\vec{n}} = \begin{bmatrix} -f'(a) \\ 1 \end{bmatrix}$",
                "normal to the tangent line",
            ),
            lk.interactive(_fig, controls=[a_line]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent plane
    # section
    lk.section("The tangent plane")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent plane
    # theorem: the graph of the affine approximation is the tangent plane
    lk.theorem(
        r"""
        $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

        > the graph of the affine approximation of $f$ at $\vec{a}$ is a plane in $\mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R}$ through $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$ with normal vector

        $$
        \vec{n} = \begin{bmatrix} -{\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\[6pt] -{\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \\[6pt] 1 \end{bmatrix}
        $$

        $\leadsto$ &nbsp; the **tangent plane** to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$
        """,
        label="thm-tangent-plane",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent plane
    # proof: the graph of the affine approximation is the tangent plane
    lk.proof(
        [
            r"""
            $\mathrm{graph}(g) = \left\{ \begin{bmatrix} x^1 \\ x^2 \\ f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \right\}$

            $\phantom{\mathrm{graph}(g)} = \left\{ \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \\ Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \right\}$

            $\phantom{\mathrm{graph}(g)} = \left\{ \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \underbrace{(x^1 - a^1)}_{t} \underbrace{\begin{bmatrix} 1 \\ 0 \\ {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \end{bmatrix}}_{\text{velocity vector}} + \underbrace{(x^2 - a^2)}_{s} \underbrace{\begin{bmatrix} 0 \\ 1 \\ {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \end{bmatrix}}_{\text{velocity vector}} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \right\}\rule[-2.4em]{0pt}{0pt}$
            """,
            lk.gap(),
            r"""
            $\vec{n} = \begin{bmatrix} n^1 \\ n^2 \\ n^3 \end{bmatrix}$ such that $\vec{n} \cdot \underbrace{\begin{bmatrix} 1 \\ 0 \\ {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \end{bmatrix}}_{\vec{u}} = 0 = \vec{n} \cdot \underbrace{\begin{bmatrix} 0 \\ 1 \\ {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \end{bmatrix}}_{\vec{v}}\rule[-2.2em]{0pt}{0pt}$

            > $\leadsto$ &nbsp; $\vec{n} = \vec{u} \times \vec{v} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 0 & {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\[4pt] 0 & 1 & {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \end{bmatrix}$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: tangent plane
    # illustration: graph(f) with its tangent plane at (a, f(a)), the velocity vectors u, v and the normal n
    def _f(x1, x2):
        return 2.4 - 0.2 * ((x1 - 1.9) ** 2 + (x2 - 1.7) ** 2)

    _a = (1.5, 1.1)
    _d1, _d2 = -0.4 * (_a[0] - 1.9), -0.4 * (_a[1] - 1.7)
    _fa = float(_f(*_a))
    _lo, _hi, _k, _v = 0.5, 3.1, 1.0, 0.8  # the graph over [lo, hi]^2, the plane over a + [-k, k]^2, velocity vectors of length v
    _x1, _x2 = np.meshgrid(np.linspace(_lo, _hi, 25), np.linspace(_lo, _hi, 25), indexing="ij")
    _w = np.linspace(_lo, _hi, 25)
    _rim = [(_c + 0 * _w, _w) for _c in (_lo, _hi)] + [(_w, _c + 0 * _w) for _c in (_lo, _hi)]

    def _g(x1, x2):
        return _fa + _d1 * (x1 - _a[0]) + _d2 * (x2 - _a[1])

    _corners = [(_a[0] + _k * _i, _a[1] + _k * _j) for _i, _j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    _s = np.linspace(0, 1, 30)
    _edges = [(_p[0] + _s * (_q[0] - _p[0]), _p[1] + _s * (_q[1] - _p[1])) for _p, _q in zip(_corners, _corners[1:] + _corners[:1])]
    _graph = lk.turntable(
        28,
        32,
        "graph of f with its tangent plane at the point above a, the two velocity vectors spanning the plane and the normal vector n",
        [
            lk.panel(
                1.0,
                surfaces=[
                    lk.sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, lk.BLUE, 0.5), (1, 4, lk.BLUE, 0.5)]),
                    lk.patch([(_c[0], _c[1], _g(*_c)) for _c in _corners], lk.GREEN, 0.18),
                ],
                lines=[(_c1, _c2, _f(_c1, _c2), lk.BLUE, 1.2) for _c1, _c2 in _rim]
                + [(_c1, _c2, _g(_c1, _c2), lk.GREEN, 1.2) for _c1, _c2 in _edges]
                + [
                    (_a[0] + 0 * _s, _a[1] * _s, 0 * _s, lk.GREY, 1.0, [4, 3]),
                    (_a[0] * _s, _a[1] + 0 * _s, 0 * _s, lk.GREY, 1.0, [4, 3]),
                    (_a[0] + 0 * _s, _a[1] + 0 * _s, _fa * _s, lk.GREY, 1.0, [4, 3]),
                ],
                points=[((_a[0], _a[1], _fa), "#000000"), ((_a[0], _a[1], 0), lk.GREY, 3.4)],
                arrows=[
                    ((_a[0], _a[1], _fa), (_a[0] + _v, _a[1], _fa + _v * _d1), lk.ORANGE),
                    ((_a[0], _a[1], _fa), (_a[0], _a[1] + _v, _fa + _v * _d2), lk.ORANGE),
                    ((_a[0], _a[1], _fa), (_a[0] - _d1, _a[1] - _d2, _fa + 1), lk.RED),
                ],
                axes=[((0, 0, 0), (3.6, 0, 0), "x^1", -150), ((0, 0, 0), (0, 3.6, 0), "x^2", -20), ((0, 0, 0), (0, 0, 3.0), "y", 90)],
                texts=[
                    ((_hi, _lo, _f(_hi, _lo)), r"y = f(\vec{x})", lk.BLUE, 200, 8),
                    ((_corners[3][0], _corners[3][1], _g(*_corners[3])), r"y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})", lk.GREEN, 10, 8),
                    ((_a[0] - _d1, _a[1] - _d2, _fa + 1), r"\vec{n}", lk.RED, 0, 6),
                    ((_a[0] + _v, _a[1], _fa + _v * _d1), r"\vec{u}", lk.ORANGE, -150, 6),
                    ((_a[0], _a[1] + _v, _fa + _v * _d2), r"\vec{v}", lk.ORANGE, -20, 6),
                    ((_a[0], _a[1], 0), r"\vec{a}", "#000000", -90, 6),
                ],
            )
        ],
        height=lk.H3D,
        width=520,
        zoom=1.3,
        bias=0.16,  # the point and the vectors at the tangency lie on both surfaces: draw them in front
    )
    lk.prose(
        r"""
        $y = f(\vec{x})$ &nbsp; $\leadsto$ &nbsp; $\begin{bmatrix} x^1 \\ x^2 \\ f(\vec{x}) \end{bmatrix}$

        $y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$ &nbsp; $\leadsto$ &nbsp; $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + (x^1 - a^1) \begin{bmatrix} 1 \\ 0 \\ {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \end{bmatrix} + (x^2 - a^2) \begin{bmatrix} 0 \\ 1 \\ {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \end{bmatrix}$
        """,
        lk.figure(_graph),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent plane
    # example: tangent plane of f = x^1 e^{x^2} at a = (1, 0)
    lk.example(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$, $\vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$

        > tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$

        > > $\leadsto$ &nbsp; $\vec{\nabla} f(\vec{a}) = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\[4pt] {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \end{bmatrix} = \begin{bmatrix} e^{a^2} \\ a^1 e^{a^2} \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$

        > > $\leadsto$ &nbsp; $\vec{n} = \begin{bmatrix} -{\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\[4pt] -{\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) \\[4pt] 1 \end{bmatrix} = \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix}$

        > > $\leadsto$ &nbsp; plane through $\begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$ normal to $\begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix}$

        > > <span class='lk-ghost'>$\leadsto$ &nbsp; plane</span> $= \left\{ \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; -1 \cdot (y^1 - 1) - 1 \cdot (y^2 - 0) + 1 \cdot (y^3 - 1) = 0 \right\}$

        > > <span class='lk-ghost'>$\leadsto$ &nbsp; plane</span> $= \left\{ \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; y^3 = y^1 + y^2 \right\} = \mathrm{graph}(g)$

        > > $\leadsto$ &nbsp; affine approximation $g(\vec{x}) = 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 \end{bmatrix} = 1 + (x^1 - 1) + x^2$
        """,
        label="ex-tangent-plane",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent plane
    # remark: how good the approximation is near a
    lk.remark(
        r"""
        $\vec{x} = \begin{bmatrix} 1.1 \\ -0.1 \end{bmatrix}$

        > $\Longrightarrow$ &nbsp; $f(\vec{x}) = 1.1 \, e^{-0.1} \approx 0.995$, &nbsp; $g(\vec{x}) = 1.1 - 0.1 = 1$

        > $\Longrightarrow$ &nbsp; $f(\vec{x}) - g(\vec{x}) \approx -0.005$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: general maps
    # section
    lk.section("The derivative of general maps")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: general maps
    # remark: components of f : R^n -> R^m
    lk.remark(
        r"""
        $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $f\left( \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \right) = \begin{bmatrix} f^1(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}$

        > with each $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ a scalar function on $\mathbb{R}^n$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: general maps
    # definition: differentiable maps, derivative and Jacobian matrix
    lk.definition(
        r"""
        $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ \vdots \\ a^n \end{bmatrix}$ if each component $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{a}$

        > $\Longrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} Df^1(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix} = \begin{bmatrix} {\large\tfrac{\partial f^1}{\partial x^1}}(\vec{a}) & \cdots & {\large\tfrac{\partial f^1}{\partial x^n}}(\vec{a}) \\ \vdots & \ddots & \vdots \\ {\large\tfrac{\partial f^m}{\partial x^1}}(\vec{a}) & \cdots & {\large\tfrac{\partial f^m}{\partial x^n}}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(m \times n)$

        > > defines an affine approximation of $f$ at $\vec{a}$ in the sense

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{\underbrace{f(\vec{x})}_{\mathbb{R}^m} - \underbrace{f(\vec{a})}_{\mathbb{R}^m} - \underbrace{Df(\vec{a})}_{\mathrm{Mat}(m \times n)} \underbrace{(\vec{x} - \vec{a})}_{\mathbb{R}^n}}{\lVert \vec{x} - \vec{a} \rVert} = \vec{0} \in \mathbb{R}^m
        $$

        If $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$, the linear transformation $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called the **derivative** of $f$ at $\vec{a}$ or the **Jacobian matrix** of $f$ at $\vec{a}$, $Df(\vec{a}) \in \mathrm{Mat}(m \times n)$
        """,
        label="def-jacobian",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: general maps
    # theorem: differentiability with one limit
    lk.theorem(
        [
            r"$f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$ if and only if",
            lk.aside(
                r"""
                $$
                \lim_{\vec{x} \to \vec{a}} \mk{\frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert}} = 0
                $$
                """,
                r"scalar valued function on $\mathbb{R}^n$",
            ),
            r"$\leadsto$ &nbsp; we only need to compute 1 limit instead of $m$",
        ],
        label="thm-one-limit",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: general maps
    # theorem: continuous partial derivatives imply differentiable
    lk.theorem(
        r"If all components $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ of $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ have "
        + lk.gloss(r"well-defined partial derivatives in an open ball centered at $\vec{a}$, and they are all continuous at $\vec{x} = \vec{a}$", r"$f$ is $C^1$-smooth at $\vec{a}$")
        + r", then $f$ is differentiable at $\vec{x} = \vec{a}$",
        label="thm-c1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: general maps
    # example: a linear map has itself as derivative
    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \underbrace{\begin{bmatrix} a & b \\ c & d \end{bmatrix}}_{A \, \in \, \mathrm{Mat}(2 \times 2)} \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \end{bmatrix} = \begin{bmatrix} f^1(\vec{x}) \\ f^2(\vec{x}) \end{bmatrix}\rule[-1.8em]{0pt}{0pt}$
            """,
            lk.aside(
                r"> $f^1(\vec{x})$, $f^2(\vec{x})$ are <span class='lk-mark'>$C^1$-smooth everywhere in $\mathbb{R}^2$</span>",
                "linear combination of<br>elementary functions",
            ),
            r"""
            > > $\Longrightarrow$ &nbsp; $f$ is differentiable at any $\vec{a} \in \mathbb{R}^2$

            > > $\Longrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} {\large\tfrac{\partial f^1}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f^1}{\partial x^2}}(\vec{a}) \\[6pt] {\large\tfrac{\partial f^2}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f^2}{\partial x^2}}(\vec{a}) \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = A$
            """,
        ],
        label="ex-linear",
    )
    return


@app.cell(hide_code=True)
def _(Arc, FancyArrowPatch, Figure, cross_axes, lk, math, pa1, pk, tip_label):
    # module: general maps
    # example: the polar map, with the images of e_1 and e_2 under Df(a)
    _a1, _a2 = pa1.value, pk.value * math.pi / 12
    _c, _s = math.cos(_a2), math.sin(_a2)
    _fa = (_a1 * _c, _a1 * _s)
    _deg = math.degrees(_a2)
    _dash = (0, (4, 3))

    # both panels are drawn at the same scale
    _fig = Figure(figsize=(lk.FULL, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[5.6, 12.6])
    for _ax, _xlim in ((_left, (-0.8, 4.8)), (_right, (-6.3, 6.3))):
        _ax.set_xlim(*_xlim)
        _ax.set_ylim(-3.5, 5.3)
        _ax.set_aspect("equal")
        _ax.axis("off")

    cross_axes(_left, (-0.6, 4.7), (-0.6, 5.2), "$x^1$", "$x^2$")
    _left.plot([_a1, _a1, 0], [0, _a2, _a2], color=lk.GREY, lw=0.9, ls=_dash)
    lk.arrow(_left, (0, 0), (_a1, _a2), "black")
    lk.arrow(_left, (_a1, _a2), (_a1 + 1, _a2), lk.BLUE)
    lk.arrow(_left, (_a1, _a2), (_a1, _a2 + 1), lk.RED)
    tip_label(_left, (_a1 + 1, _a2), 30 if pk.value == 0 else 0, r"$\vec{e}_1$", lk.BLUE)  # off the x^1 axis when the arrow lies on it
    tip_label(_left, (_a1, _a2 + 1), 90, r"$\vec{e}_2$", lk.RED)
    _left.plot(_a1, _a2, "o", color="black", ms=4, zorder=4)

    cross_axes(_right, (-6.2, 6.2), (-3.4, 5.2), "$y^1$", "$y^2$")
    _right.plot([_fa[0], _fa[0], 0], [0, _fa[1], _fa[1]], color=lk.GREY, lw=0.9, ls=_dash)
    if _deg > 0:
        _right.add_patch(Arc((0, 0), 0.8, 0.8, theta1=0, theta2=_deg, color=lk.GREEN, lw=1.4))
        _right.text(0.7 * math.cos(_a2 / 2), 0.7 * math.sin(_a2 / 2), "$a^2$", color=lk.GREEN, fontsize=11, ha="center", va="center")  # the angle of f(a)
    lk.arrow(_right, (0, 0), _fa, "black")
    tip_label(_right, (_fa[0] / 2, _fa[1] / 2), _deg + 90, "$a^1$", "black", fontsize=11)  # the length of f(a), on the side away from the angle
    _t1 = (_fa[0] + _c, _fa[1] + _s)
    _t2 = (_fa[0] - _a1 * _s, _fa[1] + _a1 * _c)
    lk.arrow(_right, _fa, _t1, lk.BLUE)
    lk.arrow(_right, _fa, _t2, lk.RED)
    tip_label(_right, _t1, _deg + 30 if pk.value % 6 == 0 else _deg, r"$Df(\vec{a})(\vec{e}_1)$", lk.BLUE, fontsize=12)  # off the axis when the arrow lies on one
    tip_label(_right, _t2, _deg + 90, r"$Df(\vec{a})(\vec{e}_2)$", lk.RED, fontsize=12)
    _right.plot(*_fa, "o", color="black", ms=4, zorder=4)

    def _free(*taken):
        """The middle of the widest gap between the directions `taken` (degrees)."""
        t = sorted({round(_q % 360, 6) for _q in taken})
        gaps = [((t[(_i + 1) % len(t)] - t[_i]) % 360 or 360, t[_i]) for _i in range(len(t))]
        g, t0 = max(gaps)
        return t0 + g / 2

    _arrow = math.degrees(math.atan2(_a2, _a1))
    _near = lambda x, y: ([0, 180] if abs(y) < 1e-9 else [225, 270, 315] if 0 < y < 0.8 else [45, 90, 135] if -0.8 < y < 0 else []) + (
        [90, 270] if abs(x) < 1e-9 else [135, 180, 225] if 0 < x < 0.8 else [-45, 0, 45] if -0.8 < x < 0 else [])  # the axes close by
    tip_label(_left, (_a1, _a2), _free(0, 90, 180, 270, _arrow + 180, *_near(_a1, _a2)), r"$\vec{a}$", "black")
    tip_label(_right, _fa, _deg - 45, r"$f(\vec{a})$", "black")  # turns with the vectors at f(a)
    # the map f takes the left picture to the right one (the arrow of the sketch)
    _fig.patches.append(
        FancyArrowPatch(
            (0.31, 0.86), (0.43, 0.86), transform=_fig.transFigure, connectionstyle="arc3,rad=-0.35", arrowstyle="-|>,head_length=5,head_width=2", color="black", lw=1.0
        )
    )
    _fig.text(0.37, 0.95, "$f$", ha="center", va="center", fontsize=13)

    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 \cos(x^2) \\ x^1 \sin(x^2) \end{bmatrix}$, $\vec{a} = \begin{bmatrix} 2 \\ \pi/3 \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} \cos(a^2) & -a^1 \sin(a^2) \\ \sin(a^2) & a^1 \cos(a^2) \end{bmatrix} = \begin{bmatrix} \sqrt{1}/2 & -\sqrt{3} \\ \sqrt{3}/2 & \sqrt{1} \end{bmatrix}$

            > $f(\vec{a}) = \begin{bmatrix} 2\cos(\pi/3) \\ 2\sin(\pi/3) \end{bmatrix} = \begin{bmatrix} \sqrt{1} \\ \sqrt{3} \end{bmatrix}$, &nbsp; $Df(\vec{a})(\vec{e}_1) = \begin{bmatrix} \sqrt{1}/2 \\ \sqrt{3}/2 \end{bmatrix}$, &nbsp; $Df(\vec{a})(\vec{e}_2) = \begin{bmatrix} -\sqrt{3} \\ \sqrt{1} \end{bmatrix}$
            """,
            lk.interactive(_fig, controls=[pa1, pk]),
        ],
        label="ex-polar",
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
    # exercise: tangent plane and estimate
    lk.exercise(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 x^2$, $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$

        a) Write the derivative and the gradient of $f$ at $\vec{a}$

        b) Write the equation for the tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$

        c) Estimate $f\left( \begin{bmatrix} 1.1 \\ 1.9 \end{bmatrix} \right)$ and compare with the exact value
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: derivative and affine approximations of a map R^2 -> R^3
    lk.exercise(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \\ (x^2)^2 \end{bmatrix}$

        a) Compute the derivative of $f$ at $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix}$

        b) Write the affine approximation of $f$ at $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$

        c) Write the affine approximation of $f$ at $\vec{b} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$

        d) How do the images of these approximations differ?
        """,
        label="ex-practice-2",
    )
    return


if __name__ == "__main__":
    app.run()
