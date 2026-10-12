import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 11 · Affine approximations and the derivative of general maps", css_file="bs101.css")


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
            arrowprops={"arrowstyle": "->,head_width=0.3,head_length=0.5", "color": color, "lw": 1.4, "shrinkA": 0, "shrinkB": 0, **kw},
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
    header("Lecture 11", "Week 06", "Lecture 11 · Affine approximations and the derivative of general maps")
    return


@app.cell(hide_code=True)
def _(arrow):
    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    The derivative and the gradient

    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$

    $$
    \Longleftrightarrow \quad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)
    $$

    defines a good affine approximation for $f$ at $\vec{a}$ in the sense that

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$

    $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the **derivative** of $f$ at $\vec{a}$ &nbsp; (linear function taking vectors to directional derivatives)

    $\vec{\nabla} f(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\ \vdots \\ \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathbb{R}^n$ is the **gradient** of $f$ at $\vec{a}$ &nbsp; (vector pointing in some direction with some length)
    """
            ),
            theorem(
                r"""
    If $\vec{\nabla} f(\vec{a}) \neq \vec{0}$, it points in the direction of steepest ascent of $f$ at $\vec{a}$, and it is perpendicular to the level set of $f$ through $\vec{a}$ (containing $\vec{a}$).
    """
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \dfrac{(x^1)^2}{9} + \dfrac{(x^2)^2}{4}$

    $$
    \leadsto \quad \text{level sets} \quad f^{-1}(r^2) = \underbrace{\left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; \frac{(x^1)^2}{9 r^2} + \frac{(x^2)^2}{4 r^2} = 1 \,\right\}}_{\text{horizontal ellipse centered at } \vec{0} \text{ with semi-axes } 3r \text{ and } 2r} \qquad (r > 0)
    $$

    For $r = 0$, $f^{-1}(0) = \{\vec{0}\}$.

    $$
    \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \frac{2}{9} a^1 \\[4pt] \frac{2}{4} a^2 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    phi = mo.ui.slider(0, 355, 5, value=40, label=r"position of $\vec{a}$ on the ellipse (degrees)", show_value=True)
    return (phi,)


@app.cell(hide_code=True)
def _(Figure, GREEN, RED, arrow, cross_axes, math, mo, np, phi):
    _p = math.radians(phi.value)
    _a = (3 * math.cos(_p), 2 * math.sin(_p))
    _grad = (2 * _a[0] / 9, 2 * _a[1] / 4)

    _fig = Figure(figsize=(5.4, 4.0), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-4.6, 4.8), (-3.4, 3.6), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    for _r in (0.5, 1.5):
        _ax.plot(3 * _r * np.cos(_th), 2 * _r * np.sin(_th), color="#bbbbbb", lw=0.7)
    _ax.plot(3 * np.cos(_th), 2 * np.sin(_th), color=RED, lw=1.8)
    for _pt, _name, _off in (((3, 0), "$3r$", (4, 6)), ((-3, 0), "$-3r$", (-30, 6)), ((0, 2), "$2r$", (-24, 4)), ((0, -2), "$-2r$", (6, -16))):
        _ax.annotate(_name, _pt, textcoords="offset points", xytext=_off, color=RED, fontsize=12)
    arrow(_ax, (0, 0), _a, RED)
    _ax.annotate(r"$\vec{a}$", (_a[0] / 2, _a[1] / 2), textcoords="offset points", xytext=(-6, 10), color=RED, fontsize=15)
    arrow(_ax, _a, (_a[0] + 1.6 * _grad[0], _a[1] + 1.6 * _grad[1]), GREEN, r"$\vec{\nabla} f(\vec{a})$", at_tip=True)
    _ax.plot(*_a, "o", color=GREEN, ms=5)
    _ax.text(2.5, -1.75, "$f^{-1}(r^2)$", color=RED, fontsize=14)

    mo.vstack(
        [
            mo.hstack([phi], justify="start", gap=3),
            mo.md(
                "| | |\n|:--|:--|\n"
                + r"| $r$ | $1$ |" + "\n"
                + rf"| $\vec{{a}}$ | $\begin{{bmatrix}} {_a[0]:.2f} \\ {_a[1]:.2f} \end{{bmatrix}}$ |" + "\n"
                + rf"| $\vec{{\nabla}} f(\vec{{a}})$ | $\begin{{bmatrix}} {_grad[0]:.2f} \\ {_grad[1]:.2f} \end{{bmatrix}}$ |"
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    **Today:** Affine approximations and their graphs. Derivative for general maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$
    """
            ),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, the **affine approximation** of $f$ at $\vec{a}$ is the affine function (linear plus constant) $g : \mathbb{R}^n \longrightarrow \mathbb{R}$

    $$
    \begin{aligned}
    g(\vec{x}) &= f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \\
    &= f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \dots + \frac{\partial f}{\partial x^n}(\vec{a})\, (x^n - a^n)
    \end{aligned}
    $$
    """
            ),
            mo.md(
                r"""
    **Remark.** For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $g : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    g(x) = f(a) + f'(a)(x - a)
    $$

    is the affine function whose graph is the tangent line to the graph of $f$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$

    $$
    y = f(a) + f'(a)(x - a) \qquad \leadsto \qquad \begin{bmatrix} a \\ f(a) \end{bmatrix} + (x - a) \underbrace{\begin{bmatrix} 1 \\ f'(a) \end{bmatrix}}_{\text{velocity vector of the tangent line}}
    \qquad \qquad
    \underbrace{\vec{n} = \begin{bmatrix} -f'(a) \\ 1 \end{bmatrix}}_{\text{normal to the tangent line}}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_line = mo.ui.slider(0.4, 3.4, 0.1, value=0.7, label="$a$", show_value=True)
    return (a_line,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, a_line, arrow, cross_axes, math, mo, np):
    OCHRE = "#9a6b1f"
    _a = a_line.value
    _fa = 4 * _a * math.exp(-_a)
    _d = 4 * (1 - _a) * math.exp(-_a)

    _fig = Figure(figsize=(7.2, 3.4), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-1.6, 5.2), (-0.5, 2.6), "$x$")
    _ax.annotate("$y$", (0, 2.6), textcoords="offset points", xytext=(-14, -12), fontsize=13)
    _x = np.linspace(-0.08, 5, 300)
    _ax.plot(_x, 4 * _x * np.exp(-_x), color=RED, lw=1.8)
    _s = np.array([-1.6, 5.2])
    _ax.plot(_s, _fa + _d * (_s - _a), color=GREEN, lw=1.3)
    arrow(_ax, (0, 0), (_a, _fa), BLUE)
    arrow(_ax, (_a, _fa), (_a - _d, _fa + 1), OCHRE, r"$\vec{n}$", at_tip=True)
    arrow(_ax, (_a, _fa), (_a + 1, _fa + _d), GREEN, lw=2.0)
    _ax.plot(_a, _fa, "o", color=BLUE, ms=5)
    _ax.annotate(r"$\genfrac{[}{]}{0}{0}{a}{f(a)}$", (_a, _fa), textcoords="offset points", xytext=(6, -30), color=BLUE, fontsize=14)
    _ax.text(3.9, 0.55, "$y = f(x)$", color=RED, fontsize=13)
    _ax.set_ylim(-0.5, 2.6)

    mo.vstack(
        [
            mo.hstack([a_line], justify="start", gap=3),
            mo.md("| | |\n|:--|:--|\n" + rf"| $f(a)$ | ${_fa:.2f}$ |" + "\n" + rf"| $f'(a)$ | ${_d:.2f}$ |"),
            _fig,
        ]
    )
    return (OCHRE,)


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

    The graph of the affine approximation of $f$ at $\vec{a}$ is a plane in $\mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R}$ through $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$ with normal vector $\vec{n} = \begin{bmatrix} -\dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] -\dfrac{\partial f}{\partial x^2}(\vec{a}) \\[8pt] 1 \end{bmatrix}$

    $\leadsto$ &nbsp; the **tangent plane** to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$
    """
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    \mathrm{graph}(g) &= \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\} \\[6pt]
    &= \left\{\, \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \\ Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\} \\[6pt]
    &= \left\{\, \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \underbrace{(x^1 - a^1)}_{t} \begin{bmatrix} 1 \\ 0 \\ \dfrac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix} + \underbrace{(x^2 - a^2)}_{s} \begin{bmatrix} 0 \\ 1 \\ \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\}
    \end{aligned}
    $$

    (the two vectors are the velocity vectors)

    $$
    \vec{n} = \begin{bmatrix} n^1 \\ n^2 \\ n^3 \end{bmatrix} \ \text{ s.t. } \
    \vec{n} \cdot \underbrace{\begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix}}_{\vec{u}} = 0 = \vec{n} \cdot \underbrace{\begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\vec{v}}
    $$

    $$
    \leadsto \quad \vec{n} = \vec{u} \times \vec{v} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 0 & \frac{\partial f}{\partial x^1}(\vec{a}) \\ 0 & 1 & \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} \qquad \square
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, OCHRE, RED, arrow, math, mo, np):
    # graph(f) with its tangent plane at (a, f(a)), in an oblique drawing:
    # x^1 comes forward to the right, x^2 goes back to the right, y is vertical
    def _flat(x1, x2, y):
        x1, x2, y = (np.asarray(v, dtype=float) for v in (x1, x2, y))
        return 0.95 * x1 + 0.62 * x2, -0.22 * x1 + 0.42 * x2 + y

    def _pt(x1, x2, y):
        q = _flat(x1, x2, y)
        return float(q[0]), float(q[1])

    def _f(x1, x2):
        return 2.7 - 0.28 * ((x1 - 1.6) ** 2 + (x2 - 1.6) ** 2)

    _a = (1.0, 1.2)
    _d1, _d2 = -0.56 * (_a[0] - 1.6), -0.56 * (_a[1] - 1.6)
    _fa = float(_f(*_a))

    _fig = Figure(figsize=(7.0, 5.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_aspect("equal")
    _ax.axis("off")
    for _tip, _name, _off in (((3.4, 0, 0), "$x^1$", (6, -12)), ((0, 3.2, 0), "$x^2$", (6, 2)), ((0, 0, 3.6), "$y$", (6, -4))):
        arrow(_ax, (0, 0), _pt(*_tip), "black", lw=0.9)
        _ax.annotate(_name, _pt(*_tip), textcoords="offset points", xytext=_off, fontsize=14)
    # the point a in the (x^1, x^2)-plane, and the point of the graph above it
    _ax.plot(*_flat([_a[0], _a[0]], [0, _a[1]], [0, 0]), ":", color="#888888", lw=1)
    _ax.plot(*_flat([0, _a[0]], [_a[1], _a[1]], [0, 0]), ":", color="#888888", lw=1)
    _ax.plot(*_flat([_a[0], _a[0]], [_a[1], _a[1]], [0, _fa]), "--", color=BLUE, lw=1.1)
    _ax.plot(*_pt(_a[0], _a[1], 0), "o", color=BLUE, ms=4)
    _ax.annotate(r"$\vec{a}$", _pt(_a[0], _a[1], 0), textcoords="offset points", xytext=(6, -14), color=BLUE, fontsize=14)
    # the surface: filled outline plus coordinate curves
    _t = np.linspace(0, 1, 40)
    _lo, _hi = 0.4, 2.8
    _w = _lo + (_hi - _lo) * _t
    _edge1 = np.concatenate([_w, np.full(40, _hi), _w[::-1], np.full(40, _lo)])
    _edge2 = np.concatenate([np.full(40, _lo), _w, np.full(40, _hi), _w[::-1]])
    _ax.fill(*_flat(_edge1, _edge2, _f(_edge1, _edge2)), color=RED, alpha=0.13, lw=0)
    for _c in np.linspace(_lo, _hi, 7):
        _lw = 1.6 if _c in (_lo, _hi) else 0.5
        _ax.plot(*_flat(_w, np.full(40, _c), _f(_w, _c)), color=RED, lw=_lw)
        _ax.plot(*_flat(np.full(40, _c), _w, _f(_c, _w)), color=RED, lw=_lw)
    # the tangent plane, spanned by the velocity vectors (1, 0, d1) and (0, 1, d2)
    _k = 0.8
    _c1 = _a[0] + _k * np.array([-1, 1, 1, -1, -1])
    _c2 = _a[1] + _k * np.array([-1, -1, 1, 1, -1])
    _cy = _fa + _d1 * (_c1 - _a[0]) + _d2 * (_c2 - _a[1])
    _ax.fill(*_flat(_c1, _c2, _cy), color=GREEN, alpha=0.3, lw=0)
    _ax.plot(*_flat(_c1, _c2, _cy), color=GREEN, lw=1.4)
    _p = _pt(_a[0], _a[1], _fa)
    arrow(_ax, _p, _pt(_a[0] + _k, _a[1], _fa + _k * _d1), GREEN, lw=2.0)
    arrow(_ax, _p, _pt(_a[0], _a[1] + _k, _fa + _k * _d2), GREEN, lw=2.0)
    arrow(_ax, _p, _pt(_a[0] - 1.1 * _d1, _a[1] - 1.1 * _d2, _fa + 1.1), OCHRE, lw=2.0)
    _ax.annotate(r"$\vec{n}$", _pt(_a[0] - 1.1 * _d1, _a[1] - 1.1 * _d2, _fa + 1.1), textcoords="offset points", xytext=(6, 0), color=OCHRE, fontsize=16)
    _ax.plot(*_p, "o", color=BLUE, ms=5)
    _ax.annotate(r"$(a^1, a^2, f(\vec{a}))$", _p, textcoords="offset points", xytext=(-205, -4), color=BLUE, fontsize=13, arrowprops={"arrowstyle": "-", "color": BLUE, "lw": 0.7})
    _ax.annotate(r"$y = f(\vec{x})$", _pt(_hi, 2.0, _f(_hi, 2.0)), textcoords="offset points", xytext=(16, -22), color=RED, fontsize=14)
    _ax.annotate(r"tangent plane", _pt(_a[0] + _k, _a[1] + _k, _fa + _k * (_d1 + _d2)), textcoords="offset points", xytext=(30, 34), color=GREEN, fontsize=13, arrowprops={"arrowstyle": "-", "color": GREEN, "lw": 0.7})
    _ax.set_xlim(-2.0, 6.0)
    _ax.set_ylim(-1.0, 4.4)

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    $$
    y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \qquad \leadsto \qquad
    \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + (x^1 - a^1) \begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix} + (x^2 - a^2) \begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}, \quad \vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$

    Tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$

    $$
    \leadsto \quad \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} e^{a^2} \\ a^1 e^{a^2} \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}
    $$

    $$
    \leadsto \quad \vec{n} = \begin{bmatrix} -\dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] -\dfrac{\partial f}{\partial x^2}(\vec{a}) \\[8pt] 1 \end{bmatrix} = \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \leadsto \quad \text{plane through } \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} \text{ normal to } \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix}
    &= \left\{\, \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; -1 \cdot (y^1 - 1) - 1 \cdot (y^2 - 0) + 1 \cdot (y^3 - 1) = 0 \,\right\} \\
    &= \left\{\, \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; y^3 = y^1 + y^2 \,\right\} = \mathrm{graph}(g)
    \end{aligned}
    $$

    $$
    \leadsto \quad \text{affine approximation} \quad g(\vec{x}) = 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 \end{bmatrix} = 1 + (x^1 - 1) + x^2
    $$

    **Remark.**

    $$
    \vec{x} = \begin{bmatrix} 1.1 \\ -0.1 \end{bmatrix} \quad \Longrightarrow \quad
    \begin{aligned} f(\vec{x}) &= 1.1\, e^{-0.1} \approx 0.995 \\ g(\vec{x}) &= 1.1 - 0.1 = 1 \end{aligned}
    \quad \Longrightarrow \quad f(\vec{x}) - g(\vec{x}) \approx -0.005
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    px1 = mo.ui.slider(0, 2, 0.05, value=1.1, label="$x^1$", show_value=True)
    px2 = mo.ui.slider(-1, 1, 0.05, value=-0.1, label="$x^2$", show_value=True)
    return px1, px2


@app.cell(hide_code=True)
def _(math, mo, px1, px2):
    _f = px1.value * math.exp(px2.value)
    _g = px1.value + px2.value
    mo.vstack(
        [
            mo.hstack([px1, px2], justify="start", gap=3),
            mo.md(
                "| | |\n|:--|:--|\n"
                + rf"| $f(\vec{{x}})$ | ${_f:.4f}$ |" + "\n"
                + rf"| $g(\vec{{x}})$ | ${_g:.4f}$ |" + "\n"
                + rf"| $f(\vec{{x}}) - g(\vec{{x}})$ | ${_f - _g:.4f}$ |"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \right) = \begin{bmatrix} f^1(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}$ &nbsp; with each $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ a scalar function on $\mathbb{R}^n$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ \vdots \\ a^n \end{bmatrix}$ if each component $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{a}$

    $$
    \Longrightarrow \quad Df(\vec{a}) = \begin{bmatrix} Df^1(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix}
    = \begin{bmatrix} \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f^1}{\partial x^n}(\vec{a}) \\ \vdots & \ddots & \vdots \\ \dfrac{\partial f^m}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f^m}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(m \times n)
    $$

    defines an affine approximation of $f$ at $\vec{a}$ in the sense

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{\overbrace{f(\vec{x})}^{\mathbb{R}^m} - \overbrace{f(\vec{a})}^{\mathbb{R}^m} - \overbrace{Df(\vec{a})}^{\mathrm{Mat}(m \times n)} \overbrace{(\vec{x} - \vec{a})}^{\mathbb{R}^n}}{\lVert \vec{x} - \vec{a} \rVert} = \vec{0} \in \mathbb{R}^m
    $$

    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$, the linear transformation $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called the **derivative** of $f$ at $\vec{a}$ or the **Jacobian matrix** of $f$ at $\vec{a}$, $Df(\vec{a}) \in \mathrm{Mat}(m \times n)$.
    """
            ),
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$ if and only if

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$

    (scalar valued function on $\mathbb{R}^n$ &nbsp; $\leadsto$ &nbsp; we only need to compute 1 limit instead of $m$)
    """
            ),
            theorem(
                r"""
    If all components $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ of $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ have well-defined partial derivatives in an open ball centered at $\vec{a}$, and they are all continuous at $\vec{x} = \vec{a}$ ($f$ is $C^1$-smooth at $\vec{a}$), then $f$ is differentiable at $\vec{x} = \vec{a}$.
    """
            ),
            mo.md(
                r"""
    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \underbrace{\begin{bmatrix} a & b \\ c & d \end{bmatrix}}_{A \,\in\, \mathrm{Mat}(2 \times 2)} \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \end{bmatrix} = \begin{bmatrix} f^1(\vec{x}) \\ f^2(\vec{x}) \end{bmatrix}
    $$

    $f^1(\vec{x})$, $f^2(\vec{x})$ are $C^1$-smooth everywhere in $\mathbb{R}^2$ &nbsp; (linear combination of elementary functions)

    $\Longrightarrow$ &nbsp; $f$ is differentiable at any $\vec{a} \in \mathbb{R}^2$

    $$
    \Longrightarrow \quad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \dfrac{\partial f^1}{\partial x^2}(\vec{a}) \\[8pt] \dfrac{\partial f^2}{\partial x^1}(\vec{a}) & \dfrac{\partial f^2}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = A\,!
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 \cos(x^2) \\ x^1 \sin(x^2) \end{bmatrix}, \quad \vec{a} = \begin{bmatrix} 2 \\ \pi/3 \end{bmatrix}$

    $$
    \Longrightarrow \quad Df(\vec{a}) = \begin{bmatrix} \cos(a^2) & -a^1 \sin(a^2) \\ \sin(a^2) & a^1 \cos(a^2) \end{bmatrix} = \begin{bmatrix} \frac{\sqrt{1}}{2} & -\sqrt{3} \\[4pt] \frac{\sqrt{3}}{2} & \sqrt{1} \end{bmatrix}
    $$

    $$
    f(\vec{a}) = \begin{bmatrix} 2 \cos(\pi/3) \\ 2 \sin(\pi/3) \end{bmatrix} = \begin{bmatrix} \sqrt{1} \\ \sqrt{3} \end{bmatrix}, \qquad
    Df(\vec{a})(\vec{e}_1) = \begin{bmatrix} \frac{\sqrt{1}}{2} \\[4pt] \frac{\sqrt{3}}{2} \end{bmatrix}, \qquad
    Df(\vec{a})(\vec{e}_2) = \begin{bmatrix} -\sqrt{3} \\ \sqrt{1} \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pa1 = mo.ui.slider(0.5, 2.5, 0.25, value=2, label="$a^1$", show_value=True)
    pk = mo.ui.slider(0, 12, 1, value=4, label=r"$a^2$ (multiples of $\pi/12$)", show_value=True)
    return pa1, pk


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, arrow, cross_axes, math, mo, np, pa1, pk):
    _a1, _a2 = pa1.value, pk.value * math.pi / 12
    _c, _s = math.cos(_a2), math.sin(_a2)
    _fa = (_a1 * _c, _a1 * _s)

    _fig = Figure(figsize=(9.2, 4.2), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    cross_axes(_left, (-0.6, 4.6), (-0.6, 4.6), "$x^1$", "$x^2$")
    arrow(_left, (0, 0), (_a1, _a2), RED)
    _left.annotate(r"$\vec{a}$", (_a1 / 2, _a2 / 2), textcoords="offset points", xytext=(4, -16), color=RED, fontsize=15)
    arrow(_left, (_a1, _a2), (_a1 + 1, _a2), BLUE, r"$\vec{e}_1$", at_tip=True)
    arrow(_left, (_a1, _a2), (_a1, _a2 + 1), BLUE, r"$\vec{e}_2$", at_tip=True)
    _left.plot(_a1, _a2, "o", color=RED, ms=5)

    cross_axes(_right, (-4.6, 4.6), (-2.8, 4.4), "$y^1$", "$y^2$")
    _th = np.linspace(0, _a2, 50)
    _right.plot(0.6 * np.cos(_th), 0.6 * np.sin(_th), color=RED, lw=1.2)
    arrow(_right, (0, 0), _fa, GREEN)
    _right.annotate(r"$f(\vec{a})$", (_fa[0] / 2, _fa[1] / 2), textcoords="offset points", xytext=(6, -16), color=GREEN, fontsize=14)
    arrow(_right, _fa, (_fa[0] + _c, _fa[1] + _s), BLUE)
    arrow(_right, _fa, (_fa[0] - _a1 * _s, _fa[1] + _a1 * _c), BLUE)
    _right.annotate(r"$Df(\vec{a})(\vec{e}_1)$", (_fa[0] + _c, _fa[1] + _s), textcoords="offset points", xytext=(8, 2), color=BLUE, fontsize=13)
    _right.annotate(r"$Df(\vec{a})(\vec{e}_2)$", (_fa[0] - _a1 * _s, _fa[1] + _a1 * _c), textcoords="offset points", xytext=(-8, 6), color=BLUE, fontsize=13, ha="right")
    _right.plot(*_fa, "o", color=GREEN, ms=5)

    mo.vstack(
        [
            mo.hstack([pa1, pk], justify="start", gap=3),
            mo.md(
                "| | |\n|:--|:--|\n"
                + rf"| $\vec{{a}}$ | $\begin{{bmatrix}} {_a1:g} \\ {_a2:.2f} \end{{bmatrix}}$ |" + "\n"
                + rf"| $Df(\vec{{a}})$ | $\begin{{bmatrix}} {_c:.2f} & {-_a1 * _s:.2f} \\ {_s:.2f} & {_a1 * _c:.2f} \end{{bmatrix}}$ |"
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q1_d1, q1_d2, q1_est = _field(), _field(), _field()
    return q1_d1, q1_d2, q1_est


@app.cell(hide_code=True)
def _(check, mo, q1_d1, q1_d2, q1_est):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 x^2, \quad \vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$

    (a) Write the derivative and the gradient of $f$ at $\vec{a}$.
    """
            ),
            _ask(r"$\dfrac{\partial f}{\partial x^1}(\vec{a}) =$", q1_d1, 4),
            _ask(r"$\dfrac{\partial f}{\partial x^2}(\vec{a}) =$", q1_d2, 1),
            mo.md(
                r"""
    (b) Write the equation for the tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$.

    (c) Estimate $f\!\left( \begin{bmatrix} 1.1 \\ 1.9 \end{bmatrix} \right)$ and compare with the exact value.
    """
            ),
            _ask(r"estimate $=$", q1_est, 2.3),
            mo.md(
                r"""
    ### Question 2

    $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \\ (x^2)^2 \end{bmatrix}$

    (a) Compute the derivative of $f$ at $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix}$.

    (b) Write the affine approximation of $f$ at $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$.

    (c) Write the affine approximation of $f$ at $\vec{b} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$.

    (d) How do the images of these approximations differ?
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
