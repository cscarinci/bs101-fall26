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
    RED, GREEN, BLUE, GREY = "#b3261e", "#2e7d32", "#1b458f", "#888888"

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
        <b>Date</b><span>{date}</span><b>Instructor</b><span>Professor Scarinci</span>
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

    def warning(body):
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 2.2, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=18)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color="#cfe3f5", lw=0.6)
        ax.set_axisbelow(True)

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, GREEN, GREY, RED, arrow, check, definition, header, plane, theorem, warning


@app.cell(hide_code=True)
def _(header):
    header("Lecture 03", "Week 02", "Lecture 03 · Matrices, linear transformations, and determinants")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, arrow, mo):
    _fig = Figure(figsize=(3.4, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.2, 3.4)
    _ax.set_ylim(-0.5, 2.3)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.plot([2, 2], [0, 1.8], "--", color=BLUE, lw=1.3)
    arrow(_ax, (0, 0), (3, 0), RED)
    arrow(_ax, (0, 0), (2, 1.8), "black")
    arrow(_ax, (0, 0), (2, 0), BLUE)
    _ax.text(2.05, 1.9, r"$\vec{x}$", fontsize=17)
    _ax.text(3.05, 0.1, r"$\vec{u}$", color=RED, fontsize=17)
    _ax.text(0.7, -0.42, r"$a\vec{u}$", color=BLUE, fontsize=17)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Dot product in $\mathbb{R}^n$: &nbsp; $\cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}$

    $$
    \vec{x} \cdot \vec{y} = x^1 y^1 + x^2 y^2 + \dots + x^n y^n
    $$

    The angle is defined only when $\vec{x}, \vec{y} \neq \vec{0}$.

    $$
    \underbrace{\lVert \vec{x} \rVert = \sqrt{\vec{x} \cdot \vec{x}}}_{\text{norm / length}}
    \qquad \qquad
    \underbrace{\theta(\vec{x}, \vec{y}) = \arccos\!\left( \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \right)}_{\text{angle}}
    $$

    **In-class practice Q3:** Given nonzero, pairwise orthogonal vectors $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$, we can write $\vec{x} \in \mathbb{R}^3$ as

    $$
    \vec{x} = a\vec{u} + b\vec{v} + c\vec{w}
    \qquad \text{where} \qquad
    a = \frac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}, \quad
    b = \frac{\vec{x} \cdot \vec{v}}{\lVert \vec{v} \rVert^2}, \quad
    c = \frac{\vec{x} \cdot \vec{w}}{\lVert \vec{w} \rVert^2}
    $$
    """
            ),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"""
    $$
    a\vec{u} = \frac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}\, \vec{u} = \mathrm{proj}_{\vec{u}}(\vec{x})
    $$

    orthogonal projection of $\vec{x}$ onto the $\vec{u}$ direction
    """
                    ),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
            mo.md(
                r"""
    $\therefore$ &nbsp; $\vec{u}, \vec{v}, \vec{w}$ pairwise orthogonal, all non-zero (orthogonal frame)

    $$
    \Longrightarrow \quad \vec{x} = \mathrm{proj}_{\vec{u}}(\vec{x}) + \mathrm{proj}_{\vec{v}}(\vec{x}) + \mathrm{proj}_{\vec{w}}(\vec{x})
    $$

    Any vector in $\mathbb{R}^3$ decomposes as the sum of orthogonal projections onto an orthogonal frame!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, definition, mo):
    from mpl_toolkits.mplot3d import proj3d as _proj3d

    _fig = Figure(figsize=(3.8, 3.4), layout="constrained")
    _ax = _fig.add_subplot(projection="3d")
    for _d in ((2.2, 0, 0), (0, 2.2, 0), (0, 0, 2.2)):
        _ax.quiver(0, 0, 0, *_d, color="black", lw=0.9, arrow_length_ratio=0.06)
    _p = (1.0, 1.6, 1.7)
    _ax.quiver(0, 0, 0, *_p, color=BLUE, lw=2.2, arrow_length_ratio=0.1)
    _ax.plot([_p[0], 0], [_p[1], 0], [_p[2], _p[2]], "--", color=BLUE, lw=1.2)
    _ax.text(0, -0.75, _p[2], r"$x^3\vec{e}_3$", color=BLUE, fontsize=15)
    _ax.text(_p[0], _p[1], _p[2] + 0.15, r"$\vec{x}$", color=BLUE, fontsize=15)
    _ax.set_xlim(0, 2)
    _ax.set_ylim(0, 2)
    _ax.set_zlim(0, 2)
    _ax.view_init(elev=22, azim=28)
    _ax.set_axis_off()
    for _d, _name, _offset, _ha, _va in (
        ((1, 0, 0), r"$\vec{e}_1$", (-8, 8), "right", "bottom"),
        ((0, 1, 0), r"$\vec{e}_2$", (6, 8), "left", "bottom"),
        ((0, 0, 1), r"$\vec{e}_3$", (8, 0), "left", "center"),
    ):
        _ax.quiver(0, 0, 0, *_d, color=GREEN, lw=2.2, arrow_length_ratio=0.15)
        _px, _py, _pz = _proj3d.proj_transform(*_d, _ax.get_proj())
        _ax.annotate(_name, (_px, _py), xytext=_offset, textcoords="offset points", ha=_ha, va=_va, color=GREEN, fontsize=15)

    mo.vstack(
        [
            definition(
                r"""
    $\mathbb{R}^n$ has a preferred orthogonal frame

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}
    \qquad \text{standard basis vectors of } \mathbb{R}^n
    $$
    """
            ),
            mo.md(
                r"""
    $\vec{e}_i \cdot \vec{e}_j = 0$ if $i \neq j$

    $\vec{e}_i \cdot \vec{e}_i = 1$ &nbsp; (unit length vectors)

    Given

    $$
    \begin{aligned}
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}
    &= x^1 \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix} + \dots + x^n \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix} \\
    &= \underbrace{x^1 \vec{e}_1}_{\mathrm{proj}_{\vec{e}_1}(\vec{x})} + \underbrace{x^2 \vec{e}_2}_{\mathrm{proj}_{\vec{e}_2}(\vec{x})} + \dots + \underbrace{x^n \vec{e}_n}_{\mathrm{proj}_{\vec{e}_n}(\vec{x})} \\
    &= (\vec{x} \cdot \vec{e}_1)\, \vec{e}_1 + (\vec{x} \cdot \vec{e}_2)\, \vec{e}_2 + \dots + (\vec{x} \cdot \vec{e}_n)\, \vec{e}_n
    \end{aligned}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    Any vector can be written uniquely as a linear combination of the standard basis vectors.

    The component $x^i$ of a vector $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}$ is the signed length of the projection of $\vec{x}$ along $\vec{e}_i$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"## 3 &nbsp; Matrices, linear transformations, and determinants (MT 1.2, 1.3)"),
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
    """
            ),
            mo.md(
                r"""
    Why are we interested in matrices?

    - generalization of vectors ($n \times 1$ matrices) — can also extend addition and multiplication to matrices!
    - will give the simplest examples of multivariable functions!
    """
            ),
            definition(
                r"""
    Given $A \in \mathrm{Mat}(m \times n)$, $B \in \mathrm{Mat}(m \times n)$, $\alpha \in \mathbb{R}$:

    $A + B \in \mathrm{Mat}(m \times n)$ has components

    $$
    (A + B)^i{}_j = A^i{}_j + B^i{}_j \qquad \text{componentwise addition}
    $$

    $\alpha A \in \mathrm{Mat}(m \times n)$ has components

    $$
    (\alpha A)^i{}_j = \alpha A^i{}_j \qquad \text{componentwise multiplication (by a scalar)}
    $$
    """
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
    """
            ),
            definition(
                r"""
    Given $A \in \mathrm{Mat}(m \times p)$, $B \in \mathrm{Mat}(p \times n)$:

    $AB \in \mathrm{Mat}(m \times n)$ has components

    $$
    (AB)^i{}_j = A^i{}_1 B^1{}_j + A^i{}_2 B^2{}_j + \dots + A^i{}_p B^p{}_j
    $$

    (sum of products of corresponding components).
    """
            ),
            mo.md(
                r"""
    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \qquad
    B = \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix} \in \mathrm{Mat}(3 \times 2)
    $$

    The number of columns of $A$ and the number of rows of $B$ must be the same in order to define $AB$.

    $$
    \begin{aligned}
    AB = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix}
    &= \begin{bmatrix}
    \textcolor{#b3261e}{1 \times 1 + 2 \times 0 + 3 \times 2} & \textcolor{#2e7d32}{1 \times 0 + 2 \times 3 + 3 \times 0} \\
    \textcolor{#1b458f}{4 \times 1 + 5 \times 0 + 6 \times 2} & \textcolor{#e65100}{4 \times 0 + 5 \times 3 + 6 \times 0}
    \end{bmatrix} \\
    &= \begin{bmatrix} 7 & 6 \\ 16 & 15 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    \end{aligned}
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
    \quad \Longrightarrow \quad
    AB = \begin{bmatrix} 11 & 1 \\ 3 & 3 \end{bmatrix} \neq BA = \begin{bmatrix} 10 & 5 \\ 2 & 4 \end{bmatrix}
    $$

    Matrix multiplication is non-commutative even for square matrices.

    **Remark.** Matrix multiplication can “transform” vectors into other vectors: $A \in \mathrm{Mat}(m \times n)$ and $\vec{x} \in \mathbb{R}^n \approx \mathrm{Mat}(n \times 1)$

    $$
    \Longrightarrow \quad A\vec{x} \in \mathrm{Mat}(m \times 1) \approx \mathbb{R}^m
    $$

    $$
    \Longrightarrow \quad A : \mathbb{R}^n \longrightarrow \mathbb{R}^m \ \text{ is a function on } \mathbb{R}^n \text{ valued in } \mathbb{R}^m \quad (\text{a multivariable function!})
    $$

    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \quad
    \vec{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \in \mathbb{R}^3 = \mathrm{Mat}(3 \times 1)
    \quad \Longrightarrow \quad
    A\vec{x} = \begin{bmatrix} 1 + 4 + 9 \\ 4 + 10 + 18 \end{bmatrix} = \begin{bmatrix} 14 \\ 32 \end{bmatrix} \in \mathbb{R}^2 = \mathrm{Mat}(2 \times 1)
    $$

    Functions defined by matrix multiplication are always linear! (very special property)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    A function $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called **linear** if $\forall\, \vec{x}, \vec{y} \in \mathbb{R}^n$ and $\forall\, \alpha, \beta \in \mathbb{R}$

    $$
    f(\alpha \vec{x} + \beta \vec{y}) = \alpha f(\vec{x}) + \beta f(\vec{y})
    $$
    """
            ),
            theorem(
                r"""
    Every function defined by an $m \times n$ matrix via matrix multiplication is linear. Conversely, every linear function $\mathbb{R}^n \longrightarrow \mathbb{R}^m$ is defined by an $m \times n$ matrix!
    """
            ),
            mo.md(
                r"""
    **Proof.**

    1. Write $A$ in terms of its column vectors ($n$ $m$-vectors):

        $$
        A = \begin{bmatrix}
        A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\
        \vdots & \vdots & & \vdots \\
        A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n
        \end{bmatrix}
        = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix} \in \mathrm{Mat}(m \times n)
        $$

    2. For $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \in \mathbb{R}^n$:

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
        x^n \begin{bmatrix} A^1{}_n \\ A^2{}_n \\ \vdots \\ A^m{}_n \end{bmatrix} \\
        &= x^1 \vec{A}_1 + x^2 \vec{A}_2 + \dots + x^n \vec{A}_n
        \end{aligned}
        $$

    3. Then

        $$
        \begin{aligned}
        A(\alpha \vec{x} + \beta \vec{y}) &= (\alpha x^1 + \beta y^1)\, \vec{A}_1 + \dots + (\alpha x^n + \beta y^n)\, \vec{A}_n \\
        &= \alpha A\vec{x} + \beta A\vec{y}
        \end{aligned}
        $$

    For the converse direction: $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ linear

    $$
    \begin{aligned}
    \Longrightarrow \quad f(\vec{x}) &= f(x^1 \vec{e}_1 + x^2 \vec{e}_2 + \dots + x^n \vec{e}_n), \qquad \forall\, \vec{x} \in \mathbb{R}^n \qquad (\vec{e}_i \text{ the std basis of } \mathbb{R}^n) \\
    &= x^1 f(\vec{e}_1) + x^2 f(\vec{e}_2) + \dots + x^n f(\vec{e}_n) \\
    &= A\vec{x} \quad \text{where} \quad A = \begin{bmatrix} f(\vec{e}_1) & f(\vec{e}_2) & \cdots & f(\vec{e}_n) \end{bmatrix} \in \mathrm{Mat}(m \times n), \quad \vec{A}_i = f(\vec{e}_i) \in \mathbb{R}^m \qquad \square
    \end{aligned}
    $$

    Linear functions (or linear transformations) are the simplest non-trivial examples of multivariable functions.

    Later, we will introduce derivatives of more general multivariable functions as their best linear approximations.

    **Remark.** Matrix multiplication is the same as composition of linear transformations

    $$
    \begin{aligned}
    A \in \mathrm{Mat}(m \times p) \quad &\leftrightsquigarrow \quad A : \mathbb{R}^p \longrightarrow \mathbb{R}^m \\
    B \in \mathrm{Mat}(p \times n) \quad &\leftrightsquigarrow \quad B : \mathbb{R}^n \longrightarrow \mathbb{R}^p \\
    AB \in \mathrm{Mat}(m \times n) \quad &\leftrightsquigarrow \quad A \circ B : \mathbb{R}^n \longrightarrow \mathbb{R}^m
    \end{aligned}
    $$

    Another way to get convinced about non-commutativity of matrix multiplication!
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
    For $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2) \ \leftrightsquigarrow \ A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ define

    $$
    \det(A) = ad - bc \in \mathbb{R} \qquad \text{the \textbf{determinant} of } A
    $$
    """
            ),
            mo.md(
                r"""
    The determinant is a fundamental property of a square matrix (also for $n > 2$).

    It measures the “signed area” of the parallelogram defined by the columns of $A$, $\vec{A}_1 = A\vec{e}_1$ and $\vec{A}_2 = A\vec{e}_2$.

    For nonzero columns, the unsigned area is

    $$
    |\det A| = \text{area} = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)
    $$

    $$
    \begin{aligned}
    (\det A)^2 = \text{area}^2 &= (\text{base} \times \text{height})^2 \\
    &= \lVert \vec{A}_1 \rVert^2\, \lVert \vec{A}_2 \rVert^2 \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \\
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
def _(Figure, GREEN, RED, arrow, ma, mb, mc, md, mo, plane):
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c

    _fig = Figure(figsize=(4.6, 4.6), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 3.5 if max(abs(_a + _b), abs(_c + _d)) <= 3 else 6.5)
    _ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color="#888888", alpha=0.25, lw=0)
    _ax.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=GREEN, alpha=0.3, lw=0)
    _ax.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=GREEN, lw=1)
    arrow(_ax, (0, 0), (_a, _c), RED)
    arrow(_ax, (0, 0), (_b, _d), "#1a237e")
    for _color, _label in ((RED, r"$\vec{A}_1$"), ("#1a237e", r"$\vec{A}_2$")):
        _ax.plot([], [], color=_color, lw=2.2, label=_label)
    _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=12)

    mo.vstack(
        [
            mo.hstack([mo.vstack([ma, mc]), mo.vstack([mb, md])], justify="start", gap=3),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        rf"$$A = \begin{{bmatrix}} {_a:g} & {_b:g} \\ {_c:g} & {_d:g} \end{{bmatrix}}$$"
                        "\n\n| | |\n|:--|:--|\n"
                        rf"| $\det(A) = ad - bc$ | ${_det:g}$ |"
                        "\n"
                        rf"| area of the parallelogram | ${abs(_det):g}$ |"
                        "\n"
                        rf"| $A$ invertible? | {'yes' if _det != 0 else 'no'} |"
                        "\n\n"
                        r"Grey: the unit square. Green: its image under $A$."
                    ).style({"max-width": "26rem"}),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It also determines whether or not $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ is **invertible**!

    $$
    \exists\, A^{-1} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2 \ \text{ s.t. } \ A \circ A^{-1}(\vec{x}) = A^{-1} \circ A(\vec{x}) = \vec{x} \quad \forall\, \vec{x} \in \mathbb{R}^2
    \qquad \Longleftrightarrow \qquad \det(A) \neq 0
    $$

    In fact, for $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ the inverse can be calculated explicitly when $\det(A) = ad - bc \neq 0$:

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

    Then find all vectors $\vec{x} \in \mathbb{R}^2$ s.t. $AB\vec{x} = BA\vec{x}$.

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


if __name__ == "__main__":
    app.run()
