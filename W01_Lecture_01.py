import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 01 · The Cartesian n-space", css_file="bs101.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc
    from mpl_toolkits.mplot3d import proj3d

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np, proj3d


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    RED, GREEN, BLUE, GREY = "#b3261e", "#2e7d32", "#1b458f", "#888888"

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

    def warning(body):
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, label_offset=(6, 6), label_ha="left", label_va="bottom", **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "->,head_width=0.3,head_length=0.5", "color": color, "lw": 1.4, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=label_offset, ha=label_ha, va=label_va, color=color, fontsize=18)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color="#cfe3f5", lw=0.6)
        ax.set_axisbelow(True)

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, GREEN, GREY, RED, arrow, check, definition, header, plane, theorem, warning


@app.cell(hide_code=True)
def _(header):
    header("Lecture 01", "Week 01", "Lecture 01 · The Cartesian n-space")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **BS101 – Multivariable Calculus**

    | | |
    |:--|:--|
    | **Instructor** | Prof. Scarinci (cscarinci@dgist.ac.kr) |
    | **Office hours** | Thu 10:45 – 11:45 (E7 L10) — schedule @ [cal.com/cscarinci](https://cal.com/cscarinci) |
    | **TAs** | 이시후, 이상아 |

    ## Course Description

    **Real-valued functions** = descriptions of how a given quantity depends on another: assigning a real output value $y = f(x)$ to each real input $x$.

    **Calculus** = study of continuous change and accumulation of real-valued functions, via differentiation and integration.

    **Multivariable functions** = extensions of real-valued functions to several inputs and/or outputs: describe how multiple quantities depend on multiple others simultaneously.

    We will develop the necessary extensions of Calculus to multivariable functions in 6 parts:

    | | | |
    |:--|:--|:--|
    | I. | Euclidean Geometry | L01 ~ L05 |
    | II. | Differentiation | L06 ~ L09 |
    | III. | Applications to Optimization | L10 ~ L14 |
    | IV. | Integration of scalar functions | L15 ~ L19 |
    | V. | Vector fields and surfaces | L20 ~ L22 |
    | VI. | Integration of vector fields | L23 ~ L28 |

    ## Textbooks

    - *Vector Calculus* by Marsden–Tromba — main textbook
    - *Calculus: Early Transcendentals* by Stewart — supplementary

    **WARNING:** the notations in my notes and BOTH textbooks may differ!

    ## Assessment

    | | |
    |:--|:--|
    | 6 quizzes | W02, W04, W06, W10, W12, W14 |
    | 2 exams | W08, W16 |
    | in-class practice | every lecture |

    **In-class practice**

    - 1–2 questions (~ 15–20 minutes)
    - open book
    - LMS upload on random days
    - honest attempt gets full credit

    **Quizzes**

    - 1–3 questions (~ 20–30 minutes)
    - closed book
    - physical submission + LMS
    - graded

    ## Grades

    $$
    X = \frac{3X_1 + 3X_2 + 3X_3 + X_4}{10}
    \qquad
    \begin{cases}
    X_1 = \text{midterm exam} \\
    X_2 = \text{final exam} \\
    X_3 = \text{quizzes} \\
    X_4 = \text{practice}
    \end{cases}
    $$

    | Letter | A+ | A0 | A− | B+ | B0 | B− | C+ | C0 | C− | D+ | D0 | D− | F |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | Minimum score | 97 | 94 | 90 | 85 | 80 | 75 | 70 | 65 | 60 | 57 | 54 | 50 | 0 |

    ## Course Policies

    - Missed exam without justification $\Longrightarrow$ F
    - Missed quiz without justification $\Longrightarrow$ that quiz $= 0$; with justification (at most two) $\Longrightarrow$ $X_3 =$ average of remaining
    - Attendance $< 75\%$ without justification $\Longrightarrow$ F
    - Cheating (plagiarism, proxy attendance) $\Longrightarrow$ F

    ## Practicalities

    - Weekly exercises on LMS (ungraded)
    - Diagnostic test + Review exercises + W01 already available
    - Solutions released the following week
    - Ask questions in class / office hours / to TAs!
    - Office hours meetings can be scheduled @ [cal.com/cscarinci](https://cal.com/cscarinci); meetings outside office hours can also be requested
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## 1 &nbsp; The Cartesian $n$-space

    **Recall:** $\mathbb{R}$ (the line of real numbers) has two algebraic operations

    | addition | multiplication |
    |:---:|:---:|
    | $+ : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}$ | $\cdot : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}$ |
    | $(\alpha, \beta) \longmapsto \alpha + \beta$ | $(\alpha, \beta) \longmapsto \alpha \cdot \beta$ |

    These allow us to perform calculations with real numbers and real-valued functions and, eventually, allow us to define Calculus.

    Our first goal is to extend these operations from real numbers to collections of real numbers.
    """
            ),
            definition(
                r"""
    For each $n \in \mathbb{Z}_{>0} = \{1, 2, 3, \dots\}$ (positive integers), we define the **Cartesian $n$-space** $\mathbb{R}^n$ as the set of all ordered lists of $n$ real numbers ($n$-tuples of real numbers)

    $$
    \mathbb{R}^n = \left\{\, \vec{x} = (x^1, x^2, \dots, x^n) \;\middle|\; x^i \in \mathbb{R},\ \forall\, i = 1, 2, \dots, n \,\right\}
    $$
    """
            ),
            mo.md(
                r"""
    **Example.**

    | | | |
    |:--|:--|:--|
    | ${n = 1}$ | ${\mathbb{R}^1 = \mathbb{R} \ni x = (x^1)}$ | list of a single number (no need for arrows here) |
    | ${n = 2}$ | ${\mathbb{R}^2 = \mathbb{R} \times \mathbb{R} \ni \vec{x} = (x^1, x^2)}$ | ordered pairs of numbers — order matters! ${(x^1, x^2) \neq (x^2, x^1)}$ unless ${x^1 = x^2}$ |
    | ${n = 3}$ | ${\mathbb{R}^3 \ni \vec{x} = (x^1, x^2, x^3)}$ | ordered triples |
    | $\;\vdots$ | | |
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, proj3d):
    def _axes3d(ax):
        for _d in ((2.2, 0, 0), (0, 2.2, 0), (0, 0, 2.2)):
            ax.quiver(0, 0, 0, *_d, color="black", lw=0.9, arrow_length_ratio=0.06)
        ax.set_xlim(0, 2)
        ax.set_ylim(0, 2)
        ax.set_zlim(0, 2)
        ax.view_init(elev=22, azim=28)
        ax.set_axis_off()

    def spaces_figure(arrows):
        """R^1, R^2, R^3 with a point (arrows=False) or an arrow from the origin (arrows=True)."""
        fig = Figure(figsize=(9.6, 3.2), layout="constrained")
        kw = {"arrowstyle": "->,head_width=0.3,head_length=0.5", "color": "black", "lw": 0.9, "shrinkA": 0, "shrinkB": 0}
        vec = {"arrowstyle": "->,head_width=0.3,head_length=0.5", "color": GREEN, "lw": 1.4, "shrinkA": 0, "shrinkB": 0}

        ax = fig.add_subplot(1, 3, 1)
        ax.set_xlim(-0.5, 2.4)
        ax.set_ylim(-1, 1)
        ax.axis("off")
        ax.annotate("", xy=(2.3, 0), xytext=(-0.5, 0), arrowprops=kw)
        if arrows:
            ax.annotate("", xy=(1.4, 0), xytext=(0, 0), arrowprops=vec)
            ax.text(0.6, 0.12, "$x$", color=GREEN)
        ax.plot([0, 1.4], [0, 0], "o", color=BLUE, ms=5)
        ax.text(-0.05, -0.28, "$0$", color=BLUE)
        ax.text(1.33, -0.28, "$x$", color=BLUE)
        ax.text(2.2, -0.3, r"$\mathbb{R}$")
        ax.set_title("$n = 1$" if arrows else "$n = 1$: the real line", y=-0.05)

        ax = fig.add_subplot(1, 3, 2)
        ax.set_xlim(-0.5, 2.4)
        ax.set_ylim(-0.5, 2.4)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.annotate("", xy=(2.3, 0), xytext=(-0.5, 0), arrowprops=kw)
        ax.annotate("", xy=(0, 2.3), xytext=(0, -0.5), arrowprops=kw)
        if arrows:
            ax.annotate("", xy=(1.4, 1.5), xytext=(0, 0), arrowprops=vec)
            ax.text(1.0, 0.55, r"$\genfrac{[}{]}{0}{0}{x^1}{x^2}$", color=GREEN)
        else:
            ax.plot([1.4, 1.4], [0, 1.5], "--", color=GREEN, lw=1.2)
            ax.plot([0, 1.4], [1.5, 1.5], "--", color=GREEN, lw=1.2)
            ax.text(1.33, -0.3, "$x^1$", color=GREEN)
            ax.text(-0.4, 1.43, "$x^2$", color=GREEN)
        ax.plot([0, 1.4], [0, 1.5], "o", color=BLUE, ms=5)
        ax.text(0.08, -0.32, "$(0,0)$", color=BLUE)
        ax.text(1.0, 1.68, r"$(x^1, x^2)$" if arrows else r"$\vec{x} = (x^1, x^2)$", color=BLUE)
        ax.set_title("$n = 2$" if arrows else "$n = 2$: the real plane", y=-0.12)

        ax = fig.add_subplot(1, 3, 3, projection="3d")
        _axes3d(ax)
        p = (1.1, 1.2, 1.3)
        if arrows:
            ax.quiver(0, 0, 0, *p, color=GREEN, lw=1.4, arrow_length_ratio=0.08)
        else:
            ax.plot([p[0], p[0]], [p[1], p[1]], [0, p[2]], "--", color=GREEN, lw=1.2)
            ax.plot([p[0], p[0]], [0, p[1]], [0, 0], "--", color=GREEN, lw=1.2)
            ax.plot([0, p[0]], [p[1], p[1]], [0, 0], "--", color=GREEN, lw=1.2)
            ax.plot([0, p[0]], [0, p[1]], [p[2], p[2]], "--", color=GREEN, lw=1.2)
            ax.text(p[0] + 0.25, -0.35, 0, "$x^1$", color=GREEN)
            ax.text(-0.3, p[1] + 0.12, 0, "$x^2$", color=GREEN)
            ax.text(0, -0.35, p[2], "$x^3$", color=GREEN)
        ax.scatter([0, p[0]], [0, p[1]], [0, p[2]], color=BLUE, s=22, depthshade=False)
        _px, _py, _ = proj3d.proj_transform(*p, ax.get_proj())
        ax.annotate(r"$(x^1, x^2, x^3)$" if arrows else r"$\vec{x} = (x^1, x^2, x^3)$", (_px, _py), textcoords="offset points", xytext=(7, 3), ha="left", va="bottom", color=BLUE, annotation_clip=False)
        ax.set_title("$n = 3$" if arrows else "$n = 3$: the real space", y=-0.08)
        return fig

    spaces_figure(False)
    return (spaces_figure,)


