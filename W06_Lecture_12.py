import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 12 · The chain rule", css_file="bs101.css")


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
    header("Lecture 12", "Week 06", "Lecture 12 · The chain rule")
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## So far

    - $f : \mathbb{R} \longrightarrow \mathbb{R}$ (single variable, scalar valued) is differentiable at $x = a$ if

        $$
        f'(a) = \lim_{x \to a} \frac{f(x) - f(a)}{x - a} \in \mathbb{R} \quad \text{is well-defined}
        $$

        (slope of tangent line to $\mathrm{graph}(f)$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$)

    - $f : \mathbb{R} \longrightarrow \mathbb{R}^m$ (single variable, vector valued: path) &nbsp; $\leadsto$ &nbsp; $f(x) = \begin{bmatrix} f^1(x) \\ f^2(x) \\ \vdots \\ f^m(x) \end{bmatrix}$, &nbsp; $f^i : \mathbb{R} \longrightarrow \mathbb{R}$

        is differentiable at $x = a$ if each component $f^i : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $x = a$ (as a single variable scalar function)

        $$
        \Longleftrightarrow \quad \lim_{x \to a} \frac{f(x) - f(a)}{x - a} = f'(a) = \begin{bmatrix} (f^1)'(a) \\ (f^2)'(a) \\ \vdots \\ (f^m)'(a) \end{bmatrix} \in \mathbb{R}^m
        $$

        derivative of $f$ at $x = a$ (velocity vector of $f$ at $x = a$)

    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ (multivariable, scalar valued) is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \\ \vdots \\ a^n \end{bmatrix}$ if

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

        where $Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)$

        derivative of $f$ at $\vec{x} = \vec{a}$ (Jacobian matrix of $f$ at $\vec{x} = \vec{a}$)

    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ (multivariable, vector valued) &nbsp; $\leadsto$ &nbsp; $f(\vec{x}) = \begin{bmatrix} f^1(\vec{x}) \\ f^2(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}$, &nbsp; $f^i : \mathbb{R}^n \longrightarrow \mathbb{R}$

        is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \\ \vdots \\ a^n \end{bmatrix}$ if each component $f^i : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a}$ (as a multivariable scalar valued function)

        $$
        \Longleftrightarrow \quad \lim_{\vec{x} \to \vec{a}} \frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

        where

        $$
        Df(\vec{a}) = \begin{bmatrix} Df^1(\vec{a}) \\ Df^2(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix}
        = \begin{bmatrix}
        \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \dfrac{\partial f^1}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f^1}{\partial x^n}(\vec{a}) \\[10pt]
        \dfrac{\partial f^2}{\partial x^1}(\vec{a}) & \dfrac{\partial f^2}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f^2}{\partial x^n}(\vec{a}) \\
        \vdots & \vdots & \ddots & \vdots \\
        \dfrac{\partial f^m}{\partial x^1}(\vec{a}) & \dfrac{\partial f^m}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f^m}{\partial x^n}(\vec{a})
        \end{bmatrix} \in \mathrm{Mat}(m \times n)
        $$

        derivative of $f$ at $\vec{a}$ (Jacobian matrix of $f$ at $\vec{a}$)

        $\Longleftrightarrow$ &nbsp; $g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$ is a good affine approximation to $f(\vec{x})$ near $\vec{a}$
    """
            ),
            theorem(
                r"""
    If all partial derivatives $\dfrac{\partial f^i}{\partial x^j}(\vec{x})$ are well-defined on an open ball around $\vec{a}$ and they are all continuous at $\vec{x} = \vec{a}$, then $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{x} = \vec{a}$!
    """
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
    **Today:** More properties

    **Recall:** $f, g : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $f$ differentiable at $a$, &nbsp; $g$ differentiable at $b = f(a)$

    $\Longrightarrow$ &nbsp; $g \circ f : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $a$ with

    $$
    (g \circ f)'(a) = g'(f(a)) \cdot f'(a) \qquad \text{chain rule}
    $$

    We want to generalize this to vector valued multivariable functions $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$

    Start with $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ (path) and $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ (scalar valued function)
    """
            ),
            theorem(
                r"""
    If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ is differentiable at $t = t_0$ and $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \gamma(t_0)$, then $g = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $t = t_0$ with

    $$
    g'(t_0) = (f \circ \gamma)'(t_0) = \underbrace{Df(\gamma(t_0))}_{\mathbb{R}^n \to \mathbb{R}}\, \underbrace{(\gamma'(t_0))}_{\mathbb{R}^n}
    $$
    """
            ),
            mo.md(
                r"""
    **Proof.** (with $\vec{x} = \gamma(t)$ and $\vec{a} = \gamma(t_0)$)

    $$
    \begin{aligned}
    \frac{g(t) - g(t_0)}{t - t_0} &= \frac{f(\gamma(t)) - f(\gamma(t_0))}{t - t_0} \\[6pt]
    &= \frac{f(\gamma(t)) - f(\gamma(t_0))}{\lVert \gamma(t) - \gamma(t_0) \rVert} \cdot \frac{\lVert \gamma(t) - \gamma(t_0) \rVert}{t - t_0} \\[6pt]
    &= \underbrace{\frac{f(\gamma(t)) - f(\gamma(t_0)) - Df(\gamma(t_0))(\gamma(t) - \gamma(t_0))}{\lVert \gamma(t) - \gamma(t_0) \rVert}}_{\to\, 0}
    \; \underbrace{\frac{\lVert \gamma(t) - \gamma(t_0) \rVert}{t - t_0}}_{\to\, \pm \lVert \gamma'(t_0) \rVert}
    + \underbrace{Df(\gamma(t_0))}_{\text{constant matrix}} \underbrace{\left( \frac{\gamma(t) - \gamma(t_0)}{t - t_0} \right)}_{\to\, \gamma'(t_0)}
    \end{aligned}
    $$

    (first factor $\to 0$ since $\gamma$ is continuous at $t_0$ and $f$ is differentiable at $\vec{a} = \gamma(t_0)$; where $\gamma(t) = \gamma(t_0)$ this factor is set to $0$, and the identity still holds)

    (second factor $\to \pm \lVert \gamma'(t_0) \rVert$ according to the sign of $t - t_0$; in particular it stays bounded, it does not go to $+\infty$!)

    $$
    \begin{aligned}
    \Longrightarrow \quad \lim_{t \to t_0} \frac{g(t) - g(t_0)}{t - t_0} &= 0 + Df(\gamma(t_0))(\gamma'(t_0))
    = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\gamma(t_0)) & \cdots & \dfrac{\partial f}{\partial x^n}(\gamma(t_0)) \end{bmatrix} \begin{bmatrix} (\gamma^1)'(t_0) \\ \vdots \\ (\gamma^n)'(t_0) \end{bmatrix} \\[4pt]
    &= \frac{\partial f}{\partial x^1}(\gamma(t_0))\, (\gamma^1)'(t_0) + \dots + \frac{\partial f}{\partial x^n}(\gamma(t_0))\, (\gamma^n)'(t_0)
    \end{aligned}
    $$

    $\therefore$ &nbsp; $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ differentiable at $t = t_0$, &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a} = \gamma(t_0)$

    then $g = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$ differentiable at $t = t_0$ with

    $$
    g'(t_0) = (f \circ \gamma)'(t_0) = \sum_{i=1}^{n} \frac{\partial f}{\partial x^i}(\gamma(t_0))\, (\gamma^i)'(t_0)
    $$

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} t^2 \\ t^3 \end{bmatrix}, \qquad f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 x^2$

    $$
    \gamma'(t_0) = \begin{bmatrix} 2 t_0 \\ 3 t_0^2 \end{bmatrix}, \qquad
    Df(\vec{a}) = \begin{bmatrix} a^2 & a^1 \end{bmatrix} \quad \leadsto \quad Df(\gamma(t_0)) = \begin{bmatrix} t_0^3 & t_0^2 \end{bmatrix} \quad (\vec{a} = \gamma(t_0))
    $$

    $$
    \Longrightarrow \quad g(t) = f \circ \gamma(t) = f\!\left( \begin{bmatrix} t^2 \\ t^3 \end{bmatrix} \right) = t^2 \cdot t^3 = t^5
    $$

    also differentiable at $t = t_0$ with

    $$
    g'(t_0) = Df(\gamma(t_0))(\gamma'(t_0)) = \begin{bmatrix} t_0^3 & t_0^2 \end{bmatrix} \begin{bmatrix} 2 t_0 \\ 3 t_0^2 \end{bmatrix} = 2 t_0^4 + 3 t_0^4 = 5 t_0^4
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t0 = mo.ui.slider(-1.5, 1.5, 0.1, value=1.0, label="$t_0$", show_value=True)
    return (t0,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, RED, arrow, mo, np, t0):
    _t = t0.value
    _p = (_t**2, _t**3)
    _v = (2 * _t, 3 * _t**2)
    _grad = (_t**3, _t**2)
    _dot = _grad[0] * _v[0] + _grad[1] * _v[1]

    _fig = Figure(figsize=(6.4, 5.4), layout="constrained")
    _ax = _fig.add_subplot()
    _X, _Y = np.meshgrid(np.linspace(-2.5, 4.5, 300), np.linspace(-3.5, 5.5, 300))
    _ax.contour(_X, _Y, _X * _Y, levels=[-8, -4, -2, -1, -0.5, 0.5, 1, 2, 4, 8], colors=GREY, linewidths=0.7, linestyles="solid")
    if abs(_t) > 0.05:
        _ax.contour(_X, _Y, _X * _Y, levels=[_t**5], colors=GREEN, linewidths=1.6, linestyles="solid")
    _s = np.linspace(-1.5, 1.5, 300)
    _ax.plot(_s**2, _s**3, color=RED, lw=2, label=r"$\gamma$")
    _ax.plot([], [], color=GREY, lw=0.7, label="level sets of $f$")
    _ax.plot([], [], color=GREEN, lw=1.6, label=r"$f^{-1}(f(\gamma(t_0)))$")
    arrow(_ax, _p, (_p[0] + _v[0], _p[1] + _v[1]), RED, r"$\gamma'(t_0)$", at_tip=True)
    arrow(_ax, _p, (_p[0] + _grad[0], _p[1] + _grad[1]), BLUE, r"$\vec{\nabla} f(\gamma(t_0))$", at_tip=True)
    _ax.plot(*_p, "o", color=RED, ms=6)
    _ax.annotate(r"$\gamma(t_0)$", _p, textcoords="offset points", xytext=(-8, -4), ha="right", va="top", color=RED, fontsize=16)
    _ax.set_xlim(-2.5, 4.5)
    _ax.set_ylim(-3.5, 5.5)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.set_xlabel("$x^1$")
    _ax.set_ylabel("$x^2$")
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)
    _ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False, fontsize=12)

    mo.vstack(
        [
            mo.hstack([t0], justify="start", gap=3),
            mo.md(
                "| | |\n|:--|:--|\n"
                + rf"| $\gamma(t_0)$ | $\begin{{bmatrix}} {_p[0]:.3f} \\ {_p[1]:.3f} \end{{bmatrix}}$ |" + "\n"
                + rf"| $\gamma'(t_0)$ | $\begin{{bmatrix}} {_v[0]:.3f} \\ {_v[1]:.3f} \end{{bmatrix}}$ |" + "\n"
                + rf"| $Df(\gamma(t_0))$ | $\begin{{bmatrix}} {_grad[0]:.3f} & {_grad[1]:.3f} \end{{bmatrix}}$ |" + "\n"
                + rf"| $Df(\gamma(t_0))(\gamma'(t_0))$ | ${_dot:.3f}$ |" + "\n"
                + rf"| $5 t_0^4$ | ${5 * _t**4:.3f}$ |"
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
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix}, \qquad f\!\left( \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \right) = (x^2)^2 + (x^3)^2$

    $$
    \Longrightarrow \quad f \circ \gamma(t) = 1 \quad \Longrightarrow \quad (f \circ \gamma)'(t) = 0
    $$

    $$
    \gamma'(t) = \begin{bmatrix} 1 \\ -\sin(t) \\ \cos(t) \end{bmatrix}, \qquad Df(\vec{a}) = \begin{bmatrix} 0 & 2 a^2 & 2 a^3 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad Df(\gamma(t))(\gamma'(t)) &= \begin{bmatrix} 0 & 2 \cos(t) & 2 \sin(t) \end{bmatrix} \begin{bmatrix} 1 \\ -\sin(t) \\ \cos(t) \end{bmatrix} \\
    &= 0 \cdot 1 + 2 \cos(t)(-\sin(t)) + 2 \sin(t) \cos(t) = 0
    \end{aligned}
    $$

    **Corollary.** For $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, $\vec{\nabla} f(\vec{a})$ is perpendicular to the level set through $\vec{a}$.

    Suppose $f(\vec{a}) = b$ and suppose $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ is differentiable at $t_0$ with $\gamma(t_0) = \vec{a}$ and $\mathrm{Im}(\gamma) \subset f^{-1}(b)$ &nbsp; (that is, $f \circ \gamma(t) = b \ \ \forall\, t$)

    $$
    \begin{aligned}
    \Longrightarrow \quad \vec{\nabla} f(\vec{a}) \cdot \gamma'(t_0) &= Df(\vec{a})(\gamma'(t_0)) \\
    &= (f \circ \gamma)'(t_0) = 0
    \end{aligned}
    $$
    """
            ),
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ differentiable at $\vec{x} = \vec{a}$, &nbsp; $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$ differentiable at $\vec{y} = \vec{b} = f(\vec{a})$

    $\Longrightarrow$ &nbsp; $g \circ f : \mathbb{R}^n \longrightarrow \mathbb{R}^p$ differentiable at $\vec{x} = \vec{a}$ with

    $$
    \underbrace{D(g \circ f)(\vec{a})}_{\mathrm{Mat}(p \times n)} = \underbrace{Dg(f(\vec{a}))}_{\mathrm{Mat}(p \times m)}\, \underbrace{Df(\vec{a})}_{\mathrm{Mat}(m \times n)} \qquad (\text{matrix multiplication!})
    $$
    """
            ),
            mo.md(
                r"""
    **Proof.** Similar idea as the previous theorem

    $$
    \begin{aligned}
    &\frac{g \circ f(\vec{x}) - g \circ f(\vec{a}) - Dg(f(\vec{a}))\, Df(\vec{a})\, (\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \\[6pt]
    &\quad = \underbrace{\frac{g \circ f(\vec{x}) - g \circ f(\vec{a}) - Dg(f(\vec{a}))\big( f(\vec{x}) - f(\vec{a}) \big)}{\lVert f(\vec{x}) - f(\vec{a}) \rVert}}_{\to\, 0}
    \; \underbrace{\frac{\lVert f(\vec{x}) - f(\vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert}}_{\text{does not go to } +\infty} \\[6pt]
    &\qquad + Dg(f(\vec{a})) \underbrace{\left( \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \right)}_{\to\, 0}
    \end{aligned}
    $$

    (“does not go to $+\infty$”: this needs some care… not here! In short: $f$ differentiable at $\vec{a}$ gives $\lVert f(\vec{x}) - f(\vec{a}) \rVert \leq C \lVert \vec{x} - \vec{a} \rVert$ for $\vec{x}$ near $\vec{a}$, so the factor is bounded; where $f(\vec{x}) = f(\vec{a})$ the first quotient is set to $0$.)

    $\Longrightarrow$ &nbsp; $D(g \circ f)(\vec{a}) = Dg(f(\vec{a}))\, Df(\vec{a})$ defines a good affine approximation to $g \circ f$ at $\vec{a}$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \end{bmatrix}, \qquad g\!\left( \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \right) = (y^1)^2 - y^2$

    $$
    \Longrightarrow \quad g \circ f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = g\!\left( \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \end{bmatrix} \right) = (x^1 x^2)^2 - (x^1 + x^2)
    $$

    $$
    Df(\vec{x}) = \begin{bmatrix} x^2 & x^1 \\ 1 & 1 \end{bmatrix}, \qquad Dg(\vec{y}) = \begin{bmatrix} 2 y^1 & -1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad Dg(f(\vec{x}))\, Df(\vec{x}) = \begin{bmatrix} 2 x^1 x^2 & -1 \end{bmatrix} \begin{bmatrix} x^2 & x^1 \\ 1 & 1 \end{bmatrix}
    = \begin{bmatrix} 2 x^1 (x^2)^2 - 1 & 2 (x^1)^2 x^2 - 1 \end{bmatrix}
    \end{aligned}
    $$

    $$
    D(g \circ f)(\vec{x}) = \begin{bmatrix} 2 (x^1 x^2) x^2 - 1 & 2 (x^1 x^2) x^1 - 1 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    Consider $\gamma(t) = \begin{bmatrix} 3 \cos(t) \\ 2 \sin(t) \end{bmatrix}$, &nbsp; $\sigma(t) = t\, \gamma(t) = \begin{bmatrix} 3t \cos(t) \\ 2t \sin(t) \end{bmatrix}$,

    $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \dfrac{(x^1)^2}{9} + \dfrac{(x^2)^2}{4}$ &nbsp; and &nbsp; $g\!\left( \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \right) = \begin{bmatrix} y^1 \cos(y^2) \\ y^1 \sin(y^2) \end{bmatrix}$

    (a) Compute $\gamma'(t)$, $\sigma'(t)$, $\vec{\nabla} f(\vec{x})$ and $Dg(\vec{y})$.

    (b) Compute $(f \circ \gamma)'(t)$, $(f \circ \sigma)'(t)$ and $D(f \circ g)(\vec{y})$

    &nbsp;&nbsp;&nbsp; (i) via the chain rule

    &nbsp;&nbsp;&nbsp; (ii) directly as maps $f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$, $f \circ \sigma : \mathbb{R} \longrightarrow \mathbb{R}$, $f \circ g : \mathbb{R}^2 \longrightarrow \mathbb{R}$
    """)
    return


if __name__ == "__main__":
    app.run()
