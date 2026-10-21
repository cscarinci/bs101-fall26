import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 14 · Local extrema and the second derivative test", css_file="bs101.css")


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
    header("Lecture 14", "Week 09", "Lecture 14 · Local extrema and the second derivative test")
    return


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
        ax.annotate(text, at, textcoords="offset points", xytext=(r * c, r * s), ha=ha, va=va, color=color, fontsize=fontsize, zorder=6, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    def num(v, digits=2):
        """Fixed-point number for the readout tables (never prints a negative zero)."""
        return f"{round(v, digits) + 0.0:.{digits}f}"

    return cross_axes, num, tip_label


@app.cell(hide_code=True)
def _(math, np):
    # ---- Drawing helpers of this lecture: graphs of functions on R^2 -----
    # Orthographic views of R^3 = R^2 x R, with x^1 pointing towards the viewer, x^2 to the right and y up.
    # A graph is drawn as an opaque surface, back to front; curves keep only the parts that no surface hides.
    from matplotlib.collections import PolyCollection

    class View:
        """The view from azimuth `az` and elevation `el` (degrees), with heights y drawn at the scale `ys`."""

        def __init__(self, az=28, el=24, ys=1.0):
            a, e = math.radians(az), math.radians(el)
            s = np.array([1.0, 1.0, ys])
            self.right = np.array([-math.sin(a), math.cos(a), 0.0]) * s
            self.up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)]) * s
            self.eye = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)]) * s  # depth of p: p @ eye
            self.sight = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e) / ys])  # towards the viewer

        def __call__(self, x1, x2, y):
            """Picture coordinates of the point(s) (x^1, x^2, y)."""
            p = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in (x1, x2, y))), -1)
            return p @ self.right, p @ self.up

    class Graph:
        """The graph y = f(x^1, x^2) over the part of the plane where inside(x^1, x^2) holds."""

        def __init__(self, f, inside):
            self.f, self.inside = f, inside

        def hides(self, view, p, reach=12.0, steps=480):
            """For each point of p (shape (N, 3)): does the graph cross the line of sight from it to the viewer?"""
            s = np.linspace(reach / steps / 8, reach, steps)
            q = p[:, None, :] + s[:, None] * view.sight
            x1, x2, y = q[..., 0], q[..., 1], q[..., 2]
            with np.errstate(all="ignore"):
                d = np.where(self.inside(x1, x2), y - self.f(x1, x2), np.nan)
            return np.any(d[:, :-1] * d[:, 1:] < 0, axis=1)

    def surface(ax, view, graph, x1, x2, tint=None, zorder=1):
        """The graph as an opaque surface through the grid points (x1, x2) (2D arrays), drawn back to front
        in tones of LIGHT, lit from the upper left; faces where tint(x^1, x^2) holds take deeper tones."""
        p = np.stack([x1, x2, graph.f(x1, x2)], -1)
        q = np.stack([p[:-1, :-1], p[1:, :-1], p[1:, 1:], p[:-1, 1:]], 2).reshape(-1, 4, 3)
        n = np.cross(q[:, 2] - q[:, 0], q[:, 3] - q[:, 1])
        n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
        k = np.clip(np.abs(n @ np.array([0.3, -0.4, 0.87])) / 1.0034, 0, 1)[:, None]
        lit, dark = np.array([0.97, 0.985, 1.0]), np.array([0.79, 0.875, 0.955])
        if tint is not None:
            m = q.mean(1)
            deep = tint(m[:, 0], m[:, 1])[:, None]
            lit, dark = np.where(deep, [0.86, 0.92, 0.985], lit), np.where(deep, [0.64, 0.76, 0.9], dark)
        col = dark + (lit - dark) * k
        order = np.argsort(q.mean(1) @ view.eye)
        verts = np.stack([q @ view.right, q @ view.up], -1)[order]
        ax.add_collection(PolyCollection(verts, facecolors=col[order], edgecolors=col[order], linewidths=0.3, zorder=zorder))

    def curve(ax, view, graphs, x1, x2, y, color, lw=1.4, ls="-", back=(0, (3, 3)), zorder=3):
        """The curve through the points (x1, x2, y): with line style `ls` where no graph hides it, and with
        `back` where one does (None: left out)."""
        p = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in (x1, x2, y))), -1).reshape(-1, 3)
        hid = np.zeros(len(p), bool)
        for g in graphs:
            hid |= g.hides(view, p)
        X, Y = view(p[:, 0], p[:, 1], p[:, 2])
        keep = ~hid | np.r_[False, ~hid[:-1]]
        ax.plot(np.where(keep, X, np.nan), np.where(keep, Y, np.nan), color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
        if back is not None and hid.any():
            keep = hid | np.r_[False, hid[:-1]]
            ax.plot(np.where(keep, X, np.nan), np.where(keep, Y, np.nan), color=color, lw=0.75 * lw, ls=back, zorder=zorder)

    def seen(view, graphs, x1, x2, y):
        """Is the point (x1, x2, y) in sight?"""
        p = np.array([[x1, x2, y]], dtype=float)
        return not any(g.hides(view, p)[0] for g in graphs)

    return Graph, View, curve, seen, surface


@app.cell(hide_code=True)
def _(arrow, curve, np, seen, tip_label):
    def axes3d(ax, view, graphs, ends, labels, dirs, tails=((0, 0, 0),) * 3, lw=0.9):
        """Coordinate axes from the points `tails` to the points `ends`, with arrow heads where the tips are in
        sight and the `labels` placed beyond the tips in the picture directions `dirs` (degrees)."""
        for tail, end, label, d in zip(tails, ends, labels, dirs):
            a, b = np.asarray(tail, float), np.asarray(end, float)
            p = a + np.linspace(0, 0.96, 160)[:, None] * (b - a)
            curve(ax, view, graphs, p[:, 0], p[:, 1], p[:, 2], "black", lw=lw, back=(0, (2, 2)), zorder=4)
            tip = tuple(float(c) for c in view(*b))
            if seen(view, graphs, *b):
                arrow(ax, tuple(float(c) for c in view(*(a + 0.9 * (b - a)))), tip, "black", lw=lw)
            tip_label(ax, tip, d, label, "black", r=4)

    def frame(ax, view, box):
        """Picture limits holding the 3D box ((x^1 lo, hi), (x^2 lo, hi), (y lo, hi)), and no frame."""
        c = np.array(np.meshgrid(*box)).reshape(3, -1)
        X, Y = view(*c)
        ax.set_xlim(X.min(), X.max())
        ax.set_ylim(Y.min(), Y.max())
        ax.set_aspect("equal")
        ax.axis("off")

    return axes3d, frame


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Higher derivatives of $f : \mathbb{R}^n \longrightarrow \mathbb{R}$

    - if $f$ is $C^2$-smooth at $\vec{x} = \vec{a}$ (continuous 2nd order partial derivatives at $\vec{a}$), then

        $$
        f(\vec{x}) = \underbrace{f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}_{\text{good quadratic approximation}} + \underbrace{o\big( \lVert \vec{x} - \vec{a} \rVert^2 \big)}_{\substack{\text{error goes to zero} \\ \text{faster than } \lVert \vec{x} - \vec{a} \rVert^2}}
        $$

    - where

        $$
        \underbrace{Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)}_{\text{derivative matrix}},
        \qquad
        \underbrace{Hf(\vec{a}) = \begin{bmatrix}
        \dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^1 \partial x^n}(\vec{a}) \\
        \vdots & \ddots & \vdots \\
        \dfrac{\partial^2 f}{\partial x^n \partial x^1}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^n \partial x^n}(\vec{a})
        \end{bmatrix} \in \mathrm{Mat}(n \times n)}_{\text{Hessian matrix}}
        $$

    **In this lecture:** application to optimization: finding maximal / minimal values of scalar valued functions

    **References:** MT 3.3
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""## III.1 &nbsp; Local extrema and the second derivative test"""),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$, a point $\vec{a} \in \mathbb{R}^n$ is

    - a **local maximum** of $f$ if there is some open ball $B(\vec{a}, \delta)$ centered at $\vec{a}$ such that

        $$
        f(\vec{x}) \leq f(\vec{a}) \qquad \forall\, \vec{x} \in B(\vec{a}, \delta)
        $$

        (the value of $f$ at $\vec{a}$ is the largest value nearby $\vec{x} = \vec{a}$)

    - a **local minimum** of $f$ if there is some open ball $B(\vec{a}, \delta)$ centered at $\vec{a}$ such that

        $$
        f(\vec{x}) \geq f(\vec{a}) \qquad \forall\, \vec{x} \in B(\vec{a}, \delta)
        $$
    """,
                "Local maximum and local minimum",
            ),
            theorem(
                r"""
    If $f$ is differentiable at $\vec{x} = \vec{a}$ and $\vec{x} = \vec{a}$ is a local maximum or a local minimum of $f$ (a **local extremum** of $f$), then

    $$
    \vec{\nabla} f(\vec{a}) = \vec{0} \in \mathbb{R}^n
    $$

    (equivalently, $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$ is the zero matrix)
    """,
                "Derivative at a local extremum",
            ),
            mo.md(
                r"""
    **Proof.** Let's assume $\vec{a}$ is a local maximum of $f$. Consider

    $$
    g : \mathbb{R} \longrightarrow \mathbb{R}, \qquad t \longmapsto g(t) = f(\vec{a} + t\vec{e}_1)
    $$

    Since $\vec{x} = \vec{a}$ is a local maximum of $f$, $t = 0$ is a local maximum of $g$:

    $$
    f(\vec{a}) \geq f(\vec{x}) \quad \forall\, \vec{x} \in B(\vec{a}, \delta)
    \qquad \Longrightarrow \qquad
    g(0) = f(\vec{a}) \geq g(t) = f(\vec{a} + t\vec{e}_1) \quad \forall\, t \in (-\delta, \delta)
    $$

    Since $f$ is differentiable at $\vec{x} = \vec{a}$, $g$ is differentiable at $t = 0$:

    $$
    g'(0) = \lim_{t \to 0} \frac{g(t) - g(0)}{t} = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{e}_1) - f(\vec{a})}{t} = \frac{\partial f}{\partial x^1}(\vec{a})
    $$

    From single variable calculus

    $$
    \Longrightarrow \qquad g'(0) = \frac{\partial f}{\partial x^1}(\vec{a}) = 0
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, LIGHT, RED, cross_axes, definition, mo, np, tip_label):
    # f has a local maximum at a; its restrictions to the lines a + t e_1 and a + t e_2
    _a, _delta = (1.5, 1.3), 0.7

    def _f(x1, x2):
        u, w = x1 - _a[0], x2 - _a[1]
        return 0.5 + np.cos(1.6 * u) + 0.6 * np.cos(2.4 * w) + 0.25 * u * w

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.2), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1, 1.2])

    _left.set_xlim(-0.3, 3.4)
    _left.set_ylim(-0.3, 2.95)
    _left.set_aspect("equal")
    _left.axis("off")
    _X, _Y = np.meshgrid(np.linspace(-0.3, 3.4, 300), np.linspace(-0.3, 2.95, 300))
    _left.contour(_X, _Y, _f(_X, _Y), levels=np.linspace(-0.6, 1.95, 9), colors=GREY, linewidths=0.6, linestyles="solid")
    cross_axes(_left, (-0.25, 3.35), (-0.25, 2.9), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _left.fill(_a[0] + _delta * np.cos(_th), _a[1] + _delta * np.sin(_th), color=LIGHT, alpha=0.6, lw=0, zorder=1)
    _left.plot(_a[0] + _delta * np.cos(_th), _a[1] + _delta * np.sin(_th), color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=2)
    _left.plot([_a[0] - 1.3, _a[0] + 1.3], [_a[1], _a[1]], color=BLUE, lw=1.6, zorder=3)
    _left.plot([_a[0], _a[0]], [_a[1] - 1.2, _a[1] + 1.2], color=RED, lw=1.6, zorder=3)
    _left.plot(*_a, "o", color="black", ms=4, zorder=5)
    tip_label(_left, _a, -135, r"$\vec{a}$", "black")
    tip_label(_left, (_a[0] + 1.3, _a[1]), 0, r"$\vec{a} + t\vec{e}_1$", BLUE, r=4)
    tip_label(_left, (_a[0], _a[1] + 1.2), 90, r"$\vec{a} + t\vec{e}_2$", RED, r=4)
    tip_label(_left, (_a[0] - 0.62 * _delta, _a[1] - 0.78 * _delta), -130, r"$B(\vec{a}, \delta)$", GREY, r=5, fontsize=12)

    _t = np.linspace(-1.35, 1.35, 300)
    _right.set_xlim(-1.75, 2.6)
    _right.set_ylim(-0.6, 2.55)
    _right.set_aspect("equal")
    _right.axis("off")
    _right.axvspan(-_delta, _delta, color=LIGHT, alpha=0.6, lw=0)
    cross_axes(_right, (-1.7, 1.75), (-0.55, 2.5), "$t$", "$y$")
    _right.plot(_t, np.full_like(_t, _f(*_a)), color=GREY, lw=1.0, ls=(0, (4, 3)))
    _right.plot(_t, _f(_a[0] + _t, _a[1]), color=BLUE, lw=1.6)
    _right.plot(_t, _f(_a[0], _a[1] + _t), color=RED, lw=1.6)
    _right.plot(0, _f(*_a), "o", color="black", ms=4, zorder=5)
    for _s, _name in ((-_delta, r"$-\delta$"), (_delta, r"$\delta$")):
        _right.plot([_s, _s], [-0.05, 0.05], color="black", lw=0.9)
        _right.text(_s, -0.12, _name, ha="center", va="top", fontsize=12, bbox=_box)
    _right.text(1.4, _f(_a[0] + 1.35, _a[1]), r"$f(\vec{a} + t\vec{e}_1)$", color=BLUE, fontsize=12, ha="left", va="center")
    _right.text(1.4, _f(_a[0], _a[1] + 1.35), r"$f(\vec{a} + t\vec{e}_2)$", color=RED, fontsize=12, ha="left", va="center")
    _right.text(1.4, _f(*_a), r"$y = f(\vec{a})$", color=GREY, fontsize=12, ha="left", va="center")

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    Repeat with $g(t) = f(\vec{a} + t\vec{e}_i)$ for each $i = 1, \dots, n$

    $$
    \Longrightarrow \qquad \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\ \vdots \\ \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 0 \\ \vdots \\ 0 \end{bmatrix} = \vec{0} \qquad \square
    $$
    """
            ),
            definition(
                r"""
    A point $\vec{a} \in \mathbb{R}^n$ such that $\vec{\nabla} f(\vec{a}) = \vec{0}$ is called a **critical point** of $f$.
    """,
                "Critical point",
            ),
            mo.md(
                r"""
    **Remark.** Local extremum where $f$ is differentiable &nbsp; $\Longrightarrow$ &nbsp; critical point!

    Critical point &nbsp; $\nRightarrow$ &nbsp; local extremum!
    """
            ),
            definition(
                r"""
    A critical point of $f$ that is not a local extremum is called a **saddle point**.
    """,
                "Saddle point",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = -(x^1)^2 + (x^2)^2$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} -2x^1 \\ 2x^2 \end{bmatrix} \qquad \Longrightarrow \qquad \vec{x} = \vec{0} \text{ is a critical point!}
    $$

    $f(\vec{0}) = -0^2 + 0^2 = 0$, but

    $$
    \begin{aligned}
    f(\vec{x}) &= -t^2 < 0 \quad \text{for } \vec{x} = t\vec{e}_1 = \begin{bmatrix} t \\ 0 \end{bmatrix}, \text{ with } t \neq 0 &&\leadsto \quad \vec{0} \text{ not min!} \\[6pt]
    f(\vec{x}) &= s^2 > 0 \quad \text{for } \vec{x} = s\vec{e}_2 = \begin{bmatrix} 0 \\ s \end{bmatrix}, \text{ with } s \neq 0 &&\leadsto \quad \vec{0} \text{ not max!}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    theta = mo.ui.slider(0, 180, 5, value=30, label=r"direction $\theta$ of $\vec{v}$ (degrees)", show_value=True)
    return (theta,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, Graph, RED, View, axes3d, cross_axes, curve, frame, math, mo, np, num, surface, table, theta, tip_label):
    _th = math.radians(theta.value)
    _v = (round(math.cos(_th), 12) + 0.0, round(math.sin(_th), 12) + 0.0)
    _c = round(-math.cos(2 * _th), 12) + 0.0  # f(t v) = c t^2

    def _f(x1, x2):
        return -(x1**2) + x2**2

    _R = 1.0
    _view = View(35, 28, 0.55)
    _g = [Graph(_f, lambda x1, x2: (np.abs(x1) <= _R + 1e-9) & (np.abs(x2) <= _R + 1e-9))]

    _fig = Figure(figsize=(FULL, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.25, 1])

    # graph(f) over the square |x^1|, |x^2| <= 1, with the sections along e_1, e_2 and v
    frame(_left, _view, ((-1.05, 1.75), (-1.05, 1.75), (-1.05, 1.45)))
    _u1, _u2 = np.meshgrid(np.linspace(-_R, _R, 41), np.linspace(-_R, _R, 41), indexing="ij")
    surface(_left, _view, _g[0], _u1, _u2)
    _t = np.linspace(-_R, _R, 161)
    for _k in np.linspace(-_R, _R, 9):
        _lw = 1.2 if abs(abs(_k) - _R) < 1e-9 else 0.5
        curve(_left, _view, _g, _t, np.full_like(_t, _k), _f(_t, _k), BLUE, lw=_lw, back=None)
        curve(_left, _view, _g, np.full_like(_t, _k), _t, _f(_k, _t), BLUE, lw=_lw, back=None)
    curve(_left, _view, _g, _t, 0 * _t, _f(_t, 0), GREY, lw=1.3)
    curve(_left, _view, _g, 0 * _t, _t, _f(0, _t), GREY, lw=1.3)
    _s = np.linspace(-1, 1, 161) * _R / max(abs(_v[0]), abs(_v[1]))
    curve(_left, _view, _g, _s * _v[0], _s * _v[1], _c * _s**2, RED, lw=1.8)
    axes3d(_left, _view, _g, ((1.7, 0, 0), (0, 1.7, 0), (0, 0, 1.4)), ("$x^1$", "$x^2$", "$y$"), (-90, -60, 90))
    _left.plot(*_view(0, 0, 0), "o", color="black", ms=4, zorder=6)

    # the sections as graphs of single variable functions
    _right.set_xlim(-1.3, 2.35)
    _right.set_ylim(-1.35, 1.45)
    _right.set_aspect("equal")
    _right.axis("off")
    cross_axes(_right, (-1.25, 1.45), (-1.3, 1.4), "$t$", "$y$")
    _right.plot(_t, -(_t**2), color=GREY, lw=1.0, ls=(0, (4, 3)))
    _right.plot(_t, _t**2, color=GREY, lw=1.0, ls=(0, (4, 3)))
    _right.plot(_t, _c * _t**2, color=RED, lw=1.6)
    _right.plot(0, 0, "o", color="black", ms=4, zorder=5)
    tip_label(_right, (1.0, 1.0), 0, r"$f(t\vec{e}_2) = t^2$", GREY, r=4, fontsize=12)
    tip_label(_right, (1.0, -1.0), 0, r"$f(t\vec{e}_1) = -t^2$", GREY, r=4, fontsize=12)
    if abs(abs(_c) - 1) > 0.15:  # (for |c| = 1 the curve is one of the two grey ones)
        tip_label(_right, (1.0, _c), 0 if abs(_c) > 0.3 else 50, r"$f(t\vec{v})$", RED, r=4, fontsize=12)

    _kind = "local maximum" if _c < 0 else "local minimum" if _c > 0 else r"neither ($f(t\vec{v}) = 0$ for all $t$)"
    mo.vstack(
        [
            mo.hstack([theta], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{v} = \begin{bmatrix} \cos\theta \\ \sin\theta \end{bmatrix}$", rf"$\textcolor{{{RED}}}{{\begin{{bmatrix}} {num(_v[0])} \\ {num(_v[1])} \end{{bmatrix}}}}$"),
                    (r"$f(t\vec{v}) = \big( \sin^2\theta - \cos^2\theta \big)\, t^2$", rf"$\textcolor{{{RED}}}{{{num(_c)}\, t^2}}$"),
                    (r"$t = 0$ for $t \longmapsto f(t\vec{v})$", _kind),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; $\mathrm{graph}(f)$ looks like a horse saddle

    Given a critical point, how do we distinguish its type (local max, local min, saddle)?

    $\leadsto$ &nbsp; look at the Hessian matrix!

    $\leadsto$ &nbsp; if $\vec{a}$ is a critical point of $f$ ($Df(\vec{a}) = 0 \in \mathrm{Mat}(1 \times n)$)

    $$
    \underbrace{f(\vec{x}) \approx f(\vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}_{\text{near } \vec{x} = \vec{a}}
    \qquad \Big( \tfrac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a}) \text{ determines the behavior of } f \text{ near } \vec{x} = \vec{a}! \Big)
    $$

    **Recall:** $f : \mathbb{R} \longrightarrow \mathbb{R}$ $C^2$-smooth with $f'(a) = 0$

    - $f''(a) < 0$ &nbsp; $\Longrightarrow$ &nbsp; local maximum
    - $f''(a) > 0$ &nbsp; $\Longrightarrow$ &nbsp; local minimum
    - $f''(a) = 0$ &nbsp; $\Longrightarrow$ &nbsp; need more information

    because near $x = a$

    $$
    f(x) = f(a) + f'(a)(x - a) + \frac{1}{2} f''(a)(x - a)^2 + \underbrace{o\big( (x - a)^2 \big)}_{\substack{\text{error goes to zero} \\ \text{faster than } (x - a)^2}}
    $$

    and if $a$ is a critical point

    $$
    \Longrightarrow \qquad f(x) \approx f(a) + \frac{1}{2} f''(a)(x - a)^2
    $$

    - if $f''(a) < 0$ &nbsp; $\leadsto$ &nbsp; parabola opens downwards &nbsp; $\Longrightarrow$ &nbsp; $a$ is local max
    - if $f''(a) > 0$ &nbsp; $\leadsto$ &nbsp; parabola opens upwards &nbsp; $\Longrightarrow$ &nbsp; $a$ is local min
    - if $f''(a) = 0$ &nbsp; $\leadsto$ &nbsp; parabola degenerates to a horizontal line … &nbsp; $\Longrightarrow$ &nbsp; not sufficient info
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, cross_axes, mo, np):
    # one function with three critical points: f''(a) > 0, f''(a) = 0 and f''(a) < 0
    def _f(x):
        return 0.25 + 2 * (x / 2) ** 3 - 1.2 * (x / 2) ** 5

    def _d2(x):
        return (12 * (x / 2) - 24 * (x / 2) ** 3) / 4

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-3.3, 4.6)
    _ax.set_ylim(-1.25, 1.75)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-3.25, 3.4), (-1.2, 1.7), "$x$", "$y$")
    _x = np.linspace(-2.85, 2.85, 400)
    _ax.plot(_x, _f(_x), color=BLUE, lw=1.6)
    for _a, _name, _dy in ((-2, r"$f''(a) > 0$", -1), (0, r"$f''(a) = 0$", 1), (2, r"$f''(a) < 0$", 1)):
        _w = np.linspace(_a - 0.75, _a + 0.75, 100)
        _ax.plot(_w, np.full_like(_w, _f(_a)), color=GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.plot(_w, _f(_a) + 0.5 * _d2(_a) * (_w - _a) ** 2, color=GREEN, lw=1.4)
        _ax.plot(_a, _f(_a), "o", color="black", ms=4, zorder=5)
        _ax.annotate(_name, (_a, _f(_a)), textcoords="offset points", xytext=(-6 if _a == 0 else 0, 12 * _dy), ha="right" if _a == 0 else "center", va="bottom" if _dy > 0 else "top", fontsize=12, bbox=_box)
    _ax.text(2.95, float(_f(2.85)), r"$y = f(x)$", color=BLUE, fontsize=12, ha="left", va="center")
    _ax.text(-3.25, 1.6, r"$y = f(a) + \frac{1}{2} f''(a)(x - a)^2$", color=GREEN, fontsize=12, ha="left", va="center")
    _ax.text(2.85, float(_f(2)), r"$y = f(a)$", color=GREY, fontsize=12, ha="left", va="center")

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; we will generalize this for $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$

    $\leadsto$ &nbsp; for $n > 2$ we need tools from Linear Algebra
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ $C^2$-smooth at a critical point $\vec{x} = \vec{a}$

    $$
    f(\vec{x}) \approx f(\vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a}) = q(\vec{x})
    $$

    Let's write $Hf(\vec{a}) = \begin{bmatrix} A & B \\ C & D \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$, that is, let

    $$
    A = \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}), \qquad
    B = \frac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{a}), \qquad
    C = \frac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{a}) = B, \qquad
    D = \frac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{a})
    $$

    $$
    \Longrightarrow \qquad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} \Big( A \underbrace{(x^1 - a^1)^2}_{(v^1)^2} + 2B \underbrace{(x^1 - a^1)(x^2 - a^2)}_{v^1 v^2} + D \underbrace{(x^2 - a^2)^2}_{(v^2)^2} \Big)
    $$

    ① &nbsp; if $A \neq 0$ &nbsp; $\leadsto$ &nbsp; complete the square

    $$
    \Longrightarrow \qquad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} \left( A \left( v^1 + \frac{B}{A} v^2 \right)^2 + \frac{AD - B^2}{A} (v^2)^2 \right)
    $$

    - if $\underbrace{A < 0 \text{ and } AD - B^2 > 0}_{\text{negative definite}}$, then $\mathrm{graph}(q)$ is a paraboloid opening downwards
    - if $\underbrace{A > 0 \text{ and } AD - B^2 > 0}_{\text{positive definite}}$, then $\mathrm{graph}(q)$ is a paraboloid opening upwards
    - if $\underbrace{A \neq 0 \text{ and } AD - B^2 < 0}_{\text{indefinite}}$, then $\mathrm{graph}(q)$ is a horse saddle
    - if $A \neq 0$ and $\underbrace{AD - B^2 = 0}_{\text{degenerate}}$

        $$
        \Longrightarrow \qquad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} A \left( v^1 + \frac{B}{A} v^2 \right)^2
        \qquad \Longrightarrow \qquad \mathrm{graph}(q) \text{ contains a horizontal line …} \quad (\text{is degenerate})
        $$

    ② &nbsp; if $A = 0$

    - $B \neq 0$ &nbsp; ($\Longleftrightarrow$ &nbsp; $AD - B^2 < 0$) &nbsp; $\Longrightarrow$ &nbsp; $q(\vec{x}) = f(\vec{a}) + \frac{1}{2} (2B v^1 + D v^2) v^2$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ is a horse saddle
    - $B = 0$ &nbsp; ($\Longleftrightarrow$ &nbsp; $AD - B^2 = 0$) &nbsp; $\Longrightarrow$ &nbsp; $q(\vec{x}) = f(\vec{a}) + \frac{1}{2} D (v^2)^2$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ contains a horizontal line
    """)
    return




