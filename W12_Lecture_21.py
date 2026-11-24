import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 21 · Green's theorem", css_file="lecturekit/style.css")


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
    lk.lecture(21, "Green's theorem")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points), arrowheads along a curve, the closed curve
    # of the regions with their boundary, and a walking figure

    def drawing(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def beside(ax, at, angle, text, color, w, h, gap=4, fontsize=13, face="none"):
        """Name centred beside the point `at`, in the direction `angle` (degrees), far enough for a
        w x h box (points) to clear it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        d = w / 2 * abs(c) + h / 2 * abs(s) + gap
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": face, "edgecolor": "none"})

    def plane(xlim, ylim, width):
        """A drawing of the xy-plane: the two axes as arrows, named at their tips."""
        fig, ax = drawing(xlim, ylim, width)
        lk.arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        lk.arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, "$x$", "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, "$y$", "black", 10, 12)
        return fig, ax

    def along(ax, x, y, color, at=(0.5,), lw=1.8):
        """Arrowheads on the curve through the points (x[k], y[k]), at the fractions `at` of its points,
        pointing the way the points run."""
        n = len(x)
        for f in at:
            k = round(f * (n - 1))
            j = max(k - max(n // 40, 1), 0)
            ax.annotate("", xy=(x[k], y[k]), xytext=(x[j], y[j]), zorder=5, arrowprops={"arrowstyle": f"->,head_length={4.5 * lw:g},head_width={2 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0})

    def blob(cy):
        """The closed curve of the two drawings of a region with its boundary, run counter-clockwise
        about the point (2.3, cy): two arrays."""
        s = np.linspace(0, 2 * np.pi, 400)
        r = 1 + 0.1 * np.cos(3 * s) + 0.06 * np.sin(2 * s)
        return 2.3 + 1.5 * r * np.cos(s), cy + 0.95 * r * np.sin(s)

    def walker(ax, at, h=0.5, color="black"):
        """A walking figure of height h centred at the point `at`: head, body, arms and legs."""
        x, y = at[0], at[1] - h / 2
        s = np.linspace(0, 2 * np.pi, 40)
        ax.plot(x + 0.13 * h * np.cos(s), y + 0.87 * h + 0.13 * h * np.sin(s), color=color, lw=1.1, zorder=7)
        for u, v in (([0, 0], [0.74, 0.36]), ([-0.2, 0, 0.2], [0.46, 0.62, 0.46]), ([-0.16, 0, 0.16], [0, 0.36, 0])):
            ax.plot(x + h * np.array(u), y + h * np.array(v), color=color, lw=1.1, zorder=7, solid_capstyle="round")

    return along, beside, blob, drawing, plane, walker


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    tc = lk.slider(-1.0, 1.0, step=0.02, value=0.5, label="$t$")
    return (tc,)


@app.cell(hide_code=True)
def _(beside, drawing, lk, np):
    # module: recap
    # recap
    # the curve C = gamma([a, b]) (blue) from gamma(a) to gamma(b); at the point gamma(t), its velocity gamma'(t) (green)
    # and the vector F(gamma(t)) of a vector field (red)
    def _g(s):
        return np.array([s, 0.9 * np.sin(1.1 * s) + 0.3 * s])

    _a, _b, _t = 0.0, 4.8, 1.2
    _fig, _ax = drawing((-1.0, 5.8), (-0.5, 2.3), 4.4)
    _ax.plot(*_g(np.linspace(_a, _b, 300)), color=lk.BLUE, lw=1.8)
    _p = _g(_t)
    _v = np.array([1.0, 0.99 * np.cos(1.1 * _t) + 0.3])
    _f = np.array([0.75, -0.55])
    lk.arrow(_ax, _p, _p + _f, lk.RED, lw=1.6)
    lk.arrow(_ax, _p, _p + _v, lk.GREEN, lw=1.6)
    for _q in (_g(_a), _g(_b), _p):
        _ax.plot(*_q, "o", color="black", ms=4.5, zorder=6)
    beside(_ax, _g(_a), 180, r"$\gamma(a)$", "black", 30, 16)
    beside(_ax, _g(_b), 0, r"$\gamma(b)$", "black", 30, 16)
    beside(_ax, _p, 135, r"$\gamma(t)$", "black", 30, 16)
    beside(_ax, _p + _v, 0, r"$\gamma'(t)$", lk.GREEN, 30, 16)
    beside(_ax, _p + _f, -90, r"$\vec{F}(\gamma(t))$", lk.RED, 52, 18)
    lk.recap(
        r"Double integration over simple regions in $\mathbb{R}^2$",
        lk.under(
        r"""
        Region $D\subseteq\mathbb{R}^2$ is called

        > <span class="lk-tab" style="--lk-tab: 4.6em">$y$-simple</span>if $D=\lbrace (x,y)\in\mathbb{R}^2 \mid a\le x\le b,\ \varphi_1(x)\le y\le\varphi_2(x)\rbrace$

        > <span class="lk-tab" style="--lk-tab: 4.6em"></span>for $\varphi_1,\varphi_2:[a,b]\to\mathbb{R}$ continuous

        > <span class="lk-tab" style="--lk-tab: 4.6em"></span>$\leadsto$ &nbsp; $\displaystyle\iint_D f(x,y)\,dxdy=\int_a^b\left(\int_{\varphi_1(x)}^{\varphi_2(x)}f(x,y)\,dy\right)dx$

        > <span class="lk-tab" style="--lk-tab: 4.6em">$x$-simple</span>if $D=\lbrace (x,y)\in\mathbb{R}^2 \mid c\le y\le d,\ \psi_1(y)\le x\le\psi_2(y)\rbrace$

        > <span class="lk-tab" style="--lk-tab: 4.6em"></span>for $\psi_1,\psi_2:[c,d]\to\mathbb{R}$ continuous

        > <span class="lk-tab" style="--lk-tab: 4.6em"></span>$\leadsto$ &nbsp; $\displaystyle\iint_D f(x,y)\,dxdy=\int_c^d\left(\int_{\psi_1(y)}^{\psi_2(y)}f(x,y)\,dx\right)dy$
        """,
        ),
        lk.gap(),
        r"Earlier: line integrals of vector fields over curves",
        lk.under(
        lk.aside(
            r"$$\int_{\mk{\vec{C}}}\vec{F}\cdot d\vec{s}=\int_a^b\vec{F}(\gamma(t))\cdot\gamma'(t)\,dt$$",
            r"$\vec{C}=\gamma([a,b])$",
        ),
        lk.figure(_fig),
        r"""
        FTC &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle\int_{\vec{C}}\vec{\nabla}f\cdot d\vec{s}=f(\gamma(b))-f(\gamma(a))$
        """,
        ),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(along, beside, blob, lk, plane):
    # module: recap
    # goals
    # a region D and its boundary curve C = Bd(D) (red), run counter-clockwise
    _x, _y = blob(1.6)
    _fig, _ax = plane((-0.6, 5.0), (-0.5, 3.4), 3.8)
    _ax.fill(_x, _y, color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot(_x, _y, color=lk.RED, lw=1.8)
    along(_ax, _x, _y, lk.RED, at=(0.3, 0.62, 0.95))
    _ax.text(2.3, 1.6, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x[45], _y[45]), 45, r"$\vec{C} = \mathrm{Bd}(D)$", lk.RED, 84, 18, gap=2)
    lk.goals(
        r"""
        Green's theorem

        > $\leadsto$ &nbsp; relation between double integral over simple regions and line integral over their boundary curve!
        """,
        lk.figure(_fig),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 8.1, 8.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Green's theorem
    # section
    lk.section("Green's theorem")
    return


@app.cell(hide_code=True)
def _(beside, blob, lk, math, plane, walker):
    # module: Green's theorem
    # definition: orientation of the boundary
    # the curve C (red) around the region D: the two walking figures go around it counter-clockwise, each in the
    # direction of its arrow, with D on their left
    _x, _y = blob(2.1)
    _fig, _ax = plane((-0.6, 5.0), (-0.5, 4.3), 3.8)
    _ax.fill(_x, _y, color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot(_x, _y, color=lk.RED, lw=1.8)
    _ax.text(2.3, 2.1, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x[150], _y[150]), 135, r"$\vec{C}$", lk.RED, 14, 18)
    for _k in (62, 277):
        # beside the point k of the curve, on its outer side; the arrow starts ahead of the figure, along the curve
        _tx, _ty = _x[_k + 1] - _x[_k - 1], _y[_k + 1] - _y[_k - 1]
        _n = math.hypot(_tx, _ty)
        _tx, _ty = _tx / _n, _ty / _n
        _cx, _cy = _x[_k] + 0.36 * _ty, _y[_k] - 0.36 * _tx
        walker(_ax, (_cx, _cy), h=0.56)
        lk.arrow(_ax, (_cx + 0.3 * _tx, _cy + 0.3 * _ty), (_cx + 0.95 * _tx, _cy + 0.95 * _ty), "black", lw=1.2)
    lk.definition(
        [
            r"""
            Given $D\subseteq\mathbb{R}^2$ a simple region, let $C=\mathrm{Bd}(D)$ denote its boundary points.
            """,
            lk.aside(
                r"We denote by $\vec{C}$ the curve $C$ with the <span class='lk-mark'>counter-clockwise orientation</span>.",
                r"walking around $\vec{C}$,<br>$D$ is always on the left.",
            ),
            lk.figure(_fig),
            lk.aside(
                r"We denote by $\vec{C}^{\,op}$ the curve $C$ with the opposite orientation (<span class='lk-mark'>clockwise</span>)",
                r"$D$ is always on the right",
            ),
            lk.gap(),
            r"""
            We also call

            $$
            \begin{aligned}
            \text{counter-clockwise orientation}&=\textbf{positive orientation}\\
            \text{clockwise orientation}&=\textbf{negative orientation}
            \end{aligned}
            $$
            """,
        ],
        label="def-orientation",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Green's theorem
    # theorem: Green
    lk.theorem(
        [
            lk.aside(
                r"Given a <span class='lk-mark'>simple</span> region $D\subseteq\mathbb{R}^2$, $\vec{C}=\mathrm{Bd}(D)$ with the positive orientation, and",
                r"both $y$-simple and $x$-simple",
            ),
            r"""
            $\vec{F}(x,y)=\begin{bmatrix} P(x,y) \\ Q(x,y) \end{bmatrix}$ &nbsp; a $C^1$-smooth vector field on $D$
            """,
            lk.aside(
                r"""
                $$
                \underbrace{\int_{\vec{C}}\vec{F}\cdot d\vec{s}}_{\footnotesize\begin{matrix}\text{line integral}\\\text{over the boundary}\end{matrix}}
                =\underbrace{\iint_D\left(\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)\right)dxdy}_{\footnotesize\begin{matrix}\text{double integral of}\\\text{some derivative of }\vec{F}\end{matrix}}
                $$
                """,
                r"some derivative of $\vec{F}$ = scalar curl!",
            ),
        ],
        title="Green",
        label="thm-green",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Green's theorem
    # consequence
    lk.prose(r"$\leadsto$ &nbsp; generalization of FTC!")
    return


@app.cell(hide_code=True)
def _(along, beside, lk, math, np, plane, tc):
    # module: Green's theorem
    # example: parabola
    # the region D and its boundary: C_1 (red), the parabola from (-1, 1) to (1, 1), and C_2 (orange), the segment from
    # (1, 1) back to (-1, 1). The points gamma_1(t) = (t, t^2) and gamma_2(t) = (-t, 1) (green) move with t
    _t = round(tc.value, 10)
    _fig, _ax = plane((-1.8, 2.25), (-0.5, 2.05), 4.6)
    _d = np.linspace(-1, 1, 200)
    _ax.fill_between(_d, _d**2, 1, color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot(_d, _d**2, color=lk.RED, lw=1.8)
    _ax.plot([1, -1], [1, 1], color=lk.ORANGE, lw=1.8)
    along(_ax, _d, _d**2, lk.RED, at=(0.3, 0.8))
    along(_ax, -_d, 1 + 0 * _d, lk.ORANGE, at=(0.3, 0.8))
    beside(_ax, (-0.75, 0.75**2), 205, r"$\vec{C}_1$", lk.RED, 16, 18)
    beside(_ax, (0.5, 1), 90, r"$\vec{C}_2$", lk.ORANGE, 16, 18)
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "none", "edgecolor": "none"}
    _ax.text(0, 0.56, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=5, bbox=_box)
    # the moving points are named inside D, towards its middle, on the colour of D
    for _p, _name in (((_t, _t**2), r"$\gamma_1(t)$"), ((-_t, 1), r"$\gamma_2(t)$")):
        _ax.plot(*_p, "o", color=lk.GREEN, ms=4.5, zorder=7)
        _c, _s = -_p[0], 0.56 - _p[1]
        _c, _s = _c / math.hypot(_c, _s), _s / math.hypot(_c, _s)
        _r = 16 * abs(_c) + 8 * abs(_s) + 5 + 10 * _p[0] ** 2
        _ax.annotate(_name, _p, textcoords="offset points", xytext=(_r * _c, _r * _s), ha="center", va="center", color=lk.GREEN, fontsize=13, zorder=6, bbox=_box)
    lk.example(
        [
            r"""
            $D=\lbrace (x,y)\mid x^2\le y\le 1\rbrace$, &nbsp; $\vec{F}(x,y)=\begin{bmatrix} -y^2 \\ xy \end{bmatrix}$

            > $C=\mathrm{Bd}(D)=\underbrace{\lbrace (x,y)\mid -1\le x\le 1,\ y=x^2\rbrace}_{C_1}\cup\underbrace{\lbrace (x,y)\mid -1\le x\le 1,\ y=1\rbrace}_{C_2}$

            > > $\vec{C}=\big\lbrace \underbrace{(t,t^2)}_{\gamma_1(t)}\mid t\in[-1,1]\big\rbrace\cup\big\lbrace \underbrace{(-t,1)}_{\gamma_2(t)}\mid t\in[-1,1]\big\rbrace$

            $$
            \begin{aligned}
            \int_{\vec{C}}\vec{F}\cdot d\vec{s}&=\int_{\vec{C}_1}\vec{F}\cdot d\vec{s}+\int_{\vec{C}_2}\vec{F}\cdot d\vec{s}\\
            &=\int_{-1}^1\begin{bmatrix} -t^4 \\ t^3 \end{bmatrix}\cdot\begin{bmatrix} 1 \\ 2t \end{bmatrix}dt+\int_{-1}^1\begin{bmatrix} -1 \\ -t \end{bmatrix}\cdot\begin{bmatrix} -1 \\ 0 \end{bmatrix}dt\\
            &=\int_{-1}^1(-t^4+2t^4)\,dt+\int_{-1}^1(1+0)\,dt=\frac25+2=\frac{12}5
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $$
            \begin{aligned}
            \iint_D\bigg(\underbrace{\frac{\partial Q}{\partial x}(x,y)}_{y}-\underbrace{\frac{\partial P}{\partial y}(x,y)}_{-2y}\bigg)dxdy&=\iint_D(3y)\,dxdy\\
            &=3\int_{-1}^1\left(\int_{x^2}^1y\,dy\right)dx=3\int_{-1}^1\left(\frac12-\frac{x^4}2\right)dx\\
            &=3\left(\frac x2-\frac{x^5}{10}\right)\bigg|_{x=-1}^{x=1}=3\left(\frac22-\frac2{10}\right)=3\cdot\frac45
            \end{aligned}
            $$
            """,
            lk.interactive(_fig, controls=[tc]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(along, beside, lk, np, plane):
    # module: Green's theorem
    # proof: Green
    # D as a y-simple region. Its boundary, run counter-clockwise: the graph y = phi_1(x) (red) to the right, the side x = b
    # (blue) upwards, the graph y = phi_2(x) (orange) to the left, the side x = a (blue) downwards
    _s = np.linspace(1.3, 3.8, 200)
    _lo, _hi = 0.9 + 0.18 * np.sin(4 * _s - 2.4), 2.3 + 0.2 * np.sin(3 * _s - 1.8)
    _fy, _ay = plane((-0.6, 5.5), (-0.5, 3.6), 4.2)
    _ay.fill_between(_s, _lo, _hi, color=lk.LIGHT, lw=0, zorder=0)
    _ay.plot(_s, _lo, color=lk.RED, lw=1.8)
    _ay.plot(_s, _hi, color=lk.ORANGE, lw=1.8)
    along(_ay, _s, _lo, lk.RED)
    along(_ay, _s[::-1], _hi[::-1], lk.ORANGE)
    for _e, _d in ((0, -1), (-1, 1)):
        _v = np.linspace(_lo[_e], _hi[_e], 60)[::_d]
        _ay.plot(_s[_e] + 0 * _v, _v, color=lk.BLUE, lw=1.8)
        along(_ay, _s[_e] + 0 * _v, _v, lk.BLUE, at=(0.6,))
    beside(_ay, (_s[100], _lo.min()), -90, r"$y = \varphi_1(x)$", lk.RED, 72, 16, gap=6)
    beside(_ay, (_s[100], _hi.max()), 90, r"$y = \varphi_2(x)$", lk.ORANGE, 72, 16, gap=6)
    beside(_ay, (_s[0], (_lo[0] + _hi[0]) / 2), 180, "$x = a$", lk.BLUE, 38, 16, gap=6)
    beside(_ay, (_s[-1], (_lo[-1] + _hi[-1]) / 2), 0, "$x = b$", lk.BLUE, 38, 16, gap=6)
    # D as an x-simple region. Its boundary, run counter-clockwise: the side y = c (blue) to the right, the curve
    # x = psi_2(y) (orange) upwards, the side y = d (blue) to the left, the curve x = psi_1(y) (red) downwards
    _u = np.linspace(0.9, 3.0, 200)
    _l, _r = 2.1 + 0.18 * np.sin(4 * _u - 1.2), 3.5 + 0.2 * np.sin(3 * _u - 0.9)
    _fx, _ax = plane((-0.6, 5.9), (-0.5, 3.9), 4.2)
    _ax.fill_betweenx(_u, _l, _r, color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot(_l, _u, color=lk.RED, lw=1.8)
    _ax.plot(_r, _u, color=lk.ORANGE, lw=1.8)
    along(_ax, _l[::-1], _u[::-1], lk.RED)
    along(_ax, _r, _u, lk.ORANGE)
    for _e, _d in ((0, 1), (-1, -1)):
        _w = np.linspace(_l[_e], _r[_e], 60)[::_d]
        _ax.plot(_w, _u[_e] + 0 * _w, color=lk.BLUE, lw=1.8)
        along(_ax, _w, _u[_e] + 0 * _w, lk.BLUE, at=(0.6,))
    beside(_ax, (_l[100], _u[100]), 180, r"$x = \psi_1(y)$", lk.RED, 72, 16, gap=6)
    beside(_ax, (_r[100], _u[100]), 0, r"$x = \psi_2(y)$", lk.ORANGE, 72, 16, gap=6)
    beside(_ax, ((_l[0] + _r[0]) / 2, _u[0]), -90, "$y = c$", lk.BLUE, 38, 16, gap=6)
    beside(_ax, ((_l[-1] + _r[-1]) / 2, _u[-1]), 90, "$y = d$", lk.BLUE, 38, 16, gap=6)
    lk.proof(
        [
            r"""
            Write &nbsp; $\vec{F}(x,y)=\begin{bmatrix} P(x,y) \\ Q(x,y) \end{bmatrix}=\underbrace{\begin{bmatrix} P(x,y) \\ 0 \end{bmatrix}}_{\vec{F}_1(x,y)}+\underbrace{\begin{bmatrix} 0 \\ Q(x,y) \end{bmatrix}}_{\vec{F}_2(x,y)}$

            > $\Longrightarrow$ &nbsp; $\displaystyle\int_{\vec{C}}\vec{F}\cdot d\vec{s}=\int_{\vec{C}}\vec{F}_1\cdot d\vec{s}+\int_{\vec{C}}\vec{F}_2\cdot d\vec{s}$
            """,
            lk.gap(),
            r"""
            For $\vec{F}_1=\begin{bmatrix} P \\ 0 \end{bmatrix}$, &nbsp; treat $D$ as $y$-simple region

            > $D=\lbrace (x,y)\mid a\le x\le b,\ \varphi_1(x)\le y\le\varphi_2(x)\rbrace$

            > > $\Longrightarrow$ &nbsp; $\mathrm{Bd}(D)=\lbrace (x,\varphi_1(x))\mid x\in[a,b]\rbrace\cup\lbrace (b,y)\mid y\in[\varphi_1(b),\varphi_2(b)]\rbrace$

            > > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\mathrm{Bd}(D)=$</span>$\cup\lbrace (x,\varphi_2(x))\mid x\in[a,b]\rbrace\cup\lbrace (a,y)\mid y\in[\varphi_1(a),\varphi_2(a)]\rbrace$
            """,
            lk.figure(_fy),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \Longrightarrow\quad\int_{\vec{C}}\vec{F}_1\cdot d\vec{s}&=\int_a^b\begin{bmatrix} P(t,\varphi_1(t)) \\ 0 \end{bmatrix}\cdot\mk{\begin{bmatrix} 1 \\ \varphi_1'(t) \end{bmatrix}}dt+\int_{\varphi_1(b)}^{\varphi_2(b)}\begin{bmatrix} P(b,t) \\ 0 \end{bmatrix}\cdot\begin{bmatrix} 0 \\ 1 \end{bmatrix}dt\\
                &\quad-\int_a^b\begin{bmatrix} P(t,\varphi_2(t)) \\ 0 \end{bmatrix}\cdot\mk{\begin{bmatrix} 1 \\ \varphi_2'(t) \end{bmatrix}}dt\mathbin{\mk{-}}\int_{\varphi_1(a)}^{\varphi_2(a)}\begin{bmatrix} P(a,t) \\ 0 \end{bmatrix}\cdot\begin{bmatrix} 0 \\ 1 \end{bmatrix}dt
                \end{aligned}
                $$
                """,
                [
                    (1, r"here we need $\varphi_1,\varphi_2$ differentiable"),
                    (2, r"parameterization has opposite orientation"),
                ],
                rows=2,
            ),
            r"""
            $$
            \begin{aligned}
            \Longrightarrow\quad\int_{\vec{C}}\vec{F}_1\cdot d\vec{s}&=\int_a^b\big(P(x,\varphi_1(x))-P(x,\varphi_2(x))\big)\,dx\\
            &=\int_a^b\left(\int_{\varphi_2(x)}^{\varphi_1(x)}\frac{\partial P}{\partial y}(x,y)\,dy\right)dx\\
            &=-\int_a^b\left(\int_{\varphi_1(x)}^{\varphi_2(x)}\frac{\partial P}{\partial y}(x,y)\,dy\right)dx=-\iint_D\frac{\partial P}{\partial y}(x,y)\,dxdy
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            Similarly, for $\vec{F}_2=\begin{bmatrix} 0 \\ Q \end{bmatrix}$, &nbsp; treat $D$ as $x$-simple

            > $D=\lbrace (x,y)\mid c\le y\le d,\ \psi_1(y)\le x\le\psi_2(y)\rbrace$

            > > $\Longrightarrow$ &nbsp; $\mathrm{Bd}(D)=\lbrace (x,c)\mid x\in[\psi_1(c),\psi_2(c)]\rbrace\cup\lbrace (\psi_2(y),y)\mid y\in[c,d]\rbrace$

            > > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $\mathrm{Bd}(D)=$</span>$\cup\lbrace (x,d)\mid x\in[\psi_1(d),\psi_2(d)]\rbrace\cup\lbrace (\psi_1(y),y)\mid y\in[c,d]\rbrace$
            """,
            lk.figure(_fx),
            r"""
            $$
            \begin{aligned}
            \Longrightarrow\quad\int_{\vec{C}}\vec{F}_2\cdot d\vec{s}&=\int_c^d\big(Q(\psi_2(y),y)-Q(\psi_1(y),y)\big)\,dy\\
            &=\int_c^d\left(\int_{\psi_1(y)}^{\psi_2(y)}\frac{\partial Q}{\partial x}(x,y)\,dx\right)dy=\iint_D\frac{\partial Q}{\partial x}(x,y)\,dxdy
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $$
            \Longrightarrow\quad\int_{\vec{C}}\vec{F}\cdot d\vec{s}=\int_{\vec{C}}(\vec{F}_1+\vec{F}_2)\cdot d\vec{s}=\iint_D\left(\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)\right)dxdy
            $$
            """,
        ],
        of="thm-green",
    )
    return


