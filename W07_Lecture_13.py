import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 13 · Higher order derivatives", css_file="bs101.css")


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
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
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
    header("Lecture 13", "Week 07", "Lecture 13 · Higher order derivatives")
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
    def cross_axes(ax, xlim, ylim, x0, y0):
        """A bare pair of coordinate axes through the origin, starting at x0 and y0."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.axis("off")
        arrow(ax, (x0, 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, y0), (0, ylim[1]), "black", lw=0.9)

    def signed(value, digits=2):
        """A number as ' + 1.20' or ' - 1.20', for writing out sums."""
        v = round(value, digits) + 0.0
        return f"{'-' if v < 0 else '+'} {abs(v):.{digits}f}"

    return cross_axes, signed


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - chain rule for maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$

        $$
        D(g \circ f)(\vec{x}) = Dg(f(\vec{x})) \cdot Df(\vec{x})
        $$

    - $\leadsto$ &nbsp; assuming $f$ differentiable at $\vec{x} \in \mathbb{R}^n$, $g$ differentiable at $\vec{y} = f(\vec{x}) \in \mathbb{R}^m$

    **In this lecture:** higher order derivatives

    **References:** MT 3.1, 3.2
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""## II.8 &nbsp; Higher order derivatives"""),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is called **$C^2$-smooth** at $\vec{x} = \vec{a}$ if all partial derivatives $\dfrac{\partial f}{\partial x^i}(\vec{x})$ are well-defined around $\vec{x} = \vec{a}$, their partial derivatives $\dfrac{\partial}{\partial x^j} \dfrac{\partial f}{\partial x^i}(\vec{x})$ are also all well-defined around $\vec{x} = \vec{a}$, and are all continuous at $\vec{x} = \vec{a}$

    $$
    \frac{\partial}{\partial x^j} \frac{\partial f}{\partial x^i}(\vec{x}) = \frac{\partial^2 f}{\partial x^j \partial x^i}(\vec{x}) \qquad (\text{second order partial derivative of } f \text{ with respect to } x^i \text{ and } x^j)
    $$
    """,
                r"$C^2$-smooth functions",
            ),
            mo.md(
                r"""
    **Remark.** By definition: $f$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $\Longrightarrow$ &nbsp; $f$ $C^1$-smooth at $\vec{x} = \vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $f$ differentiable at $\vec{x} = \vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $f$ continuous at $\vec{x} = \vec{a}$

    (opposite directions are NOT true!)
    """
            ),
            definition(
                r"""
    For $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $$
    Hf(\vec{a}) = \begin{bmatrix}
    \dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) & \dfrac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^1 \partial x^n}(\vec{a}) \\[10pt]
    \dfrac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{a}) & \dfrac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^2 \partial x^n}(\vec{a}) \\
    \vdots & \vdots & \ddots & \vdots \\
    \dfrac{\partial^2 f}{\partial x^n \partial x^1}(\vec{a}) & \dfrac{\partial^2 f}{\partial x^n \partial x^2}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^n \partial x^n}(\vec{a})
    \end{bmatrix} \in \mathrm{Mat}(n \times n)
    $$

    is called the **Hessian matrix** of $f$ at $\vec{x} = \vec{a}$.
    """,
                "Hessian matrix",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$ generalizes $f'(a)$, &nbsp; $Hf(\vec{a}) \in \mathrm{Mat}(n \times n)$ generalizes $f''(a)$

    **Remark.** $f$ $C^2$-smooth at $\vec{x} = \vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{\nabla} f$ $C^1$-smooth at $\vec{x} = \vec{a}$

    $$
    \leadsto \qquad Hf(\vec{a}) = D(\vec{\nabla} f)(\vec{a}) \qquad (\text{Hessian is the derivative of the gradient!})
    $$
    """
            ),
            theorem(
                r"""
    $f$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $$
    \Longrightarrow \qquad \frac{\partial^2 f}{\partial x^j \partial x^i}(\vec{a}) = \frac{\partial^2 f}{\partial x^i \partial x^j}(\vec{a}) \qquad \forall\, i, j = 1, \dots, n
    $$

    (order of partial derivative does not matter!)
    """,
                "Symmetry of second order partial derivatives",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$

    $$
    \frac{\partial f}{\partial x^1}(\vec{x}) = e^{x^2}, \qquad \frac{\partial f}{\partial x^2}(\vec{x}) = x^1 e^{x^2}
    \qquad \leadsto \qquad \vec{\nabla} f(\vec{x}) = \begin{bmatrix} e^{x^2} \\ x^1 e^{x^2} \end{bmatrix} \in \mathbb{R}^2
    \qquad \Longrightarrow \qquad \vec{\nabla} f : \mathbb{R}^2 \longrightarrow \mathbb{R}^2
    $$

    $$
    \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{x}) = 0, \qquad
    \frac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{x}) = e^{x^2}, \qquad
    \frac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{x}) = e^{x^2}, \qquad
    \frac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{x}) = x^1 e^{x^2}
    $$

    $$
    \leadsto \quad Hf(\vec{x}) = \begin{bmatrix} 0 & e^{x^2} \\ e^{x^2} & x^1 e^{x^2} \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    \qquad \leadsto \quad D(\vec{\nabla} f)(\vec{x}) = \begin{bmatrix}
    \dfrac{\partial}{\partial x^1}\big( e^{x^2} \big) & \dfrac{\partial}{\partial x^2}\big( e^{x^2} \big) \\[10pt]
    \dfrac{\partial}{\partial x^1}\big( x^1 e^{x^2} \big) & \dfrac{\partial}{\partial x^2}\big( x^1 e^{x^2} \big)
    \end{bmatrix}
    $$

    ### Quadratic approximation

    **Recall:** $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{x} = \vec{a}$

    $$
    \Longrightarrow \qquad f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \qquad \text{affine approximation of } f \text{ at } \vec{a} \quad (\text{1st order Taylor approximation})
    $$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ $C^2$-smooth at $\vec{x} = \vec{a}$

    $$
    f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})
    $$

    is the **quadratic approximation** of $f$ at $\vec{a}$ &nbsp; (2nd order Taylor approximation)
    """,
                "Quadratic approximation",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_taylor = mo.ui.slider(-1.5, 1.5, 0.1, value=0.5, label="$a$", show_value=True)
    return (a_taylor,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, RED, a_taylor, cross_axes, math, mo, np, signed, table):
    _a = a_taylor.value
    _fa = math.exp(_a)
    _x = np.linspace(-2.6, 2.6, 300)

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-2.6, 2.8), (-0.85, 5.2), -2.6, -0.25)
    _ax.plot(_x, np.full_like(_x, _fa), color=GREY, lw=1.2, ls=(0, (4, 3)))
    _ax.plot(_x, _fa + _fa * (_x - _a), color=RED, lw=1.4)
    _ax.plot(_x, _fa + _fa * (_x - _a) + 0.5 * _fa * (_x - _a) ** 2, color=GREEN, lw=1.4)
    _ax.plot(_x, np.exp(_x), color=BLUE, lw=1.6)
    _ax.plot(_a, _fa, "o", color="black", ms=4, zorder=4)
    _ax.plot([_a, _a], [-0.08, 0.08], color="black", lw=0.9)
    _ax.text(_a, -0.55, "$a$", ha="center", va="center", fontsize=13)

    _da = rf"(x {signed(-_a, 1)})"
    mo.vstack(
        [
            mo.hstack([a_taylor], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$y = f(x)$", rf"$\textcolor{{{BLUE}}}{{y = e^x}}$"),
                    (r"$y = f(a)$", rf"$\textcolor{{{GREY}}}{{y = {_fa:.3f}}}$"),
                    (r"$y = f(a) + f'(a)(x - a)$", rf"$\textcolor{{{RED}}}{{y = {_fa:.3f} + {_fa:.3f}\,{_da}}}$"),
                    (r"$y = f(a) + f'(a)(x - a) + \frac{1}{2} f''(a)(x - a)^2$", rf"$\textcolor{{{GREEN}}}{{y = {_fa:.3f} + {_fa:.3f}\,{_da} + {_fa / 2:.3f}\,{_da}^2}}$"),
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
            theorem(
                r"""
    If $f$ is $C^2$-smooth at $\vec{a}$, then its 2nd order Taylor approximation at $\vec{a}$ is a good approximation

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) - \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert^2} = 0
    $$

    (error goes to zero faster than $(\text{distance})^2$)
    """,
                "2nd order Taylor approximation",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}$ at $\vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$

    $$
    \leadsto \qquad f(\vec{a}) = 1, \qquad Df(\vec{a}) = \begin{bmatrix} 1 & 1 \end{bmatrix}, \qquad Hf(\vec{a}) = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad g(\vec{x}) &= 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} + \frac{1}{2} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} \cdot \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 - 0 \end{bmatrix} \\[4pt]
    &= 1 + (x^1 - 1) + x^2 + \frac{1}{2} (x^1 - 1) x^2 + \frac{1}{2} x^2 (x^1 - 1 + x^2)
    = 0 + x^1 + x^1 x^2 + \frac{1}{2} (x^2)^2
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    qx1 = mo.ui.slider(0, 2, 0.05, value=1.1, label="$x^1$", show_value=True)
    qx2 = mo.ui.slider(-1, 1, 0.05, value=-0.1, label="$x^2$", show_value=True)
    return qx1, qx2


@app.cell(hide_code=True)
def _(math, mo, qx1, qx2, table):
    _x1, _x2 = qx1.value, qx2.value
    _f = _x1 * math.exp(_x2)
    _g1 = 1 + (_x1 - 1) + _x2
    _g2 = _x1 + _x1 * _x2 + 0.5 * _x2**2
    mo.vstack(
        [
            mo.hstack([qx1, qx2], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(\vec{x}) = x^1 e^{x^2}$", rf"${_f:.4f}$"),
                    (r"1st order Taylor approximation $1 + (x^1 - 1) + x^2$", rf"${_g1 + 0.0:.4f}$"),
                    (r"error of the 1st order Taylor approximation", rf"${_f - _g1 + 0.0:.4f}$"),
                    (r"2nd order Taylor approximation $g(\vec{x}) = x^1 + x^1 x^2 + \frac{1}{2} (x^2)^2$", rf"${_g2 + 0.0:.4f}$"),
                    (r"error of the 2nd order Taylor approximation", rf"${_f - _g2 + 0.0:.4f}$"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** From Taylor approximation in single variable calculus

    $$
    e^t = 1 + t + \frac{1}{2} t^2 + \cdots \quad (\text{near } t = 0)
    \qquad \Longrightarrow \qquad x^1 e^{x^2} = x^1 \left( 1 + x^2 + \frac{1}{2} (x^2)^2 + \cdots \right)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $f$ is $C^2$-smooth at $\vec{a}$ when its second order partial derivatives are well-defined around $\vec{a}$ and continuous at $\vec{a}$; then their order does not matter
    - the Hessian matrix $Hf(\vec{a}) = D(\vec{\nabla} f)(\vec{a}) \in \mathrm{Mat}(n \times n)$ generalizes $f''(a)$
    - quadratic approximation:

        $$
        f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})
        $$

        with error going to zero faster than $\lVert \vec{x} - \vec{a} \rVert^2$

    **Next:** local extrema and the second derivative test
    """)
    return


if __name__ == "__main__":
    app.run()
