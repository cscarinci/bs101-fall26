import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 05 · Lines, planes, and the cross-product in R³", css_file="bs101.css")


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
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.3, "mutation_scale": 10, "shrinkA": 0, "shrinkB": 0, **kw},
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
    header("Lecture 05", "Week 03", "Lecture 05 · Lines, planes, and the cross-product in R³")
    return


@app.cell(hide_code=True)
def _(Figure, GREEN, RED, math):
    from matplotlib.patches import Polygon

    # One orthographic view for every 3D diagram; no per-figure camera rotation.
    _az, _el = math.radians(28), math.radians(22)
    _ca, _sa = math.cos(_az), math.sin(_az)
    _ce, _se = math.cos(_el), math.sin(_el)

    def project3(v):
        x, y, z = v
        return (-_sa * x + _ca * y, -_se * _ca * x - _se * _sa * y + _ce * z)

    def depth3(v):
        return _ce * _ca * v[0] + _ce * _sa * v[1] + _se * v[2]

    def space(figsize, xlim, ylim, axis_limits=()):
        fig = Figure(figsize=figsize)
        ax = fig.subplots()
        fig.subplots_adjust(left=0.02, right=0.98, bottom=0.03, top=0.97)
        ax.set_aspect("equal")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.axis("off")
        for d, (lo, hi) in enumerate(axis_limits):
            start, end = [0, 0, 0], [0, 0, 0]
            start[d], end[d] = lo, hi
            ax.annotate("", xy=project3(end), xytext=project3(start),
                        arrowprops={"arrowstyle": "-|>", "color": "#555b63", "lw": 0.85,
                                    "mutation_scale": 8, "shrinkA": 0, "shrinkB": 0}, zorder=1)
        return fig, ax

    def label3(ax, point, text, color, offset=(6, 6), ha="left", va="bottom", size=14):
        ax.annotate(text, project3(point), xytext=offset, textcoords="offset points",
                    color=color, fontsize=size, ha=ha, va=va, zorder=8)

    def vec3(ax, v, color, label=None, origin=(0, 0, 0), lw=1.3,
             label_offset=(6, 6), label_ha="left", label_va="bottom", zorder=5):
        tip = tuple(o + c for o, c in zip(origin, v))
        if any(v):
            ax.annotate("", xy=project3(tip), xytext=project3(origin),
                        arrowprops={"arrowstyle": "-|>", "color": color, "lw": lw,
                                    "mutation_scale": 9, "shrinkA": 0, "shrinkB": 0}, zorder=zorder)
        if label:
            label3(ax, tip, label, color, label_offset, label_ha, label_va)

    def patch3(ax, origin, u, v):
        p1 = tuple(a + b for a, b in zip(origin, u))
        p2 = tuple(a + b for a, b in zip(p1, v))
        p3 = tuple(a + b for a, b in zip(origin, v))
        ax.add_patch(Polygon([project3(p) for p in (origin, p1, p2, p3)], closed=True,
                             facecolor="#edf1f5", edgecolor="#8997a5", lw=0.9, alpha=0.65, zorder=2))

    def plane_schematic():
        # A generic tilted plane, independent of the numerical examples.
        x, u, v = (0, 1, 1), (1, 2, 0.10), (-1, 3, 0.025)
        fig, ax = space((5.2, 3.2), (-1.65, 5.55), (-1.45, 2.55),
                        ((0, 2.7), (0, 5.6), (0, 2)))
        patch3(ax, (-1.45, 0.25, 0.90875), (3.25, 0, 0.1625), (0, 4.8, 0.12))
        vec3(ax, x, RED, zorder=1)
        label3(ax, (0, 0.15, 0.15), r"$\vec{x}$", RED, (-18, -8), ha="right", va="center")
        vec3(ax, u, GREEN, r"$\vec{u}$", origin=x,
             label_offset=(-3, -12), label_ha="center", label_va="center")
        vec3(ax, v, GREEN, r"$\vec{v}$", origin=x,
             label_offset=(-4, 9), label_ha="right", label_va="center")
        ax.plot(*project3(x), "o", color=RED, ms=2.5, zorder=6)
        return fig, ax, x, u, v

    return depth3, label3, patch3, plane_schematic, project3, space, vec3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Determinants

    $$
    A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \quad \Longrightarrow \quad
    \det A = ad - bc = \text{signed area of parallelogram spanned by } \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix},\ \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix}
    $$

    $$
    A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \quad \Longrightarrow \quad
    \det A = a(ei - fh) - b(di - fg) + c(dh - eg) = \text{signed volume}
    $$

    - need to interpret sign
    - need to understand angle between vectors and planes
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, arrow, definition, mo):
    _fig = Figure(figsize=(4.2, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _x, _v, _t = (0.4, 1.4), (1.6, 0.0), 1.7
    _ax.plot([-0.6, 4.2], [1.4, 1.4], color="black", lw=1.2)
    arrow(_ax, (0, 0), _x, RED, r"$\vec{x}$")
    arrow(_ax, (0, 0), _v, GREEN, r"$\vec{v}$", at_tip=True)
    arrow(_ax, _x, (_x[0] + _t * _v[0], _x[1]), GREEN, r"$t\vec{v}$")
    arrow(_ax, (0, 0), (_x[0] + _t * _v[0], _x[1]), BLUE)
    _ax.text(1.9, 0.65, r"$\vec{x} + t\vec{v}$", color=BLUE, fontsize=15)
    _ax.text(4.25, 1.3, "$L$", fontsize=15)
    _ax.text(-0.35, -0.15, r"$\vec{0}$", fontsize=15)
    _ax.set_xlim(-0.7, 4.6)
    _ax.set_ylim(-0.3, 2.1)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(r"## 5 &nbsp; Lines and Planes and the cross-product in $\mathbb{R}^3$ (MT 1.3)"),
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
    """
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
def _(BLUE, GREEN, RED, mo, patch3, project3, space, t_line, vec3):
    _t = t_line.value
    _g = (_t + 0.0, 1 + 2 * _t + 0.0, 1)
    _fig, _ax = space((5.4, 3.0), (-3.2, 5.4), (-1.35, 2.05), ((0, 2.7), (0, 5.6), (0, 2)))
    # A gently inclined supporting plane containing the whole line.
    patch3(_ax, (-1.6, -2.2, 1), (3.6, 0, 0.216), (0, 6.6, -0.198))
    _a, _b = project3((-1.5, -2, 1)), project3((1.5, 4, 1))
    _ax.plot([_a[0], _b[0]], [_a[1], _b[1]], color="#777777", lw=0.9, zorder=4)
    vec3(_ax, (1, 2, 0), GREEN, zorder=1)
    vec3(_ax, (0, 1, 1), RED, zorder=1)
    vec3(_ax, _g, BLUE, zorder=1)
    _ax.plot(*project3(_g), "o", color=BLUE, ms=4.3, zorder=6)
    for _color, _label in ((GREEN, r"$\vec{v}$"), (RED, r"$\vec{x}$"), (BLUE, r"$\gamma(t)$")):
        _ax.plot([], [], color=_color, lw=1.3, label=_label)
    _fig.subplots_adjust(bottom=0.16)
    _fig.legend(loc="lower center", bbox_to_anchor=(0.5, 0.01), ncol=3, frameon=False, fontsize=12)

    mo.vstack(
        [
            mo.hstack(
                [t_line, mo.md(rf"$\gamma({_t:g}) = \begin{{bmatrix}} {_g[0]:g} \\ {_g[1]:g} \\ {_g[2]:g} \end{{bmatrix}}$")],
                justify="start",
                gap=3,
                align="center",
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, definition, label3, mo, plane_schematic, project3):
    _fig, _ax, _x, _u, _v = plane_schematic()
    _point = tuple(x + u + v / 2 for x, u, v in zip(_x, _u, _v))
    _ax.plot(*project3(_point), "o", color=BLUE, ms=4.3, zorder=6)
    label3(_ax, _point, r"$\varphi(s,t)$", BLUE, (-6, 8), ha="right")
    label3(_ax, (-1.45, 2.8, 0.9725), "$P$", "#455566", (0, 9), ha="center", va="center", size=13)

    mo.vstack(
        [
            definition(
                r"""
    Given a line $L$ with an affine parameterization

    $$
    \gamma(t) = \vec{x} + t\vec{v}
    $$

    we call $\vec{x}$ the **starting point** and $\vec{v}$ the **velocity** of $L$ with respect to the parameterization $\gamma$.
    """
            ),
            mo.md(
                r"""
    **Remark.** There exists a unique line through $\vec{x}, \vec{y} \in \mathbb{R}^3$ iff $\vec{y} - \vec{x}$ is non-zero.

    However, parameterizations are not unique!

    $$
    \begin{aligned}
    L &= \left\{\, \gamma(t) = \vec{x} + t(\vec{y} - \vec{x}) \;\middle|\; t \in \mathbb{R} \,\right\} \\
    &= \left\{\, \tilde{\gamma}(t) = \vec{y} + 2t(\vec{x} - \vec{y}) \;\middle|\; t \in \mathbb{R} \,\right\} \\
    &= \left\{\, \hat{\gamma}(t) = \tfrac{1}{2}(\vec{x} + \vec{y}) + t(\vec{x} - \vec{y}) \;\middle|\; t \in \mathbb{R} \,\right\}
    \end{aligned}
    $$

    **Remark.** For any pair of affine parameterizations $\gamma, \tilde{\gamma}$ of a line $L$, the velocity vectors are proportional!
    """
            ),
            definition(
                r"""
    Given $\vec{x}, \vec{u}, \vec{v} \in \mathbb{R}^3$, with $\vec{u}, \vec{v}$ not proportional, the **plane** through $\vec{x}$ in the directions of $\vec{u}$ and $\vec{v}$ is the set

    $$
    P = \left\{\, \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v} \;\middle|\; s, t \in \mathbb{R} \,\right\}
    $$

    $\varphi : \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ is an affine parameterization of the plane.
    """
            ),
            mo.center(_fig),
            mo.vstack(
                [
                    mo.md(
                        r"""
    **Example.**

    $$
    \vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad
    \vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad
    \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}
    $$

    $$
    \leadsto \quad \varphi(s, t) = \begin{bmatrix} s - t \\ 1 + 2s + 3t \\ 1 \end{bmatrix}
    $$
    """
                    ),
                ],
                gap=2,
            ),
            mo.md(
                r"""
    **Remark.** There exists a unique plane through $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^3$ iff $\vec{y} - \vec{x}$, $\vec{z} - \vec{x}$ are not proportional.

    $$
    P = \left\{\, \varphi(s, t) = \vec{x} + s(\vec{y} - \vec{x}) + t(\vec{z} - \vec{x}) \;\middle|\; s, t \in \mathbb{R} \,\right\}
    $$

    Different parameterizations are also possible, with different starting points and directions.
    """
            ),
            definition(
                r"""
    Given a plane $P = \left\{\, \vec{x} + s\vec{u} + t\vec{v} \;\middle|\; s, t \in \mathbb{R} \,\right\}$, a vector $\vec{n} \in \mathbb{R}^3$ is called **normal** to $P$ if

    $$
    \vec{n} \cdot \vec{u} = \vec{n} \cdot \vec{v} = 0
    $$

    ($\vec{n}$ is orthogonal to both directions in $P$).
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(GREEN, definition, mo, np, patch3, plane_schematic, space, vec3):
    _u, _v = (1.25, 0.3, -0.1), (0.35, 1.25, 0.15)
    _w = np.cross(_u, _v)
    _fig, _ax = space((2.8, 3.1), (-1.25, 1.65), (-1.8, 1.95))
    patch3(_ax, (0, 0, 0), _u, _v)
    vec3(_ax, _u, GREEN, r"$\vec{u}$", label_offset=(-6, -4), label_ha="right", label_va="top")
    vec3(_ax, _v, GREEN, r"$\vec{v}$", label_offset=(6, -4), label_va="top")
    vec3(_ax, _w, "black", r"$\vec{w}$")
    vec3(_ax, -_w, "black", r"$-\vec{w}$", label_offset=(6, -4), label_va="top", zorder=1)

    _fig2, _ax2, _x, _u, _v = plane_schematic()
    _normal = np.cross(_u, _v)
    _normal = 1.4 * _normal / np.linalg.norm(_normal)
    vec3(_ax2, _normal, "black", r"$\vec{n} = \alpha\, \vec{u} \times \vec{v}$", origin=_x, label_offset=(6, 5))

    mo.vstack(
        [
            definition(
                r"""
    Given two vectors $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}, \ \vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix} \in \mathbb{R}^3$, define their **cross-product** $\vec{u} \times \vec{v} = \vec{0}$ if they are linearly dependent.

    Otherwise, $\vec{w} = \vec{u} \times \vec{v} \in \mathbb{R}^3$ is the unique vector such that

    $$
    \vec{u} \cdot \vec{w} = 0, \quad \vec{v} \cdot \vec{w} = 0 \qquad (\text{orthogonal to both } \vec{u}, \vec{v})
    $$

    $$
    \lVert \vec{w} \rVert^2 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2
    = \Big(\underbrace{\lVert \vec{u} \rVert\, \lVert \vec{v} \rVert \sin\!\big(\theta(\vec{u}, \vec{v})\big)}_{\text{area of parallelogram spanned by } \vec{u} \text{ and } \vec{v}}\Big)^2
    $$

    and $\vec{u}, \vec{v}, \vec{w}$ is **right-handed** (positively oriented).
    """
            ),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"""
    With your right hand: rotating your fingers from $\vec{u}$ to $\vec{v}$ points your thumb towards $\vec{w}$.

    Algebraically: $\vec{u}, \vec{v}, \vec{w}$ is right-handed if

    $$
    \det \begin{bmatrix} \vec{u} & \vec{v} & \vec{w} \end{bmatrix} > 0
    $$
    """
                    ),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
            mo.vstack(
                [
                    mo.md(
                        r"""
    **Remark.** Given a parameterization

    $$
    \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}
    $$

    of a plane $P$, every normal vector to $P$ is proportional to the cross-product $\vec{u} \times \vec{v}$.
    """
                    ),
                    mo.center(_fig2),
                ],
                gap=2,
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
    Given $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}$ and $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix}$ in $\mathbb{R}^3$

    $$
    \begin{aligned}
    \vec{u} \times \vec{v} &= \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ u^1 & u^2 & u^3 \\ v^1 & v^2 & v^3 \end{bmatrix} \\
    &= \vec{e}_1 \det \begin{bmatrix} u^2 & u^3 \\ v^2 & v^3 \end{bmatrix} \\
    &\quad - \vec{e}_2 \det \begin{bmatrix} u^1 & u^3 \\ v^1 & v^3 \end{bmatrix} + \vec{e}_3 \det \begin{bmatrix} u^1 & u^2 \\ v^1 & v^2 \end{bmatrix} \\
    &= \vec{e}_1 (u^2 v^3 - u^3 v^2) \\
    &\quad - \vec{e}_2 (u^1 v^3 - u^3 v^1) + \vec{e}_3 (u^1 v^2 - u^2 v^1) \\
    &= \begin{bmatrix} u^2 v^3 - u^3 v^2 \\ u^3 v^1 - u^1 v^3 \\ u^1 v^2 - u^2 v^1 \end{bmatrix} = \vec{w}
    \end{aligned}
    $$
    """
            ),
            mo.md(
                r"""
    Not an honest determinant! The 1st row is made of vectors…

    **Proof.**

    $$
    \begin{aligned}
    \vec{u} \cdot \vec{w} &= \cancel{u^1 u^2 v^3} - \bcancel{u^1 u^3 v^2} + \xcancel{u^2 u^3 v^1} \\
    &\quad - \cancel{u^2 u^1 v^3} + \bcancel{u^3 u^1 v^2} - \xcancel{u^3 u^2 v^1} \\
    &= 0 \\[4pt]
    \vec{v} \cdot \vec{w} &= 0
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \lVert \vec{w} \rVert^2 &= (u^2 v^3 - u^3 v^2)^2 + (u^3 v^1 - u^1 v^3)^2 \\
    &\quad + (u^1 v^2 - u^2 v^1)^2 \\
    &= \big( (u^1)^2 + (u^2)^2 + (u^3)^2 \big) \\
    &\quad \cdot \big( (v^1)^2 + (v^2)^2 + (v^3)^2 \big) \\
    &\quad - \big( u^1 v^1 + u^2 v^2 + u^3 v^3 \big)^2 \\
    &= \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2 \quad (\text{check!})
    \end{aligned}
    $$

    $$
    \begin{aligned}
    &\det \begin{bmatrix} u^1 & v^1 & (u^2 v^3 - u^3 v^2) \\ u^2 & v^2 & (u^3 v^1 - u^1 v^3) \\ u^3 & v^3 & (u^1 v^2 - u^2 v^1) \end{bmatrix} \\
    &\qquad = \lVert \vec{w} \rVert^2 \geq 0 \qquad (\text{check!})
    \end{aligned}
    $$

    This is strictly positive when $\vec{u}, \vec{v}$ are linearly independent; otherwise $\vec{w} = \vec{0}$.

    **Example.** &nbsp; $\vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}$

    $$
    \begin{aligned}
    \leadsto \quad \vec{u} \times \vec{v} &= \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 2 & 0 \\ -1 & 3 & 0 \end{bmatrix} \\
    &= 0\, \vec{e}_1 + 0\, \vec{e}_2 + \big( 1 \cdot 3 - 2 \cdot (-1) \big)\, \vec{e}_3 \\
    &= 5\, \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 5 \end{bmatrix}
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \vec{u} \cdot (\vec{u} \times \vec{v}) &= 1 \cdot 0 + 2 \cdot 0 + 0 \cdot 5 = 0 \\
    \vec{v} \cdot (\vec{u} \times \vec{v}) &= (-1) \cdot 0 + 3 \cdot 0 + 0 \cdot 5 = 0 \\
    \lVert \vec{u} \times \vec{v} \rVert^2 &= \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2 \\
    &= (1 + 4)(1 + 9) - (-1 + 6)^2 \\
    &= 50 - 25 = 25
    \end{aligned}
    $$

    $$
    \begin{aligned}
    &\det \begin{bmatrix} 1 & -1 & 0 \\ 2 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix} \\
    &= 1\, (3 \cdot 5 - 0 \cdot 0) \\
    &\quad - (-1)\, (2 \cdot 5 - 0 \cdot 0) + 0\, (2 \cdot 0 - 3 \cdot 0) \\
    &= 25 > 0 \qquad (= \lVert \vec{u} \times \vec{v} \rVert^2\,!)
    \end{aligned}
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
def _(GREEN, depth3, math, mo, patch3, project3, space, u1, u2, u3, v1, v2, v3, vec3):
    _u = (u1.value, u2.value, u3.value)
    _v = (v1.value, v2.value, v3.value)
    _w = (_u[1] * _v[2] - _u[2] * _v[1], _u[2] * _v[0] - _u[0] * _v[2], _u[0] * _v[1] - _u[1] * _v[0])
    _w = tuple(c + 0.0 for c in _w)
    _norm = math.sqrt(sum(c * c for c in _w))
    _sum = tuple(a + b for a, b in zip(_u, _v))
    _lim = max(3.5, 1.15 * max(abs(c) for point in (_u, _v, _w, _sum) for c in project3(point)))
    _axis_len = max(1.5, max(abs(c) for c in (*_u, *_v)))

    _fig, _ax = space((5.2, 4.2), (-_lim, _lim), (-_lim, _lim), ((-0.25 * _axis_len, _axis_len),) * 3)
    patch3(_ax, (0, 0, 0), _u, _v)
    vec3(_ax, _u, GREEN, r"$\vec{u}$" if any(_u) else None,
         label_offset=(-6, -8), label_ha="right", label_va="top")
    vec3(_ax, _v, GREEN, r"$\vec{v}$" if any(_v) else None)
    if _norm > 0:
        vec3(_ax, _w, "black", zorder=5 if depth3(_w) >= 0 else 1)
    for _color, _label in ((GREEN, r"$\vec{u},\,\vec{v}$"), ("black", r"$\vec{u} \times \vec{v}$")):
        _ax.plot([], [], color=_color, lw=1.3, label=_label)
    _fig.subplots_adjust(bottom=0.13)
    _fig.legend(loc="lower center", bbox_to_anchor=(0.5, 0.01), ncol=2, frameon=False, fontsize=12)

    mo.vstack(
        [
            mo.hstack([mo.vstack([u1, u2, u3]), mo.vstack([v1, v2, v3])], justify="start", gap=3),
            mo.vstack(
                [
                    mo.center(_fig),
                    mo.md(
                        rf"$$\vec{{u}} \times \vec{{v}} = \begin{{bmatrix}} {_w[0]:g} \\ {_w[1]:g} \\ {_w[2]:g} \end{{bmatrix}}$$"
                        "\n\n"
                        rf"$$\lVert \vec{{u}} \times \vec{{v}} \rVert = {_norm:.3f} = \text{{area of the parallelogram}}$$"
                    ),
                ],
                gap=2,
            ),
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

    This **cannot** be extended to other $\mathbb{R}^n$ with $n \neq 3, 7$.
    """
            ),
            theorem(
                r"""
    Given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$, $\alpha, \beta \in \mathbb{R}$

    - $\vec{u} \times \vec{v} = -\vec{v} \times \vec{u}$ &nbsp; (anti-commutativity)
    - $\vec{u} \times (\alpha \vec{v} + \beta \vec{w}) = \alpha (\vec{u} \times \vec{v}) + \beta (\vec{u} \times \vec{w})$ and $(\alpha \vec{u} + \beta \vec{v}) \times \vec{w} = \alpha (\vec{u} \times \vec{w}) + \beta (\vec{v} \times \vec{w})$ &nbsp; (bilinearity)
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


if __name__ == "__main__":
    app.run()
