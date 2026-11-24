import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 5 · Lines and planes and the cross-product in ℝ³", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(5, r"Lines and planes and the cross-product in $\mathbb{R}^3$")
    return


@app.cell(hide_code=True)
def _(Figure):
    # Helpers of this lecture: bare sketches

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    return (blank,)


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    t_line = lk.slider(-1.5, 1.5, step=0.25, value=1, label="$t$")
    v1 = lk.slider(-2, 2, step=0.5, value=-1, label="$v^1$")
    v2 = lk.slider(-2, 3, step=0.5, value=3, label="$v^2$")
    v3 = lk.slider(-1.5, 1.5, step=0.5, value=0, label="$v^3$")
    return t_line, v1, v2, v3


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: determinants as signed area and signed volume
    _A2 = r"A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \ \Longrightarrow \ \det A"
    _A3 = r"A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \ \Longrightarrow \ \det A"
    lk.recap(
        "$" + _A2 + r" = ad - bc$",
        r"$\hphantom{" + _A2 + r"} = \text{signed area of parallelogram spanned by } \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix}, \ \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix}$",
        lk.gap(),
        "$" + _A3 + r" = a(ei - fh) - b(di - fg) + c(dh - eg)$",
        lk.aside(
            r"$\hphantom{" + _A3 + r"} = \mk{\text{signed volume}}$",
            r"$\leadsto$ need to interpret sign<br>$\leadsto$ need to understand angle between vectors and planes",
        ),
        topic="Determinants",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 1.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lines
    # section
    lk.section("Lines")
    return


@app.cell(hide_code=True)
def _(blank, lk):
    # module: lines
    # definition: line and affine parameterization, with the sketch of the line L through x in the direction of v
    _fig, _ax = blank(3.4, 1.75, (-0.6, 4.7), (-0.5, 1.95))
    _x, _v, _t = (0.4, 1.4), (1.6, 0.0), 1.7
    _g = (_x[0] + _t * _v[0], _x[1])
    _ax.plot([-0.5, 4.2], [1.4, 1.4], color="black", lw=1.0)
    lk.arrow(_ax, (0, 0), _g, lk.GREEN)
    lk.arrow(_ax, (0, 0), _x, "black")
    lk.arrow(_ax, (0, 0), _v, lk.RED)
    lk.arrow(_ax, _x, _g, lk.RED)
    _ax.plot(0, 0, "o", color="black", ms=4, zorder=4)
    _ax.text(0.08, 0.78, r"$\vec{x}$", fontsize=13, ha="right", va="center")
    _ax.text(0.8, -0.1, r"$\vec{v}$", color=lk.RED, fontsize=13, ha="center", va="top")
    _ax.text((_x[0] + _g[0]) / 2, 1.52, r"$t\vec{v}$", color=lk.RED, fontsize=13, ha="center", va="bottom")
    _ax.text(1.95, 0.62, r"$\vec{x} + t\vec{v}$", color=lk.GREEN, fontsize=13, ha="left", va="top")
    _ax.text(4.32, 1.4, "$L$", fontsize=13, ha="left", va="center")
    _ax.text(-0.1, -0.08, r"$\vec{0}$", fontsize=13, ha="right", va="top")

    lk.definition(
        [
            r"""
            Given vectors $\vec{x}$ and $\vec{v}$ in $\mathbb{R}^3$, with $\vec{v}$ non-zero, the **line** through $\vec{x}$ in the direction of $\vec{v}$ is the set

            $$
            L = \{ \gamma(t) = \vec{x} + t\vec{v} \in \mathbb{R}^3 \mid t \in \mathbb{R} \}
            $$

            We call the function &nbsp; $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^3$, &nbsp; $t \longmapsto \gamma(t) = \vec{x} + t\vec{v}$
            """,
            lk.aside(
                r"an <span class='lk-mark'>**affine**</span> **parameterization** of the line $L$",
                r"just a name for “linear plus constant”",
            ),
            lk.figure(_fig),
        ],
        label="def-line",
    )
    return


@app.cell(hide_code=True)
def _(lk, np, t_line):
    # module: lines
    # the scene of the example: the plane x^3 = 1 containing the line L through x in the direction of v, with the point
    # gamma(t) moving with the slider t
    _t = t_line.value
    _x, _v = np.array((0.0, 1.0, 1.0)), np.array((1.0, 2.0, 0.0))
    _g = _x + _t * _v + 0.0
    _plane = [(-1.8, -2.4, 1), (-1.8, 4.6, 1), (1.8, 4.6, 1), (1.8, -2.4, 1)]
    _rim = np.array(_plane + _plane[:1])
    _L = np.array([_x + _s * _v for _s in (-1.7, 1.8)])
    lk.turntable(
        24,
        26,
        "the plane x3 = 1 containing the line L through x in the direction of v, with the point gamma(t) = x + t v of L",
        [
            lk.panel(
                1.0,
                surfaces=[lk.patch(_plane, lk.LIGHT, 0.35, n=12)],
                lines=[(_rim[:, 0], _rim[:, 1], _rim[:, 2], lk.GREY, 1.0), (_L[:, 0], _L[:, 1], _L[:, 2], "#000000", 1.2)],
                points=[(tuple(_g), lk.GREEN)],
                axes=[((-0.5, 0, 0), (2.4, 0, 0), "x^1", -135), ((0, -0.5, 0), (0, 4.9, 0), "x^2", 0), ((0, 0, -0.5), (0, 0, 2.15), "x^3", 90)],
                arrows=[((0, 0, 0), tuple(_x), "#000000"), ((0, 0, 0), tuple(_v), lk.RED), ((0, 0, 0), tuple(_g), lk.GREEN)],
                texts=[((1.8, -2.4, 1), r"x^3 = 1", "#6b6b6b", 180, 6), (tuple(_L[0]), "L", "#000000", 180, 6), (tuple(0.5 * _x), r"\vec{x}", "#000000", 180, 6),
                       (tuple(_v), r"\vec{v}", lk.RED, -60, 6), (tuple(_g), r"\gamma(t)", lk.GREEN, 30, 7)],
                box=((-1.8, 2.4), (-2.4, 4.9), (-0.5, 2.15)),
            )
        ],
        height=lk.H3D,
        key="L05-line",
        bias=0.25,
        zoom=1.15,
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, t_line):
    # module: lines
    # example: a line in the plane x^3 = 1
    lk.example(
        [
            r"$\vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}$",
            r"> $\leadsto$ &nbsp; $\gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} t \\ 1 + 2t \\ 1 \end{bmatrix}$",
            lk.interactive(lk.frame("L05-line", lk.H3D), controls=[t_line]),
        ],
        label="ex-line",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lines
    # definition: starting point and velocity
    lk.definition(
        r"""
        Given a line $L$ with an affine parameterization

        $$
        \gamma(t) = \vec{x} + t\vec{v}
        $$

        we call $\vec{x}$ the **starting point** and $\vec{v}$ the **velocity** of $L$ with respect to the parameterization $\gamma$
        """,
        label="def-start-velocity",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lines
    # remark: one line through two points, many parameterizations
    lk.remark(
        r"""
        There exists a unique line through $\vec{x}, \vec{y} \in \mathbb{R}^3$ iff $\vec{y} - \vec{x}$ is non-zero

        However, parameterizations are not unique!

        > $\leadsto$ &nbsp; $L = \{ \gamma(t) = \vec{x} + t(\vec{y} - \vec{x}) \mid t \in \mathbb{R} \}$

        > <span class='lk-ghost'>$\leadsto$ &nbsp; $L$</span> $= \{ \tilde{\gamma}(t) = \vec{y} + 2t(\vec{x} - \vec{y}) \mid t \in \mathbb{R} \}$

        > <span class='lk-ghost'>$\leadsto$ &nbsp; $L$</span> $= \{ \hat{\gamma}(t) = \tfrac{1}{2}(\vec{x} + \vec{y}) + t(\vec{x} - \vec{y}) \mid t \in \mathbb{R} \}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: lines
    # remark: velocities are proportional
    lk.remark(r"For any pair of affine parameterizations $\gamma, \tilde{\gamma}$ of a line $L$, the velocity vectors are proportional!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: planes
    # section
    lk.section("Planes")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: planes
    # definition: plane and affine parameterization
    lk.definition(
        [
            r"Given $\vec{x}, \vec{u}, \vec{v} \in \mathbb{R}^3$, with $\vec{u}, \vec{v}$ not proportional, the **plane** through $\vec{x}$ in the directions of $\vec{u}$ and $\vec{v}$ is the set",
            lk.aside(
                r"$$ P = \{ \mk{\varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}} \mid s, t \in \mathbb{R} \} $$",
                r"affine parameterization of the plane<br>$\varphi : \mathbb{R}^2 \longrightarrow \mathbb{R}^3$",
            ),
        ],
        label="def-plane",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: planes
    # example: a plane, with the plane P through x in the directions of u and v and a point phi(s, t) of P
    _x, _u, _v = np.array((0.0, 1.0, 1.0)), np.array((1.0, 2.0, 0.0)), np.array((-1.0, 3.0, 0.0))
    _p = _x + 0.6 * _u + 0.4 * _v  # phi(s, t) at s = 0.6, t = 0.4
    _plane = [(-1.6, -0.6, 1), (-1.6, 4.3, 1), (1.6, 4.3, 1), (1.6, -0.6, 1)]
    _rim = np.array(_plane + _plane[:1])
    _marks = [((-0.08, 0.08), (1, 1), (0, 0)), ((-0.08, 0.08), (0, 0), (1, 1))]
    _fig = lk.turntable(
        28,
        30,
        "the plane P through x in the directions of u and v, and a point phi(s, t) of P",
        [
            lk.panel(
                1.0,
                surfaces=[lk.patch(_plane, lk.LIGHT, 0.35, n=12)],
                lines=[(_rim[:, 0], _rim[:, 1], _rim[:, 2], lk.GREY, 1.0)] + [(*_m, "#000000", 1.0) for _m in _marks],
                points=[(tuple(_p), lk.GREEN, 3.5)],
                axes=[((0, 0, 0), (2.4, 0, 0), "", 0), ((0, 0, 0), (0, 5.0, 0), "", 0), ((0, 0, 0), (0, 0, 2.0), "", 0)],
                arrows=[((0, 0, 0), tuple(_x), "#000000", 1.6), (tuple(_x), tuple(_x + _u), lk.BLUE, 1.6), (tuple(_x), tuple(_x + _v), lk.RED, 1.6), (tuple(_x), tuple(_p), lk.GREEN, 1.0)],
                texts=[((0, 1, 0), "1", "#000000", -90, 7), ((0, 0, 1), "1", "#000000", 180, 7), ((1.3, -0.4, 1), "P", "#6b6b6b", 90, 4),
                       (tuple(_x / 2), r"\vec{x}", "#000000", 180, 6), (tuple(_x + _u), r"\vec{u}", lk.BLUE, -30, 6), (tuple(_x + _v), r"\vec{v}", lk.RED, 60, 6),
                       (tuple(_p), r"\varphi(s, t)", lk.GREEN, 0, 7)],
            )
        ],
        height=lk.H3D,
        bias=0.25,
        zoom=1.15,
    )
    lk.example(
        [
            r"$\vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad \vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}$",
            r"> $\leadsto$ &nbsp; $\varphi(s, t) = \begin{bmatrix} s - t \\ 1 + 2s + 3t \\ 1 \end{bmatrix}$",
            lk.figure(_fig),
        ],
        label="ex-plane",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: planes
    # remark: one plane through three points, many parameterizations
    lk.remark(
        r"""
        There exists a unique plane through $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^3$ iff $\vec{y} - \vec{x}$, $\vec{z} - \vec{x}$ are not proportional

        $$
        P = \{ \varphi(s, t) = \vec{x} + s(\vec{y} - \vec{x}) + t(\vec{z} - \vec{x}) \mid s, t \in \mathbb{R} \}
        $$

        $\leadsto$ &nbsp; different parameterizations are also possible, with different starting points and directions
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: planes
    # definition: normal vector
    lk.definition(
        [
            r"Given a plane $P = \{ \vec{x} + s\vec{u} + t\vec{v} \mid s, t \in \mathbb{R} \}$, a vector $\vec{n} \in \mathbb{R}^3$ is called **normal** to $P$ if",
            lk.aside(r"$$ \vec{n} \cdot \vec{u} = \vec{n} \cdot \vec{v} = 0 $$", r"$\vec{n}$ is orthogonal to both directions in $P$"),
        ],
        label="def-normal",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cross-product
    # section
    lk.section("The cross-product")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: cross-product
    # definition: cross-product, with u, v, w = u x v and -w, and the turn from u to v
    _u, _v = np.array((0.7, 1.3, 0.0)), np.array((-1.0, 1.0, 0.0))
    _w = np.cross(_u, _v)
    _a, _b = _u / np.linalg.norm(_u), _v / np.linalg.norm(_v)
    _om = np.arccos(_a @ _b)
    _s = np.linspace(0.1, 0.9, 40)[:, None] * _om
    _turn = 0.75 * (np.sin(_om - _s) * _a + np.sin(_s) * _b) / np.sin(_om)
    _fig = lk.turntable(
        24,
        26,
        "the vectors u and v, their cross-product w = u x v orthogonal to both, minus w, and the turn from u to v through the angle theta",
        [
            lk.panel(
                1.0,
                arrows=[((0, 0, 0), tuple(-_w), lk.GREY, 1.8, [5, 4]), ((0, 0, 0), tuple(_w), lk.GREEN), ((0, 0, 0), tuple(_u), lk.BLUE), ((0, 0, 0), tuple(_v), lk.RED)],
                arcs=[(_turn[:, 0], _turn[:, 1], _turn[:, 2], lk.GREEN, 1.2)],
                texts=[(tuple(_turn[20]), r"\theta", lk.GREEN, -60, 4), (tuple(_u), r"\vec{u}", lk.BLUE, -30, 6), (tuple(_v), r"\vec{v}", lk.RED, 210, 6),
                       (tuple(_w), r"\vec{w} = \vec{u} \times \vec{v}", lk.GREEN, 0, 7), (tuple(-_w), r"-\vec{w}", lk.GREY, 0, 7)],
            )
        ],
        height=300,
    )
    _area = r"\begin{array}{c} \scriptstyle \text{area of parallelogram} \\ \scriptstyle \text{spanned by } \vec{u} \text{ and } \vec{v} \end{array}"
    lk.definition(
        [
            r"Given two vectors $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}, \ \vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix} \in \mathbb{R}^3$, the **cross-product** of $\vec{u}$ and $\vec{v}$ is the unique vector $\vec{w} = \vec{u} \times \vec{v} \in \mathbb{R}^3$ such that",
            lk.aside(r"$$ \vec{u} \cdot \vec{w} = 0, \quad \vec{v} \cdot \vec{w} = 0 $$", r"orthogonal to both $\vec{u}, \vec{v}$"),
            r"""
            $$
            \begin{aligned}
            \lVert \vec{w} \rVert^2 &= \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2\\[4pt]
            &= \Big( \underbrace{\lVert \vec{u} \rVert \lVert \vec{v} \rVert \sin\big(\theta(\vec{u}, \vec{v})\big)}_{"""
            + _area
            + r"""} \Big)^2
            \end{aligned}
            $$
            """,
            lk.aside(
                r"and &nbsp; $\vec{u}, \vec{v}, \vec{w}$ is <span class='lk-mark'>**right-handed**</span> (positively oriented)",
                r"with your right hand, rotating your fingers<br>from $\vec{u}$ to $\vec{v}$ points your thumb towards $\vec{w}$",
            ),
            lk.figure(_fig),
            r"algebraically: &nbsp; $\vec{u}, \vec{v}, \vec{w}$ is right-handed if",
            r"$$ \det \begin{bmatrix} \vec{u} & \vec{v} & \vec{w} \end{bmatrix} > 0 $$",
        ],
        label="def-cross",
    )
    return


@app.cell(hide_code=True)
def _(lk, np):
    # module: cross-product
    # remark: normals are proportional to u x v, with a plane P through x with the directions u and v and a normal vector
    _u, _v = np.array((0.7, 1.3, 0.0)), np.array((-1.0, 1.0, 0.0))
    _w = np.cross(_u, _v)
    _x, _n = np.array((0.4, 0.6, 1.4)), 0.7 * _w
    _plane = [_x + (_d1, _d2, 0) for _d1, _d2 in ((-1.5, -1.0), (-1.5, 1.9), (1.4, 1.9), (1.4, -1.0))]
    _rim = np.array(_plane + _plane[:1])
    _fig = lk.turntable(
        24,
        26,
        "a plane P through x with the directions u and v, a normal vector n = alpha u x v, and the vector x from the origin",
        [
            lk.panel(
                1.0,
                surfaces=[lk.patch(_plane, lk.LIGHT, 0.35, n=12)],
                lines=[(_rim[:, 0], _rim[:, 1], _rim[:, 2], lk.GREY, 1.0)],
                points=[((0, 0, 0), "#000000")],
                arrows=[((0, 0, 0), tuple(_x), "#000000"), (tuple(_x), tuple(_x + _u), lk.BLUE), (tuple(_x), tuple(_x + _v), lk.RED), (tuple(_x), tuple(_x + _n), lk.GREEN)],
                texts=[((0, 0, 0), r"\vec{0}", "#000000", 200, 6), (tuple(_x / 2), r"\vec{x}", "#000000", 180, 6), (tuple(_x + _u), r"\vec{u}", lk.BLUE, -30, 6),
                       (tuple(_x + _v), r"\vec{v}", lk.RED, 40, 7), (tuple(_x + _n), r"\vec{n} = \alpha \, \vec{u} \times \vec{v}", lk.GREEN, 0, 7), (tuple(_plane[2]), "P", "#6b6b6b", 0, 5)],
            )
        ],
        height=300,
        bias=0.25,
    )
    lk.remark(
        [
            r"""
            Given a parameterization

            $$
            \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}
            $$

            of a plane $P$, every normal vector to $P$ is proportional to the cross-product $\vec{u} \times \vec{v}$
            """,
            lk.figure(_fig),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: computing the cross-product
    # theorem: the cross-product as a formal determinant
    lk.theorem(
        [
            r"Given $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}$ and $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix}$ in $\mathbb{R}^3$",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \vec{u} \times \vec{v} &= \mk{\det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ u^1 & u^2 & u^3 \\ v^1 & v^2 & v^3 \end{bmatrix}}\\[6pt]
                &= \vec{e}_1 \det \begin{bmatrix} u^2 & u^3 \\ v^2 & v^3 \end{bmatrix} - \vec{e}_2 \det \begin{bmatrix} u^1 & u^3 \\ v^1 & v^3 \end{bmatrix} + \vec{e}_3 \det \begin{bmatrix} u^1 & u^2 \\ v^1 & v^2 \end{bmatrix}\\[6pt]
                &= \vec{e}_1 (u^2 v^3 - u^3 v^2) - \vec{e}_2 (u^1 v^3 - u^3 v^1) + \vec{e}_3 (u^1 v^2 - u^2 v^1)\\[6pt]
                &= \begin{bmatrix} u^2 v^3 - u^3 v^2 \\ u^3 v^1 - u^1 v^3 \\ u^1 v^2 - u^2 v^1 \end{bmatrix} = \vec{w}
                \end{aligned}
                $$
                """,
                r"not an honest determinant!<br>1st row is made of vectors …",
                at=1,
                rows=4,
            ),
        ],
        label="thm-cross-formula",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: computing the cross-product
    # proof
    lk.proof(
        [
            r"$\vec{u} \cdot \vec{w} = u^1 (\cancel{u^2 v^3} - \cancel{u^3 v^2}) + u^2 (\cancel{u^3 v^1} - \cancel{u^1 v^3}) + u^3 (\cancel{u^1 v^2} - \cancel{u^2 v^1})$",
            r"$\phantom{\vec{u} \cdot \vec{w}} = 0$",
            lk.gap(),
            r"$\vec{v} \cdot \vec{w} = 0$",
            lk.gap(),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \lVert \vec{w} \rVert^2 &= (u^2 v^3 - u^3 v^2)^2 + (u^3 v^1 - u^1 v^3)^2 + (u^1 v^2 - u^2 v^1)^2\\[4pt]
                &= \big( (u^1)^2 + (u^2)^2 + (u^3)^2 \big) \big( (v^1)^2 + (v^2)^2 + (v^3)^2 \big)\\
                &\phantom{=} \ - \big( u^1 v^1 + u^2 v^2 + u^3 v^3 \big)^2\\[4pt]
                &= \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2
                \end{aligned}
                $$
                """,
                "check!",
                at=2.5,
                rows=4,
            ),
            lk.aside(
                r"$$ \det \begin{bmatrix} u^1 & v^1 & (u^2 v^3 - u^3 v^2) \\ u^2 & v^2 & (u^3 v^1 - u^1 v^3) \\ u^3 & v^3 & (u^1 v^2 - u^2 v^1) \end{bmatrix} \mk{{} = \lVert \vec{w} \rVert^2} \ge 0 $$",
                "check!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, np, v1, v2, v3):
    # module: computing the cross-product
    # the scene of the example: u, v moving with the sliders, their cross-product and the parallelogram they span
    _u = np.array((1, 2, 0), float)
    _v = np.array((v1.value, v2.value, v3.value), float)
    _w = np.cross(_u, _v) + 0.0
    _R = 9  # one frame for every slider value (|u x v| < 8), no marks on the axes
    _len = 0.8 * _R
    _shafts, _axes = [], []  # axis shafts drawn beneath vectors lying along them; heads and names by the axes primitive
    for _i, (_e, _deg) in enumerate(zip(np.eye(3), (180, -60, 90))):
        _s = np.array([-0.3 * _len * _e, 0.9 * _len * _e])
        _shafts.append((_s[:, 0], _s[:, 1], _s[:, 2], "#000000", 1.1, None, -0.1 * _R))
        _axes.append((tuple(0.9 * _len * _e), tuple(_len * _e), f"x^{_i + 1}", _deg))
    _arrows, _dots = [], []
    for _p, _colour in ((_w, lk.GREEN), (_u, lk.BLUE), (_v, lk.RED)):
        if _p @ _p > 0:
            _arrows.append(((0, 0, 0), tuple(_p), _colour))
        else:  # a zero vector is a dot at the origin
            _dots.append(((0, 0, 0), _colour))
    _par = np.array([_u, _u + _v, _v])
    _b = _R / np.sqrt(3)
    lk.turntable(
        35,
        34,
        "the vectors u and v, their cross-product u x v and the parallelogram spanned by u and v",
        [
            lk.panel(
                1.0,
                surfaces=[lk.patch([np.zeros(3), _u, _u + _v, _v], lk.LIGHT, 0.7)],
                lines=[(_par[:, 0], _par[:, 1], _par[:, 2], lk.GREY, 1.0, [4, 3])] + _shafts,
                points=_dots,
                axes=_axes,
                arrows=_arrows,
                texts=[(tuple(_p), _n, _c, _a, 7) for _p, _n, _c, _a in ((_u, r"\vec{u}", lk.BLUE, -100), (_v, r"\vec{v}", lk.RED, 30), (_w, r"\vec{u} \times \vec{v}", lk.GREEN, 30)) if _p @ _p > 0],
                box=((-_b, _b), (-_b, _b), (-_b, _b)),
            )
        ],
        height=lk.H3D,
        key="L05-cross",
        apart=True,
    )
    return


@app.cell(hide_code=True)
def _(lk, v1, v2, v3):
    # module: computing the cross-product
    # example: a cross-product, checked against the definition
    lk.example(
        [
            r"$\vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}$",
            r"""
            > $$
            > \begin{aligned}
            > \leadsto \quad \vec{u} \times \vec{v} &= \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 2 & 0 \\ -1 & 3 & 0 \end{bmatrix}\\[6pt]
            > &= 0 \, \vec{e}_1 + 0 \, \vec{e}_2 + \big( 1 \cdot 3 - 2 \cdot (-1) \big) \vec{e}_3 = 5 \, \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 5 \end{bmatrix}
            > \end{aligned}
            > $$
            """,
            lk.gap(),
            r"$\vec{u} \cdot (\vec{u} \times \vec{v}) = 1 \cdot 0 + 2 \cdot 0 + 0 \cdot 5 = 0$",
            r"$\vec{v} \cdot (\vec{u} \times \vec{v}) = (-1) \cdot 0 + 3 \cdot 0 + 0 \cdot 5 = 0$",
            lk.gap(),
            r"$\lVert \vec{u} \times \vec{v} \rVert^2 = 25 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2 = (1 + 4)(1 + 9) - (-1 + 6)^2$",
            r"$\phantom{\lVert \vec{u} \times \vec{v} \rVert^2 = 25 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2} = 50 - 25$",
            lk.gap(),
            lk.aside(
                r"$\det \begin{bmatrix} 1 & -1 & 0 \\ 2 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix} = 1 \, (3 \cdot 5 - 0 \cdot 0) - (-1) \, (2 \cdot 5 - 0 \cdot 0) + 0 \, (2 \cdot 0 - 3 \cdot 0) = \mk{25} > 0$",
                r"$25 = \lVert \vec{u} \times \vec{v} \rVert^2$",
            ),
            lk.interactive(lk.frame("L05-cross", lk.H3D), controls=[v1, v2, v3]),
        ],
        label="ex-cross",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: computing the cross-product
    # remark: a product of vectors with values in vectors
    lk.remark(
        r"""
        The cross-product in $\mathbb{R}^3$ defines

        $$
        \times : \mathbb{R}^3 \times \mathbb{R}^3 \longrightarrow \mathbb{R}^3
        $$

        another extension of multiplication of vectors now taking values in vectors!

        > $\leadsto$ &nbsp; this **cannot** be extended to other $\mathbb{R}^n$ with $n \neq 3, 7$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: computing the cross-product
    # theorem: properties of the cross-product
    lk.theorem(
        [
            r"Given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$, $\alpha, \beta \in \mathbb{R}$",
            lk.aside(r"> • &nbsp; $\vec{u} \times \vec{v} = -\vec{v} \times \vec{u}$", "anti-commutativity"),
            lk.aside(
                r"> • &nbsp; $\begin{aligned} \vec{u} \times (\alpha\vec{v} + \beta\vec{w}) &= \alpha (\vec{u} \times \vec{v}) + \beta (\vec{u} \times \vec{w})\\ (\alpha\vec{u} + \beta\vec{v}) \times \vec{w} &= \alpha (\vec{u} \times \vec{w}) + \beta (\vec{v} \times \vec{w}) \end{aligned}$",
                "bilinearity",
            ),
        ],
        title="properties of the cross-product",
        label="thm-cross-properties",
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
    # exercise: points of a line
    lk.exercise(
        r"""
        Let $\vec{x} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}$, $\vec{v} = \begin{bmatrix} 2 \\ -1 \\ 4 \end{bmatrix}$, $\gamma(t) = \vec{x} + t\vec{v}$

        a) compute $\gamma(0)$, $\gamma(1)$, $\gamma(2)$

        b) compute $\gamma(2) - \gamma(1)$

        c) Is $\vec{y} = \begin{bmatrix} 7 \\ -1 \\ 12 \end{bmatrix}$ in the line $L = \{ \gamma(t) \mid t \in \mathbb{R} \}$?
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: the normal of a plane
    lk.exercise(
        r"""
        Let $\vec{u} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}$, $\vec{v} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}$, $\vec{x} = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix}$, $\varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}$

        a) Compute $\vec{n} = \vec{u} \times \vec{v}$

        b) Verify that every vector $\vec{y} \in P = \{ \varphi(s, t) \mid s, t \in \mathbb{R} \}$ satisfies $(\vec{y} - \vec{x}) \cdot \vec{n} = 0$

        c) Write $(\vec{y} - \vec{x}) \cdot \vec{n} = 0$ as equations on $y^1, y^2, y^3$ and decide if $\vec{y} = \begin{bmatrix} 2 \\ 1 \\ 2 \end{bmatrix}$ and $\vec{y} = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$ are in $P$
        """,
        label="ex-practice-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: a determinant
    lk.exercise(
        [
            r"Let $A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 1 \end{bmatrix}$",
            "a) is $A$ invertible?",
            "b) what is the volume of the parallelepiped spanned by the columns of $A$?",
            lk.aside(r"c) is $\vec{A}_1, \vec{A}_2, \vec{A}_3$ <span class='lk-mark'>right-handed</span>?", "positively oriented"),
        ],
        label="ex-practice-3",
    )
    return


if __name__ == "__main__":
    app.run()
