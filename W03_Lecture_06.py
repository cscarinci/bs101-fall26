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
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the particle, the point, the chosen vector)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (velocity, relative velocity, tangent vector)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (equator, light cone, inertial comparison)
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
    header("Lecture 06", "Week 03", "Lecture 06 · Multivariable functions")
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
def _(math, np):
    # ---- Drawing helpers of this lecture: line drawings of surfaces in R^3 ----
    # Orthographic view from elevation 22 degrees and azimuth 28 degrees (x^3 up).
    _e, _a = math.radians(22), math.radians(28)
    _sin, _cos, _tan = math.sin(_e), math.cos(_e), math.tan(_e)
    _right = np.array([-math.sin(_a), math.cos(_a), 0.0])
    _up = np.array([-_sin * math.cos(_a), -_sin * math.sin(_a), _cos])

    def ortho(p):
        """Picture coordinates of the point(s) p of R^3."""
        p = np.asarray(p, dtype=float)
        return p @ _right, p @ _up

    def ring(ax, r, z, color, slope=0.0, back=(0, (3, 3)), lw=1.0):
        """The circle of radius r at height z about the x^3-axis. `slope` is the rate at which the radius of the
        surface grows with height there; the arc on the far side of the surface gets the line style `back` (None: omitted)."""
        phi = np.linspace(-np.pi, np.pi, 361)
        h, v = r * np.sin(phi), z * _cos - r * np.cos(phi) * _sin
        near = np.cos(phi) >= slope * _tan
        ax.plot(np.where(near, h, np.nan), np.where(near, v, np.nan), color=color, lw=lw)
        if back is not None:
            ax.plot(np.where(~near, h, np.nan), np.where(~near, v, np.nan), color=color, lw=0.8 * lw, ls=back)

    def quadric(ax, b, zmax, color, wire=False, lw=1.4):
        """Line drawing of the level set (x^1)^2 + (x^2)^2 - (x^3)^2 = b for |x^3| <= zmax:
        outline, rims and waist; with `wire`, also a few circles and meridians on the visible side."""
        # outline: the points where the line of sight is tangent to the surface
        z0 = math.sqrt(max(-b, 0.0) / (1 - _tan**2))
        if z0 < zmax:
            for s in (1, -1):
                z = s * np.linspace(z0, zmax, 200)
                h = np.sqrt(np.maximum(b + z**2 * (1 - _tan**2), 0.0))
                for side in (1, -1):
                    ax.plot(side * h, z * (_cos - _sin * _tan), color=color, lw=lw)
        rim = math.sqrt(b + zmax**2)
        ring(ax, rim, zmax, color, back="-", lw=lw)
        ring(ax, rim, -zmax, color, slope=-zmax / rim, lw=lw)
        if b > 0:
            ring(ax, math.sqrt(b), 0.0, color, lw=lw)
        if wire:
            for z in (-2.0, -1.0, 1.0, 2.0):
                if b + z**2 > 0 and abs(z) < zmax:
                    r = math.sqrt(b + z**2)
                    ring(ax, r, z, color, slope=z / r, back=None, lw=0.6)
            for s in (1, -1):
                z = s * np.linspace(math.sqrt(max(-b, 0.0)) + 1e-9, zmax, 200)
                r = np.sqrt(b + z**2)
                for phi in np.radians(np.arange(-150, 181, 30)):
                    near = np.cos(phi) * r >= z * _tan
                    h, v = r * np.sin(phi), z * _cos - r * np.cos(phi) * _sin
                    ax.plot(np.where(near, h, np.nan), np.where(near, v, np.nan), color=color, lw=0.6)

    return ortho, quadric, ring


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    So far: Euclidean Geometry

    - $\leadsto$ &nbsp; vectors, lines, planes
    - $\leadsto$ &nbsp; dot products and cross-products (in $\mathbb{R}^3$): lengths, angles, areas, volumes

    **In this lecture:** multivariable functions &nbsp; $\leadsto$ &nbsp; objects of interest in Multivariable Calculus
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""## II.1 &nbsp; Multivariable functions"""),
            definition(
                r"""
    A **multivariable function** is a rule

    $$
    f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m
    $$

    that assigns to each element $\vec{x}$ in a set $A \subseteq \mathbb{R}^n$ a unique element $\vec{y} = f(\vec{x})$ in another set $B \subseteq \mathbb{R}^m$.
    """,
                "Multivariable function",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; there are 3 parts to a function

    $$
    \begin{aligned}
    \mathrm{Dom}(f) &= A = \text{set of allowed inputs} \\
    \mathrm{Codom}(f) &= B = \text{set of desired outputs} \\
    \vec{x} &\longmapsto f(\vec{x}) \quad \text{the rule of assignment}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; change any one of these and you have a different function!

    **Remark.** Sometimes we will call

    - $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}$ &nbsp; ($m = 1$) &nbsp; a **scalar function** on $\mathbb{R}^n$ (or scalar-valued function)
    - $f : A \subseteq \mathbb{R} \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; ($n = 1$) &nbsp; a **path** in $\mathbb{R}^m$
    - $f : A \subseteq \mathbb{R}^2 \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; ($n = 2$) &nbsp; a **parameterized surface** in $\mathbb{R}^m$
    - $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; a **map** from $A \subseteq \mathbb{R}^n$ to $B \subseteq \mathbb{R}^m$

    **Example.**

    - lengths

        $$
        \lVert \cdot \rVert : \mathbb{R}^n \longrightarrow \mathbb{R}, \qquad \vec{x} \longmapsto \sqrt{(x^1)^2 + (x^2)^2 + \dots + (x^n)^2}
        $$

    - affine parameterizations

        $$
        \begin{aligned}
        \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^3 \\
        \underbrace{t}_{\text{variable}} &\longmapsto \underbrace{\begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \\ x^3 + t v^3 \end{bmatrix}}_{\vec{x} \text{ and } \vec{v} \text{ fixed here}}
        \end{aligned}
        \qquad \qquad
        \begin{aligned}
        \varphi : \mathbb{R}^2 &\longrightarrow \mathbb{R}^3 \\
        \underbrace{(s, t)}_{\text{variables}} &\longmapsto \underbrace{\begin{bmatrix} x^1 + s u^1 + t v^1 \\ x^2 + s u^2 + t v^2 \\ x^3 + s u^3 + t v^3 \end{bmatrix}}_{\vec{x},\ \vec{u} \text{ and } \vec{v} \text{ fixed here!}}
        \end{aligned}
        $$

    - linear transformations

        $$
        \begin{aligned}
        T : \mathbb{R}^n &\longrightarrow \mathbb{R}^m \\
        \underbrace{\begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix}}_{\text{variables}} &\longmapsto \underbrace{\begin{bmatrix} t^1{}_1 x^1 + \dots + t^1{}_n x^n \\ \vdots \\ t^m{}_1 x^1 + \dots + t^m{}_n x^n \end{bmatrix}}_{t^i{}_j \text{ are fixed}}
        \end{aligned}
        $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Basic properties"""),
            definition(
                r"""
    Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$

    - the **image** of $f$ is

        $$
        \mathrm{Im}(f) = \left\{\, \vec{y} \in \mathbb{R}^m \;\middle|\; \exists\, \vec{x} \in A,\ f(\vec{x}) = \vec{y} \,\right\} \underbrace{\subseteq B}_{\text{not necessarily equal!}} \qquad \big(\mathrm{Im}(f) \subseteq \mathrm{Codom}(f)\big)
        $$

    - the **graph** of $f$ is

        $$
        \mathrm{graph}(f) = \left\{\, (\vec{x}, \vec{y}) \in \mathbb{R}^n \times \mathbb{R}^m \;\middle|\; \vec{x} \in A,\ \vec{y} = f(\vec{x}) \,\right\} \subseteq A \times B
        $$
    """,
                "Image and graph",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ affine parameterization, &nbsp; $\gamma(t) = \vec{x} + t\vec{v}$ &nbsp; (with $\vec{v} \neq \vec{0}$)

    $$
    \leadsto \quad \mathrm{Im}(\gamma) = \left\{\, \vec{y} \in \mathbb{R}^2 \;\middle|\; \exists\, t \in \mathbb{R},\ \vec{y} = \gamma(t) \,\right\} \qquad \text{line in } \mathbb{R}^2 \text{ through } \vec{x} \text{ in the direction of } \vec{v}
    $$

    $$
    \leadsto \quad \mathrm{graph}(\gamma) = \left\{\, (t, \vec{y}) \in \mathbb{R} \times \mathbb{R}^2 \;\middle|\; t \in \mathbb{R},\ \vec{y} = \gamma(t) \,\right\} \qquad \text{subset of } \mathbb{R} \times \mathbb{R}^2 \approx \mathbb{R}^3
    $$

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
def _(BLUE, FULL, GREEN, GREY, RED, arrow, blank, mo, t_path, table, vector):
    _x, _v, _t = (2.0, 2.0), (0.6, 0.2), t_path.value
    _g = (_x[0] + _t * _v[0], _x[1] + _t * _v[1])
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _side = 1 if _t >= 0 else -1  # the two tip labels stay on opposite sides, also when the tips coincide

    # the t-line, the map gamma, and Im(gamma): a line in R^2
    _fig, _ax = blank(FULL, 2.6, (-6.6, 5.6), (-0.7, 3.7))

    def _at(s):
        return -5.6 + 0.8 * (s + 1)

    arrow(_ax, (-6.2, 1.5), (-1.9, 1.5), "black", lw=0.9)
    _ax.text(-1.9, 1.32, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    _ax.plot(_at(0), 1.5, "o", color="black", ms=3.5)
    _ax.plot(_at(_t), 1.5, "o", color=BLUE, ms=3.5)
    _ax.text(_at(0), 1.32, "$0$", fontsize=12, ha="center", va="top")
    _ax.text(_at(_t), 1.68, "$t$", fontsize=13, ha="center", va="bottom", color=BLUE)
    arrow(_ax, (-1.55, 2.2), (-0.45, 2.2), "black", lw=0.9, connectionstyle="arc3,rad=-0.3")
    _ax.text(-1.0, 2.5, r"$\gamma$", fontsize=13, ha="center", va="bottom")

    arrow(_ax, (-0.4, 0), (4.8, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 3.5), "black", lw=0.9)
    _ax.text(4.8, -0.14, "$y^1$", fontsize=13, ha="right", va="top")
    _ax.text(-0.14, 3.5, "$y^2$", fontsize=13, ha="right", va="top")
    _ax.plot([_x[0] + s * _v[0] for s in (-1.5, 3.7)], [_x[1] + s * _v[1] for s in (-1.5, 3.7)], color="black", lw=1.2)
    _ax.text(_x[0] + 3.7 * _v[0] + 0.1, _x[1] + 3.7 * _v[1], r"$\mathrm{Im}(\gamma)$", fontsize=13, ha="left", va="center")
    vector(_ax, (0, 0), _v, GREEN, r"$\vec{v}$")
    arrow(_ax, (0, 0), _x, RED)
    arrow(_ax, (0, 0), _g, BLUE)
    _ax.plot(*_x, "o", color="black", ms=3.5, zorder=4)
    _ax.plot(*_g, "o", color="black", ms=3.5, zorder=4)
    _ax.annotate(r"$\vec{x} = \gamma(0)$", _x, textcoords="offset points", xytext=(-2, 19), ha="left", va="bottom", color=RED, fontsize=13, zorder=5, bbox=_box)
    _ax.annotate(r"$\gamma(t)$", _g, textcoords="offset points", xytext=(7, -5) if _t >= 0 else (-7, 3), ha="left" if _t >= 0 else "right", va="top" if _t >= 0 else "bottom", color=BLUE, fontsize=13, zorder=5, bbox=_box)

    # graph(gamma): a line in R x R^2, in the board's oblique view (t to the right, y^1 towards the viewer, y^2 up)
    def _pr(t, y1, y2):
        return 1.5 * t - 0.45 * y1, y2 - 0.4 * y1

    _fig2, _ax2 = blank(FULL, 4.2, (-3.9, 5.7), (-2.0, 3.3))
    for _s, _col, _cut in ((_t, GREY, 0.4), (0, "black", 0.0)):  # the (y^1, y^2)-plane over t (shorter axes), and over 0
        if _col == GREY and _t == 0:
            continue  # the two planes coincide
        arrow(_ax2, _pr(_s, -0.5, 0), _pr(_s, 4.2 - _cut, 0), _col, lw=0.9)
        arrow(_ax2, _pr(_s, 0, -0.5), _pr(_s, 0, 3.0 - _cut), _col, lw=0.9)
    arrow(_ax2, _pr(-1.4, 0, 0), _pr(3.6, 0, 0), "black", lw=0.9)
    _e1, _e2 = _pr(0, 4.2, 0), _pr(0, 0, 3.0)
    _ax2.text(_e1[0] + 0.12, _e1[1] - 0.05, "$y^1$", fontsize=13, ha="left", va="top")
    _ax2.text(_e2[0] - 0.12, _e2[1], "$y^2$", fontsize=13, ha="right", va="top")
    if _t != 0:
        _ax2.annotate("$0$", (0, 0), textcoords="offset points", xytext=(5, -5), ha="left", va="top", fontsize=12, zorder=5, bbox=_box)
    _ax2.annotate("$t$" if _t != 0 else "$t = 0$", _pr(_t, 0, 0), textcoords="offset points", xytext=(5, -5), ha="left", va="top", fontsize=13, color=BLUE, zorder=5, bbox=_box)
    _ends = [_pr(s, _x[0] + s * _v[0], _x[1] + s * _v[1]) for s in (-1.5, 3.7)]
    _ax2.plot([_ends[0][0], _ends[1][0]], [_ends[0][1], _ends[1][1]], color="black", lw=1.2)
    _ax2.text(_ends[1][0] + 0.1, _ends[1][1] - 0.08, r"$\mathrm{graph}(\gamma)$", fontsize=13, ha="left", va="top")
    _p0, _pt = _pr(0, *_x), _pr(_t, *_g)
    arrow(_ax2, (0, 0), _p0, RED)
    arrow(_ax2, _pr(_t, 0, 0), _pt, BLUE)
    _ax2.plot(*_p0, "o", color="black", ms=3.5, zorder=4)
    _ax2.plot(*_pt, "o", color="black", ms=3.5, zorder=4)
    _ax2.annotate(r"$(0, \vec{x})$", _p0, textcoords="offset points", xytext=(-6 * _side, 4), ha="right" if _side > 0 else "left", va="bottom", color=RED, fontsize=13, zorder=5, bbox=_box)
    _ax2.annotate(r"$(t, \gamma(t))$", _pt, textcoords="offset points", xytext=(6 * _side, 4), ha="left" if _side > 0 else "right", va="bottom", color=BLUE, fontsize=13, zorder=5, bbox=_box)

    mo.vstack(
        [
            mo.hstack([t_path], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{x} = \gamma(0)$", rf"$\textcolor{{{RED}}}{{\begin{{bmatrix}} {_x[0]:g} \\ {_x[1]:g} \end{{bmatrix}}}}$"),
                    (r"$\vec{v}$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_v[0]:g} \\ {_v[1]:g} \end{{bmatrix}}}}$"),
                    (r"$\gamma(t) = \vec{x} + t\vec{v}$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_g[0]:g} \\ {_g[1]:g} \end{{bmatrix}}}}$"),
                    (r"$(t, \gamma(t)) \in \mathrm{graph}(\gamma)$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_t:g} \\ {_g[0]:g} \\ {_g[1]:g} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
            _fig2,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, HALF, RED, arrow, blank, definition, mo, np, ortho, ring):
    # The sphere of radius 2: outline and equator (far half dashed), with the coordinate axes
    _fig, _ax = blank(HALF, 3.4, (-3.0, 3.6), (-2.8, 3.4))
    _th = np.linspace(0, 2 * np.pi, 361)
    for _d in np.eye(3):
        arrow(_ax, ortho(-0.9 * _d), ortho(3.2 * _d), "black", lw=0.9)
    _ax.plot(2 * np.cos(_th), 2 * np.sin(_th), color=BLUE, lw=1.4)
    ring(_ax, 2.0, 0.0, BLUE)
    for _d, _off, _ha, _va in zip(np.eye(3), ((-5, 4), (0, -7), (-6, -3)), ("right", "center", "right"), ("bottom", "top", "top")):
        _ax.plot(*ortho(2 * _d), "o", color="black", ms=3.5, zorder=4)
        _ax.annotate("$2$", ortho(2 * _d), textcoords="offset points", xytext=_off, ha=_ha, va=_va, fontsize=12)
    # two points of the level set
    for _q, _name, _off in (((0.3, 1.0, 1.7), r"$\vec{x}$", (5, 5)), ((0.2, 1.3, 1.5), r"$\vec{y}$", (7, 0))):
        _q = 2 * np.array(_q) / np.linalg.norm(_q)
        arrow(_ax, (0, 0), ortho(_q), RED)
        _ax.plot(*ortho(_q), "o", color="black", ms=3.5, zorder=4)
        _ax.annotate(_name, ortho(_q), textcoords="offset points", xytext=_off, ha="left", va="center", color=RED, fontsize=13)
    _ax.annotate(r"$\vec{0}$", (0, 0), textcoords="offset points", xytext=(5, -6), ha="left", va="top", fontsize=13)
    _ax.text(1.6, -1.75, "$f^{-1}(2)$", color=BLUE, fontsize=13, ha="left", va="top")

    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** $\mathrm{Im}(f)$ and $\mathrm{graph}(f)$ help us visualize $f$ as a set of points (very useful in lower dimensions)

    - $\leadsto$ &nbsp; we might have many functions with same image
    - $\leadsto$ &nbsp; graph essentially determines the function completely! (but it lives in higher dimensions)

    ### Level sets
    """
            ),
            definition(
                r"""
    Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$, $\vec{b} \in B$ fixed, the **level set** of $f$ with value $\vec{b}$ is

    $$
    f^{-1}(\vec{b}) = \left\{\, \vec{x} \in \mathbb{R}^n \;\middle|\; \vec{x} \in A \text{ and } f(\vec{x}) = \vec{b} \,\right\}
    $$
    """,
                "Level set",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f : \mathbb{R}^3 \longrightarrow \mathbb{R}, \quad \vec{x} \longmapsto \lVert \vec{x} \rVert$

    $$
    \text{fix } r = 2 \quad \Longrightarrow \quad f^{-1}(2) = \left\{\, \vec{x} \in \mathbb{R}^3 \;\middle|\; \lVert \vec{x} \rVert = 2 \,\right\} = \text{sphere centered at } \vec{0} \text{ with radius } r = 2
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** Here $f^{-1}(\vec{b})$ is NOT the value of the inverse function of $f$ (we don't even know if $f$ has an inverse).

    $f^{-1}(\vec{b})$ is the set of points in the domain of $f$ which gives the value “$\vec{b}$” as an output!

    $\leadsto$ &nbsp; if $f$ is invertible then, for each $\vec{b} \in B$,

    $$
    f^{-1}(\vec{b}) = \left\{\, \vec{x} \in A \;\middle|\; f(\vec{x}) = \vec{b} \,\right\} \quad \text{has a single element, which we call ``$f^{-1}(\vec{b})$''}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, HALF, RED, arrow, blank, mo, np, ortho, quadric):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    # level sets of f in the plane
    _fig, _ax = blank(HALF, 3.3, (-3.6, 4.4), (-3.6, 3.8))
    arrow(_ax, (-3.4, 0), (3.5, 0), "black", lw=0.9)
    arrow(_ax, (0, -3.4), (0, 3.5), "black", lw=0.9)
    _ax.text(3.5, -0.15, "$x^1$", fontsize=13, ha="right", va="top")
    _ax.text(0.15, 3.5, "$x^2$", fontsize=13, ha="left", va="top")
    _s = np.linspace(-2.9, 2.9, 200)
    for _sign in (1, -1):
        _ax.plot(_s, _sign * _s, color=GREEN, lw=1.4)
        _ax.plot(_sign * np.sqrt(1 + _s[20:-20] ** 2), _s[20:-20], color=BLUE, lw=1.4)
        _ax.plot(_s[35:-35], _sign * np.sqrt(4 + _s[35:-35] ** 2), color=RED, lw=1.4)
    _ax.text(3.08, 2.95, "$f^{-1}(0)$", color=GREEN, fontsize=12, ha="left", va="center")
    _ax.text(1.55, 0.55, "$f^{-1}(1)$", color=BLUE, fontsize=12, ha="left", va="center")
    _ax.text(-0.3, 3.05, "$f^{-1}(-4)$", color=RED, fontsize=12, ha="right", va="center")

    # level sets of g in space
    _fig2, _ax2 = blank(HALF, 4.2, (-3.6, 4.7), (-4.8, 4.9))
    for _d, _len in zip(np.eye(3), (5.6, 3.9, 5.0)):
        arrow(_ax2, ortho(-1.2 * _d), ortho(_len * _d), "black", lw=0.9)
    quadric(_ax2, 0, 3.0, GREEN)
    quadric(_ax2, 1, 2.2, BLUE)
    quadric(_ax2, -4, 3.6, RED)
    _ax2.text(3.15, 3.55, "$g^{-1}(-4)$", color=RED, fontsize=12, ha="left", va="center", bbox=_box)
    _ax2.text(3.15, 2.7, "$g^{-1}(0)$", color=GREEN, fontsize=12, ha="left", va="center", bbox=_box)
    _ax2.text(1.75, 0.75, "$g^{-1}(1)$", color=BLUE, fontsize=12, ha="left", va="center", bbox=_box)

    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** &nbsp; $f : \mathbb{R}^2 \longrightarrow \mathbb{R}, \quad \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \longmapsto (x^1)^2 - (x^2)^2$

    What are the level sets with values $1, 0, -4$?

    $$
    f^{-1}(b) = \left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \;\middle|\; (x^1)^2 - (x^2)^2 = b \,\right\}
    $$

    - $f^{-1}(0) \iff \lvert x^1 \rvert = \lvert x^2 \rvert$ &nbsp; two intersecting lines (a cone)
    - $f^{-1}(1) \iff (x^1)^2 - (x^2)^2 = 1$ &nbsp; a hyperbola
    - $f^{-1}(-4) \iff (x^1)^2 - (x^2)^2 = -4$ &nbsp; also a hyperbola
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    g : \mathbb{R}^3 \longrightarrow \mathbb{R}, \quad \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \longmapsto (x^1)^2 + (x^2)^2 - (x^3)^2
    $$

    - $g^{-1}(0)$ &nbsp; cone
    - $g^{-1}(1)$ &nbsp; hyperboloid of one sheet
    - $g^{-1}(-4)$ &nbsp; hyperboloid of two sheets
    """
            ),
            _fig2,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    b_level = mo.ui.slider(-4, 4, 0.5, value=1, label="$b$", show_value=True)
    return (b_level,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, arrow, b_level, mo, np, ortho, plane, quadric, table):
    _b = b_level.value

    _fig = Figure(figsize=(FULL, 3.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    # f^{-1}(b) in the plane
    plane(_left, 4)
    _left.set_xticks(range(-4, 5, 2))
    _left.set_yticks(range(-4, 5, 2))
    _left.set_xlabel("$x^1$")
    _left.set_ylabel("$x^2$", rotation=0, labelpad=10)
    _s = np.linspace(-4.2, 4.2, 400)
    for _sign in (1, -1):
        if _b > 0:
            _left.plot(_sign * np.sqrt(_b + _s**2), _s, color=BLUE, lw=1.4)
        elif _b < 0:
            _left.plot(_s, _sign * np.sqrt(_s**2 - _b), color=BLUE, lw=1.4)
        else:
            _left.plot(_s, _sign * _s, color=BLUE, lw=1.4)

    # g^{-1}(b) in space, for -3 <= x^3 <= 3
    _right.set_xlim(-4.6, 4.6)
    _right.set_ylim(-4.6, 4.6)
    _right.set_aspect("equal")
    _right.axis("off")
    for _d, _len in zip(np.eye(3), (6.0, 4.4, 4.7)):
        arrow(_right, ortho(-1.2 * _d), ortho(_len * _d), "black", lw=0.9)
    quadric(_right, _b, 3.0, BLUE, wire=True)

    _flat = "two intersecting lines (a cone)" if _b == 0 else "a hyperbola"
    _solid = "cone" if _b == 0 else "hyperboloid of one sheet" if _b > 0 else "hyperboloid of two sheets"

    mo.vstack(
        [
            mo.hstack([b_level], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f^{-1}(b) \subseteq \mathbb{R}^2$", rf"$(x^1)^2 - (x^2)^2 = {_b:g}$ &nbsp; ({_flat})"),
                    (r"$g^{-1}(b) \subseteq \mathbb{R}^3$", rf"$(x^1)^2 + (x^2)^2 - (x^3)^2 = {_b:g}$ &nbsp; ({_solid})"),
                ]
            ),
            _fig,
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

    $p^{-1}(r)$ is a plane in $\mathbb{R}^3$ (if $(a, b, c) \neq (0, 0, 0)$)

    $$
    \leadsto \quad \text{starting point } \begin{bmatrix} (r - d)/a \\ 0 \\ 0 \end{bmatrix} \ (\text{if } a \neq 0), \qquad \text{normal vector } \begin{bmatrix} a \\ b \\ c \end{bmatrix}
    $$

    (if $a = b = c = 0$, then $p^{-1}(r) = \mathbb{R}^3$ when $r = d$, and $\varnothing$ otherwise)

    For $q : \mathbb{R}^3 \longrightarrow \mathbb{R}$ a **quadratic scalar function**

    $$
    \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \longmapsto
    \begin{aligned}
    &a (x^1)^2 + b (x^2)^2 + c (x^3)^2 + d\, x^1 x^2 + e\, x^2 x^3 + f\, x^3 x^1 \\
    &+ g\, x^1 + h\, x^2 + i\, x^3 + j
    \end{aligned}
    $$

    $q^{-1}(r)$ is called a **quadratic surface**.
    """,
                "Affine and quadratic scalar functions",
            ),
            mo.md(
                r"""
    $$
    \begin{aligned}
    \frac{(x^1)^2}{a^2} + \frac{(x^2)^2}{b^2} + \frac{(x^3)^2}{c^2} &= r^2 &&\text{ellipsoids} \rule[-1.5em]{0pt}{3.4em} \\
    \frac{(x^1)^2}{a^2} + \frac{(x^2)^2}{b^2} - \frac{(x^3)^2}{c^2} &= \pm r^2 &&\text{hyperboloids} \rule[-1.5em]{0pt}{3.4em} \\
    \frac{(x^1)^2}{a^2} + \frac{(x^2)^2}{b^2} - \frac{x^3}{c} &= d &&\text{paraboloids} \rule[-1.5em]{0pt}{3.4em} \\
    &\ \,\vdots
    \end{aligned}
    \qquad (\text{here } a, b, c \neq 0 \text{ and } r > 0)
    $$

    **Remark.** Sometimes level sets of a function can be seen as graphs of another function and vice-versa!

    $\Longrightarrow$ &nbsp; geometry of sets in $\mathbb{R}^n$ or $\mathbb{R}^m$ or $\mathbb{R}^n \times \mathbb{R}^m$ is useful to study properties of various functions
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a multivariable function $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ has 3 parts: domain, codomain and rule of assignment; scalar functions ($m = 1$), paths ($n = 1$), parameterized surfaces ($n = 2$)
    - $\mathrm{Im}(f) \subseteq B$ (not necessarily equal) and $\mathrm{graph}(f) \subseteq A \times B$ help us visualize $f$ as a set of points; the graph essentially determines the function
    - the level set $f^{-1}(\vec{b}) = \{\, \vec{x} \in A \mid f(\vec{x}) = \vec{b} \,\}$ is a set of points in the domain, NOT the value of an inverse function
    - level sets of affine scalar functions on $\mathbb{R}^3$ are planes; level sets of quadratic scalar functions are quadratic surfaces (ellipsoids, hyperboloids, paraboloids, …)

    **Next:** local properties of paths
    """)
    return


if __name__ == "__main__":
    app.run()
