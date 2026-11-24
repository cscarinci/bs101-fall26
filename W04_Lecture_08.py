import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 8 · Local properties of scalar functions and maps", css_file="lecturekit/style.css")


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
    lk.lecture(8, "Local properties of scalar functions and maps")
    return


@app.cell(hide_code=True)
def _(Figure, lk, np):
    # Helpers of this lecture: bare sketches, axes through the origin, an organic region

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        lk.arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        lk.arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        rng = np.random.default_rng(seed)
        t = np.linspace(0, 2 * np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * np.cos(k * t + rng.uniform(0, 2 * np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * np.cos(t), cy + ry * r * np.sin(t)

    return blank, blob, cross_axes


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    eps = lk.slider(0.3, 2, step=0.1, value=1, label=r"$\varepsilon$")
    theta = lk.slider(0, 180, step=5, value=0, label=r"$\theta$")
    return eps, theta


@app.cell(hide_code=True)
def _(Figure, cross_axes, lk, math, np):
    # module: recap
    # recap: local properties of paths, with the sketches of gamma and sigma
    _fig = Figure(figsize=(lk.FULL, 2.9), layout="constrained")
    _ax, _ax2 = _fig.subplots(1, 2)

    cross_axes(_ax, (-1.9, 1.9), (-0.6, 2.4))
    _t = np.linspace(-1.5, 1.5, 200)
    _ax.plot(_t, _t**2, color=lk.BLUE, lw=1.4)
    _ax.plot(0, 0, "o", color="black", ms=6, mfc="white", mew=1.2, zorder=4)
    _ax.plot(0, 1, "o", color="black", ms=5, zorder=4)
    _ax.plot(-1.2, 1.44, "o", color=lk.BLUE, ms=5, zorder=4)
    _ax.text(1.3, 1.3, r"$\mathrm{Im}(\gamma)$", color=lk.BLUE, fontsize=13, ha="left", va="top")
    _ax.text(-1.3, 1.3, r"$\genfrac{[}{]}{0}{0}{t}{t^2}$", fontsize=13, ha="right", va="top")
    _ax.text(0.1, 1, r"$\genfrac{[}{]}{0}{0}{0}{1}$", fontsize=13, ha="left", va="center")
    _ax.text(0.1, -0.1, "not continuous", fontsize=12, ha="left", va="top")

    cross_axes(_ax2, (-1.6, 1.9), (-1.5, 1.7))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax2.plot(np.cos(_th), np.sin(_th), color=lk.BLUE, lw=1.4)
    _ax2.plot(1, 0, "o", color=lk.GREEN, ms=5, zorder=4)
    _ax2.plot(0, 1, "o", color="black", ms=5, zorder=4)
    _ax2.plot(math.cos(0.7), math.sin(0.7), "o", color=lk.BLUE, ms=5, zorder=4)
    _ax2.text(-0.8, -0.8, r"$\mathrm{Im}(\sigma)$", color=lk.BLUE, fontsize=13, ha="right", va="top")
    _ax2.text(1.12 * math.cos(0.7), 1.12 * math.sin(0.7), r"$\genfrac{[}{]}{0}{0}{\cos(t)}{\sin(t)}$", fontsize=13, ha="left", va="bottom")
    _ax2.text(-0.1, 1.08, r"$\genfrac{[}{]}{0}{0}{0}{1}$", fontsize=13, ha="right", va="bottom")
    _ax2.text(1.08, -0.08, r"$\lim_{t \to 0} \sigma(t)$", color=lk.GREEN, fontsize=13, ha="left", va="top")

    lk.recap(
        lk.aside(
            r"$\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, &nbsp; $\gamma(t) = \mk{\begin{bmatrix} \gamma^1(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix}}$",
            "components",
        ),
        r"> $\leadsto$ &nbsp; $\displaystyle\lim_{t \to a} \gamma(t) = \lim_{t \to a} \begin{bmatrix} \gamma^1(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix} = \begin{bmatrix} \lim_{t \to a} \gamma^1(t) \\ \vdots \\ \lim_{t \to a} \gamma^m(t) \end{bmatrix}$",
        lk.aside(
            r"> $\leadsto$ &nbsp; $\gamma$ continuous at $t = a$ if $\displaystyle\lim_{t \to a} \gamma(t) \mk{{} = \gamma(a)}$",
            r"$\gamma(a)$: position of $\gamma$ at $t = a$<br>$\gamma$ does not jump between positions at $t = a$",
        ),
        lk.aside(
            r"> $\leadsto$ &nbsp; $\gamma$ differentiable at $t = a$ if $\displaystyle\mk{\lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}}$ exists",
            r"$\gamma'(a)$: velocity of $\gamma$ at $t = a$",
        ),
        lk.gap(),
        r"""
        $\gamma(t) = \begin{cases} \begin{bmatrix} t \\ t^2 \end{bmatrix}, & t \neq 0\\[12pt] \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0 \end{cases}$ &emsp;&emsp; $\sigma(t) = \begin{cases} \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, & t \neq 0\\[12pt] \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0 \end{cases}$
        """,
        lk.figure(_fig),
        lk.aside(
            r"$\displaystyle\lim_{t \to 0} \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} \cos(2\pi) \\ \sin(2\pi) \end{bmatrix} = \begin{bmatrix} \cos(4\pi) \\ \sin(4\pi) \end{bmatrix}$",
            r"also in $\mathrm{Im}(\sigma)$",
        ),
        r"""
        $\leadsto$ &nbsp; discontinuity is a “jump” in the parameterization of the image, not necessarily a hole in $\mathrm{Im}(\sigma)$

        $\leadsto$ &nbsp; discontinuity is a hole in $\mathrm{graph}(\gamma)$!
        """,
        topic="Local properties of paths",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Local properties of scalar functions and maps", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.2")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: operations
    # remark: sums, products and compositions of maps
    lk.remark(
        r"""
        Given $f, g : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\lambda : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$, we can define

        > • &nbsp; $(f + g) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $(f + g)(\vec{x}) = f(\vec{x}) + g(\vec{x})$

        > • &nbsp; $(\lambda f) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $(\lambda f)(\vec{x}) = \lambda(\vec{x}) f(\vec{x})$

        > • &nbsp; $(f \cdot g) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $(f \cdot g)(\vec{x}) = f(\vec{x}) \cdot g(\vec{x})$

        If $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ and $g : B \subseteq \mathbb{R}^m \longrightarrow C \subseteq \mathbb{R}^p$

        > • &nbsp; $(g \circ f) : A \subseteq \mathbb{R}^n \longrightarrow C \subseteq \mathbb{R}^p$ &nbsp; $\leadsto$ &nbsp; $(g \circ f)(\vec{x}) = g(f(\vec{x}))$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: open balls
    # section
    lk.section("Limits")
    return


@app.cell(hide_code=True)
def _(blank, lk, np):
    # module: open balls
    # definition: open ball, with the sketch of a, x, x - a and the radius delta
    _fig, _ax = blank(3.6, 2.5, (-0.4, 3.8), (-0.4, 3.0))
    lk.arrow(_ax, (-0.3, 0), (3.7, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.3), (0, 2.9), "black", lw=0.9)
    _a, _d = (2.1, 1.5), 1.15
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=lk.LIGHT, lw=0)
    _ax.plot(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=lk.BLUE, lw=1.2, ls=(0, (4, 3)))
    _x = (1.35, 2.05)
    _r = (_a[0] + _d * np.cos(-0.26), _a[1] + _d * np.sin(-0.26))
    _ax.plot([_a[0], _r[0]], [_a[1], _r[1]], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    lk.arrow(_ax, (0, 0), _a, "black")
    lk.arrow(_ax, (0, 0), _x, lk.RED)
    lk.arrow(_ax, _a, _x, lk.GREEN)
    _ax.text(_a[0] / 2 + 0.08, _a[1] / 2 - 0.08, r"$\vec{a}$", fontsize=13, ha="left", va="top")
    _ax.text(_x[0] / 2 - 0.08, _x[1] / 2 + 0.05, r"$\vec{x}$", color=lk.RED, fontsize=13, ha="right", va="bottom")
    _ax.text((_a[0] + _x[0]) / 2 + 0.05, (_a[1] + _x[1]) / 2 + 0.1, r"$\vec{x} - \vec{a}$", color=lk.GREEN, fontsize=13, ha="left", va="bottom")
    _ax.text((_a[0] + _r[0]) / 2 - 0.02, (_a[1] + _r[1]) / 2 - 0.06, r"$\delta$", color=lk.GREY, fontsize=13, ha="right", va="top")
    _ax.text(_a[0] + _d * np.cos(2.3) - 0.05, _a[1] + _d * np.sin(2.3) + 0.05, r"$B(\vec{a}, \delta)$", color=lk.BLUE, fontsize=13, ha="right", va="bottom")

    lk.definition(
        [
            r"Given $\vec{a} \in \mathbb{R}^n$ and $\delta > 0$",
            lk.aside(
                r"$$ B(\vec{a}, \delta) = \big\{ \vec{x} \in \mathbb{R}^n \;\big|\; \mk{\lVert \vec{x} - \vec{a} \rVert < \delta} \big\} $$",
                r"distance of $\vec{x}$ from $\vec{a}$<br>is smaller than $\delta$",
            ),
            r"is the **open ball** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$",
            lk.figure(_fig),
        ],
        label="def-open-ball",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: open balls
    # remark: the boundary is not included; sphere and closed ball
    lk.remark(
        [
            r"""
            The “boundary” is not included!

            > Only “interior” points are part of $B(\vec{a}, \delta)$

            > $\leadsto$ &nbsp; $S(\vec{a}, \delta) = \big\{ \vec{x} \in \mathbb{R}^n \;\big|\; \lVert \vec{x} - \vec{a} \rVert = \delta \big\}$ &nbsp; (**sphere** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$)
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $\mk{\overline{B(\vec{a}, \delta)}} = B(\vec{a}, \delta) \cup S(\vec{a}, \delta)$ &nbsp; (**closed ball** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$)",
                r"$\lVert \vec{x} - \vec{a} \rVert \leq \delta$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # definition: limit of a map
    lk.definition(
        [
            r"Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\vec{a} \in \mathbb{R}^n$, $\vec{b} \in \mathbb{R}^m$, we say",
            lk.aside(
                r"$$ \lim_{\vec{x} \to \vec{a}} f(\vec{x}) \mk{{} = \vec{b}} $$",
                r"the limit of $f(\vec{x})$ as $\vec{x}$ approaches $\vec{a}$<br>exists and is equal to $\vec{b}$",
            ),
            r"""
            if for every choice of $\varepsilon > 0$

            > we can make $f(\vec{x})$ $\varepsilon$-close to $\vec{b}$

            by finding $\delta > 0$ and
            """,
            lk.aside(r"> taking $\vec{x}$ $\mk{\delta\text{-close to } \vec{a}}$", r"different from $\vec{a}$"),
        ],
        label="def-limit",
    )
    return


@app.cell(hide_code=True)
def _(blank, lk, mo, np):
    # module: limits
    # prose: the definition with balls, with the sketch of B(a, delta) in R^n and, turning, B(b, epsilon) in R^m with the
    # image of the punctured ball
    _fig, _ax = blank(3.9, 3.4, (-0.5, 5.1), (-0.6, 3.6))
    _th = np.linspace(0, 2 * np.pi, 200)
    lk.arrow(_ax, (-0.4, 0), (3.4, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.5), (0, 3.0), "black", lw=0.9)
    _ax.text(-0.15, 3.05, r"$\mathbb{R}^n$", fontsize=13, ha="right", va="center")
    _ax.fill(1.5 + 0.85 * np.cos(_th), 1.75 + 0.85 * np.sin(_th), color=lk.LIGHT, lw=0)
    _ax.plot(1.5 + 0.85 * np.cos(_th), 1.75 + 0.85 * np.sin(_th), color=lk.BLUE, lw=1.2, ls=(0, (4, 3)))
    _ax.plot(1.5, 1.75, "o", color="black", ms=5, zorder=4)
    _ax.text(1.5, 0.82, r"$B(\vec{a}, \delta)$", color=lk.BLUE, fontsize=13, ha="center", va="top")
    _ax.text(1.6, 1.75, r"$\vec{a}$", fontsize=13, ha="left", va="center")
    lk.arrow(_ax, (3.7, 2.2), (5.0, 2.2), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(4.35, 2.55, "$f$", fontsize=13, ha="center", va="bottom")

    # R^m: the ball about b, see-through (light red, a few grey circles), b, and the image of the punctured ball, a small
    # flat disk inside the ball, upper left of b
    _c, _r = np.array((0.5, 1.9, 1.7)), 1.1
    _b = _c + (0.0, 0.25, 0.12)
    _u, _w = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 49), indexing="ij")
    _ball = lk.sheet(_c[0] + _r * np.sin(_u) * np.cos(_w), _c[1] + _r * np.sin(_u) * np.sin(_w), _c[2] + _r * np.cos(_u),
                     wire=[(0, 12, lk.GREY, 1.0), (1, 12, lk.GREY, 0.5)], flat="#f4e4e1", alpha=0.5)
    _g = _c + (0.0, -0.35, 0.42)
    _s2, _w2 = np.meshgrid(np.linspace(0, 1, 4), np.linspace(0, 2 * np.pi, 37), indexing="ij")
    _d1, _d2 = _g[0] + 0.3 * _s2 * np.cos(_w2), _g[1] + 0.3 * _s2 * np.sin(_w2)
    _image = lk.sheet(_d1, _d2, np.full_like(_d1, _g[2]), flat="#bcd5c2", alpha=0.95)
    _ball3d = lk.turntable(
        25,
        20,
        "the ball about b in R^m, the point b, and the image of the punctured ball about a, a small region inside the ball",
        [
            lk.panel(
                1.0,
                surfaces=[_ball, _image],
                lines=[(_d1[-1], _d2[-1], np.full(37, _g[2]), lk.GREEN, 1.0)],
                points=[(tuple(_b), lk.RED, 4.0)],
                axes=[((0, 0, 0), (2.2, 0, 0), "", 0), ((0, 0, 0), (0, 3.6, 0), "", 0), ((0, 0, 0), (0, 0, 3.3), r"\mathbb{R}^m", 150)],
                texts=[(tuple(_c + (0, _r, 0)), r"B(\vec{b}, \varepsilon)", lk.RED, 0, 8), (tuple(_b), r"\vec{b}", "#000000", 0, 6),
                       (tuple(_c + (0, 0, _r)), r"f(B(\vec{a}, \delta) - \{\vec{a}\})", lk.GREEN, 90, 8)],
            )
        ],
        height=300,
        width=300,
    )

    lk.prose(
        r"""
        $\leadsto$ &nbsp; for every $\varepsilon > 0$, we can find $\delta > 0$ such that

        > $\vec{x} \in B(\vec{a}, \delta) - \{\vec{a}\}$ guarantees that $f(\vec{x}) \in B(\vec{b}, \varepsilon)$

        > > $\Longleftrightarrow$ &nbsp; $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$
        """,
        lk.figure(mo.hstack([_fig, _ball3d], justify="center", align="center", gap=1)),
        r"""
        choose $B(\vec{b}, \varepsilon)$ &nbsp; $\leadsto$ &nbsp; can we find $B(\vec{a}, \delta)$ such that $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$?

        > if yes for every $\varepsilon > 0$

        > > $\Longrightarrow$ &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$!
        """,
    )
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, eps, lk, np):
    # module: limits
    # example: 2 (x^1)^2 / |x| has limit 0 at 0, with B(0, delta) for delta = epsilon / 2 and its image inside B(0, epsilon)
    _e = eps.value
    _d = _e / 2
    _fig = Figure(figsize=(lk.FULL, 3.4), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 0.8])

    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.fill(_d * np.cos(_th), _d * np.sin(_th), color=lk.LIGHT, lw=0, zorder=0)
    _left.plot(_d * np.cos(_th), _d * np.sin(_th), color=lk.BLUE, lw=1.2, ls=(0, (4, 3)))
    _left.plot(0, 0, "o", color="black", ms=5, mfc="white", mew=1.1, zorder=4)

    _right.set_xlim(-1.0, 1.9)
    _right.set_ylim(-2.6, 5.9)
    _right.axis("off")
    lk.arrow(_right, (0, -2.6), (0, 5.85), "black", lw=0.9)
    _right.text(-0.2, 5.75, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    # tick names at their ticks; below 0.6 the names of +-eps sit just above and below them, and below 0.3 the 0 is not written
    _near = _e < 0.6
    for _y, _name, _va in ((_e, r"$\varepsilon$", "bottom" if _near else "center"), (-_e, r"$-\varepsilon$", "top" if _near else "center"), (0, "$0$", "center"), (5, "$5$", "center")):
        _right.plot([-0.07, 0.07], [_y, _y], color="black", lw=0.9)
        if _y != 0 or _e >= 0.3:
            _right.text(-0.2, _y, _name, ha="right", va=_va, fontsize=12)
    _right.plot([0.3, 0.3], [-_e, _e], color=lk.RED, lw=1.4)
    _right.plot([0.3, 0.3], [-_e, _e], "o", color=lk.RED, ms=5, mfc="white", mew=1.1, zorder=4)
    _right.plot([0.6, 0.6], [0, _e], color=lk.GREEN, lw=1.4)
    _right.plot(0.6, 0, "o", color=lk.GREEN, ms=5, zorder=4)
    _right.plot(0.6, _e, "o", color=lk.GREEN, ms=5, mfc="white", mew=1.1, zorder=4)
    _right.plot(0, 5, "o", color="black", ms=5, zorder=4)
    _left.text(_d * 0.71 + 0.05, _d * 0.71 + 0.05, r"$B(\vec{0}, \delta) - \{\vec{0}\}$", color=lk.BLUE, fontsize=13, ha="left", va="bottom")
    _left.text(-0.06, -0.06, r"$\vec{0}$", fontsize=13, ha="right", va="top")
    _right.text(0.22, -_e - 0.15, r"$B(0, \varepsilon)$", color=lk.RED, fontsize=13, ha="left", va="top")
    _right.text(0.5, _e + 0.15, r"$f(B(\vec{0}, \delta) - \{\vec{0}\})$", color=lk.GREEN, fontsize=13, ha="left", va="bottom")
    _right.text(0.12, 5, r"$f(\vec{0})$", fontsize=13, ha="left", va="center")

    lk.example(
        [
            r"""
            $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $f(\vec{x}) = \begin{cases} 2 \, \dfrac{(x^1)^2}{\lVert \vec{x} \rVert}, & \vec{x} \neq \vec{0}\\[10pt] 5, & \vec{x} = \vec{0} \end{cases}$

            Claim: &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{0}} f(\vec{x}) = 0$
            """,
            lk.interactive(_fig, controls=[eps]),
        ],
        label="ex-limit-zero",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limits
    # proof of the claim
    lk.proof(
        [
            r"""
            To show this

            > 1\. &nbsp; choose $\varepsilon > 0$ &nbsp; (let's say $\varepsilon = 1$)

            > 2\. &nbsp; look for $\delta > 0$ such that
            """,
            lk.aside(
                r"""
                $$
                \underbrace{0 < \lVert \vec{x} - \vec{0} \rVert < \delta}_{\begin{array}{c} \scriptstyle \text{whenever } \vec{x} \text{ is} \\ \scriptstyle \delta\text{-close to } \vec{a} = \vec{0} \end{array}} \qquad \underbrace{\Longrightarrow}_{\begin{array}{c} \scriptstyle \text{we} \\ \scriptstyle \text{guarantee} \end{array}} \qquad \underbrace{\lvert f(\vec{x}) - 0 \rvert < \varepsilon = 1}_{\begin{array}{c} \scriptstyle f(\vec{x}) \text{ is } \mk{1\text{-close}} \\ \scriptstyle \text{to } b = 0 \end{array}}\rule[-2.4em]{0pt}{0pt}
                $$
                """,
                "1-close: as close as we want it",
            ),
            r"""
            For $\vec{x} \neq \vec{0}$

            $$
            \lvert f(\vec{x}) - 0 \rvert = \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} \leq \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} + \frac{2 (x^2)^2}{\lVert \vec{x} \rVert} = 2 \, \frac{\lVert \vec{x} \rVert^2}{\lVert \vec{x} \rVert} = 2 \lVert \vec{x} \rVert
            $$

            > $\Longrightarrow$ &nbsp; $\lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert = 2 \lVert \vec{x} - \vec{0} \rVert$

            > $\Longrightarrow$ &nbsp; whenever we make $0 < \lVert \vec{x} - \vec{0} \rVert < 1/2 = \delta$ &nbsp; (for $\varepsilon = 1$) we guarantee that $\lvert f(\vec{x}) - 0 \rvert < 1$
            """,
            lk.aside(
                r"now repeat the argument for every $\varepsilon > 0$",
                r"$\varepsilon = 1/2 \leadsto \delta = 1/4$<br>$\varepsilon = 1/3 \leadsto \delta = 1/6$<br>$\vdots$",
            ),
            lk.aside(
                r"$\therefore$ &nbsp; if $0 < \lVert \vec{x} - \vec{0} \rVert < \mk{\varepsilon / 2}$",
                r"$\varepsilon / 2 = \delta$",
            ),
            r"> $\Longrightarrow$ &nbsp; $\lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert < 2 \cdot \varepsilon / 2 = \varepsilon$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: uniqueness
    # theorem: limits are unique
    lk.theorem(
        [
            r"""
            $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ and $\vec{a} \in \mathbb{R}^n$

            > if $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1 \in \mathbb{R}^m$ and $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_2 \in \mathbb{R}^m$
            """,
            lk.aside(r"> then $\mk{\vec{b}_1 = \vec{b}_2}$", "limits are unique!<br>⇝ when they exist"),
        ],
        label="thm-unique-limit",
    )
    return


@app.cell(hide_code=True)
def _(blank, blob, lk, np):
    # module: uniqueness
    # proof, with the sketch of B(a, delta), the two disjoint balls about b1, b2 and the image of the punctured ball
    _tint = (0.18, 0.49, 0.2, 0.18)
    _fig, _ax = blank(lk.FULL, 3.0, (-0.3, 9.1), (-0.15, 3.05))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(1.2 + 0.8 * np.cos(_th), 1.5 + 0.8 * np.sin(_th), color=lk.LIGHT, lw=0)
    _ax.plot(1.2 + 0.8 * np.cos(_th), 1.5 + 0.8 * np.sin(_th), color=lk.BLUE, lw=1.2, ls=(0, (4, 3)))
    _ax.plot([1.2, 1.2 + 0.8 * 0.82], [1.5, 1.5 + 0.8 * 0.57], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot(1.2, 1.5, "o", color="black", ms=5, zorder=4)
    lk.arrow(_ax, (2.5, 2.0), (3.8, 2.0), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(3.15, 2.33, "$f$", fontsize=13, ha="center", va="bottom")
    for _c, _col in ((5.5, lk.RED), (7.7, lk.ORANGE)):
        _ax.plot(_c + 1.1 * np.cos(_th), 1.5 + 1.1 * np.sin(_th), color=_col, lw=1.2, ls=(0, (4, 3)))
        _ax.plot([_c, _c + 1.1], [1.5, 1.5], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.plot(_c, 1.5, "o", color=_col, ms=5, zorder=4)
    _bx, _by = blob(5.15, 2.05, 0.4, 0.26, seed=3)
    _ax.fill(_bx, _by, color=_tint, lw=0)
    _ax.plot(_bx, _by, color=lk.GREEN, lw=1.2)
    _ax.text(1.2, 0.62, r"$B(\vec{a}, \delta)$", color=lk.BLUE, fontsize=13, ha="center", va="top")
    _ax.text(1.1, 1.5, r"$\vec{a}$", fontsize=13, ha="right", va="center")
    _ax.text(1.48, 1.8, r"$\delta$", color=lk.GREY, fontsize=13, ha="right", va="bottom")
    for _c, _col, _i in ((5.5, lk.RED, 1), (7.7, lk.ORANGE, 2)):
        _ax.text(_c + 0.55, 1.55, r"$\varepsilon$", color=lk.GREY, fontsize=13, ha="center", va="bottom")
        _ax.text(_c, 1.42, rf"$\vec{{b}}_{_i}$", fontsize=13, ha="center", va="top")
        _ax.text(_c, 0.32, rf"$B(\vec{{b}}_{_i}, \varepsilon)$", color=_col, fontsize=13, ha="center", va="top")
    _ax.text(5.15, 2.68, r"$f(B(\vec{a}, \delta) - \{\vec{a}\})$", color=lk.GREEN, fontsize=13, ha="center", va="bottom")

    lk.proof(
        [
            r"Given $\vec{b}_1 \neq \vec{b}_2 \in \mathbb{R}^m$ let $\varepsilon = \dfrac{\lVert \vec{b}_2 - \vec{b}_1 \rVert}{2}$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $B(\vec{b}_1, \varepsilon) \cap B(\vec{b}_2, \varepsilon) \mk{{} = \emptyset}$",
                "remember: the sphere is not part of the ball<br>to be more precise we need to use<br>the triangle inequality",
            ),
            lk.figure(_fig),
            r"""
            > $\Longrightarrow$ &nbsp; if $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1$, then there is a $\delta_1 > 0$ such that

            $$
            f\big( B(\vec{a}, \delta_1) - \{\vec{a}\} \big) \subset B(\vec{b}_1, \varepsilon)
            $$

            > $\Longrightarrow$ &nbsp; for any $\delta_2 < \delta_1$

            $$
            f\big( B(\vec{a}, \delta_2) - \{\vec{a}\} \big) \not\subset B(\vec{b}_2, \varepsilon)
            $$

            > $\Longrightarrow$ &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) \neq \vec{b}_2$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, cross_axes, lk, math, np, theta):
    # module: limit does not exist
    # example: (x^1)^2 / |x|^2 has no limit at 0, with the line through 0 at angle theta and its constant value
    _a = math.radians(theta.value)
    _c, _s = math.cos(_a) + 0.0, math.sin(_a) + 0.0
    _c, _s = (0.0 if abs(_c) < 1e-12 else _c), (0.0 if abs(_s) < 1e-12 else _s)
    _val = _c**2

    _fig = Figure(figsize=(lk.FULL, 3.4), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 0.8])
    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.plot(0.8 * np.cos(_th), 0.8 * np.sin(_th), color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _left.plot([-1.1 * _c, 1.1 * _c], [-1.1 * _s, 1.1 * _s], color=lk.BLUE, lw=1.4, zorder=3.5)
    _left.plot(0, 0, "o", color="black", ms=5, mfc="white", mew=1.1, zorder=4)

    _right.set_xlim(-1.2, 1.4)
    _right.set_ylim(-0.5, 1.6)
    _right.axis("off")
    lk.arrow(_right, (0, -0.5), (0, 1.58), "black", lw=0.9)
    _right.text(-0.15, 1.55, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    for _y in (0, 1):
        _right.plot([-0.05, 0.05], [_y, _y], color="black", lw=0.9)
        _right.text(-0.15, _y, f"${_y}$", ha="right", va="center", fontsize=12)
    _right.plot(0, _val, "o", color=lk.GREEN, ms=5, zorder=4)
    _m = math.radians(45 if abs(theta.value - 135) < abs(theta.value - 45) else 135)  # the side the line is not on
    _left.text(0.9 * math.cos(_m), 0.9 * math.sin(_m), r"$B(\vec{0}, \delta)$", color=lk.GREY, fontsize=13, ha="left" if math.cos(_m) > 0 else "right", va="bottom")
    _left.text(0.06 if 0 < theta.value < 90 else -0.06, -0.06, r"$\vec{0}$", fontsize=13, ha="left" if 0 < theta.value < 90 else "right", va="top")
    _right.text(0.1, _val, r"$f(\vec{x})$", color=lk.GREEN, fontsize=13, ha="left", va="center")

    lk.example(
        [
            r"$f(\vec{x}) = \dfrac{(x^1)^2}{\lVert \vec{x} \rVert^2} = \dfrac{(x^1)^2}{(x^1)^2 + (x^2)^2}$",
            lk.aside(
                r"Claim: &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{0}} f(\vec{x})$ $\mk{\text{does not exist}}$!",
                "it is not well-defined",
            ),
            lk.interactive(_fig, controls=[theta]),
        ],
        label="ex-no-limit",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: limit does not exist
    # proof of the claim: two ways of approaching 0
    lk.proof(
        [
            r"Let's consider two different ways $\vec{x}$ can approach $\vec{0}$",
            lk.aside(
                r"> 1\. &nbsp; along $\vec{x} = t\vec{e}_1 = \begin{bmatrix} t \\ 0 \end{bmatrix}$ for $t \neq 0$",
                r"since $\vec{x} \neq \vec{0}$",
            ),
            lk.aside(r"> > $f(t\vec{e}_1) = \dfrac{t^2}{t^2 + 0^2} = \mk{1}$", "constant"),
            r"> > For any chosen $\varepsilon > 0$",
            lk.aside(
                r"> > > $0 < \lVert t\vec{e}_1 - \vec{0} \rVert \mk{{} < \delta}$ &nbsp; $\Longrightarrow$ &nbsp; $\lVert f(t\vec{e}_1) - 1 \rVert = 0 < \varepsilon$",
                r"for every $\delta > 0$!<br>since $f(t\vec{e}_1) = 1$ is constant!",
            ),
            r"> > $\therefore$ &nbsp; $\displaystyle\lim_{\substack{\vec{x} \to \vec{0} \\ \vec{x} = t\vec{e}_1}} f(\vec{x}) = 1$",
            lk.gap(),
            r"""
            > 2\. &nbsp; along $\vec{x} = s\vec{e}_2 = \begin{bmatrix} 0 \\ s \end{bmatrix}$ for $s \neq 0$

            > > $f(s\vec{e}_2) = \dfrac{0^2}{0^2 + s^2} = 0 \quad \forall \, s \neq 0$

            > > For any $\varepsilon > 0$
            """,
            lk.aside(
                r"> > > $0 < \lVert s\vec{e}_2 - \vec{0} \rVert \mk{{} < \delta}$ &nbsp; $\Longrightarrow$ &nbsp; $\lVert f(s\vec{e}_2) - 0 \rVert = 0 < \varepsilon$",
                r"for every $\delta > 0$!",
            ),
            r"> > $\therefore$ &nbsp; $\displaystyle\lim_{\substack{\vec{x} \to \vec{0} \\ \vec{x} = s\vec{e}_2}} f(\vec{x}) = 0$",
            lk.gap(),
            r"""
            two possible values for the limit

            > $\Longrightarrow$ &nbsp; limit is not well-defined!
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: algebra of limits
    # theorem: limits of sums and products
    lk.theorem(
        r"""
        Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\lambda : \mathbb{R}^n \longrightarrow \mathbb{R}$

        > if $\displaystyle\lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1$, &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} g(\vec{x}) = \vec{b}_2$, &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} \lambda(\vec{x}) = \beta$

        > > • &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} (f + g)(\vec{x}) = \vec{b}_1 + \vec{b}_2$

        > > • &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} (\lambda f)(\vec{x}) = \beta \vec{b}_1$

        > > • &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} (f \cdot g)(\vec{x}) = \vec{b}_1 \cdot \vec{b}_2$
        """,
        label="thm-limit-algebra",
    )
    return


if __name__ == "__main__":
    app.run()
