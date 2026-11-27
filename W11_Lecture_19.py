import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 19 · Integration along paths", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(19, "Integration along paths")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: 2D sketches (bare axes, names beside points), the curve of the two sketches of a path,
    # and the helix of the examples

    def drawing(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges."""
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
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8)
        u = per_pt(ax)
        cx, cy = at[0] + d * c * u, at[1] + d * s * u
        return (cx - (w / 2 + 3) * u, cy - (h / 2 + 3) * u, cx + (w / 2 + 3) * u, cy + (h / 2 + 3) * u)

    def per_pt(ax):
        """Data units per point on an axis that fills its figure, with equal aspect."""
        x0, x1 = ax.get_xlim()
        return (x1 - x0) / (ax.figure.get_figwidth() * 72)

    def hits(a, b, boxes):
        """Whether the segment from a to b touches one of the boxes (x0, y0, x1, y1): the field skips arrows under names."""
        for k in np.linspace(0, 1, 9):
            x, y = a[0] + k * (b[0] - a[0]), a[1] + k * (b[1] - a[1])
            if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in boxes):
                return True
        return False

    # the path of the two sketches: gamma(s) = (s, 0.9 sin(1.1 s) + 0.3 s), with C = gamma([a, b])
    A, B = 0.0, 4.8

    def path(s):
        s = np.asarray(s, float)
        return np.array([s, 0.9 * np.sin(1.1 * s) + 0.3 * s])

    def velocity(s):
        return np.array([1.0, 0.99 * math.cos(1.1 * s) + 0.3])

    def below(v):
        """The direction (degrees) of the normal on the lower side of the curve with velocity v."""
        return math.degrees(math.atan2(-v[0], v[1]))

    def curve_sketch():
        """The path: C = gamma([a, b]) (blue) from gamma(a) to gamma(b), the path before a and after b (grey); returns the
        boxes its names take."""
        fig, ax = drawing((-1.3, 6.3), (-1.2, 2.6), 4.6)
        ax.plot(*path(np.linspace(-0.8, A, 60)), color=lk.GREY, lw=1.4)
        ax.plot(*path(np.linspace(B, B + 0.7, 60)), color=lk.GREY, lw=1.4)
        ax.plot(*path(np.linspace(A, B, 400)), color=lk.BLUE, lw=1.8)
        for s in (A, B):
            ax.plot(*path(s), "o", color="black", ms=4.5, zorder=6)
        boxes = [beside(ax, path(A), 160, r"$\gamma(a)$", "black", 30, 16), beside(ax, path(B), 90, r"$\gamma(b)$", "black", 30, 16)]
        ax.text(4.1, -0.2, r"$C = \gamma([a, b])$", color=lk.BLUE, fontsize=13, ha="center", va="center")
        u = per_pt(ax)
        boxes.append((4.1 - 40 * u, -0.2 - 11 * u, 4.1 + 40 * u, -0.2 + 11 * u))
        return fig, ax, boxes

    def helix(t):
        t = np.asarray(t, float)
        return np.array([np.cos(t), np.sin(t), t])

    def helix_lines():
        """C = gamma([0, 2 pi]) (blue), the helix before 0 and after 2 pi (grey)."""
        s, e, c = np.linspace(-1.0, 0, 40), np.linspace(2 * np.pi, 2 * np.pi + 1.0, 40), np.linspace(0, 2 * np.pi, 300)
        return [(*helix(s), lk.GREY, 1.4), (*helix(e), lk.GREY, 1.4), (*helix(c), lk.BLUE, 1.8)]

    HELIX_AXES = [((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 1.8, 0), "y", 0), ((0, 0, 0), (0, 0, 7.6), "z", 90)]
    HELIX_BOX = ((-1.3, 1.3), (-1.3, 1.3), (-0.6, 9.0))
    # the fields along the helix: points on circles of radius 1.8 about the z-axis, eight per circle, at four heights (each
    # height turned by half a step against the one below, so that no arrow stands right behind another)
    FIELD_POINTS = [np.array([1.8 * math.cos((j + l / 2) * math.pi / 4), 1.8 * math.sin((j + l / 2) * math.pi / 4), 0.6 + 2.0 * l]) for l in range(4) for j in range(8)]
    FIELD_AXES = [((0, 0, 0), (2.6, 0, 0), "x", -150), ((0, 0, 0), (0, 2.6, 0), "y", 0), ((0, 0, 0), (0, 0, 7.6), "z", 90)]
    FIELD_BOX = ((-2.3, 2.3), (-2.3, 2.3), (-0.6, 9.0))
    return A, B, FIELD_AXES, FIELD_BOX, FIELD_POINTS, HELIX_AXES, HELIX_BOX, below, beside, curve_sketch, drawing, helix, helix_lines, hits, per_pt, path, velocity


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    ta = lk.slider(0.3, 3.6, step=0.02, value=0.6, label="$t$")
    th = lk.slider(0.1, 1.6, step=0.02, value=1.3, label="$h$")
    tl = lk.slider(0.3, 4.2, step=0.02, value=1.2, label="$t$")
    tf = lk.slider(0, 6.28, step=0.04, value=1.0, label="$t$")
    tg = lk.slider(0, 6.28, step=0.04, value=1.0, label="$t$")
    return ta, tf, tg, th, tl


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Vector fields, divergence and curl

        $\leadsto$ &nbsp; when are vector fields gradients?

        $\leadsto$ &nbsp; when are vector fields curls?
        """,
        lk.gap(),
        r"""
        If <span class="lk-tab" style="--lk-tab: 6.2em">$\vec{\nabla} \times \vec{F} \neq \vec{0}$</span>$\Longrightarrow$ &nbsp; $\vec{F} \neq \vec{\nabla} f$

        <span class="lk-ghost">If </span><span class="lk-tab" style="--lk-tab: 6.2em">$\vec{\nabla} \cdot \vec{F} \neq 0$</span>$\Longrightarrow$ &nbsp; $\vec{F} \neq \vec{\nabla} \times \vec{G}$

        > $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 6.2em">$\vec{\nabla} \times \vec{F} = \vec{0}$</span>is necessary for $\vec{F} = \vec{\nabla} f$

        > <span class="lk-ghost">$\leadsto$ &nbsp; </span><span class="lk-tab" style="--lk-tab: 6.2em">$\vec{\nabla} \cdot \vec{F} = 0$</span>is necessary for $\vec{F} = \vec{\nabla} \times \vec{G}$
        """,
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.aside(
            r"Is $\vec{\nabla} \times \vec{F} = \vec{0}$ <span class='lk-mark'>sufficient</span> for $\vec{F} = \vec{\nabla} f$? (spoilers: No…)",
            r"does $\vec{\nabla} \times \vec{F} = \vec{0}$ imply $\vec{F} = \vec{\nabla} f$?",
        ),
        r"> $\leadsto$ &nbsp; integration along paths",
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 4.2, 7.1, 7.2")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: path integrals
    # section
    lk.section("Integration along paths")
    return


@app.cell(hide_code=True)
def _(below, beside, curve_sketch, lk, math, path, ta, th, velocity):
    # module: path integrals
    # definition: arc length
    # the curve C = gamma([a, b]); at gamma(t) its velocity gamma'(t) (green, at its true length) and the vector from
    # gamma(t) to gamma(t + h) (orange); t and h move with the sliders
    _t, _h = round(ta.value, 10), round(th.value, 10)
    _fig, _ax, _names = curve_sketch()
    _p, _q, _v = path(_t), path(_t + _h), velocity(_t)
    lk.arrow(_ax, _p, _q, lk.ORANGE, lw=1.6)
    lk.arrow(_ax, _p, _p + _v, lk.GREEN, lw=1.6)
    _ax.plot(*_p, "o", color="black", ms=4.5, zorder=6)
    _ax.plot(*_q, "o", color=lk.ORANGE, ms=4.5, zorder=6)
    beside(_ax, _p, below(_v), r"$\gamma(t)$", "black", 30, 16)
    beside(_ax, _q, math.degrees(math.atan2(*(_q - _p)[::-1])), r"$\gamma(t + h)$", lk.ORANGE, 48, 16)
    beside(_ax, _p + _v, math.degrees(math.atan2(_v[1], _v[0])), r"$\gamma'(t)$", lk.GREEN, 34, 16, gap=2)
    lk.module(
        lk.definition(
            [
                r"Given a differentiable path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$",
                lk.aside(r"the **arc length** of the curve $\mk{C = \gamma([a, b])}$", r"assuming $[a, b] \subseteq I$"),
                r"""
                $$
                L(C) = L(\gamma([a, b])) = \int_a^b \underbrace{\lVert \gamma'(t) \rVert}_{\footnotesize \text{speed of } \gamma \text{ at } t} \, dt,
                $$
                """,
                lk.gap(),
                lk.aside(
                    r"$$\mk{\gamma'(t)} = \lim_{h \to 0} \frac{\gamma(t + h) - \gamma(t)}{h} \quad \Longrightarrow \quad \lVert \gamma(t + h) - \gamma(t) \rVert \approx \lVert \gamma'(t) \rVert \, h.$$",
                    r"$\gamma'(t)$ = velocity of $\gamma$ at $t$",
                ),
            ],
            label="def-arc-length",
        ),
        lk.prose(lk.interactive(_fig, controls=[ta, th])),
    )
    return


@app.cell(hide_code=True)
def _(HELIX_AXES, HELIX_BOX, helix_lines, lk, np):
    # module: path integrals
    # example: arc length of the helix
    # the helix gamma(t) = (cos(t), sin(t), t); C = gamma([0, 2 pi]) (blue) from gamma(0) to gamma(2 pi); heights at
    # half scale so that the helix shows its turn
    _fig = lk.turntable(
        30,
        20,
        "the helix gamma(t) = (cos(t), sin(t), t), with the curve C = gamma([0, 2 pi]) from gamma(0) to gamma(2 pi)",
        [
            lk.panel(
                0.5,
                lines=helix_lines(),
                points=[((1, 0, 0), "#000000"), ((1, 0, 2 * np.pi), "#000000")],
                axes=HELIX_AXES,
                texts=[((1, 0, 0), r"\gamma(0)", "#000000", -60, 8), ((1, 0, 2 * np.pi), r"\gamma(2\pi)", "#000000", -30, 10), ((0, 1, np.pi / 2), r"C = \gamma([0, 2\pi])", lk.BLUE, 0, 10)],
                box=HELIX_BOX,
            )
        ],
        height=lk.H3D,
    )
    lk.example(
        [
            r"""
            $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; $\gamma'(t) = \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix}$

            $$
            \begin{aligned}
            L(\gamma([0, 2\pi])) &= \int_0^{2\pi} \left( (\sin(t))^2 + (\cos(t))^2 + 1 \right)^{\frac{1}{2}} dt\\
            &= \int_0^{2\pi} \sqrt{2} \, dt = 2\pi\sqrt{2}
            \end{aligned}
            $$
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: path integrals
    # definition: path integral
    lk.definition(
        r"""
        Given a differentiable path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ and a continuous function $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$

        the **path integral** of $f$ over $C = \gamma([a, b]) \subseteq D$ (along the path $\gamma$) is

        $$
        \int_C f \, ds = \int_a^b \underbrace{f(\gamma(t)) \lVert \gamma'(t) \rVert}_{\footnotesize \begin{array}{c} f \text{ calculated along } \gamma \\ \text{times the speed of } \gamma \end{array}} \, dt.
        $$
        """,
        label="def-path-integral",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: path integrals
    # example: path integral over the helix
    lk.example(
        r"""
        $f(x, y, z) = z$, &nbsp; $C = \gamma([0, 2\pi])$, &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$

        > $\displaystyle \int_C f \, ds = \int_0^{2\pi} t \sqrt{2} \, dt = \frac{(2\pi)^2}{2} \sqrt{2}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reparameterization
    # prose: why the speed
    lk.prose(
        r"Why do we multiply by the speed of $\gamma$?",
        lk.aside(
            r"> $\leadsto$ &nbsp; because we want these integrals to only depend on the function $f$ and on the curve $C = \gamma([a, b])$,<br>but not on the <span class='lk-mark'>choice of parameterization</span> of $C$",
            r"the specific path $\gamma$<br>with $\gamma([a, b]) = C$",
            at="last",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reparameterization
    # example: the helix twice as fast
    lk.example(
        [
            r"""
            $f(x, y, z) = z$, &nbsp; $\sigma(t) = \begin{bmatrix} \cos(2t) \\ \sin(2t) \\ 2t \end{bmatrix}$

            > $\Longrightarrow$ &nbsp; $\sigma([0, \pi]) = \gamma([0, 2\pi]) = C$
            """,
            lk.aside(
                r"> <span class='lk-ghost'>$\Longrightarrow$ &nbsp;</span>with $\lVert \sigma'(t) \rVert = 2\sqrt{2} = 2 \lVert \gamma'(t) \rVert$",
                r"$\sigma$ travels across the same $C$<br>with twice the speed of $\gamma$",
            ),
            r"""
            $$
            \begin{aligned}
            L(C) &= \underbrace{\int_0^{2\pi} \lVert \gamma'(t) \rVert \, dt = \int_0^{\pi} \lVert \sigma'(\tilde{t}) \rVert \, d\tilde{t}}_{\footnotesize \begin{array}{c} \text{length should be independent} \\ \text{of the way we travel across } C \end{array}} = \int_C (1) \, ds\\[5.6em]
            \int_C z \, ds &= \underbrace{\int_0^{2\pi} t \lVert \gamma'(t) \rVert \, dt \quad \mathrel{\overset{\mathclap{\footnotesize \begin{array}{c} \text{integration by} \\ \text{substitution} \\[-2pt] \downarrow \end{array}}}{=}} \quad \int_0^{\pi} 2\tilde{t} \lVert \sigma'(\tilde{t}) \rVert \, d\tilde{t}}_{\footnotesize \begin{array}{c} \text{integral of } f \text{ over } C \\ \text{should also be independent!} \end{array}}
            \end{aligned}
            $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reparameterization
    # definition: reparameterization
    lk.definition(
        r"""
        A **reparameterization** of a path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ is another path $\sigma = \gamma \circ \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$<br>obtained by a change of variables

        $$
        \begin{aligned}
        &\varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow I \subseteq \mathbb{R}, \qquad \tilde{t} \longmapsto t = \varphi(\tilde{t}), \qquad \varphi'(\tilde{t}) \neq 0\\[6pt]
        &\Longrightarrow\quad \gamma(t) = \gamma(\varphi(\tilde{t})) = \sigma(\tilde{t})\ \Longrightarrow\ \mathrm{Im}(\gamma) = \mathrm{Im}(\sigma).
        \end{aligned}
        $$
        """,
        label="def-reparameterization",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reparameterization
    # theorem: path integrals and reparameterization
    lk.theorem(
        r"""
        Given $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ differentiable path

        $\sigma = \gamma \circ \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ a reparameterization with

        $\varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow I \subseteq \mathbb{R}$ differentiable change of variables

        Then for any continuous function $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$

        $$
        \int_c^d f(\sigma(\tilde{t})) \lVert \sigma'(\tilde{t}) \rVert \, d\tilde{t} \ \mathrel{\underset{\mathclap{\footnotesize \begin{array}{c} \uparrow \\[-2pt] \text{substitution of} \\ \text{variables } t = \varphi(\tilde{t}) \end{array}}}{=}} \ \int_a^b f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt,
        $$

        where $[a, b] = \varphi([c, d])$.
        """,
        label="thm-path-reparameterization",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reparameterization
    # consequence: path integrals only depend on C
    lk.prose(r"$\Longrightarrow$ &nbsp; $\displaystyle \int_C f \, ds$ is independent of the choice of path $\gamma$ parameterizing $C$")
    return


@app.cell(hide_code=True)
def _(A, B, beside, curve_sketch, hits, lk, math, np, path, tl, velocity):
    # module: line integrals
    # definition: line integral
    # the curve C = gamma([a, b]) from gamma(a) to gamma(b) (the curve of the arc-length sketch); at gamma(t) its velocity
    # gamma'(t) (green) and the vector F(gamma(t)) of a vector field (red), both at their true length; the field drawn faint
    # on a regular grid over the sketch; t moves with the slider
    _t = round(tl.value, 10)
    _fig, _ax, _names = curve_sketch()

    def _F(p):
        return 0.14 * np.array([3.4 - p[1], p[0] - 2.4])

    _p, _v = path(_t), velocity(_t)
    _f = _F(_p)
    _names += [
        beside(_ax, _p, math.degrees(math.atan2(-(_v + _f)[1], -(_v + _f)[0])), r"$\gamma(t)$", "black", 30, 16),
        beside(_ax, _p + _v, math.degrees(math.atan2(_v[1], _v[0])), r"$\gamma'(t)$", lk.GREEN, 34, 16, gap=2),
        beside(_ax, _p + _f, math.degrees(math.atan2(_f[1], _f[0])), r"$\vec{F}(\gamma(t))$", lk.RED, 52, 18, gap=2),
    ]
    # the field on a regular grid over the whole sketch, faint, below the curve; no arrow under a name
    for _x in np.arange(-1.0, 6.01, 0.7):
        for _y in np.arange(-0.9, 2.31, 0.64):
            _g = np.array([_x, _y])
            if hits(_g, _g + _F(_g), _names):
                continue
            _ax.annotate("", xy=_g + _F(_g), xytext=_g, zorder=1, arrowprops={"arrowstyle": "->,head_length=0.35,head_width=0.22", "mutation_scale": 11, "color": lk.RED, "lw": 0.9, "alpha": 0.35, "shrinkA": 0, "shrinkB": 0})
    lk.arrow(_ax, _p, _p + _f, lk.RED, lw=1.6)
    lk.arrow(_ax, _p, _p + _v, lk.GREEN, lw=1.6)
    _ax.plot(*_p, "o", color="black", ms=4.5, zorder=6)
    lk.module(
        lk.definition(
            [
                r"""
                Given a differentiable path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ and a continuous vector field $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$
                """,
                r"the **line integral** of $\vec{F}$ over $C = \gamma([a, b]) \subseteq D$",
                lk.aside(r"<span class='lk-mark'>from $\gamma(a)$ to $\gamma(b)$</span> (along the path $\gamma$) is", r"orientation of $C$"),
                lk.aside(r"$$\int_{\mk{\vec{C}}} \vec{F} \cdot d\vec{s} = \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt.$$", "oriented curve"),
            ],
            label="def-line-integral",
        ),
        lk.prose(lk.interactive(_fig, controls=[tl])),
    )
    return


@app.cell(hide_code=True)
def _(FIELD_AXES, FIELD_BOX, FIELD_POINTS, helix, helix_lines, lk, np, tf):
    # module: line integrals
    # scene (no visible output; the example below shows it)
    # F(x) = (-y, x, 1) around the helix (red): on circles of radius 1.8 about the z-axis at four heights, and at gamma(t)
    # (moving with the slider) the field F(gamma(t)) = gamma'(t) (green); every arrow at 0.5 of its vector
    _t, _K = float(tf.value), 0.5

    def _F(p):
        return np.array([-p[1], p[0], 1.0])

    _p = helix(_t)
    _arrows = [(q, q + _K * _F(q), lk.RED, 1.1) for q in FIELD_POINTS]
    _arrows += [(_p, _p + _K * _F(_p), lk.GREEN, 2.2)]
    lk.turntable(
        30,
        20,
        "the vector field F = (-y, x, 1) along the helix, with gamma(t) and gamma'(t) = F(gamma(t))",
        [
            lk.panel(
                0.5,
                lines=helix_lines(),
                points=[(tuple(_p), "#000000")],
                arrows=_arrows,
                axes=FIELD_AXES,
                caption=r"\textcolor{#a8554c}{\vec{F}} \qquad \gamma(t) \qquad \textcolor{#4f7f5c}{\gamma'(t) = \vec{F}(\gamma(t))}",
                box=FIELD_BOX,
            )
        ],
        height=lk.H3D,
        key="L19-F",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, tf):
    # module: line integrals
    # example: F along the helix
    lk.example(
        [
            r"""
            $\vec{F}(x, y, z) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$, &nbsp; $\vec{C} = \gamma([0, 2\pi])$ from $\gamma(0)$ to $\gamma(2\pi)$, &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$

            > $\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_0^{2\pi} \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix} dt = \int_0^{2\pi} 2 \, dt = 4\pi$
            """,
            lk.interactive(lk.frame("L19-F", lk.H3D), controls=[tf]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(FIELD_AXES, FIELD_BOX, FIELD_POINTS, helix, helix_lines, lk, np, tg):
    # module: line integrals
    # scene (no visible output; the example below shows it)
    # G(x) = (x, y, z) around the helix (red): at the same points as F, and at gamma(t) (moving with the slider)
    # gamma'(t) (green) and G(gamma(t)) (red); every arrow at 0.3 of its vector
    _t, _K = float(tg.value), 0.3

    def _G(p):
        return np.asarray(p, float)

    _p, _v = helix(_t), np.array([-np.sin(_t), np.cos(_t), 1.0])
    _arrows = [(q, q + _K * _G(q), lk.RED, 1.0) for q in FIELD_POINTS]
    _arrows += [(_p, _p + _K * _G(_p), lk.RED, 2.2), (_p, _p + _K * _v, lk.GREEN, 2.2)]
    lk.turntable(
        30,
        20,
        "the vector field G = (x, y, z) along the helix, with gamma(t), gamma'(t) and G(gamma(t))",
        [
            lk.panel(
                0.5,
                lines=helix_lines(),
                points=[(tuple(_p), "#000000")],
                arrows=_arrows,
                axes=FIELD_AXES,
                caption=r"\gamma(t) \qquad \textcolor{#4f7f5c}{\gamma'(t)} \qquad \textcolor{#a8554c}{\vec{G}(\gamma(t))}",
                box=FIELD_BOX,
            )
        ],
        height=lk.H3D,
        key="L19-G",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, tg):
    # module: line integrals
    # example: G along the helix
    lk.example(
        [
            r"""
            $\vec{G}(x, y, z) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$

            > $\displaystyle \int_{\vec{C}} \vec{G} \cdot d\vec{s} = \int_0^{2\pi} \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix} dt = \int_0^{2\pi} t \, dt = \frac{(2\pi)^2}{2}$
            """,
            lk.interactive(lk.frame("L19-G", lk.H3D), controls=[tg]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: line integrals
    # theorem: line integrals and reparameterization
    lk.theorem(
        r"""
        Given $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$, &nbsp; $\sigma = \gamma \circ \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$

        $$
        \int_c^d \vec{F}(\sigma(\tilde{t})) \cdot \sigma'(\tilde{t}) \, d\tilde{t} = \pm \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt,
        $$

        $$
        \text{with} \quad \begin{cases} +, & \text{if } \varphi'(\tilde{t}) > 0, \\ -, & \text{if } \varphi'(\tilde{t}) < 0 \end{cases}, \qquad \text{where } [a, b] = \varphi([c, d]).
        $$
        """,
        label="thm-line-reparameterization",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: line integrals
    # consequence: line integrals only depend on C and its orientation
    lk.prose(r"$\Longrightarrow$ &nbsp; $\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s}$ only depends on $C$ and a choice of orientation of $C$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient fields
    # theorem: line integrals of gradients
    lk.theorem(
        r"""
        Given $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ $C^1$-smooth and $\vec{C} = \gamma([a, b]) \subset D$ from $\gamma(a)$ to $\gamma(b)$, then

        $$
        \int_{\vec{C}} \vec{\nabla} f \cdot d\vec{s} = f(\gamma(b)) - f(\gamma(a)).
        $$
        """,
        label="thm-gradient",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient fields
    # consequence: only the end points
    lk.prose(r"$\leadsto$ &nbsp; line integrals of gradient vector fields only depend on their end points!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient fields
    # proof
    # the two lines share their "=" (same widths); both in one aside, so that "chain rule" sits right between them (the
    # chain rule takes line 1 to line 2) and "FTC!" level with the last line
    lk.proof(
        [
            lk.aside(
                r"""
                $$\int_{\vec{C}} \vec{\nabla} f \cdot d\vec{s} = \mathrlap{\int_a^b \vec{\nabla} f(\gamma(t)) \cdot \gamma'(t) \, dt}\hphantom{\int_a^b \frac{d}{dt} \big( f(\gamma(t)) \big) \, dt = f(\gamma(b)) - f(\gamma(a)) \qquad \square}$$

                $$\hphantom{\int_{\vec{C}} \vec{\nabla} f \cdot d\vec{s}} = \int_a^b \frac{d}{dt} \big( f(\gamma(t)) \big) \, dt = f(\gamma(b)) - f(\gamma(a)) \qquad \square$$
                """,
                [(1.5, "chain rule"), (2, "FTC!")],
                rows=2,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient fields
    # example: G is a gradient
    lk.example(
        r"""
        $\displaystyle \vec{G}(x, y, z) = \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \vec{\nabla} g(x, y, z)$, &nbsp; $\displaystyle g(x, y, z) = \frac{1}{2} (x^2 + y^2 + z^2)$

        $$
        \begin{aligned}
        \Longrightarrow \quad \int_{\vec{C}} \vec{G} \cdot d\vec{s} &= g(\gamma(2\pi)) - g(\gamma(0))\\
        &= \frac{1}{2} \left( 1 + (2\pi)^2 \right) - \frac{1}{2} (1 + 0) = \frac{(2\pi)^2}{2}.
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # prose: the question again
    lk.prose(r"$\leadsto$ &nbsp; does $\vec{\nabla} \times \vec{F} = \vec{0}$ imply $\vec{F} = \vec{\nabla} f$?")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: conservative fields
    # example: H
    # H, the same on every horizontal plane, at three heights, with the unit circle C (blue) in the plane z = 0. Every arrow
    # at 0.8 of its vector, so of length 0.8 / r at the distance r from the z-axis: red on three rings at each height, strong at
    # eight points of C. The z-axis, not in the domain of H, is dashed, as long as the other axes, with an open dot at the origin
    _K = 0.8

    def _H(p):
        return np.array([-p[1], p[0], 0.0]) / (p[0] ** 2 + p[1] ** 2)

    def _ring(r, n, turn, z=0.0):
        return [np.array([r * np.cos(a), r * np.sin(a), z]) for a in turn + np.linspace(0, 2 * np.pi, n, endpoint=False)]

    _c = np.linspace(0, 2 * np.pi, 300)
    _arrows = [(q, q + _K * _H(q), lk.RED, 1.0) for z in (-1.2, 0.0, 1.2) for q in _ring(1.5, 12, np.pi / 12, z) + _ring(2.0, 16, np.pi / 16, z)]
    _arrows += [(q, q + _K * _H(q), lk.RED, 1.0) for z in (-1.2, 1.2) for q in _ring(1.0, 8, np.radians(7), z)]
    _arrows += [(q, q + _K * _H(q), lk.RED, 1.8) for q in _ring(1.0, 8, np.radians(7))]
    _arrows += [((0, 0, -2.3), (0, 0, 2.3), "#000000", 1.2, [5, 4])]
    _fig = lk.turntable(
        35,
        22,
        "the vector field H on three horizontal planes around the z-axis, with the unit circle C in the plane z = 0",
        [
            lk.panel(
                1.0,
                lines=[(np.cos(_c), np.sin(_c), 0 * _c, lk.BLUE, 1.8)],
                axes=[((-2.3, 0, 0), (2.3, 0, 0), "x", -150), ((0, -2.3, 0), (0, 2.3, 0), "y", 0)],
                arrows=_arrows,
                points=[((0, 0, 0), "#000000", 3.5, True)],
                texts=[((0, 0, 2.3), "z", "#000000", 90, 5), ((np.cos(0.4), np.sin(0.4), 0), r"\vec{C}", lk.BLUE, -60, 12)],
                box=((-2.0, 2.0), (-2.0, 2.0), (-2.0, 2.0)),
            )
        ],
        height=lk.H3D,
    )
    lk.example(
        [
            r"""
            $\displaystyle \vec{H}(\vec{x}) = \frac{1}{x^2 + y^2} \begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}$, &nbsp; $x^2 + y^2 \neq 0$

            > $\vec{\nabla} \times \vec{H} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\[2pt] {\large\tfrac{-y}{x^2 + y^2}} & {\large\tfrac{x}{x^2 + y^2}} & 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\[2pt] {\large\tfrac{-x^2 + y^2}{(x^2 + y^2)^2}} - {\large\tfrac{y^2 - x^2}{(x^2 + y^2)^2}} \end{bmatrix} = \vec{0}$

            $\vec{C}$ = unit circle in the $xy$-plane, oriented counter-clockwise

            > $\leadsto$ &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ 0 \end{bmatrix}$ &nbsp; from $t = 0$ to $t = 2\pi$

            $$
            \begin{aligned}
            \Longrightarrow \quad \int_{\vec{C}} \vec{H} \cdot d\vec{s} &= \int_0^{2\pi} \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 0 \end{bmatrix} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 0 \end{bmatrix} dt\\
            &= \int_0^{2\pi} dt = 2\pi \neq \underbrace{h(\gamma(2\pi)) - h(\gamma(0))}_{\footnotesize = 0 \ \forall \, h}
            \end{aligned}
            $$

            $\Longrightarrow$ &nbsp; $\vec{H} \neq \vec{\nabla} h$, although $\vec{\nabla} \times \vec{H} = \vec{0}$
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # theorem: gradients and end points
    lk.theorem(
        r"""
        $\vec{F} = \vec{\nabla} f$ if and only if $\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s}$ only depends on the end points of $\vec{C}$

        for every oriented curve $\vec{C} \subset D = \mathrm{Dom}(\vec{F})$
        """,
        label="thm-conservative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservative fields
    # consequence: name
    lk.prose(r"$\leadsto$ &nbsp; $\vec{F}$ is called a **conservative vector field**")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # section
    lk.section("Practice")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: arc length and path integral
    lk.exercise(
        r"""
        $$
        \gamma(t) = \begin{bmatrix} 2t \\ t^2 \\ \ln(t) \end{bmatrix}, \qquad t \in [1, e]
        $$

        a) Compute arc length

        b) Compute the path integral of $f(x, y, z) = y$ along $\gamma$
        """,
        label="ex-arc-length",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: potential function and line integrals
    lk.exercise(
        r"""
        $$
        \vec{G}(x, y, z) = \begin{bmatrix} e^y \\ x e^y + z \\ y \end{bmatrix}
        $$

        a) Check that $g(x, y, z) = x e^y + yz$ is a potential function for $\vec{G}$

        b) Compute the line integral of $\vec{G}$ along

        $$
        \begin{aligned}
        &\bullet \ \ \sigma(t) = \begin{bmatrix} t \\ t \\ t \end{bmatrix}, &&t \in [0, 1]\\[6pt]
        &\bullet \ \ \rho(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}, &&t \in [0, 2\pi],
        \end{aligned}
        $$

        from the definition of line integrals.

        Hint: for (b), compute $\tfrac{d}{dt} \left( e^{\sin(t)} \cos(t) \right)$
        """,
        label="ex-potential",
    )
    return


if __name__ == "__main__":
    app.run()
