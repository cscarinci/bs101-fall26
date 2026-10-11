import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 07 · Local properties of paths", css_file="bs101.css")


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
def _(mo, np):
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

    def path_projection(t, y1, y2):
        """Common oblique view: t rightwards, y^1 down-left, y^2 upwards."""
        t, y1, y2 = (np.asarray(c, dtype=float) for c in (t, y1, y2))
        return 0.36 * t - 0.6 * y1, y2 - 0.4 * y1 - 0.07 * t

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

    return BLUE, GREEN, GREY, OCHRE, RED, arrow, check, definition, header, path_projection, plane, theorem, warning


@app.cell(hide_code=True)
def _(header):
    header("Lecture 07", "Week 04", "Lecture 07 · Local properties of paths")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Multivariable functions $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; global properties (image, graph, level sets)

    **Today:** Local properties of paths $\gamma : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}^m$ (MT 2.4) — how a function behaves at a point (limits, continuity, differentiability)
    """
            ),
            definition(
                r"""
    A **path** in $\mathbb{R}^m$ is a function

    $$
    \begin{aligned}
    \gamma : A \subseteq \mathbb{R} &\longrightarrow \mathbb{R}^m \\
    t &\longmapsto \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix}
    \end{aligned}
    $$
    """
            ),
            mo.md(
                r"""
    **Remark.** Each component $\gamma^i : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}$ is a usual single variable real valued function!

    $\Longrightarrow$ &nbsp; paths are ordered lists of single variable scalar functions, like vectors were ordered lists of scalars!

    **Example.** $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ an affine parameterization of a line

    $$
    \gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
    $$

    $$
    \gamma^1(t) = x^1 + t v^1, \qquad \gamma^2(t) = x^2 + t v^2
    $$

    A pair of affine single variable functions.

    **Example.**

    $$
    \begin{aligned}
    \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^2 \\
    t &\longmapsto \gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
    \end{aligned}
    $$

    - $\gamma^1 : \mathbb{R} \longrightarrow \mathbb{R}$, $t \longmapsto \cos(t)$ is the cosine function
    - $\gamma^2 : \mathbb{R} \longrightarrow \mathbb{R}$, $t \longmapsto \sin(t)$ is the sine function

    $$
    \mathrm{Im}(\gamma) = \left\{\, \gamma(t) \;\middle|\; t \in \mathbb{R} \,\right\} = \left\{\, \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} \;\middle|\; t \in \mathbb{R} \,\right\}
    $$

    This is the unit circle $(y^1)^2 + (y^2)^2 = 1$.

    $$
    \mathrm{graph}(\gamma) = \left\{\, (t,\gamma(t)) \;\middle|\; t \in \mathbb{R} \,\right\} = \left\{\, \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix} \;\middle|\; t \in \mathbb{R} \,\right\}
    $$

    This is a helix in $\mathbb{R} \times \mathbb{R}^2 = \mathbb{R}^3$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_circle = mo.ui.slider(0, 12.5, 0.1, value=0.7, label="$t$", show_value=True)
    return (t_circle,)


