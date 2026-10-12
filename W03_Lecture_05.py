import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 05 · Lines and planes and the cross-product in R³", css_file="bs101.css")


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
    header("Lecture 05", "Week 03", "Lecture 05 · Lines and planes and the cross-product in R³")
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
def _(arrow):
    def oblique(p):
        """Oblique projection of R^3, as on the board: x^2 to the right, x^3 up, x^1 towards the viewer."""
        return p[1] - 0.45 * p[0], p[2] - 0.4 * p[0]

    def frame3(ax, a1, a2, a3, back=0.5, beside=False):
        """The three coordinate axes of R^3 (lengths a1, a2, a3) in the oblique projection,
        named beyond their ends, or beside them when vectors along the axes need that room."""
        ends = ((a1, 0, 0), (0, a2, 0), (0, 0, a3))
        offsets = ((10, 2), (-2, -7), (-7, -10)) if beside else ((-5, -5), (6, 0), (0, 5))
        aligns = (("left", "top"), ("right", "top"), ("right", "top")) if beside else (("right", "top"), ("left", "center"), ("center", "bottom"))
        for i, (end, off, (ha, va)) in enumerate(zip(ends, offsets, aligns)):
            start = tuple(-back * c / max(end) for c in end)
            arrow(ax, oblique(start), oblique(end), "black", lw=0.9)
            ax.annotate(f"$x^{i + 1}$", oblique(end), textcoords="offset points", xytext=off, fontsize=12, ha=ha, va=va)

    return frame3, oblique


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - determinants

        $$
        A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \quad \Longrightarrow \quad
        \det A = ad - bc = \text{signed area of parallelogram spanned by } \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix},\ \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix}
        $$

        $$
        A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \quad \Longrightarrow \quad
        \det A = a(ei - fh) - b(di - fg) + c(dh - eg) = \text{signed volume}
        $$

    - $\leadsto$ &nbsp; need to interpret sign
    - $\leadsto$ &nbsp; need to understand angle between vectors and planes

    **In this lecture:** lines and planes in $\mathbb{R}^3$, and the cross-product
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, HALF, RED, arrow, blank, definition, mo):
    _fig, _ax = blank(HALF, 1.75, (-0.6, 4.7), (-0.5, 1.95))
    _x, _v, _t = (0.4, 1.4), (1.6, 0.0), 1.7
    _g = (_x[0] + _t * _v[0], _x[1])
    _ax.plot([-0.5, 4.2], [1.4, 1.4], color="black", lw=1.0)
    arrow(_ax, (0, 0), _g, BLUE)
    arrow(_ax, (0, 0), _x, RED)
    arrow(_ax, (0, 0), _v, GREEN)
    arrow(_ax, _x, _g, GREEN)
    _ax.plot(0, 0, "o", color="black", ms=3, zorder=4)
    _ax.text(0.08, 0.78, r"$\vec{x}$", color=RED, fontsize=13, ha="right", va="center")
    _ax.text(0.8, -0.1, r"$\vec{v}$", color=GREEN, fontsize=13, ha="center", va="top")
    _ax.text((_x[0] + _g[0]) / 2, 1.52, r"$t\vec{v}$", color=GREEN, fontsize=13, ha="center", va="bottom")
    _ax.text(1.95, 0.62, r"$\vec{x} + t\vec{v}$", color=BLUE, fontsize=13, ha="left", va="top")
    _ax.text(4.32, 1.4, "$L$", fontsize=13, ha="left", va="center")
    _ax.text(-0.12, -0.05, r"$\vec{0}$", fontsize=13, ha="right", va="top")

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.5 &nbsp; Lines and planes and the cross-product in $\mathbb{R}^3$ (MT 1.3)

    ### Lines
    """
            ),
            definition(
                r"""
    Given vectors $\vec{x}$ and $\vec{v}$ in $\mathbb{R}^3$, with $\vec{v}$ non-zero, the **line** through $\vec{x}$ in the direction of $\vec{v}$ is the set

    $$
    L = \left\{\, \gamma(t) = \vec{x} + t\vec{v} \in \mathbb{R}^3 \;\middle|\; t \in \mathbb{R} \,\right\}
    $$

    We call the function

    $$
    \begin{aligned}
    \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^3 \\
    t &\longmapsto \gamma(t) = \vec{x} + t\vec{v}
    \end{aligned}
    $$

    an **affine parameterization** of the line $L$ (just a name for “linear plus constant”).
    """,
                "Line and affine parameterization",
            ),
            _fig,
            mo.md(
                r"""
    **Example.**

    $$
    \vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}
    \qquad \leadsto \qquad
    \gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} t \\ 1 + 2t \\ 1 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_line = mo.ui.slider(-1.5, 1.5, 0.25, value=1, label="$t$", show_value=True)
    return (t_line,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, RED, blank, frame3, mo, oblique, t_line, table, vector):
    _t = t_line.value
    _g = (_t + 0.0, 1 + 2 * _t + 0.0, 1)

    _fig, _ax = blank(FULL, 3.0, (-3.5, 5.7), (-1.25, 2.5))
    frame3(_ax, 2.4, 4.9, 2.15)
    # the plane x^3 = 1 (outline only) and the line L inside it
    _corners = [oblique(p) for p in ((-1.8, -2.4, 1), (-1.8, 4.6, 1), (1.8, 4.6, 1), (1.8, -2.4, 1))]
    _ax.plot(*zip(*(_corners + _corners[:1])), color=GREY, lw=0.9)
    _ax.text(4.35, 1.5, "$x^3 = 1$", color=GREY, fontsize=12, ha="center", va="center")
    _a, _b = oblique((-1.7, -2.4, 1)), oblique((1.8, 4.6, 1))
    _ax.plot([_a[0], _b[0]], [_a[1], _b[1]], color="black", lw=1.0)
    _ax.text(_b[0] + 0.1, _b[1] - 0.04, "$L$", fontsize=13, ha="left", va="top")
    # labels above the line, on opposite sides of the tip of x, so that they stay apart when gamma(t) passes x
    _side = 1 if _t >= 0 else -1
    vector(_ax, (0, 0), oblique((1, 2, 0)), GREEN, r"$\vec{v}$", -75)
    vector(_ax, (0, 0), oblique((0, 1, 1)), RED, r"$\vec{x}$", 45 + 37 * _side, r=18)
    vector(_ax, (0, 0), oblique(_g), BLUE)
    _tip = oblique(_g)
    _ax.plot(*_tip, "o", color=BLUE, ms=4, zorder=4)
    _ax.annotate(r"$\gamma(t)$", _tip, textcoords="offset points", xytext=(11 * _side, 15), ha="center", va="center", color=BLUE, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    mo.vstack(
        [
            mo.hstack([t_line], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$t$", rf"${_t:g}$"),
                    (r"$\gamma(t) = \vec{x} + t\vec{v}$", rf"$\textcolor{{{RED}}}{{\begin{{bmatrix}} 0 \\ 1 \\ 1 \end{{bmatrix}}}} + ({_t:g}) \textcolor{{{GREEN}}}{{\begin{{bmatrix}} 1 \\ 2 \\ 0 \end{{bmatrix}}}} = \textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_g[0]:g} \\ {_g[1]:g} \\ {_g[2]:g} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Given a line $L$ with an affine parameterization

    $$
    \gamma(t) = \vec{x} + t\vec{v}
    $$

    we call $\vec{x}$ the **starting point** and $\vec{v}$ the **velocity** of $L$ with respect to the parameterization $\gamma$.
    """,
                "Starting point and velocity",
            ),
            mo.md(
                r"""
    **Remark.** There exists a unique line through $\vec{x}, \vec{y} \in \mathbb{R}^3$ if and only if $\vec{y} - \vec{x}$ is non-zero.

    However, parameterizations are not unique!

    $$
    \begin{aligned}
    \leadsto \quad L &= \left\{\, \gamma(t) = \vec{x} + t(\vec{y} - \vec{x}) \;\middle|\; t \in \mathbb{R} \,\right\}
    = \left\{\, \tilde{\gamma}(t) = \vec{y} + 2t(\vec{x} - \vec{y}) \;\middle|\; t \in \mathbb{R} \,\right\} \\
    &= \left\{\, \hat{\gamma}(t) = \tfrac{1}{2}(\vec{x} + \vec{y}) + t(\vec{x} - \vec{y}) \;\middle|\; t \in \mathbb{R} \,\right\}
    \end{aligned}
    $$

    **Remark.** For any pair of affine parameterizations $\gamma, \tilde{\gamma}$ of a line $L$, the velocity vectors are proportional!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, RED, arrow, blank, definition, frame3, mo, oblique):
    _x, _u, _v = (0, 1, 1), (1, 2, 0), (-1, 3, 0)
    _pu = tuple(a + b for a, b in zip(_x, _u))
    _pv = tuple(a + b for a, b in zip(_x, _v))
    _puv = tuple(a + b for a, b in zip(_pu, _v))
    _X, _U, _V, _S = oblique(_x), oblique(_pu), oblique(_pv), oblique(_puv)

    _fig, _ax = blank(FULL, 2.75, (-1.75, 8.75), (-1.2, 2.5))
    frame3(_ax, 2.4, 3.2, 2.15)
    _corners = [oblique(p) for p in ((-1.6, -0.6, 1), (-1.6, 7.7, 1), (1.6, 7.7, 1), (1.6, -0.6, 1))]
    _ax.plot(*zip(*(_corners + _corners[:1])), color=GREY, lw=0.9)
    _ax.text(7.75, 1.42, "$P$", color=GREY, fontsize=13, ha="center", va="center")
    # x = (0, 1, 1): unit marks on the axes and drop lines to them
    _ax.plot([1, 1], [0, 1], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([0, 1], [1, 1], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([1, 1], [-0.05, 0.05], color="black", lw=0.9)
    _ax.plot([-0.05, 0.05], [1, 1], color="black", lw=0.9)
    _ax.text(1, -0.12, "$1$", fontsize=12, ha="center", va="top")
    _ax.text(-0.12, 1.02, "$1$", fontsize=12, ha="right", va="bottom")
    # phi(1, 1) = x + u + v completes the parallelogram
    _ax.plot([_U[0], _S[0], _V[0]], [_U[1], _S[1], _V[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    arrow(_ax, (0, 0), _X, RED)
    arrow(_ax, _X, _U, GREEN)
    arrow(_ax, _X, _V, GREEN)
    _ax.plot(*_S, "o", color=BLUE, ms=4, zorder=4)
    _ax.text(0.42, 0.62, r"$\vec{x}$", color=RED, fontsize=13, ha="right", va="bottom")
    _ax.text((_X[0] + _U[0]) / 2, (_X[1] + _U[1]) / 2 - 0.12, r"$\vec{u}$", color=GREEN, fontsize=13, ha="right", va="top")
    _ax.text((_X[0] + _V[0]) / 2, (_X[1] + _V[1]) / 2 + 0.1, r"$\vec{v}$", color=GREEN, fontsize=13, ha="right", va="bottom")
    _ax.text(_S[0] + 0.14, _S[1], r"$\varphi(s,t)$", color=BLUE, fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.md(r"""### Planes"""),
            definition(
                r"""
    Given $\vec{x}, \vec{u}, \vec{v} \in \mathbb{R}^3$, with $\vec{u}, \vec{v}$ not proportional, the **plane** through $\vec{x}$ in the directions of $\vec{u}$ and $\vec{v}$ is the set

    $$
    P = \left\{\, \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v} \;\middle|\; s, t \in \mathbb{R} \,\right\}
    $$

    ($\varphi : \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ is an **affine parameterization** of the plane).
    """,
                "Plane and affine parameterization",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    \vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad
    \vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad
    \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}
    \qquad \leadsto \qquad
    \varphi(s, t) = \begin{bmatrix} s - t \\ 1 + 2s + 3t \\ 1 \end{bmatrix}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** There exists a unique plane through $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^3$ if and only if $\vec{y} - \vec{x}$, $\vec{z} - \vec{x}$ are not proportional.

    $$
    P = \left\{\, \varphi(s, t) = \vec{x} + s(\vec{y} - \vec{x}) + t(\vec{z} - \vec{x}) \;\middle|\; s, t \in \mathbb{R} \,\right\}
    $$

    $\leadsto$ &nbsp; different parameterizations are also possible, with different starting points and directions
    """
            ),
            definition(
                r"""
    Given a plane $P = \left\{\, \vec{x} + s\vec{u} + t\vec{v} \;\middle|\; s, t \in \mathbb{R} \,\right\}$, a vector $\vec{n} \in \mathbb{R}^3$ is called **normal** to $P$ if

    $$
    \vec{n} \cdot \vec{u} = \vec{n} \cdot \vec{v} = 0 \qquad (\vec{n} \text{ is orthogonal to both directions in } P)
    $$
    """,
                "Normal vector",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, RED, arrow, blank, definition, mo):
    # u, v, w = u x v and -w, with the rotation from u to v
    _fig, _ax = blank(HALF, 2.75, (-1.9, 2.6), (-1.55, 1.9))
    _u, _v = (1.7, -0.55), (1.55, 0.75)
    arrow(_ax, (0, 0), (0, -1.15), GREY, linestyle=(0, (4, 3)))
    arrow(_ax, (0, 0), (0, 1.5), GREEN)
    arrow(_ax, (0, 0), _u, BLUE)
    arrow(_ax, (0, 0), _v, RED)
    arrow(_ax, (0.76, -0.25), (0.72, 0.35), "black", lw=0.9, connectionstyle="arc3,rad=0.3")
    _ax.text(0.98, 0.07, r"$\theta$", fontsize=13, ha="left", va="center")
    _ax.text(_u[0] + 0.1, _u[1] - 0.04, r"$\vec{u}$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax.text(_v[0] + 0.1, _v[1] + 0.04, r"$\vec{v}$", color=RED, fontsize=13, ha="left", va="center")
    _ax.text(0, 1.58, r"$\vec{w}$", color=GREEN, fontsize=13, ha="center", va="bottom")
    _ax.text(0, -1.22, r"$-\vec{w}$", color=GREY, fontsize=13, ha="center", va="top")

    # a plane through x with directions u, v and a normal vector
    _fig2, _ax2 = blank(HALF, 2.6, (-0.3, 5.3), (-1.3, 2.75))
    _ax2.plot([0, 3.7, 4.6, 0.9, 0], [0, 0, 1.4, 1.4, 0], color=GREY, lw=0.9)
    _p = (1.8, 0.55)
    arrow(_ax2, (1.2, -1.0), _p, "black")
    arrow(_ax2, _p, (3.3, 0.3), BLUE)
    arrow(_ax2, _p, (2.95, 1.1), RED)
    arrow(_ax2, _p, (1.8, 2.15), GREEN)
    _ax2.plot(1.2, -1.0, "o", color="black", ms=3, zorder=4)
    _ax2.text(1.08, -1.0, r"$\vec{0}$", fontsize=13, ha="right", va="center")
    _ax2.text(1.62, -0.55, r"$\vec{x}$", fontsize=13, ha="left", va="center")
    _ax2.text(3.4, 0.28, r"$\vec{u}$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax2.text(3.05, 1.12, r"$\vec{v}$", color=RED, fontsize=13, ha="left", va="center")
    _ax2.text(1.95, 2.2, r"$\vec{n} = \alpha\, \vec{u} \times \vec{v}$", color=GREEN, fontsize=13, ha="left", va="center")
    _ax2.text(0.55, 0.2, "$P$", color=GREY, fontsize=13, ha="center", va="center")

    mo.vstack(
        [
            mo.md(r"""### The cross-product"""),
            definition(
                r"""
    Given two vectors $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}, \ \vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix} \in \mathbb{R}^3$, the **cross-product** of $\vec{u}$ and $\vec{v}$ is the unique vector $\vec{w} = \vec{u} \times \vec{v} \in \mathbb{R}^3$ such that

    $$
    \vec{u} \cdot \vec{w} = 0, \quad \vec{v} \cdot \vec{w} = 0 \qquad (\text{orthogonal to both } \vec{u}, \vec{v})
    $$

    $$
    \lVert \vec{w} \rVert^2 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2
    = \Big(\underbrace{\lVert \vec{u} \rVert\, \lVert \vec{v} \rVert \sin\!\big(\theta(\vec{u}, \vec{v})\big)}_{\text{area of parallelogram spanned by } \vec{u} \text{ and } \vec{v}}\Big)^2
    $$

    (if $\vec{u}, \vec{v}$ are proportional this forces $\vec{w} = \vec{0}$) and $\vec{u}, \vec{v}, \vec{w}$ is **right-handed** (positively oriented).
    """,
                "Cross-product",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; with your right hand: rotating your fingers from $\vec{u}$ to $\vec{v}$ points your thumb towards $\vec{w}$
    """
            ),
            _fig,
            mo.md(
                r"""
    Algebraically: $\vec{u}, \vec{v}, \vec{w}$ is right-handed if

    $$
    \det \begin{bmatrix} \vec{u} & \vec{v} & \vec{w} \end{bmatrix} > 0
    $$

    **Remark.** Given a parameterization

    $$
    \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}
    $$

    of a plane $P$, every normal vector to $P$ is proportional to the cross-product $\vec{u} \times \vec{v}$.
    """
            ),
            _fig2,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Computing the cross-product"""),
            theorem(
                r"""
    Given $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}$ and $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix}$ in $\mathbb{R}^3$

    $$
    \begin{aligned}
    \vec{u} \times \vec{v} &= \underbrace{\det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ u^1 & u^2 & u^3 \\ v^1 & v^2 & v^3 \end{bmatrix}}_{\substack{\text{not an honest determinant!} \\ \text{1st row is made of vectors…}}}
    = \vec{e}_1 \det \begin{bmatrix} u^2 & u^3 \\ v^2 & v^3 \end{bmatrix} - \vec{e}_2 \det \begin{bmatrix} u^1 & u^3 \\ v^1 & v^3 \end{bmatrix} + \vec{e}_3 \det \begin{bmatrix} u^1 & u^2 \\ v^1 & v^2 \end{bmatrix} \\
    &= \vec{e}_1 (u^2 v^3 - u^3 v^2) - \vec{e}_2 (u^1 v^3 - u^3 v^1) + \vec{e}_3 (u^1 v^2 - u^2 v^1)
    = \begin{bmatrix} u^2 v^3 - u^3 v^2 \\ u^3 v^1 - u^1 v^3 \\ u^1 v^2 - u^2 v^1 \end{bmatrix} = \vec{w}
    \end{aligned}
    $$
    """,
                "Cross-product formula",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \vec{u} \cdot \vec{w} = u^1 (\cancel{u^2 v^3} - \bcancel{u^3 v^2}) + u^2 (\xcancel{u^3 v^1} - \cancel{u^1 v^3}) + u^3 (\bcancel{u^1 v^2} - \xcancel{u^2 v^1}) = 0, \qquad \vec{v} \cdot \vec{w} = 0
    $$

    $$
    \begin{aligned}
    \lVert \vec{w} \rVert^2 &= (u^2 v^3 - u^3 v^2)^2 + (u^3 v^1 - u^1 v^3)^2 + (u^1 v^2 - u^2 v^1)^2 \\
    &= \big( (u^1)^2 + (u^2)^2 + (u^3)^2 \big) \big( (v^1)^2 + (v^2)^2 + (v^3)^2 \big) - \big( u^1 v^1 + u^2 v^2 + u^3 v^3 \big)^2 \qquad (\text{check!}) \\
    &= \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2
    \end{aligned}
    $$

    $$
    \det \begin{bmatrix} u^1 & v^1 & (u^2 v^3 - u^3 v^2) \\ u^2 & v^2 & (u^3 v^1 - u^1 v^3) \\ u^3 & v^3 & (u^1 v^2 - u^2 v^1) \end{bmatrix} = \lVert \vec{w} \rVert^2 \geq 0 \qquad (\text{check!})
    $$

    This is strictly positive when $\vec{u}, \vec{v}$ are not proportional; otherwise $\vec{w} = \vec{0}$. $\square$

    **Example.** &nbsp; $\vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}$

    $$
    \leadsto \quad \vec{u} \times \vec{v} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 2 & 0 \\ -1 & 3 & 0 \end{bmatrix}
    = 0\, \vec{e}_1 + 0\, \vec{e}_2 + \big( 1 \cdot 3 - 2 \cdot (-1) \big)\, \vec{e}_3 = 5\, \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 5 \end{bmatrix}
    $$

    $$
    \vec{u} \cdot (\vec{u} \times \vec{v}) = 1 \cdot 0 + 2 \cdot 0 + 0 \cdot 5 = 0, \qquad
    \vec{v} \cdot (\vec{u} \times \vec{v}) = (-1) \cdot 0 + 3 \cdot 0 + 0 \cdot 5 = 0
    $$

    $$
    \lVert \vec{u} \times \vec{v} \rVert^2 = 25 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2 = (1 + 4)(1 + 9) - (-1 + 6)^2 = 50 - 25
    $$

    $$
    \det \begin{bmatrix} 1 & -1 & 0 \\ 2 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix}
    = 1\, (3 \cdot 5 - 0 \cdot 0) - (-1)\, (2 \cdot 5 - 0 \cdot 0) + 0\, (2 \cdot 0 - 3 \cdot 0) = \underbrace{25}_{\lVert \vec{u} \times \vec{v} \rVert^2\,!} > 0
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _s(label, value):
        return mo.ui.slider(-3, 3, 0.5, value=value, label=label, show_value=True)

    u1, u2, u3 = _s("$u^1$", 1), _s("$u^2$", 2), _s("$u^3$", 0)
    v1, v2, v3 = _s("$v^1$", -1), _s("$v^2$", 3), _s("$v^3$", 0)
    return u1, u2, u3, v1, v2, v3


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, LIGHT, RED, blank, frame3, math, mo, oblique, table, u1, u2, u3, v1, v2, v3, vector):
    _u = (u1.value, u2.value, u3.value)
    _v = (v1.value, v2.value, v3.value)
    _w = (_u[1] * _v[2] - _u[2] * _v[1], _u[2] * _v[0] - _u[0] * _v[2], _u[0] * _v[1] - _u[1] * _v[0])
    _w = tuple(c + 0.0 for c in _w)
    _norm = math.sqrt(sum(c * c for c in _w))
    _U, _V, _W = oblique(_u), oblique(_v), oblique(_w)
    _S = (_U[0] + _V[0], _U[1] + _V[1])

    # the frame follows the vectors: nothing is clipped
    _lim = max([3.2] + [1.3 * abs(p[1]) for p in (_U, _V, _W, _S)] + [1.3 * abs(p[0]) / 1.6 for p in (_U, _V, _W, _S)])
    _step = 1 if _lim <= 5 else 2 if _lim <= 10 else 5
    _len = 0.88 * _lim
    _low = _lim if min(p[1] for p in (_U, _V, _W, _S)) < -0.3 * _lim else 0.5 * _lim  # room below only when a vector points there
    _fig, _ax = blank(FULL, FULL * (_lim + _low) / (3.2 * _lim), (-1.6 * _lim, 1.6 * _lim), (-_low, _lim))
    _ax.fill([0, _U[0], _S[0], _V[0]], [0, _U[1], _S[1], _V[1]], color=LIGHT, lw=0, zorder=0)
    _ax.plot([_U[0], _S[0], _V[0]], [_U[1], _S[1], _V[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    frame3(_ax, _len, 1.6 * _len, _len, back=0.3 * _len, beside=True)
    _d = 0.012 * _lim
    for _k in range(_step, int(0.95 * _len) + 1, _step):  # axis marks every `_step` units
        for _i, (_dx, _dy) in enumerate(((_d, -_d), (0, _d), (_d, 0))):
            _m = oblique(tuple(_k if _j == _i else 0 for _j in range(3)))
            _ax.plot([_m[0] - _dx, _m[0] + _dx], [_m[1] - _dy, _m[1] + _dy], color="black", lw=0.8)
    _ax.annotate(f"${_step}$", (_step, 0), textcoords="offset points", xytext=(0, -6), fontsize=11, ha="center", va="top", bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})
    _side = -1 if _U[0] * _V[1] - _U[1] * _V[0] < 0 else 1  # labels go on the outer side of each arrow
    vector(_ax, (0, 0), _W, GREEN, r"$\vec{u} \times \vec{v}$", 0, r=22)
    vector(_ax, (0, 0), _U, BLUE, r"$\vec{u}$", -75 * _side)
    vector(_ax, (0, 0), _V, RED, r"$\vec{v}$", 75 * _side)

    def _col(vec, color):
        return rf"$\textcolor{{{color}}}{{\begin{{bmatrix}} {vec[0]:g} \\ {vec[1]:g} \\ {vec[2]:g} \end{{bmatrix}}}}$"

    mo.vstack(
        [
            mo.vstack(
                [
                    mo.hstack([u1, u2, u3], justify="start", gap=2, wrap=True),
                    mo.hstack([v1, v2, v3], justify="start", gap=2, wrap=True),
                ]
            ),
            table(
                [
                    (r"$\vec{u}, \ \vec{v}$", _col(_u, BLUE) + r", &nbsp; " + _col(_v, RED)),
                    (r"$\vec{u} \times \vec{v}$", _col(_w, GREEN)),
                    (r"$\lVert \vec{u} \times \vec{v} \rVert$ = area of the parallelogram", rf"${_norm:.3f}$"),
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
    **Remark.** The cross-product in $\mathbb{R}^3$ defines

    $$
    \times : \mathbb{R}^3 \times \mathbb{R}^3 \longrightarrow \mathbb{R}^3
    $$

    another extension of multiplication of vectors, now taking values in vectors!

    $\leadsto$ &nbsp; this **cannot** be extended to other $\mathbb{R}^n$ with $n \neq 3, 7$

    ### Properties of the cross-product
    """
            ),
            theorem(
                r"""
    Given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$, $\alpha, \beta \in \mathbb{R}$

    - $\vec{u} \times \vec{v} = -\vec{v} \times \vec{u}$ &nbsp; (**anti-commutativity**)
    - $\vec{u} \times (\alpha \vec{v} + \beta \vec{w}) = \alpha (\vec{u} \times \vec{v}) + \beta (\vec{u} \times \vec{w})$ and
      $(\alpha \vec{u} + \beta \vec{v}) \times \vec{w} = \alpha (\vec{u} \times \vec{w}) + \beta (\vec{v} \times \vec{w})$ &nbsp; (**bilinearity**)
    """,
                "Properties of the cross-product",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q2_1, q2_2, q2_3, q3_vol = (_field() for _ in range(4))
    return q2_1, q2_2, q2_3, q3_vol


@app.cell(hide_code=True)
def _(check, mo, q2_1, q2_2, q2_3, q3_vol):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $\vec{x} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 2 \\ -1 \\ 4 \end{bmatrix}, \; \gamma(t) = \vec{x} + t\vec{v}$.

    (a) Compute $\gamma(0)$, $\gamma(1)$, $\gamma(2)$.

    (b) Compute $\gamma(2) - \gamma(1)$.

    (c) Is $\vec{y} = \begin{bmatrix} 7 \\ -1 \\ 12 \end{bmatrix}$ in the line $L = \{\, \gamma(t) \mid t \in \mathbb{R} \,\}$?

    ### Question 2

    Let $\vec{u} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \; \vec{x} = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix}, \; \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}$.

    (a) Compute $\vec{n} = \vec{u} \times \vec{v}$.
    """
            ),
            _ask(r"$n^1 =$", q2_1, 1),
            _ask(r"$n^2 =$", q2_2, -1),
            _ask(r"$n^3 =$", q2_3, 1),
            mo.md(
                r"""
    (b) Verify that every vector $\vec{y} \in P = \{\, \varphi(s, t) \mid s, t \in \mathbb{R} \,\}$ satisfies $(\vec{y} - \vec{x}) \cdot \vec{n} = 0$.

    (c) Write $(\vec{y} - \vec{x}) \cdot \vec{n} = 0$ as equations on $y^1, y^2, y^3$ and decide if $\vec{y} = \begin{bmatrix} 2 \\ 1 \\ 2 \end{bmatrix}$ and $\vec{y} = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$ are in $P$.

    ### Question 3

    Let $A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 1 \end{bmatrix}$.

    (a) Is $A$ invertible?

    (b) What is the volume of the parallelepiped spanned by the columns of $A$?
    """
            ),
            _ask(r"volume $=$", q3_vol, 2),
            mo.md(r"(c) Is $\vec{A}_1, \vec{A}_2, \vec{A}_3$ right-handed (positively oriented)?"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a line in $\mathbb{R}^3$ is $L = \{\, \gamma(t) = \vec{x} + t\vec{v} \mid t \in \mathbb{R} \,\}$ with $\vec{v}$ non-zero: starting point $\vec{x}$, velocity $\vec{v}$; parameterizations are not unique, but their velocities are proportional
    - a plane in $\mathbb{R}^3$ is $P = \{\, \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v} \mid s, t \in \mathbb{R} \,\}$ with $\vec{u}, \vec{v}$ not proportional; $\vec{n}$ is normal to $P$ if $\vec{n} \cdot \vec{u} = \vec{n} \cdot \vec{v} = 0$
    - the cross-product $\vec{w} = \vec{u} \times \vec{v}$ is orthogonal to both $\vec{u}, \vec{v}$, has $\lVert \vec{w} \rVert$ = area of the parallelogram spanned by $\vec{u}$ and $\vec{v}$, and $\vec{u}, \vec{v}, \vec{w}$ is right-handed: $\det \begin{bmatrix} \vec{u} & \vec{v} & \vec{w} \end{bmatrix} > 0$
    - $\vec{u} \times \vec{v}$ is computed as a formal $3 \times 3$ determinant with first row $\vec{e}_1, \vec{e}_2, \vec{e}_3$; every normal vector to $P$ is proportional to $\vec{u} \times \vec{v}$
    - the cross-product is anti-commutative and bilinear

    **Next:** multivariable functions
    """)
    return


if __name__ == "__main__":
    app.run()
