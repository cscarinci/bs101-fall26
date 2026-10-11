import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 09", css_file="bs101.css")


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
    header("Lecture 09", "Week 05", "Lecture 09")
    return


@app.cell(hide_code=True)
def _(Figure, GREEN, RED, arrow, mo, np):
    OCHRE = "#9a6b1f"

    def _gamma(t):
        return 0.9 + 2.9 * t, 1.7 + 1.0 * np.sin(3.3 * t) - 0.3 * t

    _fig = Figure(figsize=(8.4, 2.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1, 1.9])
    _left.set_xlim(-0.2, 3.2)
    _left.set_ylim(-1, 1)
    _left.axis("off")
    arrow(_left, (-0.1, 0), (3.1, 0), "black", lw=0.9)
    for _x, _name in ((1.0, "$a$"), (1.8, "$t$")):
        _left.plot(_x, 0, "o", color=RED, ms=5)
        _left.text(_x, -0.3, _name, color=RED, ha="center", fontsize=14)
    arrow(_left, (2.2, 0.55), (3.1, 0.55), "black", lw=1.2, connectionstyle="arc3,rad=-0.3")
    _left.text(2.6, 0.82, r"$\gamma$", fontsize=15)

    _right.set_xlim(-0.3, 7.2)
    _right.set_ylim(-0.3, 3.6)
    _right.set_aspect("equal")
    _right.axis("off")
    arrow(_right, (-0.3, 0), (7.0, 0), "black", lw=0.9)
    arrow(_right, (0, -0.3), (0, 3.5), "black", lw=0.9)
    _s = np.linspace(0, 1.9, 300)
    _right.plot(*_gamma(_s), color="black", lw=1.6)
    _a, _t, _h = 0.3, 0.72, 1e-4
    _pa, _pt = _gamma(_a), _gamma(_t)
    _va = ((_gamma(_a + _h)[0] - _pa[0]) / _h, (_gamma(_a + _h)[1] - _pa[1]) / _h)
    arrow(_right, _pa, _pt, GREEN, lw=1.4)
    arrow(_right, _pa, (_pa[0] + 0.45 * _va[0], _pa[1] + 0.45 * _va[1]), OCHRE, lw=1.6)
    _right.plot(*_pa, "o", color=RED, ms=5)
    _right.plot(*_pt, "o", color=RED, ms=5)
    _right.annotate(r"$\gamma(a)$", _pa, textcoords="offset points", xytext=(-38, 4), color=RED, fontsize=14)
    _right.annotate(r"$\gamma(t)$", _pt, textcoords="offset points", xytext=(8, -14), color=RED, fontsize=14)
    _right.annotate(r"$\gamma'(a)$", (_pa[0] + 0.45 * _va[0], _pa[1] + 0.45 * _va[1]), textcoords="offset points", xytext=(6, 2), color=OCHRE, fontsize=14)
    _right.text(5.6, 2.6, r"$\mathrm{Im}(\gamma)$", fontsize=13)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Limits of multivariable functions

    $$
    f : \mathbb{R}^n \longrightarrow \mathbb{R}^m, \quad \vec{a} \in \mathbb{R}^n, \quad \vec{b} \in \mathbb{R}^m
    $$

    $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$ &nbsp; if for every $B(\vec{b}, \varepsilon) \subset \mathbb{R}^m$ we can find $B(\vec{a}, \delta) \subset \mathbb{R}^n$ such that $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$

    We can make $f(\vec{x})$ as close as we want to $\vec{b}$ by taking $\vec{x}$ close enough, but different, to $\vec{a}$.

    **Today:** Differentiability and the derivative, for $n = 2$, $m = 1$ &nbsp; $\leadsto$ &nbsp; scalar functions on $\mathbb{R}^2$

    **Recall:** path in $\mathbb{R}^2$ &nbsp; ($n = 1$, $m = 2$)

    $$
    \gamma : \mathbb{R} \longrightarrow \mathbb{R}^2, \qquad \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix} \in \mathbb{R}^2 \qquad \leadsto \quad \text{position of } \gamma \text{ at time } t
    $$

    $$
    \gamma'(a) = \underbrace{\lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}}_{\text{displacement per unit of time}} = \begin{bmatrix} (\gamma^1)'(a) \\ (\gamma^2)'(a) \end{bmatrix} \qquad \leadsto \quad \text{velocity of } \gamma \text{ at time } t = a
    $$
    """
            ),
            _fig,
        ]
    )
    return (OCHRE,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How do we generalize to scalar functions on $\mathbb{R}^2$?

    Could try

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\vec{x} - \vec{a}}
    $$

    Makes NO sense! We cannot divide by $\vec{x} - \vec{a} \in \mathbb{R}^2$!

    Could try instead

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert}
    $$

    This makes sense! But if this limit exists (say equal $m \in \mathbb{R}$)

    $$
    \Longrightarrow \quad f(\vec{x}) \approx f(\vec{a}) + m \lVert \vec{x} - \vec{a} \rVert \quad \text{for } \vec{x} \approx \vec{a}
    $$

    Too restrictive!

    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 \quad \Longrightarrow \quad
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \ \text{ does not exist}
    $$

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a})}{\lVert \vec{x} - \vec{a} \rVert}
    = \lim_{\vec{x} \to \vec{a}} \frac{x^1 - a^1}{\lVert \vec{x} - \vec{a} \rVert}
    \quad \text{depends on how } \vec{x} \text{ approaches } \vec{a}\,!
    \qquad \begin{cases} = 1 & \text{along } \vec{x} = \vec{a} + t\vec{e}_1,\ t \to 0^+ \\ = 0 & \text{along } \vec{x} = \vec{a} + s\vec{e}_2 \end{cases}
    $$

    We should hope to give a definition of derivatives for which this simple function is differentiable!
    """)
    return