@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, Graph, View, axes3d, curve, frame, mo, np, surface, tip_label):
    # graph(q) near a in the four cases, each with its point (a, f(a)): over a disc, or over a square
    _a = (1.0, 1.8)
    _cases = (
        ("negative definite", -2.4, 0.5, -2.0, 2.2, False),
        ("positive definite", 2.4, 0.5, 2.0, 0.4, False),
        ("indefinite", -1.4, 0.3, 1.8, 1.2, True),
        ("degenerate", 1.6, 0.0, 0.0, 0.7, True),
    )
    _view = View(28, 24, 0.6)
    _phi = np.linspace(0, 2 * np.pi, 241)
    _t = np.linspace(0, 1, 60)
    _w = np.linspace(-1, 1, 121)
    _s = np.linspace(0, 1, 80)

    def _panel(ax, name, A, B, D, fa, square):
        def q(x1, x2):
            v1, v2 = x1 - _a[0], x2 - _a[1]
            return fa + 0.5 * (A * v1**2 + 2 * B * v1 * v2 + D * v2**2)

        if square:
            g = [Graph(q, lambda x1, x2: (np.abs(x1 - _a[0]) <= 0.85 + 1e-9) & (np.abs(x2 - _a[1]) <= 0.85 + 1e-9))]
            u1, u2 = np.meshgrid(_a[0] + 0.85 * _w[::4], _a[1] + 0.85 * _w[::4], indexing="ij")
        else:
            g = [Graph(q, lambda x1, x2: (x1 - _a[0]) ** 2 + (x2 - _a[1]) ** 2 <= 1 + 1e-9)]
            r, p = np.meshgrid(np.linspace(0, 1, 13), np.linspace(0, 2 * np.pi, 73), indexing="ij")
            u1, u2 = _a[0] + r * np.cos(p), _a[1] + r * np.sin(p)
        frame(ax, _view, ((-0.2, 2.2), (-0.2, 3.2), (-0.2, 2.9)))
        surface(ax, _view, g[0], u1, u2)
        if square:
            for k in np.linspace(-0.85, 0.85, 7):
                lw = 1.2 if abs(abs(k) - 0.85) < 1e-9 else 0.5
                c1, c2 = _a[0] + k + 0 * _w, _a[1] + 0.85 * _w
                curve(ax, _view, g, c1, c2, q(c1, c2), BLUE, lw=lw, back=None)
                c1, c2 = _a[0] + 0.85 * _w, _a[1] + k + 0 * _w
                curve(ax, _view, g, c1, c2, q(c1, c2), BLUE, lw=lw, back=None)
        else:
            for rr in (1 / 3, 2 / 3, 1):
                c1, c2 = _a[0] + rr * np.cos(_phi), _a[1] + rr * np.sin(_phi)
                curve(ax, _view, g, c1, c2, q(c1, c2), BLUE, lw=1.2 if rr == 1 else 0.5, back=None)
            for ang in np.radians(np.arange(0, 360, 30)):
                c1, c2 = _a[0] + _t * np.cos(ang), _a[1] + _t * np.sin(ang)
                curve(ax, _view, g, c1, c2, q(c1, c2), BLUE, lw=0.5, back=None)
        if name == "degenerate":  # the horizontal line v^1 + (B / A) v^2 = 0 at height f(a)
            d = np.array([-B, A]) / np.hypot(A, B)
            curve(ax, _view, g, _a[0] + 0.85 * _w * d[0], _a[1] + 0.85 * _w * d[1], np.full_like(_w, fa), GREEN, lw=1.8)
        # the point a below (a, f(a)), and f(a) on the y-axis
        curve(ax, _view, g, np.full_like(_s, _a[0]), np.full_like(_s, _a[1]), _s * fa, GREY, lw=0.9, ls=(0, (3, 2)), back=None)
        curve(ax, _view, g, _s * _a[0], _s * _a[1], np.full_like(_s, fa), GREY, lw=0.9, ls=(0, (3, 2)), back=None)
        axes3d(ax, _view, g, ((2.2, 0, 0), (0, 3.2, 0), (0, 0, 2.9)), ("$x^1$", "$x^2$", "$y$"), (-150, -20, 90))
        for p in ((_a[0], _a[1], 0), (_a[0], _a[1], fa)):
            ax.plot(*_view(*p), "o", color="black", ms=3.5, zorder=6)
        tip_label(ax, tuple(float(c) for c in _view(_a[0], _a[1], 0)), -60, r"$\vec{a}$", "black", r=4, fontsize=12)
        tip_label(ax, tuple(float(c) for c in _view(0, 0, fa)), 180, r"$f(\vec{a})$", "black", r=4, fontsize=12)
        ax.text(0.5, 0.0, name, transform=ax.transAxes, ha="center", va="bottom", fontsize=12)

    _fig = Figure(figsize=(FULL, 5.6), layout="constrained")
    for _ax, _case in zip(_fig.subplots(2, 2).flat, _cases):
        _panel(_ax, *_case)
    _fig
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    $H = \begin{bmatrix} A & B \\ B & D \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$ is called

    - **negative definite** if $\det H > 0$ and $A < 0$
    - **positive definite** if $\det H > 0$ and $A > 0$
    - **indefinite** if $\det H < 0$
    - **degenerate** if $\det H = 0$
    """,
        "Definite, indefinite and degenerate matrices",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    hA = mo.ui.slider(-2, 2, 0.25, value=1, label="$A$", show_value=True)
    hB = mo.ui.slider(-2, 2, 0.25, value=0.5, label="$B$", show_value=True)
    hD = mo.ui.slider(-2, 2, 0.25, value=1, label="$D$", show_value=True)
    return hA, hB, hD


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, Graph, View, axes3d, cross_axes, curve, frame, hA, hB, hD, mo, np, surface, table):
    _A, _B, _D = hA.value, hB.value, hD.value
    _det = _A * _D - _B**2  # exact: the slider values are multiples of 1/4

    def _q(x1, x2):
        return 0.5 * (_A * x1**2 + 2 * _B * x1 * x2 + _D * x2**2)

    if _det > 0:
        _kind, _shape = ("negative definite", "paraboloid opening downwards") if _A < 0 else ("positive definite", "paraboloid opening upwards")
    elif _det < 0:
        _kind, _shape = "indefinite", "horse saddle"
    else:
        _kind, _shape = "degenerate", "contains a horizontal line"

    _view = View(35, 28, 0.5)
    _g = [Graph(_q, lambda x1, x2: x1**2 + x2**2 <= 1 + 1e-9)]
    _fig = Figure(figsize=(FULL, 3.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1.5, 1])

    # graph(q) over the unit disc, at a fixed scale
    frame(_left, _view, ((-1.05, 1.5), (-1.05, 1.5), (-2.05, 2.05)))
    _r, _p = np.meshgrid(np.linspace(0, 1, 15), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    surface(_left, _view, _g[0], _r * np.cos(_p), _r * np.sin(_p))
    _phi = np.linspace(0, 2 * np.pi, 241)
    for _rr in (0.25, 0.5, 0.75, 1):
        _c1, _c2 = _rr * np.cos(_phi), _rr * np.sin(_phi)
        curve(_left, _view, _g, _c1, _c2, _q(_c1, _c2), BLUE, lw=1.2 if _rr == 1 else 0.5, back=None)
    _t = np.linspace(-1, 1, 121)
    for _ang in np.radians(np.arange(0, 180, 30)):
        _c1, _c2 = _t * np.cos(_ang), _t * np.sin(_ang)
        curve(_left, _view, _g, _c1, _c2, _q(_c1, _c2), BLUE, lw=0.5, back=None)
    axes3d(_left, _view, _g, ((1.6, 0, 0), (0, 1.6, 0), (0, 0, 1.9)), ("$x^1$", "$x^2$", "$y$"), (-120, -40, 90))
    _left.plot(*_view(0, 0, 0), "o", color="black", ms=4, zorder=6)

    # level sets of q (negative levels dashed)
    _right.set_xlim(-1.25, 1.35)
    _right.set_ylim(-1.2, 1.3)
    _right.set_aspect("equal")
    _right.axis("off")
    _X, _Y = np.meshgrid(np.linspace(-1, 1, 301), np.linspace(-1, 1, 301))
    _Q = np.where(_X**2 + _Y**2 <= 1, _q(_X, _Y), np.nan)
    if np.nanmax(np.abs(_Q)) > 1e-9:
        _right.contour(_X, _Y, _Q, levels=[-1.5, -1, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1, 1.5], colors=GREY, linewidths=0.8)
    _right.plot(np.cos(_phi), np.sin(_phi), color=GREY, lw=0.6)
    cross_axes(_right, (-1.2, 1.3), (-1.15, 1.25), "$x^1$", "$x^2$")
    _right.plot(0, 0, "o", color="black", ms=4, zorder=5)
    _right.text(-1.2, -1.15, "level sets of $q$", color=GREY, fontsize=12, ha="left", va="bottom", bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    mo.vstack(
        [
            mo.hstack([hA, hB, hD], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$q(\vec{x})$, with $\vec{a} = \vec{0}$ and $f(\vec{a}) = 0$", r"$\frac{1}{2} \big( A (x^1)^2 + 2B\, x^1 x^2 + D (x^2)^2 \big)$"),
                    (r"$Hf(\vec{a}) = \begin{bmatrix} A & B \\ B & D \end{bmatrix}$", rf"$\begin{{bmatrix}} {_A:g} & {_B:g} \\ {_B:g} & {_D:g} \end{{bmatrix}}$"),
                    (r"$\det Hf(\vec{a}) = AD - B^2$", rf"${_det:g}$"),
                    (r"$Hf(\vec{a})$ is", _kind),
                    (r"$\mathrm{graph}(q)$", rf"$\textcolor{{{BLUE}}}{{\text{{{_shape}}}}}$"),
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
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ $C^2$-smooth at a critical point $\vec{x} = \vec{a}$

    - if $Hf(\vec{a})$ is negative definite &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is local max
    - if $Hf(\vec{a})$ is positive definite &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is local min
    - if $Hf(\vec{a})$ is indefinite &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is a saddle
    - if $Hf(\vec{a})$ is degenerate &nbsp; $\Longrightarrow$ &nbsp; not sufficient info …
    """,
                "Second derivative test",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^3 - 3x^1 x^2 + (x^2)^3$

    $\leadsto$ &nbsp; critical points:

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 3(x^1)^2 - 3x^2 \\ -3x^1 + 3(x^2)^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    \quad \Longleftrightarrow \quad
    \begin{cases} x^2 = (x^1)^2 \\ x^1 = (x^2)^2 \end{cases}
    \quad \Longleftrightarrow \quad
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \underbrace{\begin{bmatrix} 0 \\ 0 \end{bmatrix}}_{\vec{a}} \text{ or } \underbrace{\begin{bmatrix} 1 \\ 1 \end{bmatrix}}_{\vec{b}}
    $$

    $\leadsto$ &nbsp; Hessian matrix:

    $$
    Hf(\vec{x}) = \begin{bmatrix} 6x^1 & -3 \\ -3 & 6x^2 \end{bmatrix}
    $$

    At $\vec{a} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$:

    $$
    Hf(\vec{a}) = \begin{bmatrix} 0 & -3 \\ -3 & 0 \end{bmatrix}
    \qquad \Longrightarrow \qquad \underbrace{\det Hf(\vec{a}) = -9 < 0}_{\text{indefinite}}
    \qquad \Longrightarrow \qquad \vec{a} \text{ is a saddle}
    $$

    At $\vec{b} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$:

    $$
    Hf(\vec{b}) = \begin{bmatrix} 6 & -3 \\ -3 & 6 \end{bmatrix}
    \qquad \Longrightarrow \qquad \underbrace{\det Hf(\vec{b}) = 27 > 0, \quad \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{b}) = 6 > 0}_{\text{positive definite}}
    \qquad \Longrightarrow \qquad \vec{b} \text{ is local min}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, np, tip_label):
    # level sets of f around the saddle a and the local minimum b
    def _f(x1, x2):
        return x1**3 - 3 * x1 * x2 + x2**3

    _fig = Figure(figsize=(HALF + 1.0, HALF + 0.6), layout="constrained")
    _ax = _fig.subplots()
    _X, _Y = np.meshgrid(np.linspace(-1.6, 2.2, 500), np.linspace(-1.6, 2.2, 500))
    _ax.contour(_X, _Y, _f(_X, _Y), levels=[-0.9, -0.6, -0.3, 0.3, 0.8, 1.6, 3], colors=GREY, linewidths=0.6, linestyles="solid")
    _ax.contour(_X, _Y, _f(_X, _Y), levels=[0], colors=BLUE, linewidths=1.4, linestyles="solid")
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.grid(True, color=LIGHT, lw=0.6)
    _ax.set_axisbelow(True)
    _ax.set_xlim(-1.6, 2.2)
    _ax.set_ylim(-1.6, 2.2)
    _ax.set_aspect("equal")
    _ax.set_xticks([-1, 0, 1, 2])
    _ax.set_yticks([-1, 0, 1, 2])
    _ax.set_xlabel("$x^1$")
    _ax.set_ylabel("$x^2$", rotation=0, labelpad=10)
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)
    for _p, _name, _d in (((0, 0), r"$\vec{a}$", -135), ((1, 1), r"$\vec{b}$", -45)):
        _ax.plot(*_p, "o", color="black", ms=4, zorder=5)
        tip_label(_ax, _p, _d, _name, "black")
    tip_label(_ax, (1.5, 1.5), 45, r"$f^{-1}(0)$", BLUE, r=5, fontsize=12)
    _ax.text(-1.55, -1.55, "level sets of $f$", color=GREY, fontsize=12, ha="left", va="bottom", bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $\vec{a}$ is a local maximum (minimum) of $f$ if $f(\vec{x}) \leq f(\vec{a})$ ($f(\vec{x}) \geq f(\vec{a})$) for all $\vec{x}$ in some open ball $B(\vec{a}, \delta)$
    - a local extremum where $f$ is differentiable is a critical point, $\vec{\nabla} f(\vec{a}) = \vec{0}$; a critical point that is not a local extremum is a saddle point
    - near a critical point

        $$
        f(\vec{x}) \approx f(\vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})
        $$

    - $H = \begin{bmatrix} A & B \\ B & D \end{bmatrix}$ is negative definite if $\det H > 0$ and $A < 0$, positive definite if $\det H > 0$ and $A > 0$, indefinite if $\det H < 0$, and degenerate if $\det H = 0$
    - second derivative test for $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ at a critical point $\vec{a}$: $Hf(\vec{a})$ negative definite $\Longrightarrow$ local max; positive definite $\Longrightarrow$ local min; indefinite $\Longrightarrow$ saddle point; degenerate $\Longrightarrow$ not sufficient info

    **Next:** global extrema on closed and bounded domains
    """)
    return


if __name__ == "__main__":
    app.run()
