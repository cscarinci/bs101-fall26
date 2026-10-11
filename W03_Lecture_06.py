import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 06 · Multivariable functions", css_file="bs101.css")


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
    OCHRE = "#9a6b1f"

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
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.3, "mutation_scale": 9, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=14)

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

    return BLUE, GREEN, GREY, OCHRE, RED, arrow, check, definition, header, plane, theorem, warning


@app.cell(hide_code=True)
def _(header):
    header("Lecture 06", "Week 03", "Lecture 06 · Multivariable functions")
    return


@app.cell(hide_code=True)
def _(Figure):
    # ---- 3D drawing helpers  -----------------------------
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    def space(figsize, xlim, ylim, zlim, elev=22, azim=28, zoom=1.2):
        """A 3D axis showing the three coordinate axes, with equal scales."""
        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(projection="3d")
        ax.set_proj_type("ortho")
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        for lo, hi, d in ((xlim[0], xlim[1], 0), (ylim[0], ylim[1], 1), (zlim[0], zlim[1], 2)):
            a, b = [0, 0, 0], [0, 0, 0]
            a[d], b[d] = min(lo, 0), hi
            ax.quiver(*a, *[q - p for p, q in zip(a, b)], color="black", lw=0.9, arrow_length_ratio=0.04)
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_zlim(*zlim)
        ax.set_box_aspect((xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0]), zoom=zoom)
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
        return fig, ax

    def vec3(ax, v, color, label=None, origin=(0, 0, 0), lw=1.3):
        """Draw the vector v starting at `origin`."""
        ax.quiver(*origin, *v, color=color, lw=lw, arrow_length_ratio=0.12)
        if label:
            tip = [o + 1.08 * c for o, c in zip(origin, v)]
            ax.text(*tip, label, color=color, fontsize=15)

    def patch3(ax, origin, u, v, color, alpha=0.2):
        """Shade the parallelogram with corner `origin` and sides u, v."""
        o = list(origin)
        p1 = [a + b for a, b in zip(o, u)]
        p2 = [a + b for a, b in zip(p1, v)]
        p3 = [a + b for a, b in zip(o, v)]
        ax.add_collection3d(Poly3DCollection([[o, p1, p2, p3]], color=color, alpha=alpha, lw=0))

    return patch3, space, vec3


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## So far

    Euclidean Geometry

    - vectors, lines, planes
    - dot products and cross-products (in $\mathbb{R}^3$): lengths, angles, areas, volumes

    **Today:** Multivariable functions — objects of interest in Multivariable Calculus
    """
            ),
            definition(
                r"""
    A **multivariable function** is a rule

    $$
    f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m
    $$

    that assigns to each element $\vec{x}$ in a set $A \subseteq \mathbb{R}^n$ a unique element $\vec{y} = f(\vec{x})$ in another set $B \subseteq \mathbb{R}^m$.
    """
            ),
            mo.md(
                r"""
    There are 3 parts to a function:

    | | |
    |:--|:--|
    | $\mathrm{Dom}(f) = A$ | set of allowed inputs |
    | $\mathrm{Codom}(f) = B$ | set of desired outputs |
    | $\vec{x} \longmapsto f(\vec{x})$ | the rule of assignment |

    Change any one of these and you have a different function!

    **Remark.** Sometimes we will call

    - $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}$ &nbsp; ($m = 1$) &nbsp; a **scalar function** on $\mathbb{R}^n$ (or scalar-valued function)
    - $f : A \subseteq \mathbb{R} \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; ($n = 1$) &nbsp; a **path** in $\mathbb{R}^m$
    - $f : A \subseteq \mathbb{R}^2 \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; ($n = 2$) &nbsp; a **parameterized surface** in $\mathbb{R}^m$
    - $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; a **map** from $A \subseteq \mathbb{R}^n$ to $B \subseteq \mathbb{R}^m$

    **Example.** Lengths

    $$
    \begin{aligned}
    \lVert \cdot \rVert : \mathbb{R}^n &\longrightarrow \mathbb{R} \\
    \vec{x} &\longmapsto \sqrt{(x^1)^2 + (x^2)^2 + \dots + (x^n)^2}
    \end{aligned}
    $$

    Affine parameterizations

    $$
    \begin{aligned}
    \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^3 \\
    t &\longmapsto \begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \\ x^3 + t v^3 \end{bmatrix}
    \end{aligned}
    $$

    $t$ is the variable; $\vec{x}$ and $\vec{v}$ are fixed here.

    $$
    \begin{aligned}
    \varphi : \mathbb{R}^2 &\longrightarrow \mathbb{R}^3 \\
    (s, t) &\longmapsto \begin{bmatrix} x^1 + s u^1 + t v^1 \\ x^2 + s u^2 + t v^2 \\ x^3 + s u^3 + t v^3 \end{bmatrix}
    \end{aligned}
    $$

    $(s,t)$ are the variables; $\vec{x}$, $\vec{u}$ and $\vec{v}$ are fixed here.

    Linear transformations

    $$
    \begin{aligned}
    T : \mathbb{R}^n &\longrightarrow \mathbb{R}^m \\
    \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} &\longmapsto \begin{bmatrix} t^1{}_1 x^1 + \dots + t^1{}_n x^n \\ \vdots \\ t^m{}_1 x^1 + \dots + t^m{}_n x^n \end{bmatrix}
    \end{aligned}
    $$

    $x^1, \dots, x^n$ are the variables, $t^i{}_j$ are fixed.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"## Basic properties"),
            definition(
                r"""
    Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$

    - the **image** of $f$ is

        $$
        \mathrm{Im}(f) = \left\{\, f(\vec{x}) \;\middle|\; \vec{x} \in A \,\right\} \subseteq B
        $$

        Not necessarily equal! $\mathrm{Im}(f) \subseteq \mathrm{Codom}(f)$

    - the **graph** of $f$ is

        $$
        \mathrm{graph}(f) = \left\{\, (\vec{x}, f(\vec{x})) \;\middle|\; \vec{x} \in A \,\right\} \subseteq A \times B
        $$
    """
            ),
            mo.md(
                r"""
    **Example.** $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ affine parameterization

    $$
    \gamma(t) = \vec{x} + t\vec{v} \qquad (\text{with } \vec{v} \neq \vec{0})
    $$

    $$
    \mathrm{Im}(\gamma) = \left\{\, \gamma(t) \;\middle|\; t \in \mathbb{R} \,\right\} \subseteq \mathbb{R}^2
    $$

    This is the line through $\vec{x}$ in the direction of $\vec{v}$.

    $$
    \mathrm{graph}(\gamma) = \left\{\, (t, \gamma(t)) \;\middle|\; t \in \mathbb{R} \,\right\}
    $$

    It lies in $\mathbb{R} \times \mathbb{R}^2 \approx \mathbb{R}^3$.

    $$
    (0, \vec{x}) = \begin{bmatrix} 0 \\ x^1 \\ x^2 \end{bmatrix}, \qquad
    (t, \vec{x} + t\vec{v}) = \begin{bmatrix} t \\ x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_path = mo.ui.slider(-1, 3, 0.25, value=1.5, label="$t$", show_value=True)
    return (t_path,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, OCHRE, RED, arrow, mo, t_path):
    _x, _v, _t = (3.2, 0.8), (-0.8, 0.5), t_path.value
    _g = (_x[0] + _t * _v[0], _x[1] + _t * _v[1])

    _fig = Figure(figsize=(5.2, 3.2))
    _fig.subplots_adjust(left=0.04, right=0.96, bottom=0.06, top=0.88)

    # Im(gamma): a line in R^2
    _ax = _fig.subplots()
    _ax.set_xlim(-1.2, 5.6)
    _ax.set_ylim(-0.6, 3.4)
    _ax.set_aspect("equal")
    _ax.axis("off")
    arrow(_ax, (-1.2, 0), (5.3, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.6), (0, 3.1), "black", lw=0.9)
    _ax.text(5.1, -0.4, "$y^1$")
    _ax.text(-0.5, 2.95, "$y^2$")
    _ax.plot([_x[0] - 1.6 * _v[0], _x[0] + 3.6 * _v[0]], [_x[1] - 1.6 * _v[1], _x[1] + 3.6 * _v[1]], color=OCHRE, lw=1.6)
    arrow(_ax, (0, 0), _v, GREEN, r"$\vec{v}$", at_tip=True)
    arrow(_ax, (0, 0), _x, RED)
    arrow(_ax, (0, 0), _g, BLUE)
    _ax.plot(*_x, "o", color=RED, ms=4)
    _ax.plot(*_g, "o", color=BLUE, ms=4)
    _ax.annotate(r"$\vec{x} = \gamma(0)$", _x, xytext=(-6, -16), textcoords="offset points", ha="right", va="top", color=RED, fontsize=13)
    _ax.annotate(r"$\gamma(t)$", _g, xytext=(6, 8), textcoords="offset points", color=BLUE, fontsize=13)
    _ax.set_title(r"$\mathrm{Im}(\gamma)$", color=OCHRE)

    # graph(gamma): a line in R x R^2, drawn with t to the right, y^1 towards us, y^2 up
    _fig3 = Figure(figsize=(5.2, 3.8))
    _fig3.subplots_adjust(left=0.02, right=0.98, bottom=0.16, top=0.90)
    _ax3 = _fig3.add_subplot(projection="3d")
    _ax3.set_proj_type("ortho")
    for _d in ((4.6, 0, 0), (0, 4, 0), (0, 0, 3)):
        _ax3.quiver(0, 0, 0, *_d, color="black", lw=0.9, arrow_length_ratio=0.05)
    _ax3.plot([0, 0], [-1.25, 0], [0, 0], color="black", lw=0.9)
    _ax3.text(4.6, 0.25, 0, "$y^1$")
    _ax3.text(0, 3.6, 0.25, "$t$")
    _ax3.text(0, -0.1, 3.15, "$y^2$")
    _ts = (-1, 3)
    _ax3.plot([_x[0] + s * _v[0] for s in _ts], list(_ts), [_x[1] + s * _v[1] for s in _ts], color=OCHRE, lw=1.6)
    _ax3.plot([0, _g[0]], [_t, _t], [0, 0], "--", color="#888888", lw=1)
    _ax3.plot([_g[0], _g[0]], [0, _t], [0, 0], "--", color="#888888", lw=1)
    _ax3.plot([_g[0], _g[0]], [_t, _t], [0, _g[1]], "--", color="#888888", lw=1)
    _ax3.plot([0, _g[0]], [0, _t], [_g[1], _g[1]], "--", color="#888888", lw=1)
    _ax3.scatter([_x[0]], [0], [_x[1]], color=RED, s=20, depthshade=False, label=r"$(0,\vec{x})$")
    _ax3.scatter([_g[0]], [_t], [_g[1]], color=BLUE, s=20, depthshade=False, label=r"$(t,\gamma(t))$")
    _ax3.set_xlim(0, 4.6)
    _ax3.set_ylim(-1.25, 4)
    _ax3.set_zlim(0, 3)
    _ax3.set_box_aspect((4.6, 5.25, 3), zoom=1.05)
    _ax3.view_init(elev=22, azim=28)
    _ax3.set_axis_off()
    _ax3.set_title(r"$\mathrm{graph}(\gamma)$", color=OCHRE)
    _fig3.legend(loc="lower center", bbox_to_anchor=(0.5, 0.02), ncol=2, frameon=False, fontsize=12)

    mo.vstack([t_path, mo.center(_fig), mo.center(_fig3)])
    return


@app.cell(hide_code=True)
def _(Figure, OCHRE, RED, arrow, definition, math, mo, np):
    # The sphere of radius 2, drawn as seen from a fixed direction (orthographic view)
    _e, _a = math.radians(22), math.radians(28)
    _right = np.array([-math.sin(_a), math.cos(_a), 0.0])
    _up = np.array([-math.sin(_e) * math.cos(_a), -math.sin(_e) * math.sin(_a), math.cos(_e)])
    _toward = np.array([math.cos(_e) * math.cos(_a), math.cos(_e) * math.sin(_a), math.sin(_e)])

    def _flat(p):
        p = np.asarray(p, dtype=float)
        return p @ _right, p @ _up

    _fig = Figure(figsize=(4.4, 4.2), layout="constrained")
    _ax = _fig.subplots()
    _th = np.linspace(0, 2 * np.pi, 361)
    _ax.fill(2 * np.cos(_th), 2 * np.sin(_th), color=OCHRE, alpha=0.10, lw=0)
    _ax.plot(2 * np.cos(_th), 2 * np.sin(_th), color=OCHRE, lw=1.8)
    # equator: solid on the near side, dashed on the far side
    _eq = np.stack([2 * np.cos(_th), 2 * np.sin(_th), 0 * _th], axis=1)
    _near = _eq @ _toward >= 0
    for _mask, _style in ((_near, "-"), (~_near, "--")):
        _u, _w = _flat(np.where(_mask[:, None], _eq, np.nan))
        _ax.plot(_u, _w, _style, color=OCHRE, lw=1.3)
    # coordinate axes, with the points where they meet the sphere
    for _d, _off in zip(np.eye(3), ((4, 5), (-4, -16), (5, 5))):
        _tail, _tip = _flat(-0.9 * _d), _flat(3.1 * _d)
        arrow(_ax, _tail, _tip, "black", lw=0.9)
        _ax.plot(*_flat(2 * _d), "o", color=RED, ms=4)
        _m = _flat(2 * _d)
        _ax.annotate("$2$", _m, textcoords="offset points", xytext=_off, color=RED, fontsize=12)
    # two points of the level set
    for _mix, _name in (((0.42, 0.85, 0.3), r"$\vec{x}$"), ((0.8, 0.5, 0.33), r"$\vec{y}$")):
        _pt = _mix[0] * _right + _mix[1] * _up + _mix[2] * _toward
        _q = 2 * _pt / np.linalg.norm(_pt)
        arrow(_ax, (0, 0), _flat(_q), RED, _name, at_tip=True)
        _ax.plot(*_flat(_q), "o", color=RED, ms=4)
    _ax.annotate(r"$\vec{0}$", (0, 0), textcoords="offset points", xytext=(6, -16), color=RED, fontsize=14)
    _ax.text(1.5, -2.25, "$f^{-1}(2)$", color=OCHRE, fontsize=16)
    _ax.set_xlim(-2.9, 3.3)
    _ax.set_ylim(-2.7, 3.3)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** $\mathrm{Im}(f)$ and $\mathrm{graph}(f)$ help us visualize $f$ as a set of points (very useful in lower dimensions).

    - We might have many functions with same image.
    - The graph determines the domain and rule, but not the codomain (and lives in higher dimensions).
    """
            ),
            definition(
                r"""
    Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$, $\vec{b} \in B$ fixed

    - the **level set** of $f$ with value $\vec{b}$ is

        $$
        f^{-1}(\vec{b}) = \left\{\, \vec{x} \in A \;\middle|\; f(\vec{x}) = \vec{b} \,\right\}
        $$
    """
            ),
            mo.vstack(
                [
                    mo.md(
                        r"""
    **Example.**

    $$
    \begin{aligned}
    f : \mathbb{R}^3 &\longrightarrow \mathbb{R} \\
    \vec{x} &\longmapsto \lVert \vec{x} \rVert
    \end{aligned}
    $$

    Fix $r = 2$

    $$
    f^{-1}(2) = \left\{\, \vec{x} \in \mathbb{R}^3 \;\middle|\; \lVert \vec{x} \rVert = 2 \,\right\}
    $$

    This is the sphere centered at $\vec{0}$ with radius $2$.
    """
                    ),
                    mo.center(_fig),
                ],
                gap=2,
            ),
            mo.md(
                r"""
    **Remark.** Here $f^{-1}(\vec{b})$ is NOT the value of the inverse function of $f$ (we don't even know if $f$ has an inverse).

    $f^{-1}(\vec{b})$ is the set of points in the domain of $f$ which gives the value “$\vec{b}$” as an output!

    If $f$ is invertible then, for each $\vec{b} \in B$,

    $$
    f^{-1}(\vec{b}) = \left\{\, \vec{x} \in A \;\middle|\; f(\vec{x}) = \vec{b} \,\right\}
    $$

    has a single element, which we call “$f^{-1}(\vec{b})$”.

    **Example.**

    $$
    \begin{aligned}
    f : \mathbb{R}^2 &\longrightarrow \mathbb{R} \\
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} &\longmapsto (x^1)^2 - (x^2)^2
    \end{aligned}
    $$

    What are the level sets with values $1, 0, -4$?

    $$
    f^{-1}(b) = \left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \;\middle|\; (x^1)^2 - (x^2)^2 = b \,\right\}
    $$

    - $f^{-1}(0) \iff \lvert x^1 \rvert = \lvert x^2 \rvert$ &nbsp; a cone
    - $f^{-1}(1) \iff (x^1)^2 - (x^2)^2 = 1$ &nbsp; a hyperbola
    - $f^{-1}(-4) \iff (x^1)^2 - (x^2)^2 = -4$ &nbsp; also a hyperbola
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    b_level = mo.ui.slider(-4, 4, 0.5, value=1, label="$b$", show_value=True)
    return (b_level,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, OCHRE, RED, b_level, mo, np):
    _b = b_level.value
    _g = np.linspace(-4, 4, 401)
    _X, _Y = np.meshgrid(_g, _g)
    _F = _X**2 - _Y**2

    _fig = Figure(figsize=(4.6, 4.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-4, 4)
    _ax.set_ylim(-4, 4)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.set_xlabel("$x^1$")
    _ax.set_ylabel("$x^2$", rotation=0)
    for _val, _col in ((0, GREEN), (1, OCHRE), (-4, RED)):
        _ax.contour(_X, _Y, _F, levels=[_val], colors=[_col], linewidths=1.2, alpha=0.55, linestyles="solid")
    _ax.contour(_X, _Y, _F, levels=[_b], colors=[BLUE], linewidths=1.6, linestyles="solid")
    _ax.set_title(rf"$f^{{-1}}({_b:g})$", color=BLUE)

    mo.vstack(
        [
            b_level,
            mo.vstack(
                [
                    mo.center(_fig),
                    mo.md(
                        rf"$$f^{{-1}}({_b:g}) : \quad (x^1)^2 - (x^2)^2 = {_b:g}$$"
                        "\n\n"
                        r"The thin curves are $f^{-1}(0)$, $f^{-1}(1)$ and $f^{-1}(-4)$."
                    ).style({"max-width": "26rem"}),
                ],
                gap=2,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{aligned}
    g : \mathbb{R}^3 &\longrightarrow \mathbb{R} \\
    \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} &\longmapsto (x^1)^2 + (x^2)^2 - (x^3)^2
    \end{aligned}
    $$

    - $g^{-1}(0)$ &nbsp; cone
    - $g^{-1}(1)$ &nbsp; hyperboloid of one sheet
    - $g^{-1}(-4)$ &nbsp; hyperboloid of two sheets
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, b_level, mo, np, space):
    _b = b_level.value
    _fig, _ax = space((5.0, 4.8), (-4, 4), (-4, 4), (-3.5, 3.5), zoom=1.3)
    _th = np.linspace(0, 2 * np.pi, 49)
    if _b >= 0:
        # one sheet (or the cone): radius as a function of height
        _z = np.linspace(-3, 3, 41)
        _TH, _Z = np.meshgrid(_th, _z)
        _R = np.sqrt(_b + _Z**2)
        _sheets = [(_R * np.cos(_TH), _R * np.sin(_TH), _Z)]
        _name = "cone" if _b == 0 else "hyperboloid of one sheet"
    else:
        # two sheets: height as a function of radius
        _r = np.linspace(0, np.sqrt(9 + _b), 25)
        _TH, _R = np.meshgrid(_th, _r)
        _Z = np.sqrt(_R**2 - _b)
        _sheets = [(_R * np.cos(_TH), _R * np.sin(_TH), _Z), (_R * np.cos(_TH), _R * np.sin(_TH), -_Z)]
        _name = "hyperboloid of two sheets"
    for _S in _sheets:
        _ax.plot_surface(*_S, color=BLUE, alpha=0.20, lw=0.3, edgecolor=BLUE, rstride=4, cstride=4)

    mo.vstack(
        [
            b_level,
            mo.vstack(
                [
                    mo.center(_fig),
                    mo.md(rf"$$g^{{-1}}({_b:g}) : \quad (x^1)^2 + (x^2)^2 - (x^3)^2 = {_b:g}$$" "\n\n" + _name).style(
                        {"max-width": "26rem"}
                    ),
                ],
                gap=2,
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
    For $p : \mathbb{R}^3 \longrightarrow \mathbb{R}$ an **affine scalar function**

    $$
    p\!\left( \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \right) = a x^1 + b x^2 + c x^3 + d
    $$

    If $(a,b,c) \neq (0,0,0)$, then $p^{-1}(r)$ is a plane with normal vector $\begin{bmatrix} a \\ b \\ c \end{bmatrix}$.

    If $a \neq 0$, a starting point is $\begin{bmatrix} (r-d)/a \\ 0 \\ 0 \end{bmatrix}$.

    If $a=b=c=0$, then $p^{-1}(r)=\mathbb{R}^3$ when $r=d$, and $\varnothing$ otherwise.

    For $q : \mathbb{R}^3 \longrightarrow \mathbb{R}$ a **quadratic scalar function**

    $$
    \begin{aligned}
    q(\vec{x}) &= a (x^1)^2 + b (x^2)^2 + c (x^3)^2 \\
    &\quad + d\, x^1 x^2 + e\, x^2 x^3 + f\, x^3 x^1 \\
    &\quad + g\, x^1 + h\, x^2 + i\, x^3 + j
    \end{aligned}
    $$

    $q^{-1}(r)$ is called a **quadratic surface**.
    """
            ),
            mo.md(
                r"""
    | | |
    |:--|:--|
    | $\dfrac{(x^1)^2}{a^2} + \dfrac{(x^2)^2}{b^2} + \dfrac{(x^3)^2}{c^2} = r^2$ | ellipsoids |
    | $\dfrac{(x^1)^2}{a^2} + \dfrac{(x^2)^2}{b^2} - \dfrac{(x^3)^2}{c^2} = \pm r^2$ | hyperboloids |
    | $\dfrac{(x^1)^2}{a^2} + \dfrac{(x^2)^2}{b^2} - \dfrac{x^3}{c} = d$ | paraboloids |
    | $\dots$ | |

    Here $a,b,c \neq 0$ and $r>0$.

    **Remark.** Sometimes level sets of a function can be seen as graphs of another function and vice-versa!

    $\Longrightarrow$ &nbsp; geometry of sets in $\mathbb{R}^n$ or $\mathbb{R}^m$ or $\mathbb{R}^n \times \mathbb{R}^m$ is useful to study properties of various functions!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ### Question 1

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \ln\!\big( x^2 - (x^1)^2 \big)
    $$

    (a) Find the largest possible domain and codomain.

    (b) For those, find the image.

    (c) Sketch the level sets $f^{-1}(0)$, $f^{-1}(\ln 4)$.

    ### Question 2

    Let $T : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ be given by

    $$
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \longmapsto \begin{bmatrix} x^1 + x^2 \\ (x^1 + x^2)^2 \end{bmatrix}
    $$

    (a) Sketch $\mathrm{Im}(T)$.

    (b) Describe $T^{-1}\!\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right)$ and $T^{-1}\!\left( \begin{bmatrix} 1 \\ 2 \end{bmatrix} \right)$.

    ### Question 3

    Consider the surface

    $$
    S = \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \in \mathbb{R}^3 \;\middle|\; (x^1)^2 + (x^2)^2 - x^3 = 1 \,\right\}
    $$

    Find

    (a) a function $f$ such that $S$ is a level set of $f$

    (b) a function $g$ such that $S$ is the graph of $g$

    (c) a function $h$ such that $S$ is the image of $h$
    """)
    return


if __name__ == "__main__":
    app.run()