@app.cell(hide_code=True)
def _(beside, lk, np, plane):
    # module: Green's theorem
    # example: ellipse
    # the region D inside the ellipse, which crosses the x axis at -a and a and the y axis at -b and b
    _a, _b = 1.7, 1.05
    _s = np.linspace(0, 2 * np.pi, 300)
    _fig, _ax = plane((-2.6, 2.9), (-1.7, 2.0), 4.2)
    _ax.fill(_a * np.cos(_s), _b * np.sin(_s), color=lk.LIGHT, lw=0, zorder=0)
    _ax.plot(_a * np.cos(_s), _b * np.sin(_s), color=lk.BLUE, lw=1.8)
    for _p, _angle, _name in (((-_a, 0), -135, "$-a$"), ((_a, 0), -45, "$a$"), ((0, -_b), -135, "$-b$"), ((0, _b), 135, "$b$")):
        _ax.plot(*_p, "o", color="black", ms=4, zorder=6)
        beside(_ax, _p, _angle, _name, "black", 22 if "-" in _name else 10, 14, gap=3)
    _ax.text(0.85, 0.42, "$D$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=1)
    lk.example(
        [
            r"""
            $D=\left\lbrace (x,y)\;\middle|\;\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le1\right\rbrace$ &nbsp; $\leadsto$ &nbsp; inside an ellipse
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \iint_D1\,dxdy&=\ ?\\
                &=\int_{-a}^a\left(\int_{-b\sqrt{1-x^2/a^2}}^{b\sqrt{1-x^2/a^2}}1\,dy\right)dx\\
                &=\int_{-a}^a2b\sqrt{1-x^2/a^2}\,dx=\ \dots\ \text{trig. substitution}\\
                &=\iint_D\bigg(\underbrace{\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)}_{\footnotesize=1\text{ for some }\vec{F}=\left[\begin{smallmatrix}P\\Q\end{smallmatrix}\right]}\bigg)dxdy
                \end{aligned}
                $$
                """,
                "might make life easier!",
                at="last",
            ),
            lk.gap(),
            r"""
            Consider &nbsp; $\vec{F}(x,y)={\large\tfrac12}\begin{bmatrix} -y \\ x \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $\dfrac{\partial Q}{\partial x}-\dfrac{\partial P}{\partial y}=\dfrac12(1+1)=1$

            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \Longrightarrow\quad\iint_D1\,dxdy&=\int_{\mk{\vec{C}}}\vec{F}\cdot d\vec{s}\\
                &=\int_0^{2\pi}\frac12\begin{bmatrix} -b\sin(t) \\ a\cos(t) \end{bmatrix}\cdot\begin{bmatrix} -a\sin(t) \\ b\cos(t) \end{bmatrix}dt\\
                &=\frac12\int_0^{2\pi}ab\,dt=ab\pi
                \end{aligned}
                $$
                """,
                [(1, r"$\gamma(t)=\begin{bmatrix} a\cos(t) \\ b\sin(t) \end{bmatrix}$, $t\in[0,2\pi]$")],
                rows=3,
            ),
            r"""
            $\leadsto$ &nbsp; if $a=b=r$ &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle\iint_D dxdy=r^2\pi$
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # lead-in
    lk.prose(r"$\leadsto$ &nbsp; consequence for gradient vector fields")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # corollary: zero scalar curl
    lk.corollary(
        r"""
        Given a vector field $\vec{F}(x,y)=\begin{bmatrix} P(x,y) \\ Q(x,y) \end{bmatrix}$, &nbsp; $C^1$-smooth over the whole plane $\mathbb{R}^2$ and with zero scalar curl

        $$
        \frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)=0
        $$

        then $\vec{F}(x,y)$ is a conservative vector field with potential function

        $$
        f(x,y)=\int_0^xP(t,0)\,dt+\int_0^yQ(x,t)\,dt
        $$
        """,
        label="cor-potential",
    )
    return


@app.cell(hide_code=True)
def _(along, beside, lk, np, plane):
    # module: conservative fields
    # proof: zero scalar curl
    # the rectangle R = [0, x] x [0, y] and its boundary: C_1 (red) from (0, 0) along the bottom side to (x, 0) and up the
    # right side to (x, y); C_2 (orange) from (x, y) along the top side to (0, y) and down the left side to (0, 0)
    _x, _y = 2.7, 1.7
    _fig, _ax = plane((-1.1, 4.2), (-0.8, 2.9), 4.2)
    _ax.fill([0, _x, _x, 0], [0, 0, _y, _y], color=lk.LIGHT, lw=0, zorder=0)
    _u = np.linspace(0, 1, 60)
    for _p, _q, _c in (((0, 0), (_x, 0), lk.RED), ((_x, 0), (_x, _y), lk.RED), ((_x, _y), (0, _y), lk.ORANGE), ((0, _y), (0, 0), lk.ORANGE)):
        _ax.plot([_p[0], _q[0]], [_p[1], _q[1]], color=_c, lw=1.8, zorder=4)
        along(_ax, _p[0] + (_q[0] - _p[0]) * _u, _p[1] + (_q[1] - _p[1]) * _u, _c, at=(0.6,))
    for _p, _angle, _name in (((0, 0), -135, "$(0, 0)$"), ((_x, 0), -90, "$(x, 0)$"), ((_x, _y), 45, "$(x, y)$"), ((0, _y), 180, "$(0, y)$")):
        _ax.plot(*_p, "o", color="black", ms=4, zorder=6)
        beside(_ax, _p, _angle, _name, "black", 36, 16, gap=11 if _angle == -135 else 4)
    _ax.text(_x / 2, _y / 2, "$R$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x, _y / 2), 0, r"$\vec{C}_1$", lk.RED, 16, 18, gap=6)
    beside(_ax, (_x / 2, _y), 90, r"$\vec{C}_2$", lk.ORANGE, 16, 18, gap=6)
    lk.proof(
        [
            r"Consider a rectangle $R=[0,x]\times[0,y]$",
            lk.figure(_fig),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \text{Green}\quad\Longrightarrow\quad\int_{\mk{\vec{C}}}\vec{F}\cdot d\vec{s}&=\iint_R\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dxdy\\
                &=0=\int_{\vec{C}_1}\vec{F}\cdot d\vec{s}+\int_{\vec{C}_2}\vec{F}\cdot d\vec{s}
                \end{aligned}
                $$
                """,
                [(1, r"$\vec{C}=\mathrm{Bd}(R)=\vec{C}_1\cup\vec{C}_2$")],
                rows=2,
            ),
            r"""
            $$
            \begin{aligned}
            \int_{\vec{C}_1}\vec{F}\cdot d\vec{s}&=\int_0^x\begin{bmatrix} P(t,0) \\ Q(t,0) \end{bmatrix}\cdot\begin{bmatrix} 1 \\ 0 \end{bmatrix}dt+\int_0^y\begin{bmatrix} P(x,t) \\ Q(x,t) \end{bmatrix}\cdot\begin{bmatrix} 0 \\ 1 \end{bmatrix}dt\\
            &=\int_0^xP(t,0)\,dt+\int_0^yQ(x,t)\,dt=f(x,y)\\[10pt]
            \int_{\vec{C}_2}\vec{F}\cdot d\vec{s}&=-\int_0^y\begin{bmatrix} P(0,t) \\ Q(0,t) \end{bmatrix}\cdot\begin{bmatrix} 0 \\ 1 \end{bmatrix}dt-\int_0^x\begin{bmatrix} P(t,y) \\ Q(t,y) \end{bmatrix}\cdot\begin{bmatrix} 1 \\ 0 \end{bmatrix}dt\\
            &=-\int_0^yQ(0,t)\,dt-\int_0^xP(t,y)\,dt=-f(x,y)
            \end{aligned}
            $$

            $$
            \leadsto\quad\text{FTC}:\quad\frac{\partial}{\partial x}f(x,y)=P(x,y)\quad\text{and}\quad\frac{\partial}{\partial y}f(x,y)=Q(x,y)
            $$
            """,
        ],
        of="cor-potential",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # example: potential function
    lk.example(
        [
            lk.aside(
                r"$\mk{\vec{F}(x,y)=\begin{bmatrix} 2xy \\ x^2+3y^2 \end{bmatrix}}$ &nbsp; $\leadsto$ &nbsp; $\dfrac{\partial Q}{\partial x}(x,y)-\dfrac{\partial P}{\partial y}(x,y)=2x-2x=0$",
                r"$C^1$-smooth everywhere!",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $\vec{F}(x,y)=\vec{\nabla}f(x,y)$ for

            $$
            \begin{aligned}
            f(x,y)&=\int_0^xP(t,0)\,dt+\int_0^yQ(x,t)\,dt\\
            &=\int_0^x2t\cdot0\,dt+\int_0^y(x^2+3t^2)\,dt=x^2y+y^3\\
            \llap{\text{or}\qquad}&=\int_0^yQ(0,t)\,dt+\int_0^xP(t,y)\,dt\\
            &=\int_0^y(0+3t^2)\,dt+\int_0^x2ty\,dt=y^3+x^2y
            \end{aligned}
            $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # remark: not a gradient
    lk.remark(
        r"""
        $\vec{H}(x,y)=\underbrace{\dfrac1{x^2+y^2}}_{\mathclap{\footnotesize\text{not }C^1\text{-smooth at }(0,0)}}\begin{bmatrix} -y \\ x \end{bmatrix}$ &nbsp; has zero scalar curl but is not a gradient!

        > $\Longrightarrow$ &nbsp; Green's theorem does not apply!
        """
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
    # exercise: triangle
    lk.exercise(
        r"""
        $D$ triangle with corners $(0,0)$, $(2,0)$, $(1,1)$

        a) parameterize $\mathrm{Bd}(D)$ with positive orientation

        b) compute line integral of

        $$
        \vec{F}(x,y)=\begin{bmatrix} y^2 \\ 3xy \end{bmatrix}\quad\text{over }\mathrm{Bd}(D)
        $$

        c) compute $\displaystyle\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dxdy$ with Fubini's theorem
        """,
        label="ex-triangle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: potential
    lk.exercise(
        r"""
        Let

        $$
        \vec{G}(x,y)=\begin{bmatrix} e^y \\ xe^y+2y \end{bmatrix}
        $$

        a) check that the scalar curl is zero

        b) compute a potential function for $\vec{G}(x,y)$
        """,
        label="ex-potential",
    )
    return


if __name__ == "__main__":
    app.run()
