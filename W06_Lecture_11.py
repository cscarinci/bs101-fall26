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
    header("Lecture 11", "Week 06", "Lecture 11 · Affine approximations and the derivative of general maps")
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
def _(arrow, math):
    # ---- Helpers of this lecture ----------------------------------------
    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr."""
        arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    def tip_label(ax, at, angle, text, color, r=7, fontsize=13):
        """Label next to the point `at`, pushed away from it in the direction `angle` (degrees);
        the text is anchored on the side facing the point, so that long labels never run back over it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ha = "left" if c > 0.35 else "right" if c < -0.35 else "center"
        va = "bottom" if s > 0.35 else "top" if s < -0.35 else "center"
        ax.annotate(text, at, textcoords="offset points", xytext=(r * c, r * s), ha=ha, va=va, color=color, fontsize=fontsize, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    def num(v, digits=2):
        """Fixed-point number for the readout tables (never prints a negative zero)."""
        return f"{round(v, digits) + 0.0:.{digits}f}"

    return cross_axes, num, tip_label


@app.cell(hide_code=True)
def _(mo):
    phi = mo.ui.slider(0, 355, 5, value=40, label=r"position of $\vec{a}$ on the ellipse (degrees)", show_value=True)
    return (phi,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, arrow, blank, cross_axes, math, mo, np, num, phi, table, tip_label):
    _p = math.radians(phi.value)
    _a = (3 * math.cos(_p), 2 * math.sin(_p))
    _grad = (2 * _a[0] / 9, 2 * _a[1] / 4)
    _tip = (_a[0] + _grad[0], _a[1] + _grad[1])
    _dir = math.degrees(math.atan2(_grad[1], _grad[0]))

    _fig, _ax = blank(FULL, 5.5, (-4.75, 5.0), (-3.55, 3.7))
    cross_axes(_ax, (-4.5, 4.9), (-3.4, 3.6), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(3 * np.cos(_th), 2 * np.sin(_th), color=BLUE, lw=1.4)
    _q = _p + math.pi + 0.6  # the name of the level set sits on the ellipse, away from a and its gradient
    tip_label(_ax, (3 * math.cos(_q), 2 * math.sin(_q)), math.degrees(math.atan2(math.sin(_q) / 2, math.cos(_q) / 3)), "$f^{-1}(r^2)$", BLUE)
    arrow(_ax, (0, 0), _a, "black")
    tip_label(_ax, (_a[0] / 2, _a[1] / 2), math.degrees(_p) + 90, r"$\vec{a}$", "black")
    arrow(_ax, _a, _tip, GREEN)
    tip_label(_ax, _tip, _dir + 40, r"$\vec{\nabla} f(\vec{a})$", GREEN)
    _ax.plot(*_a, "o", color="black", ms=4, zorder=4)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    The derivative and the gradient

    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$ &nbsp; $\Longleftrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} \frac{\partial f}{\partial x^1}(\vec{a}) & \cdots & \frac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)$ defines a good affine approximation for $f$ at $\vec{a}$ in the sense that

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

    - $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the **derivative** of $f$ at $\vec{a}$ (linear function taking vectors to directional derivatives)
    - $\vec{\nabla} f(\vec{a}) \in \mathbb{R}^n$, the column of the partial derivatives $\frac{\partial f}{\partial x^1}(\vec{a}), \dots, \frac{\partial f}{\partial x^n}(\vec{a})$, is the **gradient** of $f$ at $\vec{a}$ (vector pointing in some direction with some length)
    - theorem: $\vec{\nabla} f(\vec{a})$ (if not $\vec{0}$) points in the direction of steepest ascent of $f$ at $\vec{a}$, and it is perpendicular to the level set of $f$ through $\vec{a}$ (containing $\vec{a}$)
    - example: $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \dfrac{(x^1)^2}{9} + \dfrac{(x^2)^2}{4}$ &nbsp; $\leadsto$ &nbsp; level sets and gradient

        $$
        f^{-1}(r^2) = \underbrace{\left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; \frac{(x^1)^2}{9 r^2} + \frac{(x^2)^2}{4 r^2} = 1 \,\right\}}_{\text{horizontal ellipse centered at } \vec{0} \text{ with semi-axes } 3r \text{ and } 2r} \quad (r > 0),
        \qquad
        \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \frac{2}{9} a^1 \\[4pt] \frac{2}{4} a^2 \end{bmatrix}
        $$
    """
            ),
            mo.hstack([phi], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"semi-axes $3r$ and $2r$ of the level set $\textcolor{" + BLUE + r"}{f^{-1}(r^2)}$, with $r = 1$", r"$3$ and $2$"),
                    (r"$\vec{a}$", rf"$\begin{{bmatrix}} {num(_a[0])} \\ {num(_a[1])} \end{{bmatrix}}$"),
                    (r"$\vec{\nabla} f(\vec{a})$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {num(_grad[0])} \\ {num(_grad[1])} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
            mo.md(
                r"""
    **In this lecture:** affine approximations and their graphs; derivative for general maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$

    **References:** MT 2.3
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.6 &nbsp; Affine approximations and the derivative of general maps

    ### Affine approximations
    """
            ),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, the **affine approximation** of $f$ at $\vec{a}$ is the affine function (linear plus constant) $g : \mathbb{R}^n \longrightarrow \mathbb{R}$

    $$
    g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})
    = f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \dots + \frac{\partial f}{\partial x^n}(\vec{a})\, (x^n - a^n)
    $$
    """,
                "Affine approximation",
            ),
            mo.md(
                r"""
    **Remark.** For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $g : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    g(x) = f(a) + f'(a)(x - a)
    $$

    is the affine function whose graph is the tangent line to the graph of $f$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$

    $$
    y = f(a) + f'(a)(x - a) \qquad \leadsto \qquad \begin{bmatrix} a \\ f(a) \end{bmatrix} + (x - a) \underbrace{\begin{bmatrix} 1 \\ f'(a) \end{bmatrix}}_{\substack{\text{velocity vector of} \\ \text{the tangent line}}}
    \qquad \qquad
    \underbrace{\vec{n} = \begin{bmatrix} -f'(a) \\ 1 \end{bmatrix}}_{\substack{\text{normal to the} \\ \text{tangent line}}}
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
def _(BLUE, FULL, GREEN, ORANGE, a_line, arrow, blank, cross_axes, math, mo, np, num, table, tip_label):
    _a = a_line.value
    _fa = 4 * _a * math.exp(-_a)
    _d = 4 * (1 - _a) * math.exp(-_a)
    _slope = math.degrees(math.atan2(_d, 1))

    _fig, _ax = blank(FULL, 3.4, (-1.75, 6.25), (-0.6, 3.1))
    cross_axes(_ax, (-1.7, 6.2), (-0.5, 3.0), "$x$", "$y$")
    _x = np.linspace(-0.1, 5.1, 300)
    _ax.plot(_x, 4 * _x * np.exp(-_x), color=BLUE, lw=1.4)
    _ax.text(5.2, 0.34, "$y = f(x)$", color=BLUE, fontsize=13, ha="left", va="center")
    # the tangent line, as far as it stays inside the frame
    _s = np.linspace(-1.7, 5.2, 400)
    _t = _fa + _d * (_s - _a)
    _in = (_t > -0.5) & (_t < 3.0)
    _ax.plot(_s[_in], _t[_in], color=GREEN, lw=1.0)
    arrow(_ax, (0, 0), (_a, _fa), "black")
    arrow(_ax, (_a, _fa), (_a + 1, _fa + _d), GREEN)
    arrow(_ax, (_a, _fa), (_a - _d, _fa + 1), ORANGE)
    _nx = _a - _d  # the label of the normal steps aside when its tip comes close to the y-axis
    tip_label(_ax, (_nx, _fa + 1), _slope + 90 + (-70 if -0.05 < _nx < 0.5 else 70 if -0.5 < _nx <= -0.05 else 0), r"$\vec{n}$", ORANGE)
    _ax.plot(_a, _fa, "o", color="black", ms=4, zorder=4)
    # the label of the point sits in the wedge between the velocity vector and the normal, which nothing else enters
    _w = math.radians(_slope + (45 if _a >= 0.7 else 30))
    _ax.annotate(r"$\genfrac{[}{]}{0}{0}{a}{f(a)}$", (_a, _fa), textcoords="offset points", xytext=(38 * math.cos(_w), 38 * math.sin(_w)), ha="center", va="center", fontsize=13)

    mo.vstack(
        [
            mo.hstack([a_line], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(x) = 4x\,e^{-x}$ at $x = a$: &nbsp; $f(a)$", rf"${num(_fa)}$"),
                    (r"$f'(a)$", rf"${num(_d)}$"),
                    (r"velocity vector of the tangent line $\begin{bmatrix} 1 \\ f'(a) \end{bmatrix}$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} 1 \\ {num(_d)} \end{{bmatrix}}}}$"),
                    (r"normal to the tangent line $\vec{n} = \begin{bmatrix} -f'(a) \\ 1 \end{bmatrix}$", rf"$\textcolor{{{ORANGE}}}{{\begin{{bmatrix}} {num(-_d)} \\ 1 \end{{bmatrix}}}}$"),
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
            mo.md(r"""### The tangent plane"""),
            theorem(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

    The graph of the affine approximation of $f$ at $\vec{a}$ is a plane in $\mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R}$ through $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$ with normal vector

    $$
    \vec{n} = \begin{bmatrix} -\dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] -\dfrac{\partial f}{\partial x^2}(\vec{a}) \\[8pt] 1 \end{bmatrix}
    $$

    $\leadsto$ &nbsp; the **tangent plane** to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$
    """,
                "Tangent plane",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    \mathrm{graph}(g) &= \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\} \\[6pt]
    &= \left\{\, \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \\ Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\} \\[6pt]
    &= \Bigg\{\, \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \underbrace{(x^1 - a^1)}_{t} \underbrace{\begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix}}_{\text{velocity vector}} + \underbrace{(x^2 - a^2)}_{s} \underbrace{\begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\text{velocity vector}} \;\Bigg|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\Bigg\}
    \end{aligned}
    $$

    $$
    \begin{gathered}
    \vec{n} = \begin{bmatrix} n^1 \\ n^2 \\ n^3 \end{bmatrix} \ \text{ such that } \
    \vec{n} \cdot \underbrace{\begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix}}_{\vec{u}} = 0 = \vec{n} \cdot \underbrace{\begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\vec{v}} \\[8pt]
    \leadsto \qquad \vec{n} = \vec{u} \times \vec{v} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 0 & \frac{\partial f}{\partial x^1}(\vec{a}) \\ 0 & 1 & \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} \qquad \square
    \end{gathered}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, LIGHT, ORANGE, arrow, blank, math, mo, np, tip_label):
    # graph(f) as a wireframe with its tangent plane at (a, f(a)), in orthographic projection
    _az, _el = math.radians(28), math.radians(32)

    def _pr(x1, x2, y):
        x1, x2, y = (np.asarray(v, dtype=float) for v in (x1, x2, y))
        return -x1 * math.sin(_az) + x2 * math.cos(_az), y * math.cos(_el) - (x1 * math.cos(_az) + x2 * math.sin(_az)) * math.sin(_el)

    def _pt(x1, x2, y):
        q = _pr(x1, x2, y)
        return float(q[0]), float(q[1])

    def _f(x1, x2):
        return 2.4 - 0.2 * ((x1 - 1.9) ** 2 + (x2 - 1.7) ** 2)

    _a = (1.5, 1.1)
    _d1, _d2 = -0.4 * (_a[0] - 1.9), -0.4 * (_a[1] - 1.7)
    _fa = float(_f(*_a))

    _fig, _ax = blank(FULL, 5.0, (-3.4, 4.6), (-2.3, 3.6))
    for _end, _name, _dir in (((3.9, 0, 0), "$x^1$", 200), ((0, 3.9, 0), "$x^2$", 0), ((0, 0, 3.7), "$y$", 90)):
        arrow(_ax, (0, 0), _pt(*_end), "black", lw=0.9)
        tip_label(_ax, _pt(*_end), _dir, _name, "black", r=5)
    # the point a in the (x^1, x^2)-plane, below the point of the graph
    _ax.plot(*_pr([_a[0], _a[0], 0], [0, _a[1], _a[1]], [0, 0, 0]), color=GREY, lw=0.9, ls=(0, (4, 3)))
    _ax.plot(*_pr([_a[0], _a[0]], [_a[1], _a[1]], [0, _fa]), color=GREY, lw=0.9, ls=(0, (4, 3)))
    _ax.plot(*_pt(_a[0], _a[1], 0), "o", color="black", ms=4)
    tip_label(_ax, _pt(_a[0], _a[1], 0), -60, r"$\vec{a}$", "black")
    # the surface: a few coordinate curves
    _lo, _hi = 0.5, 3.1
    _w = np.linspace(_lo, _hi, 40)
    for _c in np.linspace(_lo, _hi, 7):
        _lw = 1.2 if _c in (_lo, _hi) else 0.5
        _ax.plot(*_pr(_w, np.full(40, _c), _f(_w, _c)), color=BLUE, lw=_lw)
        _ax.plot(*_pr(np.full(40, _c), _w, _f(_c, _w)), color=BLUE, lw=_lw)
    # the tangent plane, spanned by the velocity vectors (1, 0, d1) and (0, 1, d2); it lies above the graph
    _k = 1.0
    _c1 = _a[0] + _k * np.array([-1, 1, 1, -1, -1])
    _c2 = _a[1] + _k * np.array([-1, -1, 1, 1, -1])
    _cy = _fa + _d1 * (_c1 - _a[0]) + _d2 * (_c2 - _a[1])
    _ax.fill(*_pr(_c1, _c2, _cy), facecolor=LIGHT, edgecolor=GREEN, lw=1.0, zorder=3)
    _p = _pt(_a[0], _a[1], _fa)
    arrow(_ax, _p, _pt(_a[0] + _k, _a[1], _fa + _k * _d1), GREEN, zorder=4)
    arrow(_ax, _p, _pt(_a[0], _a[1] + _k, _fa + _k * _d2), GREEN, zorder=4)
    _n = _pt(_a[0] - _d1, _a[1] - _d2, _fa + 1)
    arrow(_ax, _p, _n, ORANGE, zorder=4)
    tip_label(_ax, _n, 90, r"$\vec{n}$", ORANGE)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=5)
    _ax.annotate(r"$(a^1, a^2, f(\vec{a}))$", _p, xytext=(1.5, 3.1), color="black", fontsize=13, ha="left", va="center", arrowprops={"arrowstyle": "-", "color": GREY, "lw": 0.7, "shrinkB": 4})
    tip_label(_ax, _pt(_hi, 0.9, _f(_hi, 0.9)), 200, r"$y = f(\vec{x})$", BLUE)
    tip_label(_ax, _pt(_a[0] + _k, _a[1] - _k, _fa + _k * (_d1 - _d2)), 160, r"$y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$", GREEN)

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    $$
    y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \qquad \leadsto \qquad
    \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + (x^1 - a^1) \begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix} + (x^2 - a^2) \begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}, \quad \vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$

    $$
    \leadsto \qquad \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \frac{\partial f}{\partial x^1}(\vec{a}) \\[4pt] \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} e^{a^2} \\ a^1 e^{a^2} \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}
    \qquad \leadsto \qquad \vec{n} = \begin{bmatrix} -\frac{\partial f}{\partial x^1}(\vec{a}) \\[4pt] -\frac{\partial f}{\partial x^2}(\vec{a}) \\[4pt] 1 \end{bmatrix} = \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    & \leadsto \qquad \text{plane through } \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} \text{ normal to } \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix} \\
    & \phantom{\leadsto \qquad \text{plane }} = \left\{\, \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; -1 \cdot (y^1 - 1) - 1 \cdot (y^2 - 0) + 1 \cdot (y^3 - 1) = 0 \,\right\} \\
    & \phantom{\leadsto \qquad \text{plane }} = \left\{\, \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; y^3 = y^1 + y^2 \,\right\} = \mathrm{graph}(g)
    \end{aligned}
    $$

    $$
    \leadsto \qquad \text{affine approximation} \quad g(\vec{x}) = 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 \end{bmatrix} = 1 + (x^1 - 1) + x^2
    $$

    **Remark.**

    $$
    \vec{x} = \begin{bmatrix} 1.1 \\ -0.1 \end{bmatrix} \qquad \Longrightarrow \qquad
    \begin{aligned} f(\vec{x}) &= 1.1\, e^{-0.1} \approx 0.995 \\ g(\vec{x}) &= 1.1 - 0.1 = 1 \end{aligned}
    \qquad \Longrightarrow \qquad f(\vec{x}) - g(\vec{x}) \approx -0.005
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
def _(math, mo, num, px1, px2, table):
    _f = px1.value * math.exp(px2.value)
    _g = px1.value + px2.value
    mo.vstack(
        [
            mo.hstack([px1, px2], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(\vec{x}) = x^1 e^{x^2}$", rf"${num(_f, 4)}$"),
                    (r"$g(\vec{x}) = 1 + (x^1 - 1) + x^2$", rf"${num(_g, 4)}$"),
                    (r"$f(\vec{x}) - g(\vec{x})$", rf"${num(_f - _g, 4)}$"),
                ]
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
    ### The derivative of general maps

    **Remark.** &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \right) = \begin{bmatrix} f^1(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}$ &nbsp; with each $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ a scalar function on $\mathbb{R}^n$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ \vdots \\ a^n \end{bmatrix}$ if each component $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{a}$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} Df^1(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix}
    = \begin{bmatrix} \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f^1}{\partial x^n}(\vec{a}) \\ \vdots & \ddots & \vdots \\ \dfrac{\partial f^m}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f^m}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(m \times n)
    $$

    defines an affine approximation of $f$ at $\vec{a}$ in the sense

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{\overbrace{f(\vec{x})}^{\mathbb{R}^m} - \overbrace{f(\vec{a})}^{\mathbb{R}^m} - \overbrace{Df(\vec{a})}^{\mathrm{Mat}(m \times n)} \overbrace{(\vec{x} - \vec{a})}^{\mathbb{R}^n}}{\lVert \vec{x} - \vec{a} \rVert} = \vec{0} \in \mathbb{R}^m
    $$

    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$, the linear transformation $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called the **derivative** of $f$ at $\vec{a}$ or the **Jacobian matrix** of $f$ at $\vec{a}$, $Df(\vec{a}) \in \mathrm{Mat}(m \times n)$.
    """,
                "Differentiability and the Jacobian matrix",
            ),
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$ if and only if

    $$
    \lim_{\vec{x} \to \vec{a}} \underbrace{\frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert}}_{\text{scalar valued function on } \mathbb{R}^n} = 0
    $$

    $\leadsto$ &nbsp; we only need to compute 1 limit instead of $m$
    """,
                "Differentiability with a single limit",
            ),
            theorem(
                r"""
    If all components $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ of $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ have well-defined partial derivatives in an open ball centered at $\vec{a}$, and they are all continuous at $\vec{x} = \vec{a}$ ($f$ is $C^1$-smooth at $\vec{a}$), then $f$ is differentiable at $\vec{x} = \vec{a}$.
    """,
                r"$C^1$-smooth implies differentiable",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \underbrace{\begin{bmatrix} a & b \\ c & d \end{bmatrix}}_{A \,\in\, \mathrm{Mat}(2 \times 2)} \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \end{bmatrix} = \begin{bmatrix} f^1(\vec{x}) \\ f^2(\vec{x}) \end{bmatrix}
    $$

    $f^1(\vec{x})$, $f^2(\vec{x})$ are $C^1$-smooth everywhere in $\mathbb{R}^2$ (linear combination of elementary functions) &nbsp; $\Longrightarrow$ &nbsp; $f$ is differentiable at any $\vec{a} \in \mathbb{R}^2$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \dfrac{\partial f^1}{\partial x^2}(\vec{a}) \\[8pt] \dfrac{\partial f^2}{\partial x^1}(\vec{a}) & \dfrac{\partial f^2}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = A\,!
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 \cos(x^2) \\ x^1 \sin(x^2) \end{bmatrix}, \quad \vec{a} = \begin{bmatrix} 2 \\ \pi/3 \end{bmatrix}$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} \cos(a^2) & -a^1 \sin(a^2) \\ \sin(a^2) & a^1 \cos(a^2) \end{bmatrix} = \begin{bmatrix} \frac{\sqrt{1}}{2} & -\sqrt{3} \\[4pt] \frac{\sqrt{3}}{2} & \sqrt{1} \end{bmatrix}
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
def _(Arc, BLUE, FULL, Figure, GREEN, GREY, RED, arrow, cross_axes, math, mo, num, pa1, pk, table, tip_label):
    _a1, _a2 = pa1.value, pk.value * math.pi / 12
    _c, _s = math.cos(_a2), math.sin(_a2)
    _fa = (_a1 * _c, _a1 * _s)
    _deg = math.degrees(_a2)
    _dash = (0, (4, 3))

    # both panels are drawn at the same scale
    _fig = Figure(figsize=(FULL, 3.75), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[5.6, 12.6])
    for _ax, _xlim in ((_left, (-0.8, 4.8)), (_right, (-6.3, 6.3))):
        _ax.set_xlim(*_xlim)
        _ax.set_ylim(-3.5, 5.3)
        _ax.set_aspect("equal")
        _ax.axis("off")

    cross_axes(_left, (-0.6, 4.7), (-0.6, 5.2), "$x^1$", "$x^2$")
    _left.plot([_a1, _a1, 0], [0, _a2, _a2], color=GREY, lw=0.9, ls=_dash)
    arrow(_left, (0, 0), (_a1, _a2), "black")
    arrow(_left, (_a1, _a2), (_a1 + 1, _a2), BLUE)
    arrow(_left, (_a1, _a2), (_a1, _a2 + 1), RED)
    tip_label(_left, (_a1 + 1, _a2), 0, r"$\vec{e}_1$", BLUE)
    tip_label(_left, (_a1, _a2 + 1), 90, r"$\vec{e}_2$", RED)
    _left.plot(_a1, _a2, "o", color="black", ms=4, zorder=4)
    tip_label(_left, (_a1, _a2), -45, r"$\vec{a}$", "black")

    cross_axes(_right, (-6.2, 6.2), (-3.4, 5.2), "$y^1$", "$y^2$")
    _right.plot([_fa[0], _fa[0], 0], [0, _fa[1], _fa[1]], color=GREY, lw=0.9, ls=_dash)
    if _deg > 0:
        _right.add_patch(Arc((0, 0), 0.8, 0.8, theta1=0, theta2=_deg, color=GREEN, lw=1.4))
    arrow(_right, (0, 0), _fa, "black")
    _t1 = (_fa[0] + _c, _fa[1] + _s)
    _t2 = (_fa[0] - _a1 * _s, _fa[1] + _a1 * _c)
    arrow(_right, _fa, _t1, BLUE)
    arrow(_right, _fa, _t2, RED)
    tip_label(_right, _t1, _deg, r"$Df(\vec{a})(\vec{e}_1)$", BLUE, fontsize=12)
    tip_label(_right, _t2, _deg + 90, r"$Df(\vec{a})(\vec{e}_2)$", RED, fontsize=12)
    _right.plot(*_fa, "o", color="black", ms=4, zorder=4)
    tip_label(_right, _fa, _deg - 90, r"$f(\vec{a})$", "black", fontsize=12)

    mo.vstack(
        [
            mo.hstack([pa1, pk], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{a}$", rf"$\begin{{bmatrix}} {num(_a1)} \\ {num(_a2)} \end{{bmatrix}}$"),
                    (r"angle $a^2$ of $f(\vec{a})$", rf"$\textcolor{{{GREEN}}}{{{pk.value}\,\pi/12}}$"),
                    (r"$f(\vec{a})$", rf"$\begin{{bmatrix}} {num(_fa[0])} \\ {num(_fa[1])} \end{{bmatrix}}$"),
                    (
                        r"$Df(\vec{a}) = \begin{bmatrix} Df(\vec{a})(\vec{e}_1) & Df(\vec{a})(\vec{e}_2) \end{bmatrix}$",
                        rf"$\begin{{bmatrix}} \textcolor{{{BLUE}}}{{{num(_c)}}} & \textcolor{{{RED}}}{{{num(-_a1 * _s)}}} \\ \textcolor{{{BLUE}}}{{{num(_s)}}} & \textcolor{{{RED}}}{{{num(_a1 * _c)}}} \end{{bmatrix}}$",
                    ),
                ]
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

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 x^2, \qquad \vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
    $$

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

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \\ (x^2)^2 \end{bmatrix}
    $$

    (a) Compute the derivative of $f$ at $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix}$.

    (b) Write the affine approximation of $f$ at $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$.

    (c) Write the affine approximation of $f$ at $\vec{b} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$.

    (d) How do the images of these approximations differ?
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - the affine approximation of $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ at $\vec{a}$ is

        $$
        g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})
        $$

        (linear plus constant)
    - $n = 1$: $\mathrm{graph}(g)$ is the tangent line to the graph of $f$

        $n = 2$: $\mathrm{graph}(g)$ is the tangent plane to $\mathrm{graph}(f)$, through $(a^1, a^2, f(\vec{a}))$ with normal vector

        $$
        \vec{n} = \Big( {-\frac{\partial f}{\partial x^1}(\vec{a})},\ {-\frac{\partial f}{\partial x^2}(\vec{a})},\ 1 \Big)
        $$
    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$ if each component $f^j$ is; the rows of the Jacobian matrix $Df(\vec{a}) \in \mathrm{Mat}(m \times n)$ are the derivatives $Df^j(\vec{a})$
    - $f$ is differentiable at $\vec{a}$ if and only if

        $$
        \frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert} \longrightarrow 0 \quad \text{as } \vec{x} \to \vec{a}
        $$

        $C^1$-smooth at $\vec{a}$ $\Longrightarrow$ differentiable at $\vec{a}$
    - a linear map $f(\vec{x}) = A\vec{x}$ has $Df(\vec{a}) = A$ at every $\vec{a}$

    **Next:** the chain rule
    """)
    return


if __name__ == "__main__":
    app.run()
