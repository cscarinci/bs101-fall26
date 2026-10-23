import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 03 · Matrices, linear transformations, and determinants", css_file="bs101.css")


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
    header("Lecture 03", "Week 02", "Lecture 03 · Matrices, linear transformations, and determinants")
    return


@app.cell(hide_code=True)
def _(arrow):
    def vector(ax, tail, tip, color, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length)."""
        if tip[0] == tail[0] and tip[1] == tail[1]:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
        else:
            arrow(ax, tail, tip, color, **kw)

    def legend_box(fig, entries, loc="outside right center", ncols=1):
        """A legend box for the figure, so that no label covers the drawing: entries (kind, colour, label[, style])
        with kind "dot", "ring", "line" (style: line style) or "area" (style: edge colour)."""
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch

        handles = []
        for kind, c, _label, *style in entries:
            if kind == "dot":
                handles.append(Line2D([], [], ls="none", marker="o", ms=6, color=c))
            elif kind == "ring":
                handles.append(Line2D([], [], ls="none", marker="o", ms=6, mfc="white", mec=c, mew=1.3))
            elif kind == "line":
                handles.append(Line2D([], [], color=c, lw=1.6, ls=style[0] if style else "-"))
            else:
                handles.append(Patch(facecolor=c, edgecolor=style[0] if style else c, lw=1.0))
        fig.legend(handles, [e[2] for e in entries], loc=loc, ncols=ncols, fontsize=12, frameon=True, fancybox=False, edgecolor="#c8c8c8")

    return legend_box, vector


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, RED, arrow, blank, mo):
    _fig, _ax = blank(HALF, 2.0, (-0.3, 3.6), (-0.6, 2.2))
    _ax.plot([2, 2], [0, 1.8], color=GREY, lw=1.0, ls=(0, (4, 3)))
    arrow(_ax, (0, 0), (3, 0), RED)
    arrow(_ax, (0, 0), (2, 0), GREEN)
    arrow(_ax, (0, 0), (2, 1.8), BLUE)
    _ax.text(2.08, 1.88, r"$\vec{x}$", color=BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(3.1, 0, r"$\vec{u}$", color=RED, fontsize=13, ha="left", va="center")
    _ax.text(1.0, -0.14, r"$a\vec{u} = \mathrm{proj}_{\vec{u}}(\vec{x})$", color=GREEN, fontsize=13, ha="center", va="top")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - dot product in $\mathbb{R}^n$: &nbsp; $\cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}$, &nbsp; $\vec{x} \cdot \vec{y} = x^1 y^1 + x^2 y^2 + \dots + x^n y^n$
    - norm / length $\lVert \vec{x} \rVert = \sqrt{\vec{x} \cdot \vec{x}}$ &nbsp; and angle $\theta(\vec{x}, \vec{y}) = \arccos\!\left( \dfrac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \right)$ &nbsp; (only when $\vec{x}, \vec{y} \neq \vec{0}$)
    - in-class practice Q3: given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$ pairwise orthogonal, all non-zero (**orthogonal frame**), we can write $\vec{x} \in \mathbb{R}^3$ as $\vec{x} = a\vec{u} + b\vec{v} + c\vec{w}$ where $a = \dfrac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}$, $b = \dfrac{\vec{x} \cdot \vec{v}}{\lVert \vec{v} \rVert^2}$, $c = \dfrac{\vec{x} \cdot \vec{w}}{\lVert \vec{w} \rVert^2}$
    - $a\vec{u} = \dfrac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}\, \vec{u} = \mathrm{proj}_{\vec{u}}(\vec{x})$ &nbsp; (orthogonal projection of $\vec{x}$ onto the $\vec{u}$ direction)
    - $\Longrightarrow$ &nbsp; $\vec{x} = \mathrm{proj}_{\vec{u}}(\vec{x}) + \mathrm{proj}_{\vec{v}}(\vec{x}) + \mathrm{proj}_{\vec{w}}(\vec{x})$: any vector in $\mathbb{R}^3$ decomposes as the sum of orthogonal projections onto an orthogonal frame!
    """
            ),
            _fig,
            mo.md(r"""**In this lecture:** the standard basis as preferred orthogonal frame, matrices, linear transformations and determinants

            **References:** MT 1.3, 1.5""").style({"display": "block"}),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, RED, arrow, blank, definition, mo):
    def _pr(x1, x2, x3):
        """Oblique projection of R^3, as on the board: x^2 to the right, x^3 up, x^1 towards the viewer."""
        return x2 - 0.45 * x1, x3 - 0.4 * x1

    _fig, _ax = blank(HALF, 2.9, (-1.4, 2.9), (-1.1, 2.5))
    arrow(_ax, _pr(-0.5, 0, 0), _pr(2.2, 0, 0), "black", lw=0.9)
    arrow(_ax, (-0.6, 0), (2.5, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.6), (0, 2.4), "black", lw=0.9)
    _p = (0.6, 2.2, 2.0)
    _P = _pr(*_p)
    _ax.plot([_P[0], 0], [_P[1], _p[2]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    arrow(_ax, (0, 0), (0, _p[2]), GREEN)
    for _tip in (_pr(1, 0, 0), (1, 0), (0, 1)):
        arrow(_ax, (0, 0), _tip, RED)
    arrow(_ax, (0, 0), _P, BLUE)
    _e1 = _pr(1, 0, 0)
    _ax.text(_e1[0] - 0.12, _e1[1] + 0.12, r"$\vec{e}_1$", color=RED, fontsize=13, ha="right", va="bottom")
    _ax.text(0.6, -0.14, r"$\vec{e}_2$", color=RED, fontsize=13, ha="center", va="top")
    _ax.text(0.14, 0.55, r"$\vec{e}_3$", color=RED, fontsize=13, ha="left", va="center")
    _ax.text(-0.14, 1.6, r"$x^3\vec{e}_3$", color=GREEN, fontsize=13, ha="right", va="center")
    _ax.text(_P[0] + 0.1, _P[1] + 0.05, r"$\vec{x}$", color=BLUE, fontsize=13, ha="left", va="bottom")

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.3 &nbsp; Matrices, linear transformations, and determinants

    ### The standard basis
    """
            ),
            definition(
                r"""
    $\mathbb{R}^n$ has a preferred orthogonal frame

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}
    \qquad \text{the \textbf{standard basis vectors} of } \mathbb{R}^n
    $$
    """,
                "Standard basis",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $\vec{e}_i \cdot \vec{e}_j = 0$ if $i \neq j$

    $\leadsto$ &nbsp; $\vec{e}_i \cdot \vec{e}_i = 1$ &nbsp; (unit length vectors)

    Given

    $$
    \begin{aligned}
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}
    &= x^1 \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix} + \dots + x^n \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix} \\
    &= \underbrace{x^1 \vec{e}_1}_{\mathrm{proj}_{\vec{e}_1}(\vec{x})} + \underbrace{x^2 \vec{e}_2}_{\mathrm{proj}_{\vec{e}_2}(\vec{x})} + \dots + \underbrace{x^n \vec{e}_n}_{\mathrm{proj}_{\vec{e}_n}(\vec{x})}
    = (\vec{x} \cdot \vec{e}_1)\, \vec{e}_1 + (\vec{x} \cdot \vec{e}_2)\, \vec{e}_2 + \dots + (\vec{x} \cdot \vec{e}_n)\, \vec{e}_n
    \end{aligned}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; any vector can be written uniquely as a linear combination of the standard basis vectors

    $\leadsto$ &nbsp; the component $x^i$ of a vector $\vec{x}$ is the signed length of the projection of $\vec{x}$ along $\vec{e}_i$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Matrices"""),
            definition(
                r"""
    Given $m, n \in \mathbb{Z}_{>0}$, an **$m \times n$ matrix** is an array of real numbers with $m$ rows and $n$ columns

    $$
    A = \begin{bmatrix}
    A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\
    A^2{}_1 & A^2{}_2 & \cdots & A^2{}_n \\
    \vdots & & & \vdots \\
    A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n
    \end{bmatrix} \in \mathrm{Mat}(m \times n),
    \qquad A^i{}_j \in \mathbb{R} \quad \forall\, i = 1, \dots, m, \ j = 1, \dots, n
    $$

    $A^i{}_j$ is the $(i, j)$ component of the matrix $A$: superscript $i$ denotes the row, subscript $j$ denotes the column. In $\mathrm{Mat}(m \times n)$, $m$ counts rows and $n$ counts columns.
    """,
                "Matrix",
            ),
            mo.md(
                r"""
    Why are we interested in matrices?

    $\leadsto$ &nbsp; generalization of vectors ($n \times 1$ matrices): can also extend addition and multiplication to matrices!

    $\leadsto$ &nbsp; will give the simplest examples of multivariable functions!
    """
            ),
            definition(
                r"""
    Given $A \in \mathrm{Mat}(m \times n)$, $B \in \mathrm{Mat}(m \times n)$, $\alpha \in \mathbb{R}$

    $A + B \in \mathrm{Mat}(m \times n)$ has components

    $$
    (A + B)^i{}_j = A^i{}_j + B^i{}_j \qquad (\text{componentwise addition})
    $$

    $\alpha A \in \mathrm{Mat}(m \times n)$ has components

    $$
    (\alpha A)^i{}_j = \alpha A^i{}_j \qquad (\text{componentwise multiplication by a scalar})
    $$
    """,
                "Matrix addition and scalar multiplication",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}, \quad
    B = \begin{bmatrix} 6 & 4 & 2 \\ 5 & 3 & 1 \end{bmatrix} \in \mathrm{Mat}(2 \times 3)
    \qquad \leadsto \qquad
    A + B = \begin{bmatrix} 7 & 6 & 5 \\ 9 & 8 & 7 \end{bmatrix}, \quad
    3A = \begin{bmatrix} 3 & 6 & 9 \\ 12 & 15 & 18 \end{bmatrix}
    $$

    ### Matrix multiplication
    """
            ),
            definition(
                r"""
    Given $A \in \mathrm{Mat}(m \times p)$, $B \in \mathrm{Mat}(p \times n)$

    $AB \in \mathrm{Mat}(m \times n)$ has components

    $$
    (AB)^i{}_j = \underbrace{A^i{}_1 B^1{}_j + A^i{}_2 B^2{}_j + \dots + A^i{}_p B^p{}_j}_{\text{sum of products of corresponding components}}
    $$
    """,
                "Matrix multiplication",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \qquad
    B = \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix} \in \mathrm{Mat}(3 \times 2)
    $$

    (the number of columns of $A$ and the number of rows of $B$ must be the same in order to define $AB$)

    $$
    AB = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix}
    = \begin{bmatrix}
    1 \times 1 + 2 \times 0 + 3 \times 2 & 1 \times 0 + 2 \times 3 + 3 \times 0 \\
    4 \times 1 + 5 \times 0 + 6 \times 2 & 4 \times 0 + 5 \times 3 + 6 \times 0
    \end{bmatrix}
    = \begin{bmatrix} 7 & 6 \\ 16 & 15 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    $$

    **Remark.** Most times we cannot multiply two matrices: $A \in \mathrm{Mat}(m \times q)$, $B \in \mathrm{Mat}(p \times n)$

    - $AB$ can only be defined if $p = q$ $\;\Longrightarrow\; AB \in \mathrm{Mat}(m \times n)$
    - $BA$ can only be defined if $m = n$ $\;\Longrightarrow\; BA \in \mathrm{Mat}(p \times q)$
    - $p = q$ and $m = n$ $\;\not\Longrightarrow\; AB = BA$! &nbsp; ($AB \in \mathrm{Mat}(n \times n)$, $BA \in \mathrm{Mat}(p \times p)$)
    - $p = q = m = n$ $\;\not\Longrightarrow\; AB = BA$!

    **Example.**

    $$
    A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}, \quad
    B = \begin{bmatrix} 5 & 0 \\ 1 & 1 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    \qquad \Longrightarrow \qquad
    AB = \begin{bmatrix} 11 & 1 \\ 3 & 3 \end{bmatrix} \neq BA = \begin{bmatrix} 10 & 5 \\ 2 & 4 \end{bmatrix}
    $$

    (matrix multiplication is non-commutative even for square matrices)

    **Remark.** Matrix multiplication can “transform” vectors into other vectors: $A \in \mathrm{Mat}(m \times n)$ and $\vec{x} \in \mathbb{R}^n \approx \mathrm{Mat}(n \times 1)$

    $$
    \Longrightarrow \qquad A\vec{x} \in \mathrm{Mat}(m \times 1) \approx \mathbb{R}^m
    $$

    $$
    \Longrightarrow \qquad A : \mathbb{R}^n \longrightarrow \mathbb{R}^m \ \text{ is a function on } \mathbb{R}^n \text{ valued in } \mathbb{R}^m \quad (\text{a multivariable function!})
    $$

    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \quad
    \vec{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \in \mathbb{R}^3 = \mathrm{Mat}(3 \times 1)
    $$

    $$
    \Longrightarrow \qquad A\vec{x} = \begin{bmatrix} 1 + 4 + 9 \\ 4 + 10 + 18 \end{bmatrix} = \begin{bmatrix} 14 \\ 32 \end{bmatrix} \in \mathbb{R}^2 = \mathrm{Mat}(2 \times 1)
    $$

    $\leadsto$ &nbsp; functions defined by matrix multiplication are always linear! (very special property)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Linear transformations"""),
            definition(
                r"""
    A function $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called **linear** if $\forall\, \vec{x}, \vec{y} \in \mathbb{R}^n$ and $\forall\, \alpha, \beta \in \mathbb{R}$

    $$
    f(\alpha \vec{x} + \beta \vec{y}) = \alpha f(\vec{x}) + \beta f(\vec{y})
    $$
    """,
                "Linear function",
            ),
            theorem(
                r"""
    Every function defined by an $m \times n$ matrix via matrix multiplication is linear. Conversely, every linear function $\mathbb{R}^n \longrightarrow \mathbb{R}^m$ is defined by an $m \times n$ matrix!
    """,
                "Linear functions and matrices",
            ),
            mo.md(
                r"""
    **Proof.**

    1. Write $A$ in terms of its column vectors ($n$ $m$-vectors)

        $$
        A = \begin{bmatrix}
        A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\
        \vdots & \vdots & & \vdots \\
        A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n
        \end{bmatrix}
        = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix} \in \mathrm{Mat}(m \times n)
        $$

    2. For $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \in \mathbb{R}^n$

        $$
        \begin{aligned}
        A\vec{x} &= \begin{bmatrix}
        A^1{}_1 x^1 + A^1{}_2 x^2 + \dots + A^1{}_n x^n \\
        A^2{}_1 x^1 + A^2{}_2 x^2 + \dots + A^2{}_n x^n \\
        \vdots \\
        A^m{}_1 x^1 + A^m{}_2 x^2 + \dots + A^m{}_n x^n
        \end{bmatrix} \\
        &= x^1 \begin{bmatrix} A^1{}_1 \\ A^2{}_1 \\ \vdots \\ A^m{}_1 \end{bmatrix} +
        x^2 \begin{bmatrix} A^1{}_2 \\ A^2{}_2 \\ \vdots \\ A^m{}_2 \end{bmatrix} +
        \dots +
        x^n \begin{bmatrix} A^1{}_n \\ A^2{}_n \\ \vdots \\ A^m{}_n \end{bmatrix}
        = x^1 \vec{A}_1 + x^2 \vec{A}_2 + \dots + x^n \vec{A}_n
        \end{aligned}
        $$

    3. Then

        $$
        A(\alpha \vec{x} + \beta \vec{y}) = (\alpha x^1 + \beta y^1)\, \vec{A}_1 + \dots + (\alpha x^n + \beta y^n)\, \vec{A}_n = \alpha A\vec{x} + \beta A\vec{y}
        $$

    For the converse direction: $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ linear

    $$
    \begin{aligned}
    \Longrightarrow \quad f(\vec{x}) &= f(x^1 \vec{e}_1 + x^2 \vec{e}_2 + \dots + x^n \vec{e}_n), \qquad \forall\, \vec{x} \in \mathbb{R}^n \qquad (\vec{e}_i \text{ the standard basis of } \mathbb{R}^n) \\
    &= x^1 f(\vec{e}_1) + x^2 f(\vec{e}_2) + \dots + x^n f(\vec{e}_n) \\
    &= A\vec{x} \quad \text{where} \quad A = \begin{bmatrix} f(\vec{e}_1) & f(\vec{e}_2) & \cdots & f(\vec{e}_n) \end{bmatrix} \in \mathrm{Mat}(m \times n), \quad \vec{A}_i = f(\vec{e}_i) \in \mathbb{R}^m \qquad \square
    \end{aligned}
    $$

    $\leadsto$ &nbsp; linear functions (or linear transformations) are the simplest non-trivial examples of multivariable functions

    $\leadsto$ &nbsp; later, we will introduce derivatives of more general multivariable functions as their best linear approximations

    **Remark.** Matrix multiplication is the same as composition of linear transformations

    $$
    \begin{aligned}
    A \in \mathrm{Mat}(m \times p) \quad &\leftrightsquigarrow \quad A : \mathbb{R}^p \longrightarrow \mathbb{R}^m \\
    B \in \mathrm{Mat}(p \times n) \quad &\leftrightsquigarrow \quad B : \mathbb{R}^n \longrightarrow \mathbb{R}^p \\
    AB \in \mathrm{Mat}(m \times n) \quad &\leftrightsquigarrow \quad A \circ B : \mathbb{R}^n \longrightarrow \mathbb{R}^m
    \end{aligned}
    $$

    $\leadsto$ &nbsp; another way to get convinced about non-commutativity of matrix multiplication!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Determinants of $2 \times 2$ matrices"""),
            definition(
                r"""
    For $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2) \ \leftrightsquigarrow \ A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ define

    $$
    \det(A) = ad - bc \in \mathbb{R} \qquad \text{the \textbf{determinant} of } A
    $$
    """,
                "Determinant",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; the determinant is a fundamental property of a square matrix (also for $n > 2$)

    $\leadsto$ &nbsp; it measures the “signed area” of the parallelogram defined by the columns of $A$, $\vec{A}_1 = A\vec{e}_1$ and $\vec{A}_2 = A\vec{e}_2$

    For nonzero columns, the unsigned area is

    $$
    |\det A| = \text{area} = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)
    $$

    $$
    \begin{aligned}
    (\det A)^2 = \text{area}^2 = (\text{base} \times \text{height})^2 &= \lVert \vec{A}_1 \rVert^2\, \lVert \vec{A}_2 \rVert^2 \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \\
    &= \lVert \vec{A}_1 \rVert^2\, \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2 = (ad - bc)^2
    \end{aligned}
    $$

    If either column is zero, both the area and determinant are zero.

    For independent columns, the smaller turn from $\vec{A}_1$ to $\vec{A}_2$ is counterclockwise when $\det A > 0$, clockwise when $\det A < 0$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ma = mo.ui.slider(-3, 3, 0.5, value=2, label="$a$", show_value=True)
    mb = mo.ui.slider(-3, 3, 0.5, value=1, label="$b$", show_value=True)
    mc = mo.ui.slider(-3, 3, 0.5, value=0.5, label="$c$", show_value=True)
    md = mo.ui.slider(-3, 3, 0.5, value=1.5, label="$d$", show_value=True)
    return ma, mb, mc, md


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, RED, legend_box, ma, mb, mc, md, mo, plane, table, vector):
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c + 0.0

    _fig = Figure(figsize=(HALF + 0.4, HALF + 0.7), layout="constrained")
    _ax = _fig.subplots()
    _small = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_a + _b), abs(_c + _d)) <= 3
    plane(_ax, 4.4 if _small else 7.6)  # the frame follows the parallelogram: nothing is clipped
    _ticks = range(-4, 5, 2) if _small else range(-6, 7, 3)
    _ax.set_xticks(_ticks)
    _ax.set_yticks(_ticks)
    _ax.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=LIGHT, lw=0)  # A(unit square)
    _ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=GREY, lw=1.0)  # the unit square
    _ax.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_ax, (0, 0), (_a, _c), BLUE)
    vector(_ax, (0, 0), (_b, _d), RED)
    legend_box(
        _fig,
        [("line", BLUE, r"$\vec{A}_1$"), ("line", RED, r"$\vec{A}_2$"), ("area", "white", "unit square", GREY), ("area", LIGHT, "its image under $A$")],
        loc="outside lower center",
        ncols=2,
    )

    mo.vstack(
        [
            mo.hstack([ma, mb, mc, md], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$", rf"$\begin{{bmatrix}} \textcolor{{{BLUE}}}{{{_a:g}}} & \textcolor{{{RED}}}{{{_b:g}}} \\ \textcolor{{{BLUE}}}{{{_c:g}}} & \textcolor{{{RED}}}{{{_d:g}}} \end{{bmatrix}}$"),
                    (r"$\det(A) = ad - bc$", rf"$({_a:g})({_d:g}) - ({_b:g})({_c:g}) = {_det:g}$"),
                    (r"area of the parallelogram", rf"${abs(_det):g}$"),
                    (r"$A$ invertible", "yes" if _det != 0 else "no"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; it also determines whether or not $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ is **invertible**!

    $$
    \exists\, A^{-1} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2 \ \text{ such that } \ A \circ A^{-1}(\vec{x}) = A^{-1} \circ A(\vec{x}) = \vec{x} \quad \forall\, \vec{x} \in \mathbb{R}^2
    \qquad \Longleftrightarrow \qquad \det(A) \neq 0
    $$

    $\leadsto$ &nbsp; in fact, for $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ the inverse can be calculated explicitly when $\det(A) = ad - bc \neq 0$

    $$
    A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q1_1, q1_2, q3_m2, q3_0, q3_2 = (_field() for _ in range(5))
    return q1_1, q1_2, q3_0, q3_2, q3_m2


@app.cell(hide_code=True)
def _(check, mo, q1_1, q1_2, q3_0, q3_2, q3_m2):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $f : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ be linear, with

    $$
    f\!\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right) = \begin{bmatrix} 3 \\ 1 \end{bmatrix}
    \qquad \text{and} \qquad
    f\!\left( \begin{bmatrix} 1 \\ -1 \end{bmatrix} \right) = \begin{bmatrix} 1 \\ 3 \end{bmatrix}.
    $$

    Find the matrix representation of $f$. Then compute $f\!\left( \begin{bmatrix} 2 \\ -1 \end{bmatrix} \right)$.
    """
            ),
            _ask(r"1st component $=$", q1_1, 3),
            _ask(r"2nd component $=$", q1_2, 5),
            mo.md(
                r"""
    ### Question 2

    Let $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \; B = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix}$.

    Compute $AB$ and $BA$.

    Then find all vectors $\vec{x} \in \mathbb{R}^2$ such that $AB\vec{x} = BA\vec{x}$.

    Conclude that $AB \neq BA$ does not imply $AB\vec{x} \neq BA\vec{x}$ $\;\forall\, \vec{x} \in \mathbb{R}^2$.

    ### Question 3

    For $t \in \mathbb{R}$, consider

    $$
    C_t = \begin{bmatrix} t & 1 \\ 2 & t - 1 \end{bmatrix}
    $$

    For which values of $t$ is $C_t$ invertible?

    Let $Q = [0, 1] \times [0, 1] \subseteq \mathbb{R}^2$ be the unit square in $\mathbb{R}^2$.

    Draw $C_t(Q)$ and compute its area for $t = -2$, $t = 0$, $t = 2$.
    """
            ),
            _ask(r"area for $t = -2$:", q3_m2, 4),
            _ask(r"area for $t = 0$:", q3_0, 2),
            _ask(r"area for $t = 2$:", q3_2, 0),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - the standard basis is the preferred orthogonal frame of $\mathbb{R}^n$: $\vec{x} = (\vec{x} \cdot \vec{e}_1)\, \vec{e}_1 + \dots + (\vec{x} \cdot \vec{e}_n)\, \vec{e}_n$, and $x^i$ is the signed length of the projection of $\vec{x}$ along $\vec{e}_i$
    - matrices in $\mathrm{Mat}(m \times n)$ are added and multiplied by scalars componentwise; $AB$ is defined only when the number of columns of $A$ equals the number of rows of $B$, and is non-commutative even for square matrices
    - $A \in \mathrm{Mat}(m \times n)$ $\leftrightsquigarrow$ linear function $A : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ with columns $\vec{A}_i = A\vec{e}_i$; matrix multiplication is composition
    - for $A \in \mathrm{Mat}(2 \times 2)$, $\det(A) = ad - bc$ is the signed area of the parallelogram defined by the columns, and $A$ is invertible $\Longleftrightarrow$ $\det(A) \neq 0$

    **Next:** determinants, areas and volumes
    """)
    return


if __name__ == "__main__":
    app.run()
