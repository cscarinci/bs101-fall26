import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 08", css_file="bs101.css")


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
    header("Lecture 08", "Week 04", "Lecture 08")
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
def _(Figure, GREEN, RED, cross_axes, mo, np):
    _fig = Figure(figsize=(3.6, 2.8), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-2, 2.3), (-0.6, 2.6))
    _t = np.linspace(-1.55, 1.55, 200)
    _ax.plot(_t, _t**2, color=RED, lw=1.6)
    _ax.plot(0, 0, "o", color=GREEN, ms=7, mfc="white", mew=1.6)
    _ax.plot(0, 1, "o", color=GREEN, ms=6)
    _ax.plot(-1.2, 1.44, "o", color=RED, ms=5)
    _ax.text(-1.95, 1.5, r"$\genfrac{[}{]}{0}{0}{t}{t^2}$", color=RED, fontsize=14)
    _ax.text(0.12, 0.95, r"$\genfrac{[}{]}{0}{0}{0}{1}$", color=GREEN, fontsize=15)
    _ax.text(1.5, 1.5, r"$\mathrm{Im}(\gamma)$", color=RED, fontsize=13)
    _ax.text(0.15, -0.5, "not continuous", color=GREEN, fontsize=12)

    _fig2 = Figure(figsize=(3.6, 2.8), layout="constrained")
    _ax2 = _fig2.subplots()
    cross_axes(_ax2, (-1.6, 2.4), (-1.5, 1.6))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax2.plot(np.cos(_th), np.sin(_th), color=RED, lw=1.6)
    _ax2.plot(1, 0, "o", color=GREEN, ms=6)
    _ax2.plot(0, 1, "o", color=GREEN, ms=6)
    _ax2.text(0.12, 1.1, r"$\genfrac{[}{]}{0}{0}{0}{1}$", color=GREEN, fontsize=15)
    _ax2.text(0.85, 0.75, r"$\genfrac{[}{]}{0}{0}{\cos(t)}{\sin(t)}$", color=RED, fontsize=15)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Local properties of paths

    $$
    \gamma : \mathbb{R} \longrightarrow \mathbb{R}^m, \qquad \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix} \quad (\text{components})
    $$

    $$
    \lim_{t \to a} \gamma(t) = \lim_{t \to a} \begin{bmatrix} \gamma^1(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix} = \begin{bmatrix} \lim_{t \to a} \gamma^1(t) \\ \vdots \\ \lim_{t \to a} \gamma^m(t) \end{bmatrix}
    $$

    - $\gamma$ continuous at $t = a$ if $\displaystyle \lim_{t \to a} \gamma(t) = \gamma(a)$ &nbsp; ($\gamma(a)$ is the position of $\gamma$ at $t = a$; $\gamma$ does not jump between positions at $t = a$)
    - $\gamma$ differentiable at $t = a$ if $\displaystyle \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}$ exists &nbsp; ($\gamma'(a)$, the velocity of $\gamma$ at $t = a$)
    """
            ),
            mo.hstack(
                [
                    mo.md(
                        r"""
    **Example.**

    $$
    \gamma(t) = \begin{cases}
    \begin{bmatrix} t \\ t^2 \end{bmatrix}, & t \neq 0 \\[12pt]
    \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0
    \end{cases}
    $$
    """
                    ),
                    _fig,
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
            mo.hstack(
                [
                    mo.md(
                        r"""
    $$
    \sigma(t) = \begin{cases}
    \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, & t \neq 0 \\[12pt]
    \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0
    \end{cases}
    $$
    """
                    ),
                    _fig2,
                ],
                widths=[1, 1],
                gap=2,
                align="center",
            ),
            mo.md(
                r"""
    $$
    \lim_{t \to 0} \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}
    = \begin{bmatrix} \cos(2\pi) \\ \sin(2\pi) \end{bmatrix} = \begin{bmatrix} \cos(4\pi) \\ \sin(4\pi) \end{bmatrix} \qquad \text{also in } \mathrm{Im}(\sigma)
    $$

    - discontinuity is a “jump” in the parameterization of the image, not necessarily a hole in $\mathrm{Im}(\gamma)$
    - discontinuity is a hole in $\mathrm{graph}(\gamma)$!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, GREY, arrow, cross_axes, definition, mo, np):
    _fig = Figure(figsize=(3.4, 3.0), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-0.4, 3.6), (-0.4, 3.2))
    _a, _d = (1.9, 1.7), 1.1
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), color=GREY, alpha=0.18, lw=0)
    _ax.plot(_a[0] + _d * np.cos(_th), _a[1] + _d * np.sin(_th), "--", color=GREY, lw=1.3)
    _x = (1.2, 2.2)
    arrow(_ax, (0, 0), _a, "black", r"$\vec{a}$", at_tip=True)
    arrow(_ax, (0, 0), _x, GREY)
    _ax.text(0.5, 1.6, r"$\vec{x}$", color="#555555", fontsize=16)
    arrow(_ax, _a, _x, GREY, lw=1.3)
    _ax.text(1.5, 2.12, r"$\vec{x} - \vec{a}$", color="#555555", fontsize=12)
    _ax.plot([_a[0], _a[0] + _d * 0.94], [_a[1], _a[1] + _d * 0.34], color=GREY, lw=1)
    _ax.text(2.4, 1.6, r"$\delta$", color="#555555", fontsize=14)

    mo.vstack(
        [
            mo.md(
                r"""
    **Today:** Local properties of scalar functions and maps

    **Remark.** Given $f, g : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\lambda : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$, we can define

    - $(f + g) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $(f + g)(\vec{x}) = f(\vec{x}) + g(\vec{x})$
    - $(\lambda f) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $(\lambda f)(\vec{x}) = \lambda(\vec{x}) f(\vec{x})$
    - $(f \cdot g) : A \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $(f \cdot g)(\vec{x}) = f(\vec{x}) \cdot g(\vec{x})$

    If $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ and $g : B \subseteq \mathbb{R}^m \longrightarrow C \subseteq \mathbb{R}^p$

    - $(g \circ f) : A \subseteq \mathbb{R}^n \longrightarrow C \subseteq \mathbb{R}^p$ &nbsp; $\leadsto$ &nbsp; $(g \circ f)(\vec{x}) = g(f(\vec{x}))$

    ## Limits
    """
            ),
            mo.hstack(
                [
                    definition(
                        r"""
    Given $\vec{a} \in \mathbb{R}^n$ and $\delta > 0$

    $$
    B(\vec{a}, \delta) = \left\{\, \vec{x} \in \mathbb{R}^n \;\middle|\; \lVert \vec{x} - \vec{a} \rVert < \delta \,\right\}
    $$

    (the distance of $\vec{x}$ from $\vec{a}$ is smaller than $\delta$) is the **open ball** in $\mathbb{R}^n$ centered at $\vec{a}$ with radius $\delta$.
    """
                    ),
                    _fig,
                ],
                widths=[3, 2],
                gap=2,
                align="center",
            ),
            mo.md(
                r"""
    **Remark.** The “boundary” is not included! Only “interior” points are part of $B(\vec{a}, \delta)$.

    $$
    \begin{aligned}
    S(\vec{a}, \delta) &= \left\{\, \vec{x} \in \mathbb{R}^n \;\middle|\; \lVert \vec{x} - \vec{a} \rVert = \delta \,\right\} && \text{sphere in } \mathbb{R}^n \text{ centered at } \vec{a} \text{ with radius } \delta \\[4pt]
    \overline{B(\vec{a}, \delta)} &= B(\vec{a}, \delta) \cup S(\vec{a}, \delta) && \text{closed ball in } \mathbb{R}^n \text{ centered at } \vec{a} \text{ with radius } \delta \quad (\lVert \vec{x} - \vec{a} \rVert \leq \delta)
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, arrow, definition, mo, np):
    _fig = Figure(figsize=(8.8, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.3, 11.6)
    _ax.set_ylim(-0.4, 3.2)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _th = np.linspace(0, 2 * np.pi, 200)
    # domain
    arrow(_ax, (-0.2, 0.2), (3.2, 0.2), "black", lw=0.9)
    arrow(_ax, (0.2, -0.3), (0.2, 3.0), "black", lw=0.9)
    _ax.text(-0.3, 2.9, r"$\mathbb{R}^n$", fontsize=14)
    _ax.fill(1.7 + 0.8 * np.cos(_th), 1.7 + 0.8 * np.sin(_th), color=BLUE, alpha=0.18, lw=0)
    _ax.plot(1.7 + 0.8 * np.cos(_th), 1.7 + 0.8 * np.sin(_th), "--", color=BLUE, lw=1.2)
    _ax.plot(1.7, 1.7, "o", color="black", ms=4)
    _ax.text(1.8, 1.75, r"$\vec{a}$", fontsize=14)
    _ax.text(1.0, 0.45, r"$B(\vec{a}, \delta)$", color=BLUE, fontsize=12)
    # the map
    arrow(_ax, (3.6, 2.2), (5.0, 2.2), "black", lw=1.2, connectionstyle="arc3,rad=-0.3")
    _ax.text(4.2, 2.65, "$f$", fontsize=15)
    # codomain
    arrow(_ax, (5.6, 0.2), (9.4, 0.2), "black", lw=0.9)
    arrow(_ax, (5.9, -0.3), (5.9, 3.0), "black", lw=0.9)
    _ax.text(5.35, 2.9, r"$\mathbb{R}^m$", fontsize=14)
    _ax.fill(7.6 + 1.25 * np.cos(_th), 1.7 + 1.25 * np.sin(_th), color=GREY, alpha=0.15, lw=0)
    _ax.plot(7.6 + 1.25 * np.cos(_th), 1.7 + 1.25 * np.sin(_th), "--", color=GREY, lw=1.2)
    _bx = 7.35 + 0.55 * np.cos(_th) + 0.12 * np.cos(3 * _th)
    _by = 2.05 + 0.38 * np.sin(_th) + 0.08 * np.sin(2 * _th)
    _ax.fill(_bx, _by, color=BLUE, alpha=0.3, lw=0)
    _ax.plot(7.75, 1.6, "o", color="black", ms=4)
    _ax.text(7.85, 1.5, r"$\vec{b}$", fontsize=14)
    _ax.text(8.75, 0.5, r"$B(\vec{b}, \varepsilon)$", color="#555555", fontsize=12)
    _ax.text(9.0, 2.2, r"$f(B(\vec{a}, \delta) - \{\vec{a}\})$", color=BLUE, fontsize=12)
    _ax.plot([7.95, 8.95], [2.15, 2.28], color=BLUE, lw=0.8)

    mo.vstack(
        [
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\vec{a} \in \mathbb{R}^n$, $\vec{b} \in \mathbb{R}^m$, we say

    $$
    \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b} \qquad (\text{the limit of } f(\vec{x}) \text{ as } \vec{x} \text{ approaches } \vec{a} \text{ exists and is equal to } \vec{b})
    $$

    if for every choice of $\varepsilon > 0$ we can make $f(\vec{x})$ $\varepsilon$-close to $\vec{b}$ by finding $\delta > 0$ and taking $\vec{x}$ $\delta$-close to $\vec{a}$ (different from $\vec{a}$).
    """
            ),
            mo.md(
                r"""
    For every $\varepsilon > 0$, we can find $\delta > 0$ such that $\vec{x} \in B(\vec{a}, \delta) - \{\vec{a}\}$ guarantees that $f(\vec{x}) \in B(\vec{b}, \varepsilon)$

    $$
    \Longleftrightarrow \quad f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    Choose $B(\vec{b}, \varepsilon)$. Can we find $B(\vec{a}, \delta)$ such that $f\big( B(\vec{a}, \delta) - \{\vec{a}\} \big) \subseteq B(\vec{b}, \varepsilon)$?

    If yes for every $\varepsilon > 0$ &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}$!

    **Example.** $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$

    $$
    f(\vec{x}) = \begin{cases}
    \dfrac{2 (x^1)^2}{\lVert \vec{x} \rVert}, & \vec{x} \neq \vec{0} \\[10pt]
    5, & \vec{x} = \vec{0}
    \end{cases}
    $$

    Claim: $\displaystyle \lim_{\vec{x} \to \vec{0}} f(\vec{x}) = 0$

    **Proof.** To show this

    1. choose $\varepsilon > 0$ (let's say $\varepsilon = 1$)
    2. look for $\delta > 0$ such that

        $$
        0 < \lVert \vec{x} - \vec{0} \rVert < \delta \quad \Longrightarrow \quad \lvert f(\vec{x}) - 0 \rvert < \varepsilon = 1
        $$

        Whenever $\vec{x}$ is $\delta$-close to $\vec{a} = \vec{0}$, we guarantee $f(\vec{x})$ is $1$-close to $b = 0$ (as close as we want it).

    For $\vec{x} \neq \vec{0}$

    $$
    \lvert f(\vec{x}) - 0 \rvert = \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} \leq \frac{2 (x^1)^2}{\lVert \vec{x} \rVert} + \frac{2 (x^2)^2}{\lVert \vec{x} \rVert} = 2\, \frac{\lVert \vec{x} \rVert^2}{\lVert \vec{x} \rVert} = 2 \lVert \vec{x} \rVert
    $$

    $$
    \Longrightarrow \quad \lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert = 2 \lVert \vec{x} - \vec{0} \rVert
    $$

    $\Longrightarrow$ &nbsp; whenever we make $0 < \lVert \vec{x} - \vec{0} \rVert < \tfrac{1}{2} = \delta$ (for $\varepsilon = 1$) we guarantee that $\lvert f(\vec{x}) - 0 \rvert < 1$!

    Now repeat the argument for every $\varepsilon > 0$: &nbsp; $\varepsilon = \tfrac{1}{2} \leadsto \delta = \tfrac{1}{4}$, &nbsp; $\varepsilon = \tfrac{1}{3} \leadsto \delta = \tfrac{1}{6}$, &nbsp; …

    $\therefore$ &nbsp; if $0 < \lVert \vec{x} - \vec{0} \rVert < \tfrac{\varepsilon}{2} = \delta$

    $$
    \Longrightarrow \quad \lvert f(\vec{x}) - 0 \rvert \leq 2 \lVert \vec{x} \rVert < 2 \cdot \tfrac{\varepsilon}{2} = \varepsilon \qquad \square
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    eps = mo.ui.slider(0.1, 2, 0.1, value=1, label=r"$\varepsilon$", show_value=True)
    return (eps,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, arrow, cross_axes, eps, mo, np):
    _e = eps.value
    _d = _e / 2
    _fig = Figure(figsize=(8.4, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 1])

    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.fill(_d * np.cos(_th), _d * np.sin(_th), color=BLUE, alpha=0.2, lw=0)
    _left.plot(_d * np.cos(_th), _d * np.sin(_th), "--", color=BLUE, lw=1.3)
    _left.set_title(rf"$B(\vec{{0}}, \delta)$,  $\delta = \varepsilon / 2 = {_d:g}$", color=BLUE, fontsize=13)

    _right.set_xlim(-1.6, 2.2)
    _right.set_ylim(-2.3, 2.5)
    _right.axis("off")
    arrow(_right, (0, -2.3), (0, 2.4), "black", lw=0.9)
    _right.text(0.15, 2.25, r"$\mathbb{R}$", fontsize=13)
    _right.plot([0, 0], [-_e, _e], color=GREY, lw=7, alpha=0.35, solid_capstyle="butt")
    _right.plot([0, 0], [0, 2 * _d], color=BLUE, lw=3.5, solid_capstyle="butt")
    for _y, _name in ((_e, r"$\varepsilon$"), (-_e, r"$-\varepsilon$"), (0, "$0$")):
        _right.plot([-0.08, 0.08], [_y, _y], color="black", lw=1)
        _right.text(-0.2, _y, _name, ha="right", va="center", fontsize=13)
    _right.plot(0, 5, "o", color=RED, ms=5, clip_on=True)
    _right.text(0.25, _e * 0.5, r"$f(B(\vec{0}, \delta) - \{\vec{0}\})$", color=BLUE, fontsize=12, va="center")
    _right.text(0.25, -_e * 0.6, r"$B(0, \varepsilon)$", color="#555555", fontsize=12, va="center")

    mo.vstack([eps, _fig])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, arrow, mo, np, theorem):
    _fig = Figure(figsize=(7.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.2, 9.2)
    _ax.set_ylim(0, 2.9)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(1.2 + 0.8 * np.cos(_th), 1.4 + 0.8 * np.sin(_th), color=BLUE, alpha=0.18, lw=0)
    _ax.plot(1.2 + 0.8 * np.cos(_th), 1.4 + 0.8 * np.sin(_th), "--", color=BLUE, lw=1.2)
    _ax.plot(1.2, 1.4, "o", color="black", ms=5, mfc="white")
    _ax.text(1.05, 1.0, r"$\vec{a}$", fontsize=14)
    _ax.plot([1.2, 1.85], [1.4, 1.85], color=BLUE, lw=1)
    _ax.text(1.4, 1.75, r"$\delta$", color=BLUE, fontsize=12)
    _ax.text(0.6, 0.2, r"$B(\vec{a}, \delta)$", color=BLUE, fontsize=12)
    arrow(_ax, (2.5, 1.9), (3.9, 1.9), "black", lw=1.2, connectionstyle="arc3,rad=-0.3")
    _ax.text(3.1, 2.4, "$f$", fontsize=15)
    for _c, _name in ((5.3, r"$\vec{b}_1$"), (7.5, r"$\vec{b}_2$")):
        _ax.plot(_c + 1.1 * np.cos(_th), 1.4 + 1.1 * np.sin(_th), "--", color="black", lw=1.2)
        _ax.plot(_c, 1.4, "o", color="black", ms=4)
        _ax.text(_c - 0.15, 0.95, _name, fontsize=14)
        _ax.plot([_c, _c + 1.1], [1.4, 1.4], color=GREY, lw=1)
        _ax.text(_c + 0.5, 1.5, r"$\varepsilon$", fontsize=12)
    _bx = 4.95 + 0.42 * np.cos(_th) + 0.1 * np.cos(3 * _th)
    _by = 1.95 + 0.28 * np.sin(_th) + 0.06 * np.sin(2 * _th)
    _ax.fill(_bx, _by, color=BLUE, alpha=0.3, lw=0)
    _ax.text(3.6, 0.1, r"$f(B(\vec{a}, \delta) \setminus \{\vec{a}\})$", color=BLUE, fontsize=12)

    mo.vstack(
        [
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ and $\vec{a} \in \mathbb{R}^n$

    If $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1 \in \mathbb{R}^m$ and $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_2 \in \mathbb{R}^m$ then $\vec{b}_1 = \vec{b}_2$.

    Limits are unique! (when they exist)
    """
            ),
            mo.md(
                r"""
    **Proof.** Given $\vec{b}_1 \neq \vec{b}_2 \in \mathbb{R}^m$ let $\varepsilon = \dfrac{\lVert \vec{b}_2 - \vec{b}_1 \rVert}{2}$

    $$
    \Longrightarrow \quad B(\vec{b}_1, \varepsilon) \cap B(\vec{b}_2, \varepsilon) = \emptyset
    $$

    Remember: the sphere is not part of the ball. (To be more precise we need to use the triangle inequality.)
    """
            ),
            _fig,
            mo.md(
                r"""
    $\Longrightarrow$ &nbsp; if $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1$, then there is a $\delta_1 > 0$ s.t.

    $$
    f\big( B(\vec{a}, \delta_1) \setminus \{\vec{a}\} \big) \subset B(\vec{b}_1, \varepsilon)
    $$

    $\Longrightarrow$ &nbsp; for any $\delta_2 < \delta_1$

    $$
    f\big( B(\vec{a}, \delta_2) \setminus \{\vec{a}\} \big) \not\subset B(\vec{b}_2, \varepsilon)
    $$

    $$
    \Longrightarrow \quad \lim_{\vec{x} \to \vec{a}} f(\vec{x}) \neq \vec{b}_2 \qquad \square
    $$

    **Example.**

    $$
    f(\vec{x}) = \frac{(x^1)^2}{\lVert \vec{x} \rVert^2} = \frac{(x^1)^2}{(x^1)^2 + (x^2)^2}
    $$

    Claim: $\displaystyle \lim_{\vec{x} \to \vec{0}} f(\vec{x})$ does not exist! (it is not well-defined)

    **Proof.** Let's consider two different ways $\vec{x}$ can approach $\vec{0}$

    1. along $\vec{x} = t\vec{e}_1 = \begin{bmatrix} t \\ 0 \end{bmatrix}$ for $t \neq 0$ (since $\vec{x} \neq \vec{0}$)

        $$
        f(t\vec{e}_1) = \frac{t^2}{t^2 + 0^2} = 1 \qquad (\text{constant})
        $$

        For any chosen $\varepsilon > 0$

        $$
        0 < \lVert t\vec{e}_1 - \vec{0} \rVert < \delta \quad \Longrightarrow \quad \lVert f(t\vec{e}_1) - 1 \rVert = 0 < \varepsilon
        $$

        for every $\delta > 0$! since $f(t\vec{e}_1) = 1$ is constant!

        $$
        \therefore \quad \lim_{\substack{\vec{x} \to \vec{0} \\ \vec{x} = t\vec{e}_1}} f(\vec{x}) = 1
        $$

    2. along $\vec{x} = s\vec{e}_2 = \begin{bmatrix} 0 \\ s \end{bmatrix}$ for $s \neq 0$

        $$
        f(s\vec{e}_2) = \frac{0^2}{0^2 + s^2} = 0 \qquad \forall\, s \neq 0
        $$

        For any $\varepsilon > 0$

        $$
        0 < \lVert s\vec{e}_2 - \vec{0} \rVert < \delta \quad \Longrightarrow \quad \lVert f(s\vec{e}_2) - 0 \rVert = 0 < \varepsilon
        $$

        for every $\delta > 0$!

        $$
        \therefore \quad \lim_{\substack{\vec{x} \to \vec{0} \\ \vec{x} = s\vec{e}_2}} f(\vec{x}) = 0
        $$

    Two possible values for the limit &nbsp; $\Longrightarrow$ &nbsp; limit is not well-defined!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    theta = mo.ui.slider(0, 180, 5, value=0, label=r"direction (degrees from $\vec{e}_1$)", show_value=True)
    return (theta,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, arrow, cross_axes, math, mo, np, theta):
    _a = math.radians(theta.value)
    _c, _s = math.cos(_a), math.sin(_a)
    _val = _c**2

    _fig = Figure(figsize=(8.4, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.3, 1])
    cross_axes(_left, (-1.5, 1.6), (-1.3, 1.4), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.plot(0.8 * np.cos(_th), 0.8 * np.sin(_th), "--", color=GREY, lw=1.2)
    _left.text(0.62, -0.85, r"$B(\vec{0}, \delta)$", color="#555555", fontsize=12)
    _left.plot([-1.2 * _c, 1.2 * _c], [-1.2 * _s, 1.2 * _s], color=BLUE, lw=2.4)
    _left.plot(0, 0, "o", color=BLUE, ms=6, mfc="white", mew=1.5)

    _right.set_xlim(-1.4, 1.8)
    _right.set_ylim(-0.5, 1.6)
    _right.axis("off")
    arrow(_right, (0, -0.5), (0, 1.55), "black", lw=0.9)
    _right.text(0.12, 1.45, r"$\mathbb{R}$", fontsize=13)
    for _y in (0, 1):
        _right.plot([-0.06, 0.06], [_y, _y], color="black", lw=1)
        _right.text(-0.15, _y, f"${_y}$", ha="right", va="center", fontsize=13)
    _right.plot(0, _val, "o", color=BLUE, ms=8)
    _right.text(0.2, _val, rf"$f = {_val:.2f}$", color=BLUE, fontsize=13, va="center")

    mo.vstack([theta, _fig])
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\lambda : \mathbb{R}^n \longrightarrow \mathbb{R}$

    if $\displaystyle \lim_{\vec{x} \to \vec{a}} f(\vec{x}) = \vec{b}_1$, &nbsp; $\displaystyle \lim_{\vec{x} \to \vec{a}} g(\vec{x}) = \vec{b}_2$, &nbsp; $\displaystyle \lim_{\vec{x} \to \vec{a}} \lambda(\vec{x}) = \beta$

    - $\displaystyle \lim_{\vec{x} \to \vec{a}} (f + g)(\vec{x}) = \vec{b}_1 + \vec{b}_2$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} (\lambda f)(\vec{x}) = \beta\, \vec{b}_1$
    - $\displaystyle \lim_{\vec{x} \to \vec{a}} (f \cdot g)(\vec{x}) = \vec{b}_1 \cdot \vec{b}_2$
    """
    )
    return


if __name__ == "__main__":
    app.run()
