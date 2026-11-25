import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 14 · Local extrema and the second derivative test", css_file="lecturekit/style.css")


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
    lk.lecture(14, "Local extrema and the second derivative test")
    return


@app.cell(hide_code=True)
def _(lk):
    # Helpers of this lecture: bare coordinate axes

    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr."""
        lk.arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        lk.arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    theta = lk.slider(0, 180, step=5, value=30, label=r"$\theta$")
    level = lk.slider(-1.2, 0.8, step=0.1, value=-0.5, label="$c$")
    return level, theta


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"Higher derivatives of $f : \mathbb{R}^n \longrightarrow \mathbb{R}$",
        lk.gap(),
        lk.aside(
            r"If $f$ is <span class='lk-mark'>$C^2$-smooth at $\vec{x} = \vec{a}$</span>",
            r"continuous 2nd order partial<br>derivatives at $\vec{a}$",
        ),
        lk.aside(
            r"""
            $$
            \Longrightarrow \quad f(\vec{x}) = \underbrace{f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2} (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}_{\text{good quadratic approximation}} + \mk{o\big( \lVert \vec{x} - \vec{a} \rVert^2 \big)}
            $$
            """,
            r"error goes to zero<br>faster than $\lVert \vec{x} - \vec{a} \rVert^2$",
        ),
        r"where",
        lk.aside(
            r"""
            $$
            \begin{aligned}
            Df(\vec{a}) &= \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) & \cdots & {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)\\[8pt]
            Hf(\vec{a}) &= \begin{bmatrix} {\large\tfrac{\partial^2 f}{\partial x^1 \partial x^1}}(\vec{a}) & \cdots & {\large\tfrac{\partial^2 f}{\partial x^1 \partial x^n}}(\vec{a})\\ \vdots & \ddots & \vdots\\ {\large\tfrac{\partial^2 f}{\partial x^n \partial x^1}}(\vec{a}) & \cdots & {\large\tfrac{\partial^2 f}{\partial x^n \partial x^n}}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(n \times n)
            \end{aligned}
            $$
            """,
            [(1, "derivative matrix"), (2.6, "Hessian matrix")],
            rows=3,
        ),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.aside(
            r"Application to <span class='lk-mark'>optimization</span>",
            "finding maximal / minimal values<br>of scalar valued functions",
        ),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 3.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # section
    lk.section("Local extrema")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # definition: local maximum and minimum
    lk.definition(
        [
            r"""
            Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$, a point $\vec{a} \in \mathbb{R}^n$ is

            > • &nbsp; a **local maximum** of $f$ if there is some open ball $B(\vec{a}, \delta)$ centered at $\vec{a}$ such that
            """,
            lk.aside(
                r"$$ \mk{f(\vec{x}) \leq f(\vec{a})} \quad \forall \, \vec{x} \in B(\vec{a}, \delta) $$",
                r"the value of $f$ at $\vec{a}$ is the<br>largest value nearby $\vec{x} = \vec{a}$",
            ),
            r"""
            > • &nbsp; a **local minimum** of $f$ if there is some open ball $B(\vec{a}, \delta)$ centered at $\vec{a}$ such that

            $$
            f(\vec{x}) \geq f(\vec{a}) \quad \forall \, \vec{x} \in B(\vec{a}, \delta)
            $$
            """,
        ],
        label="def-local-extrema",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # theorem: gradient at a local extremum
    lk.theorem(
        [
            lk.aside(
                r"If $f$ is differentiable at $\vec{a}$ and $\vec{a}$ is <span class='lk-mark'>a local maximum or a local minimum of $f$</span>",
                r"a local extremum of $f$",
            ),
            lk.aside(
                r"then $\mk{\vec{\nabla} f(\vec{a}) = \vec{0}} \in \mathbb{R}^n$",
                r"equivalently, $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$<br>is the zero matrix",
            ),
        ],
        label="thm-critical",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: local extrema
    # figure scene: f near its local maximum at a (larger values further along e_1), with its restrictions to the lines
    # a + t e_1 and a + t e_2
    _a = (1.4, 1.3)

    def _f(x1, x2):
        u, w = x1 - _a[0], x2 - _a[1]
        return 0.2 + 1.3 * np.exp(-(u**2 + 1.6 * w**2)) + 1.8 * np.exp(-2 * ((u - 2.3) ** 2 + w**2))

    _fa = float(_f(*_a))
    _u1, _u2 = np.meshgrid(np.linspace(_a[0] - 1.3, _a[0] + 3.2, 91), np.linspace(_a[1] - 1.2, _a[1] + 1.2, 49), indexing="ij")
    _t1, _t2 = np.linspace(-1.3, 3.2, 181), np.linspace(-1.2, 1.2, 97)
    _k = np.array([-0.9, 0.9])
    lk.turntable(
        28,
        24,
        "graph of f near its local maximum at a, with the restrictions of f to the lines through a in the directions e1 and e2",
        [
            lk.panel(
                0.8,
                surfaces=[lk.sheet(_u1, _u2, _f(_u1, _u2), wire=[(0, 5, lk.BLUE, 0.5), (1, 6, lk.BLUE, 0.5)])],
                lines=[
                    (_a[0] + _t1, _a[1] + 0 * _t1, _f(_a[0] + _t1, _a[1]), lk.BLUE, 2.4),
                    (_a[0] + 0 * _t2, _a[1] + _t2, _f(_a[0], _a[1] + _t2), lk.RED, 2.4),
                    (_a[0] + _t1, _a[1] + 0 * _t1, 0 * _t1, lk.BLUE, 1.0, [4, 3]),
                    (_a[0] + 0 * _t2, _a[1] + _t2, 0 * _t2, lk.RED, 1.0, [4, 3]),
                    (_a[0] + _k, _a[1] + 0 * _k, _fa + 0 * _k, lk.GREEN, 2.2),
                    (_a[0] + 0 * _k, _a[1] + _k, _fa + 0 * _k, lk.GREEN, 2.2),
                ],
                points=[((_a[0], _a[1], _fa), "#000000")],
                axes=[((0, 0, 0), (5.0, 0, 0), "x^1", -150), ((0, 0, 0), (0, 2.9, 0), "x^2", -20), ((0, 0, 0), (0, 0, 2.5), "y", 90)],
                texts=[
                    ((_a[0] + 2.3, _a[1], _f(_a[0] + 2.3, _a[1])), r"y = f(\vec{a} + t\vec{e}_1)", lk.BLUE, 150, 6),
                    ((_a[0], _a[1] + 0.35, _f(_a[0], _a[1] + 0.35)), r"y = f(\vec{a} + t\vec{e}_2)", lk.RED, 45, 45),
                    ((_a[0] + _t1[-1], _a[1], 0), r"\vec{a} + t\vec{e}_1", lk.BLUE, -60, 6),
                    ((_a[0], _a[1] + _t2[-1], 0), r"\vec{a} + t\vec{e}_2", lk.RED, -20, 6),
                ],
            )
        ],
        height=lk.H3D,
        width=520,
        key="L14-max",
        apart=True,
        zoom=1.3,
    )
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, lk, np):
    # module: local extrema
    # proof: gradient at a local extremum
    # y = g(t) with its local maximum at t = 0 and the line y = g(0) touching it there
    _fig = Figure(figsize=(2.6, 1.7), layout="constrained")
    _ax = _fig.add_axes((0, 0, 1, 1))
    _ax.set_xlim(-1.3, 2.4)
    _ax.set_ylim(-0.5, 1.9)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-1.25, 2.3), (-0.45, 1.85), "$t$")
    _t = np.linspace(-1.2, 2.2, 300)
    _g = 1.25 * np.exp(-2.2 * _t**2) + 0.9 * np.exp(-2.5 * (_t - 1.7) ** 2) - 0.25 + 0.15 * _t
    _ax.plot(_t, _g, color=lk.GREEN, lw=1.6)
    _g0 = 1.25 * np.exp(0) + 0.9 * np.exp(-2.5 * 1.7**2) - 0.25
    _ax.plot([-0.55, 0.55], [_g0, _g0], color=lk.RED, lw=1.4)
    _ax.plot(0, _g0, "o", color="black", ms=3.5, zorder=5)
    _ax.text(2.2, 0.42, "$y = g(t)$", color=lk.GREEN, fontsize=12, ha="right", va="top")
    _ax.text(0.6, _g0, "$y = g(0)$", color=lk.RED, fontsize=12, ha="left", va="center")
    lk.proof(
        [
            r"""
            Let's assume $\vec{a}$ is a local maximum of $f$

            Consider $g : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $t \longmapsto g(t) = f(\vec{a} + t\vec{e}_1)$

            Since $\vec{x} = \vec{a}$ is local maximum of $f$, $t = 0$ is local maximum of $g$

            > $f(\vec{a}) \geq f(\vec{x}) \quad \forall \, \vec{x} \in B(\vec{a}, \delta)$

            > > $\Longrightarrow$ &nbsp; $g(0) = f(\vec{a}) \geq g(t) = f(\vec{a} + t\vec{e}_1) \quad \forall \, t \in (-\delta, \delta)$
            """,
            lk.figure(lk.frame("L14-max", lk.H3D, width=520)),
            r"""
            Since $f$ is differentiable at $\vec{x} = \vec{a}$, $g$ is differentiable at $t = 0$

            > $$
            > g'(0) = \lim_{t \to 0} \frac{g(t) - g(0)}{t} = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{e}_1) - f(\vec{a})}{t} = \frac{\partial f}{\partial x^1}(\vec{a})
            > $$
            """,
            lk.side(
                r"""
                From single variable calculus

                > $\Longrightarrow$ &nbsp; $\displaystyle g'(0) = \frac{\partial f}{\partial x^1}(\vec{a}) = 0$
                """,
                _fig,
            ),
            r"""
            Repeat with $g(t) = f(\vec{a} + t\vec{e}_i)$ for each $i = 1, \dots, n$

            > $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a}) = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) \\ \vdots \\ {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 0 \\ \vdots \\ 0 \end{bmatrix} = \vec{0}$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # definition: critical point
    lk.definition(
        r"A point $\vec{a} \in \mathbb{R}^n$ such that $\vec{\nabla} f(\vec{a}) = \vec{0}$ is called a **critical point** of $f$",
        label="def-critical",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # remark: critical points and local extrema
    lk.remark(
        r"""
        Local extremum where $f$ is differentiable

        > $\Longrightarrow$ &nbsp; critical point!

        Critical point &nbsp; $\not\Longrightarrow$ &nbsp; local extremum!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: local extrema
    # definition: saddle point
    lk.definition(
        r"A critical point of $f$ that is not a local extremum is called a **saddle point**",
        label="def-saddle",
    )
    return


@app.cell(hide_code=True)
def _(lk, math, np, theta):
    # module: local extrema
    # figure scene: graph(f), a horse saddle, with its sections along e_1, e_2 and u = (cos theta, sin theta)
    _th = math.radians(theta.value)
    _u = (round(math.cos(_th), 12) + 0.0, round(math.sin(_th), 12) + 0.0)
    _c = round(-math.cos(2 * _th), 12) + 0.0  # f(t u) = c t^2

    def _f(x1, x2):
        return -(x1**2) + x2**2

    _R = 1.0
    _g1, _g2 = np.meshgrid(np.linspace(-_R, _R, 41), np.linspace(-_R, _R, 41), indexing="ij")
    _t = np.linspace(-_R, _R, 161)
    _s = np.linspace(-1, 1, 161) * _R / max(abs(_u[0]), abs(_u[1]))
    _edges = [(_t, _k + 0 * _t, _f(_t, _k), lk.BLUE, 1.2) for _k in (-_R, _R)] + [(_k + 0 * _t, _t, _f(_k, _t), lk.BLUE, 1.2) for _k in (-_R, _R)]
    lk.turntable(
        35,
        28,
        "graph of f, a horse saddle, with its sections along e1, e2 and u",
        [
            lk.panel(
                0.55,
                surfaces=[lk.sheet(_g1, _g2, _f(_g1, _g2), wire=[(0, 5, lk.BLUE, 0.5), (1, 5, lk.BLUE, 0.5)])],
                lines=_edges + [(_t, 0 * _t, _f(_t, 0), lk.GREEN, 1.6), (0 * _t, _t, _f(0, _t), lk.ORANGE, 1.6), (_s * _u[0], _s * _u[1], _c * _s**2, lk.RED, 2.4)],
                points=[((0, 0, 0), "#000000")],
                axes=[((0, 0, 0), (1.7, 0, 0), "x^1", -90), ((0, 0, 0), (0, 1.7, 0), "x^2", -60), ((0, 0, 0), (0, 0, 1.4), "y", 90)],
                texts=[
                    ((_R, 0, _f(_R, 0)), r"y = f\left( \begin{bmatrix} t \\ 0 \end{bmatrix} \right)", lk.GREEN, -150, 10),
                    ((0, -_R, _f(0, -_R)), r"y = f\left( \begin{bmatrix} 0 \\ s \end{bmatrix} \right)", lk.ORANGE, 100, 6),
                    ((_s[-1] * _u[0], _s[-1] * _u[1], _c * _s[-1] ** 2), r"y = f(t\vec{u})", lk.RED, 0, 8),
                    ((0, 0, 0), r"\vec{0}", "#000000", 60, 25),
                ],
                box=((-1, 1.7), (-1, 1.7), (-1, 1.4)),
            )
        ],
        height=lk.H3D,
        width=520,
        key="L14-saddle",
        apart=True,
        zoom=1.2,
    )
    return


@app.cell(hide_code=True)
def _(lk, theta):
    # module: local extrema
    # example: a saddle point
    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = -(x^1)^2 + (x^2)^2$

            > $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} -2x^1 \\ 2x^2 \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{x} = \vec{0}$ is a critical point!

            > $f(\vec{0}) = -0^2 + 0^2 = 0$, but

            > > <span class="lk-tab" style="--lk-tab: 23em">$f(\vec{x}) = -t^2 < 0$ for $\vec{x} = t\vec{e}_1 = \begin{bmatrix} t \\ 0 \end{bmatrix}$, with $t \neq 0$</span>$\leadsto$ &nbsp; $\vec{0}$ not min!

            > and

            > > <span class="lk-tab" style="--lk-tab: 23em">$f(\vec{x}) = s^2 > 0$ for $\vec{x} = s\vec{e}_2 = \begin{bmatrix} 0 \\ s \end{bmatrix}$, with $s \neq 0$</span>$\leadsto$ &nbsp; $\vec{0}$ not max!
            """,
            lk.aside(lk.interactive(lk.frame("L14-saddle", lk.H3D, width=520), controls=[theta]), "looks like a horse saddle"),
        ],
        label="ex-saddle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: second derivative test
    # section
    lk.section("Second derivative test")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: second derivative test
    # prose: the Hessian matrix decides
    lk.prose(
        r"Given a critical point, how do we distinguish its type (local max, local min, saddle)?",
        r"> $\leadsto$ &nbsp; look at the Hessian matrix!",
        lk.aside(
            r"> $\leadsto$ &nbsp; if $\vec{a}$ is <span class='lk-mark'>critical point</span> of $f$",
            r"$Df(\vec{a}) = 0 \in \mathrm{Mat}(1 \times n)$",
        ),
        lk.aside(
            r"""
            $$
            f(\vec{x}) \mathrel{\mk{\approx}} f(\vec{a}) + \underbrace{\frac{1}{2} (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}_{\begin{array}{c} \text{determines the behavior} \\ \text{of } f \text{ near } \vec{x} = \vec{a} \end{array}}
            $$
            """,
            r"$\approx$ near $\vec{x} = \vec{a}$",
        ),
    )
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, lk, np):
    # module: second derivative test
    # recall: one variable
    # the three cases, one panel each, with a critical point at a
    _a = 1.3
    _cases = (
        (r"$f''(a) < 0$", lambda x: 0.75 + 0.55 * np.cos(1.5 * (x - _a)), -0.55 * 1.5**2),
        (r"$f''(a) > 0$", lambda x: 1.25 - 0.55 * np.cos(1.5 * (x - _a)), 0.55 * 1.5**2),
        (r"$f''(a) = 0$", lambda x: 0.95 + 0.22 * (x - _a) ** 3, 0.0),
    )
    _fig = Figure(figsize=(lk.FULL, 2.7), layout="constrained")
    _x = np.linspace(_a - 1.45, _a + 1.45, 200)
    _w = np.linspace(_a - 1.1, _a + 1.1, 100)
    for _i, (_ax, (_name, _f, _d2)) in enumerate(zip(_fig.subplots(1, 3), _cases)):
        _ax.set_xlim(-0.35, 3.0)
        _ax.set_ylim(-0.3, 2.05)
        _ax.set_aspect("equal")
        _ax.axis("off")
        cross_axes(_ax, (-0.3, 2.95), (-0.25, 2.0), "$x$", "$y$")
        _ax.plot(_x, _f(_x), color=lk.BLUE, lw=1.6)
        if _d2 != 0:
            _ax.plot(_w, np.full_like(_w, _f(_a)), color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.plot(_w, _f(_a) + 0.5 * _d2 * (_w - _a) ** 2, color=lk.GREEN, lw=1.4)
        if _i == 0:
            _ax.text(2.3, 0.97, "$y = f(x)$", color=lk.BLUE, fontsize=11, ha="left", va="bottom")
            _ax.text(_w[0] + 0.05, _f(_a) + 0.06, "$y = f(a)$", color="#6b6b6b", fontsize=11, ha="left", va="bottom")
            _ax.text(1.4, 0.5, r"$y = f(a) + \frac{1}{2} f''(a)(x - a)^2$", color=lk.GREEN, fontsize=11, ha="center", va="top")
        _ax.plot(_a, _f(_a), "o", color="black", ms=4, zorder=5)
        _ax.plot([_a, _a], [-0.05, 0.05], color="black", lw=0.9)
        _ax.text(_a, -0.1, "$a$", ha="center", va="top", fontsize=12)
        _ax.set_title(_name, fontsize=13, y=-0.16)
    lk.recall(
        [
            r"""
            $f : \mathbb{R} \longrightarrow \mathbb{R}$ $C^2$-smooth with $f'(a) = 0$

            > • &nbsp; <span class="lk-tab" style="--lk-tab: 6.5em">$f''(a) < 0$</span>$\Longrightarrow$ &nbsp; local maximum

            > • &nbsp; <span class="lk-tab" style="--lk-tab: 6.5em">$f''(a) > 0$</span>$\Longrightarrow$ &nbsp; local minimum

            > • &nbsp; <span class="lk-tab" style="--lk-tab: 6.5em">$f''(a) = 0$</span>$\Longrightarrow$ &nbsp; need more information

            because near $x = a$
            """,
            lk.aside(
                r"$$ f(x) = f(a) + f'(a)(x - a) + \frac{1}{2} f''(a)(x - a)^2 + \mk{o\big( (x - a)^2 \big)} $$",
                r"error goes to zero<br>faster than $(x - a)^2$",
            ),
            r"""
            and if $a$ is critical point

            > $\Longrightarrow$ &nbsp; $\displaystyle f(x) \approx f(a) + \frac{1}{2} f''(a)(x - a)^2$

            > > • &nbsp; if $f''(a) < 0$ &nbsp; $\leadsto$ &nbsp; parabola opens downwards

            > > > $\Longrightarrow$ &nbsp; $a$ is local max

            > > • &nbsp; if $f''(a) > 0$ &nbsp; $\leadsto$ &nbsp; parabola opens upwards

            > > > $\Longrightarrow$ &nbsp; $a$ is local min

            > > • &nbsp; if $f''(a) = 0$ &nbsp; $\leadsto$ &nbsp; parabola degenerates to a horizontal line …

            > > > $\Longrightarrow$ &nbsp; not sufficient info
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: second derivative test
    # prose: towards two variables
    lk.prose(
        r"""
        $\leadsto$ &nbsp; we will generalize this for $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$

        $\leadsto$ &nbsp; for $n > 2$ we need tools from Linear Algebra
        """
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: second derivative test
    # figure: graph(q) near a in the four cases, with the point (a, f(a)): over a disc, or over a square
    _a = (1.0, 1.8)
    _cases = (
        ("negative definite", -2.4, 0.5, -2.0, 2.2, False),
        ("positive definite", 2.4, 0.5, 2.0, 0.4, False),
        ("indefinite", -1.4, 0.3, 1.8, 1.2, True),
        ("degenerate", 1.6, 0.0, 0.0, 0.7, True),
    )
    _w = np.linspace(-1, 1, 121)
    _s = np.linspace(0, 1, 40)
    _phi = np.linspace(0, 2 * np.pi, 241)
    _panels = []
    for _name, _A, _B, _D, _fa, _square in _cases:

        def _q(x1, x2, A=_A, B=_B, D=_D, fa=_fa):
            v1, v2 = x1 - _a[0], x2 - _a[1]
            return fa + 0.5 * (A * v1**2 + 2 * B * v1 * v2 + D * v2**2)

        if _square:
            _x1, _x2 = np.meshgrid(_a[0] + 0.85 * np.linspace(-1, 1, 35), _a[1] + 0.85 * np.linspace(-1, 1, 35), indexing="ij")
            _wire = [(0, 5, lk.BLUE, 0.5), (1, 5, lk.BLUE, 0.5)]
            _rim = [(_a[0] + 0.85 * _k + 0 * _w, _a[1] + 0.85 * _w) for _k in (-1, 1)] + [(_a[0] + 0.85 * _w, _a[1] + 0.85 * _k + 0 * _w) for _k in (-1, 1)]
        else:
            _r, _p = np.meshgrid(np.linspace(0, 1, 13), np.linspace(0, 2 * np.pi, 73), indexing="ij")
            _x1, _x2 = _a[0] + _r * np.cos(_p), _a[1] + _r * np.sin(_p)
            _wire = [(0, 4, lk.BLUE, 0.5), (1, 6, lk.BLUE, 0.5)]
            _rim = [(_a[0] + np.cos(_phi), _a[1] + np.sin(_phi))]
        _rr, _bk = (0.85, 0.85) if _square else (1.0, 0.0)  # the point of the rim beside which the name of the graph goes
        _lines = [(_c1, _c2, _q(_c1, _c2), lk.BLUE, 1.2) for _c1, _c2 in _rim]
        _lines.append((_a[0] + 0 * _s, _a[1] + 0 * _s, _fa * _s, lk.GREY, 1.0, [3, 3]))
        _lines.append((_a[0] * _s, _a[1] * _s, _fa + 0 * _s, lk.GREY, 1.0, [3, 3]))  # from f(a) on the y axis to the point
        if _name == "degenerate":  # the horizontal line v^1 + (B / A) v^2 = 0 at height f(a)
            _d = np.array([-_B, _A]) / np.hypot(_A, _B)
            _lines.append((_a[0] + 0.85 * _w * _d[0], _a[1] + 0.85 * _w * _d[1], _fa + 0 * _w, lk.GREEN, 2.2))
        _panels.append(
            lk.panel(
                0.6,
                surfaces=[lk.sheet(_x1, _x2, _q(_x1, _x2), wire=_wire, alpha=0.6 if _name == "positive definite" else 1.0)],
                lines=_lines,
                points=[((_a[0], _a[1], _fa), "#000000"), ((_a[0], _a[1], 0), lk.GREY, 3.4)],
                axes=[((0, 0, 0), (2.2, 0, 0), "x^1", -150), ((0, 0, 0), (0, 3.2, 0), "x^2", -20), ((0, 0, 0), (0, 0, 2.9), "y", 90)],
                texts=[
                    ((_a[0], _a[1], 0), r"\vec{x} = \vec{a}", "#000000", -30, 6),
                    ((0, 0, _fa), r"f(\vec{a})", "#000000", 180, 6),
                    ((_a[0] - _bk, _a[1] + _rr, _q(_a[0] - _bk, _a[1] + _rr)), r"y = q(\vec{x})", lk.BLUE, 90 if _name == "degenerate" else 20 if _square else 10, 6),
                ],
                caption=rf"\text{{{_name}}}",
                box=((-0.2, 2.2), (-0.2, 3.2), (-0.2, 2.9)),
            )
        )
    _four = lk.turntable(
        28,
        24,
        "graph of q near a critical point a in the four cases: negative definite, positive definite, indefinite, degenerate",
        _panels,
        height=260,
        cols=2,
    )
    lk.prose(
        r"""
        For $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, $C^2$-smooth at a critical point $\vec{a}$

        > $\displaystyle f(\vec{x}) \approx f(\vec{a}) + \frac{1}{2} (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a}) = q(\vec{x})$
        """,
        lk.aside(
            r"Let's write $Hf(\vec{a}) = \begin{bmatrix} A & B \\ \mk{C} & D \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$, that is, let",
            r"$C = B$",
        ),
        r"""
        > $$
        > \begin{aligned}
        > A &= \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) & \qquad B &= \frac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{a})\\[6pt]
        > C &= \frac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{a}) = B & \qquad D &= \frac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{a})
        > \end{aligned}
        > $$

        $$
        \Longrightarrow \quad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} \Big( A \underbrace{(x^1 - a^1)^2}_{(v^1)^2} + 2B \underbrace{(x^1 - a^1)(x^2 - a^2)}_{v^1 v^2} + D \underbrace{(x^2 - a^2)^2}_{(v^2)^2} \Big)
        $$
        """,
        lk.gap(),
        r"""
        if $A \neq 0$ &nbsp; $\leadsto$ &nbsp; complete the square

        > $\Longrightarrow$ &nbsp; $\displaystyle q(\vec{x}) = f(\vec{a}) + \frac{1}{2} \left( A \left( v^1 + \frac{B}{A} v^2 \right)^2 + \frac{AD - B^2}{A} (v^2)^2 \right)$
        """,
        lk.aside(
            r"> • &nbsp; if <span class='lk-mark'>$A < 0$ and $AD - B^2 > 0$</span>, then $\mathrm{graph}(q)$ is a paraboloid opening downwards",
            "negative definite",
        ),
        lk.aside(
            r"> • &nbsp; if <span class='lk-mark'>$A > 0$ and $AD - B^2 > 0$</span>, then $\mathrm{graph}(q)$ is a paraboloid opening upwards",
            "positive definite",
        ),
        lk.aside(
            r"> • &nbsp; if <span class='lk-mark'>$A \neq 0$ and $AD - B^2 < 0$</span>, then $\mathrm{graph}(q)$ is a horse saddle",
            "indefinite",
        ),
        lk.aside(
            r"> • &nbsp; if $A \neq 0$ and <span class='lk-mark'>$AD - B^2 = 0$</span>",
            "degenerate",
        ),
        r"> > $\Longrightarrow$ &nbsp; $\displaystyle q(\vec{x}) = f(\vec{a}) + \frac{1}{2} A \left( v^1 + \frac{B}{A} v^2 \right)^2$",
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ contains a <span class='lk-mark'>horizontal line</span> …",
            r"$\mathrm{graph}(q)$ is degenerate",
        ),
        lk.figure(_four),
        r"""
        if $A = 0$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 7em">$B \neq 0$</span>$\Longrightarrow$ &nbsp; $\displaystyle q(\vec{x}) = f(\vec{a}) + \frac{1}{2} (2B v^1 + D v^2) v^2$

        > <span class='lk-ghost'>• &nbsp; </span><span class="lk-tab" style="--lk-tab: 7em">&nbsp;&nbsp;&nbsp;&nbsp;$\Updownarrow$</span>

        > <span class='lk-ghost'>• &nbsp; </span><span class="lk-tab" style="--lk-tab: 7em">$AD - B^2 < 0$</span>$\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ is a horse saddle

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 7em">$B = 0$</span>$\Longrightarrow$ &nbsp; $\displaystyle q(\vec{x}) = f(\vec{a}) + \frac{1}{2} D (v^2)^2$

        > <span class='lk-ghost'>• &nbsp; </span><span class="lk-tab" style="--lk-tab: 7em">&nbsp;&nbsp;&nbsp;&nbsp;$\Updownarrow$</span>

        > <span class='lk-ghost'>• &nbsp; </span><span class="lk-tab" style="--lk-tab: 7em">$AD - B^2 = 0$</span>$\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ contains a horizontal line
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: second derivative test
    # definition: definite, indefinite, degenerate
    lk.definition(
        r"""
        $H = \begin{bmatrix} A & B \\ B & D \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$ is called

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 9.5em">**negative definite**</span>if $\det H > 0$ and $A < 0$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 9.5em">**positive definite**</span>if $\det H > 0$ and $A > 0$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 9.5em">**indefinite**</span>if $\det H < 0$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 9.5em">**degenerate**</span>if $\det H = 0$
        """,
        label="def-definite",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: second derivative test
    # theorem: second derivative test
    lk.theorem(
        r"""
        $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, $C^2$-smooth at a critical point $\vec{a}$

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 15em">if $Hf(\vec{a})$ is negative definite</span>$\Longrightarrow$ &nbsp; $\vec{a}$ is local max

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 15em">if $Hf(\vec{a})$ is positive definite</span>$\Longrightarrow$ &nbsp; $\vec{a}$ is local min

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 15em">if $Hf(\vec{a})$ is indefinite</span>$\Longrightarrow$ &nbsp; $\vec{a}$ is a saddle

        > • &nbsp; <span class="lk-tab" style="--lk-tab: 15em">if $Hf(\vec{a})$ is degenerate</span>$\Longrightarrow$ &nbsp; not sufficient info …
        """,
        title="second derivative test",
        label="thm-second-derivative-test",
    )
    return


@app.cell(hide_code=True)
def _(level, lk, np):
    # module: second derivative test
    # figure scene: graph(f) over a disc around the saddle a and the local minimum b, cut by the plane y = c
    import contourpy

    def _f(x1, x2):
        return x1**3 - 3 * x1 * x2 + x2**3

    _lc = level.value
    _o, _R = (0.5, 0.5), 1.0
    _r, _p = np.meshgrid(np.linspace(0, _R, 21), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _x1, _x2 = _o[0] + _r * np.cos(_p), _o[1] + _r * np.sin(_p)
    _phi = np.linspace(0, 2 * np.pi, 241)
    _rim = (_o[0] + _R * np.cos(_phi), _o[1] + _R * np.sin(_phi))
    _top = (_o[0] + _R * np.cos(-np.pi / 4), _o[1] + _R * np.sin(-np.pi / 4))  # the highest point of the rim
    _g = np.linspace(-_R, _R, 241)
    _G1, _G2 = np.meshgrid(_o[0] + _g, _o[1] + _g)
    _pieces = []
    for _ln in contourpy.contour_generator(_G1, _G2, _f(_G1, _G2)).lines(_lc):
        _in = np.hypot(_ln[:, 0] - _o[0], _ln[:, 1] - _o[1]) <= _R
        _cut = np.flatnonzero(np.diff(_in.astype(int))) + 1
        for _seg, _keep in zip(np.split(_ln, _cut), np.split(_in, _cut)):
            if _keep[0] and len(_seg) > 1:
                _pieces.append(_seg)
    _plane = [(_o[0] - _R, _o[1] - _R, _lc), (_o[0] + _R, _o[1] - _R, _lc), (_o[0] + _R, _o[1] + _R, _lc), (_o[0] - _R, _o[1] + _R, _lc)]
    lk.turntable(
        -135,
        30,
        "graph of f over a disc around the saddle a and the local minimum b, cut by the plane y = c along the level set f = c",
        [
            lk.panel(
                0.45,
                surfaces=[lk.sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, lk.BLUE, 0.5), (1, 8, lk.BLUE, 0.5)])],
                lines=[(_rim[0], _rim[1], _f(*_rim), lk.BLUE, 1.2)]
                + [(_q[:, 0], _q[:, 1], _lc + 0 * _q[:, 0], lk.RED, 2.4) for _q in _pieces]
                + [(np.linspace(_e0[0], _e1[0], 60), np.linspace(_e0[1], _e1[1], 60), np.full(60, _lc), lk.GREY, 1.2) for _e0, _e1 in zip(_plane, _plane[1:] + _plane[:1])],
                points=[((0, 0, 0), "#000000"), ((1, 1, -1), "#000000")],
                axes=[((0, 0, 0), (2.4, 0, 0), "x^1", 90), ((0, 0, 0), (0, 2.4, 0), "x^2", 90), ((0, 0, 0), (0, 0, 2.6), "y", 90)],
                texts=[
                    ((0, 0, 0), r"\vec{a}", "#000000", -90, 8),
                    ((1, 1, -1), r"\vec{b}", "#000000", 0, 9),
                    ((_top[0], _top[1], _f(*_top)), r"y = f(\vec{x})", lk.BLUE, 0, 6),
                    (_plane[3], r"y = c", lk.GREY, 180, 6),
                ],
                box=((_o[0] - _R, _o[0] + _R + 0.1), (_o[1] - _R, _o[1] + _R + 0.1), (-1.2, 2.6)),
            )
        ],
        height=lk.H3D,
        width=520,
        key="L14-level",
        apart=True,
        zoom=1.3,
    )
    return