@app.cell(hide_code=True)
def _(Arc, BLUE, Figure, GREY, OCHRE, arrow, math, mo, np, path_projection, t_circle):
    _t = t_circle.value
    _fig = Figure(figsize=(4.4, 3.8), layout="constrained")
    _left = _fig.subplots()

    # Im(gamma): the unit circle
    _left.set_xlim(-1.5, 1.9)
    _left.set_ylim(-1.5, 1.8)
    _left.set_aspect("equal")
    _left.axis("off")
    arrow(_left, (-1.5, 0), (1.8, 0), "black", lw=0.9)
    arrow(_left, (0, -1.5), (0, 1.6), "black", lw=0.9)
    _left.text(1.65, -0.28, "$y^1$")
    _left.text(-0.35, 1.5, "$y^2$")
    _th = np.linspace(0, 2 * np.pi, 361)
    _left.plot(np.cos(_th), np.sin(_th), color=OCHRE, lw=1.5)
    _p = (math.cos(_t), math.sin(_t))
    arrow(_left, (0, 0), _p, BLUE)
    _left.plot(*_p, "o", color=BLUE, ms=4.5)
    _left.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=math.degrees(_t % (2 * math.pi)), color=BLUE, lw=1))
    _left.set_title(r"$\mathrm{Im}(\gamma)$", color=OCHRE)

    # graph(gamma): graph points have three coordinates, (t, gamma(t)).
    _fig3 = Figure(figsize=(6.2, 3.8), layout="constrained")
    _right = _fig3.subplots()
    _right.set_xlim(-1.8, 5.9)
    _right.set_ylim(-2.3, 1.9)
    _right.set_aspect("equal")
    _right.axis("off")
    arrow(_right, path_projection(-4, 0, 0), path_projection(15, 0, 0), "black", lw=0.9)
    arrow(_right, path_projection(0, -1.5, 0), path_projection(0, 2.3, 0), "black", lw=0.9)
    arrow(_right, path_projection(0, 0, -1.5), path_projection(0, 0, 1.7), "black", lw=0.9)
    _right.text(5.55, -1.2, "$t$")
    _right.text(-1.65, -1.2, "$y^1$")
    _right.text(0.12, 1.6, "$y^2$")
    _s = np.linspace(-4, 14.2, 900)
    _hx, _hy = path_projection(_s, np.cos(_s), np.sin(_s))
    _phase = np.mod(_s, 2 * np.pi)
    _front = ~((_phase > 2.9) & (_phase < 1.5 * np.pi))
    _right.plot(np.where(_front, np.nan, _hx), np.where(_front, np.nan, _hy), color=OCHRE, lw=1, alpha=0.6)
    _right.plot(np.where(_front, _hx, np.nan), np.where(_front, _hy, np.nan), color=OCHRE, lw=1.5)
    for _m in (-3.4, 1.3, 7.6, 13.85):
        _p0 = path_projection(_m - 0.12, math.cos(_m - 0.12), math.sin(_m - 0.12))
        _p1 = path_projection(_m + 0.12, math.cos(_m + 0.12), math.sin(_m + 0.12))
        _right.annotate("", xy=_p1, xytext=_p0, arrowprops={"arrowstyle": "-|>", "color": OCHRE, "lw": 0.8, "mutation_scale": 9, "shrinkA": 0, "shrinkB": 0})
    for _n, _name in enumerate(("$t=0$", r"$t=\pi$", r"$t=2\pi$", r"$t=3\pi$", r"$t=4\pi$")):
        _q = path_projection(_n * math.pi, math.cos(_n * math.pi), math.sin(_n * math.pi))
        _right.plot(*_q, "o", color=GREY, ms=3)
        _right.annotate(_name, _q, textcoords="offset points", xytext=(-8, 8) if _n % 2 == 0 else (7, 7), ha="right" if _n % 2 == 0 else "left", color="#555555", fontsize=12)
    _right.plot(*path_projection(_t, math.cos(_t), math.sin(_t)), "o", color=BLUE, ms=4.5, label=r"$(t,\gamma(t))$")
    _right.set_title(r"$\mathrm{graph}(\gamma)$: helix", color=OCHRE)
    _right.legend(loc="lower center", bbox_to_anchor=(0.5, -0.17), frameon=False, fontsize=13)

    mo.vstack(
        [
            mo.hstack(
                [t_circle, mo.md(rf"$\gamma({_t:g}) = \begin{{bmatrix}} {math.cos(_t):.2f} \\ {math.sin(_t):.2f} \end{{bmatrix}}$")],
                justify="start", gap=3, align="center",
            ),
            mo.center(_fig),
            mo.center(_fig3),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** We can extend vector operations to paths. Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^m$, and $\lambda : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    \begin{aligned}
    \underbrace{(\gamma + \sigma)(t)}_{\text{addition of paths}} &= \underbrace{\gamma(t) + \sigma(t)}_{\text{addition of vectors}} &\qquad \gamma + \sigma &: \mathbb{R} \longrightarrow \mathbb{R}^m \\[10pt]
    \underbrace{(\lambda \gamma)(t)}_{\substack{\text{multiplication of scalar} \\ \text{function and a path}}} &= \underbrace{\lambda(t)\, \gamma(t)}_{\substack{\text{multiplication of} \\ \text{scalar and vector}}} &\qquad \lambda \gamma &: \mathbb{R} \longrightarrow \mathbb{R}^m \\[10pt]
    \underbrace{(\gamma \cdot \sigma)(t)}_{\text{dot product of paths}} &= \underbrace{\gamma(t) \cdot \sigma(t)}_{\text{dot product of vectors}} &\qquad \gamma \cdot \sigma &: \mathbb{R} \longrightarrow \mathbb{R} \\[10pt]
    \underbrace{(\gamma \times \sigma)(t)}_{\substack{\text{cross-product of} \\ \text{paths in } \mathbb{R}^3}} &= \underbrace{\gamma(t) \times \sigma(t)}_{\substack{\text{cross-product of} \\ \text{vectors in } \mathbb{R}^3}} &\qquad \gamma \times \sigma &: \mathbb{R} \longrightarrow \mathbb{R}^3 \quad (m = 3)
    \end{aligned}
    $$

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, \quad \sigma(t) = \begin{bmatrix} at + b \\ ct + d \end{bmatrix}, \quad \lambda(t) = \cos(t)$

    $$
    \begin{aligned}
    (\gamma + \sigma)(t) &= \begin{bmatrix} \cos(t) + at + b \\ \sin(t) + ct + d \end{bmatrix} \\[4pt]
    (\gamma \cdot \sigma)(t) &= \cos(t)(at + b) + \sin(t)(ct + d) \\[4pt]
    \lVert \gamma \rVert^2(t) &= (\gamma \cdot \gamma)(t) = \cos(t)^2 + \sin(t)^2 = 1 \\[4pt]
    (\lambda \gamma)(t) &= \begin{bmatrix} \cos(t)^2 \\ \cos(t) \sin(t) \end{bmatrix}
    \end{aligned}
    $$

    ## Limits
    """
            ),
            definition(
                r"""
    Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $a \in \mathbb{R}$ and $\vec{b} \in \mathbb{R}^m$ we say

    $$
    \lim_{t \to a} \gamma(t) = \vec{b}
    $$

    if we can make $\gamma(t)$ *arbitrarily* close to $\vec{b}$ by taking $t$ *sufficiently* close to, but different from, $a$.

    Precisely, for every $\varepsilon > 0$ there exists $\delta > 0$ such that

    $$
    0 < \lvert t - a \rvert < \delta \quad \Longrightarrow \quad \lVert \gamma(t) - \vec{b} \rVert < \varepsilon.
    $$

    The value at $t = a$ is irrelevant; $\gamma$ need not be defined there.
    """
            ),
            theorem(
                r"""
    Limit of paths can be calculated componentwise

    $$
    \begin{gathered}
    \lim_{t \to a} \gamma(t) = \vec{b} \quad \Longleftrightarrow \quad \lim_{t \to a} \gamma^i(t) = b^i \\
    \forall\, i = 1, 2, \dots, m
    \end{gathered}
    $$
    """
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

    $$
    \lim_{t \to \pi/2} \gamma(t) = \begin{bmatrix} \lim_{t \to \pi/2} \cos(t) \\ \lim_{t \to \pi/2} \sin(t) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    $$

    **Remark.** Limits are unique, provided they exist!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, OCHRE, arrow, definition, mo, np, path_projection, theorem):
    _fig = Figure(figsize=(5.6, 4.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-1.8, 2.9)
    _ax.set_ylim(-1.8, 1.9)
    _ax.set_aspect("equal")
    _ax.axis("off")
    arrow(_ax, path_projection(-3.8, 0, 0), path_projection(7, 0, 0), "black", lw=0.9)
    arrow(_ax, path_projection(0, -1.4, 0), path_projection(0, 2.3, 0), "black", lw=0.9)
    arrow(_ax, path_projection(0, 0, -1.5), path_projection(0, 0, 1.7), "black", lw=0.9)
    _ax.text(2.6, -0.7, "$t$")
    _ax.text(-1.65, -1.2, "$y^1$")
    _ax.text(0.12, 1.6, "$y^2$")
    for _s in (np.linspace(-2.8, -0.001, 250), np.linspace(0.001, 6.2, 600)):
        _ax.plot(*path_projection(_s, np.cos(_s), np.sin(_s)), color=OCHRE, lw=1.5)
    _limit = path_projection(0, 1, 0)
    _value = path_projection(0, 0, 1)
    _ax.plot(*_limit, "o", color=BLUE, ms=6, mfc="white", mew=1.2)
    _ax.plot(*_value, "o", color=BLUE, ms=4.5)
    _ax.annotate(r"$(0,\lim_{t\to0}\gamma(t))$", _limit, xytext=(-5, -66), textcoords="offset points", ha="center", color=BLUE, fontsize=13)
    _ax.annotate(r"$(0,\gamma(0))$", _value, xytext=(-8, 8), textcoords="offset points", ha="right", color=BLUE, fontsize=13)
    _ax.set_title(r"$\mathrm{graph}(\gamma)$", color=OCHRE)

    mo.vstack(
        [
            mo.md(r"## Continuity"),
            definition(
                r"""
    A path $\gamma$ is **continuous** at $t = a$ if

    $$
    \lim_{t \to a} \gamma(t) = \gamma(a)
    $$

    $\gamma$ is continuous in $(a_1, a_2) \subset \mathbb{R}$ if it is continuous at every $t \in (a_1, a_2)$.
    """
            ),
            theorem(
                r"""
    A path is continuous iff all of its components are continuous

    $$
    \begin{gathered}
    \lim_{t \to a} \gamma(t) = \gamma(a) \quad \Longleftrightarrow \quad \lim_{t \to a} \gamma^i(t) = \gamma^i(a) \\
    \forall\, i = 1, 2, \dots, m
    \end{gathered}
    $$
    """
            ),
            mo.vstack(
                [
                    mo.md(
                        r"""
    **Example.**

    $$
    \gamma(t) = \begin{cases}
    \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, & t \neq 0 \\[12pt]
    \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0
    \end{cases}
    $$
    """
                    ),
                    mo.center(_fig),
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
            mo.md(r"## Differentiability"),
            definition(
                r"""
    A path $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is **differentiable** at $t = a$ if

    $$
    \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} \quad \text{exists.}
    $$

    If it exists we call it the **derivative** of $\gamma$ at $t = a$ and denote it $\gamma'(a)$.
    """
            ),
            mo.md(
                r"""
    We also call $\gamma'(a)$ the **velocity** of the path $\gamma$ at $t = a$; &nbsp; $\gamma(a)$ is the **position** of $\gamma$ at $t = a$.

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

    $$
    \begin{aligned}
    \gamma'(a) &= \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} = \lim_{t \to a} \begin{bmatrix} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix} \\[6pt]
    &= \begin{bmatrix} \displaystyle \lim_{t \to a} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \displaystyle \lim_{t \to a} \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix} = \begin{bmatrix} \dfrac{d}{dt} \cos(t) \Big|_{t = a} \\[10pt] \dfrac{d}{dt} \sin(t) \Big|_{t = a} \end{bmatrix} = \begin{bmatrix} -\sin(a) \\ \cos(a) \end{bmatrix}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_circle = mo.ui.slider(0, 6.25, 0.05, value=0.8, label="$a$", show_value=True)
    return (a_circle,)