@app.cell(hide_code=True)
def _(mo, spaces_figure):
    mo.vstack(
        [
            mo.md(
                r"""
    Geometrically, elements in $\mathbb{R}^n$ are points in an “$n$-dimensional” space with $n$ “orthogonal axes” intersecting at a single point (the origin).

    To extend the operations $+$ and $\cdot$ to $\mathbb{R}^n$, we need yet another way to think about its elements!
    """
            ),
            mo.md(
                r"""
    **Remark.** Every element $\vec{x} = (x^1, \dots, x^n) \in \mathbb{R}^n$ can be realized as a unique arrow from the origin $\vec{0} = (0, \dots, 0)$.
    """
            ),
            spaces_figure(True),
            mo.md(
                r"""
    We will denote this arrow by an **$n$-vector** (an $n \times 1$ array, a column matrix of size $n$)

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \in \mathrm{Mat}(n \times 1)
    \qquad (n \text{ rows},\ 1 \text{ column})
    $$

    In this course there is no fundamental difference between “points in space” and “arrows from the origin”. We can think of it as a change in perspective.

    When the distinction matters, we will use

    $$
    \vec{x} = (x^1, \dots, x^n) \ \text{ for points} \qquad \text{and} \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \ \text{ for arrows from the origin}
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
            definition(
                r"""
    On $\mathbb{R}^n$ we can define two operations

    $$
    {+} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n \quad (\text{vector addition})
    \qquad \text{and} \qquad
    \cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n \quad (\text{scalar–vector multiplication})
    $$

    via

    $$
    \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} + \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} = \begin{bmatrix} x^1 + y^1 \\ x^2 + y^2 \\ \vdots \\ x^n + y^n \end{bmatrix}
    \qquad \qquad
    \alpha \cdot \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \alpha x^2 \\ \vdots \\ \alpha x^n \end{bmatrix}
    $$

    (component-wise addition and component-wise multiplication).
    """
            ),
            mo.md(
                r"""
    Note that multiplication is defined between real numbers (*scalars*) and elements in $\mathbb{R}^n$ (*$n$-vectors*).

    And the reason to use $n$-vectors (arrows from origin) here, instead of $n$-tuples (points in $n$-space), has to do with geometric interpretation.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    x1 = mo.ui.slider(-4, 4, 0.5, value=3, label="$x^1$", show_value=True)
    x2 = mo.ui.slider(-4, 4, 0.5, value=1, label="$x^2$", show_value=True)
    y1 = mo.ui.slider(-4, 4, 0.5, value=1, label="$y^1$", show_value=True)
    y2 = mo.ui.slider(-4, 4, 0.5, value=2.5, label="$y^2$", show_value=True)
    alpha = mo.ui.slider(-2, 2, 0.25, value=2, label=r"$\alpha$", show_value=True)
    return alpha, x1, x2, y1, y2


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, alpha, arrow, mo, plane, x1, x2, y1, y2):
    _x = (x1.value, x2.value)
    _y = (y1.value, y2.value)
    _s = (_x[0] + _y[0], _x[1] + _y[1])
    _a = alpha.value
    _ax_ = (_a * _x[0], _a * _x[1])

    _fig = Figure(figsize=(9.2, 4.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    plane(_left, 8.5)
    _left.plot([_x[0], _s[0]], [_x[1], _s[1]], "--", color=BLUE, lw=1.2)
    _left.plot([_y[0], _s[0]], [_y[1], _s[1]], "--", color=GREEN, lw=1.2)
    arrow(_left, (0, 0), _s, RED, r"$\vec{x}+\vec{y}$", at_tip=True)
    arrow(_left, (0, 0), _x, GREEN, r"$\vec{x}$", at_tip=True, label_offset=(6, -6), label_va="top")
    arrow(_left, (0, 0), _y, BLUE, r"$\vec{y}$", at_tip=True, label_offset=(-6, 6), label_ha="right")

    plane(_right, 8.5)
    arrow(_right, (0, 0), _ax_, RED, r"$\alpha\vec{x}$", at_tip=True)
    arrow(_right, (0, 0), _x, GREEN, r"$\vec{x}$", at_tip=True, label_offset=(6, -6), label_va="top")
    for _ax in (_left, _right):
        _ax.set_xticks(range(-8, 9, 2))
        _ax.set_yticks(range(-8, 9, 2))

    mo.vstack(
        [
            mo.hstack([mo.vstack([x1, x2]), mo.vstack([y1, y2]), alpha], justify="start", gap=3),
            mo.md(
                "| | | | |\n|:--|:--|:--|:--|\n"
                + rf"| $\vec{{x}}$ | $\begin{{bmatrix}} {_x[0]:g} \\ {_x[1]:g} \end{{bmatrix}}$ "
                + rf"| $\vec{{y}}$ | $\begin{{bmatrix}} {_y[0]:g} \\ {_y[1]:g} \end{{bmatrix}}$ |"
                + "\n"
                + rf"| $\vec{{x}} + \vec{{y}}$ | $\begin{{bmatrix}} {_s[0]:g} \\ {_s[1]:g} \end{{bmatrix}}$ "
                + rf"| $\alpha \vec{{x}}$ | $\begin{{bmatrix}} {_ax_[0]:g} \\ {_ax_[1]:g} \end{{bmatrix}}$ |"
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    We can interpret the operations in terms of arrows from the origin, not in terms of points.

    These carry most of the properties of the usual addition and multiplication in $\mathbb{R}$.
    """
            ),
            theorem(
                r"""
    For every $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and $\alpha, \beta \in \mathbb{R}$

    - $(\vec{x} + \vec{y}) + \vec{z} = \vec{x} + (\vec{y} + \vec{z})$ and $\alpha \cdot (\beta \cdot \vec{x}) = (\alpha\beta) \cdot \vec{x}$ &nbsp; (associativity)
    - $(\alpha + \beta) \cdot \vec{x} = \alpha \cdot \vec{x} + \beta \cdot \vec{x}$ and $\alpha \cdot (\vec{x} + \vec{y}) = \alpha \cdot \vec{x} + \alpha \cdot \vec{y}$ &nbsp; (distributivity)
    - $\vec{x} + \vec{y} = \vec{y} + \vec{x}$ &nbsp; (commutativity)
    - $\vec{x} + \vec{0} = \vec{x}$, &nbsp; $(1) \cdot \vec{x} = \vec{x}$ &nbsp; (neutral operations)
    - $0 \cdot \vec{x} = \vec{0}$, &nbsp; $\alpha \cdot \vec{0} = \vec{0}$ &nbsp; (null operations)
    """
            ),
            mo.md(r"**Proof.** Exercise!"),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
