import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 17 • Differentiation of vector fields", css_file="bs101.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Figure, math, mo, np


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

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        One line weight for every figure; the head is open and sized in points from the line width,
        so arrows look alike across lectures at any axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={2 * lw:g},head_width={0.87 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, definition, header, table


@app.cell(hide_code=True)
def _(header):
    header("Lecture 17", "Week 10", "Lecture 17 • Differentiation of vector fields")
    return


@app.cell(hide_code=True)
def _(Figure, HALF, arrow, math, np):
    # ---- Helpers of this lecture ----------------------------------------
    FAINT = "#b8b8b8"  # flow lines behind a field

    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr.
        Returns the boxes the axis names take, in data coordinates (fields and flow lines keep clear of them)."""
        arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        u, boxes = per_pt(ax), []
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
            boxes.append((xr[1] - 14 * u, -24 * u, xr[1] + 2 * u, -2 * u))
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)
            boxes.append((2 * u, yr[1] - 18 * u, 18 * u, yr[1] + 2 * u))
        return boxes

    def panel(ax, xl, yl=None):
        """A bare axis over xl x yl (a square [-xl, xl]^2 when xl is a number)."""
        if not isinstance(xl, tuple):
            xl = (-xl, xl)
        ax.set_xlim(*xl)
        ax.set_ylim(*(yl or xl))
        ax.set_aspect("equal")
        ax.axis("off")

    def sketch(xlim, ylim, width=HALF):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges;
        the scale never changes with a slider (names are kept inside the ranges)."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        panel(ax, xlim, ylim)
        return fig, ax

    def per_pt(ax):
        """Data units per point on an axis of fixed place and equal aspect."""
        x0, x1 = ax.get_xlim()
        return (x1 - x0) / (ax.figure.get_figwidth() * 72 * ax.get_position().width)

    def beside(ax, at, angle, text, color, w, h, gap=4, fontsize=13):
        """Name centred beside the point `at`, in the direction `angle` (degrees), far enough for a
        w x h box (points) to clear it. Returns the box the name takes, in data coordinates."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        d = w / 2 * abs(c) + h / 2 * abs(s) + gap
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})
        u = per_pt(ax)
        cx, cy = at[0] + d * c * u, at[1] + d * s * u
        return (cx - (w / 2 + 2) * u, cy - (h / 2 + 2) * u, cx + (w / 2 + 2) * u, cy + (h / 2 + 2) * u)

    def masked(xs, ys, avoid):
        """The polyline with the points under a name in `avoid` left out (the line is broken there)."""
        xs, ys = np.array(xs, float), np.array(ys, float)
        for b in avoid:
            m = (xs >= b[0]) & (xs <= b[2]) & (ys >= b[1]) & (ys <= b[3])
            xs[m], ys[m] = np.nan, np.nan
        return xs, ys

    def label(ax, at, text, color, w, h, fontsize=12, ha="center"):
        """A name kept at one place `at` (data coordinates); returns its box in data coordinates."""
        ax.text(*at, text, color=color, fontsize=fontsize, ha=ha, va="center", zorder=8, linespacing=1.15)
        u = per_pt(ax)
        x0 = at[0] - (w / 2 if ha == "center" else (w if ha == "right" else 0)) * u
        return (x0 - 2 * u, at[1] - (h / 2 + 2) * u, x0 + (w + 2) * u, at[1] + (h / 2 + 2) * u)

    def clear_of(boxes, p, q):
        """True when the segment from p to q stays out of every box."""
        for b in boxes:
            for i in range(21):
                x, y = p[0] + (q[0] - p[0]) * i / 20, p[1] + (q[1] - p[1]) * i / 20
                if b[0] <= x <= b[2] and b[1] <= y <= b[3]:
                    return False
        return True

    def ring(r, n, off=0.0):
        """n points evenly spaced on the circle of radius r, the first at the angle `off` (degrees)."""
        return [(r * math.cos(math.radians(off + 360 * k / n)), r * math.sin(math.radians(off + 360 * k / n))) for k in range(n)]

    # every field is drawn at the same base points (a square grid of spacing 1, offset by 1/2 so that no point lies
    # on an axis), each arrow at 1/2 of its vector, so that the fields can be compared point by point
    GRID = [(sx * a, sy * b) for a, b in ((0.5, 0.5), (1.5, 0.5), (0.5, 1.5), (1.5, 1.5), (2.5, 0.5), (0.5, 2.5)) for sx in (1, -1) for sy in (1, -1)]
    SCALE = 1 / 2
    # the rotation and radial fields F and H, whose arrows grow, on a denser grid: spacing 3/4, offset by half a step,
    # within 2.7 of the origin (so that the longest arrows do not run into each other)
    GRID_DENSE = [(0.75 * (i + 0.5), 0.75 * (j + 0.5)) for i in range(-4, 4) for j in range(-4, 4) if math.hypot(0.75 * (i + 0.5), 0.75 * (j + 0.5)) <= 2.7]
    # for the rotation field, four points (one orbit of the quarter turn) whose arrows would almost touch their neighbours are left out
    GRID_ROT = [p for p in GRID_DENSE if p not in ((1.875, 1.125), (-1.125, 1.875), (-1.875, -1.125), (1.125, -1.875))]

    def farrow(ax, tail, tip, color, lw=1.1, alpha=1.0, zorder=3):
        """A field arrow: solid shaft (1.1 pt, about 1.5 px) with a small open head of the same stroke. Every arrow of a
        field, named or not, is drawn this way; only the colour sets a named one apart."""
        ax.annotate("", xy=tip, xytext=tail, zorder=zorder,
                    arrowprops={"arrowstyle": "->,head_length=0.35,head_width=0.22", "mutation_scale": 11, "color": color, "lw": lw, "alpha": alpha, "shrinkA": 0, "shrinkB": 0})

    def vfield(ax, F, color, pts=GRID, k=SCALE, lw=1.1, alpha=1.0, skip=(), avoid=(), cross=()):
        """The vectors k F(p) drawn from their base points p (by default the grid above, at 1/2). The points in
        `skip`, the arrows that would run under a name in `avoid`, and the arrows that cross or touch one of the
        curves in `cross` (pairs of arrays xs, ys), are left out."""
        for p in pts:
            if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 1e-9 for q in skip):
                continue
            v = F(*p)
            tip = (p[0] + k * v[0], p[1] + k * v[1])
            near = False
            for xs, ys in cross:
                for i in range(21):
                    qx, qy = p[0] + (tip[0] - p[0]) * i / 20, p[1] + (tip[1] - p[1]) * i / 20
                    if np.min(np.hypot(np.asarray(xs) - qx, np.asarray(ys) - qy)) < 0.08:
                        near = True
                        break
                if near:
                    break
            if not near and clear_of(avoid, p, tip):
                farrow(ax, p, tip, color, lw=lw, alpha=alpha)

    def chevron(ax, at, angle, color, size=4.5, lw=1.0):
        """A small open head at `at`, pointing in the direction `angle` (radians): a direction mark on a flow line."""
        u = per_pt(ax) * size
        for s in (1, -1):
            b = angle + math.pi + s * 0.55
            ax.plot([at[0] + u * math.cos(b), at[0]], [at[1] + u * math.sin(b), at[1]], color=color, lw=lw, solid_capstyle="round", zorder=2)

    def flow_circles(ax, radii, color=FAINT, at=(0.9, 0.9 + math.pi), lw=0.9, zorder=1):
        """Circles about the origin, travelled anticlockwise, with two direction marks each."""
        s = np.linspace(0, 2 * math.pi, 361)
        for r in radii:
            ax.plot(r * np.cos(s), r * np.sin(s), color=color, lw=lw, zorder=zorder)
            for a in at:
                chevron(ax, (r * math.cos(a), r * math.sin(a)), a + math.pi / 2, color, lw=lw)

    def flow_rays(ax, angles, r1, color=FAINT, lw=0.9, mark=0.6, zorder=1):
        """Rays from the origin to the radius r1, travelled outwards, with a direction mark part-way along."""
        for a in angles:
            c, d = math.cos(a), math.sin(a)
            ax.plot([0, r1 * c], [0, r1 * d], color=color, lw=lw, zorder=zorder)
            chevron(ax, (mark * r1 * c, mark * r1 * d), a, color, lw=lw)

    def disc_patch(c, rho, n=2000):
        """The boundary of the disc of radius rho about c, as two arrays."""
        s = np.linspace(0, 2 * math.pi, n, endpoint=False)
        return c[0] + rho * np.cos(s), c[1] + rho * np.sin(s)

    def area(xs, ys):
        """Area enclosed by a closed polygon (shoelace formula)."""
        return 0.5 * abs(float(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1))))

    def num(v, digits=2):
        """Number for the readout tables: exact when a multiple of 1/2, otherwise fixed-point (never a negative zero)."""
        if abs(2 * v - round(2 * v)) < 1e-9:
            return f"{round(2 * v) / 2 + 0.0:g}"
        return f"{round(v, digits) + 0.0:.{digits}f}"

    def rot(x, y):
        return (-y / 2, x / 2)

    def unit_rot(x, y):
        r = math.hypot(x, y)
        return (-y / r, x / r)

    def rad(x, y):
        return (x / 2, y / 2)

    def unit_rad(x, y):
        r = math.hypot(x, y)
        return (x / r, y / r)

    return FAINT, GRID, GRID_DENSE, GRID_ROT, SCALE, area, beside, chevron, clear_of, cross_axes, disc_patch, farrow, flow_circles, flow_rays, label, masked, num, panel, rad, ring, rot, sketch, unit_rad, unit_rot, vfield


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## So far

    Differentiation of $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, mostly for $n = 1$ (paths) and $m = 1$ (scalar valued)

    **In this lecture:** vector fields, flow lines, divergence

    **References:** MT 4.3, 4.4
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## IV.1 &nbsp; Differentiation of vector fields $(n = m)$

    **Remark.** For the rest of the course we will work mostly with $n = 1, 2, 3$ $\leadsto$ we will simplify the notation

    $$
    \begin{alignedat}{3}
    & \text{in } \mathbb{R}: \quad && t \in \mathbb{R} \quad && (\text{as we were already writing}) \\[6pt]
    & \text{in } \mathbb{R}^2: && \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} x \\ y \end{bmatrix} \in \mathbb{R}^2 \quad && \leadsto \quad x^1 = x, \quad x^2 = y \\[10pt]
    & \text{in } \mathbb{R}^3: && \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} = \begin{bmatrix} x \\ y \\ z \end{bmatrix} \in \mathbb{R}^3 \quad && \leadsto \quad x^1 = x, \quad x^2 = y, \quad x^3 = z
    \end{alignedat}
    $$

    $\leadsto$ &nbsp; no more indices!
    """
            ),
            definition(
                r"""
    A **vector field** in $\mathbb{R}^2$ is a map

    $$
    \begin{aligned}
    \vec{F} : D \subseteq \mathbb{R}^2 & \longrightarrow \mathbb{R}^2 \\
    \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix} & \longmapsto \vec{F}(\vec{x}) = \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \end{bmatrix}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; $P : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ and $Q : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ are called the **components** of $\vec{F}$
    """,
                "Vector field",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(GREEN, beside, cross_axes, label, math, mo, sketch, vfield):
    # the vector field F(x) = 1/2 (-y, x) at its true length, at points on five circles about the origin (r = 0.5, 1, ..., 2.5,
    # eight points each, every other circle turned by 22.5 degrees), so that each circle shows the same pattern scaled and
    # no two arrows touch; three of the points marked, each named with its vector
    def _F(x, y):
        return (-y / 2, x / 2)

    _pts = [(_r * math.cos(math.radians((22.5 if _i % 2 == 0 else 0) + 45 * _j)), _r * math.sin(math.radians((22.5 if _i % 2 == 0 else 0) + 45 * _j)))
            for _i, _r in enumerate((0.5, 1.0, 1.5, 2.0, 2.5)) for _j in range(8)]
    _fig, _ax = sketch((-4.2, 4.2), (-4.2, 4.2))
    _names = [label(_ax, (1.3, 3.6), "rotation\nvector field $\\vec{F}$", GREEN, 84, 34, fontsize=13, ha="left")]
    _names += cross_axes(_ax, (-4.1, 4.1), (-4.1, 4.1), "$x$", "$y$")
    vfield(_ax, _F, GREEN, pts=_pts, k=1.0, avoid=_names)
    # three of the points named with their vectors right beside them, over other arrows (white box) but clear of the axes
    # and of the arrow they name, in a small font
    beside(_ax, (1.0, 0.42), 0, r"$\vec{F}\left(\genfrac{[}{]}{0}{0}{1}{0}\right) = \genfrac{[}{]}{0}{0}{0}{1/2}$", "black", 66, 21, gap=5, fontsize=8.5)
    beside(_ax, (-1.0, 2.0), 90, r"$\vec{F}\left(\genfrac{[}{]}{0}{0}{0}{2}\right) = \genfrac{[}{]}{0}{0}{-1}{0}$", "black", 66, 21, gap=7, fontsize=8.5)
    beside(_ax, (-math.sqrt(2), -math.sqrt(2)), 180, r"$\vec{F}\left(\genfrac{[}{]}{0}{0}{-\sqrt{2}}{-\sqrt{2}}\right) = \genfrac{[}{]}{0}{0}{\sqrt{2}/2}{-\sqrt{2}/2}$", "black", 78, 23, gap=14, fontsize=8.5)
    for _q in ((1.0, 0.0), (0.0, 2.0), (-math.sqrt(2), -math.sqrt(2))):
        _ax.plot(*_q, "o", color="black", ms=2.7, zorder=7)

    mo.vstack(
        [
            mo.md(r"""**Example.** &nbsp; $\vec{F} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$, &nbsp; $\vec{F}(\vec{x}) = \frac{1}{2}\begin{bmatrix} -y \\ x \end{bmatrix}$"""),
            mo.hstack([_fig], justify="center"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note: &nbsp; $\lVert \vec{F}(\vec{x}) \rVert^2 = \frac{1}{4}\big( (-y)^2 + \underbrace{x^2}_{\mathclap{\footnotesize (x)^2}\vphantom{\footnotesize (x)^2}} \big) = \frac{1}{4} \lVert \vec{x} \rVert^2$ &nbsp; $\Longrightarrow$ &nbsp; vectors are getting bigger away from $\vec{0}$

    $$
    \vec{G}(\vec{x}) = \begin{cases} \dfrac{1}{\lVert \vec{x} \rVert} \begin{bmatrix} -y \\ x \end{bmatrix}, & \vec{x} \neq \vec{0} \\[10pt] \vec{0}, & \vec{x} = \vec{0} \end{cases}
    $$

    $$
    \Longrightarrow \qquad \lVert \vec{G}(\vec{x}) \rVert^2 = \begin{cases} \dfrac{1}{\lVert \vec{x} \rVert^2}\, \lVert \vec{x} \rVert^2 = 1, & \vec{x} \neq \vec{0} \\[10pt] 0, & \vec{x} = \vec{0} \end{cases}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, SCALE, beside, cross_axes, farrow, label, mo, np, sketch, unit_rot, vfield):
    # the unit rotation vector field, every arrow at 1/2 of its vector (all of length 1/2), on rings of radius
    # 1/2, 1, ..., 5/2 with 6, 9, 12, 15, 18 evenly spread points (so the axes carry points at every arrow length);
    # x is the point of the radius-2 ring at 48 degrees and G(x) its arrow
    _pts = [(0.5 * _k * np.cos(2 * np.pi * _j / (3 * _k + 3)), 0.5 * _k * np.sin(2 * np.pi * _j / (3 * _k + 3)))
            for _k in range(1, 6) for _j in range(3 * _k + 3)]
    _xv = _pts[27 + 2]
    _g = unit_rot(*_xv)
    _tip = (_xv[0] + SCALE * _g[0], _xv[1] + SCALE * _g[1])
    _fig, _ax = sketch((-3.5, 3.5), (-3.5, 3.5))
    _names = [
        beside(_ax, ((_xv[0] + _tip[0]) / 2, (_xv[1] + _tip[1]) / 2), 45, r"$\vec{G}(\vec{x})$", BLUE, 34, 16, gap=4),
        beside(_ax, _xv, -45, r"$\vec{x}$", "black", 10, 12, gap=2),
        label(_ax, (-3.45, -3.05), "unit rotation\nvector field $\\vec{G}$", GREEN, 90, 34, fontsize=13, ha="left"),
    ]
    _names += cross_axes(_ax, (-3.4, 3.4), (-3.4, 3.4), "$x$", "$y$")
    vfield(_ax, unit_rot, GREEN, pts=_pts, skip=[_xv], avoid=_names[2:])
    farrow(_ax, _xv, _tip, BLUE, zorder=6)
    _ax.plot(*_xv, "o", color=BLUE, ms=2.7, zorder=7)

    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(Figure, GREEN, cross_axes, label, math, mo, panel, rad, unit_rad, vfield):
    # the radial field H(x) = x/2 at its true length, on the five circles of the rotation field, circles 1 and 2 on the
    # axes and diagonals, circles 1/2, 3/2, 5/2 halfway between (angles pi/4 j or pi/4 j + pi/8); the unit radial field I at 1/2 of its vectors (all of length 1/2), on the
    # same points as H, so the two can be compared point by point
    _fig = Figure(figsize=(7.2, 3.4))
    _left = _fig.add_axes((0, 0, 3.4 / 7.2, 1))
    _right = _fig.add_axes((3.8 / 7.2, 0, 3.4 / 7.2, 1))
    _hpts = [(0.5 * (_k + 1) * math.cos(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0)),
              0.5 * (_k + 1) * math.sin(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0))) for _k in range(5) for _j in range(8)]
    _ipts = _hpts
    for _ax, _F, _pts, _k, _lim, _name in ((_left, rad, _hpts, 1.0, 4.2, "radial vector\nfield $\\vec{H}$"), (_right, unit_rad, _ipts, 0.5, 3.5, "unit radial\nvector field $\\vec{I}$")):
        panel(_ax, _lim)
        _names = [label(_ax, (-_lim + 0.05, -_lim + 0.35), _name, GREEN, 84, 34, fontsize=13, ha="left")]
        _names += cross_axes(_ax, (-_lim + 0.1, _lim - 0.1), (-_lim + 0.1, _lim - 0.1), "$x$", "$y$")
        vfield(_ax, _F, GREEN, pts=_pts, k=_k, avoid=_names)

    mo.vstack(
        [
            mo.md(
                r"""
    $$
    \begin{array}{cc}
    \vec{H}(\vec{x}) = \frac{1}{2}\begin{bmatrix} x \\ y \end{bmatrix} = \frac{1}{2}\vec{x} \qquad\qquad & \vec{I}(\vec{x}) = \begin{cases} \dfrac{\vec{x}}{\lVert \vec{x} \rVert}, & \vec{x} \neq \vec{0} \\[10pt] \vec{0}, & \vec{x} = \vec{0} \end{cases} \\[24pt]
    \text{radial vector field} \qquad\qquad & \text{unit radial vector field}
    \end{array}
    $$
    """
            ),
            mo.hstack([_fig], justify="center"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    definition(
        r"""
    Given a vector field $\vec{F} : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^2$, a path $\gamma : (-\varepsilon, \varepsilon) \subseteq \mathbb{R} \longrightarrow D \subseteq \mathbb{R}^2$ is called a **flow line** of the vector field $\vec{F}$ if

    $$
    \gamma'(t) = \vec{F}(\gamma(t)) \qquad \forall\, t \in (-\varepsilon, \varepsilon)
    $$
    """,
        "Flow line",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    lt = mo.ui.slider(-3, 3, 0.05, value=0.6, label="$t$", show_value=True)
    return (lt,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, ORANGE, RED, farrow, label, lt, math, mo, np, sketch, vfield):
    # a generic vector field, unnamed as on the page, every arrow at 0.6 of its vector, its base points the points of gamma
    # translated up and down (rows parallel to gamma); the flow line gamma in red, with the field's arrows along it in green; the velocity in blue; gamma(t) moves
    def _p(x):
        return x**3 / 14 - x / 3

    def _F(x, y):
        return (1.0, 3 * x * x / 14 - 1 / 3)

    _k = 0.6
    _fig, _ax = sketch((-3.4, 3.8), (-2.0, 4.2))
    _t = round(lt.value, 10)
    _g = (_t, _p(_t))
    _names = [
        label(_ax, (1.85, -1.75), r"$\gamma'(t) = \vec{F}(\gamma(t))$", BLUE, 100, 18, fontsize=13),
        label(_ax, (-3.22, -0.55), r"$\gamma$", RED, 10, 14, fontsize=13),
    ]
    _grid = [(_x, _p(_x) + _c) for _x in np.arange(-3.0, 3.01, 0.75) for _c in (-0.75, 0.75, 1.5, 2.25)]
    vfield(_ax, _F, GREEN, pts=_grid, k=_k, avoid=_names)
    _s = np.linspace(-3.3, 3.3, 400)
    _ys = _p(_s)
    _m = np.abs(_ys) < 3.3
    _ax.plot(_s[_m], _ys[_m], color=RED, lw=1.6, zorder=4)
    vfield(_ax, _F, GREEN, pts=[(_x, _p(_x)) for _x in np.arange(-3.0, 3.01, 0.75)], k=_k)
    farrow(_ax, _g, (_g[0] + _k * _F(*_g)[0], _g[1] + _k * _F(*_g)[1]), BLUE, lw=2.0, zorder=6)
    _ax.plot(*_g, "o", color=BLUE, ms=3.3, zorder=7)
    # gamma(t) moves with its point (it names the moving point); the velocity is named once, in the free strip below
    _ax.annotate(r"$\gamma(t)$", _g, textcoords="offset points", xytext=(-4, 9), ha="right", va="bottom", fontsize=12, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    mo.vstack(
        [
            mo.hstack([lt], justify="start"),
            mo.hstack([_fig], justify="center"),
            mo.md(r"at every $t$, the velocity of $\gamma$ agrees with $\vec{F}$ at $\gamma(t)$!"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** $\gamma'(t) = \vec{F}(\gamma(t))$ is nothing but a 1st order system of ODEs!

    $\leadsto$ &nbsp; write $\gamma(t) = \begin{bmatrix} x(t) \\ y(t) \end{bmatrix}$, &nbsp; $\vec{F}(\gamma(t)) = \begin{bmatrix} P(x(t), y(t)) \\ Q(x(t), y(t)) \end{bmatrix}$

    $$
    \gamma'(t) = \vec{F}(\gamma(t)) \qquad \Longleftrightarrow \qquad \begin{cases} x'(t) = P(x(t), y(t)) \\ y'(t) = Q(x(t), y(t)) \end{cases}
    $$

    **Example.** &nbsp; $\vec{F}(\vec{x}) = \frac{1}{2}\begin{bmatrix} -y \\ x \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; find flow lines by solving

    $$
    \begin{aligned}
    & \begin{bmatrix} x'(t) \\ y'(t) \end{bmatrix} = \frac{1}{2}\begin{bmatrix} -y(t) \\ x(t) \end{bmatrix}, \qquad \gamma(0) = \begin{bmatrix} x_0 \\ y_0 \end{bmatrix} \\[10pt]
    \Longrightarrow \quad & \gamma(t) = \begin{bmatrix} x_0 \cos(t/2) - y_0 \sin(t/2) \\ x_0 \sin(t/2) + y_0 \cos(t/2) \end{bmatrix} \qquad \text{circular paths!}
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ct = mo.ui.slider(0, 12.56, 0.04, value=2.0, label="$t$", show_value=True)
    return (ct,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, beside, ct, cross_axes, farrow, label, math, mo, np, rot, sketch, vfield):
    # the flow line of F(x) = 1/2 (-y, x) through x0 = (2, 0): it turns by the angle t/2, once round for t up to 4 pi.
    # The field is drawn as on p. 2 (five circles of eight points, at true length); gamma is the circle of radius 2,
    # thin, and gamma'(t) is blue with a thicker shaft
    _t = round(ct.value, 10)
    _fig, _ax = sketch((-3.6, 3.6), (-3.6, 3.6))
    _x0 = (2.0, 0.0)
    _r, _a0 = 2.0, 0.0
    _g = (_r * math.cos(_a0 + _t / 2), _r * math.sin(_a0 + _t / 2))
    _names = [
        label(_ax, (-2.95, -1.3), r"$\gamma$", RED, 10, 14, fontsize=13),
        label(_ax, (2.2, 2.95), r"$\gamma'(t) = \vec{F}(\gamma(t))$", BLUE, 100, 18, fontsize=13),
        label(_ax, (-3.55, -3.2), r"$\vec{F}(\vec{x}) = \frac{1}{2}\genfrac{[}{]}{0}{0}{-y}{x}$", GREEN, 96, 34, fontsize=13, ha="left"),
    ]
    _names += cross_axes(_ax, (-3.5, 3.5), (-3.5, 3.5), "$x$", "$y$")
    _pts = [(0.5 * (_k + 1) * math.cos(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0)),
             0.5 * (_k + 1) * math.sin(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0))) for _k in range(5) for _j in range(8)]
    vfield(_ax, rot, GREEN, pts=_pts, k=1.0)
    _s = np.linspace(0, 2 * math.pi, 300)
    _ax.plot(_r * np.cos(_s), _r * np.sin(_s), color=RED, lw=1.6, zorder=3)
    farrow(_ax, _g, (_g[0] + rot(*_g)[0], _g[1] + rot(*_g)[1]), BLUE, lw=2.0, zorder=6)
    _ax.plot(*_x0, "o", color=BLUE, ms=3.3, zorder=7)
    _ax.plot(*_g, "o", color=BLUE, ms=3.3, zorder=7)
    beside(_ax, _g, math.degrees(_a0 + _t / 2) - 30, r"$\gamma(t)$", "black", 26, 16)
    beside(_ax, _x0, 32, r"$\vec{x}_0 = \gamma(0)$", "black", 62, 16, gap=3, fontsize=12)

    mo.vstack([mo.hstack([ct], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{aligned}
    \vec{H}(\vec{x}) = \frac{1}{2}\vec{x} \quad \leadsto \quad \sigma'(t) = \frac{1}{2}\sigma(t) \quad \leadsto \quad & \begin{bmatrix} x'(t) \\ y'(t) \end{bmatrix} = \frac{1}{2}\begin{bmatrix} x(t) \\ y(t) \end{bmatrix} \\[10pt]
    \Longrightarrow \quad & \sigma(t) = \begin{bmatrix} x_0 e^{t/2} \\ y_0 e^{t/2} \end{bmatrix} \qquad \text{radial paths}
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    rt = mo.ui.slider(-2, 2, 0.02, value=0, label="$t$", show_value=True)
    return (rt,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, beside, cross_axes, farrow, label, math, mo, rad, rt, sketch, vfield):
    # the flow line of H(x) = x/2 through x0 = (1, 1), a ray: sigma(t) = e^(t/2) x0 moves in towards 0 for
    # t < 0 and out for t > 0. The field is drawn as on p. 2 (the same points, at true length); sigma'(t) is blue with a
    # thicker shaft
    _t = round(rt.value, 10)
    _fig, _ax = sketch((-4.4, 4.4), (-4.4, 4.4))
    _x0 = (1.0, 1.0)
    _sg = (_x0[0] * math.exp(_t / 2), _x0[1] * math.exp(_t / 2))
    _tip = (_sg[0] + rad(*_sg)[0], _sg[1] + rad(*_sg)[1])
    _names = [
        label(_ax, (3.75, 4.15), r"$\sigma$", RED, 10, 14, fontsize=13),
        label(_ax, (2.8, 1.2), r"$\sigma'(t) = \vec{H}(\sigma(t))$", BLUE, 100, 18, fontsize=13),
        label(_ax, (-3.75, -3.35), r"$\vec{H}(\vec{x}) = \frac{1}{2}\vec{x}$", GREEN, 80, 22, fontsize=13, ha="left"),
    ]
    _names += cross_axes(_ax, (-4.3, 4.3), (-4.3, 4.3), "$x$", "$y$")
    _pts = [(0.5 * (_k + 1) * math.cos(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0)),
             0.5 * (_k + 1) * math.sin(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0))) for _k in range(5) for _j in range(8)]
    vfield(_ax, rad, GREEN, pts=_pts, k=1.0, avoid=_names)
    _ax.plot([0, 4.25], [0, 4.25], color=RED, lw=1.6, zorder=3)
    farrow(_ax, _sg, _tip, BLUE, lw=2.0, zorder=6)
    _ax.plot(*_x0, "o", color=BLUE, ms=3.3, zorder=7)
    _ax.plot(*_sg, "o", color=BLUE, ms=3.3, zorder=7)
    beside(_ax, _x0, -20, r"$\vec{x}_0 = \sigma(0)$", "black", 62, 16, gap=3, fontsize=12)
    # sigma(t) moves with its point, on the upper-left side of the ray
    _ax.annotate(r"$\sigma(t)$", _sg, textcoords="offset points", xytext=(-7, 5), ha="right", va="bottom", fontsize=12, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    mo.vstack([mo.hstack([rt], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""$\leadsto$ &nbsp; differentiation of vector fields?"""),
            definition(
                r"""
    Given $\vec{F}(\vec{x}) = \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \end{bmatrix}$ differentiable

    $$
    \Longrightarrow \qquad D\vec{F}(\vec{x}) = \begin{bmatrix} \dfrac{\partial P}{\partial x}(\vec{x}) & \dfrac{\partial P}{\partial y}(\vec{x}) \\[10pt] \dfrac{\partial Q}{\partial x}(\vec{x}) & \dfrac{\partial Q}{\partial y}(\vec{x}) \end{bmatrix} \quad \text{is well-defined}
    $$

    The **divergence** of $\vec{F}$ is the scalar function

    $$
    \mathrm{div}(\vec{F})(\vec{x}) = \vec{\nabla} \cdot \vec{F}(\vec{x}) = \frac{\partial P}{\partial x}(\vec{x}) + \frac{\partial Q}{\partial y}(\vec{x}) = \mathrm{tr}\big( D\vec{F}(\vec{x}) \big)
    $$
    """,
                "Divergence",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $\vec{\nabla} \cdot \vec{F}(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \end{bmatrix}$ &nbsp; useful abuse of notation!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What does $\mathrm{div}(\vec{F})$ tell us about $\vec{F}$?

    $\leadsto$ &nbsp; $\mathrm{div}(\vec{F})(\vec{x})$ = rate of compression/expansion of “area at $\vec{x}$” under the “flow of $\vec{F}$”

    **Example.** &nbsp; $\vec{F}(\vec{x}) = \frac{1}{2}\begin{bmatrix} -y \\ x \end{bmatrix}$ &nbsp; rotation vector field

    $$
    \Longrightarrow \qquad \mathrm{div}(\vec{F})(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \frac{1}{2}\begin{bmatrix} -y \\ x \end{bmatrix} = \frac{1}{2}\left( \frac{\partial}{\partial x}(-y) + \frac{\partial}{\partial y}(x) \right) = 0
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    at = mo.ui.slider(0, 6.28, 0.04, value=2.0, label="$t$", show_value=True)
    return (at,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, LIGHT, RED, area, at, beside, chevron, cross_axes, disc_patch, label, math, mo, np, num, rot, sketch, table, vfield):
    # the flow of F(x) = 1/2 (-y, x) turns every point of the disc around x0 by the angle t/2: the moved patch is the image of the disc
    # the two flow circles pass through the field's own points (radius 1 and 2), so the arrows there are tangent to them
    _r1, _r2, _rc, _a, _rho = 1.0, 2.0, 1.5, math.radians(50), 0.5
    _t = round(at.value, 10)
    _fig, _ax = sketch((-3.5, 3.5), (-3.5, 3.5))
    _x0 = (_rc * math.cos(_a), _rc * math.sin(_a))
    _g = (_rc * math.cos(_a + _t / 2), _rc * math.sin(_a + _t / 2))
    # the field as on p. 2 (five circles of eight points, at true length)
    _pts = [(0.5 * (_k + 1) * math.cos(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0)),
             0.5 * (_k + 1) * math.sin(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0))) for _k in range(5) for _j in range(8)]
    _names = [label(_ax, (2.3, -3.2), r"flow lines of $\vec{F}$", RED, 100, 18, fontsize=13)]
    _names += cross_axes(_ax, (-3.4, 3.4), (-3.4, 3.4), "$x$", "$y$")
    vfield(_ax, rot, GREEN, pts=_pts, k=1.0, avoid=_names)
    _s = np.linspace(0, 2 * math.pi, 300)
    for _rr in (_r1, _r2):
        _ax.plot(_rr * np.cos(_s), _rr * np.sin(_s), color=RED, lw=1.3, zorder=3)
        for _hh in (math.radians(-110), math.radians(70)):
            chevron(_ax, (_rr * math.cos(_hh), _rr * math.sin(_hh)), _hh + math.pi / 2, RED, lw=1.2)
    _bx, _by = disc_patch(_x0, _rho)
    _c, _sn = math.cos(_t / 2), math.sin(_t / 2)
    _mx, _my = _c * _bx - _sn * _by, _sn * _bx + _c * _by
    for _px, _py in ((_bx, _by), (_mx, _my)):
        _ax.fill(_px, _py, color=LIGHT, alpha=0.9, lw=0, zorder=4)
        _ax.plot(np.append(_px, _px[0]), np.append(_py, _py[0]), color=BLUE, lw=1.3, zorder=5)
    _ax.plot(*_x0, "o", color=BLUE, ms=3, zorder=7)
    _ax.plot(*_g, "o", color=BLUE, ms=3, zorder=7)
    # x0 named outside its patch, away from the origin; gamma(t) ahead of its patch, along the circle the patch follows
    beside(_ax, (_x0[0] * (1 + (_rho + 0.02) / _rc), _x0[1] * (1 + (_rho + 0.02) / _rc)), math.degrees(_a), r"$\vec{x}_0$", "black", 16, 14, gap=2)
    _f = _a + _t / 2 + (_rho + 0.04) / _rc
    beside(_ax, (_rc * math.cos(_f), _rc * math.sin(_f)), math.degrees(_f) + 90, r"$\gamma(t)$", "black", 26, 16, gap=2)

    mo.vstack(
        [
            mo.hstack([at], justify="start"),
            mo.hstack([_fig], justify="center"),
            table([(r"$\dfrac{\text{area of moved patch}}{\text{area of patch at } \vec{x}_0}$", rf"$= {num(round(area(_mx, _my) / area(_bx, _by), 6))}$")]),
            mo.md(r"“flow of $\vec{F}$” does not compress/expand the area around any point $\vec{x}_0$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\vec{H}(\vec{x}) = \frac{1}{2}\begin{bmatrix} x \\ y \end{bmatrix}$ &nbsp; radial vector field

    $$
    \Longrightarrow \qquad \mathrm{div}(\vec{H})(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \frac{1}{2}\begin{bmatrix} x \\ y \end{bmatrix} = \frac{1}{2}\left( \frac{\partial}{\partial x}(x) + \frac{\partial}{\partial y}(y) \right) = 1 > 0
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    st = mo.ui.slider(-2, 2, 0.02, value=1.0, label="$t$", show_value=True)
    return (st,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, LIGHT, RED, area, beside, cross_axes, disc_patch, flow_rays, math, mo, np, num, rad, sketch, st, table, vfield):
    # the flow of H(x) = x/2 moves every point of the disc around x0 to e^(t/2) times itself: the moved patch is the image of the disc
    _rc, _a, _rho = 1.0, math.radians(67.5), 0.35
    _t = round(st.value, 10)
    _e = math.exp(_t / 2)
    _fig, _ax = sketch((-4.0, 4.0), (-4.0, 4.0))
    _x0 = (_rc * math.cos(_a), _rc * math.sin(_a))
    _sg = (_e * _x0[0], _e * _x0[1])
    # the field as on p. 2 (the same points, at true length)
    _pts = [(0.5 * (_k + 1) * math.cos(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0)),
             0.5 * (_k + 1) * math.sin(math.pi / 4 * _j + (math.pi / 8 if _k % 2 == 0 else 0))) for _k in range(5) for _j in range(8)]
    _names = cross_axes(_ax, (-3.9, 3.9), (-3.9, 3.9), "$x$", "$y$")
    # eight rays along the axes and diagonals, with a direction mark part-way; the patch stays in the wedge between the
    # diagonal and the vertical axis;
    # the field arrows that lie on a ray are left out (they would hide under it)
    _rays = [(np.linspace(0, 3.9, 80) * math.cos(math.radians(45 * _j)), np.linspace(0, 3.9, 80) * math.sin(math.radians(45 * _j))) for _j in range(8)]
    vfield(_ax, rad, GREEN, pts=_pts, k=1.0, avoid=_names, cross=_rays)
    flow_rays(_ax, [math.radians(45 * _j) for _j in range(8)], 3.9, RED, lw=1.6, mark=0.45, zorder=3)
    _bx, _by = disc_patch(_x0, _rho)
    _mx, _my = _e * _bx, _e * _by
    for _px, _py in ((_bx, _by), (_mx, _my)):
        _ax.fill(_px, _py, color=LIGHT, alpha=0.9, lw=0, zorder=4)
        _ax.plot(np.append(_px, _px[0]), np.append(_py, _py[0]), color=BLUE, lw=1.3, zorder=5)
    _ax.plot(*_x0, "o", color=BLUE, ms=3, zorder=7)
    _ax.plot(*_sg, "o", color=BLUE, ms=3, zorder=7)
    # x0 named between its patch and the origin, sigma(t) beyond its patch, away from the origin
    _fi = 1 - (_rho + 0.02) / _rc
    _fo = 1 + (_rho + 0.02) / _rc
    _q = (_x0[0] + (_rho + 0.04) * math.cos(math.radians(-45)), _x0[1] + (_rho + 0.04) * math.sin(math.radians(-45)))
    beside(_ax, _q, -45, r"$\vec{x}_0$", "black", 16, 14, gap=2)
    beside(_ax, (_fo * _sg[0], _fo * _sg[1]), math.degrees(_a), r"$\sigma(t)$", "black", 26, 16, gap=2)

    mo.vstack(
        [
            mo.hstack([st], justify="start"),
            mo.hstack([_fig], justify="center"),
            table([(r"$\dfrac{\text{area of moved patch}}{\text{area of patch at } \vec{x}_0}$", rf"$= e^{{t}} = {num(round(area(_mx, _my) / area(_bx, _by), 6))}$")]),
            mo.md(r"“flow of $\vec{H}$” expands the area around each $\vec{x}$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \vec{G}(\vec{x}) = \begin{cases} \dfrac{1}{\lVert \vec{x} \rVert} \begin{bmatrix} -y \\ x \end{bmatrix}, & \vec{x} \neq \vec{0} \\[10pt] \vec{0}, & \vec{x} = \vec{0} \quad \longleftarrow \ \vec{G} \text{ not differentiable at } \vec{0} \end{cases}
    $$

    $$
    \begin{aligned}
    \text{for } \vec{x} \neq \vec{0}: \quad \mathrm{div}(\vec{G})(\vec{x}) & = \frac{\partial}{\partial x} \left( \frac{-y}{\sqrt{x^2 + y^2}} \right) + \frac{\partial}{\partial y} \left( \frac{x}{\sqrt{x^2 + y^2}} \right) \\[1ex]
    & = \frac{xy}{(x^2 + y^2)^{3/2}} - \frac{xy}{(x^2 + y^2)^{3/2}} = 0
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    gt = mo.ui.slider(0, 4, 0.05, value=1.5, label="$t$", show_value=True)
    return (gt,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, LIGHT, RED, area, beside, chevron, cross_axes, disc_patch, gt, math, mo, np, num, sketch, table, unit_rot, vfield):
    # the flow of G: every point moves at unit speed on its circle, so a point at distance r from the origin turns
    # by the angle t / r; the moved patch is the image of the disc around x0
    _rc, _a, _rho = 1.5, math.radians(50), 0.5
    _t = round(gt.value, 10)
    _fig, _ax = sketch((-3.1, 3.1), (-3.1, 3.1))
    _x0 = (_rc * math.cos(_a), _rc * math.sin(_a))
    # the field as on p. 2 (the points of the unit rotation field, every arrow of length 1/2)
    _pts = [(0.5 * _k * np.cos(2 * np.pi * _j / (3 * _k + 3)), 0.5 * _k * np.sin(2 * np.pi * _j / (3 * _k + 3)))
            for _k in range(1, 6) for _j in range(3 * _k + 3)]
    _names = cross_axes(_ax, (-3.0, 3.0), (-3.0, 3.0), "$x$", "$y$")
    vfield(_ax, unit_rot, GREEN, pts=_pts, avoid=_names)
    _s = np.linspace(0, 2 * math.pi, 300)
    for _rr in (_rc - _rho, _rc + _rho):
        _ax.plot(_rr * np.cos(_s), _rr * np.sin(_s), color=RED, lw=1.6, zorder=3)
        for _hh in (math.radians(-110), math.radians(170)):
            chevron(_ax, (_rr * math.cos(_hh), _rr * math.sin(_hh)), _hh + math.pi / 2, RED, lw=1.2)
    _bx, _by = disc_patch(_x0, _rho, n=4000)
    _ang = _t / np.hypot(_bx, _by)
    _mx, _my = np.cos(_ang) * _bx - np.sin(_ang) * _by, np.sin(_ang) * _bx + np.cos(_ang) * _by
    for _px, _py in ((_bx, _by), (_mx, _my)):
        _ax.fill(_px, _py, color=LIGHT, alpha=0.9, lw=0, zorder=4)
        _ax.plot(np.append(_px, _px[0]), np.append(_py, _py[0]), color=BLUE, lw=1.3, zorder=5)
    _ax.plot(*_x0, "o", color=BLUE, ms=3, zorder=7)
    # the centre of the disc moves too: at distance rc it turns by t / rc
    _ax.plot(_rc * math.cos(_a + _t / _rc), _rc * math.sin(_a + _t / _rc), "o", color=BLUE, ms=3, zorder=7)
    # x0 named behind its patch (clockwise), where no moved point goes
    _b = _a - (_rho + 0.04) / _rc
    beside(_ax, (_rc * math.cos(_b), _rc * math.sin(_b)), math.degrees(_b) - 90, r"$\vec{x}_0$", "black", 16, 14, gap=2)

    mo.vstack(
        [
            mo.hstack([gt], justify="start"),
            mo.hstack([_fig], justify="center"),
            table([(r"$\dfrac{\text{area of moved patch}}{\text{area of patch at } \vec{x}_0}$", rf"$= {num(round(area(_mx, _my) / area(_bx, _by), 6))}$")]),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
