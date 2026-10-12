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
    header("Lecture 07", "Week 04", "Lecture 07 · Local properties of paths")
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
def _(arrow, np):
    def path_projection(t, y1, y2):
        """Oblique view of R x R^2 for graphs of paths, as on the board: t to the right (compressed),
        y^2 up, y^1 towards the viewer."""
        t, y1, y2 = (np.asarray(c, dtype=float) for c in (t, y1, y2))
        return 0.36 * t - 0.45 * y1, y2 - 0.4 * y1

    def path_axes(ax, t0, t1):
        """The three coordinate axes of R x R^2 in the oblique view, with their names."""
        for tail, tip in (((t0, 0, 0), (t1, 0, 0)), ((0, -1.5, 0), (0, 2.3, 0)), ((0, 0, -1.5), (0, 0, 1.75))):
            p, q = path_projection(*tail), path_projection(*tip)
            arrow(ax, (float(p[0]), float(p[1])), (float(q[0]), float(q[1])), "black", lw=0.9)
        e = path_projection(t1, 0, 0)
        ax.text(float(e[0]) + 0.08, float(e[1]), "$t$", fontsize=13, ha="left", va="center")
        e = path_projection(0, 2.3, 0)
        ax.text(float(e[0]) - 0.06, float(e[1]) - 0.04, "$y^1$", fontsize=13, ha="right", va="top")
        ax.text(0.1, 1.72, "$y^2$", fontsize=13, ha="left", va="center")

    def helix(ax, t0, t1, color, gaps=()):
        """graph of t -> (cos t, sin t) for t in [t0, t1]: the half behind the (t, y^2)-plane is dashed."""
        s = np.linspace(t0, t1, 1600)
        for g in gaps:
            s = s[np.abs(s - g) > 0.07]
        x, y = path_projection(s, np.cos(s), np.sin(s))
        back = np.cos(s) < 0
        cut = np.zeros_like(back)
        cut[1:] = np.diff(s) > 0.05
        ax.plot(np.where(back | cut, np.nan, x), np.where(back | cut, np.nan, y), color=color, lw=1.5)
        ax.plot(np.where(~back | cut, np.nan, x), np.where(~back | cut, np.nan, y), color=color, lw=1.0, ls=(0, (4, 3)))

    return helix, path_axes, path_projection


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - multivariable functions $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$
    - $\leadsto$ &nbsp; global properties (image, graph, level sets)

    **In this lecture:** local properties of paths $\gamma : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}^m$ (MT 2.4): how a function behaves at a point (limits, continuity, differentiability)
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.2 &nbsp; Local properties of paths

    ### Paths
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
    """,
                "Path",
            ),
            mo.md(
                r"""
    **Remark.** Each component $\gamma^i : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}$ is a usual single variable real valued function!

    $\Longrightarrow$ &nbsp; paths are ordered lists of single variable scalar functions, like vectors were ordered lists of scalars!

    **Example.** $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ an affine parameterization of a line

    $$
    \gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
    \quad \leadsto \quad
    \underbrace{\gamma^1(t) = x^1 + t v^1, \quad \gamma^2(t) = x^2 + t v^2}_{\text{pair of affine single variable functions}}
    $$

    **Example.**

    $$
    \begin{aligned}
    \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^2 \\
    t &\longmapsto \gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; $\gamma^1 : \mathbb{R} \longrightarrow \mathbb{R}$, $t \longmapsto \cos(t)$ is the cosine function

    $\leadsto$ &nbsp; $\gamma^2 : \mathbb{R} \longrightarrow \mathbb{R}$, $t \longmapsto \sin(t)$ is the sine function

    $$
    \begin{aligned}
    \mathrm{Im}(\gamma) &= \left\{\, \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; \exists\, t \in \mathbb{R},\ y^1 = \gamma^1(t),\ y^2 = \gamma^2(t) \,\right\} \\
    &= \underbrace{\left\{\, \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; t \in \mathbb{R} \,\right\}}_{\text{unit circle } (y^1)^2 + (y^2)^2 = 1}
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \mathrm{graph}(\gamma) &= \left\{\, \begin{bmatrix} t \\ y^1 \\ y^2 \end{bmatrix} \in \mathbb{R} \times \mathbb{R}^2 = \mathbb{R}^3 \;\middle|\; t \in \mathbb{R},\ y^1 = \gamma^1(t),\ y^2 = \gamma^2(t) \,\right\} \\
    &= \underbrace{\left\{\, \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix} \in \mathbb{R}^3 \;\middle|\; t \in \mathbb{R} \,\right\}}_{\text{helix}}
    \end{aligned}
    $$
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
def _(Arc, BLUE, FULL, GREY, HALF, arrow, blank, helix, math, mo, np, path_axes, path_projection, t_circle, table, vector):
    _t = t_circle.value
    _p = (math.cos(_t), math.sin(_t))
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    # Im(gamma): the unit circle
    _fig, _ax = blank(HALF, 3.3, (-1.7, 2.0), (-1.6, 1.8))
    arrow(_ax, (-1.5, 0), (1.75, 0), "black", lw=0.9)
    arrow(_ax, (0, -1.5), (0, 1.6), "black", lw=0.9)
    _ax.text(1.8, -0.06, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.1, 1.62, "$y^2$", fontsize=13, ha="right", va="center")
    _th = np.linspace(0, 2 * np.pi, 361)
    _ax.plot(np.cos(_th), np.sin(_th), color=BLUE, lw=1.5)
    _angle = _t % (2 * math.pi)
    _ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=math.degrees(_angle), color=GREY, lw=1.0))
    if _angle >= 0.5:
        _ax.text(0.5 * math.cos(_angle / 2), 0.5 * math.sin(_angle / 2), "$t$", color=GREY, fontsize=12, ha="center", va="center", bbox=_box)
    vector(_ax, (0, 0), _p, BLUE, r"$\gamma(t)$", -35, r=19)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    _ax.text(-1.65, 1.6, r"$\mathrm{Im}(\gamma)$", fontsize=13, ha="left", va="center")

    # graph(gamma): the helix; its points have three coordinates (t, gamma(t))
    _fig3, _ax3 = blank(FULL, 3.55, (-2.4, 5.6), (-1.95, 1.9))
    path_axes(_ax3, -5.2, 14.2)
    helix(_ax3, -4.4, 13.6, BLUE)
    for _m in (-5.2, 1.0, 7.3):
        _p0 = path_projection(_m - 0.1, math.cos(_m - 0.1), math.sin(_m - 0.1))
        _p1 = path_projection(_m + 0.1, math.cos(_m + 0.1), math.sin(_m + 0.1))
        if _m > -4.4:
            arrow(_ax3, (float(_p0[0]), float(_p0[1])), (float(_p1[0]), float(_p1[1])), BLUE)
    for _n, _name in enumerate(("$t=0$", r"$t=\pi$", r"$t=2\pi$", r"$t=3\pi$", r"$t=4\pi$")):
        _q = path_projection(_n * math.pi, math.cos(_n * math.pi), math.sin(_n * math.pi))
        _ax3.plot(*_q, "o", color=GREY, ms=3.5, zorder=4)
        _ax3.annotate(_name, (float(_q[0]), float(_q[1])), textcoords="offset points", xytext=(5, -9) if _n % 2 == 0 else (-5, 9), ha="left" if _n % 2 == 0 else "right", va="top" if _n % 2 == 0 else "bottom", color=GREY, fontsize=12, bbox=_box, zorder=3)
    _g = path_projection(_t, _p[0], _p[1])
    _out = (-0.45 * _p[0], _p[1] - 0.4 * _p[0])  # direction from the t-axis to the point, in the picture
    _norm = math.hypot(*_out)
    _dx, _dy = 11 * _out[0] / _norm, 11 * _out[1] / _norm
    _ax3.plot(*_g, "o", color="black", ms=4.5, zorder=6)
    _ax3.annotate(r"$(t, \gamma(t))$", (float(_g[0]), float(_g[1])), textcoords="offset points", xytext=(_dx, _dy), ha="left" if _dx > 0 else "right", va="bottom" if _dy > 0 else "top", fontsize=12, bbox=_box, zorder=5)
    _ax3.text(-2.35, 1.7, r"$\mathrm{graph}(\gamma)$", fontsize=13, ha="left", va="center")

    def _f(v):
        return f"{round(v, 2) + 0.0:.2f}"

    mo.vstack(
        [
            mo.hstack([t_circle], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\gamma(t)$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_f(_p[0])} \\ {_f(_p[1])} \end{{bmatrix}}}}$"),
                    (r"$(t, \gamma(t))$", rf"$\begin{{bmatrix}} {_t:.1f} \\ {_f(_p[0])} \\ {_f(_p[1])} \end{{bmatrix}}$"),
                ]
            ),
            _fig,
            _fig3,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** We can extend vector operations to paths. Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^m$, and $\lambda : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    \begin{aligned}
    \underbrace{(\gamma + \sigma)(t)}_{\text{addition of paths}} &= \underbrace{\gamma(t) + \sigma(t)}_{\text{addition of vectors}} && \leadsto \quad \gamma + \sigma : \mathbb{R} \longrightarrow \mathbb{R}^m \\[26pt]
    \underbrace{(\lambda \gamma)(t)}_{\substack{\text{multiplication of scalar} \\ \text{function and a path}}} &= \underbrace{\lambda(t)\, \gamma(t)}_{\substack{\text{multiplication of} \\ \text{scalar and vector}}} && \leadsto \quad \lambda \gamma : \mathbb{R} \longrightarrow \mathbb{R}^m \\[26pt]
    \underbrace{(\gamma \cdot \sigma)(t)}_{\text{dot product of paths}} &= \underbrace{\gamma(t) \cdot \sigma(t)}_{\text{dot product of vectors}} && \leadsto \quad \gamma \cdot \sigma : \mathbb{R} \longrightarrow \mathbb{R} \\[26pt]
    \underbrace{(\gamma \times \sigma)(t)}_{\text{cross-product of paths in } \mathbb{R}^3} &= \underbrace{\gamma(t) \times \sigma(t)}_{\text{cross-product of vectors in } \mathbb{R}^3} && \leadsto \quad \gamma \times \sigma : \mathbb{R} \longrightarrow \mathbb{R}^3 \quad (\text{if } m = 3) \\[10pt]
    \end{aligned}
    $$

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, \quad \sigma(t) = \begin{bmatrix} at + b \\ ct + d \end{bmatrix}, \quad \lambda(t) = \cos(t)$

    $$
    \begin{aligned}
    &\leadsto \quad (\gamma + \sigma)(t) = \begin{bmatrix} \cos(t) + at + b \\ \sin(t) + ct + d \end{bmatrix} \\[4pt]
    &\leadsto \quad (\gamma \cdot \sigma)(t) = \cos(t)(at + b) + \sin(t)(ct + d) \\[4pt]
    &\leadsto \quad \lVert \gamma \rVert^2(t) = (\gamma \cdot \gamma)(t) = \cos(t)^2 + \sin(t)^2 = 1 \\[4pt]
    &\leadsto \quad (\lambda \gamma)(t) = \begin{bmatrix} \cos(t)^2 \\ \cos(t) \sin(t) \end{bmatrix}
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Limits

    (how does a path behave as we “approach” a certain input?)
    """
            ),
            definition(
                r"""
    Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $a \in \mathbb{R}$ and $\vec{b} \in \mathbb{R}^m$ we say

    $$
    \lim_{t \to a} \gamma(t) = \vec{b} \qquad (\text{the limit of } \gamma \text{ as } t \text{ approaches } a \text{ is equal to } \vec{b})
    $$

    if we can make $\gamma(t)$ **arbitrarily** close to $\vec{b}$ (as close as we want) by taking $t$ **sufficiently** close to $a$ (as close as we need), but different from $a$ (we don't even need $\gamma$ to be defined at $t = a$ to talk about limits).
    """,
                "Limit of a path",
            ),
            mo.md(
                r"""
    Choose how close to $\vec{b}$ you would like &nbsp; $\leadsto$ &nbsp; want $\lVert \gamma(t) - \vec{b} \rVert < \varepsilon$, for $\varepsilon > 0$.

    Can we achieve this, by taking $t$ close enough to $a$? &nbsp; $\leadsto$ &nbsp; can we find $\delta > 0$ such that

    $$
    0 < \lvert t - a \rvert < \delta \quad \Longrightarrow \quad \lVert \gamma(t) - \vec{b} \rVert < \varepsilon \ ?
    $$

    Can we do this for every $\varepsilon > 0$? If yes, then $\displaystyle \lim_{t \to a} \gamma(t) = \vec{b}$!
    """
            ),
            theorem(
                r"""
    Limit of paths can be calculated componentwise

    $$
    \lim_{t \to a} \gamma(t) = \vec{b} \quad \Longleftrightarrow \quad \lim_{t \to a} \gamma^i(t) = b^i \quad \forall\, i = 1, 2, \dots, m
    $$
    """,
                "Limits componentwise",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

    $$
    \lim_{t \to \pi/2} \gamma(t) = \begin{bmatrix} \displaystyle \lim_{t \to \pi/2} \cos(t) \\[8pt] \displaystyle \lim_{t \to \pi/2} \sin(t) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    $$

    **Remark.** Limits are unique, provided they exist!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, blank, definition, helix, mo, path_axes, path_projection, theorem):
    _fig, _ax = blank(FULL, 3.55, (-3.3, 4.7), (-1.95, 1.9))
    path_axes(_ax, -6.6, 11.2)
    helix(_ax, -5.9, 10.6, BLUE, gaps=(0,))
    _limit = tuple(float(c) for c in path_projection(0, 1, 0))
    _value = tuple(float(c) for c in path_projection(0, 0, 1))
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _ax.plot(*_limit, "o", color="black", ms=6, mfc="white", mew=1.2, zorder=5)
    _ax.plot(*_value, "o", color="black", ms=4.5, zorder=5)
    _ax.annotate(r"$(0, \lim_{t \to 0} \gamma(t))$", _limit, xytext=(8, -12), textcoords="offset points", ha="left", va="top", fontsize=12, bbox=_box, zorder=4)
    _ax.annotate(r"$(0, \gamma(0))$", _value, xytext=(-9, 2), textcoords="offset points", ha="right", va="center", fontsize=12, bbox=_box, zorder=4)
    _ax.text(-3.25, 1.7, r"$\mathrm{graph}(\gamma)$", fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.md(r"""### Continuity"""),
            definition(
                r"""
    A path $\gamma$ is **continuous** at $t = a$ if

    $$
    \lim_{t \to a} \gamma(t) = \gamma(a)
    $$

    $\gamma$ is continuous in $(a_1, a_2) \subset \mathbb{R}$ if it is continuous at every $t \in (a_1, a_2)$.
    """,
                "Continuity of a path",
            ),
            theorem(
                r"""
    A path is continuous if and only if all of its components are continuous

    $$
    \lim_{t \to a} \gamma(t) = \gamma(a) \quad \Longleftrightarrow \quad \lim_{t \to a} \gamma^i(t) = \gamma^i(a) \quad \forall\, i = 1, 2, \dots, m
    $$
    """,
                "Continuity componentwise",
            ),
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
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Differentiability"""),
            definition(
                r"""
    A path $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is **differentiable** at $t = a$ if

    $$
    \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} \quad \text{exists.}
    $$

    $\leadsto$ &nbsp; if it exists we call it the **derivative** of $\gamma$ at $t = a$ and denote it $\gamma'(a)$
    """,
                "Derivative of a path",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; we also call $\gamma'(a)$ the **velocity** of the path $\gamma$ at $t = a$ &nbsp; ($\gamma(a)$ is the **position** of $\gamma$ at $t = a$)

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

    $$
    \begin{aligned}
    \gamma'(a) &= \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} = \lim_{t \to a} \begin{bmatrix} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix}
    = \begin{bmatrix} \displaystyle \lim_{t \to a} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \displaystyle \lim_{t \to a} \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix} \\[6pt]
    &= \begin{bmatrix} \dfrac{d}{dt} \cos(t) \Big|_{t = a} \\[10pt] \dfrac{d}{dt} \sin(t) \Big|_{t = a} \end{bmatrix} = \begin{bmatrix} -\sin(a) \\ \cos(a) \end{bmatrix}
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
def _(Arc, BLUE, GREEN, GREY, HALF, a_circle, arrow, blank, math, mo, np, table, vector):
    _a = a_circle.value
    _p = (math.cos(_a), math.sin(_a))
    _v = (-math.sin(_a), math.cos(_a))
    _tip = (_p[0] + _v[0], _p[1] + _v[1])
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    _fig, _ax = blank(HALF, 3.4, (-2.25, 2.25), (-2.1, 2.15))
    arrow(_ax, (-1.9, 0), (1.95, 0), "black", lw=0.9)
    arrow(_ax, (0, -1.9), (0, 1.95), "black", lw=0.9)
    _ax.text(2.0, -0.08, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(0.1, 1.98, "$y^2$", fontsize=13, ha="left", va="center")
    _th = np.linspace(0, 2 * np.pi, 361)
    _ax.plot(np.cos(_th), np.sin(_th), color=BLUE, lw=1.5)
    _ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=math.degrees(_a), color=GREY, lw=1.0))
    if _a >= 0.5:
        _ax.text(0.5 * math.cos(_a / 2), 0.5 * math.sin(_a / 2), "$a$", color=GREY, fontsize=12, ha="center", va="center", bbox=_box)
    vector(_ax, (0, 0), _p, BLUE, r"$\gamma(a)$", -40, r=20)
    vector(_ax, _p, _tip, GREEN, r"$\gamma'(a)$", 0, r=19)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)

    def _f(v):
        return f"{round(v, 2) + 0.0:.2f}"

    mo.vstack(
        [
            mo.hstack([a_circle], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"position $\gamma(a)$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_f(_p[0])} \\ {_f(_p[1])} \end{{bmatrix}}}}$"),
                    (r"velocity $\gamma'(a)$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_f(_v[0])} \\ {_f(_v[1])} \end{{bmatrix}}}}$"),
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
            theorem(
                r"""
    Derivatives of paths can be computed componentwise

    $$
    \gamma'(a) = \vec{v} \quad \Longleftrightarrow \quad \frac{d}{dt} \gamma^i(t) \Big|_{t = a} = v^i \quad \forall\, i = 1, 2, \dots, m
    $$
    """,
                "Derivatives componentwise",
            ),
            definition(
                r"""
    If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is differentiable at $t = a$ with velocity vector $\gamma'(a) \neq \vec{0}$, we call the line through $\vec{x} = \gamma(a)$ in the direction of $\vec{v} = \gamma'(a)$ the **tangent line** to $\gamma$ at $t = a$

    $$
    T_a \gamma = \left\{\, \vec{y} = \gamma(a) + s\, \gamma'(a) \;\middle|\; s \in \mathbb{R} \,\right\}
    $$
    """,
                "Tangent line",
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
def _(BLUE, FULL, GREEN, ORANGE, a_parabola, arrow, blank, math, mo, np, table, vector):
    _a = a_parabola.value
    _p, _v = (_a**2, _a), (2 * _a, 1.0)
    _tip = (_p[0] + _v[0], _p[1] + _v[1])
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    _fig, _ax = blank(FULL, 4.2, (-3.6, 6.4), (-2.7, 3.0))
    arrow(_ax, (-3.4, 0), (6.1, 0), "black", lw=0.9)
    arrow(_ax, (0, -2.6), (0, 2.8), "black", lw=0.9)
    _ax.text(6.15, -0.1, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.12, 2.8, "$y^2$", fontsize=13, ha="right", va="center")
    _t = np.linspace(-2.45, 2.45, 300)
    _ax.plot(_t**2, _t, color=BLUE, lw=1.5)
    _ax.text(5.0, -1.75, r"$\mathrm{Im}(\gamma)$", color=BLUE, fontsize=13, ha="center", va="center")
    _s = np.array([-12.0, 12.0])
    _ax.plot(_p[0] + _s * _v[0], _p[1] + _s * _v[1], color=ORANGE, lw=1.0)
    # the names sit off the line: T_a gamma on the outer side of the parabola, gamma(a) on the inner side
    _n = math.hypot(*_v)
    _out = (-_v[1] / _n, _v[0] / _n)
    _q = (_p[0] - 1.4 * _v[0] / _n, _p[1] - 1.4 * _v[1] / _n)
    _ax.annotate(r"$T_a\gamma$", _q, textcoords="offset points", xytext=(15 * _out[0], 15 * _out[1]), ha="center", va="center", color=ORANGE, fontsize=13, bbox=_box, zorder=3)
    vector(_ax, _p, _tip, GREEN, r"$\gamma'(a)$", 0, r=20)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    _ax.annotate(r"$\gamma(a)$", _p, textcoords="offset points", xytext=(-19 * _out[0], -19 * _out[1]), ha="center", va="center", fontsize=13, bbox=_box, zorder=3)

    mo.vstack(
        [
            mo.hstack([a_parabola], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"position $\gamma(a)$", rf"$\begin{{bmatrix}} {_p[0] + 0.0:.2f} \\ {_p[1] + 0.0:g} \end{{bmatrix}}$"),
                    (r"velocity $\gamma'(a)$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_v[0] + 0.0:g} \\ 1 \end{{bmatrix}}}}$"),
                    (
                        r"tangent line $T_a \gamma$",
                        rf"$\textcolor{{{ORANGE}}}{{\left\{{\, \vec{{y}} = \begin{{bmatrix}} {_p[0] + 0.0:.2f} \\ {_p[1] + 0.0:g} \end{{bmatrix}} + s \begin{{bmatrix}} {_v[0] + 0.0:g} \\ 1 \end{{bmatrix}} \;\middle\vert\; s \in \mathbb{{R}} \,\right\}}}}$",
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a path $\gamma : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}^m$ is an ordered list of single variable functions $\gamma^1, \dots, \gamma^m$; vector operations extend to paths
    - $\displaystyle \lim_{t \to a} \gamma(t) = \vec{b}$: we can make $\gamma(t)$ arbitrarily close to $\vec{b}$ by taking $t$ sufficiently close to $a$ (but different from $a$); $\gamma$ is continuous at $t = a$ if $\displaystyle \lim_{t \to a} \gamma(t) = \gamma(a)$
    - the derivative (velocity) $\gamma'(a) = \displaystyle \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}$; $\gamma(a)$ is the position
    - limits, continuity and derivatives of paths can be computed componentwise
    - if $\gamma'(a) \neq \vec{0}$, the tangent line to $\gamma$ at $t = a$ is $T_a \gamma = \{\, \vec{y} = \gamma(a) + s\, \gamma'(a) \mid s \in \mathbb{R} \,\}$

    **Next:** local properties of scalar functions and maps: limits
    """)
    return


if __name__ == "__main__":
    app.run()
