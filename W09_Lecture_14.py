import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 14 · Local maxima and minima of scalar valued functions", css_file="bs101.css")


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
    header("Lecture 14", "Week 09", "Lecture 14 · Local maxima and minima of scalar valued functions")
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

    - $f$ is $C^2$-smooth at $\vec{a}$ when its second order partial derivatives are well-defined around $\vec{a}$ and continuous at $\vec{a}$; then their order does not matter
    - the Hessian matrix $Hf(\vec{a}) = D(\vec{\nabla} f)(\vec{a}) \in \mathrm{Mat}(n \times n)$ generalizes $f''(a)$
    - quadratic approximation: $f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})$, with error going to zero faster than $\lVert \vec{x} - \vec{a} \rVert^2$

    **In this lecture:** local maxima and minima of scalar valued functions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## III.1 &nbsp; Local maxima and minima of scalar valued functions

    **Recall:** if $f : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable and has a local maximum at $x = a$ (or local minimum)

    $$
    \Longrightarrow \quad f'(a) = 0 \qquad \left( \text{tangent line to } \mathrm{graph}(f) \text{ is horizontal at } \begin{bmatrix} a \\ f(a) \end{bmatrix} \right)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    a_ext = mo.ui.slider(-0.4, 4.6, 0.05, value=0.5, label="$a$", show_value=True)
    return (a_ext,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, a_ext, cross_axes, math, mo, np, signed, table):
    def _f(x):
        return 1.3 + np.sin(1.9 * x - 0.4) + 0.12 * x

    _a = a_ext.value
    _fa = float(_f(_a))
    _d1 = 1.9 * math.cos(1.9 * _a - 0.4) + 0.12
    _d2 = -(1.9**2) * math.sin(1.9 * _a - 0.4)

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _ax = _fig.subplots()
    cross_axes(_ax, (-1.3, 6.8), (-0.55, 3.5), -1.3, -0.15)
    _ax.set_aspect("equal")
    _x = np.linspace(-0.7, 5.75, 400)
    _ax.plot(_x, _f(_x), color=BLUE, lw=1.6)
    _ax.text(5.83, float(_f(5.75)), "$y = f(x)$", color=BLUE, fontsize=13, ha="left", va="center")
    # horizontal tangent lines at the local maxima and minima
    _c = math.acos(-0.12 / 1.9)
    for _u in (_c, 2 * math.pi - _c, 2 * math.pi + _c):
        _xc = (_u + 0.4) / 1.9
        _ax.plot([_xc - 0.6, _xc + 0.6], [float(_f(_xc))] * 2, color=GREY, lw=1.0, ls=(0, (4, 3)))
    # the tangent line at a: a segment of fixed length
    _s = 0.9 / math.hypot(1, _d1)
    _ax.plot([_a - _s, _a + _s], [_fa - _d1 * _s, _fa + _d1 * _s], color=GREEN, lw=1.4)
    _ax.plot(_a, _fa, "o", color="black", ms=4, zorder=4)
    _ax.plot([_a, _a], [-0.06, 0.06], color="black", lw=0.9)
    _ax.text(_a, -0.34, "$a$", ha="center", va="center", fontsize=13)

    mo.vstack(
        [
            mo.hstack([a_ext], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f'(a)$", rf"${_d1 + 0.0:.2f}$"),
                    (r"$f''(a)$", rf"${_d2 + 0.0:.2f}$"),
                    (r"tangent line $y = f(a) + f'(a)(x - a)$", rf"$\textcolor{{{GREEN}}}{{y = {_fa:.2f} {signed(_d1)}\,(x {signed(-_a)})}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    Moreover, if $f' : \mathbb{R} \longrightarrow \mathbb{R}$ is also differentiable then, at a local maximum $x = a$, $f''(a) \leq 0$

    Conversely, if $f'(a) = 0$ and $f''(a) < 0$ &nbsp; $\Longrightarrow$ &nbsp; $f'(x)$ is strictly decreasing nearby $x = a$ &nbsp; $\Longrightarrow$ &nbsp; $x = a$ is a local maximum

    $\leadsto$ &nbsp; to discuss local maxima / minima of multivariable functions we need higher order derivatives

    ### Local extrema, critical points, 2nd derivative test
    """
            ),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$, a point $\vec{a} \in \mathbb{R}^n$ is

    - **local maximum** of $f$ if there is an open ball $B$ around $\vec{a}$ such that $f(\vec{x}) \leq f(\vec{a}) \quad \forall\, \vec{x} \in B$
    - **local minimum** of $f$ if there is an open ball $B$ around $\vec{a}$ such that $f(\vec{x}) \geq f(\vec{a}) \quad \forall\, \vec{x} \in B$

    (local: only around nearby points)
    """,
                "Local maximum and local minimum",
            ),
            theorem(
                r"""
    $f$ differentiable and has local maximum (minimum) at $\vec{x} = \vec{a}$

    $\Longrightarrow$ &nbsp; $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the zero linear map &nbsp; ($Df(\vec{a})(\vec{v}) = 0$)

    $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a}) = \vec{0} \in \mathbb{R}^n$
    """,
                "Derivative at a local extremum",
            ),
            mo.md(
                r"""
    **Proof.** For any $\vec{v} \in \mathbb{R}^n$, let $\gamma(t) = \vec{a} + t\vec{v}$ and $g(t) = f \circ \gamma(t)$

    $\vec{a}$ is local maximum of $f$ &nbsp; $\Longrightarrow$ &nbsp; $0$ is local maximum of $g$ &nbsp; $\forall\, \vec{v}$

    $$
    0 = g'(0) = (f \circ \gamma)'(0) = Df(\gamma(0))(\gamma'(0)) = Df(\vec{a})(\vec{v})
    \quad \Longrightarrow \quad Df(\vec{a})(\vec{v}) = 0 \quad \forall\, \vec{v} \in \mathbb{R}^n \qquad \square
    $$
    """
            ),
            definition(
                r"""
    If $\vec{\nabla} f(\vec{a}) = \vec{0}$ we call $\vec{a}$ a **critical point** of $f$.
    """,
                "Critical point",
            ),
            mo.md(
                r"""
    **Remark.** $f$ differentiable, $\vec{a}$ local extremum &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is critical point

    $\leadsto$ &nbsp; strategy to find maxima / minima is to find critical points and decide if they are local maxima or local minima (there are also critical points that are not local extrema!)
    """
            ),
            definition(
                r"""
    A critical point that is not a local extremum is called a **saddle point**.
    """,
                "Saddle point",
            ),
            theorem(
                r"""
    If $f$ is $C^2$-smooth at a critical point $\vec{a}$, let $H = Hf(\vec{a}) \in \mathrm{Mat}(n \times n)$ be the Hessian matrix, then

    - $\vec{a}$ is a local maximum if

        $$
        \vec{v} \cdot H\vec{v} < 0 \qquad \forall\, \vec{v} \in \mathbb{R}^n \setminus \{\vec{0}\}
        $$

    - $\vec{a}$ is a local minimum if

        $$
        \vec{v} \cdot H\vec{v} > 0 \qquad \forall\, \vec{v} \in \mathbb{R}^n \setminus \{\vec{0}\}
        $$

    - $\vec{a}$ is a saddle point if

        $$
        \vec{u} \cdot H\vec{u} < 0, \quad \vec{v} \cdot H\vec{v} > 0 \qquad \text{for some } \vec{u}, \vec{v} \in \mathbb{R}^n
        $$
    """,
                "2nd derivative test",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $f$ differentiable with a local extremum at $\vec{a}$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is a critical point: $\vec{\nabla} f(\vec{a}) = \vec{0}$; a critical point that is not a local extremum is a saddle point
    - 2nd derivative test at a critical point, with $H = Hf(\vec{a})$: local maximum if $\vec{v} \cdot H\vec{v} < 0$ for all $\vec{v} \neq \vec{0}$, local minimum if $\vec{v} \cdot H\vec{v} > 0$ for all $\vec{v} \neq \vec{0}$, saddle point if both signs occur

    **Next:** to be announced
    """)
    return


if __name__ == "__main__":
    app.run()
