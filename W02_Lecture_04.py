import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 04 · Determinants, areas and volumes", css_file="bs101.css")


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
    header("Lecture 04", "Week 02", "Lecture 04 · Determinants, areas and volumes")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Matrices $A \in \mathrm{Mat}(m \times n)$ &nbsp; $\leadsto$ &nbsp; linear transformation via matrix multiplication

    $$
    \begin{aligned}
    A : \mathbb{R}^n &\longrightarrow \mathbb{R}^m \\
    \vec{x} &\longmapsto A\vec{x}
    \end{aligned}
    $$

    $$
    A = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \in \mathrm{Mat}(3 \times 2), \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2
    $$

    $$
    \Longrightarrow \quad A\vec{x} = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} x^1 \\ x^2 \end{bmatrix}
    = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \\ e x^1 + f x^2 \end{bmatrix}
    = \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \in \mathbb{R}^3
    $$

    **Remark.** Standard basis vectors of $\mathbb{R}^2$: &nbsp; $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

    $$
    A\vec{e}_1 = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix}
    = \underbrace{\begin{bmatrix} a \\ c \\ e \end{bmatrix}}_{\text{1st column of } A} \in \mathbb{R}^3
    \qquad \qquad
    A\vec{e}_2 = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    = \underbrace{\begin{bmatrix} b \\ d \\ f \end{bmatrix}}_{\text{2nd column of } A} \in \mathbb{R}^3
    $$

    In general: $A \in \mathrm{Mat}(m \times n)$

    $$
    A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix}, \qquad
    \vec{A}_i = \begin{bmatrix} A^1{}_i \\ A^2{}_i \\ \vdots \\ A^m{}_i \end{bmatrix} = A\vec{e}_i \in \mathbb{R}^m
    $$

    where $\vec{e}_i \in \mathbb{R}^n$ is the std basis of $\mathbb{R}^n$ (only one non-zero entry)

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}
    $$

    Columns of $A$ are the images of the std basis vectors via $A$!
    """)
    return


@app.cell(hide_code=True)
def _(Arc, Figure, GREEN, RED, arrow, definition, mo, theorem):
    _fig = Figure(figsize=(4.4, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _a1, _a2 = (2.6, -0.5), (2.0, 1.3)
    _ax.fill([0, _a1[0], _a1[0] + _a2[0], _a2[0]], [0, _a1[1], _a1[1] + _a2[1], _a2[1]], color=GREEN, alpha=0.3, lw=0)
    _ax.plot([_a1[0], _a1[0] + _a2[0], _a2[0]], [_a1[1], _a1[1] + _a2[1], _a2[1]], color="#888888", lw=1)
    # foot of the height from the tip of A2 onto the A1 direction
    _t = (_a1[0] * _a2[0] + _a1[1] * _a2[1]) / (_a1[0] ** 2 + _a1[1] ** 2)
    _ax.plot([_a2[0], _t * _a1[0]], [_a2[1], _t * _a1[1]], "--", color="black", lw=1.3)
    arrow(_ax, (0, 0), _a1, RED)
    arrow(_ax, (0, 0), _a2, "#1a237e")
    _ax.annotate(r"$\vec{A}_1$", _a1, xytext=(6, -6), textcoords="offset points", color=RED, fontsize=18, va="top")
    _ax.annotate(r"$\vec{A}_2$", _a2, xytext=(-4, 6), textcoords="offset points", color="#1a237e", fontsize=18, ha="right", va="bottom")
    _ax.add_patch(Arc((0, 0), 1.1, 1.1, theta1=-10.9, theta2=33, color="black", lw=1.2))
    _ax.text(0.7, 0.05, r"$\theta$", fontsize=15)
    _ax.set_xlim(-0.2, 5.3)
    _ax.set_ylim(-0.9, 1.9)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(
                r"""
    ## 4 &nbsp; Determinants, areas and volumes, and the cross-product in $\mathbb{R}^3$

    Let's focus, for now, on square matrices $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; linear transformations $A : \mathbb{R}^n \longrightarrow \mathbb{R}^n$ &nbsp; (mainly for $n = 2$ and $n = 3$)

    ### $n = 2$
    """
            ),
            definition(
                r"""
    Given a $2 \times 2$ matrix

    $$
    A = \begin{bmatrix} A^1{}_1 & A^1{}_2 \\ A^2{}_1 & A^2{}_2 \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    $$

    the **determinant** of $A$ is the real number

    $$
    \det A = A^1{}_1 A^2{}_2 - A^1{}_2 A^2{}_1 = ad - bc
    $$
    """
            ),
            mo.md(
                r"""
    - one of the main characteristics of a matrix
    - use to determine if $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ admits an inverse
    - measure of how $A$ “deforms” areas in $\mathbb{R}^2$
    """
            ),
            theorem(
                r"""
    For $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

    $$
    \lvert \det A \rvert = \text{area of parallelogram spanned by the columns of } A
    $$
    """
            ),
            mo.hstack(
                [
                    mo.md(
                        r"""
    **Proof.** &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$

    If either column is zero, both the area and determinant are zero. Otherwise:

    $$
    \begin{aligned}
    \text{area} &= (\text{base length}) \times (\text{height}) \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\theta, \qquad \theta \in [0, \pi]
    \end{aligned}
    $$
    """
                    ),
                    _fig,
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
            mo.md(
                r"""
    $$
    \begin{aligned}
    \text{area} &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big) \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \Big( 1 - \cos\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \Big)^{1/2} \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \left( 1 - \left( \frac{\vec{A}_1 \cdot \vec{A}_2}{\lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert} \right)^{\!2} \right)^{1/2}
    = \Big( \lVert \vec{A}_1 \rVert^2 \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2 \Big)^{1/2} \\
    &= \Big( (a^2 + c^2)(b^2 + d^2) - (ab + cd)^2 \Big)^{1/2} \\
    &= \Big( \cancel{a^2 b^2} + a^2 d^2 + c^2 b^2 + \cancel{c^2 d^2} - \cancel{a^2 b^2} - \cancel{c^2 d^2} - 2abcd \Big)^{1/2} \\
    &= \big( a^2 d^2 - 2abcd + b^2 c^2 \big)^{1/2} = \big( (ad - bc)^2 \big)^{1/2} = \lvert \det A \rvert \qquad \square
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, definition, mo, theorem):
    from mpl_toolkits.mplot3d import proj3d as _proj3d

    _A1, _A2, _A3 = (2.0, 0.0, 0.0), (0.6, 1.8, 0.0), (0.5, 0.6, 1.6)

    def _add(*vs):
        return tuple(sum(c) for c in zip(*vs))

    _fig = Figure(figsize=(4.6, 3.6), layout="constrained")
    _ax = _fig.add_subplot(projection="3d")
    _O = (0.0, 0.0, 0.0)
    for _v, _col, _starts in (
        (_A1, RED, (_A2, _A3, _add(_A2, _A3))),
        (_A2, GREEN, (_A1, _A3, _add(_A1, _A3))),
        (_A3, BLUE, (_A1, _A2, _add(_A1, _A2))),
    ):
        for _s in _starts:
            _e = _add(_s, _v)
            _ax.plot([_s[0], _e[0]], [_s[1], _e[1]], [_s[2], _e[2]], color=_col, lw=1.3)
    for _v, _col in ((_A1, RED), (_A2, GREEN), (_A3, BLUE)):
        _ax.quiver(*_O, *_v, color=_col, lw=2.4, arrow_length_ratio=0.12)
    _ax.plot([_A3[0], _A3[0]], [_A3[1], _A3[1]], [_A3[2], 0], "--", color="black", lw=1.3)
    _ax.plot([0, _A3[0]], [0, _A3[1]], [0, 0], "--", color="black", lw=1)
    _ax.text(0.28, 0.3, 0.32, r"$\varphi$", fontsize=13)
    _ax.set_box_aspect((3.1, 2.4, 1.6))
    _ax.set_xlim(0, 3.1)
    _ax.set_ylim(0, 2.4)
    _ax.set_zlim(0, 1.6)
    _ax.view_init(elev=20, azim=-62)
    _ax.set_axis_off()
    for _v, _col, _name, _offset, _ha, _va in (
        (_A1, RED, r"$\vec{A}_1$", (0, -8), "center", "top"),
        (_A2, GREEN, r"$\vec{A}_2$", (-8, 7), "right", "bottom"),
        (_A3, BLUE, r"$\vec{A}_3$", (-8, 6), "right", "bottom"),
    ):
        _px, _py, _pz = _proj3d.proj_transform(*_v, _ax.get_proj())
        _ax.annotate(_name, (_px, _py), xytext=_offset, textcoords="offset points", color=_col, fontsize=15, ha=_ha, va=_va)

    mo.vstack(
        [
            mo.md(r"### $n = 3$"),
            definition(
                r"""
    Given a $3 \times 3$ matrix

    $$
    A = \begin{bmatrix} A^1{}_1 & A^1{}_2 & A^1{}_3 \\ A^2{}_1 & A^2{}_2 & A^2{}_3 \\ A^3{}_1 & A^3{}_2 & A^3{}_3 \end{bmatrix}
    = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \in \mathrm{Mat}(3 \times 3)
    $$

    the **determinant** of $A$ is the real number

    $$
    \det A = a \det \begin{bmatrix} e & f \\ h & i \end{bmatrix} - b \det \begin{bmatrix} d & f \\ g & i \end{bmatrix} + c \det \begin{bmatrix} d & e \\ g & h \end{bmatrix}
    $$
    """
            ),
            mo.md(
                r"""
    $$
    \textcolor{#b3261e}{\begin{bmatrix} a & - & - \\ | & e & f \\ | & h & i \end{bmatrix}}
    \qquad
    \textcolor{#1b458f}{\begin{bmatrix} - & b & - \\ d & | & f \\ g & | & i \end{bmatrix}}
    \qquad
    \textcolor{#2e7d32}{\begin{bmatrix} - & - & c \\ d & e & | \\ g & h & | \end{bmatrix}}
    $$

    Note the negative sign!!!
    """
            ),
            theorem(
                r"""
    For $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

    $$
    \lvert \det A \rvert = \text{volume of the parallelepiped spanned by the columns of } A
    $$
    """
            ),
            mo.hstack(
                [
                    mo.md(
                        r"""
    **Proof sketch.**

    $$
    A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \vec{A}_3 \end{bmatrix}, \quad
    \vec{A}_1 = \begin{bmatrix} a \\ d \\ g \end{bmatrix}, \
    \vec{A}_2 = \begin{bmatrix} b \\ e \\ h \end{bmatrix}, \
    \vec{A}_3 = \begin{bmatrix} c \\ f \\ i \end{bmatrix}
    $$

    If $\vec{A}_1, \vec{A}_2$ are linearly dependent or $\vec{A}_3 = \vec{0}$, both the volume and determinant are zero. Otherwise:

    $$
    \begin{aligned}
    \text{volume} &= (\text{base area}) \times \text{height} \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\theta \times \lVert \vec{A}_3 \rVert \sin\varphi
    \end{aligned}
    $$
    """
                    ),
                    _fig,
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
            mo.md(
                r"""
    $\varphi$ is the angle between a vector and a plane — we will need to define this more precisely!

    $$
    \text{volume} = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert\, \lVert \vec{A}_3 \rVert \sin\theta \sin\varphi = \cdots = \lvert \det A \rvert
    $$

    **Remark.** We can continue up in dimension!

    - $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; $\det A$ gets complicated quickly! But it can be defined!
    - $\lvert \det A \rvert = n$-volume of the $n$-parallelepiped spanned by its $n$ columns!
    - Let's not do this explicitly!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear admits an **inverse** iff $\det A \neq 0$.

    - as a function: $\exists\, B : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ s.t. $A \circ B = B \circ A = \mathrm{id}_{\mathbb{R}^2}$, i.e. $A \circ B(\vec{x}) = B \circ A(\vec{x}) = \vec{x} \quad \forall\, \vec{x} \in \mathbb{R}^2$
    - as a matrix: $\exists\, B \in \mathrm{Mat}(2 \times 2)$ s.t. $AB = BA = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$
    """
            ),
            mo.md(
                r"""
    **Proof** (brute force!). &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \quad B = \begin{bmatrix} e & f \\ g & h \end{bmatrix}$

    $$
    AB = \begin{bmatrix} ae + bg & af + bh \\ ce + dg & cf + dh \end{bmatrix}
    = BA = \begin{bmatrix} ea + fc & eb + fd \\ ga + hc & gb + hd \end{bmatrix}
    = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
    $$

    $$
    \Longleftrightarrow \quad ad - bc \neq 0 \quad \text{and} \quad e = \frac{d}{ad - bc}, \quad f = -\frac{b}{ad - bc}, \quad g = -\frac{c}{ad - bc}, \quad h = \frac{a}{ad - bc}
    $$

    $\therefore$ &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ admits inverse iff $\det A = ad - bc \neq 0$ &nbsp; $\leadsto$ &nbsp; the inverse is

    $$
    B = A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \qquad \square
    $$

    Key intuition:

    $$
    A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \quad \Longrightarrow \quad
    \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix} = A\vec{e}_1, \quad
    \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix} = A\vec{e}_2
    $$

    $\Longrightarrow$ &nbsp; parallelogram spanned by $\vec{A}_1, \vec{A}_2$ is the image of the unit square spanned by $\vec{e}_1, \vec{e}_2$
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
    md = mo.ui.slider(-3, 3, 0.5, value=2, label="$d$", show_value=True)
    return ma, mb, mc, md


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, arrow, ma, math, mb, mc, md, mo, plane):
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c

    def _turn(ax, p, q, ccw, radius):
        """Curved arrow from the direction of p to the direction of q."""
        t1, t2 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
        start = (radius * math.cos(t1), radius * math.sin(t1))
        end = (radius * math.cos(t2), radius * math.sin(t2))
        arrow(ax, start, end, BLUE, lw=1.4, connectionstyle=f"arc3,rad={0.35 if ccw else -0.35}")

    _fig = Figure(figsize=(9.2, 4.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    plane(_left, 2.2)
    _left.fill([0, 1, 1, 0], [0, 0, 1, 1], color=BLUE, alpha=0.2, lw=0)
    arrow(_left, (0, 0), (1, 0), RED)
    arrow(_left, (0, 0), (0, 1), GREEN)
    _turn(_left, (1, 0), (0, 1), True, 0.45)
    _left.set_title("area $= 1$,  counter-clockwise")

    plane(_right, 3.5 if max(abs(_a + _b), abs(_c + _d)) <= 3 else 6.5)
    _right.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=BLUE, alpha=0.2, lw=0)
    _right.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color="#888888", lw=1)
    arrow(_right, (0, 0), (_a, _c), RED)
    arrow(_right, (0, 0), (_b, _d), GREEN)
    if _det != 0:
        _r = 0.45 * min(math.hypot(_a, _c), math.hypot(_b, _d), 2.0)
        _turn(_right, (_a, _c), (_b, _d), _det > 0, max(_r, 0.3))
        _direction = "counter-clockwise" if _det > 0 else "clockwise"
    else:
        _direction = "collapsed"
    _right.set_title(rf"area $= |\det A| = {abs(_det):g}$,  {_direction}")

    for _ax, _labels in ((_left, (r"$\vec{e}_1$", r"$\vec{e}_2$")), (_right, (r"$\vec{A}_1$", r"$\vec{A}_2$"))):
        for _color, _label in zip((RED, GREEN), _labels):
            _ax.plot([], [], color=_color, lw=2.2, label=_label)
        _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=12)

    det_explorer = mo.vstack(
        [
            mo.hstack(
                [
                    mo.vstack([ma, mc]),
                    mo.vstack([mb, md]),
                    mo.md(
                        rf"$A = \begin{{bmatrix}} {_a:g} & {_b:g} \\ {_c:g} & {_d:g} \end{{bmatrix}}, \qquad \det A = {_det:g}$"
                    ),
                ],
                justify="start",
                gap=3,
                align="center",
            ),
            _fig,
        ]
    )
    det_explorer
    return (det_explorer,)


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    If $\det A = 0$ &nbsp; $\Longrightarrow$ &nbsp; $A$ “collapses” the unit square into a line segment (or zero) &nbsp; $\leadsto$ &nbsp; a parallelogram of area zero

    $\Longrightarrow$ &nbsp; $A$ cannot be invertible &nbsp; $\leadsto$ &nbsp; we cannot “recover” the square from a line segment! (not bijective)

    If $\det A \neq 0$ &nbsp; $\Longrightarrow$ &nbsp; $A$ deforms the unit square without “collapse” &nbsp; $\leadsto$ &nbsp; linearity is then enough for us to find the inverse!
    """
            ),
            theorem(
                r"""
    For every $n \in \mathbb{Z}_{>0}$

    $$
    A \in \mathrm{Mat}(n \times n) \quad \leftrightsquigarrow \quad A : \mathbb{R}^n \longrightarrow \mathbb{R}^n \ \text{ linear}
    $$

    admits an inverse iff $\det A \neq 0$!
    """
            ),
            mo.md(r"What about the sign of the determinant?"),
            theorem(
                r"""
    $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

    If $\det A > 0$, $A$ preserves the direction of rotations around the origin.

    If $\det A < 0$, $A$ reverses the direction of rotations around the origin.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the explorer above to compare positive and negative determinants.
    """)
    return


@app.cell(hide_code=True)
def _(Figure, mo):
    _fig = Figure(figsize=(3.0, 2.8), layout="constrained")
    _ax = _fig.add_subplot(projection="3d")
    for _d, _name in (((1, 0, 0), r"$\vec{e}_1$"), ((0, 1, 0), r"$\vec{e}_2$"), ((0, 0, 1), r"$\vec{e}_3$")):
        _ax.quiver(0, 0, 0, *_d, color="black", lw=1.8, arrow_length_ratio=0.15)
        _ax.text(*[1.12 * _c for _c in _d], _name, fontsize=15, ha="center")
    _ax.set_xlim(0, 1.3)
    _ax.set_ylim(0, 1.3)
    _ax.set_zlim(0, 1.3)
    _ax.view_init(elev=22, azim=28)
    _ax.set_axis_off()

    mo.vstack(
        [
            mo.md(
                r"""
    $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

    If $\det A > 0$, $A$ preserves “handedness” of orthogonal frames (triples of pairwise orthogonal vectors).

    If $\det A < 0$, $A$ reverses “handedness”.
    """
            ),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"""
    **Right-hand rule:** $\vec{e}_1, \vec{e}_2, \vec{e}_3$ have positive “handedness” (orientation):

    if rotating fingers from $\vec{e}_1$ to $\vec{e}_2$, your thumb points to $\vec{e}_3$.
    """
                    ),
                ],
                widths=[1, 2],
                gap=2,
                align="center",
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
