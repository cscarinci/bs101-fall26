import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 1 · The Cartesian n-space", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, mo


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(1, "The Cartesian $n$-space")
    return


@app.cell(hide_code=True)
def _(Figure, lk, mo):
    # Helpers of this lecture: the spaces R^1, R^2, R^3 with a point or an arrow, coordinate planes, and
    # labelled vectors from the origin

    def column(ax, x, y, entries, color, dy=0.3, w=0.2):
        """A column vector drawn at (x, y): stacked entries between two square brackets."""
        n = len(entries)
        top, bot = y + dy * n / 2, y - dy * n / 2
        for k, e in enumerate(entries):
            ax.text(x, top - dy * (k + 0.5), e, color=color, fontsize=13, ha="center", va="center")
        for s in (-1, 1):
            ax.plot([x + s * (w - 0.07), x + s * w, x + s * w, x + s * (w - 0.07)], [top, top, bot, bot], color=color, lw=0.9)

    def spaces(arrows):
        """R^1 and R^2 (drawn flat) beside R^3 (a rotatable view), with a point (arrows=False) or the arrow from
        the origin to it (arrows=True)."""
        fig = Figure(figsize=(4.6, 3.1 if not arrows else 2.5), layout="constrained")
        a1, a2 = fig.subplots(1, 2)
        lo = -1.25 if not arrows else -0.6
        for ax in (a1, a2):
            ax.set_xlim(-0.5, 2.9)
            ax.set_ylim(lo, 2.75)
            ax.set_aspect("equal")
            ax.axis("off")

        # n = 1
        lk.arrow(a1, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        a1.text(2.6, 0, r"$x$" if arrows else r"$\mathbb{R}$", fontsize=14, va="center")
        if arrows:
            lk.arrow(a1, (0, 0), (1.4, 0), lk.BLUE)
            a1.text(0.7, 0.14, "$x$", color=lk.BLUE, fontsize=14, ha="center")
        a1.plot(0, 0, "o", color="black", ms=5, zorder=4)
        a1.plot(1.4, 0, "o", color=lk.BLUE, ms=5, zorder=4)
        a1.text(0, -0.16, "$0$", fontsize=14, ha="center", va="top")
        a1.text(1.4, -0.16, "$x$", fontsize=14, ha="center", va="top")

        # n = 2
        p = (1.4, 1.5)
        lk.arrow(a2, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        lk.arrow(a2, (0, -0.5), (0, 2.4), "black", lw=0.9)
        # points: the axes are copies of R; arrows (n-vectors): the axes are the components x^1, x^2
        a2.text(2.6, 0, r"$x^1$" if arrows else r"$\mathbb{R}$", fontsize=14, va="center")
        a2.text(0, 2.48, r"$x^2$" if arrows else r"$\mathbb{R}$", fontsize=14, ha="center", va="bottom")
        a2.text(0.08, -0.12, "$(0, 0)$", fontsize=13, ha="left", va="top")
        if arrows:
            lk.arrow(a2, (0, 0), p, lk.BLUE)
            column(a2, 1.3, 0.62, ("$x^1$", "$x^2$"), lk.BLUE)
            a2.text(p[0] + 0.1, p[1] + 0.06, "$(x^1, x^2)$", fontsize=13, ha="left", va="bottom")
        else:
            a2.plot([p[0], p[0], 0], [0, p[1], p[1]], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
            a2.text(p[0] + 0.12, -0.12, "$x^1$", fontsize=14, ha="left", va="top")
            a2.text(-0.12, p[1], "$x^2$", fontsize=14, ha="right", va="center")
            a2.text(p[0] + 0.1, p[1] + 0.06, r"$\vec{x} = (x^1, x^2)$", fontsize=13, ha="left", va="bottom")
        a2.plot(0, 0, "o", color="black", ms=5, zorder=4)
        a2.plot(*p, "o", color=lk.BLUE, ms=5, zorder=4)

        if not arrows:
            for ax, n, name in ((a1, 1, "the real line"), (a2, 2, "the real plane")):
                ax.text(1.2, -0.72, f"$n = {n}$\n{name}", fontsize=14, ha="center", va="top", linespacing=1.4)

        # n = 3
        q = (1.0, 1.8, 1.6)
        names = ("x^1", "x^2", "x^3") if arrows else (r"\mathbb{R}",) * 3
        axes = [((0 if arrows else -0.5, 0, 0), (2.1, 0, 0), names[0], -150), ((0, -0.4, 0), (0, 2.3, 0), names[1], 0), ((0, 0, -0.4), (0, 0, 2.1), names[2], 90)]
        dots = [((0, 0, 0), "#000000"), (q, lk.BLUE)]
        origin = ((0, 0, 0), "(0, 0, 0)", "#000000", -60, 12)
        if arrows:
            space = lk.panel(
                1.0,
                arrows=[((0, 0, 0), q, lk.BLUE)],
                points=dots,
                axes=axes,
                texts=[origin, (q, "(x^1, x^2, x^3)", "#000000", 30, 7), (tuple(0.7 * c for c in q), r"\begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix}", lk.BLUE, 150, 14)],
            )
            alt = "the arrow from the origin to the point (x1, x2, x3) in R3, written as a column vector"
        else:
            floor = (q[0], q[1], 0)
            guides = [(q, floor), (floor, (q[0], 0, 0)), (floor, (0, q[1], 0)), (q, (0, 0, q[2]))]
            space = lk.panel(
                1.0,
                lines=[([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], lk.GREY, 1.0, [4, 3]) for a, b in guides],
                points=dots,
                axes=axes,
                texts=[origin, (q, r"\vec{x} = (x^1, x^2, x^3)", "#000000", 30, 7), ((q[0], 0, 0), "x^1", "#000000", 150), ((0, q[1], 0), "x^2", "#000000", 60), ((0, 0, q[2]), "x^3", "#000000", 180)],
                caption=r"\begin{gathered} n = 3 \\ \text{the real space} \end{gathered}",
            )
            alt = "the real space R3: three axes through the origin and a point x = (x1, x2, x3), with dashed lines to its coordinates on the axes"
        view = lk.turntable(30, 22, alt, [space], height=300)
        return mo.Html(
            '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem 1rem;">'
            f'<div style="flex: 1.4 1 360px; min-width: 260px;">{mo.as_html(fig).text}</div>'
            f'<div style="flex: 1 1 280px; min-width: 240px;">{view.text}</div></div>'
        )

    def plane(ax, lim, ticks):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=lk.LIGHT, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_xticks(ticks, [f"${k}$" for k in ticks])
        ax.set_yticks(ticks, [f"${k}$" for k in ticks])

    def vector(ax, tip, color, name, away=None):
        """Arrow from the origin (a dot when the vector is zero), named beside its tip: beyond the tip, or to the
        side of the arrow away from the vector `away` (no box behind the name)."""
        if tip[0] == 0 and tip[1] == 0:
            ax.plot(0, 0, "o", color=color, ms=4, zorder=4)
        else:
            lk.arrow(ax, (0, 0), tip, color)
        d = tip if away is None else (-tip[1], tip[0])
        if away is not None and d[0] * away[0] + d[1] * away[1] > 0:
            d = (-d[0], -d[1])
        r = (d[0] ** 2 + d[1] ** 2) ** 0.5
        d = (d[0] / r, d[1] / r) if r else (0.7, 0.7)
        ax.annotate(name, tip, textcoords="offset points", xytext=(9 * d[0], 9 * d[1]), color=color, fontsize=13,
                    ha="left" if d[0] > 0.3 else "right" if d[0] < -0.3 else "center", va="bottom" if d[1] > 0.3 else "top" if d[1] < -0.3 else "center", zorder=5)

    return plane, spaces, vector


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure of the two operations.
    x1 = lk.slider(-4, 4, step=0.5, value=3, label="$x^1$")
    x2 = lk.slider(-4, 4, step=0.5, value=1, label="$x^2$")
    y1 = lk.slider(-4, 4, step=0.5, value=1, label="$y^1$")
    y2 = lk.slider(-4, 4, step=0.5, value=2.5, label="$y^2$")
    alpha = lk.slider(-2, 2, step=0.25, value=2, label=r"$\alpha$")
    return alpha, x1, x2, y1, y2


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # references
    lk.references("MT 1.1, 1.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # recall: the two operations on R
    lk.recall(
        [
            lk.aside(r"$\mk{\mathbb{R}}$ has two algebraic operations", r"$\mathbb{R}$ = line of real numbers"),
            r"""
            $$
            \begin{array}{cc}
            {+} : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R} & \qquad \cdot : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}\\
            \phantom{+ :} (\alpha, \beta) \longmapsto \alpha + \beta & \qquad \phantom{\cdot :} (\alpha, \beta) \longmapsto \alpha \cdot \beta\\[4pt]
            \text{addition} & \qquad \text{multiplication}
            \end{array}
            $$
            """,
            r"$\leadsto$ &nbsp; allow us to perform calculations with real numbers and real-valued functions and, eventually, allow us to define Calculus",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # motivation: the first goal
    lk.prose(r"$\leadsto$ &nbsp; our first goal is to extend these operations from real numbers to collections of real numbers")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # definition: the Cartesian n-space
    lk.definition(
        [
            lk.aside(r"For each $n \in \mk{\mathbb{Z}_{>0}} = \{1, 2, 3, \dots\}$, we define", r"$\mathbb{Z}_{>0}$ = positive integers"),
            r"the **Cartesian $n$-space** $\mathbb{R}^n$ as the set of all",
            lk.aside(r"<span class='lk-mark'>ordered lists of $n$ real numbers</span>", r"= $n$-tuples of real numbers"),
            r"$$ \mathbb{R}^n = \left\{\, \vec{x} = (x^1, x^2, \dots, x^n) \;\middle|\; x^i \in \mathbb{R}, \ \forall\, i = 1, 2, \dots, n \,\right\} $$",
        ],
        label="def-cartesian",
    )
    return


@app.cell(hide_code=True)
def _(lk, spaces):
    # module: Cartesian n-space
    # example: n = 1, 2, 3, with the sketch of the real line, plane and space
    lk.example(
        [
            lk.aside(r"$n = 1$ &nbsp; $\leadsto$ &nbsp; $\mathbb{R}^1 = \mathbb{R} \ni \mk{x} = (x^1)$ &nbsp; (list of a single number)", "no need for arrows here"),
            lk.aside(
                r"$n = 2$ &nbsp; $\leadsto$ &nbsp; $\mathbb{R}^2 = \mathbb{R} \times \mathbb{R} \ni \vec{x} = (x^1, x^2)$ &nbsp; (<span class='lk-mark'>ordered</span> pairs of numbers)",
                r"order matters!<br>$(x^1, x^2) \neq (x^2, x^1)$ unless $x^1 = x^2$",
            ),
            r"$n = 3$ &nbsp; $\leadsto$ &nbsp; $\mathbb{R}^3 \ni \vec{x} = (x^1, x^2, x^3)$ &nbsp; (ordered triples)",
            r"<span class='lk-ghost'>$n = 3$ &nbsp; $\leadsto$ &nbsp;</span>$\vdots$",
            lk.figure(spaces(False)),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # comments: points in n-space, and the need for another way to think about them
    lk.prose(
        r"$\leadsto$ &nbsp; geometrically, elements in $\mathbb{R}^n$ are points in an “$n$-dimensional” space with $n$ “orthogonal axes” intersecting at a single point (the origin)",
        r"$\leadsto$ &nbsp; to extend the operations $+$ and $\cdot$ to $\mathbb{R}^n$, we need yet another way to think about its elements!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # theorem: points as arrows from the origin
    lk.theorem(
        r"Every element $\vec{x} = (x^1, \dots, x^n) \in \mathbb{R}^n$ can be realized as a unique arrow from the origin $\vec{0} = (0, \dots, 0)$.",
        label="thm-arrows",
    )
    return


@app.cell(hide_code=True)
def _(lk, spaces):
    # module: Cartesian n-space
    # proof: the sketch of the arrows
    lk.proof(lk.figure(spaces(True)))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # n-vectors, and points versus arrows
    lk.prose(
        lk.aside(r"we will denote this arrow by an <span class='lk-mark'>**$n$-vector**</span>", r"= an $n \times 1$ array<br>= column matrix size $n$"),
        r"""
        $$
        \vec{x} = \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \in \mathrm{Mat}(\underset{\substack{\uparrow \\ \mathclap{n \text{ rows}}}}{n} \times \underset{\substack{\uparrow \\ \mathclap{1 \text{ column}}}}{1})
        $$
        """,
        r"$\leadsto$ &nbsp; in this course there is no fundamental difference between “points in space” and “arrows from the origin”",
        r"$\leadsto$ &nbsp; we can think of it as a change in perspective",
        r"$\leadsto$ &nbsp; when the distinction matters, we will use",
        r"""
        $$
        \begin{aligned}
        \vec{x} &= (x^1, \dots, x^n) && \text{for points and}\\[4pt]
        \vec{x} &= \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} && \text{for arrows from the origin}
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # definition: vector addition and scalar-vector multiplication
    lk.definition(
        [
            r"On $\mathbb{R}^n$ we can define two operations",
            r"""
            $$
            \begin{array}{ccc}
            {+} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n & \qquad \text{and} \qquad & \cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n\\[2pt]
            \text{vector addition} & & \text{scalar-vector multiplication}
            \end{array}
            $$
            """,
            "via",
            r"""
            $$
            \begin{array}{cc}
            \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} + \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} = \begin{bmatrix} x^1 + y^1 \\ x^2 + y^2 \\ \vdots \\ x^n + y^n \end{bmatrix} & \qquad \alpha \cdot \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \alpha x^2 \\ \vdots \\ \alpha x^n \end{bmatrix}\\[4pt]
            \text{componentwise addition} & \qquad \text{componentwise multiplication}
            \end{array}
            $$
            """,
        ],
        label="def-operations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # comments: scalars and n-vectors, and why n-vectors
    lk.prose(
        r"$\leadsto$ &nbsp; note that multiplication is defined between real numbers (**scalars**) and elements in $\mathbb{R}^n$ (**$n$-vectors**)",
        r"$\leadsto$ &nbsp; and the reason to use $n$-vectors (arrows from origin) here, instead of $n$-tuples (points in $n$-space), has to do with geometric interpretation",
    )
    return


@app.cell(hide_code=True)
def _(Figure, alpha, lk, plane, vector, x1, x2, y1, y2):
    # module: Cartesian n-space
    # figure: the parallelogram of x + y, and alpha x
    _x = (x1.value, x2.value)
    _y = (y1.value, y2.value)
    _s = (_x[0] + _y[0], _x[1] + _y[1])
    _ax_ = (alpha.value * _x[0], alpha.value * _x[1])

    _fig = Figure(figsize=(lk.FULL, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    # range 6 either way (the vectors fill the plane); wider only when a vector would leave it
    _far = max(abs(c) for v in (_x, _y, _s, _ax_) for c in v)
    _lim = max(7, int(_far) + 1)
    for _a in (_left, _right):
        plane(_a, _lim, range(-(_lim // 3) * 3, _lim + 1, 3))
    _left.plot([_x[0], _s[0], _y[0]], [_x[1], _s[1], _y[1]], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_left, _s, lk.GREEN, r"$\vec{x}+\vec{y}$")
    vector(_left, _x, lk.BLUE, r"$\vec{x}$", away=_y)
    vector(_left, _y, lk.RED, r"$\vec{y}$", away=_x)
    vector(_right, _ax_, lk.GREEN, r"$\alpha \cdot \vec{x}$")
    vector(_right, _x, lk.BLUE, r"$\vec{x}$", away=(_x[1], -_x[0]))

    lk.prose(lk.interactive(_fig, controls=[x1, x2, y1, y2, alpha]))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # comments: arrows, and the properties they carry
    lk.prose(
        r"$\leadsto$ &nbsp; we can interpret the operations in terms of arrows from the origin, not in terms of points",
        r"$\leadsto$ &nbsp; these carry most of the properties of the usual addition and multiplication in $\mathbb{R}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # theorem: properties of the operations
    lk.theorem(
        [
            r"For every $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and $\alpha, \beta \in \mathbb{R}$",
            r"""
            $$
            \begin{aligned}
            &\begin{array}{l} \bullet \ \ (\vec{x} + \vec{y}) + \vec{z} = \vec{x} + (\vec{y} + \vec{z}) \\[4pt] \bullet \ \ \alpha \cdot (\beta \cdot \vec{x}) = (\alpha \beta) \cdot \vec{x} \end{array} && (\text{associativity})\\[10pt]
            &\begin{array}{l} \bullet \ \ (\alpha + \beta) \cdot \vec{x} = \alpha \cdot \vec{x} + \beta \cdot \vec{x} \\[4pt] \bullet \ \ \alpha \cdot (\vec{x} + \vec{y}) = \alpha \cdot \vec{x} + \alpha \cdot \vec{y} \end{array} \qquad && (\text{distributivity})\\[10pt]
            &\begin{array}{l} \bullet \ \ \vec{x} + \vec{y} = \vec{y} + \vec{x} \end{array} && (\text{commutativity})\\[6pt]
            &\begin{array}{l} \bullet \ \ \vec{x} + \vec{0} = \vec{x}, \quad (1) \cdot \vec{x} = \vec{x} \end{array} && (\text{neutral operations})\\[6pt]
            &\begin{array}{l} \bullet \ \ 0 \cdot \vec{x} = \vec{0}, \quad \alpha \cdot \vec{0} = \vec{0} \end{array} && (\text{null operations})
            \end{aligned}
            $$
            """,
        ],
        label="thm-operations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian n-space
    # proof
    lk.proof("exercise!")
    return


if __name__ == "__main__":
    app.run()
