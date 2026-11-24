import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 9 · Differentiability and the derivative", css_file="lecturekit/style.css")


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
    lk.lecture(9, "Differentiability and the derivative")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math):
    # Helpers of this lecture: a bare sketch, an arrow with its name

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def vector(ax, tail, tip, color, label=None, turn=0, r=15):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip; `turn` (degrees)
        rotates the label about the tip. No box behind the label."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            lk.arrow(ax, tail, tip, color)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5)

    return blank, vector


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    last_t = lk.slider(0.4, 5, step=0.05, value=3, label="$t$")
    return (last_t,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: limits of multivariable functions
    lk.recap(
        r"""
        $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\vec{a} \in \mathbb{R}^n$, $\vec{b} \in \mathbb{R}^m$

        $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$ if

        > for every $B(\vec{b}, \varepsilon) \subset \mathbb{R}^m$ we can find $B(\vec{a}, \delta) \subset \mathbb{R}^n$ such that $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$

        > $\leadsto$ &nbsp; we can make $f(\vec{x})$ as close as we want to $\vec{b}$ by taking $\vec{x}$ close enough, but different, to $\vec{a}$
        """,
        topic="Limits of multivariable functions",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Differentiability and the derivative

        > for $n = 2$, $m = 1$ &nbsp; $\leadsto$ &nbsp; scalar functions on $\mathbb{R}^2$
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.3, 2.6")
    return


@app.cell(hide_code=True)
def _(blank, last_t, lk, np, vector):
    # module: motivation
    # recall: the velocity of a path in R^2, with the difference quotient (gamma(t) - gamma(a)) / (t - a)
    # the path: three cubic pieces, two units of time each (t in [0, 6]), through the points _K with the velocities _V
    _K = np.array([(5.05, 1.45), (8.35, 2.6), (6.8, 0.6), (10.55, 1.8)])
    _V = np.array([(0.4, 4.5), (-0.6, -3.0), (4.0, 0.0), (2.0, -1.5)])

    def _gamma(t):
        _u = np.asarray(t, float) / 2
        _i = np.clip(np.floor(_u).astype(int), 0, 2)
        _u = (_u - _i)[..., None]
        _g = (2 * _u**3 - 3 * _u**2 + 1) * _K[_i] + (_u**3 - 2 * _u**2 + _u) * _V[_i] + (3 * _u**2 - 2 * _u**3) * _K[_i + 1] + (_u**3 - _u**2) * _V[_i + 1]
        return _g[..., 0], _g[..., 1]

    _fig, _ax = blank(lk.FULL, 3.0, (-0.2, 11.9), (-0.55, 4.25))
    # the time axis
    lk.arrow(_ax, (0, 1.2), (3.0, 1.2), "black", lw=0.9)
    _a, _t, _h = 0.8, last_t.value, 1e-4
    _near = abs(_t - _a) < 0.9  # t this close to a: no room for the name of gamma(t) beside gamma(a)
    _ax.plot(0.2 + 0.43 * _t, 1.2, "o", color=lk.RED, ms=4)
    _ax.plot(0.2 + 0.43 * _a, 1.2, "o", color="black", ms=4)
    _ax.text(0.2 + 0.43 * _a, 0.98, "$a$", ha="center", va="top", fontsize=13)
    if abs(_t - _a) >= 0.45:
        _ax.text(0.2 + 0.43 * _t, 0.98, "$t$", ha="center", va="top", fontsize=13)
    lk.arrow(_ax, (3.3, 1.4), (4.0, 1.4), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(3.65, 1.67, r"$\gamma$", fontsize=13, ha="center", va="bottom")
    # the plane with the image of the path
    lk.arrow(_ax, (4.2, 0), (11.5, 0), "black", lw=0.9)
    lk.arrow(_ax, (4.5, -0.3), (4.5, 3.5), "black", lw=0.9)
    _s = np.linspace(0, 6, 600)
    _ax.plot(*_gamma(_s), color=lk.BLUE, lw=1.4)
    _pa, _pt = _gamma(_a), _gamma(_t)
    _va = ((_gamma(_a + _h)[0] - _pa[0]) / _h, (_gamma(_a + _h)[1] - _pa[1]) / _h)
    if _t != _a:
        _q = ((_pt[0] - _pa[0]) / (_t - _a), (_pt[1] - _pa[1]) / (_t - _a))
        lk.arrow(_ax, _pa, (_pa[0] + _q[0], _pa[1] + _q[1]), lk.RED)
    vector(_ax, _pa, (_pa[0] + _va[0], _pa[1] + _va[1]), lk.GREEN, r"$\gamma'(a)$", 0, r=20)
    _ax.plot(*_pa, "o", color="black", ms=4, zorder=4)
    _ax.plot(*_pt, "o", color=lk.RED, ms=4, zorder=4)
    _end = _gamma(6)
    _ax.text(_end[0] + 0.15, _end[1], r"$\mathrm{Im}(\gamma)$", color=lk.BLUE, fontsize=13, ha="left", va="center")
    _ax.text(_pa[0] - 0.08, _pa[1] + 0.1, r"$\gamma(a)$", fontsize=13, ha="right", va="bottom")
    # the red arrow named once, fixed, below gamma(a) inside the arch
    _ax.text(_pa[0] + 0.17, _pa[1] - 0.92, r"$\dfrac{\gamma(t) - \gamma(a)}{t - a}$", color=lk.RED, fontsize=13, ha="center", va="top")
    if not _near:
        # gamma(t) named just past its point, away from gamma(a)
        _d = np.array((_pt[0] - _pa[0], _pt[1] - _pa[1])) / np.hypot(_pt[0] - _pa[0], _pt[1] - _pa[1])
        _ax.annotate(r"$\gamma(t)$", _pt, textcoords="offset points", xytext=(24 * _d[0], 17 * _d[1]), fontsize=13, ha="center", va="center", zorder=5)

    lk.recall(
        [
            lk.aside(r"path in $\mathbb{R}^2$", "$n = 1$, $m = 2$"),
            lk.aside(
                r"> $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$, &nbsp; $\mk{\gamma(t)} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix} \in \mathbb{R}^2$",
                r"position of $\gamma$ at time $t$",
            ),
            lk.aside(
                r"> > $\leadsto$ &nbsp; $\mk{\gamma'(a)} = \displaystyle\lim_{t \to a} \underbrace{\frac{\gamma(t) - \gamma(a)}{t - a}}_{\text{displacement per unit of time}} = \begin{bmatrix} (\gamma^1)'(a) \\ (\gamma^2)'(a) \end{bmatrix}\rule[-1.6em]{0pt}{0pt}$",
                r"velocity of $\gamma$ at time $t = a$",
            ),
            lk.interactive(_fig, controls=[last_t]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: motivation
    # motivation: why the difference quotient of one variable does not carry over
    lk.motivation(
        [
            "How do we generalize to scalar functions on $\\mathbb{R}^2$?",
            lk.aside(
                r"> $\leadsto$ &nbsp; could try $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\mk{\vec{x} - \vec{a}}}$",
                r"makes NO sense! we cannot divide<br>by $\vec{x} - \vec{a} \in \mathbb{R}^2$!",
            ),
            lk.aside(
                r"> $\leadsto$ &nbsp; could try instead $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\mk{\lVert \vec{x} - \vec{a} \rVert}}$",
                "this makes sense!",
            ),
            r"> > but if this limit exists (say equal $m \in \mathbb{R}$)",
            lk.aside(
                r"> > > $\Longrightarrow$ &nbsp; $f(\vec{x}) \approx \mk{f(\vec{a}) + m \lVert \vec{x} - \vec{a} \rVert}$ for $\vec{x} \approx \vec{a}$",
                "too restrictive!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: motivation
    # example: f = x^1 has no limit of the norm quotient
    lk.example(
        [
            lk.aside(
                r"$f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \mk{x^1}$",
                "we should hope to give a definition of derivatives<br>for which this simple function is differentiable!",
            ),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert} &= \lim_{\vec{x} \to \vec{a}} \mk{\frac{x^1 - a^1}{\lVert \vec{x} - \vec{a} \rVert}}\\[4pt]
                &= 1 \quad \text{along } \vec{x} = \vec{a} + t\vec{e}_1\\[4pt]
                &= 0 \quad \text{along } \vec{x} = \vec{a} + s\vec{e}_2
                \end{aligned}
                $$
                """,
                r"depends on how $\vec{x}$ approaches $\vec{a}$!",
                at=1,
                rows=3,
            ),
            r"> $\Longrightarrow$ &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert}$ does not exist",
        ],
        label="ex-norm-quotient",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: partial derivatives
    # section
    lk.section("Partial derivatives")
    return


@app.cell(hide_code=True)
def _(blank, lk):
    # module: partial derivatives
    # definition: partial derivatives, with the sketch of the two lines through a and their values
    _fig, _ax = blank(lk.FULL, 2.6, (-0.7, 9.0), (-0.55, 3.2))
    lk.arrow(_ax, (-0.4, 0), (4.5, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.4), (0, 3.0), "black", lw=0.9)
    _ax.text(4.5, -0.12, "$x^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.12, 3.0, "$x^2$", fontsize=13, ha="right", va="center")
    _a = (1.6, 0.9)
    lk.arrow(_ax, (0.6, _a[1]), (4.0, _a[1]), lk.BLUE)
    lk.arrow(_ax, (_a[0], 0.2), (_a[0], 2.9), lk.RED)
    _ax.text(4.1, _a[1], "$t$", color=lk.BLUE, fontsize=13, ha="left", va="center")
    _ax.text(_a[0], 2.95, "$s$", color=lk.RED, fontsize=13, ha="center", va="bottom")
    # the points and their values, coloured as the line they lie on
    for _pt, _c in ((_a, "black"), ((2.9, _a[1]), lk.BLUE), ((_a[0], 2.2), lk.RED)):
        _ax.plot(*_pt, "o", color=_c, ms=4, zorder=4)
    lk.arrow(_ax, (4.9, 2.0), (5.9, 2.0), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(5.4, 2.32, "$f$", fontsize=13, ha="center", va="bottom")
    # the real line of values
    lk.arrow(_ax, (6.6, -0.4), (6.6, 3.0), "black", lw=0.9)
    for _y, _c in ((2.2, lk.BLUE), (1.3, "black"), (0.5, lk.RED)):
        _ax.plot(6.6, _y, "o", color=_c, ms=4, zorder=4)
    _ax.text(_a[0] - 0.08, _a[1] - 0.08, r"$\vec{a}$", fontsize=13, ha="right", va="top")
    _ax.text(2.9, _a[1] + 0.1, r"$\vec{a} + t\vec{e}_1$", fontsize=13, ha="center", va="bottom")
    _ax.text(_a[0] + 0.1, 2.2, r"$\vec{a} + s\vec{e}_2$", fontsize=13, ha="left", va="center")
    for _y, _name in ((2.2, r"$f(\vec{a} + t\vec{e}_1)$"), (1.3, r"$f(\vec{a})$"), (0.5, r"$f(\vec{a} + s\vec{e}_2)$")):
        _ax.text(6.75, _y, _name, fontsize=13, ha="left", va="center")

    lk.definition(
        [
            r"""
            Given a function $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, the **partial derivative** of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ is

            $$
            \frac{\partial f}{\partial x^1}(\vec{a}) = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{e}_1) - f(\vec{a})}{t}
            $$

            provided that the limit exists
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $\dfrac{\partial f}{\partial x^1}(\vec{a}) = \mk{\dfrac{d}{dt}} f(\vec{a} + t\vec{e}_1) \Big|_{t=0}$",
                r"real single variable<br>differentiation at $t = 0$",
            ),
            lk.aside(
                r"> > $\leadsto$ &nbsp; $\mk{t \longmapsto f(\vec{a} + t\vec{e}_1)}$",
                "real single variable<br>real valued function!",
            ),
            lk.gap(),
            r"""
            Similarly, the partial derivative of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ is

            $$
            \frac{\partial f}{\partial x^2}(\vec{a}) = \lim_{s \to 0} \frac{f(\vec{a} + s\vec{e}_2) - f(\vec{a})}{s}
            $$

            provided that the limit exists

            > $\leadsto$ &nbsp; $\dfrac{\partial f}{\partial x^2}(\vec{a}) = \dfrac{d}{ds} f(\vec{a} + s\vec{e}_2) \Big|_{s=0}$
            """,
            lk.figure(_fig),
        ],
        label="def-partial",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: partial derivatives
    # example: partial derivatives of sin(x^1) and of (x^1)^2 (x^2)^3
    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \sin(x^1)$

            $$
            \begin{aligned}
            \Longrightarrow \quad \frac{\partial}{\partial x^1} f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) &= \lim_{t \to 0} \frac{f\left( \begin{bmatrix} a^1 + t \\ a^2 + 0 \end{bmatrix} \right) - f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t}\\[4pt]
            &= \lim_{t \to 0} \frac{\sin(a^1 + t) - \sin(a^1)}{t}\\[4pt]
            &= \frac{d}{dt} \sin(a^1 + t) \Big|_{t=0} = \cos(a^1)\\[12pt]
            \frac{\partial}{\partial x^2} f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) &= \lim_{s \to 0} \frac{f\left( \begin{bmatrix} a^1 + 0 \\ a^2 + s \end{bmatrix} \right) - f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{s}\\[4pt]
            &= \lim_{s \to 0} \frac{\sin(a^1) - \sin(a^1)}{s} = 0
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) = (a^1)^2 (a^2)^3$

            $$
            \begin{aligned}
            \Longrightarrow \quad \frac{\partial}{\partial x^1} f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) &= \lim_{t \to 0} \frac{(a^1 + t)^2 (a^2)^3 - (a^1)^2 (a^2)^3}{t}\\[4pt]
            &= \lim_{t \to 0} \frac{(a^1 + t)^2 - (a^1)^2}{t} \, (a^2)^3\\[4pt]
            &= \frac{d}{dt} (a^1 + t)^2 \cdot (a^2)^3 = 2(a^1) \cdot (a^2)^3\\[12pt]
            \frac{\partial}{\partial x^2} f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) &= \lim_{s \to 0} \frac{(a^1)^2 (a^2 + s)^3 - (a^1)^2 (a^2)^3}{s}\\[4pt]
            &= (a^1)^2 \cdot \frac{d}{ds} (a^2 + s)^3 \Big|_{s=0} = 3(a^1)^2 (a^2)^2
            \end{aligned}
            $$
            """,
            r"$\leadsto$ &nbsp; the partial derivative in the direction of $\vec{e}_i$ is the usual single variable derivative with respect to $x^i$, assuming "
            + lk.gloss("$x^j$", r"$j \neq i$")
            + " is held constant",
        ],
        label="ex-partials",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # section
    lk.section("Directional derivatives")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # prose: partial derivatives are not enough
    lk.prose(
        r"""
        $\leadsto$ &nbsp; the existence of partial derivatives will be necessary for the notion of differentiability but will not be sufficient

        > $\leadsto$ &nbsp; $f$ could behave badly in other directions!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # definition: directional derivative
    lk.definition(
        r"""
        Given $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, the **directional derivative** of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$ is

        $$
        \begin{aligned}
        Df(\vec{a})(\vec{v}) &= \lim_{t \to 0} \frac{f(\vec{a} + t\vec{v}) - f(\vec{a})}{t}\\[4pt]
        &= \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t=0}
        \end{aligned}
        $$

        provided the derivative exists
        """,
        label="def-directional",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # prose: what differentiability should also ask for
    lk.prose(
        r"$\leadsto$ &nbsp; to call a function $f$ differentiable at $\vec{x} = \vec{a}$ we want also that all directional derivatives for all $\vec{v} \in \mathbb{R}^2$ be well-defined and that",
        lk.aside(
            r"$$ Df(\vec{a})(\vec{v}) = \mk{v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})} $$",
            "linear combination of<br>partial derivatives",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # remark: partial derivatives are directional derivatives
    lk.remark(r"$\dfrac{\partial f}{\partial x^i}(\vec{a}) = Df(\vec{a})(\vec{e}_i)$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # section
    lk.section("Differentiability")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # definition: differentiable at a
    lk.definition(
        [
            r"""
            $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

            > if the directional derivative $Df(\vec{a})(\vec{v})$

            > exists for every $\vec{v} = v^1 \vec{e}_1 + v^2 \vec{e}_2 = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \in \mathbb{R}^2$,

            > satisfies
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                Df(\vec{a})(\vec{v}) &= Df(\vec{a})(v^1 \vec{e}_1 + v^2 \vec{e}_2)\\[4pt]
                &= v^1 Df(\vec{a})(\vec{e}_1) + v^2 Df(\vec{a})(\vec{e}_2)\\[4pt]
                &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})
                \end{aligned}
                $$
                """,
                [(1.5, r"linearity in $\vec{v}$")],
                rows=3,
            ),
            r"> and",
            lk.aside(
                r"""
                $$
                \lim_{\mk{\vec{x} \to \vec{a}}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
                $$
                """,
                "now NOT a limit over real numbers!<br>(stronger than just existence +<br>linearity of directional derivatives!)",
            ),
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $f(\vec{x}) \approx f(\vec{a}) + \mk{Df(\vec{a})(\vec{x} - \vec{a})}$ for $\vec{x} \approx \vec{a}$",
                r"more flexible than $m \lVert \vec{x} - \vec{a} \rVert$",
            ),
        ],
        label="def-differentiable",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentiability
    # example: f = x^1 is differentiable everywhere
    lk.example(
        [
            r"""
            $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$

            $$
            \begin{aligned}
            \Longrightarrow \quad Df(\vec{a})(\vec{v}) &= \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t=0}\\[4pt]
            &= \frac{d}{dt} (a^1 + t v^1) \Big|_{t=0} = v^1\\[4pt]
            &= v^1 \underbrace{\frac{\partial f}{\partial x^1}(\vec{a})}_{= \, 1} + v^2 \underbrace{\frac{\partial f}{\partial x^2}(\vec{a})}_{= \, 0} \quad \forall \, \vec{v}\\[18pt]
            \end{aligned}
            $$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 & 0 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $\begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto v^1$",
                r"linear in $\vec{v}$",
            ),
            lk.gap(),
            r"""
            For the final limit:

            $$
            \begin{aligned}
            &\frac{f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) - f\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) - Df(\vec{a})\left( \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \end{bmatrix} \right)}{\lVert \vec{x} - \vec{a} \rVert}\\[6pt]
            &\qquad = \frac{x^1 - a^1 - (x^1 - a^1)}{\lVert \vec{x} - \vec{a} \rVert} = 0 \quad \forall \, \vec{x} \in \mathbb{R}^2
            \end{aligned}
            $$

            > $\Longrightarrow$ &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0$

            > $\Longrightarrow$ &nbsp; $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$ is differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \in \mathbb{R}^2$
            """,
        ],
        label="ex-x1-differentiable",
    )
    return


if __name__ == "__main__":
    app.run()
