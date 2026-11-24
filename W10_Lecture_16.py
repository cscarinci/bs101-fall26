import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 16 · Method of Lagrange multipliers", css_file="lecturekit/style.css")


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
    lk.lecture(16, "Method of Lagrange multipliers")
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
    fx = lk.slider(0, 50, step=0.5, value=10, label="$x^1$")
    kc = lk.slider(1, 7, step=0.5, value=6, label="$k$")
    return fx, kc


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Existence of global extrema on closed and bounded domains

        If $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a $\underbrace{\text{closed}}_{\footnotesize \begin{array}{c} \text{contains its} \\ \text{boundary} \end{array}}$ and $\underbrace{\text{bounded}}_{\footnotesize \begin{array}{c} \text{doesn't run off} \\ \text{to infinity} \end{array}}$ domain $D \subseteq \mathbb{R}^2$, then<br>$f$ has both global extrema in $D$
        """,
        lk.gap(),
        r"""
        Strategy: find all candidates and compare them

        > 1\. &nbsp; in $D - \mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; local extrema &nbsp; $\Longrightarrow$ &nbsp; critical points of $f$

        > <span class="lk-ghost">1\. &nbsp; in $D - \mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; local extrema &nbsp;</span>$\Longrightarrow$ &nbsp; $\vec{x} \in D - \mathrm{Bd}(D)$ such that $\vec{\nabla} f(\vec{x}) = \vec{0}$

        > 2\. &nbsp; in $\mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; global extrema of $f \circ \gamma$ on $[a, b]$ for some parameterization of $\mathrm{Bd}(D)$

        > <span class="lk-ghost">2\. &nbsp; in $\mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp;</span>&emsp;&emsp;$\gamma : [a, b] \longrightarrow \mathbb{R}^2$ such that $\mathrm{Im}(\gamma) = \mathrm{Bd}(D)$

        > <span class="lk-ghost">2\. &nbsp; in $\mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp;</span>$\Longrightarrow$ &nbsp; $\gamma(t) \in \mathrm{Bd}(D)$ with

        > <span class="lk-ghost">2\. &nbsp; in $\mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; $\Longrightarrow$ &nbsp; or &nbsp;</span>• &nbsp; $t \in (a, b)$, &nbsp; $(f \circ \gamma)'(t) = 0$

        > <span class="lk-ghost">2\. &nbsp; in $\mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; $\Longrightarrow$ &nbsp;</span>or &nbsp; • &nbsp; $t = a, b$
        """,
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Method of Lagrange multipliers", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 3.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # section
    lk.section("Method of Lagrange multipliers")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # prose: why level sets
    lk.prose(
        r"""
        $\leadsto$ &nbsp; parameterizing $\mathrm{Bd}(D)$ is generally hard…

        $\leadsto$ &nbsp; describing $\mathrm{Bd}(D)$ with level sets is much easier!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # example: the boundary of D as level sets
    lk.example(
        [
            r"""
            $D = \left\{ \vec{x} \;\middle|\; (x^1)^2 \leqslant x^2 \leqslant 1 \right\}$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\mathrm{Bd}(D) = \Big\{ \vec{x} \;\Big|\; \mk{\overbrace{(x^1)^2 = x^2}^{\footnotesize (x^1)^2 - x^2 = 0}}, \ x^2 \leqslant 1 \Big\}$",
                r"level set of $g(\vec{x}) = (x^1)^2 - x^2$",
            ),
            lk.aside(
                r'> <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\mathrm{Bd}(D) =$</span> $\cup \Big\{ \vec{x} \;\Big|\; \mk{x^2 = 1}, \ -1 \leqslant x^1 \leqslant 1 \Big\}$',
                r"level set of $h(\vec{x}) = x^2 - 1$",
            ),
        ],
        label="ex-level-sets",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # prose: what Lagrange multipliers do
    lk.prose(
        r"""
        $\leadsto$ &nbsp; Lagrange multipliers allow us to find extrema of one function on the level sets of another

        > $\Longrightarrow$ &nbsp; no parameterizations needed!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # definition: constraint
    lk.definition(
        r"""
        A **constraint** is an $\underbrace{\text{equation } g(\vec{x}) = c}_{\footnotesize \text{constraint equation}}$, restricting the allowed values of $\vec{x}$ to the $\underbrace{\text{level set } g^{-1}(c)}_{\footnotesize \text{constraint curve}}$ of some $\underbrace{\text{function } g : \mathbb{R}^2 \longrightarrow \mathbb{R}}_{\footnotesize \text{constraint function}}$.
        """,
        label="def-constraint",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # prose: the problem
    lk.prose(
        r"""
        Problem: &nbsp; Given a function $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ and a constraint $g(\vec{x}) = c$, how to find max / min of $f$ restricted to the constraint curve $g^{-1}(c)$?
        """
    )
    return


@app.cell(hide_code=True)
def _(Figure, fx, lk):
    # module: lagrange
    # example: the fence
    # the rectangle with perimeter 100 at true proportions, x^2 = 50 - x^1, in a fixed window
    _x1 = round(fx.value, 10) + 0.0
    _x2 = 50 - _x1
    _fig = Figure(figsize=(2.3, 2.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-5, 60)
    _ax.set_ylim(-7, 55)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.fill([0, _x1, _x1, 0], [0, 0, _x2, _x2], color=lk.LIGHT, lw=0)
    _ax.plot([0, _x1, _x1, 0, 0], [0, 0, _x2, _x2, 0], color=lk.BLUE, lw=1.4)
    _ax.text(_x1 / 2, -1.5, "$x^1$", ha="center", va="top", fontsize=13)
    _ax.text(_x1 + 1.5, _x2 / 2, "$x^2$", ha="left", va="center", fontsize=13)
    lk.example(
        [
            r"Suppose you want to build a fence around some rectangular region. The fence must have perimeter $100\,$m. How to maximize the area?",
            lk.interactive(_fig, controls=[fx]),
            r"""
            > $\leadsto$ &nbsp; $\begin{cases} f(\vec{x}) = \text{area} = x^1 x^2 \\[6pt] g(\vec{x}) = \text{perimeter} = \underbrace{2x^1 + 2x^2 = 100}_{\footnotesize \text{constraint}} \end{cases}$
            """,
        ],
        label="ex-fence",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # definition: global maximum restricted to a constraint curve
    lk.definition(
        r"""
        Given $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ and $g : \mathbb{R}^2 \longrightarrow \mathbb{R}$, $\vec{a} \in g^{-1}(c)$ is a **global maximum of $f$ restricted to $g^{-1}(c)$** if

        $$
        f(\vec{a}) \geqslant f(\vec{x}) \qquad \forall \, \vec{x} \in g^{-1}(c)
        $$
        """,
        label="def-restricted-max",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # theorem: Lagrange multipliers
    lk.theorem(
        r"""
        Given $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ and $g : \mathbb{R}^2 \longrightarrow \mathbb{R}$ $C^1$-smooth

        If $\vec{a}$ is a global maximum of $f$ restricted to $g^{-1}(c)$ with $\vec{\nabla} g(\vec{a}) \neq \vec{0}$, then

        $$
        \underbrace{\text{there exists } \lambda \in \mathbb{R} \text{ such that } \vec{\nabla} f(\vec{a}) = \lambda \vec{\nabla} g(\vec{a})}_{\footnotesize \vec{\nabla} f(\vec{a}) \text{ is proportional to } \vec{\nabla} g(\vec{a})}
        $$
        """,
        title="Lagrange multipliers",
        label="thm-lagrange",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # prose: the name
    lk.prose(r"$\leadsto$ &nbsp; $\lambda$ is called a **Lagrange multiplier**")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # proof: Lagrange multipliers
    lk.proof(
        [
            r"""
            Given $\vec{a} \in g^{-1}(c)$ with $\vec{\nabla} g(\vec{a}) \neq \vec{0}$, we can

            find a parameterization $\gamma(t)$ of $g^{-1}(c)$ near $\vec{a}$ such that $\gamma(0) = \vec{a}$ and $\gamma'(0) \neq \vec{0}$
            """,
            lk.aside(r"> $\leadsto$ &nbsp; exists because $\vec{\nabla} g(\vec{a}) \neq \vec{0}$", "big theorem we cannot prove!"),
            lk.gap(),
            r"""
            evaluate both $f$ and $g$ along $\gamma(t)$ and differentiate at $t = 0$

            > • &nbsp; $\vec{a}$ is max of $f$ restricted to $g^{-1}(c)$

            > > $\Longrightarrow$ &nbsp; $0$ is max of $f \circ \gamma$

            > > $\Longrightarrow$ &nbsp; $\left. \dfrac{d}{dt} \right|_{t = 0} f(\gamma(t)) = \vec{\nabla} f(\vec{a}) \cdot \gamma'(0) = 0$

            > • &nbsp; $\gamma$ is parameterization of $g^{-1}(c)$

            > > $\Longrightarrow$ &nbsp; $g \circ \gamma = c$ is constant

            > > $\Longrightarrow$ &nbsp; $\left. \dfrac{d}{dt} \right|_{t = 0} g(\gamma(t)) = \vec{\nabla} g(\vec{a}) \cdot \gamma'(0) = 0$
            """,
            lk.gap(),
            r"""
            $\vec{\nabla} f(\vec{a})$ and $\vec{\nabla} g(\vec{a})$ orthogonal to $\gamma'(0) \neq \vec{0}$ in $\mathbb{R}^2$

            > $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a})$ and $\vec{\nabla} g(\vec{a})$ must be proportional!

            > $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a}) = \lambda \vec{\nabla} g(\vec{a})$ for some $\lambda \in \mathbb{R}$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(kc, lk, math, np):
    # module: lagrange
    # figure scene: graph of f over a disc, the ellipse g^{-1}(3) in the plane and lifted onto the graph, the plane y = k
    # (edge only) and its cut, the circle f = k
    _c = round(kc.value, 10)
    _th = np.linspace(0, 2 * np.pi, 361)
    _u, _v = math.sqrt(6) * np.cos(_th), math.sqrt(2) * np.sin(_th)
    _e1, _e2 = (_u + _v) / math.sqrt(2), (-_u + _v) / math.sqrt(2)

    def _f(x1, x2):
        return x1**2 + x2**2

    _R = 2.7  # holds the circle f = k up to k = 7
    _rr, _pp = np.meshgrid(np.linspace(0, _R, 15), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _ring = (_R * np.cos(_th), _R * np.sin(_th))
    _sq = [(-_R, -_R, _c), (_R, -_R, _c), (_R, _R, _c), (-_R, _R, _c)]
    _top = (-math.sqrt(3), math.sqrt(3), 6.0)
    lk.turntable(
        45,
        25,
        "graph of f over a disc, the ellipse g^{-1}(3) in the plane and lifted onto the graph, and the plane y = k cutting the graph along the circle f = k",
        [
            lk.panel(
                0.4,
                surfaces=[lk.sheet(_rr * np.cos(_pp), _rr * np.sin(_pp), _f(_rr * np.cos(_pp), _rr * np.sin(_pp)), wire=[(0, 2, lk.BLUE, 0.4), (1, 8, lk.BLUE, 0.4)], alpha=0.85)],
                lines=[(_ring[0], _ring[1], _f(*_ring), lk.BLUE, 1.0), (_e1, _e2, 0 * _e1, lk.BLUE, 1.0, [4, 3]), (_e1, _e2, _f(_e1, _e2), lk.BLUE, 2.4),
                       (math.sqrt(_c) * np.cos(_th), math.sqrt(_c) * np.sin(_th), _c + 0 * _th, lk.RED, 2.4)]
                + [(np.linspace(_a[0], _b[0], 60), np.linspace(_a[1], _b[1], 60), np.full(60, _c), lk.GREY, 1.2) for _a, _b in zip(_sq, _sq[1:] + _sq[:1])],
                axes=[((0, 0, 0), (3.3, 0, 0), "x^1", -90), ((0, 0, 0), (0, 3.3, 0), "x^2", -90), ((0, 0, 0), (0, 0, 11.0), "y", 90)],
                texts=[
                    (_top, r"\begin{matrix} \text{graph of } f \\ \text{restricted} \\ \text{to } g^{-1}(3) \end{matrix}", lk.BLUE, 0, 75),
                    ((1, 1, 0), r"g^{-1}(3)", lk.BLUE, -90, 6),
                    (_sq[1], r"y = k", lk.GREY, 180, 6),
                ],
                box=((-3.6, _R), (-_R, 3.6), (0, 11.0)),
            )
        ],
        height=lk.H3D,
        width=500,
        key="L16-c",
        apart=True,
        zoom=1.35,
    )
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, kc, lk, math, mo, np, tip_label):
    # module: lagrange
    # example: f = |x|^2 on the ellipse g = 3
    # the circle f = k (radius sqrt k) with g^{-1}(3); at k = 2 and k = 6 it touches the ellipse, and then the
    # gradients there are drawn (all at the same scale K)
    _c = round(kc.value, 10)
    _K = 0.25
    _r3 = math.sqrt(3)
    _th = np.linspace(0, 2 * np.pi, 361)
    _fig = Figure(figsize=(lk.HALF + 0.6, 3.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-4.9, 4.3)
    _ax.set_ylim(-3.55, 3.6)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-3.0, 3.4), (-2.9, 3.0), "$x^1$", "$x^2$")
    # the ellipse (x^1)^2 + x^1 x^2 + (x^2)^2 = 3: half axes sqrt(6) along (1, -1) and sqrt(2) along (1, 1)
    _u, _v = math.sqrt(6) * np.cos(_th), math.sqrt(2) * np.sin(_th)
    _ax.plot((_u + _v) / math.sqrt(2), (-_u + _v) / math.sqrt(2), color=lk.BLUE, lw=1.6, zorder=3)
    _ax.plot(math.sqrt(_c) * np.cos(_th), math.sqrt(_c) * np.sin(_th), color=lk.RED, lw=1.2, zorder=2)
    _ax.text(-1.75, 2.75, r"$g^{-1}(3)$", ha="center", va="center", color=lk.BLUE, fontsize=12)
    _w = math.radians(63)
    _ax.text((math.sqrt(_c) + 1.0) * math.cos(_w), (math.sqrt(_c) + 1.0) * math.sin(_w), r"$f(\vec{x}) = k$", ha="center", va="center", color=lk.RED, fontsize=12)

    def _out(p, k):
        return (p[0] + k * p[0], p[1] + k * p[1])

    # grad f = 2x, grad g = (2x^1 + x^2, 2x^2 + x^1): at k = 6 grad g = x (lambda = 2), at k = 2 grad g = 3x / 2 (lambda = 2/3)
    _v3 = r"\sqrt{3}"
    if _c == 6:
        _P, _Q = (_r3, -_r3), (-_r3, _r3)
        for _p in (_P, _Q):
            lk.arrow(_ax, _p, _out(_p, 2 * _K), lk.RED, lw=1.4)
        for _p in (_P, _Q):
            lk.arrow(_ax, _p, _out(_p, _K), lk.BLUE, lw=1.4)
            _ax.plot(*_p, "o", color=lk.RED, ms=5, zorder=5)
        tip_label(_ax, _out(_Q, 2 * _K), 180, rf"$\vec{{\nabla}} f\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{-{_v3}}}{{{_v3}}}\right)$", lk.RED, r=3, fontsize=12)
        _ax.text(-2.6, 1.45, rf"$\vec{{\nabla}} g\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{-{_v3}}}{{{_v3}}}\right)$", color=lk.BLUE, fontsize=12, ha="right", va="top")
        tip_label(_ax, _out(_P, 2 * _K), -90, rf"$\vec{{\nabla}} f\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{{_v3}}}{{-{_v3}}}\right)$", lk.RED, r=9, fontsize=12)
        tip_label(_ax, _out(_P, _K), 30, rf"$\vec{{\nabla}} g\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{{_v3}}}{{-{_v3}}}\right)$", lk.BLUE, r=5, fontsize=12)
    elif _c == 2:
        _A, _B = (1.0, 1.0), (-1.0, -1.0)
        for _p in (_A, _B):
            lk.arrow(_ax, _p, _out(_p, 3 * _K), lk.BLUE, lw=1.4)
        for _p in (_A, _B):
            lk.arrow(_ax, _p, _out(_p, 2 * _K), lk.RED, lw=1.4)
            _ax.plot(*_p, "o", color=lk.RED, ms=5, zorder=5)
        tip_label(_ax, _out(_A, 2 * _K), -30, r"$\vec{\nabla} f\left(\genfrac{[}{]}{0}{0}{1}{1}\right)$", lk.RED, r=4, fontsize=12)
        tip_label(_ax, _out(_A, 3 * _K), 30, r"$\vec{\nabla} g\left(\genfrac{[}{]}{0}{0}{1}{1}\right)$", lk.BLUE, r=8, fontsize=12)
        tip_label(_ax, _out(_B, 2 * _K), 150, r"$\vec{\nabla} f\left(\genfrac{[}{]}{0}{0}{-1}{-1}\right)$", lk.RED, r=4, fontsize=12)
        tip_label(_ax, _out(_B, 3 * _K), -90, r"$\vec{\nabla} g\left(\genfrac{[}{]}{0}{0}{-1}{-1}\right)$", lk.BLUE, r=4, fontsize=12)
    lk.example(
        [
            r"""
            $f(\vec{x}) = (x^1)^2 + (x^2)^2$<br>
            $g(\vec{x}) = (x^1)^2 + x^1 x^2 + (x^2)^2 = 3$

            > $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 \\ 2x^2 \end{bmatrix}$, &nbsp; $\vec{\nabla} g(\vec{x}) = \begin{bmatrix} 2x^1 + x^2 \\ 2x^2 + x^1 \end{bmatrix}$

            > > $\vec{\nabla} g(\vec{x}) \neq \vec{0}$ &nbsp; $\forall \, \vec{x} \neq \vec{0} \notin g^{-1}(3)$
            """,
            lk.interactive(mo.Html('<div class="lk-pair">' f'<div>{mo.as_html(_fig).text}</div><div class="lk-pair-3d">{lk.frame("L16-c", lk.H3D, width=500).text}</div></div>'), controls=[kc]),
            r"""
            $$
            \begin{aligned}
            \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\[4pt] g(\vec{x}) = 3 \end{cases} \quad & \Longleftrightarrow \quad \begin{cases} 2x^1 = \lambda (2x^1 + x^2) \\ 2x^2 = \lambda (2x^2 + x^1) \\ (x^1)^2 + x^1 x^2 + (x^2)^2 = 3 \end{cases}\\[14pt]
            & \Longleftrightarrow \quad \begin{cases} (2 - \lambda)(x^1 - x^2) = 0 \\ (2 - 3\lambda)(x^1 + x^2) = 0 \\ (x^1)^2 + x^1 x^2 + (x^2)^2 = 3 \end{cases}\\[14pt]
            & \Longleftrightarrow \quad \begin{cases} \lambda = 2, \quad x^2 = -x^1, \quad (x^1)^2 = 3 \\[4pt] \lambda = {\large\tfrac{2}{3}}, \quad x^2 = x^1, \quad 3(x^1)^2 = 3 \end{cases}
            \end{aligned}
            $$
            """,
        ],
        label="ex-ellipse",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lagrange
    # prose: new strategy
    lk.prose(
        r"New strategy if $\mathrm{Bd}(D) = g^{-1}(c)$",
        r"""
        > 2$'$. &nbsp; $\leadsto$ &nbsp; constrained extrema

        > <span class="lk-ghost">2$'$. &nbsp; $\leadsto$ &nbsp;</span>$\Longrightarrow$ &nbsp; $\vec{x} \in \mathrm{Bd}(D)$ such that $\begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\ g(\vec{x}) = c \end{cases}$

        > <span class="lk-ghost">2$'$. &nbsp; $\leadsto$ &nbsp; $\Longrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; solve for $\vec{x}$ and $\lambda$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: corners
    # remark: several components
    lk.remark(r"If $\mathrm{Bd}(D)$ has multiple components, use one constraint per component and include the corners!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: corners
    # example: the first example again, with two constraints
    lk.example(
        [
            r"""
            $f(\vec{x}) = x^2 (x^1 - 2)$, &nbsp; $D = \left\{ (x^1)^2 \leqslant x^2 \leqslant 1 \right\}$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\mathrm{Bd}(D) = \Big\{ \mk{g(\vec{x})} = 0, \ 0 \leqslant x^2 \leqslant 1 \Big\} \cup \Big\{ \mk{h(\vec{x})} = 1, \ -1 \leqslant x^1 \leqslant 1 \Big\}$",
                r"with $g(\vec{x}) = (x^1)^2 - x^2$<br>and $h(\vec{x}) = x^2$",
            ),
            r"""
            > $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} x^2 \\ x^1 - 2 \end{bmatrix}$, &nbsp; $\vec{\nabla} g(\vec{x}) = \begin{bmatrix} 2x^1 \\ -1 \end{bmatrix}$, &nbsp; $\vec{\nabla} h(\vec{x}) = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

            $$
            \begin{aligned}
            \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\[4pt] g(\vec{x}) = 0 \end{cases} \quad & \Longleftrightarrow \quad \begin{cases} x^2 = 2 \lambda x^1 \\ x^1 - 2 = -\lambda \\ (x^1)^2 - x^2 = 0 \end{cases}\\[14pt]
            & \Longleftrightarrow \quad \lambda = 2, \ x^1 = 0, \ x^2 = 0\\[4pt]
            & \phantom{\Longleftrightarrow} \quad \text{or } \lambda = {\large\tfrac{2}{3}}, \ \underbrace{x^1 = {\large\tfrac{4}{3}}, \ x^2 = {\large\tfrac{16}{9}}}_{\footnotesize \text{not on } \mathrm{Bd}(D)}
            \end{aligned}
            $$
            """,
            lk.aside(
                r"""
                $$
                \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} h(\vec{x}) \\[4pt] h(\vec{x}) = 1 \end{cases} \quad \Longleftrightarrow \quad \begin{cases} x^2 = 0 \\ x^1 - 2 = \lambda \\ x^2 = 1 \end{cases}
                $$
                """,
                "no solution!",
            ),
        ],
        label="ex-two-constraints",
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
    # exercise: Lagrange multipliers on an ellipse
    lk.exercise(
        r"""
        $f(\vec{x}) = x^1 + x^2$, &nbsp; $g(\vec{x}) = (x^1)^2 + 4(x^2)^2 = 20$

        a) find all solutions of

        $$
        \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\ g(\vec{x}) = 20 \end{cases}
        $$

        b) find the global max / min of $f$ restricted to $g^{-1}(20)$.
        """,
        label="ex-practice",
    )
    return


if __name__ == "__main__":
    app.run()