@app.cell(hide_code=True)
def _(Arc, BLUE, Figure, GREEN, OCHRE, a_circle, arrow, math, mo, np):
    _a = a_circle.value
    _p = (math.cos(_a), math.sin(_a))
    _v = (-math.sin(_a), math.cos(_a))
    _tip = (_p[0] + _v[0], _p[1] + _v[1])

    _fig = Figure(figsize=(4.8, 4.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-2.2, 2.2)
    _ax.set_ylim(-2, 2)
    _ax.set_aspect("equal")
    _ax.axis("off")
    arrow(_ax, (-1.8, 0), (1.8, 0), "black", lw=0.9)
    arrow(_ax, (0, -1.8), (0, 1.8), "black", lw=0.9)
    _th = np.linspace(0, 2 * np.pi, 361)
    _ax.plot(np.cos(_th), np.sin(_th), color=OCHRE, lw=1.5)
    arrow(_ax, (0, 0), _p, BLUE)
    arrow(_ax, _p, _tip, GREEN)
    _ax.plot(*_p, "o", color=BLUE, ms=4.5)
    _ax.annotate(r"$\gamma(a)$", _p, textcoords="offset points", xytext=(8 * _p[0], 8 * _p[1]), ha="left" if _p[0] >= 0 else "right", va="bottom" if _p[1] >= 0 else "top", color=BLUE, fontsize=13)
    _ax.annotate(r"$\gamma'(a)$", _tip, textcoords="offset points", xytext=(6 * _tip[0], 6 * _tip[1]), ha="left" if _tip[0] >= 0 else "right", va="bottom" if _tip[1] >= 0 else "top", color=GREEN, fontsize=13)
    _ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=math.degrees(_a), color=BLUE, lw=1))

    mo.vstack(
        [
            a_circle,
            mo.center(_fig),
            mo.md(rf"$$\gamma({_a:g}) = \begin{{bmatrix}} {_p[0]:.2f} \\ {_p[1]:.2f} \end{{bmatrix}}, \qquad \gamma'({_a:g}) = \begin{{bmatrix}} {_v[0]:.2f} \\ {_v[1]:.2f} \end{{bmatrix}}$$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Derivatives of paths can be computed componentwise

    $$
    \begin{gathered}
    \gamma'(a) = \vec{v} \quad \Longleftrightarrow \quad \frac{d}{dt} \gamma^i(t) \Big|_{t = a} = v^i \\
    \forall\, i = 1, 2, \dots, m
    \end{gathered}
    $$
    """
            ),
            definition(
                r"""
    If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is differentiable at $t = a$ with velocity vector $\gamma'(a) \neq \vec{0}$, we call the line through $\vec{x} = \gamma(a)$ in the direction of $\vec{v} = \gamma'(a)$ the **tangent line** to $\gamma$ at $t = a$

    $$
    T_a \gamma = \left\{\, \vec{y} = \gamma(a) + s\, \gamma'(a) \;\middle|\; s \in \mathbb{R} \,\right\}
    $$
    """
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} t^2 \\ t \end{bmatrix} \quad \leadsto \quad \gamma'(t) = \begin{bmatrix} 2t \\ 1 \end{bmatrix}$

    $$
    T_a \gamma = \left\{\, \vec{y} = \begin{bmatrix} a^2 \\ a \end{bmatrix} + s \begin{bmatrix} 2a \\ 1 \end{bmatrix} \;\middle|\; s \in \mathbb{R} \,\right\}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_parabola = mo.ui.slider(-1.5, 1.5, 0.1, value=0.7, label="$a$", show_value=True)
    return (a_parabola,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, OCHRE, a_parabola, arrow, mo, np):
    _a = a_parabola.value
    _p, _v = (_a**2, _a), (2 * _a, 1.0)
    _tip = (_p[0] + _v[0], _p[1] + _v[1])

    _fig = Figure(figsize=(5.8, 4.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-1.8, 6.2)
    _ax.set_ylim(-2.5, 3.1)
    _ax.set_aspect("equal")
    _ax.axis("off")
    arrow(_ax, (-1.7, 0), (6, 0), "black", lw=0.9)
    arrow(_ax, (0, -2.4), (0, 2.9), "black", lw=0.9)
    _ax.text(5.8, -0.4, "$y^1$")
    _ax.text(-0.5, 2.7, "$y^2$")
    _t = np.linspace(-2.45, 2.45, 300)
    _ax.plot(_t**2, _t, color=OCHRE, lw=1.5)
    _s = np.array([-8.0, 8.0])
    _ax.plot(_p[0] + _s * _v[0], _p[1] + _s * _v[1], color=GREY, lw=1)
    arrow(_ax, _p, _tip, GREEN)
    _ax.annotate(r"$\gamma'(a)$", _tip, textcoords="offset points", xytext=(-6, 7) if _a >= 0 else (6, 7), ha="right" if _a >= 0 else "left", va="bottom", color=GREEN, fontsize=13)
    _ax.plot(*_p, "o", color=BLUE, ms=4.5)
    _ax.annotate(r"$\gamma(a)$", _p, textcoords="offset points", xytext=(18, -14) if _a >= 0 else (18, 8), va="top" if _a >= 0 else "bottom", color=BLUE, fontsize=13)

    mo.vstack(
        [
            a_parabola,
            mo.center(_fig),
            mo.md(rf"$$T_a \gamma = \left\{{\, \vec{{y}} = \begin{{bmatrix}} {_p[0]:.2f} \\ {_p[1]:g} \end{{bmatrix}} + s \begin{{bmatrix}} {_v[0]:g} \\ 1 \end{{bmatrix}} \;\middle|\; s \in \mathbb{{R}} \,\right\}}$$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q1_a, q1_b = _field(), _field()
    return q1_a, q1_b


@app.cell(hide_code=True)
def _(check, mo, q1_a, q1_b):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let

    $$
    \gamma(t) = \begin{cases}
    \begin{bmatrix} t \\ \dfrac{\sin(t)}{t} \end{bmatrix}, & t \neq 0 \\[14pt]
    \begin{bmatrix} a \\ b \end{bmatrix}, & t = 0
    \end{cases}
    $$

    (a) Find $\displaystyle \lim_{t \to 0} \gamma(t)$.

    (b) Find $a, b \in \mathbb{R}$ such that $\gamma$ is continuous at $t = 0$.
    """
            ),
            _ask(r"$a =$", q1_a, 0),
            _ask(r"$b =$", q1_b, 1),
            mo.md(
                r"""
    ### Question 2

    Consider $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^3$, $\sigma(t) = \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix}$ and $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$, $f(\vec{x}) = (x^2)^2 + (x^3)^2$.

    (a) Show that $\mathrm{Im}(\sigma) \subseteq f^{-1}(1)$.

    (b) Compute $\sigma'(t)$, and find an affine parameterization of the tangent line to $\sigma$ at $t = 0$.

    (c) Is the entire tangent line contained in $f^{-1}(1)$? Justify your answers!
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
