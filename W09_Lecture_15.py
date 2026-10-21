import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 15 · Global extrema on closed and bounded domains", css_file="bs101.css")


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
    header("Lecture 15", "Week 09", "Lecture 15 · Global extrema on closed and bounded domains")
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
def _(BLUE, FULL, Figure, Graph, View, axes3d, curve, frame, math, mo, np, surface, theorem, tip_label):
    def _f(x1, x2):
        return x1**2 * np.exp(-(x1**2)) + x2**2

    _L, _W = 2.6, 0.8
    _view = View(-70, 36, 1.0)
    _g = [Graph(_f, lambda x1, x2: (np.abs(x1) <= _L + 1e-9) & (np.abs(x2) <= _W + 1e-9))]
    _fig = Figure(figsize=(FULL, 3.3), layout="constrained")
    _ax = _fig.subplots()
    frame(_ax, _view, ((-2.75, 3.0), (-0.85, 1.1), (-0.05, 1.35)))
    _u1, _u2 = np.meshgrid(np.linspace(-_L, _L, 105), np.linspace(-_W, _W, 33), indexing="ij")
    surface(_ax, _view, _g[0], _u1, _u2)
    _s1, _s2 = np.linspace(-_L, _L, 261), np.linspace(-_W, _W, 81)
    for _k in np.linspace(-_W, _W, 9):
        _edge = abs(abs(_k) - _W) < 1e-9
        curve(_ax, _view, _g, _s1, np.full_like(_s1, _k), _f(_s1, _k), BLUE, lw=1.2 if _edge else 0.5, back=None)
    curve(_ax, _view, _g, _s1, 0 * _s1, _f(_s1, 0), BLUE, lw=1.6, back=None)
    for _k in np.linspace(-_L, _L, 14):
        _edge = abs(abs(_k) - _L) < 1e-9
        curve(_ax, _view, _g, np.full_like(_s2, _k), _s2, _f(_k, _s2), BLUE, lw=1.2 if _edge else 0.5, back=None)
    axes3d(_ax, _view, _g, ((3.0, 0, 0), (0, 1.1, 0), (0, 0, 1.3)), ("$x^1$", "$x^2$", "$y$"), (-60, 60, 90), tails=((-2.75, 0, 0), (0, 0, 0), (0, 0, 0)))
    for _x, _name, _d in ((-1, "saddle", 120), (1, "saddle", 60), (0, "global minimum", -60)):
        _p = tuple(float(c) for c in _view(_x, 0, _f(_x, 0)))
        _ax.plot(*_p, "o", color="black", ms=4, zorder=6)
        tip_label(_ax, _p, _d, _name, "black", r=6, fontsize=12)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Local extrema via 2nd derivative test
    """
            ),
            theorem(
                r"""
    If $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is $C^2$-smooth at a critical point $\vec{x} = \vec{a}$ &nbsp; ($\vec{\nabla} f(\vec{a}) = \vec{0}$)

    - if $Hf(\vec{a})$ is **negative definite**, then $\vec{a}$ is local max

        $\Big( \det Hf(\vec{a}) > 0$ and $\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) < 0 \Big)$

    - if $Hf(\vec{a})$ is **positive definite**, then $\vec{a}$ is local min

        $\Big( \det Hf(\vec{a}) > 0$ and $\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) > 0 \Big)$

    - if $Hf(\vec{a})$ is **indefinite**, then $\vec{a}$ is a saddle point &nbsp; $\big( \det Hf(\vec{a}) < 0 \big)$
    - if $Hf(\vec{a})$ is **degenerate**, we need more info &nbsp; $\big( \det Hf(\vec{a}) = 0 \big)$

        (could be local max, local min, or saddle …)
    """,
                "Second derivative test",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 e^{-(x^1)^2} + (x^2)^2$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 e^{-(x^1)^2} - 2(x^1)^3 e^{-(x^1)^2} \\ 2x^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    $$

    $$
    \Longleftrightarrow \qquad x^2 = 0, \quad x^1 \big( 1 - (x^1)^2 \big) e^{-(x^1)^2} = 0
    \qquad \Longleftrightarrow \qquad x^2 = 0, \quad x^1 \in \{ -1, 0, 1 \}
    $$

    $$
    Hf(\vec{x}) = \begin{bmatrix} \big( 4(x^1)^4 - 10(x^1)^2 + 2 \big) e^{-(x^1)^2} & 0 \\ 0 & 2 \end{bmatrix}
    $$

    At $\vec{a} = \begin{bmatrix} -1 \\ 0 \end{bmatrix}$ and $\vec{b} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$:

    $$
    Hf(\vec{a}) = Hf(\vec{b}) = \begin{bmatrix} -4e^{-1} & 0 \\ 0 & 2 \end{bmatrix} \qquad \text{indefinite} \quad \Longrightarrow \quad \text{saddle}
    $$

    At $\vec{0} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$:

    $$
    Hf(\vec{0}) = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix} \qquad \text{positive definite} \quad \Longrightarrow \quad \text{minimum}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; global minimum: &nbsp; $f(\vec{0}) = 0 < f(\vec{x}) \quad \forall\, \vec{x} \neq \vec{0}$!

    **In this lecture:** global extrema

    **References:** MT 3.3
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""## III.2 &nbsp; Global extrema on closed and bounded domains"""),
            definition(
                r"""
    Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, a point $\vec{a} \in D$ is

    - a **global maximum** of $f$ if

        $$
        f(\vec{x}) \leq f(\vec{a}) \qquad \forall\, \vec{x} \in D
        $$

    - a **global minimum** of $f$ if

        $$
        f(\vec{x}) \geq f(\vec{a}) \qquad \forall\, \vec{x} \in D
        $$
    """,
                "Global maximum and global minimum",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; to determine global extrema, we will also need to look at properties of the domain of $f$!

    **Example.** &nbsp; $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$

    $\Longrightarrow$ &nbsp; $\begin{bmatrix} 0 \\ 0 \end{bmatrix}$ is global minimum and there is no global maximum

    $g : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $g\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ &nbsp; for

    $$
    D = \left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; 0 < x^1 \leq 1,\ 0 < x^2 \leq 1 \,\right\}
    $$

    $\Longrightarrow$ &nbsp; there is no global minimum; &nbsp; $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ is the global maximum!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, Graph, LIGHT, View, axes3d, cross_axes, curve, frame, mo, np, surface, tip_label):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.5), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1, 1.35])

    # D = (0, 1] x (0, 1]: the edges on the axes are not in D
    def _domain(ax, view=None):
        P = (lambda x1, x2: tuple(float(c) for c in view(x1, x2, 0))) if view else (lambda x1, x2: (x1, x2))
        sq = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
        ax.fill(*zip(*sq), color=LIGHT, lw=0, zorder=0)
        ax.plot(*zip(P(1, 0), P(1, 1), P(0, 1)), color=BLUE, lw=1.4, zorder=2)
        ax.plot(*zip(P(0, 1), P(0, 0), P(1, 0)), color=BLUE, lw=1.4, ls=(0, (3, 2)), zorder=2)
        for c in ((0, 0), (1, 0), (0, 1)):
            ax.plot(*P(*c), "o", ms=5, mfc="white", mec=BLUE, mew=1.2, zorder=3)
        ax.plot(*P(1, 1), "o", ms=5, color=BLUE, zorder=3)
        return P

    _left.set_xlim(-0.2, 1.45)
    _left.set_ylim(-0.2, 1.35)
    _left.set_aspect("equal")
    _left.axis("off")
    cross_axes(_left, (-0.15, 1.4), (-0.15, 1.3), "$x^1$", "$x^2$")
    _domain(_left)
    _a = (0.55, 0.75)
    _left.plot([0, _a[0] / _a[1]], [0, 1], color=GREY, lw=0.9, ls=(0, (4, 3)), zorder=1)
    _left.plot(*_a, "o", color="black", ms=4, zorder=4)
    _left.plot(_a[0] / 2, _a[1] / 2, "o", color="black", ms=4, zorder=4)
    tip_label(_left, _a, 0, r"$\vec{a}$", "black")
    tip_label(_left, (_a[0] / 2, _a[1] / 2), 0, r"$\vec{x}$", "black")
    tip_label(_left, (1, 0.5), 0, "$D$", BLUE)
    _left.text(1, -0.05, "$1$", ha="center", va="top", fontsize=12, bbox=_box)
    _left.text(-0.05, 1, "$1$", ha="right", va="center", fontsize=12, bbox=_box)

    # graph(f) over the disc of radius 3/2, with graph(g) above D in a deeper tone
    def _f(x1, x2):
        return x1**2 + x2**2

    def _inD(x1, x2):
        return (x1 > 0) & (x1 <= 1) & (x2 > 0) & (x2 <= 1)

    _R = 1.5
    _view = View(45, 14, 0.55)
    _g = [Graph(_f, lambda x1, x2: x1**2 + x2**2 <= _R**2 + 1e-9)]
    frame(_right, _view, ((-1.55, 1.95), (-1.55, 1.95), (-0.1, 2.6)))
    _P = _domain(_right, _view)
    _r, _p = np.meshgrid(np.linspace(0, _R, 31), np.linspace(0, 2 * np.pi, 145), indexing="ij")
    surface(_right, _view, _g[0], _r * np.cos(_p), _r * np.sin(_p), tint=_inD)
    for _k in np.arange(-1.5, 1.51, 0.25):
        _h = np.sqrt(max(_R**2 - _k**2, 0.0))
        _w = np.linspace(-_h, _h, 161)
        for _c1, _c2 in ((np.full_like(_w, _k), _w), (_w, np.full_like(_w, _k))):
            _in = _inD(_c1, _c2)
            curve(_right, _view, _g, np.where(_in, np.nan, _c1), _c2, _f(_c1, _c2), GREY, lw=0.4, back=None)
            curve(_right, _view, _g, np.where(_in, _c1, np.nan), _c2, _f(_c1, _c2), BLUE, lw=0.6, back=None)
    _phi = np.linspace(0, 2 * np.pi, 241)
    curve(_right, _view, _g, _R * np.cos(_phi), _R * np.sin(_phi), np.full_like(_phi, _R**2), GREY, lw=1.0, back=None)
    _s = np.linspace(0, 1, 81)
    _one = np.ones_like(_s)
    curve(_right, _view, _g, _one, _s, _f(1, _s), BLUE, lw=1.4)
    curve(_right, _view, _g, _s, _one, _f(_s, 1), BLUE, lw=1.4)
    curve(_right, _view, _g, 0 * _s, _s, _f(0, _s), BLUE, lw=1.4, ls=(0, (3, 2)))
    curve(_right, _view, _g, _s, 0 * _s, _f(_s, 0), BLUE, lw=1.4, ls=(0, (3, 2)))
    axes3d(_right, _view, _g, ((1.95, 0, 0), (0, 1.95, 0), (0, 0, 2.6)), ("$x^1$", "$x^2$", "$y$"), (-150, -30, 90))
    _top = tuple(float(c) for c in _view(1, 1, 2))
    _right.plot(*_top, "o", color="black", ms=4, zorder=6)
    _right.annotate(r"$g\left(\genfrac{[}{]}{0}{0}{1}{1}\right) = 2$", _top, xytext=(78, 12), textcoords="offset points", fontsize=12, ha="left", va="center", arrowprops={"arrowstyle": "-", "color": GREY, "lw": 0.7, "shrinkB": 4}, bbox=_box, zorder=6)
    _right.plot(*_view(0, 0, 0), "o", ms=5, mfc="white", mec=BLUE, mew=1.2, zorder=6)
    tip_label(_right, tuple(float(c) for c in _view(1.06, -1.06, 2.25)), 180, r"$y = f(\vec{x})$", GREY, r=4, fontsize=12)
    tip_label(_right, tuple(float(c) for c in _view(1, 0.25, 1.06)), -160, r"$y = g(\vec{x})$", BLUE, r=8, fontsize=12)
    tip_label(_right, _P(1, 0.5), -90, "$D$", BLUE, r=6, fontsize=12)

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    Starting from any $\vec{a} \in D$,

    - can make $g(\vec{x}) < g(\vec{a})$ moving towards $\vec{0}$, but never reach $g(\vec{x}) = 0$ since $\vec{0} \notin D$

        $\Longrightarrow$ &nbsp; no $\vec{a} \in D$ can be a minimum!

    - can make $g(\vec{x}) > g(\vec{a})$ moving away from $\vec{0}$, unless $a^1 = 1$ or $a^2 = 1$
    - if $a^2 = 1$, can make $g(\vec{x}) > g(\vec{a})$ moving right, unless $a^1 = 1$ (likewise, if $a^1 = 1$, moving up, unless $a^2 = 1$)

        $\Longrightarrow$ &nbsp; $\vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix} \in D$ is the maximum!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, LIGHT, RED, cross_axes, definition, mo, np, tip_label):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    _th = np.linspace(0, 2 * np.pi, 241)
    for _ax in (_left, _right):
        _ax.set_xlim(-2.3, 2.3)
        _ax.set_ylim(-1.6, 2.0)
        _ax.set_aspect("equal")
        _ax.axis("off")

    # bounded: the rectangle 0 <= x^1 <= a, 0 <= x^2 <= b inside B(0, r)
    _a, _b, _r = 1.2, 0.8, 1.55
    _left.fill(_r * np.cos(_th), _r * np.sin(_th), color=RED, alpha=0.06, lw=0)
    _left.plot(_r * np.cos(_th), _r * np.sin(_th), color=RED, lw=1.2)
    _left.fill([0, _a, _a, 0], [0, 0, _b, _b], color=LIGHT, lw=0)
    _left.plot([0, _a, _a, 0, 0], [0, 0, _b, _b, 0], color=BLUE, lw=1.4)
    cross_axes(_left, (-2.0, 2.2), (-1.5, 1.95), "$x^1$", "$x^2$")
    _left.text(_a, -0.06, "$a$", ha="center", va="top", fontsize=12, bbox=_box)
    _left.text(-0.06, _b, "$b$", ha="right", va="center", fontsize=12, bbox=_box)
    _left.text(_a / 2, _b / 2, "$D$", color=BLUE, ha="center", va="center", fontsize=13)
    tip_label(_left, (_r * np.cos(-0.6), _r * np.sin(-0.6)), -30, r"$B(\vec{0}, r)$, $r^2 > a^2 + b^2$", RED, r=4, fontsize=12)

    # unbounded: the strip a <= x^2 <= b leaves every ball
    _a, _b, _r = 0.4, 1.0, 1.3
    _right.fill([-2.3, 2.3, 2.3, -2.3], [_a, _a, _b, _b], color=LIGHT, lw=0)
    for _h in (_a, _b):
        _right.plot([-2.3, 2.3], [_h, _h], color=BLUE, lw=1.4)
    _right.fill(_r * np.cos(_th), _r * np.sin(_th), color=RED, alpha=0.06, lw=0)
    _right.plot(_r * np.cos(_th), _r * np.sin(_th), color=RED, lw=1.2)
    cross_axes(_right, (-2.25, 2.25), (-1.5, 1.95), "$x^1$", "$x^2$")
    _right.text(-0.06, _a, "$a$", ha="right", va="top", fontsize=12, bbox=_box)
    _right.text(-0.06, _b, "$b$", ha="right", va="bottom", fontsize=12, bbox=_box)
    _right.text(1.8, (_a + _b) / 2, "$D$", color=BLUE, ha="center", va="center", fontsize=13)
    tip_label(_right, (_r * np.cos(-0.6), _r * np.sin(-0.6)), -30, r"$B(\vec{0}, r)$", RED, r=4, fontsize=12)

    mo.vstack(
        [
            definition(
                r"""
    $D \subseteq \mathbb{R}^2$ is called **bounded** if “we cannot take its points to infinity”

    $\Longleftrightarrow$ &nbsp; it is contained in some ball of finite radius

    $\Longleftrightarrow$ &nbsp; there exists $B(\vec{0}, r) \supseteq D$

    $D \subseteq \mathbb{R}^2$ is **unbounded** if it cannot be contained in any ball of finite radius.
    """,
                "Bounded and unbounded sets",
            ),
            mo.md(
                r"""
    $$
    D = \left\{\, 0 \leq x^1 \leq a,\ 0 \leq x^2 \leq b \,\right\} \ \text{ is bounded},
    \qquad \qquad
    D = \left\{\, -\infty < x^1 < +\infty,\ a \leq x^2 \leq b \,\right\} \ \text{ is unbounded}
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
            definition(
                r"""
    Given $D \subseteq \mathbb{R}^2$, the **boundary** of $D$ is the set $\mathrm{Bd}(D)$ of points $\vec{a} \in \mathbb{R}^2$ such that any ball centered at $\vec{a}$ contains both points in $D$ *and* points not in $D$.
    """,
                "Boundary",
            ),
            mo.md(
                r"""
    $$
    D = \left\{\, -\infty < x^1 < +\infty,\ a \leq x^2 \leq b \,\right\}
    \qquad \Longrightarrow \qquad
    \mathrm{Bd}(D) = \left\{\, x^2 = a \,\right\} \cup \left\{\, x^2 = b \,\right\}
    $$

    $$
    D = \left\{\, x^1 > 0,\ x^2 > 0,\ (x^1)^2 + (x^2)^2 < 1 \,\right\}
    \qquad \Longrightarrow \qquad
    \begin{aligned}
    \mathrm{Bd}(D) = {} & \left\{\, x^1 \geq 0,\ x^2 \geq 0,\ (x^1)^2 + (x^2)^2 = 1 \,\right\} \\
    & \cup \left\{\, 0 \leq x^1 \leq 1,\ x^2 = 0 \,\right\} \cup \left\{\, x^1 = 0,\ 0 \leq x^2 \leq 1 \,\right\}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    bp1 = mo.ui.slider(-0.4, 1.4, 0.05, value=0.6, label="$p^1$", show_value=True)
    bp2 = mo.ui.slider(-0.4, 1.4, 0.05, value=0.8, label="$p^2$", show_value=True)
    br = mo.ui.slider(0.05, 0.5, 0.05, value=0.2, label="$r$", show_value=True)
    return bp1, bp2, br


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, LIGHT, RED, bp1, bp2, br, cross_axes, math, mo, np, table, tip_label):
    _p = (round(bp1.value, 10) + 0.0, round(bp2.value, 10) + 0.0)
    _r = round(br.value, 10)
    _eps = 1e-9
    # the point of the closure of D nearest to p, and the distance from p to the outside of D
    _q = (max(_p[0], 0.0), max(_p[1], 0.0))
    _n = math.hypot(*_q)
    if _n > 1:
        _q = (_q[0] / _n, _q[1] / _n)
    _to_D = math.hypot(_p[0] - _q[0], _p[1] - _q[1])
    _in_D = _p[0] > _eps and _p[1] > _eps and math.hypot(*_p) < 1 - _eps
    _to_out = min(_p[0], _p[1], 1 - math.hypot(*_p)) if _in_D else 0.0
    _meets_D = _to_D < _r - _eps
    _meets_out = not (_in_D and _r <= _to_out + _eps)
    _on_Bd = _to_D < _eps and not _in_D

    def _yes(b):
        return "yes" if b else "no"

    _fig = Figure(figsize=(HALF + 1.2, HALF + 0.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.6, 1.75)
    _ax.set_ylim(-0.6, 1.6)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _th = np.linspace(0, np.pi / 2, 120)
    _ax.fill(np.r_[0, np.cos(_th)], np.r_[0, np.sin(_th)], color=LIGHT, lw=0, zorder=0)
    _ax.plot(np.r_[0, np.cos(_th), 0], np.r_[0, np.sin(_th), 0], color=GREEN, lw=2.0, ls=(0, (4, 2)), zorder=2)
    cross_axes(_ax, (-0.55, 1.7), (-0.55, 1.55), "$x^1$", "$x^2$")
    _c = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_p[0] + _r * np.cos(_c), _p[1] + _r * np.sin(_c), color=RED, alpha=0.12, lw=0, zorder=3)
    _ax.plot(_p[0] + _r * np.cos(_c), _p[1] + _r * np.sin(_c), color=RED, lw=1.2, zorder=3)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=5)
    tip_label(_ax, (_p[0] + _r * 0.71, _p[1] - _r * 0.71), -45, r"$B(\vec{p}, r)$", RED, r=3, fontsize=12)
    _lab = (_p[0] + 0.71 * _r + 0.15, _p[1] - 0.71 * _r - 0.05)  # about where the label of the ball sits
    _spot = max(((0.3, 0.25), (0.65, 0.2), (0.2, 0.65)), key=lambda c: min(math.hypot(c[0] - _p[0], c[1] - _p[1]) - _r, math.hypot(c[0] - _lab[0], c[1] - _lab[1])))
    tip_label(_ax, _spot, 0, "$D$", BLUE, r=0)
    tip_label(_ax, (0.92, 0.92), 45, r"$\mathrm{Bd}(D)$", GREEN, r=8, fontsize=12)

    mo.vstack(
        [
            mo.hstack([bp1, bp2, br], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{p}$", rf"$\begin{{bmatrix}} {_p[0]:g} \\ {_p[1]:g} \end{{bmatrix}}$"),
                    (r"$\textcolor{" + RED + r"}{B(\vec{p}, r)}$ contains points in $D$", _yes(_meets_D)),
                    (r"$\textcolor{" + RED + r"}{B(\vec{p}, r)}$ contains points not in $D$", _yes(_meets_out)),
                    (r"$\vec{p} \in D$", _yes(_in_D)),
                    (r"$\vec{p} \in \textcolor{" + GREEN + r"}{\mathrm{Bd}(D)}$", _yes(_on_Bd)),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, LIGHT, RED, cross_axes, definition, mo, np, tip_label):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _a, _b, _c, _d = 0.5, 1.7, 0.45, 1.3
    _fig = Figure(figsize=(FULL, 2.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax, _closed in ((_left, False), (_right, True)):
        _ax.set_xlim(-0.3, 2.3)
        _ax.set_ylim(-0.3, 1.65)
        _ax.set_aspect("equal")
        _ax.axis("off")
        cross_axes(_ax, (-0.2, 2.25), (-0.2, 1.6), "$x^1$", "$x^2$")
        _ax.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=LIGHT, lw=0)
        _ax.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=BLUE, lw=1.4, ls="-" if _closed else (0, (3, 2)))
        for _x in (_a, _b):
            for _y in (_c, _d):
                if _closed:
                    _ax.plot(_x, _y, "o", ms=5, color=BLUE, zorder=3)
                else:
                    _ax.plot(_x, _y, "o", ms=5, mfc="white", mec=BLUE, mew=1.2, zorder=3)
        for _x, _name in ((_a, "$a$"), (_b, "$b$")):
            _ax.text(_x, -0.05, _name, ha="center", va="top", fontsize=12, bbox=_box)
        for _y, _name in ((_c, "$c$"), (_d, "$d$")):
            _ax.text(-0.05, _y, _name, ha="right", va="center", fontsize=12, bbox=_box)
        _ax.text((_a + _b) / 2, (_c + _d) / 2, "$D$", color=BLUE, ha="center", va="center", fontsize=13)
    _t = np.linspace(0, 2 * np.pi, 120)
    _left.fill(_a + 0.16 * np.cos(_t), _c + 0.16 * np.sin(_t), color=RED, alpha=0.12, lw=0, zorder=2)
    _left.plot(_a + 0.16 * np.cos(_t), _c + 0.16 * np.sin(_t), color=RED, lw=1.0, zorder=2)
    tip_label(_left, (_a - 0.12, _c + 0.12), 150, r"$\genfrac{[}{]}{0}{0}{a}{c}$", RED, r=3, fontsize=12)

    mo.vstack(
        [
            definition(
                r"""
    A set $D \subseteq \mathbb{R}^2$ is called **closed** if it contains all of its boundary, &nbsp; $\mathrm{Bd}(D) \subseteq D$.
    """,
                "Closed set",
            ),
            _fig,
            mo.md(
                r"""
    $D = \left\{\, a < x^1 < b,\ c < x^2 < d \,\right\}$ is not closed! &nbsp; $\begin{bmatrix} a \\ c \end{bmatrix} \in \mathrm{Bd}(D)$, but $\begin{bmatrix} a \\ c \end{bmatrix} \notin D$ &nbsp; (one missing point is enough!)

    $D = \left\{\, a \leq x^1 \leq b,\ c \leq x^2 \leq d \,\right\}$ is closed!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, cross_axes, mo, theorem, tip_label):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(HALF, 2.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.35, 2.4)
    _ax.set_ylim(-0.3, 1.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.2, 1.5), (-0.2, 1.4), "$x^1$", "$x^2$")
    _ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color=LIGHT, lw=0)
    _ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=BLUE, lw=1.4)
    tip_label(_ax, (0.5, 0.5), 0, r"$\bar{D}$", BLUE, r=0)
    for _pt, _text, _d in (((0, 0), r"$h\left(\genfrac{[}{]}{0}{0}{0}{0}\right) = 0$", -30), ((1, 1), r"$h\left(\genfrac{[}{]}{0}{0}{1}{1}\right) = 2$", 20)):
        _ax.plot(*_pt, "o", color="black", ms=4, zorder=5)
        tip_label(_ax, _pt, _d, _text, "black", r=6, fontsize=12)

    mo.vstack(
        [
            theorem(
                r"""
    If $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a closed and bounded domain $D$, then $f$ must have both points of global maximum and global minimum!
    """,
                "Extreme value theorem",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; functions defined on unbounded domains or on non-closed domains might not admit any global extrema!

    **Remark.** $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ over $\mathbb{R}^2$ has no global maximum, which is possible because $\mathbb{R}^2$ is unbounded

    $g\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ over $D = (0, 1] \times (0, 1]$ has no global minimum, which is possible because $D$ is not closed

    $h\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ over $\bar{D} = [0, 1] \times [0, 1]$ has both global extrema!
    """
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a closed bounded domain $D$.

    How can we find the global extrema?

    If $\vec{a} \in D$ is a global extremum:

    - $\vec{a} \in \mathrm{Bd}(D) \subseteq D$

    or

    - $\vec{a} \notin \mathrm{Bd}(D)$ &nbsp; $\Longrightarrow$ &nbsp; there is some open ball $B(\vec{a}, r)$ which only contains points of $D$

        $\Longrightarrow$ &nbsp; there exists $B(\vec{a}, r) \subseteq D$ with

        $$
        f(\vec{x}) \leq f(\vec{a}) \quad \forall\, \vec{x} \in B(\vec{a}, r) \qquad (\vec{a} \text{ is local maximum})
        $$

        or

        $$
        f(\vec{x}) \geq f(\vec{a}) \quad \forall\, \vec{x} \in B(\vec{a}, r) \qquad (\vec{a} \text{ is local minimum})
        $$

    $\Longrightarrow$ &nbsp; for differentiable functions defined over closed and bounded domains we get a well-defined strategy to find global extrema!

    ### Strategy to find global extrema

    1. find critical points on the interior $D \setminus \mathrm{Bd}(D)$ (not on the boundary)
    2. find global extrema in $\mathrm{Bd}(D)$ (optimization problem in lower dimension &nbsp; $\Longrightarrow$ &nbsp; easier once we have a parameterization of the boundary)
    3. compare the values of all candidate points

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2 - 2x^1$ &nbsp; on &nbsp; $D = \left\{\, (x^1)^2 + (x^2)^2 \leq 4 \,\right\}$

    $$
    \mathrm{Bd}(D) = \left\{\, (x^1)^2 + (x^2)^2 = 4 \,\right\} = \underbrace{\left\{\, \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \;\middle|\; t \in [0, 2\pi] \,\right\}}_{\text{parameterization of } \mathrm{Bd}(D)},
    \qquad
    D \setminus \mathrm{Bd}(D) = \left\{\, (x^1)^2 + (x^2)^2 < 4 \,\right\}
    $$

    ① &nbsp; Critical points in $D \setminus \mathrm{Bd}(D)$:

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 - 2 \\ 2x^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    \qquad \Longleftrightarrow \qquad
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \vec{a}
    \qquad (\text{interior candidate for global extremum})
    $$

    ② &nbsp; Restrict $f$ to $\mathrm{Bd}(D)$:

    $$
    f\!\left( \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \right) = 4 - 4\cos(t) = g(t)
    \qquad \leadsto \qquad g'(t) = 4\sin(t) = 0 \quad \Longleftrightarrow \quad t = 0 \text{ or } t = \pi
    \quad (t = 2\pi \text{ gives the same point as } t = 0)
    $$

    $$
    \Longrightarrow \qquad
    \vec{b} = \begin{bmatrix} 2\cos(0) \\ 2\sin(0) \end{bmatrix} = \begin{bmatrix} 2 \\ 0 \end{bmatrix},
    \qquad
    \vec{c} = \begin{bmatrix} 2\cos(\pi) \\ 2\sin(\pi) \end{bmatrix} = \begin{bmatrix} -2 \\ 0 \end{bmatrix}
    \qquad (\text{boundary candidates})
    $$

    ③ &nbsp; Compare:

    $$
    f(\vec{a}) = -1 \ \ (\text{min}), \qquad f(\vec{b}) = 0, \qquad f(\vec{c}) = 8 \ \ (\text{max})
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    st = mo.ui.slider(0, 24, 1, value=4, label=r"$t$ (multiples of $\pi/12$)", show_value=True)
    return (st,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, LIGHT, RED, cross_axes, math, mo, np, num, st, table, tip_label):
    _t = st.value * math.pi / 12
    _pt = (2 * math.cos(_t), 2 * math.sin(_t))
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    def _g(t):
        return 4 - 4 * np.cos(t)

    _fig = Figure(figsize=(FULL, 3.3), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1, 1.35])

    # D with the level sets of f (circles about a), the candidates and the point of Bd(D) at time t
    _left.set_xlim(-2.6, 2.75)
    _left.set_ylim(-2.45, 2.6)
    _left.set_aspect("equal")
    _left.axis("off")
    _th = np.linspace(0, 2 * np.pi, 241)
    _left.fill(2 * np.cos(_th), 2 * np.sin(_th), color=LIGHT, lw=0, zorder=0)
    _disc = _left.fill(2 * np.cos(_th), 2 * np.sin(_th), color="none", lw=0)[0]
    for _c in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        (_ring,) = _left.plot(1 + math.sqrt(_c + 1) * np.cos(_th), math.sqrt(_c + 1) * np.sin(_th), color=GREY, lw=0.6, zorder=1)
        _ring.set_clip_path(_disc)
    _left.plot(2 * np.cos(_th), 2 * np.sin(_th), color=BLUE, lw=1.4, zorder=2)
    cross_axes(_left, (-2.5, 2.7), (-2.4, 2.55), "$x^1$", "$x^2$")
    for _p, _name, _d in (((1, 0), r"$\vec{a}$", -90), ((2, 0), r"$\vec{b}$", -120), ((-2, 0), r"$\vec{c}$", -135)):
        _left.plot(*_p, "o", color="black", ms=4, zorder=5)
        tip_label(_left, _p, _d, _name, "black")
    _left.plot(*_pt, "o", color=RED, ms=6, zorder=6)
    tip_label(_left, (-1.45, -1.45), -135, r"$\mathrm{Bd}(D)$", BLUE, r=4, fontsize=12)

    # g(t) = f on Bd(D), with the value of f at the interior candidate
    _right.set_xlim(-0.6, 7.6)
    _right.set_ylim(-1.8, 9.2)
    _right.set_aspect(0.55)
    _right.axis("off")
    cross_axes(_right, (-0.4, 7.2), (-1.6, 9.1), "$t$", "$y$")
    _s = np.linspace(0, 2 * math.pi, 300)
    _right.plot(_s, _g(_s), color=BLUE, lw=1.6)
    _right.plot([0, 2 * math.pi], [-1, -1], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _right.text(math.pi, -1.2, r"$f(\vec{a}) = -1$", color=GREY, fontsize=12, ha="center", va="top")
    for _x, _name in ((math.pi, r"$\pi$"), (2 * math.pi, r"$2\pi$")):
        _right.plot([_x, _x], [-0.15, 0.15], color="black", lw=0.9)
        _right.text(_x, 0.35, _name, ha="center", va="bottom", fontsize=12, bbox=_box)
    for _x, _name in ((0, r"$\vec{b}$"), (math.pi, r"$\vec{c}$"), (2 * math.pi, r"$\vec{b}$")):
        _right.plot(_x, _g(_x), "o", color="black", ms=4, zorder=5)
    _right.text(math.pi, 8.3, r"$\vec{c}$", ha="center", va="bottom", fontsize=12)
    _right.text(4.9, 7.9, r"$g(t) = 4 - 4\cos(t)$", color=BLUE, fontsize=12, ha="left", va="center")
    _right.plot(_t, _g(_t), "o", color=RED, ms=6, zorder=6)

    mo.vstack(
        [
            mo.hstack([st], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \in \mathrm{Bd}(D)$", rf"$\textcolor{{{RED}}}{{\begin{{bmatrix}} {num(_pt[0])} \\ {num(_pt[1])} \end{{bmatrix}}}}$"),
                    (r"$g(t) = 4 - 4\cos(t)$", rf"$\textcolor{{{RED}}}{{{num(4 - 4 * math.cos(_t))}}}$"),
                    (r"$g'(t) = 4\sin(t)$", rf"${num(4 * math.sin(_t))}$"),
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

    q1_max, q1_min = _field(), _field()
    return q1_max, q1_min


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, check, cross_axes, mo, q1_max, q1_min):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(HALF - 0.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.6, 3.1)
    _ax.set_ylim(-0.6, 3.75)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.4, 3.0), (-0.4, 3.7), "$x^1$", "$x^2$")
    _ax.fill([0, 2, 2, 0], [0, 0, 3, 3], color=LIGHT, lw=0)
    _ax.plot([0, 2, 2, 0, 0], [0, 0, 3, 3, 0], color=BLUE, lw=1.4)
    for _c in ((0, 0), (2, 0), (2, 3), (0, 3)):
        _ax.plot(*_c, "o", ms=4, color=BLUE, zorder=3)
    _ax.text(2, -0.1, "$2$", ha="center", va="top", fontsize=12, bbox=_box)
    _ax.text(-0.1, 3, "$3$", ha="right", va="center", fontsize=12, bbox=_box)
    _ax.text(1, 1.5, "$D$", color=BLUE, ha="center", va="center", fontsize=13)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^3 + (x^2)^2 - 3x^1 - 2x^2
    $$

    (a) Find all critical points in $\mathbb{R}^2$.

    (b) Decide their type (via 2nd derivative test).

    (c) Find the global maximum and global minimum over

    $$
    D = [0, 2] \times [0, 3] = \left\{\, 0 \leq x^1 \leq 2,\ 0 \leq x^2 \leq 3 \,\right\}
    $$
    """
            ),
            _fig,
            mo.md(r"""$\leadsto$ &nbsp; parameterize the boundary with 4 different line segments"""),
            _ask(r"global maximum value of $f$ over $D$ $=$", q1_max, 5),
            _ask(r"global minimum value of $f$ over $D$ $=$", q1_min, -3),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $\vec{a} \in D$ is a global maximum (minimum) of $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ if $f(\vec{x}) \leq f(\vec{a})$ ($f(\vec{x}) \geq f(\vec{a})$) for all $\vec{x} \in D$
    - $D$ is bounded if it is contained in some ball $B(\vec{0}, r)$; its boundary $\mathrm{Bd}(D)$ is the set of points $\vec{a}$ such that any ball centered at $\vec{a}$ contains both points in $D$ and points not in $D$; $D$ is closed if $\mathrm{Bd}(D) \subseteq D$
    - a continuous $f$ over a closed and bounded domain $D$ has both a global maximum and a global minimum
    - a global extremum lies in $\mathrm{Bd}(D)$, or it is a local extremum in $D \setminus \mathrm{Bd}(D)$
    - strategy: find the critical points in $D \setminus \mathrm{Bd}(D)$; find the global extrema of $f$ on $\mathrm{Bd}(D)$, via a parameterization of the boundary; compare the values of all candidate points
    """)
    return


if __name__ == "__main__":
    app.run()
