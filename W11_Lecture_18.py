import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 18 · Gradient vector fields and curl", css_file="lecturekit/style.css")


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
    lk.lecture(18, "Gradient vector fields and curl")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Helpers of this lecture: the flow lines of the two fields, and a horizontal disc (a circle and its fill) carried by a flow

    def F(p):
        """The field F(x) = (-y, x, 1) of the examples."""
        return np.array([-p[1], p[0], 1.0])

    def circle(c, r):
        """The horizontal circle of radius r about c, as three arrays."""
        a = np.linspace(0, 2 * np.pi, 121)
        return c[0] + r * np.cos(a), c[1] + r * np.sin(a), c[2] + 0 * a

    def disc(c, r):
        """The horizontal disc of radius r about c, filled."""
        rr, ss = np.meshgrid(np.linspace(0, r, 6), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        return lk.sheet(c[0] + rr * np.cos(ss), c[1] + rr * np.sin(ss), c[2] + 0 * rr, flat=lk.LIGHT, alpha=0.9)

    FAINT = "#c9a29c"  # the field where it is not the point of the figure: RED halfway to white
    return F, FAINT, circle, disc


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    th = lk.slider(0, 6.28, step=0.04, value=1.6, label="$t$")
    tg = lk.slider(-0.5, 0.9, step=0.02, value=0.6, label="$t$")
    tf = lk.slider(0, 3.14, step=0.02, value=1.2, label="$t$")
    return tf, tg, th


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$

        Flow lines $\gamma : (-\varepsilon, \varepsilon) \subseteq \mathbb{R} \longrightarrow \mathbb{R}^n$ such that $\gamma'(t) = \vec{F}(\gamma(t))$

        > $\gamma(t) = (x(t), y(t))$ &nbsp; such that &nbsp; $\begin{bmatrix} x'(t) \\ y'(t) \end{bmatrix} = \begin{bmatrix} P(x(t), y(t)) \\ Q(x(t), y(t)) \end{bmatrix}$

        Divergence $\vec{\nabla} \cdot \vec{F} : D \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$

        > $\displaystyle\vec{\nabla} \cdot \vec{F}(x, y) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix} = \frac{\partial P}{\partial x}(x, y) + \frac{\partial Q}{\partial y}(x, y)$
        """,
        title="Last time",
        topic=lk.aside(r"Vector fields $\vec{F} : D \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^n$", r"$n = 2$"),
    )
    return


@app.cell(hide_code=True)
def _(F, FAINT, lk, np, th):
    # module: recap
    # scene (no visible output; the example below shows it)
    # the field F(x) = (-y, x, 1) (faint: the figure is about the flow line), every arrow at 2/5 of its vector, at eight points on the circle of radius 3 about the
    # z-axis, at the heights 5/4, 17/4 and 29/4 (every other level turned by half a step, so that no arrows cross); the flow
    # line through gamma(0) = (2, 0, 0) is the helix gamma(t) = (2 cos(t), 2 sin(t), t) (blue), drawn past the slider's range
    # so that its name sits where the point never goes; gamma(t) moves with t and gamma'(t) = F(gamma(t)) is drawn from it
    # (green), at the scale of the field. Heights at true scale
    _k = 0.4
    _pts = [np.array([3.0 * np.cos(np.radians((_j + _l / 2) * 45)), 3.0 * np.sin(np.radians((_j + _l / 2) * 45)), 1.25 + 3 * _l]) for _l in range(3) for _j in range(8)]
    _s = np.linspace(0, 2 * np.pi + 1.4, 271)
    _t = float(th.value)
    _g = np.array([2 * np.cos(_t), 2 * np.sin(_t), _t])
    # the name of gamma(t) beside its point, on the outer side of the velocity as seen in the first view: along the screen
    # normal of the velocity, just far enough for its box to clear the dot; it turns with t and never jumps
    _az, _el, _ys = np.radians(30), np.radians(30), 1.0
    _r = np.array([-np.sin(_az), np.cos(_az), 0])
    _u = np.array([-np.sin(_el) * np.cos(_az), -np.sin(_el) * np.sin(_az), np.cos(_el) * _ys])
    _w = np.array([-np.sin(_el) * np.cos(_az), -np.sin(_el) * np.sin(_az), np.cos(_el) / _ys])
    _sv = np.array([_r @ F(_g), _u @ F(_g)])
    _n = np.array([_sv[1], -_sv[0]]) / np.hypot(*_sv)
    _d = (15 * abs(_n[0]) + 8 * abs(_n[1]) + 5) / 40
    _at = _g + _d * (_n[0] * _r + _n[1] * _w) + 0.2 * _w
    _end = (2 * np.cos(2 * np.pi + 1.4), 2 * np.sin(2 * np.pi + 1.4), 2 * np.pi + 1.4)
    lk.turntable(
        30,
        30,
        "the vector field F(x) = (-y, x, 1) around the z-axis, and its flow line through gamma(0) = (2, 0, 0), a helix moving up around the z-axis, with gamma(t) and gamma'(t) = F(gamma(t))",
        [
            lk.panel(
                1.0,
                lines=[(2 * np.cos(_s), 2 * np.sin(_s), _s, lk.BLUE, 1.8)],
                points=[((2, 0, 0), "#000000", 3.5), (tuple(_g), "#000000", 4.0)],
                axes=[((0, 0, 0), (4.0, 0, 0), "x", -150), ((0, 0, 0), (0, 4.0, 0), "y", 0), ((0, 0, 0), (0, 0, 9.0), "z", 90)],
                arrows=[(_p, _p + _k * F(_p), FAINT, 1.1) for _p in _pts] + [(_g, _g + _k * F(_g), lk.GREEN, 2.2)],
                texts=[(_end, r"\gamma", lk.BLUE, 0, 6), ((2, 0, 0), r"\gamma(0)", "#000000", 180, 7), (tuple(_at), r"\gamma(t)", "#000000", -90, 0)],
                caption=r"\gamma(t) \qquad \textcolor{#4f7f5c}{\gamma'(t) = \vec{F}(\gamma(t))}",
                box=((-3.4, 3.4), (-3.4, 3.4), (0, 9.2)),
            )
        ],
        height=lk.H3D,
        key="L18-helix",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(F, lk, np, th):
    # module: recap
    # example: a field spiraling upwards
    # the two parts of F side by side: the rotation vector field (-y, x, 0) and the constant vector field (0, 0, 1), at the
    # same points on circles of radius 3/2 and 3 at the heights 1/2, 5/2 and 9/2 (eight per circle; each height turned by
    # 15 degrees against the one below, the inner circle by 22.5, so that no arrow stands right behind another); every
    # arrow at 1/2 of its vector, so that the rotation visibly grows away from the axis. Below them, their sum F = (-y, x,
    # 1), drawn the same way at the same points
    _pts = [np.array([_r * np.cos(np.radians(45 * _j + 15 * _l + 22.5 * _i)), _r * np.sin(np.radians(45 * _j + 15 * _l + 22.5 * _i)), 0.5 + 2.0 * _l]) for _l in range(3) for _i, _r in enumerate((1.5, 3.0)) for _j in range(8)]
    _axes = [((0, 0, 0), (4.4, 0, 0), "x", -150), ((0, 0, 0), (0, 4.4, 0), "y", 0), ((0, 0, 0), (0, 0, 6.0), "z", 90)]
    _box = ((-3.2, 3.2), (-3.2, 3.2), (0.4, 5.0))

    def _panel(f, name):
        return lk.panel(1.0, axes=_axes, arrows=[(p, p + 0.5 * f(p), lk.RED, 1.3) for p in _pts], caption=name, box=_box)

    _parts = lk.turntable(
        30,
        30,
        "the rotation vector field (-y, x, 0) on xy-directions and the constant vector field (0, 0, 1) on z-direction, side by side",
        [
            _panel(lambda p: np.array([-p[1], p[0], 0.0]), r"\begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}"),
            _panel(lambda p: np.array([0.0, 0.0, 1.0]), r"\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}"),
        ],
        height=440,
        cols=2,
        key="L18-parts",
    )
    _whole = lk.turntable(
        30,
        30,
        "their sum, the vector field F = (-y, x, 1), at the same points",
        [_panel(F, r"\vec{F} = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}")],
        height=340,
        key="L18-whole",
    )
    lk.example(
        [
            lk.aside(r"$\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$", r"$n = 3$"),
            r"""
            > $\displaystyle\vec{F}(x, y, z) = \begin{bmatrix} P(x, y, z) \\ Q(x, y, z) \\ R(x, y, z) \end{bmatrix} = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix} = \overbrace{\begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}}^{\footnotesize \begin{array}{c} \text{rotation vector field} \\ \text{on } xy\text{-directions} \end{array}} + \underbrace{\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}}_{\footnotesize \begin{array}{c} \text{constant vector field} \\ \text{on } z\text{-direction} \end{array}}$

            > > $\Longrightarrow$ &nbsp; vector field spiraling upwards
            """,
            lk.figure(_parts),
            lk.figure(_whole),
            lk.gap(),
            r"""
            flow line = helix moving up around $z$-axis

            > $\gamma'(t) = \begin{bmatrix} x'(t) \\ y'(t) \\ z'(t) \end{bmatrix} = \vec{F}(\gamma(t)) = \begin{bmatrix} -y(t) \\ x(t) \\ 1 \end{bmatrix}$, &nbsp; $\gamma(0) = \begin{bmatrix} x_0 \\ y_0 \\ z_0 \end{bmatrix}$

            > > $\Longrightarrow$ &nbsp; $\gamma(t) = \begin{bmatrix} x_0 \cos(t) - y_0 \sin(t) \\ x_0 \sin(t) + y_0 \cos(t) \\ z_0 + t \end{bmatrix}$
            """,
            lk.aside(
                r"$\displaystyle\mathrm{div}(\vec{F})(\vec{x}) = (\vec{\nabla} \cdot \vec{F})(\vec{x}) = \frac{\partial}{\partial x}(-y) + \frac{\partial}{\partial y}(x) + \frac{\partial}{\partial z}(1) = 0$",
                r"flow does not expand/contract<br>volumes around $\vec{x}$",
            ),
            lk.interactive(lk.frame("L18-helix", lk.H3D), controls=[th]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        <span class="lk-tab" style="--lk-tab: 15.5em">Special type of vector fields</span>$\leadsto$ &nbsp; gradients

        <span class="lk-tab" style="--lk-tab: 15.5em">Another differential operation</span>$\leadsto$ &nbsp; in $\mathbb{R}^3$
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 4.3, 4.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient vector fields
    # section
    lk.section("Gradient vector fields and curl")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient vector fields
    # recall: gradient
    lk.recall(
        r"""
        Given $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ differentiable at $\vec{x} \in D$, we can define the gradient of $f$ at $\vec{x}$

        $$
        \vec{\nabla} f(\vec{x}) = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x}}(\vec{x}) \\[6pt] {\large\tfrac{\partial f}{\partial y}}(\vec{x}) \\[6pt] {\large\tfrac{\partial f}{\partial z}}(\vec{x}) \end{bmatrix}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient vector fields
    # consequence: the gradient is a vector field
    lk.prose(
            r"""
            If $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ is differentiable $\forall \, \vec{x} \in D$, then $\vec{\nabla} f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ is a vector field!
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; note that &nbsp; $\vec{\nabla} f(\vec{x}) = \mk{\begin{bmatrix} \partial / \partial x \\ \partial / \partial y \\ \partial / \partial z \end{bmatrix}} f(\vec{x})$",
                r"useful to think of $\vec{\nabla}$ as a vector of<br>partial derivatives for gradients as well!",
            ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradient vector fields
    # definition: gradient vector field
    lk.definition(
        r"""
        A vector field $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ is called a **gradient vector field**<br>if $\vec{F} = \vec{\nabla} f$ for some differentiable function $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$.

        $\leadsto$ &nbsp; $f$ is called a **potential function** for $\vec{F}$.
        """,
        label="def-gradient-field",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: gradient vector fields
    # example: radial fields
    # the radial vector field G(x) = x (every arrow at 1/2 of its vector) and the unit radial vector field H(x) = x/|x| (every
    # arrow at full length) at the same 20 points on two shells, so that G grows outward and H does not; side by side, one view
    # for both. The two shells: the 8 corners of [-1, 1]^3 and the 12 edge midpoints of [-5/2, 5/2]^3; the origin, where H is
    # not defined, as an open dot
    _pts = [np.array([a, b, c]) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)] + [np.array(q) for s in (-2.5, 2.5) for t in (-2.5, 2.5) for q in ((s, t, 0), (s, 0, t), (0, s, t))]
    _axes = [((-4.0, 0, 0), (4.0, 0, 0), "x", -147), ((0, -4.0, 0), (0, 4.0, 0), "y", 0), ((0, 0, -4.0), (0, 0, 4.0), "z", 90)]
    _box = ((-4.2, 4.2), (-4.2, 4.2), (-4.2, 4.2))
    _fig = lk.turntable(
        30,
        22,
        "the radial vector field G(x) = (x, y, z) and the unit radial vector field H(x) = x/|x| at 20 points on two shells, side by side",
        [
            lk.panel(1.0, axes=_axes, arrows=[(p, 1.5 * p, lk.RED, 1.4) for p in _pts], caption=r"\vec{G}", box=_box),
            lk.panel(1.0, axes=_axes, arrows=[(p, p + p / np.linalg.norm(p), lk.RED, 1.4) for p in _pts], points=[((0, 0, 0), "#000000", 3.5, True)], caption=r"\vec{H}", box=_box),
        ],
        height=lk.H3D,
        cols=2,
        key="L18-radial",
    )
    lk.example(
        [
            lk.aside(
                r"$\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$",
                r"radial vector field<br>is a gradient vector field",
            ),
            r"""
            > $\leadsto$ &nbsp; $\vec{G}(\vec{x}) = \vec{\nabla} g(\vec{x})$ for $g(\vec{x}) = \frac{1}{2}(x^2 + y^2 + z^2)$
            """,
            lk.aside(
                r"$\displaystyle\vec{H}(\vec{x}) = \underbrace{\frac{1}{\sqrt{x^2 + y^2 + z^2}}}_{\vec{x} \neq \vec{0}} \begin{bmatrix} x \\ y \\ z \end{bmatrix}$",
                r"unit radial vector field is also a<br>gradient vector field (for $\vec{x} \neq \vec{0}$)",
            ),
            r"""
            > $\leadsto$ &nbsp; $\vec{H}(\vec{x}) = \vec{\nabla} h(\vec{x})$ for $\underbrace{h(\vec{x}) = \sqrt{x^2 + y^2 + z^2}}_{\text{not differentiable at } \vec{x} = \vec{0}}$
            """,
            lk.figure(_fig),
            lk.gap(),
            r"""
            $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$ &nbsp; is not a gradient vector field!

            > $\leadsto$ &nbsp; there is no function $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ such that $\vec{\nabla} f = \vec{F}$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curl
    # lead-in
    lk.prose("How to decide whether a vector field is a gradient or not?")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curl
    # definition: curl
    lk.definition(
        [
            r"""
            Given $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ differentiable,

            > $\vec{F}(\vec{x}) = \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \\ R(\vec{x}) \end{bmatrix}$

            the **curl** of $\vec{F}$ is the vector field
            """,
            lk.aside(
                r"$$\mathrm{Curl}(\vec{F})(\vec{x}) = (\vec{\nabla} \times \vec{F})(\vec{x}) = \begin{bmatrix} {\large\tfrac{\partial R}{\partial y}}(\vec{x}) - {\large\tfrac{\partial Q}{\partial z}}(\vec{x}) \\[6pt] {\large\tfrac{\partial P}{\partial z}}(\vec{x}) - {\large\tfrac{\partial R}{\partial x}}(\vec{x}) \\[6pt] {\large\tfrac{\partial Q}{\partial x}}(\vec{x}) - {\large\tfrac{\partial P}{\partial y}}(\vec{x}) \end{bmatrix} = \mk{\det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ P(\vec{x}) & Q(\vec{x}) & R(\vec{x}) \end{bmatrix}}.$$",
                r"cross-product of $\vec{\nabla}$ and $\vec{F}(\vec{x})$",
            ),
        ],
        label="def-curl",
    )
    return


@app.cell(hide_code=True)
def _(FAINT, circle, disc, lk, np, tg):
    # module: curl
    # scene (no visible output; the example below shows it)
    # the flow of G(x) = x moves every point p to e^t p. A horizontal disc about x0 = (0.3, 1, 0.6), radius 0.45, with one
    # radius marked, is carried to the disc about e^t x0 of radius e^t 0.45: it grows and moves out along the ray through x0
    # (the flow line gamma, blue), and the marked radius keeps its direction (no turning). The disc at t = 0 stays, dashed grey.
    # The field G (red): 36 arrows, each at 3/10 of its vector, twelve on each of three circles of radius 1.3 about the ray, at
    # 1, 2.2 and 3.4 along it, and fainter six on circles of radius 1/2 in the path of the disc
    _e = np.exp(float(tg.value))
    _m = np.array([-np.sqrt(3) / 2, -0.5, 0.0])
    _x0, _rho = np.array([0.3, 1.0, 0.6]), 0.45
    _c = _e * _x0
    _u = _x0 / np.linalg.norm(_x0)
    _ray = np.linspace(0, 6.0, 80)[:, None] * _u[None, :]
    _a = np.cross(_u, [0, 0, 1.0])
    _a /= np.linalg.norm(_a)
    _b = np.cross(_u, _a)
    _pts = [_l * _u + 1.3 * (np.cos(np.radians((_j + _k / 2) * 30)) * _a + np.sin(np.radians((_j + _k / 2) * 30)) * _b) for _k, _l in enumerate((1.0, 2.2, 3.4)) for _j in range(12)]
    _path = [_l * _u + 0.5 * (np.cos(np.radians(60 * _j + 30 * _k)) * _a + np.sin(np.radians(60 * _j + 30 * _k)) * _b) for _k, _l in enumerate((1.0, 2.2, 3.4)) for _j in range(6)]
    lk.turntable(
        30,
        35,
        "the flow of the radial vector field G carries a disc about x out along a ray; the disc grows and its marked radius keeps its direction",
        [
            lk.panel(
                1.0,
                surfaces=[disc(_c, _e * _rho)],
                lines=[
                    (_ray[:, 0], _ray[:, 1], _ray[:, 2], lk.BLUE, 1.6),
                    (*circle(_x0, _rho), lk.GREY, 1.0, [3, 3]),
                    (*np.array([_x0, _x0 + _rho * _m]).T, lk.GREY, 1.2, [3, 3]),
                    (*circle(_c, _e * _rho), lk.GREEN, 1.5),
                    (*np.array([_c, _c + _e * _rho * _m]).T, lk.GREEN, 2.0),
                ],
                points=[(_x0, "#000000", 2.5)],
                arrows=[(p, 1.3 * p, lk.RED, 1.3) for p in _pts] + [(p, 1.3 * p, FAINT, 1.1) for p in _path],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 4.6, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(_x0, r"\vec{x}", "#000000", 180, 6), (_ray[-1], r"\gamma", lk.BLUE, 30, 5)],
                caption=r"\textcolor{#a8554c}{\vec{G}}",
                box=((-0.2, 3.0), (-0.2, 4.6), (-0.2, 3.0)),
            )
        ],
        height=lk.H3D,
        key="L18-flow-G",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, tg):
    # module: curl
    # example: curl of G
    lk.example(
        [
            r"""
            $\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $\displaystyle(\vec{\nabla} \times \vec{G})(\vec{x}) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ x & y & z \end{bmatrix} = \begin{bmatrix} {\large\tfrac{\partial}{\partial y}} z - {\large\tfrac{\partial}{\partial z}} y \\[6pt] {\large\tfrac{\partial}{\partial z}} x - {\large\tfrac{\partial}{\partial x}} z \\[6pt] {\large\tfrac{\partial}{\partial x}} y - {\large\tfrac{\partial}{\partial y}} x \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$",
                r"$\leadsto$ flow has no rotation around $\vec{x}$",
            ),
            lk.interactive(lk.frame("L18-flow-G", lk.H3D), controls=[tg]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(F, FAINT, circle, disc, lk, np, tf):
    # module: curl
    # scene (no visible output; the example below shows it)
    # the flow of F(x) = (-y, x, 1) turns every point about the z-axis by the angle t and lifts it by t. A horizontal disc
    # about x0 = (2, 0, 1/2), radius 0.8, with one radius marked, is carried along the helix through x0 (gamma, blue); the
    # marked radius turns by the angle t about the vertical through the disc's centre, the direction of curl F = (0, 0, 2),
    # drawn from the centre (orange, at full length). The field (red) at radius 3.4 and 1, twelve and six arrows at the heights
    # 1, 3 and 5 (1 and 3 at radius 1), and fainter at radius 2, where the disc passes. Heights at true scale.
    _t = float(tf.value)
    _x0, _rho = np.array([2.0, 0.0, 0.5]), 0.8
    _m0 = np.array([-0.5, np.sqrt(3) / 2, 0.0])

    def _flow(p, t):
        return np.array([p[0] * np.cos(t) - p[1] * np.sin(t), p[0] * np.sin(t) + p[1] * np.cos(t), p[2] + t])

    _c = _flow(_x0, _t)
    _m = _flow(_m0, _t) - np.array([0, 0, _t])
    _pts = [np.array([3.4 * np.cos(np.radians((_j + _l / 2) * 30)), 3.4 * np.sin(np.radians((_j + _l / 2) * 30)), 1.0 + 2 * _l]) for _l in range(3) for _j in range(12)]
    _pts += [np.array([np.cos(np.radians((_j + _l / 2) * 60)), np.sin(np.radians((_j + _l / 2) * 60)), 1.0 + 2 * _l]) for _l in range(2) for _j in range(6)]
    _mid = [np.array([2 * np.cos(np.radians((_j + _l / 2) * 30)), 2 * np.sin(np.radians((_j + _l / 2) * 30)), 1.0 + 2 * _l]) for _l in range(2) for _j in range(12)]
    _s = np.linspace(0, np.pi + 0.6, 120)
    lk.turntable(
        30,
        40,
        "the flow of F carries a disc about x along a helix; the marked radius turns about the vertical through the disc's centre, the direction of curl F = (0, 0, 2)",
        [
            lk.panel(
                1.0,
                surfaces=[disc(_c, _rho)],
                lines=[
                    (2 * np.cos(_s), 2 * np.sin(_s), 0.5 + _s, lk.BLUE, 1.6),
                    (*circle(_x0, _rho), lk.GREY, 1.0, [3, 3]),
                    (*np.array([_x0, _x0 + _rho * _m0]).T, lk.GREY, 1.2, [3, 3]),
                    (*circle(_c, _rho), lk.GREEN, 1.5),
                    (*np.array([_c, _c + _rho * _m]).T, lk.GREEN, 2.0),
                ],
                points=[(_x0, "#000000", 2.5)],
                axes=[((0, 0, 0), (4.2, 0, 0), "x", -150), ((0, 0, 0), (0, 4.2, 0), "y", 0), ((0, 0, 0), (0, 0, 5.6), "z", 90)],
                arrows=[(p, p + 0.3 * F(p), lk.RED, 1.3) for p in _pts] + [(p, p + 0.3 * F(p), FAINT, 1.1) for p in _mid] + [(_c, _c + np.array([0, 0, 2.0]), lk.ORANGE, 2.2)],
                texts=[(_x0, r"\vec{x}", "#000000", -100, 6), (_flow(_x0, np.pi + 0.6), r"\gamma", lk.BLUE, 90, 6)],
                caption=r"\textcolor{#a8554c}{\vec{F}} \qquad \textcolor{#b9853f}{\vec{\nabla} \times \vec{F}}",
                box=((-3.6, 3.6), (-3.6, 3.6), (0, 6.0)),
            )
        ],
        height=440,
        key="L18-flow-F",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, tf):
    # module: curl
    # example: curl of F
    lk.example(
        [
            r"""
            $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $(\vec{\nabla} \times \vec{F})(\vec{x}) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ -y & x & 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$",
                r"flow rotates around $\vec{x}$ with axis<br>of rotation along the $z$-axis",
            ),
            lk.interactive(lk.frame("L18-flow-F", 440), controls=[tf]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curl
    # consequence: what the curl determines
    lk.prose(r"$\leadsto$ &nbsp; $\mathrm{Curl}(\vec{F})(\vec{x})$ determines the axis and speed of rotation of the flow around $\vec{x}$.")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curl
    # remark: scalar curl
    lk.remark(
        r"""
        Curl is only defined for vector fields in $\mathbb{R}^3$.

        For $\vec{F} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$, we can define the “scalar curl” of &nbsp; $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$

        as the scalar function $\tfrac{\partial Q}{\partial x}(x, y) - \tfrac{\partial P}{\partial y}(x, y)$ obtained from

        $$
        \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \\ \partial / \partial z \end{bmatrix} \times \begin{bmatrix} P(x, y) \\ Q(x, y) \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ {\large\tfrac{\partial Q}{\partial x}}(x, y) - {\large\tfrac{\partial P}{\partial y}}(x, y) \end{bmatrix}.
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # theorem: curl of a gradient
    lk.theorem(
        [
            r"Gradient vector fields in $\mathbb{R}^3$ have zero curl!",
            lk.aside(
                r"$$\mathrm{Curl}(\vec{\nabla} f) = \vec{\nabla} \times (\vec{\nabla} f) = \mk{\vec{0}}$$",
                r"$\vec{0}$ = constant vector field",
            ),
        ],
        label="thm-curl-gradient",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # proof
    lk.proof(
        lk.aside(
            r"$$\vec{\nabla} \times (\vec{\nabla} f) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ \partial f / \partial x & \partial f / \partial y & \partial f / \partial z \end{bmatrix} = \mk{\begin{bmatrix} {\large\tfrac{\partial^2 f}{\partial y \partial z}} - {\large\tfrac{\partial^2 f}{\partial z \partial y}} \\[6pt] {\large\tfrac{\partial^2 f}{\partial z \partial x}} - {\large\tfrac{\partial^2 f}{\partial x \partial z}} \\[6pt] {\large\tfrac{\partial^2 f}{\partial x \partial y}} - {\large\tfrac{\partial^2 f}{\partial y \partial x}} \end{bmatrix}} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix} \qquad \square$$",
            r"assuming $f$ is $C^2$-smooth…",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # corollary: zero scalar curl
    lk.corollary(r"Gradient vector fields in $\mathbb{R}^2$ have zero scalar curl!", label="cor-scalar-curl")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # corollary: non-zero curl
    lk.corollary(r"If a vector field $\vec{F}$ has non-zero curl (scalar curl for $n = 2$), it cannot be a gradient!", label="cor-nonzero-curl")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # example: F is not a gradient
    lk.example(
        r"""
        $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; $\vec{\nabla} \times \vec{F}(\vec{x}) = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$

        > $\Longrightarrow$ &nbsp; there cannot exist any potential function $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ such that $\vec{F} = \vec{\nabla} f$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # theorem: divergence of a curl
    # the theorem on one line; its proof (the expansion) is the next cell
    lk.theorem(
        [
            lk.aside(
                r"$$\mathrm{Div}(\mathrm{Curl}(\vec{F})) = \vec{\nabla} \cdot (\vec{\nabla} \times \underbrace{\vec{F}}_{\text{assuming } C^2\text{-smooth}}) = \mk{0}$$",
                r"$0$ = constant function",
            ),
        ],
        label="thm-div-curl",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gradients have zero curl
    # proof
    lk.proof(
        r"""
        $$
        \vec{\nabla} \cdot (\vec{\nabla} \times \vec{F}) = \frac{\partial}{\partial x}\left( \cancel{\frac{\partial R}{\partial y}} - \bcancel{\frac{\partial Q}{\partial z}} \right) + \frac{\partial}{\partial y}\left( \xcancel{\frac{\partial P}{\partial z}} - \cancel{\frac{\partial R}{\partial x}} \right) + \frac{\partial}{\partial z}\left( \bcancel{\frac{\partial Q}{\partial x}} - \xcancel{\frac{\partial P}{\partial y}} \right) = 0
        $$
        """
    )
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
    # exercise: divergence and curl
    lk.exercise(
        r"""
        $$
        \vec{F}(\vec{x}) = \begin{bmatrix} yz \\ -xz \\ 0 \end{bmatrix} \qquad \vec{G}(\vec{x}) = \begin{bmatrix} e^y \\ x e^y + z \\ y \end{bmatrix} \qquad \vec{H}(\vec{x}) = \begin{bmatrix} xy \\ yz \\ zx \end{bmatrix}
        $$

        a) Compute the divergence and the curl

        b) Can the vector field be a gradient?

        c) Can the vector field be a curl?
        """,
        label="ex-div-curl",
    )
    return


if __name__ == "__main__":
    app.run()
