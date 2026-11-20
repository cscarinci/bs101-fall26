import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 21 • Green's theorem", css_file="bs101.css")


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

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        One line weight for every figure; the head is open and sized in points from the line width,
        so arrows look alike across lectures at any axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={4.5 * lw:g},head_width={2 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    return BLUE, GREEN, GREY, LIGHT, ORANGE, RED, arrow, corollary, definition, header, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 21", "Week 12", "Lecture 21 • Green's theorem")
    return


@app.cell(hide_code=True)
def _(Figure, arrow, math, np):
    # ---- Helpers of this lecture ----------------------------------------
    def sketch(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges;
        the scale never changes with a slider (names are kept inside the ranges)."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def beside(ax, at, angle, text, color, w, h, gap=4, fontsize=13):
        """Name centred beside the point `at`, in the direction `angle` (degrees), far enough for a
        w x h box (points) to clear it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        d = w / 2 * abs(c) + h / 2 * abs(s) + gap
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    def plane(xlim, ylim, width):
        """A sketch of the xy-plane: the two axes as arrows, named at their tips."""
        fig, ax = sketch(xlim, ylim, width)
        arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, "$x$", "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, "$y$", "black", 10, 12)
        return fig, ax

    def along(ax, x, y, color, at=(0.5,), lw=1.8):
        """Arrowheads on the curve through the points (x[k], y[k]), at the fractions `at` of its points,
        pointing the way the points run."""
        n = len(x)
        for f in at:
            k = round(f * (n - 1))
            j = max(k - max(n // 40, 1), 0)
            ax.annotate("", xy=(x[k], y[k]), xytext=(x[j], y[j]), zorder=5, arrowprops={"arrowstyle": f"->,head_length={4.5 * lw:g},head_width={2 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0})

    def blob(cy):
        """The closed curve of the two sketches of a region with its boundary (pp. 1 and 2), run counter-clockwise
        about the point (2.3, cy): two arrays."""
        s = np.linspace(0, 2 * np.pi, 400)
        r = 1 + 0.1 * np.cos(3 * s) + 0.06 * np.sin(2 * s)
        return 2.3 + 1.5 * r * np.cos(s), cy + 0.95 * r * np.sin(s)

    def walker(ax, at, h=0.5, color="black"):
        """A walking figure of height h centred at the point `at`: head, body, arms and legs."""
        x, y = at[0], at[1] - h / 2
        s = np.linspace(0, 2 * np.pi, 40)
        ax.plot(x + 0.13 * h * np.cos(s), y + 0.87 * h + 0.13 * h * np.sin(s), color=color, lw=1.1, zorder=7)
        for u, v in (([0, 0], [0.74, 0.36]), ([-0.2, 0, 0.2], [0.46, 0.62, 0.46]), ([-0.16, 0, 0.16], [0, 0.36, 0])):
            ax.plot(x + h * np.array(u), y + h * np.array(v), color=color, lw=1.1, zorder=7, solid_capstyle="round")

    return along, beside, blob, plane, sketch, walker


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Double integration over simple regions in $\mathbb{R}^2$

    A region $D \subseteq \mathbb{R}^2$ is called $y$-simple if

    $$
    D = \left\{ (x, y) \in \mathbb{R}^2 \mid a \leq x \leq b, \ \varphi_1(x) \leq y \leq \varphi_2(x) \right\}
    $$

    for continuous functions $\varphi_1, \varphi_2 : [a, b] \longrightarrow \mathbb{R}$

    $$
    \leadsto \quad \iint_D f(x, y) \, dxdy = \int_a^b \left( \int_{\varphi_1(x)}^{\varphi_2(x)} f(x, y) \, dy \right) dx
    $$

    $x$-simple if

    $$
    D = \left\{ (x, y) \in \mathbb{R}^2 \mid c \leq y \leq d, \ \psi_1(y) \leq x \leq \psi_2(y) \right\}
    $$

    for continuous functions $\psi_1, \psi_2 : [c, d] \longrightarrow \mathbb{R}$

    $$
    \leadsto \quad \iint_D f(x, y) \, dxdy = \int_c^d \left( \int_{\psi_1(y)}^{\psi_2(y)} f(x, y) \, dx \right) dy
    $$

    **Earlier:** Line integrals of vector fields over curves

    $$
    \underbrace{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}_{\mathclap{\footnotesize \vec{C} = \gamma([a, b])}} = \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, arrow, beside, mo, np, sketch):
    # the curve C = gamma([a, b]) (red) from gamma(a) to gamma(b) (p. 1); at the point gamma(t) (blue), its velocity gamma'(t)
    # (blue) and the vector F(gamma(t)) of a vector field (green). The curve is the one of lecture 19's sketches
    def _g(s):
        return np.array([s, 0.9 * np.sin(1.1 * s) + 0.3 * s])

    _a, _b, _t = 0.0, 4.8, 1.2
    _fig, _ax = sketch((-1.0, 5.8), (-0.5, 2.3), 4.4)
    _ax.plot(*_g(np.linspace(_a, _b, 300)), color=RED, lw=1.8)
    _p = _g(_t)
    _v = np.array([1.0, 0.99 * np.cos(1.1 * _t) + 0.3])
    _f = np.array([0.75, -0.55])
    arrow(_ax, _p, _p + _f, GREEN, lw=1.6)
    arrow(_ax, _p, _p + _v, BLUE, lw=1.6)
    for _q, _c in ((_g(_a), RED), (_g(_b), RED), (_p, BLUE)):
        _ax.plot(*_q, "o", color=_c, ms=4.5, zorder=6)
    beside(_ax, _g(_a), 180, r"$\gamma(a)$", "black", 30, 16)
    beside(_ax, _g(_b), 0, r"$\gamma(b)$", "black", 30, 16)
    beside(_ax, _p, 135, r"$\gamma(t)$", "black", 30, 16)
    beside(_ax, _p + _v, 0, r"$\gamma'(t)$", BLUE, 30, 16)
    beside(_ax, _p + _f, -90, r"$\vec{F}(\gamma(t))$", GREEN, 52, 18)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \text{FTC} \quad \Longrightarrow \quad \int_{\vec{C}} \vec{\nabla} f \cdot d\vec{s} = f(\gamma(b)) - f(\gamma(a))
    $$

    **In this lecture:** Green's theorem

    $\leadsto$ &nbsp; relation between double integral over simple regions and line integral over their boundary curve
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, RED, along, beside, blob, mo, plane):
    # a region D and its boundary curve C = Bd(D) (red), run counter-clockwise (p. 1, at "Today")
    _x, _y = blob(1.6)
    _fig, _ax = plane((-0.6, 5.0), (-0.5, 3.4), 3.8)
    _ax.fill(_x, _y, color=LIGHT, lw=0, zorder=0)
    _ax.plot(_x, _y, color=RED, lw=1.8)
    along(_ax, _x, _y, RED, at=(0.3, 0.62, 0.95))
    _ax.text(2.3, 1.6, "$D$", color=BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x[45], _y[45]), 45, r"$\vec{C} = \mathrm{Bd}(D)$", RED, 84, 18, gap=2)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **References:** MT 8.1, 8.3

    ## IV.5 &nbsp; Green's theorem
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given $D \subseteq \mathbb{R}^2$ a simple region, let $C = \mathrm{Bd}(D)$ denote its boundary points. We denote by $\vec{C}$ the curve $C$ with the $\underbrace{\text{counter-clockwise orientation}}_{\mathclap{\footnotesize \text{walking around } \vec{C}, \ D \text{ is always on the left}}\vphantom{\footnotesize \text{walking around } \vec{C}, \ D \text{ is always on the left}}}$.

    We denote by $\vec{C}^{\,op}$ the curve $C$ with the opposite orientation ($\underbrace{\text{clockwise}}_{\mathclap{\footnotesize D \text{ is always on the right}}\vphantom{\footnotesize D \text{ is always on the right}}}$)

    We also call

    $$
    \text{counter-clockwise orientation} = \textbf{positive orientation}
    $$

    $$
    \text{clockwise orientation} = \textbf{negative orientation}
    $$
    """,
        "Orientation of the boundary",
    )
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, RED, arrow, beside, blob, math, mo, plane, walker):
    # the curve C (red) around the region D (p. 2): the two walking figures go around it counter-clockwise, each in the
    # direction of its arrow, with D on their left
    _x, _y = blob(2.1)
    _fig, _ax = plane((-0.6, 5.0), (-0.5, 4.3), 3.8)
    _ax.fill(_x, _y, color=LIGHT, lw=0, zorder=0)
    _ax.plot(_x, _y, color=RED, lw=1.8)
    _ax.text(2.3, 2.1, "$D$", color=BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x[150], _y[150]), 135, r"$\vec{C}$", RED, 14, 18)
    for _k in (62, 277):
        # beside the point k of the curve, on its outer side; the arrow starts ahead of the figure, along the curve
        _tx, _ty = _x[_k + 1] - _x[_k - 1], _y[_k + 1] - _y[_k - 1]
        _n = math.hypot(_tx, _ty)
        _tx, _ty = _tx / _n, _ty / _n
        _cx, _cy = _x[_k] + 0.36 * _ty, _y[_k] - 0.36 * _tx
        walker(_ax, (_cx, _cy), h=0.56)
        arrow(_ax, (_cx + 0.3 * _tx, _cy + 0.3 * _ty), (_cx + 0.95 * _tx, _cy + 0.95 * _ty), "black", lw=1.2)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given a $\underbrace{\text{simple}}_{\mathclap{\footnotesize \text{both } y\text{-simple and } x\text{-simple}}\vphantom{\footnotesize \text{both } y\text{-simple and } x\text{-simple}}}$ region $D \subseteq \mathbb{R}^2$, $\vec{C} = \mathrm{Bd}(D)$ with the positive orientation, and $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$ a $C^1$-smooth vector field on $D$, then

    $$
    \underbrace{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}_{\mathclap{\footnotesize \begin{matrix} \text{line integral} \\ \text{over the boundary} \end{matrix}}} = \underbrace{\iint_D \left( \frac{\partial Q}{\partial x}(x, y) - \frac{\partial P}{\partial y}(x, y) \right) dxdy}_{\footnotesize \begin{matrix} \text{double integral of some derivative of } \vec{F} \\ \leadsto \ \text{scalar curl} \end{matrix}}
    $$
    """,
        "Green",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; generalization of FTC!

    **Example.** &nbsp; $D = \left\{ (x, y) \mid x^2 \leq y \leq 1 \right\}$, &nbsp; $\vec{F}(x, y) = \begin{bmatrix} -y^2 \\ xy \end{bmatrix}$

    <span class="chain">$\displaystyle C = \mathrm{Bd}(D) = \underbrace{\left\{ (x, y) \mid -1 \leq x \leq 1, \ y = x^2 \right\}}_{\footnotesize C_1}$ $\displaystyle \cup \ \underbrace{\left\{ (x, y) \mid -1 \leq x \leq 1, \ y = 1 \right\}}_{\footnotesize C_2}$</span>

    <span class="chain">$\displaystyle \vec{C} = \big\{ \underbrace{(t, t^2)}_{\footnotesize \gamma_1(t)} \mid t \in [-1, 1] \big\}$ $\displaystyle \cup \ \big\{ \underbrace{(-t, 1)}_{\footnotesize \gamma_2(t)} \mid t \in [-1, 1] \big\}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    tc = mo.ui.slider(-1.0, 1.0, 0.02, value=0.5, label="$t$", show_value=True)
    return (tc,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, LIGHT, ORANGE, RED, along, beside, math, mo, np, plane, tc):
    # the region D of the example (p. 3) and its boundary: C_1 (red), the parabola from (-1, 1) to (1, 1), and C_2 (orange),
    # the segment from (1, 1) back to (-1, 1). The points gamma_1(t) = (t, t^2) and gamma_2(t) = (-t, 1) (green) move with t
    _t = round(tc.value, 10)
    _fig, _ax = plane((-1.8, 2.25), (-0.5, 2.05), 4.6)
    _d = np.linspace(-1, 1, 200)
    _ax.fill_between(_d, _d**2, 1, color=LIGHT, lw=0, zorder=0)
    _ax.plot(_d, _d**2, color=RED, lw=1.8)
    _ax.plot([1, -1], [1, 1], color=ORANGE, lw=1.8)
    along(_ax, _d, _d**2, RED, at=(0.3, 0.8))
    along(_ax, -_d, 1 + 0 * _d, ORANGE, at=(0.3, 0.8))
    beside(_ax, (-0.75, 0.75**2), 205, r"$\vec{C}_1$", RED, 16, 18)
    beside(_ax, (0.5, 1), 90, r"$\vec{C}_2$", ORANGE, 16, 18)
    _box = {"boxstyle": "round,pad=0.1", "facecolor": LIGHT, "edgecolor": "none"}
    _ax.text(0, 0.56, "$D$", color=BLUE, fontsize=13, ha="center", va="center", zorder=5, bbox=_box)
    # the two moving points are named inside D, each on the side of the middle of D, on the colour of D (so that the y axis does
    # not strike a name through) and farther from its point near the two corners, where D is narrow; the names of the
    # curves stay outside, where nothing moves
    for _p, _name in (((_t, _t**2), r"$\gamma_1(t)$"), ((-_t, 1), r"$\gamma_2(t)$")):
        _ax.plot(*_p, "o", color=GREEN, ms=4.5, zorder=7)
        _c, _s = -_p[0], 0.56 - _p[1]
        _c, _s = _c / math.hypot(_c, _s), _s / math.hypot(_c, _s)
        _r = 16 * abs(_c) + 8 * abs(_s) + 5 + 10 * _p[0] ** 2
        _ax.annotate(_name, _p, textcoords="offset points", xytext=(_r * _c, _r * _s), ha="center", va="center", color=GREEN, fontsize=13, zorder=6, bbox=_box)
    mo.vstack([mo.hstack([tc], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_{\vec{C}_1} \vec{F} \cdot d\vec{s} + \int_{\vec{C}_2} \vec{F} \cdot d\vec{s}$ $\displaystyle = \int_{-1}^1 \begin{bmatrix} -t^4 \\ t^3 \end{bmatrix} \cdot \begin{bmatrix} 1 \\ 2t \end{bmatrix} dt + \int_{-1}^1 \begin{bmatrix} -1 \\ -t \end{bmatrix} \cdot \begin{bmatrix} -1 \\ 0 \end{bmatrix} dt$ $\displaystyle = \int_{-1}^1 (-t^4 + 2t^4) \, dt + \int_{-1}^1 (1 + 0) \, dt = \frac{2}{5} + 2 = \frac{12}{5}$</span>

    <span class="chain">$\displaystyle \iint_D \bigg( \underbrace{\frac{\partial Q}{\partial x}(x, y)}_{\footnotesize y} - \underbrace{\frac{\partial P}{\partial y}(x, y)}_{\footnotesize -2y} \bigg) dxdy = \iint_D (3y) \, dxdy$ $\displaystyle = 3 \int_{-1}^1 \left( \int_{x^2}^1 y \, dy \right) dx = 3 \int_{-1}^1 \left( \frac{1}{2} - \frac{x^4}{2} \right) dx$ $\displaystyle = 3 \left( \frac{x}{2} - \frac{x^5}{10} \right) \bigg|_{x=-1}^{x=1} = 3 \left( \frac{2}{2} - \frac{2}{10} \right) = 3 \cdot \frac{4}{5}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof.** Write

    <span class="chain">$\displaystyle \vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix} = \underbrace{\begin{bmatrix} P(x, y) \\ 0 \end{bmatrix}}_{\footnotesize \vec{F}_1(x, y)} + \underbrace{\begin{bmatrix} 0 \\ Q(x, y) \end{bmatrix}}_{\footnotesize \vec{F}_2(x, y)}$ $\displaystyle \Longrightarrow \quad \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_{\vec{C}} \vec{F}_1 \cdot d\vec{s} + \int_{\vec{C}} \vec{F}_2 \cdot d\vec{s}$</span>

    For $\vec{F}_1 = \begin{bmatrix} P \\ 0 \end{bmatrix}$, treat $D$ as a $y$-simple region &nbsp; $D = \left\{ (x, y) \mid a \leq x \leq b, \ \varphi_1(x) \leq y \leq \varphi_2(x) \right\}$

    <span class="chain">$\displaystyle \Longrightarrow \quad \mathrm{Bd}(D) = \left\{ (x, \varphi_1(x)) \mid x \in [a, b] \right\} \cup \left\{ (b, y) \mid y \in [\varphi_1(b), \varphi_2(b)] \right\}$ $\displaystyle \cup \ \left\{ (x, \varphi_2(x)) \mid x \in [a, b] \right\} \cup \left\{ (a, y) \mid y \in [\varphi_1(a), \varphi_2(a)] \right\}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, along, beside, mo, np, plane):
    # the first sketch of the proof (p. 4): D as a y-simple region. Its boundary, run counter-clockwise: the graph y = phi_1(x)
    # (red) to the right, the side x = b (blue) upwards, the graph y = phi_2(x) (orange) to the left, the side x = a (blue)
    # downwards
    _s = np.linspace(1.3, 3.8, 200)
    _lo, _hi = 0.9 + 0.18 * np.sin(4 * _s - 2.4), 2.3 + 0.2 * np.sin(3 * _s - 1.8)
    _fig, _ax = plane((-0.6, 5.5), (-0.5, 3.6), 4.2)
    _ax.fill_between(_s, _lo, _hi, color=LIGHT, lw=0, zorder=0)
    _ax.plot(_s, _lo, color=RED, lw=1.8)
    _ax.plot(_s, _hi, color=ORANGE, lw=1.8)
    along(_ax, _s, _lo, RED)
    along(_ax, _s[::-1], _hi[::-1], ORANGE)
    for _e, _d in ((0, -1), (-1, 1)):
        _v = np.linspace(_lo[_e], _hi[_e], 60)[::_d]
        _ax.plot(_s[_e] + 0 * _v, _v, color=BLUE, lw=1.8)
        along(_ax, _s[_e] + 0 * _v, _v, BLUE, at=(0.6,))
    beside(_ax, (_s[100], _lo.min()), -90, r"$y = \varphi_1(x)$", RED, 72, 16, gap=6)
    beside(_ax, (_s[100], _hi.max()), 90, r"$y = \varphi_2(x)$", ORANGE, 72, 16, gap=6)
    beside(_ax, (_s[0], (_lo[0] + _hi[0]) / 2), 180, "$x = a$", BLUE, 38, 16, gap=6)
    beside(_ax, (_s[-1], (_lo[-1] + _hi[-1]) / 2), 0, "$x = b$", BLUE, 38, 16, gap=6)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \Longrightarrow \quad \int_{\vec{C}} \vec{F}_1 \cdot d\vec{s} = \int_a^b \begin{bmatrix} P(t, \varphi_1(t)) \\ 0 \end{bmatrix} \cdot \underbrace{\begin{bmatrix} 1 \\ \varphi_1'(t) \end{bmatrix}}_{\mathclap{\footnotesize \begin{matrix} \text{here we need} \\ \varphi_1, \varphi_2 \text{ differentiable} \end{matrix}}} dt$ $\displaystyle + \int_{\varphi_1(b)}^{\varphi_2(b)} \begin{bmatrix} P(b, t) \\ 0 \end{bmatrix} \cdot \begin{bmatrix} 0 \\ 1 \end{bmatrix} dt$ $\displaystyle \underbrace{- \int_a^b \begin{bmatrix} P(t, \varphi_2(t)) \\ 0 \end{bmatrix} \cdot \begin{bmatrix} 1 \\ \varphi_2'(t) \end{bmatrix} dt - \int_{\varphi_1(a)}^{\varphi_2(a)} \begin{bmatrix} P(a, t) \\ 0 \end{bmatrix} \cdot \begin{bmatrix} 0 \\ 1 \end{bmatrix} dt}_{\footnotesize \text{parameterization has opposite orientation}}$</span>

    <span class="chain">$\displaystyle \Longrightarrow \quad \int_{\vec{C}} \vec{F}_1 \cdot d\vec{s} = \int_a^b \big( P(x, \varphi_1(x)) - P(x, \varphi_2(x)) \big) \, dx$ $\displaystyle = \int_a^b \left( \int_{\varphi_2(x)}^{\varphi_1(x)} \frac{\partial P}{\partial y}(x, y) \, dy \right) dx$ $\displaystyle = - \int_a^b \left( \int_{\varphi_1(x)}^{\varphi_2(x)} \frac{\partial P}{\partial y}(x, y) \, dy \right) dx = - \iint_D \frac{\partial P}{\partial y}(x, y) \, dxdy$</span>

    Similarly, for $\vec{F}_2 = \begin{bmatrix} 0 \\ Q \end{bmatrix}$, treat $D$ as $x$-simple &nbsp; $D = \left\{ (x, y) \mid c \leq y \leq d, \ \psi_1(y) \leq x \leq \psi_2(y) \right\}$

    <span class="chain">$\displaystyle \Longrightarrow \quad \mathrm{Bd}(D) = \left\{ (x, c) \mid x \in [\psi_1(c), \psi_2(c)] \right\} \cup \left\{ (\psi_2(y), y) \mid y \in [c, d] \right\}$ $\displaystyle \cup \ \left\{ (x, d) \mid x \in [\psi_1(d), \psi_2(d)] \right\} \cup \left\{ (\psi_1(y), y) \mid y \in [c, d] \right\}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, along, beside, mo, np, plane):
    # the second sketch of the proof (p. 5): D as an x-simple region. Its boundary, run counter-clockwise: the side y = c (blue)
    # to the right, the curve x = psi_2(y) (orange) upwards, the side y = d (blue) to the left, the curve x = psi_1(y) (red)
    # downwards
    _t = np.linspace(0.9, 3.0, 200)
    _l, _r = 2.1 + 0.18 * np.sin(4 * _t - 1.2), 3.5 + 0.2 * np.sin(3 * _t - 0.9)
    _fig, _ax = plane((-0.6, 5.9), (-0.5, 3.9), 4.2)
    _ax.fill_betweenx(_t, _l, _r, color=LIGHT, lw=0, zorder=0)
    _ax.plot(_l, _t, color=RED, lw=1.8)
    _ax.plot(_r, _t, color=ORANGE, lw=1.8)
    along(_ax, _l[::-1], _t[::-1], RED)
    along(_ax, _r, _t, ORANGE)
    for _e, _d in ((0, 1), (-1, -1)):
        _u = np.linspace(_l[_e], _r[_e], 60)[::_d]
        _ax.plot(_u, _t[_e] + 0 * _u, color=BLUE, lw=1.8)
        along(_ax, _u, _t[_e] + 0 * _u, BLUE, at=(0.6,))
    beside(_ax, (_l[100], _t[100]), 180, r"$x = \psi_1(y)$", RED, 72, 16, gap=6)
    beside(_ax, (_r[100], _t[100]), 0, r"$x = \psi_2(y)$", ORANGE, 72, 16, gap=6)
    beside(_ax, ((_l[0] + _r[0]) / 2, _t[0]), -90, "$y = c$", BLUE, 38, 16, gap=6)
    beside(_ax, ((_l[-1] + _r[-1]) / 2, _t[-1]), 90, "$y = d$", BLUE, 38, 16, gap=6)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \Longrightarrow \quad \int_{\vec{C}} \vec{F}_2 \cdot d\vec{s} = \int_c^d \big( Q(\psi_2(y), y) - Q(\psi_1(y), y) \big) \, dy$ $\displaystyle = \int_c^d \left( \int_{\psi_1(y)}^{\psi_2(y)} \frac{\partial Q}{\partial x}(x, y) \, dx \right) dy = \iint_D \frac{\partial Q}{\partial x}(x, y) \, dxdy$</span>

    $$
    \Longrightarrow \quad \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_{\vec{C}} (\vec{F}_1 + \vec{F}_2) \cdot d\vec{s} = \iint_D \left( \frac{\partial Q}{\partial x}(x, y) - \frac{\partial P}{\partial y}(x, y) \right) dxdy \tag*{$\square$}
    $$

    **Example.** &nbsp; $D = \left\{ (x, y) \mid \dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} \leq 1 \right\}$ &nbsp; $\leadsto$ &nbsp; inside an ellipse
    """)
    return


