import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 12 • The chain rule", css_file="bs101.css")


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
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a result made from them (sum, multiple, angle, tangent vector, gradient)
    #   ORANGE (ochre) a third object, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
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
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
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
        One line weight for every figure; the head is open and sized in points from the line width,
        so arrows look alike across lectures at any axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={3 * lw:g},head_width={1.3 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 12", "Week 06", "Lecture 12 • The chain rule")
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
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## So far

    - $f : \mathbb{R} \longrightarrow \mathbb{R}$ (single variable, scalar valued) is differentiable at $x = a$ if

        $$
        \begin{gathered}
        f'(a) = \lim_{x \to a} \frac{f(x) - f(a)}{x - a} \in \mathbb{R} \quad \text{is well-defined} \\[6pt]
        \Big( \text{slope of tangent line to } \mathrm{graph}(f) \text{ at } \begin{bmatrix} a \\ f(a) \end{bmatrix} \Big)
        \end{gathered}
        $$

    - $f : \mathbb{R} \longrightarrow \mathbb{R}^m$ (single variable, vector valued: path)

        $$
        \leadsto \qquad f(x) = \begin{bmatrix} f^1(x) \\ \vdots \\ f^m(x) \end{bmatrix}, \quad f^i : \mathbb{R} \longrightarrow \mathbb{R}
        $$

        is differentiable at $x = a$ if each component $f^i : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $x = a$ (as a single variable scalar function)

        $$
        \Longleftrightarrow \qquad \lim_{x \to a} \frac{f(x) - f(a)}{x - a} = \underbrace{f'(a)}_{\mathclap{\footnotesize \begin{matrix}\text{derivative} \\ \text{of } f \text{ at } x = a\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{derivative} \\ \text{of } f \text{ at } x = a\end{matrix}}} = \begin{bmatrix} (f^1)'(a) \\ \vdots \\ (f^m)'(a) \end{bmatrix} \in \mathbb{R}^m
        \qquad (\text{velocity vector of } f \text{ at } x = a)
        $$

    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ (multivariable, scalar valued) is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ \vdots \\ a^n \end{bmatrix}$ if

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

        where the derivative of $f$ at $\vec{x} = \vec{a}$ (Jacobian matrix of $f$ at $\vec{x} = \vec{a}$) is

        $$
        Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \dfrac{\partial f}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)
        $$

    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ (multivariable, vector valued)

        $$
        \leadsto \qquad f(\vec{x}) = \begin{bmatrix} f^1(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}, \quad f^i : \mathbb{R}^n \longrightarrow \mathbb{R}
        $$

        is differentiable at $\vec{x} = \vec{a}$ if each component $f^i : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a}$ (as a multivariable scalar valued function)

        $$
        \Longleftrightarrow \qquad \lim_{\vec{x} \to \vec{a}} \frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

        where the derivative of $f$ at $\vec{a}$ (Jacobian matrix of $f$ at $\vec{a}$) is

        $$
        Df(\vec{a}) = \begin{bmatrix} Df^1(\vec{a}) \\ Df^2(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix}
        = \begin{bmatrix}
        \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \dfrac{\partial f^1}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f^1}{\partial x^n}(\vec{a}) \\[10pt]
        \dfrac{\partial f^2}{\partial x^1}(\vec{a}) & \dfrac{\partial f^2}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f^2}{\partial x^n}(\vec{a}) \\
        \vdots & \vdots & \ddots & \vdots \\
        \dfrac{\partial f^m}{\partial x^1}(\vec{a}) & \dfrac{\partial f^m}{\partial x^2}(\vec{a}) & \cdots & \dfrac{\partial f^m}{\partial x^n}(\vec{a})
        \end{bmatrix} \in \mathrm{Mat}(m \times n)
        $$

        $\Longleftrightarrow$ &nbsp; $g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$ is a good affine approximation to $f(\vec{x})$ near $\vec{a}$
    """
            ),
            theorem(
                r"""
    If all partial derivatives $\partial f^i / \partial x^j (\vec{x})$ are well-defined on an open ball around $\vec{a}$ and they are all continuous at $\vec{x} = \vec{a}$, then $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{x} = \vec{a}$!
    """,
                "Continuous partial derivatives",
            ),
            mo.md(r"""**In this lecture:** the chain rule

            **References:** MT 2.5, 2.6""").style({"display": "block"}),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.7 &nbsp; The chain rule

    **Recall:** $f, g : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $f$ differentiable at $a$, &nbsp; $g$ differentiable at $b = f(a)$

    $\Longrightarrow$ &nbsp; $g \circ f : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $a$ with

    $$
    (g \circ f)'(a) = g'(f(a)) \cdot f'(a) \qquad (\textbf{chain rule})
    $$

    $\leadsto$ &nbsp; we want to generalize this to vector valued multivariable functions $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$

    $\leadsto$ &nbsp; start with $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ (path) and $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ (scalar valued function)

    ### The chain rule along a path
    """
            ),
            theorem(
                r"""
    If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ is differentiable at $t = t_0$ and $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \gamma(t_0)$, then ${g = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}}$ is differentiable at $t = t_0$ with

    $$
    g'(t_0) = (f \circ \gamma)'(t_0) = \underbrace{Df(\gamma(t_0))}_{\mathclap{\footnotesize \mathbb{R}^n \to \mathbb{R}}\vphantom{\footnotesize \mathbb{R}^n \to \mathbb{R}}}\, \underbrace{(\gamma'(t_0))}_{\mathclap{\footnotesize \in \mathbb{R}^n}\vphantom{\footnotesize \in \mathbb{R}^n}}
    $$
    """,
                "Chain rule along a path",
            ),
            mo.md(
                r"""
    **Proof.** (with $\vec{x} = \gamma(t)$ and $\vec{a} = \gamma(t_0)$)

    $$
    \begin{aligned}
    \frac{g(t) - g(t_0)}{t - t_0} &= \frac{f(\gamma(t)) - f(\gamma(t_0))}{t - t_0}
    = \frac{f(\gamma(t)) - f(\gamma(t_0))}{\lVert \gamma(t) - \gamma(t_0) \rVert} \cdot \frac{\lVert \gamma(t) - \gamma(t_0) \rVert}{t - t_0} \\[6pt]
    &= \underbrace{\frac{f(\gamma(t)) - f(\gamma(t_0)) - Df(\gamma(t_0))(\gamma(t) - \gamma(t_0))}{\lVert \gamma(t) - \gamma(t_0) \rVert}}_{\mathclap{\footnotesize \to\, 0}\vphantom{\footnotesize \to\, 0}}
    \; \underbrace{\frac{\lVert \gamma(t) - \gamma(t_0) \rVert}{t - t_0}}_{\mathclap{\footnotesize \to\, \pm \lVert \gamma'(t_0) \rVert \ (\text{not } \pm\infty!)}\vphantom{\footnotesize \to\, \pm \lVert \gamma'(t_0) \rVert \ (\text{not } \pm\infty!)}} \\[30pt]
    &\qquad + \underbrace{Df(\gamma(t_0))}_{\mathclap{\footnotesize \begin{matrix}\text{constant} \\ \text{matrix}\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{constant} \\ \text{matrix}\end{matrix}}} \underbrace{\left( \frac{\gamma(t) - \gamma(t_0)}{t - t_0} \right)}_{\mathclap{\footnotesize \to\, \gamma'(t_0)}\vphantom{\footnotesize \to\, \gamma'(t_0)}}
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad \lim_{t \to t_0} \frac{g(t) - g(t_0)}{t - t_0} &= 0 + Df(\gamma(t_0))(\gamma'(t_0))
    = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\gamma(t_0)) & \cdots & \dfrac{\partial f}{\partial x^n}(\gamma(t_0)) \end{bmatrix} \begin{bmatrix} (\gamma^1)'(t_0) \\ \vdots \\ (\gamma^n)'(t_0) \end{bmatrix} \\[4pt]
    &= \frac{\partial f}{\partial x^1}(\gamma(t_0))\, (\gamma^1)'(t_0) + \dots + \frac{\partial f}{\partial x^n}(\gamma(t_0))\, (\gamma^n)'(t_0)
    \end{aligned}
    $$

    $\therefore$ &nbsp; $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ differentiable at $t = t_0$, &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a} = \gamma(t_0)$

    then $g = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$ differentiable at $t = t_0$ with

    $$
    g'(t_0) = (f \circ \gamma)'(t_0) = \sum_{i=1}^{n} \frac{\partial f}{\partial x^i}(\gamma(t_0))\, (\gamma^i)'(t_0) \tag*{$\square$}
    $$

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} t^2 \\ t^3 \end{bmatrix}, \qquad f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 x^2$

    $$
    \gamma'(t_0) = \begin{bmatrix} 2 t_0 \\ 3 t_0^2 \end{bmatrix}, \qquad
    Df(\vec{a}) = \begin{bmatrix} a^2 & a^1 \end{bmatrix} \qquad \leadsto \qquad Df(\underbrace{\gamma(t_0)}_{\mathclap{\footnotesize \vec{a}}\vphantom{\footnotesize \vec{a}}}) = \begin{bmatrix} t_0^3 & t_0^2 \end{bmatrix}
    $$

    $$
    \Longrightarrow \qquad g(t) = f \circ \gamma(t) = f\!\left( \begin{bmatrix} t^2 \\ t^3 \end{bmatrix} \right) = t^2 \cdot t^3 = t^5
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
def _(corollary, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix}, \qquad f\!\left( \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \right) = (x^2)^2 + (x^3)^2$

    $$
    \Longrightarrow \qquad f \circ \gamma(t) = 1 \qquad \Longrightarrow \qquad (f \circ \gamma)'(t) = 0
    $$

    $$
    \gamma'(t) = \begin{bmatrix} 1 \\ -\sin(t) \\ \cos(t) \end{bmatrix}, \qquad Df(\vec{a}) = \begin{bmatrix} 0 & 2 a^2 & 2 a^3 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad Df(\gamma(t))(\gamma'(t)) &= \begin{bmatrix} 0 & 2 \cos(t) & 2 \sin(t) \end{bmatrix} \begin{bmatrix} 1 \\ -\sin(t) \\ \cos(t) \end{bmatrix} \\
    &= 0 \cdot 1 + 2 \cos(t)(-\sin(t)) + 2 \sin(t) \cos(t) = 0
    \end{aligned}
    $$

    ### The gradient and level sets
    """
            ),
            corollary(
                r"""
    For $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, $\vec{\nabla} f(\vec{a})$ is perpendicular to the level set through $\vec{a}$.
    """,
                "Gradient and level sets",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; suppose $f(\vec{a}) = b$ and suppose $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ is differentiable at $t_0$ with $\gamma(t_0) = \vec{a}$ and $\mathrm{Im}(\gamma) \subset f^{-1}(b)$ &nbsp; (that is, ${f \circ \gamma(t) = b \ \ \forall\, t}$)

    $$
    \Longrightarrow \qquad \vec{\nabla} f(\vec{a}) \cdot \gamma'(t_0) = Df(\vec{a})(\gamma'(t_0)) = (f \circ \gamma)'(t_0) = 0
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### The chain rule for maps"""),
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ differentiable at $\vec{x} = \vec{a}$, &nbsp; $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$ differentiable at $\vec{y} = \vec{b} = f(\vec{a})$

    $\Longrightarrow$ &nbsp; $g \circ f : \mathbb{R}^n \longrightarrow \mathbb{R}^p$ differentiable at $\vec{x} = \vec{a}$ with

    $$
    \underbrace{D(g \circ f)(\vec{a})}_{\mathclap{\footnotesize \in \mathrm{Mat}(p \times n)}\vphantom{\footnotesize \in \mathrm{Mat}(p \times n)}} = \underbrace{Dg(f(\vec{a}))}_{\mathclap{\footnotesize \in \mathrm{Mat}(p \times m)}\vphantom{\footnotesize \in \mathrm{Mat}(p \times m)}} \qquad\; \underbrace{Df(\vec{a})}_{\mathclap{\footnotesize \in \mathrm{Mat}(m \times n)}\vphantom{\footnotesize \in \mathrm{Mat}(m \times n)}} \qquad (\text{matrix multiplication!})
    $$
    """,
                "Chain rule",
            ),
            mo.md(
                r"""
    **Proof.** Similar idea as the previous theorem

    $$
    \begin{aligned}
    &\frac{g \circ f(\vec{x}) - g \circ f(\vec{a}) - Dg(f(\vec{a}))\, Df(\vec{a})\, (\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \\[6pt]
    &\quad = \underbrace{\frac{g \circ f(\vec{x}) - g \circ f(\vec{a}) - Dg(f(\vec{a}))\big( f(\vec{x}) - f(\vec{a}) \big)}{\lVert f(\vec{x}) - f(\vec{a}) \rVert}}_{\mathclap{\footnotesize \to\, 0}\vphantom{\footnotesize \to\, 0}}
    \; \underbrace{\frac{\lVert f(\vec{x}) - f(\vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert}}_{\mathclap{\footnotesize \text{does not go to } +\infty}\vphantom{\footnotesize \text{does not go to } +\infty}} \\[30pt]
    &\qquad + Dg(f(\vec{a})) \underbrace{\left( \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} \right)}_{\mathclap{\footnotesize \to\, 0}\vphantom{\footnotesize \to\, 0}}
    \end{aligned}
    $$

    (“does not go to $+\infty$”: this needs some care… not here!)

    $\Longrightarrow$ &nbsp; $D(g \circ f)(\vec{a}) = Dg(f(\vec{a}))\, Df(\vec{a})$ defines a good affine approximation to $g \circ f$ at $\vec{a}$  <span class=qed>$\square$</span>

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \end{bmatrix}, \qquad g\!\left( \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \right) = (y^1)^2 - y^2$

    $$
    \Longrightarrow \qquad g \circ f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = g\!\left( \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \end{bmatrix} \right) = (x^1 x^2)^2 - (x^1 + x^2)
    $$

    $$
    Df(\vec{x}) = \begin{bmatrix} x^2 & x^1 \\ 1 & 1 \end{bmatrix}, \qquad Dg(\vec{y}) = \begin{bmatrix} 2 y^1 & -1 \end{bmatrix}
    $$

    $$
    \Longrightarrow \qquad Dg(f(\vec{x}))\, Df(\vec{x}) = \begin{bmatrix} 2 x^1 x^2 & -1 \end{bmatrix} \begin{bmatrix} x^2 & x^1 \\ 1 & 1 \end{bmatrix}
    = \begin{bmatrix} 2 x^1 (x^2)^2 - 1 & 2 (x^1)^2 x^2 - 1 \end{bmatrix}
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
