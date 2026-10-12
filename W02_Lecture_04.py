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
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the particle, the point, the chosen vector)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (velocity, relative velocity, tangent vector)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (equator, light cone, inertial comparison)
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
    header("Lecture 04", "Week 02", "Lecture 04 · Determinants, areas and volumes")
    return


@app.cell(hide_code=True)
def _(arrow, math):
    def vector(ax, tail, tip, color, label=None, turn=0, r=15, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip on a white box;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            arrow(ax, tail, tip, color, **kw)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    return (vector,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - matrices $A \in \mathrm{Mat}(m \times n)$ &nbsp; $\leadsto$ &nbsp; linear transformation $A : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\vec{x} \longmapsto A\vec{x}$ via matrix multiplication

        $$
        A = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \in \mathrm{Mat}(3 \times 2), \quad
        \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2
        \quad \Longrightarrow \quad A\vec{x}
        = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \\ e x^1 + f x^2 \end{bmatrix}
        = \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \in \mathbb{R}^3
        $$

    - standard basis vectors of $\mathbb{R}^2$: &nbsp; $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

        $$
        A\vec{e}_1 = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix}
        = \underbrace{\begin{bmatrix} a \\ c \\ e \end{bmatrix}}_{\text{1st column of } A} \in \mathbb{R}^3
        \qquad \qquad
        A\vec{e}_2 = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix}
        = \underbrace{\begin{bmatrix} b \\ d \\ f \end{bmatrix}}_{\text{2nd column of } A} \in \mathbb{R}^3
        $$

    - in general, $A \in \mathrm{Mat}(m \times n)$: &nbsp; $A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix}$, &nbsp; $\vec{A}_i = A\vec{e}_i \in \mathbb{R}^m$, where $\vec{e}_i \in \mathbb{R}^n$ is the standard basis of $\mathbb{R}^n$ (only one non-zero entry)
    - $\leadsto$ &nbsp; columns of $A$ are the images of the standard basis vectors via $A$!

    **Today:** determinants of square matrices: areas, volumes, inverses and orientation
    """)
    return


@app.cell(hide_code=True)
def _(Arc, BLUE, GREEN, GREY, HALF, LIGHT, RED, arrow, blank, definition, math, mo, theorem):
    _fig, _ax = blank(HALF, 2.1, (-0.5, 5.3), (-1.1, 2.0))
    _a1, _a2 = (2.6, -0.5), (2.0, 1.3)
    _ax.fill([0, _a1[0], _a1[0] + _a2[0], _a2[0]], [0, _a1[1], _a1[1] + _a2[1], _a2[1]], color=LIGHT, lw=0)
    _ax.plot([_a1[0], _a1[0] + _a2[0], _a2[0]], [_a1[1], _a1[1] + _a2[1], _a2[1]], color="black", lw=1.0)
    # the height: from the tip of A2 to its foot on the A1 direction, with a right-angle mark
    _t = (_a1[0] * _a2[0] + _a1[1] * _a2[1]) / (_a1[0] ** 2 + _a1[1] ** 2)
    _foot = (_t * _a1[0], _t * _a1[1])
    _ax.plot([_a2[0], _foot[0]], [_a2[1], _foot[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _n1 = math.hypot(*_a1)
    _u, _v = (_a1[0] / _n1, _a1[1] / _n1), (-_a1[1] / _n1, _a1[0] / _n1)
    _s = 0.14
    _ax.plot(
        [_foot[0] - _s * _u[0], _foot[0] - _s * _u[0] + _s * _v[0], _foot[0] + _s * _v[0]],
        [_foot[1] - _s * _u[1], _foot[1] - _s * _u[1] + _s * _v[1], _foot[1] + _s * _v[1]],
        color=GREY,
        lw=0.8,
    )
    arrow(_ax, (0, 0), _a1, BLUE)
    arrow(_ax, (0, 0), _a2, RED)
    _ax.text(_a1[0] / 2, _a1[1] / 2 - 0.16, r"$\vec{A}_1$", color=BLUE, fontsize=13, ha="center", va="top")
    _ax.text(_a2[0] / 2 - 0.12, _a2[1] / 2 + 0.14, r"$\vec{A}_2$", color=RED, fontsize=13, ha="right", va="bottom")
    _th1, _th2 = math.degrees(math.atan2(_a1[1], _a1[0])), math.degrees(math.atan2(_a2[1], _a2[0]))
    _ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=_th1, theta2=_th2, color=GREEN, lw=1.4))
    _ax.text(0.82, 0.12, r"$\theta$", color=GREEN, fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.4 &nbsp; Determinants, areas and volumes, and the cross-product in $\mathbb{R}^3$

    Let's focus, for now, on square matrices $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; linear transformations $A : \mathbb{R}^n \longrightarrow \mathbb{R}^n$ &nbsp; (mainly for $n = 2$ and $n = 3$)

    ### $n = 2$: determinants and areas
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
    """,
                r"Determinant of a $2 \times 2$ matrix",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; one of the main characteristics of a matrix

    $\leadsto$ &nbsp; use to determine if $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ admits an inverse

    $\leadsto$ &nbsp; measure of how $A$ “deforms” areas in $\mathbb{R}^2$
    """
            ),
            theorem(
                r"""
    For $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

    $$
    \lvert \det A \rvert = \text{area of parallelogram spanned by the columns of } A
    $$
    """,
                "Determinant and area",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$
    """
            ),
            _fig,
            mo.md(
                r"""
    If either column is zero, both the area and determinant are zero. Otherwise

    $$
    \begin{aligned}
    \text{area} &= (\text{base length}) \times (\text{height}) = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big) \qquad (\theta \in [0, \pi]) \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \Big( 1 - \cos\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \Big)^{1/2}
    = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \left( 1 - \left( \frac{\vec{A}_1 \cdot \vec{A}_2}{\lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert} \right)^{\!2} \right)^{1/2} \\
    &= \Big( \lVert \vec{A}_1 \rVert^2 \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2 \Big)^{1/2}
    = \Big( (a^2 + c^2)(b^2 + d^2) - (ab + cd)^2 \Big)^{1/2} \\
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
def _(Arc, BLUE, GREEN, GREY, HALF, ORANGE, RED, arrow, blank, definition, math, mo, np, theorem):
    # A parallelepiped in perspective: visible edges solid, the three edges behind it dashed
    _az, _el = math.radians(-120), math.radians(20)

    def _pr(p):
        x, y, z = p
        X = -x * math.sin(_az) + y * math.cos(_az)
        Y = z * math.cos(_el) - (x * math.cos(_az) + y * math.sin(_az)) * math.sin(_el)
        D = (x * math.cos(_az) + y * math.sin(_az)) * math.cos(_el) + z * math.sin(_el)
        return X, Y, D

    _A = [np.array(v) for v in ((2.0, 0.0, 0.0), (0.3, 2.4, 0.0), (1.0, 0.2, 1.5))]
    _O = np.zeros(3)
    _verts = {(i, j, k): i * _A[0] + j * _A[1] + k * _A[2] for i in (0, 1) for j in (0, 1) for k in (0, 1)}
    _eye = np.array([math.cos(_el) * math.cos(_az), math.cos(_el) * math.sin(_az), math.sin(_el)])

    def _is_hidden(c):
        """A vertex is hidden when the three faces meeting at it all face away from the eye."""
        for k in range(3):
            i, j = [n for n in range(3) if n != k]
            n_out = np.cross(_A[i], _A[j])
            n_out = n_out * np.sign(n_out @ _A[k]) * (1 if c[k] == 1 else -1)
            if n_out @ _eye > 0:
                return False
        return True

    _back = next(c for c in _verts if _is_hidden(c))

    _fig, _ax = blank(HALF, 2.9, (-1.5, 2.9), (-0.5, 3.05))
    for _c, _p in _verts.items():
        for _axis in range(3):
            if _c[_axis] == 0:
                _c2 = tuple(1 if n == _axis else v for n, v in enumerate(_c))
                if _c == (0, 0, 0):
                    continue  # the three edges at the origin are the arrows drawn below
                _hidden = _back in (_c, _c2)
                _P, _Q = _pr(_p), _pr(_verts[_c2])
                _ax.plot([_P[0], _Q[0]], [_P[1], _Q[1]], color="black", lw=0.7 if _hidden else 1.0, ls=(0, (3, 3)) if _hidden else "-")
    _foot = np.array([_A[2][0], _A[2][1], 0.0])
    _T, _F = _pr(_A[2]), _pr(_foot)
    _ax.plot([_T[0], _F[0]], [_T[1], _F[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([0, _F[0]], [0, _F[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    for _v, _col in zip(_A, (BLUE, RED, ORANGE)):
        arrow(_ax, (0, 0), _pr(_v)[:2], _col)
    _ax.add_patch(Arc((0, 0), 1.1, 1.1, theta1=math.degrees(math.atan2(_F[1], _F[0])), theta2=math.degrees(math.atan2(_T[1], _T[0])), color=GREEN, lw=1.4))
    _ax.text(0.52, 0.52, r"$\varphi$", color=GREEN, fontsize=13, ha="left", va="center")
    _P1, _P2 = _pr(_A[0]), _pr(_A[1])
    _ax.text(_P1[0] / 2, _P1[1] / 2 - 0.14, r"$\vec{A}_1$", color=BLUE, fontsize=13, ha="center", va="top")
    _ax.text(_P2[0] / 2 - 0.05, _P2[1] / 2 - 0.14, r"$\vec{A}_2$", color=RED, fontsize=13, ha="right", va="top")
    _ax.text(_T[0] / 2 - 0.14, _T[1] / 2 + 0.2, r"$\vec{A}_3$", color=ORANGE, fontsize=13, ha="right", va="bottom")

    mo.vstack(
        [
            mo.md(r"""### $n = 3$: determinants and volumes"""),
            definition(
                r"""
    Given a $3 \times 3$ matrix

    $$
    A = \begin{bmatrix} A^1{}_1 & A^1{}_2 & A^1{}_3 \\ A^2{}_1 & A^2{}_2 & A^2{}_3 \\ A^3{}_1 & A^3{}_2 & A^3{}_3 \end{bmatrix}
    = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \in \mathrm{Mat}(3 \times 3)
    $$

    the **determinant** of $A$ is the real number

    $$
    \det A = a \det \begin{bmatrix} e & f \\ h & i \end{bmatrix} \underbrace{{} - b \det \begin{bmatrix} d & f \\ g & i \end{bmatrix}}_{\text{note the negative sign!}} + c \det \begin{bmatrix} d & e \\ g & h \end{bmatrix}
    $$
    """,
                r"Determinant of a $3 \times 3$ matrix",
            ),
            mo.md(
                r"""
    $$
    \begin{bmatrix} a & - & - \\ | & e & f \\ | & h & i \end{bmatrix}
    \qquad
    \begin{bmatrix} - & b & - \\ d & | & f \\ g & | & i \end{bmatrix}
    \qquad
    \begin{bmatrix} - & - & c \\ d & e & | \\ g & h & | \end{bmatrix}
    $$
    """
            ),
            theorem(
                r"""
    For $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

    $$
    \lvert \det A \rvert = \text{volume of the parallelepiped spanned by the columns of } A
    $$
    """,
                "Determinant and volume",
            ),
            mo.md(
                r"""
    **Proof** (sketch).

    $$
    A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \vec{A}_3 \end{bmatrix}, \quad
    \vec{A}_1 = \begin{bmatrix} a \\ d \\ g \end{bmatrix}, \
    \vec{A}_2 = \begin{bmatrix} b \\ e \\ h \end{bmatrix}, \
    \vec{A}_3 = \begin{bmatrix} c \\ f \\ i \end{bmatrix}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \begin{aligned}
    \text{volume} &= (\text{base area}) \times \text{height} = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\theta \times \lVert \vec{A}_3 \rVert \sin\varphi \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert\, \lVert \vec{A}_3 \rVert \sin\theta \sin\varphi = \cdots = \lvert \det A \rvert \qquad \square
    \end{aligned}
    $$

    ($\varphi$ = angle between a vector and a plane: we will need to define this more precisely!)

    **Remark.** We can continue up in dimension!

    - $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; $\det A$ gets complicated quickly, but it can be defined!
    - $\lvert \det A \rvert = n$-volume of the $n$-parallelepiped spanned by its $n$ columns!
    - let's not do this explicitly!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Determinants and inverses"""),
            theorem(
                r"""
    $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear admits an **inverse** if and only if $\det A \neq 0$.

    - as a function: $\exists\, B : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ such that $A \circ B = B \circ A = \mathrm{id}_{\mathbb{R}^2}$, that is, $A \circ B(\vec{x}) = B \circ A(\vec{x}) = \vec{x} \quad \forall\, \vec{x} \in \mathbb{R}^2$
    - as a matrix: $\exists\, B \in \mathrm{Mat}(2 \times 2)$ such that $AB = BA = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$
    """,
                r"Inverse of a $2 \times 2$ matrix",
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

    $\therefore$ &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ admits inverse if and only if $\det A = ad - bc \neq 0$ &nbsp; $\leadsto$ &nbsp; the inverse is

    $$
    B = A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \qquad \square
    $$

    $\leadsto$ &nbsp; key intuition:

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
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, RED, arrow, ma, math, mb, mc, md, mo, plane, table, vector):
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c

    def _turn(ax, p, q, ccw, radius):
        """Curved arrow from the direction of p to the direction of q."""
        t1, t2 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
        start = (radius * math.cos(t1), radius * math.sin(t1))
        end = (radius * math.cos(t2), radius * math.sin(t2))
        arrow(ax, start, end, GREEN, connectionstyle=f"arc3,rad={0.35 if ccw else -0.35}")

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    plane(_left, 2.2)
    _left.set_xticks(range(-2, 3))
    _left.set_yticks(range(-2, 3))
    _left.fill([0, 1, 1, 0], [0, 0, 1, 1], color=LIGHT, lw=0)
    _left.plot([1, 1, 0], [0, 1, 1], color=GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_left, (0, 0), (1, 0), BLUE, r"$\vec{e}_1$", -75)
    vector(_left, (0, 0), (0, 1), RED, r"$\vec{e}_2$", 75)
    _turn(_left, (1, 0), (0, 1), True, 0.45)

    _small = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_a + _b), abs(_c + _d)) <= 3
    plane(_right, 4.4 if _small else 7.6)  # the frame follows the parallelogram: nothing is clipped
    _ticks = range(-4, 5, 2) if _small else range(-6, 7, 3)
    _right.set_xticks(_ticks)
    _right.set_yticks(_ticks)
    _right.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=LIGHT, lw=0)
    _right.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _side = -1 if _det < 0 else 1  # labels go on the outer side of each arrow
    vector(_right, (0, 0), (_a, _c), BLUE, r"$\vec{A}_1$", -75 * _side)
    vector(_right, (0, 0), (_b, _d), RED, r"$\vec{A}_2$", 75 * _side)
    if _det != 0:
        _r = 0.45 * min(math.hypot(_a, _c), math.hypot(_b, _d), 2.0)
        _turn(_right, (_a, _c), (_b, _d), _det > 0, max(_r, 0.3))
        _direction = rf"$\textcolor{{{GREEN}}}{{\text{{{'counter-clockwise' if _det > 0 else 'clockwise'}}}}}$"
    else:
        _direction = r"need $\det A \neq 0$"

    mo.vstack(
        [
            mo.hstack([ma, mb, mc, md], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$", rf"$\begin{{bmatrix}} \textcolor{{{BLUE}}}{{{_a:g}}} & \textcolor{{{RED}}}{{{_b:g}}} \\ \textcolor{{{BLUE}}}{{{_c:g}}} & \textcolor{{{RED}}}{{{_d:g}}} \end{{bmatrix}}$"),
                    (r"$\det A = ad - bc$", rf"$({_a:g})({_d:g}) - ({_b:g})({_c:g}) = {_det:g}$"),
                    (r"area of $A$(unit square) $= \lvert \det A \rvert$", rf"${abs(_det):g}$"),
                    (r"turn from $\vec{A}_1$ to $\vec{A}_2$", _direction),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(GREEN, HALF, arrow, blank, mo, theorem):
    def _pr(x1, x2, x3):
        """Oblique projection of R^3, as on the board: x^2 to the right, x^3 up, x^1 towards the viewer."""
        return x2 - 0.45 * x1, x3 - 0.4 * x1

    _fig, _ax = blank(HALF, 2.2, (-1.6, 2.2), (-1.0, 1.6))
    _e1 = _pr(1.5, 0, 0)
    arrow(_ax, _pr(-0.4, 0, 0), _e1, "black")
    arrow(_ax, (-0.4, 0), (1.3, 0), "black")
    arrow(_ax, (0, -0.4), (0, 1.3), "black")
    _ax.text(_e1[0] - 0.1, _e1[1] - 0.02, r"$\vec{e}_1$", fontsize=13, ha="right", va="center")
    _ax.text(1.4, 0, r"$\vec{e}_2$", fontsize=13, ha="left", va="center")
    _ax.text(0, 1.38, r"$\vec{e}_3$", fontsize=13, ha="center", va="bottom")
    _s, _t = _pr(0.75, 0, 0), (0.62, 0)
    arrow(_ax, (_s[0] + 0.06, _s[1] - 0.08), (_t[0], _t[1] - 0.1), GREEN, connectionstyle="arc3,rad=0.45")  # fingers rotate from e1 to e2

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

    admits an inverse if and only if $\det A \neq 0$!
    """,
                r"Inverse of an $n \times n$ matrix",
            ),
            mo.md(
                r"""
    ### The sign of the determinant

    $\leadsto$ &nbsp; what about the sign of the determinant?
    """
            ),
            theorem(
                r"""
    $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

    - if $\det A > 0$, $A$ preserves the direction of rotations around the origin
    - if $\det A < 0$, $A$ reverses the direction of rotations around the origin

    $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

    - if $\det A > 0$, $A$ preserves “handedness” of orthogonal frames (triples of pairwise orthogonal vectors)
    - if $\det A < 0$, $A$ reverses “handedness”
    """,
                "Sign of the determinant",
            ),
            mo.md(
                r"""
    **Right-hand rule:** $\vec{e}_1, \vec{e}_2, \vec{e}_3$ have positive “handedness” (orientation): if rotating fingers from $\vec{e}_1$ to $\vec{e}_2$, your thumb points to $\vec{e}_3$
    """
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - for $A \in \mathrm{Mat}(2 \times 2)$, $\det A = ad - bc$ and $\lvert \det A \rvert$ = area of the parallelogram spanned by the columns of $A$ = area of the image of the unit square
    - for $A \in \mathrm{Mat}(3 \times 3)$, $\det A$ is defined via three $2 \times 2$ determinants (note the negative sign) and $\lvert \det A \rvert$ = volume of the parallelepiped spanned by the columns of $A$
    - $A \in \mathrm{Mat}(n \times n)$ admits an inverse if and only if $\det A \neq 0$
    - $\det A > 0$ preserves, and $\det A < 0$ reverses, the direction of rotations ($n = 2$) or the “handedness” of orthogonal frames ($n = 3$)

    **Next:** lines and planes and the cross-product in $\mathbb{R}^3$
    """)
    return


if __name__ == "__main__":
    app.run()
