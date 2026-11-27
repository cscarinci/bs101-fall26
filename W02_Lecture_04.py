import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 4 · Determinants, areas and volumes", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Arc, Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(4, "Determinants, areas and volumes")
    return


@app.cell(hide_code=True)
def _(Arc, Figure, lk, math):
    # Helpers of this lecture: bare sketches, coordinate planes, labelled vectors

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=lk.LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def vector(ax, tail, tip, color, label=None, turn=0, r=15):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip (no box behind the label);
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            lk.arrow(ax, tail, tip, color)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5)

    def turn(ax, p, q, ccw, radius):
        """Circular arc from the direction of p to the direction of q (counterclockwise when ccw), with a head at its end."""
        t1, t2 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
        span = (t2 - t1) % (2 * math.pi) if ccw else -((t1 - t2) % (2 * math.pi))
        lo, hi = (t1, t1 + span) if ccw else (t1 + span, t1)
        ax.add_patch(Arc((0, 0), 2 * radius, 2 * radius, theta1=math.degrees(lo), theta2=math.degrees(hi), color=lk.GREEN, lw=1.4))
        end = (radius * math.cos(t2), radius * math.sin(t2))
        step = math.copysign(min(0.35 * abs(span), 0.2), span)
        back = (radius * math.cos(t2 - step), radius * math.sin(t2 - step))
        d = (end[0] - back[0], end[1] - back[1])
        n = math.hypot(*d)  # the head follows the chord of the last part of the arc
        lk.arrow(ax, (end[0] - 1e-3 * d[0] / n, end[1] - 1e-3 * d[1] / n), end, lk.GREEN)

    return blank, plane, turn, vector


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    ma = lk.slider(-3, 3, step=0.5, value=2, label="$a$")
    mb = lk.slider(-3, 3, step=0.5, value=1, label="$b$")
    mc = lk.slider(-3, 3, step=0.5, value=0.5, label="$c$")
    md = lk.slider(-3, 3, step=0.5, value=2, label="$d$")
    return ma, mb, mc, md


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: matrices as linear transformations, their columns as images of the standard basis
    _A = r"\begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix}"
    lk.recap(
        lk.gap(),
        r"$A = " + _A + r" \in \mathrm{Mat}(3 \times 2), \qquad \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2$",
        r"> $\Longrightarrow$ &nbsp; $A\vec{x} = " + _A + r" \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \\ e x^1 + f x^2 \end{bmatrix} = \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \in \mathbb{R}^3$",
        lk.gap(),
        r"standard basis vectors of $\mathbb{R}^2$: &nbsp; $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$",
        lk.aside(r"> $A\vec{e}_1 = " + _A + r" \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \mk{\begin{bmatrix} a \\ c \\ e \end{bmatrix}} \in \mathbb{R}^3$", "1st column of $A$"),
        lk.aside(r"> $A\vec{e}_2 = " + _A + r" \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \mk{\begin{bmatrix} b \\ d \\ f \end{bmatrix}} \in \mathbb{R}^3$", "2nd column of $A$"),
        lk.gap(),
        r"in general: &nbsp; $A \in \mathrm{Mat}(m \times n)$",
        lk.aside(
            r"> $A = \begin{bmatrix} \mk{\vec{A}_1} & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix}, \quad \vec{A}_i = A\vec{e}_i \in \mathbb{R}^m$",
            r"$\vec{A}_i = \begin{bmatrix} A^1{}_i \\ \vdots \\ A^m{}_i \end{bmatrix}$",
        ),
        lk.aside(
            r"> > where $\vec{e}_i \in \mathbb{R}^n$ standard basis of $\mathbb{R}^n$: &nbsp; $\mk{\vec{e}_1} = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \ \dots, \ \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}$",
            "only one non-zero entry",
        ),
        r"$\leadsto$ &nbsp; columns of $A$ are the images of the standard basis vectors via $A$!",
        topic=r"Matrices $A \in \mathrm{Mat}(m \times n)$ &nbsp; $\leftrightsquigarrow$ &nbsp; linear transformation $A : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, &nbsp; $\vec{x} \longmapsto A\vec{x}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 1.3, 1.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 2
    # section
    lk.section(r"Determinants and areas ($n = 2$)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 2
    # motivation: square matrices
    lk.prose(
        r"""
        Let's focus, for now, on square matrices $A \in \mathrm{Mat}(n \times n)$

        > $\leadsto$ &nbsp; linear transformations $A : \mathbb{R}^n \longrightarrow \mathbb{R}^n$ (mainly for $n = 2$ and $n = 3$)
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 2
    # definition: determinant of a 2 x 2 matrix
    lk.definition(
        r"""
        Given a $2 \times 2$ matrix $A = \begin{bmatrix} A^1{}_1 & A^1{}_2 \\ A^2{}_1 & A^2{}_2 \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$, the **determinant** of $A$ is the real number

        $$
        \det A = A^1{}_1 A^2{}_2 - A^1{}_2 A^2{}_1 = ad - bc.
        $$
        """,
        label="def-det2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 2
    # consequences: what the determinant is for
    lk.prose(
        r"""
        $\leadsto$ &nbsp; one of the main characteristics of a matrix

        $\leadsto$ &nbsp; used to determine if $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ admits an inverse

        $\leadsto$ &nbsp; measure of how $A$ “deforms” areas in $\mathbb{R}^2$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 2
    # theorem: determinant and area
    lk.theorem(
        r"""
        For $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

        $$
        \lvert \det A \rvert = \text{area of parallelogram spanned by the columns of } A.
        $$
        """,
        label="thm-det-area",
    )
    return


@app.cell(hide_code=True)
def _(Arc, blank, lk, math):
    # module: n = 2
    # proof, with the parallelogram spanned by A1, A2, its height and the angle theta
    _fig, _ax = blank(3.6, 2.1, (-0.5, 5.3), (-1.1, 2.0))
    _a1, _a2 = (2.6, -0.5), (2.0, 1.3)
    _ax.fill([0, _a1[0], _a1[0] + _a2[0], _a2[0]], [0, _a1[1], _a1[1] + _a2[1], _a2[1]], color=lk.LIGHT, lw=0)
    _ax.plot([_a1[0], _a1[0] + _a2[0], _a2[0]], [_a1[1], _a1[1] + _a2[1], _a2[1]], color="black", lw=1.0)
    _t = (_a1[0] * _a2[0] + _a1[1] * _a2[1]) / (_a1[0] ** 2 + _a1[1] ** 2)  # the foot of the height on the A1 direction
    _foot = (_t * _a1[0], _t * _a1[1])
    _ax.plot([_a2[0], _foot[0]], [_a2[1], _foot[1]], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _n1 = math.hypot(*_a1)
    _u, _v = (_a1[0] / _n1, _a1[1] / _n1), (-_a1[1] / _n1, _a1[0] / _n1)
    _s = 0.14
    _ax.plot(
        [_foot[0] - _s * _u[0], _foot[0] - _s * _u[0] + _s * _v[0], _foot[0] + _s * _v[0]],
        [_foot[1] - _s * _u[1], _foot[1] - _s * _u[1] + _s * _v[1], _foot[1] + _s * _v[1]],
        color=lk.GREY,
        lw=0.8,
    )
    lk.arrow(_ax, (0, 0), _a1, lk.BLUE)
    lk.arrow(_ax, (0, 0), _a2, lk.RED)
    _ax.text(_a1[0] / 2, _a1[1] / 2 - 0.16, r"$\vec{A}_1$", color=lk.BLUE, fontsize=13, ha="center", va="top")
    _ax.text(_a2[0] / 2 - 0.12, _a2[1] / 2 + 0.14, r"$\vec{A}_2$", color=lk.RED, fontsize=13, ha="right", va="bottom")
    _th1, _th2 = math.degrees(math.atan2(_a1[1], _a1[0])), math.degrees(math.atan2(_a2[1], _a2[0]))
    _ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=_th1, theta2=_th2, color=lk.GREEN, lw=1.4))
    _ax.text(0.82, 0.12, r"$\theta$", color=lk.GREEN, fontsize=13, ha="left", va="center")

    lk.proof(
        [
            r"$A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$",
            lk.aside(
                lk.figure(_fig),
                r"area = (base length) $\times$ (height)<br>= $\lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \sin\theta$",
            ),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \text{area} &= \lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \sin\big(\mk{\theta(\vec{A}_1, \vec{A}_2)}\big)\\[4pt]
                &= \lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \Big( 1 - \cos\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \Big)^{1/2}\\[4pt]
                &= \lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \left( 1 - \left( \frac{\vec{A}_1 \cdot \vec{A}_2}{\lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert} \right)^2 \right)^{1/2}\\[4pt]
                &= \Big( \lVert \vec{A}_1 \rVert^2 \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2 \Big)^{1/2}\\[4pt]
                &= \Big( (a^2 + c^2)(b^2 + d^2) - (ab + cd)^2 \Big)^{1/2}\\[4pt]
                &= \Big( \cancel{a^2 b^2} + a^2 d^2 + c^2 b^2 + \cancel{c^2 d^2} - \cancel{a^2 b^2} - \cancel{c^2 d^2} - 2abcd \Big)^{1/2}\\[4pt]
                &= \big( a^2 d^2 - 2abcd + b^2 c^2 \big)^{1/2} = \big( (ad - bc)^2 \big)^{1/2} = \lvert \det A \rvert
                \end{aligned}
                $$
                """,
                r"$\theta \in [0, \pi]$",
                at=1,
                rows=7,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 3
    # section
    lk.section(r"Determinants and volumes ($n = 3$)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 3
    # definition: determinant of a 3 x 3 matrix, with the crossed-out rows and columns of each term
    lk.definition(
        [
            r"""
            Given a $3 \times 3$ matrix

            $$
            A = \begin{bmatrix} A^1{}_1 & A^1{}_2 & A^1{}_3 \\ A^2{}_1 & A^2{}_2 & A^2{}_3 \\ A^3{}_1 & A^3{}_2 & A^3{}_3 \end{bmatrix} = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \in \mathrm{Mat}(3 \times 3),
            $$

            the **determinant** of $A$ is the real number
            """,
            lk.aside(
                r"$$ \det A = a \det \begin{bmatrix} e & f \\ h & i \end{bmatrix} \mathbin{\mk{-}} b \det \begin{bmatrix} d & f \\ g & i \end{bmatrix} + c \det \begin{bmatrix} d & e \\ g & h \end{bmatrix}, $$",
                "note the negative sign!!!",
            ),
            r"$$ \begin{bmatrix} a & - & - \\ | & e & f \\ | & h & i \end{bmatrix} \qquad \begin{bmatrix} - & b & - \\ d & | & f \\ g & | & i \end{bmatrix} \qquad \begin{bmatrix} - & - & c \\ d & e & | \\ g & h & | \end{bmatrix}. $$",
        ],
        label="def-det3",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 3
    # theorem: determinant and volume
    lk.theorem(
        r"""
        For $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

        $$
        \lvert \det A \rvert = \text{volume of the parallelepiped spanned by the columns of } A.
        $$
        """,
        label="thm-det-volume",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: n = 3
    # proof, with the parallelepiped spanned by the columns, the height of A3 over the base and the two angles: A3 leans
    # over the base, so that its height falls inside the base
    _A = [np.array(v) for v in ((2.0, 0.0, 0.0), (0.3, 2.4, 0.0), (1.0, 0.9, 1.5))]
    _faces, _edges = [], []
    for _k in range(3):
        _p, _q, _r = _A[_k], _A[(_k + 1) % 3], _A[(_k + 2) % 3]
        _faces += [lk.patch([_c, _c + _p, _c + _p + _q, _c + _q], lk.LIGHT, 0.35) for _c in (0 * _r, _r)]
        _edges += [np.array([_c, _c + _p]) for _c in (_q, _r, _q + _r)]  # the edge along p at the origin is an arrow
    _foot = np.array([_A[2][0], _A[2][1], 0.0])

    def _arc(a, b, r):
        """The circular arc of radius r about the origin from the direction of a to the direction of b."""
        a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
        w = np.arccos(a @ b)
        s = np.linspace(0, 1, 40)[:, None]
        return r * (np.sin((1 - s) * w) * a + np.sin(s * w) * b) / np.sin(w)

    _theta, _phi = _arc(_A[0], _A[1], 0.5), _arc(_foot, _A[2], 0.8)
    _fig = lk.turntable(
        -60,
        22,
        "parallelepiped spanned by the columns A1, A2, A3 of A, with the height of A3 over the base, the angle theta between A1 and A2 and the angle phi between A3 and the base",
        [
            lk.panel(
                1.0,
                surfaces=_faces,
                lines=[(_e[:, 0], _e[:, 1], _e[:, 2], "#000000", 1.0) for _e in _edges]
                + [
                    ((_A[2][0], _foot[0]), (_A[2][1], _foot[1]), (_A[2][2], 0), lk.GREY, 1.0, [4, 3]),
                    ((0, _foot[0]), (0, _foot[1]), (0, 0), lk.GREY, 1.0, [4, 3]),
                    (_theta[:, 0], _theta[:, 1], _theta[:, 2], lk.GREEN, 1.4),
                    (_phi[:, 0], _phi[:, 1], _phi[:, 2], lk.GREEN, 1.4),
                ],
                arrows=[((0, 0, 0), tuple(_v), _c) for _v, _c in zip(_A, (lk.BLUE, lk.RED, lk.ORANGE))],
                texts=[(tuple(_theta[20]), r"\theta", lk.GREEN, -20, 5), (tuple(_phi[16]), r"\varphi", lk.GREEN, -10, 4)]
                + [(tuple(_v), _n, _c, _d, 7) for _v, _n, _c, _d in zip(_A, (r"\vec{A}_1", r"\vec{A}_2", r"\vec{A}_3"), (lk.BLUE, lk.RED, lk.ORANGE), (-60, -30, 120))],
            )
        ],
        height=lk.H3D,
        bias=0.15,
    )
    lk.proof(
        [
            r"$A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \vec{A}_3 \end{bmatrix}, \quad \vec{A}_1 = \begin{bmatrix} a \\ d \\ g \end{bmatrix}, \ \vec{A}_2 = \begin{bmatrix} b \\ e \\ h \end{bmatrix}, \ \vec{A}_3 = \begin{bmatrix} c \\ f \\ i \end{bmatrix}$",
            lk.aside(
                lk.figure(_fig),
                r"volume = (base area) $\times$ height<br>= $\lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \sin\theta \times \lVert \vec{A}_3 \rVert \sin\varphi$",
            ),
            lk.aside(
                r"$\text{volume} = \lVert \vec{A}_1 \rVert \lVert \vec{A}_2 \rVert \lVert \vec{A}_3 \rVert \sin\theta \, \mk{\sin\varphi}$",
                r"$\varphi$ = angle between a vector and a plane:<br>we will need to define this more precisely!",
            ),
            r"$\phantom{\text{volume}} = \dots = \lvert \det A \rvert$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: n = 3
    # remark: higher dimensions
    lk.remark(
        r"""
        we can continue up in dimension!

        > $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; $\det A$ gets complicated quickly! but it can be defined!

        > > $\leadsto$ &nbsp; $\lvert \det A \rvert$ = $n$-volume of the $n$-parallelepiped spanned by its $n$ columns!

        > > $\leadsto$ &nbsp; let's not do this explicitly!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: inverses
    # section
    lk.section("Determinants and inverses")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: inverses
    # theorem: invertible 2 x 2 matrices, with what "inverse" means as a matrix and as a function
    _f = r"$\leadsto$ &nbsp; as a function &nbsp; $\leadsto$ &nbsp; $\exists \, B : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ such that "
    lk.theorem(
        [
            lk.aside(
                r"$A \in \mathrm{Mat}(2 \times 2)$ admits an **inverse** iff $\det A \neq 0$",
                r"$A \in \mathrm{Mat}(2 \times 2) \ \leftrightsquigarrow \ A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear",
            ),
            r"> $\leadsto$ &nbsp; as a matrix &nbsp; $\leadsto$ &nbsp; $\exists \, B \in \mathrm{Mat}(2 \times 2)$ such that $AB = BA = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$",
            "> " + _f + r"$A \circ B = B \circ A = \mathrm{id}_{\mathbb{R}^2}$",
            r"> > $A \circ B(\vec{x}) = B \circ A(\vec{x}) = \vec{x} \quad \forall \, \vec{x} \in \mathbb{R}^2$",
        ],
        label="thm-inverse2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: inverses
    # proof (brute force)
    lk.proof(
        [
            r"$A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \quad B = \begin{bmatrix} e & f \\ g & h \end{bmatrix}$",
            r"$$ AB = \begin{bmatrix} ae + bg & af + bh \\ ce + dg & cf + dh \end{bmatrix} = BA = \begin{bmatrix} ea + fc & eb + fd \\ ga + hc & gb + hd \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} $$",
            r"> $\iff$ &nbsp; $e = \dfrac{d}{ad - bc}, \quad f = -\dfrac{b}{ad - bc}, \quad g = -\dfrac{c}{ad - bc}, \quad h = \dfrac{a}{ad - bc}$ $\rule[-1em]{0pt}{2.6em}$",
            r"$\therefore$ &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ admits inverse iff $\det A = ad - bc \neq 0$",
            r"> $\leadsto$ &nbsp; the inverse is $B = A^{-1} = \dfrac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$",
        ],
        title="brute force!",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, ma, math, mb, mc, md, plane, turn, vector):
    # module: inverses
    # key intuition, with the unit square spanned by e1, e2 and its image, the parallelogram spanned by A1, A2, moving with
    # the sliders a, b, c, d; the turn from the first to the second vector reverses when det A < 0
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c + 0.0

    _fig = Figure(figsize=(lk.FULL, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    plane(_left, 2.2)
    _left.set_xticks(range(-2, 3), [f"${_k}$" for _k in range(-2, 3)])
    _left.set_yticks(range(-2, 3), [f"${_k}$" for _k in range(-2, 3)])
    _left.fill([0, 1, 1, 0], [0, 0, 1, 1], color=lk.LIGHT, lw=0)
    _left.plot([1, 1, 0], [0, 1, 1], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_left, (0, 0), (1, 0), lk.BLUE, r"$\vec{e}_1$", turn=-60)
    vector(_left, (0, 0), (0, 1), lk.RED, r"$\vec{e}_2$", turn=60)
    turn(_left, (1, 0), (0, 1), True, 0.6)

    _small = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_a + _b), abs(_c + _d)) <= 3
    plane(_right, 4.4 if _small else 7.6)  # the frame follows the parallelogram: nothing is clipped
    _ticks = range(-4, 5, 2) if _small else range(-6, 7, 3)
    _right.set_xticks(_ticks, [f"${_k}$" for _k in _ticks])
    _right.set_yticks(_ticks, [f"${_k}$" for _k in _ticks])
    _right.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=lk.LIGHT, lw=0)
    _right.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_right, (0, 0), (_a, _c), lk.BLUE, r"$\vec{A}_1$")
    vector(_right, (0, 0), (_b, _d), lk.RED, r"$\vec{A}_2$")
    if _det != 0:
        _r = 0.6 * min(math.hypot(_a, _c), math.hypot(_b, _d), 2.0)
        turn(_right, (_a, _c), (_b, _d), _det > 0, max(_r, 0.3))

    lk.prose(
        r"$\leadsto$ &nbsp; key intuition:",
        r"> $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \quad \Longrightarrow \quad \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix} = A\vec{e}_1, \quad \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix} = A\vec{e}_2$",
        r"> > $\Longrightarrow$ &nbsp; parallelogram spanned by $\vec{A}_1, \vec{A}_2$ is the image of the unit square spanned by $\vec{e}_1, \vec{e}_2$",
        lk.aside(lk.interactive(_fig, controls=[ma, mb, mc, md]), r"unit square: area = 1<br>parallelogram: area = $\lvert \det A \rvert$"),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: inverses
    # consequences: collapse and invertibility
    lk.prose(
        r"if $\det A = 0$ &nbsp; $\Longrightarrow$ &nbsp; $A$ “collapses” the unit square into a line segment (or zero)",
        r"> <span class='lk-ghost'>if $\det A = 0$ &nbsp; $\Longrightarrow$ &nbsp; </span>$\leadsto$ &nbsp; a parallelogram of area zero",
        r"<span class='lk-ghost'>if $\det A = 0$</span> &nbsp; $\Longrightarrow$ &nbsp; $A$ cannot be invertible",
        r"> <span class='lk-ghost'>if $\det A = 0$ &nbsp; $\Longrightarrow$ &nbsp; </span>$\leadsto$ &nbsp; we cannot “recover” the square from a line segment! (not bijective)",
        lk.gap(),
        r"if $\det A \neq 0$ &nbsp; $\Longrightarrow$ &nbsp; $A$ deforms the unit square without “collapse”",
        r"> <span class='lk-ghost'>if $\det A \neq 0$ &nbsp; $\Longrightarrow$ &nbsp; </span>$\leadsto$ &nbsp; linearity is then enough for us to find the inverse!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: inverses
    # theorem: invertible n x n matrices
    lk.theorem(
        [
            lk.aside(
                r"For every $n \in \mathbb{Z}_{>0}$, $A \in \mathrm{Mat}(n \times n)$ admits an inverse iff $\det A \neq 0$.",
                r"$A \in \mathrm{Mat}(n \times n) \ \leftrightsquigarrow \ A : \mathbb{R}^n \longrightarrow \mathbb{R}^n$ linear",
            ),
        ],
        label="thm-inverse-n",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: sign
    # section
    lk.section("The sign of the determinant")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: sign
    # motivation and theorem: the sign of the determinant
    lk.prose(r"$\leadsto$ &nbsp; what about the sign of the determinant?")
    return


@app.cell(hide_code=True)
def _(Figure, lk, turn, vector):
    # module: sign
    # theorem: sign of the determinant and orientation, with the turn from e1 to e2 is counterclockwise, and so
    # is the turn from A e1 to A e2 when det A > 0; it is clockwise when det A < 0
    _fig = Figure(figsize=(lk.FULL, 2.2), layout="constrained")
    _cases = [
        ((1, 0), (0, 1), "counterclockwise", r"$\vec{e}_1, \vec{e}_2$"),
        ((1, 0.4), (-0.3, 1), "counterclockwise", r"$\det A > 0$"),
        ((1, 0.4), (0.4, -0.9), "clockwise", r"$\det A < 0$"),
    ]
    for _ax, (_p, _q, _name, _head) in zip(_fig.subplots(1, 3), _cases):
        _ax.set_xlim(-1.3, 1.6)
        _ax.set_ylim(-1.2, 1.4)
        _ax.set_aspect("equal")
        _ax.axis("off")
        _ax.plot([-0.9, 1.4], [0, 0], color="black", lw=0.8)
        _ax.plot([0, 0], [-0.75, 1.25], color="black", lw=0.8)
        vector(_ax, (0, 0), _p, lk.BLUE)
        vector(_ax, (0, 0), _q, lk.RED)
        turn(_ax, _p, _q, _name == "counterclockwise", 0.5)
        _ax.set_title(_head, fontsize=12)
        _ax.text(0.25, -1.15, _name, fontsize=11, ha="center", va="bottom", color=lk.GREEN)
    lk.theorem(
        [
            r"$A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear",
            r"""
            > if $\det A > 0$, $A$ preserves the direction of rotations around the origin

            > if $\det A < 0$, $A$ reverses the direction of rotations around the origin
            """,
            lk.figure(_fig),
            lk.gap(),
            r"$A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear",
            r"""
            > if $\det A > 0$, $A$ preserves “handedness” of orthogonal frames (triples of pairwise orthogonal vectors)

            > if $\det A < 0$, $A$ reverses “handedness”
            """,
        ],
        label="thm-sign",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: sign
    # right-hand rule, with the standard basis of R^3 and, beside it, the turn of the fingers from e1 to e2 and the thumb
    # along e3
    _s = np.radians(np.linspace(-40, 180, 110))
    _tail = (1 + 0.3 * np.cos(_s[0]), 1 + 0.3 * np.sin(_s[0]))  # the thumb rises above the tail of the turn
    _fig = lk.turntable(
        24,
        26,
        "the standard basis vectors e1, e2, e3 of R^3, with a turn around e3 in the direction from e1 to e2",
        [
            lk.panel(
                1.0,
                # each axis is left out from the origin to the tip of e_i, so that the axis never covers the arrow
                lines=[([-0.4, 0], [0, 0], [0, 0], "#000000", 1.1), ([1, 1.5], [0, 0], [0, 0], "#000000", 1.1), ([0, 0], [-0.4, 0], [0, 0], "#000000", 1.1),
                       ([0, 0], [1, 1.4], [0, 0], "#000000", 1.1), ([0, 0], [0, 0], [-0.4, 0], "#000000", 1.1), ([0, 0], [0, 0], [1, 1.4], "#000000", 1.1)],
                arrows=[((0, 0, 0), (1, 0, 0), lk.BLUE), ((0, 0, 0), (0, 1, 0), lk.BLUE), ((0, 0, 0), (0, 0, 1), lk.BLUE), ((_tail[0], _tail[1], 0.95), (_tail[0], _tail[1], 1.65), lk.GREEN)],
                arcs=[(1 + 0.3 * np.cos(_s), 1 + 0.3 * np.sin(_s), 0.8 + 0 * _s, lk.GREEN)],
                texts=[((1, 0, 0), r"\vec{e}_1", lk.BLUE, 180, 8), ((0, 1, 0), r"\vec{e}_2", lk.BLUE, -90, 8), ((0, 0, 1), r"\vec{e}_3", lk.BLUE, 180, 8)],
            )
        ],
        height=lk.H3D_FLAT,
    )
    lk.prose(
        lk.side(
            lk.figure(_fig),
            r"""
            right-hand rule

            > $\vec{e}_1, \vec{e}_2, \vec{e}_3$ have positive “handedness” (orientation)

            > if rotating fingers from $\vec{e}_1$ to $\vec{e}_2$ your thumb points to $\vec{e}_3$
            """,
        )
    )
    return


if __name__ == "__main__":
    app.run()
