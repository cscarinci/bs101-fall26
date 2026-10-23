import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 01 · The Cartesian n-space", css_file="bs101.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#1b458f", "#b3261e", "#2e7d32", "#e65100", "#888888", "#cfe3f5"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS101 &bull; {running}</div>
      <div class="bs-title">Multivariable Calculus</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>BS101-04/05</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def proposition(body, title=""):
        return _statement("Proposition", title, body)

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def postulate(body, title=""):
        return _statement("Postulate", title, body)

    def note(body):
        """Editorial note of the notebook (not part of the lecture)."""
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        One head size and one line weight for every figure, so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>,head_width=0.15,head_length=0.35", "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        from matplotlib.figure import Figure as _Figure

        fig = _Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        import numpy as _np

        rng = _np.random.default_rng(seed)
        t = _np.linspace(0, 2 * _np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * _np.cos(k * t + rng.uniform(0, 2 * _np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * _np.cos(t), cy + ry * r * _np.sin(t)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 01", "Week 01", "Lecture 01 · The Cartesian n-space")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## I.1 &nbsp; The Cartesian $n$-space

    **References:** MT 1.1, 1.5

    ### Points in $n$-space

    **Recall:** $\mathbb{R}$ (the line of real numbers) has two algebraic operations

    | addition | multiplication |
    |:---:|:---:|
    | $+ : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}$ | $\cdot : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}$ |
    | $(\alpha, \beta) \longmapsto \alpha + \beta$ | $(\alpha, \beta) \longmapsto \alpha \cdot \beta$ |

    $\leadsto$ &nbsp; allow us to perform calculations with real numbers and real-valued functions and, eventually, allow us to define Calculus

    $\leadsto$ &nbsp; our first goal is to extend these operations from real numbers to collections of real numbers
    """
            ),
            definition(
                r"""
    For each $n \in \mathbb{Z}_{>0} = \{1, 2, 3, \dots\}$ (positive integers), we define the **Cartesian $n$-space** $\mathbb{R}^n$ as the set of all ordered lists of $n$ real numbers ($n$-tuples of real numbers)

    $$
    \mathbb{R}^n = \left\{\, \vec{x} = (x^1, x^2, \dots, x^n) \;\middle|\; x^i \in \mathbb{R},\ \forall\, i = 1, 2, \dots, n \,\right\}
    $$
    """,
                "Cartesian $n$-space",
            ),
            mo.md(
                r"""
    **Example.**

    | | | |
    |:--|:--|:--|
    | ${n = 1}$ | ${\mathbb{R}^1 = \mathbb{R} \ni x = (x^1)}$ | list of a single number (no need for arrows here) |
    | ${n = 2}$ | ${\mathbb{R}^2 = \mathbb{R} \times \mathbb{R} \ni \vec{x} = (x^1, x^2)}$ | ordered pairs of numbers (order matters! ${(x^1, x^2) \neq (x^2, x^1)}$ unless ${x^1 = x^2}$) |
    | ${n = 3}$ | ${\mathbb{R}^3 \ni \vec{x} = (x^1, x^2, x^3)}$ | ordered triples |
    | $\;\vdots$ | | |
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, arrow):
    def _pr(x1, x2, x3):
        """Oblique projection of R^3, as on the board: x^2 to the right, x^3 up, x^1 towards the viewer."""
        return x2 - 0.45 * x1, x3 - 0.4 * x1

    def _column(ax, x, y, entries, color, dy=0.3, w=0.2):
        """A column vector drawn by hand at (x, y): stacked entries between two square brackets."""
        n = len(entries)
        top, bot = y + dy * n / 2, y - dy * n / 2
        for k, e in enumerate(entries):
            ax.text(x, top - dy * (k + 0.5), e, color=color, fontsize=11, ha="center", va="center")
        for s in (-1, 1):
            ax.plot([x + s * (w - 0.07), x + s * w, x + s * w, x + s * (w - 0.07)], [top, top, bot, bot], color=color, lw=0.9)

    def spaces_figure(arrows):
        """R^1, R^2, R^3 with a point (arrows=False) or the arrow from the origin to it (arrows=True)."""
        fig = Figure(figsize=(FULL, 2.9 if not arrows else 2.4), layout="constrained")
        a1, a2, a3 = fig.subplots(1, 3, width_ratios=[1, 1, 1.25])
        lo = -1.25 if not arrows else -1.05
        for ax, xlim in ((a1, (-0.5, 2.9)), (a2, (-0.5, 2.9)), (a3, (-1.3, 2.95))):
            ax.set_xlim(*xlim)
            ax.set_ylim(lo, 2.75)
            ax.set_aspect("equal")
            ax.axis("off")

        # n = 1
        arrow(a1, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        a1.text(2.6, 0, r"$\mathbb{R}$", fontsize=12, va="center")
        if arrows:
            arrow(a1, (0, 0), (1.4, 0), BLUE)
            a1.text(0.7, 0.14, "$x$", color=BLUE, fontsize=12, ha="center")
        a1.plot([0, 1.4], [0, 0], "o", color="black", ms=4, zorder=4)
        a1.text(0, -0.14, "$0$", fontsize=12, ha="center", va="top")
        a1.text(1.4, -0.14, "$x$", fontsize=12, ha="center", va="top")

        # n = 2
        p = (1.4, 1.5)
        arrow(a2, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        arrow(a2, (0, -0.5), (0, 2.4), "black", lw=0.9)
        a2.text(2.6, 0, r"$\mathbb{R}$", fontsize=12, va="center")
        a2.text(0, 2.48, r"$\mathbb{R}$", fontsize=12, ha="center", va="bottom")
        if arrows:
            arrow(a2, (0, 0), p, BLUE)
            _column(a2, 1.3, 0.62, ("$x^1$", "$x^2$"), BLUE)
            a2.text(p[0] + 0.1, p[1] + 0.08, r"$(x^1, x^2)$", fontsize=12, ha="left", va="bottom")
        else:
            a2.plot([p[0], p[0], 0], [0, p[1], p[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
            a2.text(p[0], -0.14, "$x^1$", fontsize=12, ha="center", va="top")
            a2.text(-0.12, p[1], "$x^2$", fontsize=12, ha="right", va="center")
            a2.text(p[0] + 0.1, p[1] + 0.08, r"$\vec{x} = (x^1, x^2)$", fontsize=12, ha="center", va="bottom")
        a2.plot([0, p[0]], [0, p[1]], "o", color="black", ms=4, zorder=4)
        a2.text(0.1, -0.14, "$(0,0)$", fontsize=11, ha="left", va="top")

        # n = 3
        q = (1.0, 1.9, 1.9)
        Q = _pr(*q)
        arrow(a3, (0, 0) if arrows else _pr(-0.6, 0, 0), _pr(2.3, 0, 0), "black", lw=0.9)
        arrow(a3, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        arrow(a3, (0, -0.5), (0, 2.4), "black", lw=0.9)
        a3.text(2.6, 0, r"$\mathbb{R}$", fontsize=12, va="center")
        a3.text(0, 2.48, r"$\mathbb{R}$", fontsize=12, ha="center", va="bottom")
        _e = _pr(2.3, 0, 0)
        a3.text(_e[0] - 0.08, _e[1] + 0.02, r"$\mathbb{R}$", fontsize=12, ha="right", va="bottom")
        if arrows:
            arrow(a3, (0, 0), Q, BLUE)
            _column(a3, 1.6, 0.72, ("$x^1$", "$x^2$", "$x^3$"), BLUE)
            a3.text(Q[0] + 0.1, Q[1] + 0.08, r"$(x^1, x^2, x^3)$", fontsize=12, ha="center", va="bottom")
        else:
            _floor = _pr(q[0], q[1], 0)
            for _a, _b in ((Q, _floor), (_floor, _pr(q[0], 0, 0)), (_floor, _pr(0, q[1], 0)), (Q, _pr(0, 0, q[2]))):
                a3.plot([_a[0], _b[0]], [_a[1], _b[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
            _x1 = _pr(q[0], 0, 0)
            a3.text(_x1[0] - 0.1, _x1[1] + 0.06, "$x^1$", fontsize=12, ha="right", va="bottom")
            a3.text(q[1] + 0.08, 0.1, "$x^2$", fontsize=12, ha="left", va="bottom")
            a3.text(-0.12, q[2] + 0.05, "$x^3$", fontsize=12, ha="right", va="center")
            a3.text(Q[0] + 0.3, Q[1] + 0.22, r"$\vec{x} = (x^1, x^2, x^3)$", fontsize=12, ha="center", va="bottom")
        a3.plot([0, Q[0]], [0, Q[1]], "o", color="black", ms=4, zorder=4)
        a3.text(0.1, -0.1, "$(0,0,0)$", fontsize=11, ha="left", va="top")

        if not arrows:
            for ax, n, name in ((a1, 1, "the real line"), (a2, 2, "the real plane"), (a3, 3, "the real space")):
                x0, x1 = ax.get_xlim()
                ax.text((x0 + x1) / 2, -0.72, f"$n = {n}$\n{name}", fontsize=12, ha="center", va="top", linespacing=1.4)
        return fig

    return (spaces_figure,)


@app.cell(hide_code=True)
def _(mo, spaces_figure):
    mo.vstack(
        [
            spaces_figure(False),
            mo.md(
                r"""
    $\leadsto$ &nbsp; geometrically, elements in $\mathbb{R}^n$ are points in an “$n$-dimensional” space with $n$ “orthogonal axes” intersecting at a single point (the origin)

    $\leadsto$ &nbsp; to extend the operations $+$ and $\cdot$ to $\mathbb{R}^n$, we need yet another way to think about its elements!

    ### Arrows from the origin
    """
            ),
            mo.md(
                r"""
    **Remark.** Every element $\vec{x} = (x^1, \dots, x^n) \in \mathbb{R}^n$ can be realized as a unique arrow from the origin $\vec{0} = (0, \dots, 0)$.
    """
            ),
            spaces_figure(True),
            mo.md(
                r"""
    We will denote this arrow by an **$n$-vector** (an $n \times 1$ array, a column matrix of size $n$)

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \in \mathrm{Mat}(n \times 1)
    \qquad (n \text{ rows},\ 1 \text{ column})
    $$

    $\leadsto$ &nbsp; in this course there is no fundamental difference between “points in space” and “arrows from the origin”

    $\leadsto$ &nbsp; we can think of it as a change in perspective

    $\leadsto$ &nbsp; when the distinction matters, we will use

    $$
    \vec{x} = (x^1, \dots, x^n) \ \text{ for points} \qquad \text{and} \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \ \text{ for arrows from the origin}
    $$

    ### Vector addition and scalar–vector multiplication
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    On $\mathbb{R}^n$ we can define two operations

    $$
    {+} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n \quad (\text{vector addition})
    \qquad \text{and} \qquad
    \cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n \quad (\text{scalar–vector multiplication})
    $$

    via

    $$
    \underbrace{\begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} + \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} = \begin{bmatrix} x^1 + y^1 \\ x^2 + y^2 \\ \vdots \\ x^n + y^n \end{bmatrix}}_{\text{component-wise addition}}
    \qquad \qquad
    \underbrace{\alpha \cdot \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \alpha x^2 \\ \vdots \\ \alpha x^n \end{bmatrix}}_{\text{component-wise multiplication}}
    $$
    """,
                "Vector addition and scalar–vector multiplication",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; note that multiplication is defined between real numbers (**scalars**) and elements in $\mathbb{R}^n$ (**$n$-vectors**)

    $\leadsto$ &nbsp; and the reason to use $n$-vectors (arrows from origin) here, instead of $n$-tuples (points in $n$-space), has to do with geometric interpretation
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    x1 = mo.ui.slider(-4, 4, 0.5, value=3, label="$x^1$", show_value=True)
    x2 = mo.ui.slider(-4, 4, 0.5, value=1, label="$x^2$", show_value=True)
    y1 = mo.ui.slider(-4, 4, 0.5, value=1, label="$y^1$", show_value=True)
    y2 = mo.ui.slider(-4, 4, 0.5, value=2.5, label="$y^2$", show_value=True)
    alpha = mo.ui.slider(-2, 2, 0.25, value=2, label=r"$\alpha$", show_value=True)
    return alpha, x1, x2, y1, y2


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, RED, alpha, arrow, math, mo, plane, table, x1, x2, y1, y2):
    _x = (x1.value, x2.value)
    _y = (y1.value, y2.value)
    _s = (_x[0] + _y[0], _x[1] + _y[1])
    _a = alpha.value
    _ax_ = (_a * _x[0], _a * _x[1])

    def _vector(ax, tip, color, label, turn, r=15):
        """Arrow from the origin (a dot when the vector is zero), labelled beyond its tip on a white box;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        if tip[0] == 0 and tip[1] == 0:
            ax.plot(0, 0, "o", color=color, ms=4, zorder=4)
            _d = math.radians(45 + turn)
        else:
            arrow(ax, (0, 0), tip, color)
            _d = math.atan2(tip[1], tip[0]) + math.radians(turn)
        ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(_d), r * math.sin(_d)), ha="center", va="center", color=color, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    plane(_left, 12)
    _left.plot([_x[0], _s[0], _y[0]], [_x[1], _s[1], _y[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _vector(_left, _s, GREEN, r"$\vec{x}+\vec{y}$", 0, r=24)
    _side = -1 if _x[0] * _y[1] - _x[1] * _y[0] < 0 else 1  # labels go on the outer side of each arrow
    _vector(_left, _x, BLUE, r"$\vec{x}$", -75 * _side)
    _vector(_left, _y, RED, r"$\vec{y}$", 75 * _side)

    plane(_right, 12)
    _vector(_right, _ax_, GREEN, r"$\alpha \cdot \vec{x}$", 75)
    _vector(_right, _x, BLUE, r"$\vec{x}$", -75)
    for _ax in (_left, _right):
        _ax.set_xticks(range(-8, 9, 4))
        _ax.set_yticks(range(-8, 9, 4))

    def _col(v, color):
        return rf"\textcolor{{{color}}}{{\begin{{bmatrix}} {v[0] + 0.0:g} \\ {v[1] + 0.0:g} \end{{bmatrix}}}}"

    mo.vstack(
        [
            mo.hstack([x1, x2, y1, y2, alpha], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{x} + \vec{y}$", rf"${_col(_x, BLUE)} + {_col(_y, RED)} = {_col(_s, GREEN)}$"),
                    (r"$\alpha \cdot \vec{x}$", rf"$({_a:g}) \cdot {_col(_x, BLUE)} = {_col(_ax_, GREEN)}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; we can interpret the operations in terms of arrows from the origin, not in terms of points

    $\leadsto$ &nbsp; these carry most of the properties of the usual addition and multiplication in $\mathbb{R}$
    """
            ),
            theorem(
                r"""
    For every $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and $\alpha, \beta \in \mathbb{R}$

    - $(\vec{x} + \vec{y}) + \vec{z} = \vec{x} + (\vec{y} + \vec{z})$ and $\alpha \cdot (\beta \cdot \vec{x}) = (\alpha\beta) \cdot \vec{x}$ &nbsp; (associativity)
    - $(\alpha + \beta) \cdot \vec{x} = \alpha \cdot \vec{x} + \beta \cdot \vec{x}$ and $\alpha \cdot (\vec{x} + \vec{y}) = \alpha \cdot \vec{x} + \alpha \cdot \vec{y}$ &nbsp; (distributivity)
    - $\vec{x} + \vec{y} = \vec{y} + \vec{x}$ &nbsp; (commutativity)
    - $\vec{x} + \vec{0} = \vec{x}$, &nbsp; $(1) \cdot \vec{x} = \vec{x}$ &nbsp; (neutral operations)
    - $0 \cdot \vec{x} = \vec{0}$, &nbsp; $\alpha \cdot \vec{0} = \vec{0}$ &nbsp; (null operations)
    """,
                "Properties of the operations",
            ),
            mo.md(r"**Proof.** Exercise! $\square$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $\mathbb{R}^n$ is the set of ordered lists $\vec{x} = (x^1, \dots, x^n)$ of $n$ real numbers: points in an $n$-dimensional space
    - every point is also a unique arrow from the origin, the $n$-vector $\vec{x}$ (a column matrix of size $n$)
    - vector addition and scalar–vector multiplication are defined component-wise, and are interpreted in terms of arrows from the origin
    - they are associative, distributive and commutative, with neutral and null operations, as in $\mathbb{R}$

    **Next:** the Euclidean inner product (the dot product)
    """)
    return


if __name__ == "__main__":
    app.run()