@app.cell(hide_code=True)
def _(level, lk):
    # module: second derivative test
    # example: a saddle and a local minimum
    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^3 - 3x^1 x^2 + (x^2)^3$

            > $\leadsto$ &nbsp; critical points: &nbsp; $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} 3(x^1)^2 - 3x^2 \\ -3x^1 + 3(x^2)^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$

            > > $\Longleftrightarrow$ &nbsp; $\begin{cases} x^2 = (x^1)^2 \\ x^1 = (x^2)^2 \end{cases}$ &nbsp; $\Longleftrightarrow$ &nbsp; $\begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \underbrace{\begin{bmatrix} 0 \\ 0 \end{bmatrix}}_{\vec{a}}$ or $\underbrace{\begin{bmatrix} 1 \\ 1 \end{bmatrix}}_{\vec{b}}$

            > $\leadsto$ &nbsp; Hessian matrix: &nbsp; $Hf(\vec{x}) = \begin{bmatrix} 6x^1 & -3 \\ -3 & 6x^2 \end{bmatrix}$
            """,
            lk.aside(
                r"at $\vec{a} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$: &nbsp; $Hf(\vec{a}) = \begin{bmatrix} 0 & -3 \\ -3 & 0 \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\mk{\det Hf(\vec{a}) = -9 < 0}$",
                "indefinite",
            ),
            r"""
            <span class='lk-ghost'>at $\vec{a} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$: &nbsp; $Hf(\vec{a}) = \begin{bmatrix} 0 & -3 \\ -3 & 0 \end{bmatrix}$ &nbsp; </span>$\Longrightarrow$ &nbsp; $\vec{a}$ is a saddle
            """,
            lk.aside(
                r"""
                at $\vec{b} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$: &nbsp; $Hf(\vec{b}) = \begin{bmatrix} 6 & -3 \\ -3 & 6 \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\mk{\det Hf(\vec{b}) = 27 > 0}$, &nbsp; $\mk{\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{b}) = 6 > 0}$
                """,
                "positive definite",
            ),
            r"""
            <span class='lk-ghost'>at $\vec{b} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$: &nbsp; $Hf(\vec{b}) = \begin{bmatrix} 6 & -3 \\ -3 & 6 \end{bmatrix}$ &nbsp; </span>$\Longrightarrow$ &nbsp; $\vec{b}$ is local min
            """,
            lk.interactive(lk.frame("L14-level", lk.H3D, width=520), controls=[level]),
        ],
        label="ex-second-derivative-test",
    )
    return


if __name__ == "__main__":
    app.run()