@app.cell(hide_code=True)
def _(LIGHT, RED, beside, mo, np, plane):
    # the region D inside the ellipse (p. 6), which crosses the x axis at -a and a and the y axis at -b and b
    _a, _b = 1.7, 1.05
    _s = np.linspace(0, 2 * np.pi, 300)
    _fig, _ax = plane((-2.6, 2.9), (-1.7, 2.0), 4.2)
    _ax.fill(_a * np.cos(_s), _b * np.sin(_s), color=LIGHT, lw=0, zorder=0)
    _ax.plot(_a * np.cos(_s), _b * np.sin(_s), color=RED, lw=1.8)
    for _p, _angle, _name in (((-_a, 0), -135, "$-a$"), ((_a, 0), -45, "$a$"), ((0, -_b), -135, "$-b$"), ((0, _b), 135, "$b$")):
        _ax.plot(*_p, "o", color="black", ms=4, zorder=6)
        beside(_ax, _p, _angle, _name, "black", 22 if "-" in _name else 10, 14, gap=3)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \iint_D 1 \, dxdy = \ ?
    $$

    <span class="chain">$\displaystyle = \int_{-a}^a \left( \int_{-b\sqrt{1 - x^2/a^2}}^{b\sqrt{1 - x^2/a^2}} 1 \, dy \right) dx$ $\displaystyle = \int_{-a}^a 2b \sqrt{1 - x^2/a^2} \, dx = \ldots \ \text{trigonometric substitution}$ $\displaystyle = \iint_D \bigg( \underbrace{\frac{\partial Q}{\partial x}(x, y) - \frac{\partial P}{\partial y}(x, y)}_{\footnotesize \begin{matrix} = 1 \text{ for some } \vec{F} = \begin{bmatrix} P \\ Q \end{bmatrix} \\ \leadsto \ \text{might make life easier} \end{matrix}} \bigg) dxdy$</span>

    Consider $\vec{F}(x, y) = \dfrac{1}{2} \begin{bmatrix} -y \\ x \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y} = \dfrac{1}{2}(1 + 1) = 1$

    <span class="chain">$\displaystyle \Longrightarrow \quad \iint_D 1 \, dxdy = \underbrace{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}_{\mathclap{\footnotesize \gamma(t) = \begin{bmatrix} a \cos(t) \\ b \sin(t) \end{bmatrix}, \ t \in [0, 2\pi]}}$ $\displaystyle = \int_0^{2\pi} \frac{1}{2} \begin{bmatrix} -b \sin(t) \\ a \cos(t) \end{bmatrix} \cdot \begin{bmatrix} -a \sin(t) \\ b \cos(t) \end{bmatrix} dt$ $\displaystyle = \frac{1}{2} \int_0^{2\pi} ab \, dt = ab\pi$</span>

    $\leadsto$ &nbsp; if $a = b = r$ &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle \iint_D dxdy = r^2 \pi$

    $\leadsto$ &nbsp; consequence for gradient vector fields
    """)
    return


@app.cell(hide_code=True)
def _(corollary):
    corollary(
        r"""
    Given a vector field $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$ $C^1$-smooth over the whole plane $\mathbb{R}^2$ and with zero scalar curl

    $$
    \frac{\partial Q}{\partial x}(x, y) - \frac{\partial P}{\partial y}(x, y) = 0
    $$

    then $\vec{F}(x, y)$ is a conservative vector field with potential function

    $$
    f(x, y) = \int_0^x P(t, 0) \, dt + \int_0^y Q(x, t) \, dt
    $$
    """,
        "Vector fields with zero scalar curl",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof.** Consider a rectangle $R = [0, x] \times [0, y]$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, along, beside, mo, np, plane):
    # the rectangle R = [0, x] x [0, y] of the proof (p. 7) and its boundary: C_1 (red) from (0, 0) along the bottom side to
    # (x, 0) and up the right side to (x, y); C_2 (orange) from (x, y) along the top side to (0, y) and down the left side
    # to (0, 0)
    _x, _y = 2.7, 1.7
    _fig, _ax = plane((-1.1, 4.2), (-0.8, 2.9), 4.2)
    _ax.fill([0, _x, _x, 0], [0, 0, _y, _y], color=LIGHT, lw=0, zorder=0)
    _u = np.linspace(0, 1, 60)
    for _p, _q, _c in (((0, 0), (_x, 0), RED), ((_x, 0), (_x, _y), RED), ((_x, _y), (0, _y), ORANGE), ((0, _y), (0, 0), ORANGE)):
        _ax.plot([_p[0], _q[0]], [_p[1], _q[1]], color=_c, lw=1.8, zorder=4)
        along(_ax, _p[0] + (_q[0] - _p[0]) * _u, _p[1] + (_q[1] - _p[1]) * _u, _c, at=(0.6,))
    for _p, _angle, _name, _w in (((0, 0), -135, "$(0, 0)$", 36), ((_x, 0), -90, "$(x, 0)$", 36), ((_x, _y), 45, "$(x, y)$", 36), ((0, _y), 180, "$(0, y)$", 36)):
        _ax.plot(*_p, "o", color="black", ms=4, zorder=6)
        beside(_ax, _p, _angle, _name, "black", _w, 16, gap=11 if _angle == -135 else 4)
    _ax.text(_x / 2, _y / 2, "$R$", color=BLUE, fontsize=13, ha="center", va="center", zorder=1)
    beside(_ax, (_x, _y / 2), 0, r"$\vec{C}_1$", RED, 16, 18, gap=6)
    beside(_ax, (_x / 2, _y), 90, r"$\vec{C}_2$", ORANGE, 16, 18, gap=6)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \text{Green} \quad \Longrightarrow \quad \underbrace{\int_{\vec{C}} \vec{F} \cdot d\vec{s}}_{\mathclap{\footnotesize \vec{C} = \mathrm{Bd}(R) = \vec{C}_1 \cup \vec{C}_2}} = \iint_R \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy$ $\displaystyle = 0 = \int_{\vec{C}_1} \vec{F} \cdot d\vec{s} + \int_{\vec{C}_2} \vec{F} \cdot d\vec{s}$</span>

    <span class="chain">$\displaystyle \int_{\vec{C}_1} \vec{F} \cdot d\vec{s} = \int_0^x \begin{bmatrix} P(t, 0) \\ Q(t, 0) \end{bmatrix} \cdot \begin{bmatrix} 1 \\ 0 \end{bmatrix} dt + \int_0^y \begin{bmatrix} P(x, t) \\ Q(x, t) \end{bmatrix} \cdot \begin{bmatrix} 0 \\ 1 \end{bmatrix} dt$ $\displaystyle = \int_0^x P(t, 0) \, dt + \int_0^y Q(x, t) \, dt = f(x, y)$</span>

    <span class="chain">$\displaystyle \int_{\vec{C}_2} \vec{F} \cdot d\vec{s} = - \int_0^y \begin{bmatrix} P(0, t) \\ Q(0, t) \end{bmatrix} \cdot \begin{bmatrix} 0 \\ 1 \end{bmatrix} dt - \int_0^x \begin{bmatrix} P(t, y) \\ Q(t, y) \end{bmatrix} \cdot \begin{bmatrix} 1 \\ 0 \end{bmatrix} dt$ $\displaystyle = - \int_0^y Q(0, t) \, dt - \int_0^x P(t, y) \, dt = - f(x, y)$</span>

    $$
    \leadsto \quad \text{FTC:} \quad \frac{\partial}{\partial x} f(x, y) = P(x, y) \quad \text{and} \quad \frac{\partial}{\partial y} f(x, y) = Q(x, y) \tag*{$\square$}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.**

    $$
    \vec{F}(x, y) = \underbrace{\begin{bmatrix} 2xy \\ x^2 + 3y^2 \end{bmatrix}}_{\mathclap{\footnotesize C^1\text{-smooth everywhere}}} \quad \leadsto \quad \frac{\partial Q}{\partial x}(x, y) - \frac{\partial P}{\partial y}(x, y) = 2x - 2x = 0
    $$

    $\Longrightarrow$ &nbsp; $\vec{F}(x, y) = \vec{\nabla} f(x, y)$ for

    <span class="chain">$\displaystyle f(x, y) = \int_0^x P(t, 0) \, dt + \int_0^y Q(x, t) \, dt$ $\displaystyle = \int_0^x 2t \cdot 0 \, dt + \int_0^y (x^2 + 3t^2) \, dt = x^2 y + y^3$</span>

    <span class="chain">$\displaystyle \text{or} \quad = \int_0^y Q(0, t) \, dt + \int_0^x P(t, y) \, dt$ $\displaystyle = \int_0^y (0 + 3t^2) \, dt + \int_0^x 2ty \, dt = y^3 + x^2 y$</span>

    **Remark.**

    $$
    \vec{H}(x, y) = \underbrace{\frac{1}{x^2 + y^2}}_{\mathclap{\footnotesize \text{not } C^1\text{-smooth at } (0, 0)}} \begin{bmatrix} -y \\ x \end{bmatrix}
    $$

    has zero scalar curl but is not a gradient!

    $\Longrightarrow$ &nbsp; Green's theorem does not apply
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ① &nbsp; $D$ is the triangle with corners $(0, 0)$, $(2, 0)$, $(1, 1)$

    a) &nbsp; Parameterize $\mathrm{Bd}(D)$ with positive orientation.

    b) &nbsp; Compute the line integral of $\vec{F}(x, y) = \begin{bmatrix} y^2 \\ 3xy \end{bmatrix}$ over $\mathrm{Bd}(D)$.

    c) &nbsp; Compute $\displaystyle \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy$ with Fubini's theorem.

    ② &nbsp; Let $\vec{G}(x, y) = \begin{bmatrix} e^y \\ x e^y + 2y \end{bmatrix}$

    a) &nbsp; Check that the scalar curl is zero.

    b) &nbsp; Compute a potential function for $\vec{G}(x, y)$.
    """)
    return


if __name__ == "__main__":
    app.run()