@app.cell(hide_code=True)
def _(Figure, GREEN, OCHRE, RED, arrow, definition, mo):
    _fig = Figure(figsize=(8.0, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.6, 1])
    _left.set_xlim(-0.4, 4.6)
    _left.set_ylim(-0.4, 3.2)
    _left.set_aspect("equal")
    _left.axis("off")
    arrow(_left, (-0.4, 0), (4.4, 0), "black", lw=0.9)
    arrow(_left, (0, -0.4), (0, 3.0), "black", lw=0.9)
    _left.text(4.3, -0.35, "$x^1$", fontsize=13)
    _left.text(-0.4, 2.85, "$x^2$", fontsize=13)
    _a = (1.6, 0.9)
    arrow(_left, (0.8, _a[1]), (3.9, _a[1]), GREEN, lw=1.3)
    arrow(_left, (_a[0], 0.2), (_a[0], 2.9), OCHRE, lw=1.3)
    _left.text(3.95, _a[1] + 0.1, "$t$", color=GREEN, fontsize=13)
    _left.text(_a[0] + 0.12, 2.8, "$s$", color=OCHRE, fontsize=13)
    for _pt, _name, _off in ((_a, r"$\vec{a}$", (6, -18)), ((2.9, _a[1]), r"$\vec{a} + t\vec{e}_1$", (-14, -20)), ((_a[0], 2.2), r"$\vec{a} + s\vec{e}_2$", (10, -6))):
        _left.plot(*_pt, "o", color=RED, ms=5)
        _left.annotate(_name, _pt, textcoords="offset points", xytext=_off, color=RED, fontsize=13)
    arrow(_left, (3.4, 2.3), (4.4, 2.3), "black", lw=1.2, connectionstyle="arc3,rad=-0.3")
    _left.text(3.85, 2.7, "$f$", fontsize=15)

    _right.set_xlim(-0.5, 2.6)
    _right.set_ylim(-0.4, 3.2)
    _right.axis("off")
    arrow(_right, (0, -0.4), (0, 3.1), "black", lw=0.9)
    for _y, _name in ((2.2, r"$f(\vec{a} + t\vec{e}_1)$"), (1.3, r"$f(\vec{a})$"), (0.5, r"$f(\vec{a} + s\vec{e}_2)$")):
        _right.plot(0, _y, "o", color=RED, ms=5)
        _right.text(0.2, _y, _name, color=RED, fontsize=13, va="center")

    mo.vstack(
        [
            definition(
                r"""
    Given a function $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, the **partial derivative** of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ is

    $$
    \frac{\partial f}{\partial x^1}(\vec{a}) = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{e}_1) - f(\vec{a})}{t}
    $$

    provided that the limit exists.

    $$
    \leadsto \quad \frac{\partial f}{\partial x^1}(\vec{a}) = \frac{d}{dt} f(\vec{a} + t\vec{e}_1) \Big|_{t = 0}
    $$

    (real single variable differentiation at $t = 0$; &nbsp; $t \longmapsto f(\vec{a} + t\vec{e}_1)$ is a real single variable real valued function!)

    Similarly, the partial derivative of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ is

    $$
    \frac{\partial f}{\partial x^2}(\vec{a}) = \lim_{s \to 0} \frac{f(\vec{a} + s\vec{e}_2) - f(\vec{a})}{s}
    $$

    provided that the limit exists.

    $$
    \leadsto \quad \frac{\partial f}{\partial x^2}(\vec{a}) = \frac{d}{ds} f(\vec{a} + s\vec{e}_2) \Big|_{s = 0}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \sin(x^1)$

    $$
    \begin{aligned}
    \Longrightarrow \quad \frac{\partial}{\partial x^1} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{t \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + t \\ a^2 + 0 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{t} \\[4pt]
    &= \lim_{t \to 0} \frac{\sin(a^1 + t) - \sin(a^1)}{t} \\[4pt]
    &= \frac{d}{dt} \sin(a^1 + t) \Big|_{t = 0} = \cos(a^1)
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \frac{\partial}{\partial x^2} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{s \to 0} \frac{f\!\left( \begin{bmatrix} a^1 + 0 \\ a^2 + s \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)}{s} \\[4pt]
    &= \lim_{s \to 0} \frac{\sin(a^1) - \sin(a^1)}{s} = 0
    \end{aligned}
    $$

    $$
    f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) = (a^1)^2 (a^2)^3
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad \frac{\partial}{\partial x^1} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{t \to 0} \frac{(a^1 + t)^2 (a^2)^3 - (a^1)^2 (a^2)^3}{t} \\[4pt]
    &= \lim_{t \to 0} \frac{(a^1 + t)^2 - (a^1)^2}{t}\, (a^2)^3 \\[4pt]
    &= \frac{d}{dt} (a^1 + t)^2 \Big|_{t = 0} \cdot (a^2)^3 = 2 (a^1) \cdot (a^2)^3
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \frac{\partial}{\partial x^2} f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right)
    &= \lim_{s \to 0} \frac{(a^1)^2 (a^2 + s)^3 - (a^1)^2 (a^2)^3}{s} \\[4pt]
    &= (a^1)^2 \cdot \frac{d}{ds} (a^2 + s)^3 \Big|_{s = 0} = 3 (a^1)^2 (a^2)^2
    \end{aligned}
    $$

    The partial derivative in the direction of $\vec{e}_i$ is the usual single variable derivative with respect to $x^i$, assuming $x^j$ is held constant ($j \neq i$).

    The existence of partial derivatives will be necessary for the notion of differentiability but will not be sufficient &nbsp; $\leadsto$ &nbsp; $f$ could behave badly in other directions!
    """
            ),
            definition(
                r"""
    Given $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, the **directional derivative** of $f$ at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ in the direction of $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix}$ is

    $$
    \begin{aligned}
    Df(\vec{a})(\vec{v}) &= \lim_{t \to 0} \frac{f(\vec{a} + t\vec{v}) - f(\vec{a})}{t} \\
    &= \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t = 0}
    \end{aligned}
    $$

    provided the derivative exists.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    angle = mo.ui.slider(0, 355, 5, value=30, label=r"direction of $\vec{v}$ (degrees)", show_value=True)
    return (angle,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, angle, arrow, math, mo, np):
    _th = math.radians(angle.value)
    _v = (math.cos(_th), math.sin(_th))
    _a = (1.0, 1.0)

    def _f(x1, x2):
        return x1**2 * x2**3

    _D = 2 * _a[0] * _a[1] ** 3 * _v[0] + 3 * _a[0] ** 2 * _a[1] ** 2 * _v[1]

    _fig = Figure(figsize=(8.8, 4.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    _g = np.linspace(-0.4, 2.4, 200)
    _X, _Y = np.meshgrid(_g, _g)
    _left.contour(_X, _Y, _f(_X, _Y), levels=[-1, -0.3, 0.1, 0.5, 1, 2, 4, 8, 16], colors="#888888", linewidths=0.8, linestyles="solid")
    _left.plot([_a[0] - 1.3 * _v[0], _a[0] + 1.3 * _v[0]], [_a[1] - 1.3 * _v[1], _a[1] + 1.3 * _v[1]], color=GREEN, lw=1.2)
    arrow(_left, _a, (_a[0] + _v[0], _a[1] + _v[1]), GREEN, r"$\vec{v}$", at_tip=True)
    _left.plot(*_a, "o", color=RED, ms=6)
    _left.annotate(r"$\vec{a}$", _a, textcoords="offset points", xytext=(-16, -16), color=RED, fontsize=15)
    _left.set_xlim(-0.4, 2.4)
    _left.set_ylim(-0.4, 2.4)
    _left.set_aspect("equal")
    _left.set_xlabel("$x^1$")
    _left.set_ylabel("$x^2$", rotation=0)
    _left.set_title("level sets of $f$", fontsize=13)

    _t = np.linspace(-1, 1, 200)
    _right.plot(_t, _f(_a[0] + _t * _v[0], _a[1] + _t * _v[1]), color=GREEN, lw=2)
    _right.plot(_t, 1 + _D * _t, color=BLUE, lw=1.3)
    _right.plot(0, 1, "o", color=RED, ms=6)
    _right.axhline(0, color="black", lw=0.8)
    _right.axvline(0, color="black", lw=0.8)
    _right.set_xlim(-1, 1)
    _right.set_ylim(-3, 8)
    _right.set_xlabel("$t$")
    _right.set_title(r"$t \mapsto f(\vec{a} + t\vec{v})$", fontsize=13)

    mo.vstack(
        [
            mo.md(r"For $f(\vec{x}) = (x^1)^2 (x^2)^3$ at $\vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$:"),
            mo.hstack(
                [
                    angle,
                    mo.md(
                        rf"$\vec{{v}} = \begin{{bmatrix}} {_v[0]:.2f} \\ {_v[1]:.2f} \end{{bmatrix}}, \qquad Df(\vec{{a}})(\vec{{v}}) = {_D:.2f}$"
                    ),
                ],
                justify="start",
                gap=3,
                align="center",
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
    To call a function $f$ differentiable at $\vec{x} = \vec{a}$ we want also that all directional derivatives for all $\vec{v} \in \mathbb{R}^2$ be well-defined and that

    $$
    Df(\vec{a})(\vec{v}) = \underbrace{v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})}_{\text{linear combination of partial derivatives}}
    $$

    **Remark.** &nbsp; $\dfrac{\partial f}{\partial x^i}(\vec{a}) = Df(\vec{a})(\vec{e}_i)$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$ if the directional derivative

    $$
    Df(\vec{a})(\vec{v})
    $$

    exists for every $\vec{v} = v^1 \vec{e}_1 + v^2 \vec{e}_2 = \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \in \mathbb{R}^2$, satisfies

    $$
    \begin{aligned}
    Df(\vec{a})(\vec{v}) &= Df(\vec{a})(v^1 \vec{e}_1 + v^2 \vec{e}_2) \\
    &= v^1\, Df(\vec{a})(\vec{e}_1) + v^2\, Df(\vec{a})(\vec{e}_2) && (\text{linearity in } \vec{v}) \\
    &= v^1 \frac{\partial f}{\partial x^1}(\vec{a}) + v^2 \frac{\partial f}{\partial x^2}(\vec{a})
    \end{aligned}
    $$

    and

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$
    """
            ),
            mo.md(
                r"""
    Now NOT a limit over real numbers! (Stronger than just existence + linearity of directional derivatives!)

    $$
    \Longrightarrow \quad f(\vec{x}) \approx f(\vec{a}) + \underbrace{Df(\vec{a})(\vec{x} - \vec{a})}_{\text{more flexible than } m \lVert \vec{x} - \vec{a} \rVert} \quad \text{for } \vec{x} \approx \vec{a}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$

    $$
    \begin{aligned}
    \Longrightarrow \quad Df(\vec{a})(\vec{v}) &= \frac{d}{dt} f(\vec{a} + t\vec{v}) \Big|_{t = 0} \\
    &= \frac{d}{dt} (a^1 + t v^1) \Big|_{t = 0} = v^1 \\
    &= v^1 \underbrace{\frac{\partial f}{\partial x^1}(\vec{a})}_{= 1} + v^2 \underbrace{\frac{\partial f}{\partial x^2}(\vec{a})}_{= 0} \qquad \forall\, \vec{v}
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 & 0 \end{bmatrix} : \mathbb{R}^2 \longrightarrow \mathbb{R}, \qquad \begin{bmatrix} v^1 \\ v^2 \end{bmatrix} \longmapsto v^1 \qquad (\text{linear in } \vec{v})
    $$

    For the final limit:

    $$
    \frac{f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) - f\!\left( \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \right) - Df(\vec{a})\!\left( \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \end{bmatrix} \right)}{\lVert \vec{x} - \vec{a} \rVert}
    = \frac{x^1 - a^1 - (x^1 - a^1)}{\lVert \vec{x} - \vec{a} \rVert} = 0 \qquad \forall\, \vec{x} \in \mathbb{R}^2 \setminus \{\vec{a}\}
    $$

    $$
    \Longrightarrow \quad \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
    $$

    $\Longrightarrow$ &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1$ is differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix} \in \mathbb{R}^2$!
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
