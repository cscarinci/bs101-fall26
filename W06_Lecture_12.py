import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 12 · The chain rule", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return (lk,)


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(12, "The chain rule")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: differentiability of the four kinds of maps, and continuous partial derivatives
    lk.recap(
        lk.aside(
            r"• &nbsp; $\mk{f : \mathbb{R} \longrightarrow \mathbb{R}}$ is differentiable at $x = a$ if",
            "single variable scalar valued",
        ),
        lk.aside(
            r"> $\mk{f'(a)} = \displaystyle\lim_{x \to a} \frac{f(x) - f(a)}{x - a} \in \mathbb{R}$ is well-defined",
            r"$f'(a)$ = slope of tangent line to $\mathrm{graph}(f)$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$",
        ),
        lk.gap(),
        lk.aside(
            r"• &nbsp; $\mk{f : \mathbb{R} \longrightarrow \mathbb{R}^m}$ &nbsp; $\leadsto$ &nbsp; $f(x) = \begin{bmatrix} f^1(x) \\ f^2(x) \\ \vdots \\ f^m(x) \end{bmatrix}$, $f^i : \mathbb{R} \longrightarrow \mathbb{R}$",
            "single variable vector valued (path)",
        ),
        lk.aside(
            r"> is differentiable at $x = a$ if each component $f^i$ <span class='lk-mark'>is differentiable at $x = a$</span>",
            "as a single variable scalar function",
        ),
        lk.aside(
            r"> > $\Longleftrightarrow$ &nbsp; $\displaystyle\lim_{x \to a} \frac{f(x) - f(a)}{x - a} = \mk{f'(a)} = \begin{bmatrix} (f^1)'(a) \\ (f^2)'(a) \\ \vdots \\ (f^m)'(a) \end{bmatrix} \in \mathbb{R}^m$",
            r"derivative of $f$ at $x = a$<br>(velocity vector of $f$ at $x = a$)",
        ),
        lk.gap(),
        lk.aside(
            r"• &nbsp; $\mk{f : \mathbb{R}^n \longrightarrow \mathbb{R}}$ is differentiable at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ a^2 \\ \vdots \\ a^n \end{bmatrix}$ if",
            "multivariable scalar valued",
        ),
        r"> $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0$",
        lk.aside(
            r"> > where $\mk{Df(\vec{a})} = \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f}{\partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial f}{\partial x^n}}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)$",
            r"derivative of $f$ at $\vec{x} = \vec{a}$<br>(Jacobian matrix of $f$ at $\vec{x} = \vec{a}$)",
        ),
        lk.gap(),
        lk.aside(
            r"• &nbsp; $\mk{f : \mathbb{R}^n \longrightarrow \mathbb{R}^m}$ &nbsp; $\leadsto$ &nbsp; $f(\vec{x}) = \begin{bmatrix} f^1(\vec{x}) \\ f^2(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}$, $f^i : \mathbb{R}^n \longrightarrow \mathbb{R}$",
            "multivariable vector valued",
        ),
        lk.aside(
            r"> is differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \\ \vdots \\ a^n \end{bmatrix}$ if each component $f^i$ <span class='lk-mark'>is differentiable at $\vec{a}$</span>",
            "as a multivariable scalar valued function",
        ),
        r"""
        > > $\Longleftrightarrow$ &nbsp; $\displaystyle\lim_{\vec{x} \to \vec{a}} \frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert} = 0$

        > > > where
        """,
        lk.aside(
            r"""
            $$
            \mk{Df(\vec{a})} = \begin{bmatrix} Df^1(\vec{a}) \\ Df^2(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix} = \begin{bmatrix}
            {\large\tfrac{\partial f^1}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f^1}{\partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial f^1}{\partial x^n}}(\vec{a})\\[6pt]
            {\large\tfrac{\partial f^2}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f^2}{\partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial f^2}{\partial x^n}}(\vec{a})\\
            \vdots & \vdots & \ddots & \vdots\\
            {\large\tfrac{\partial f^m}{\partial x^1}}(\vec{a}) & {\large\tfrac{\partial f^m}{\partial x^2}}(\vec{a}) & \cdots & {\large\tfrac{\partial f^m}{\partial x^n}}(\vec{a}).
            \end{bmatrix} \in \mathrm{Mat}(m \times n)
            $$
            """,
            r"derivative of $f$ at $\vec{a}$<br>(Jacobian matrix of $f$ at $\vec{a}$)",
        ),
        r"""
        > > $\Longleftrightarrow$ &nbsp; $g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})$ is the affine approximation of $f$ at $\vec{a}$
        """,
        lk.gap(),
        r"""
        If all partial derivatives ${\large\tfrac{\partial f^i}{\partial x^j}}(\vec{x})$ are well-defined on an open ball around $\vec{a}$ and they are all continuous at $\vec{x} = \vec{a}$, then $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{x} = \vec{a}$
        """,
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("More properties", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("MT 2.5, 2.6")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: motivation
    # recall: the chain rule in one variable
    lk.recall(
        [
            r"""
            $f, g : \mathbb{R} \longrightarrow \mathbb{R}$, $f$ differentiable at $a$, $g$ differentiable at $b = f(a)$

            > $\Longrightarrow$ &nbsp; $g \circ f : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $a$
            """,
            lk.aside(
                r"> <span class='lk-ghost'>$\Longrightarrow$ &nbsp; </span>with $\mk{(g \circ f)'(a) = g'(f(a)) \cdot f'(a)}$",
                "chain rule",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: motivation
    # prose: what we want to generalize, and where we start
    lk.prose(
        r"""
        $\leadsto$ &nbsp; we want to generalize this to multivariable maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$
        """,
        lk.aside(
            r"$\leadsto$ &nbsp; start with $\mk{\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n}$ and $\mk{f : \mathbb{R}^n \longrightarrow \mathbb{R}}$",
            r"$\gamma$ = path<br>$f$ = scalar valued function",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule along a path
    # theorem: chain rule for f o gamma
    lk.theorem(
        r"""
        If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ is differentiable at $t = t_0$ and $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{x} = \vec{a} = \gamma(t_0)$, then $g = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$ is differentiable at $t = t_0$ with

        $$
        g'(t_0) = (f \circ \gamma)'(t_0) = \underbrace{Df(\gamma(t_0))}_{\mathbb{R}^n \to \mathbb{R}} \, \underbrace{(\gamma'(t_0))}_{\mathbb{R}^n}.
        $$
        """,
        label="thm-chain-path",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule along a path
    # proof: chain rule for f o gamma
    lk.proof(
        [
            r"""
            $\dfrac{g(t) - g(t_0)}{t - t_0} = \dfrac{f(\gamma(t)) - f(\gamma(t_0))}{t - t_0}$

            $\phantom{\dfrac{g(t) - g(t_0)}{t - t_0}} = \dfrac{f(\gamma(t)) - f(\gamma(t_0))}{\lVert \gamma(t) - \gamma(t_0) \rVert} \cdot \dfrac{\lVert \gamma(t) - \gamma(t_0) \rVert}{t - t_0}$
            """,
            lk.aside(
                r"$\phantom{\dfrac{g(t) - g(t_0)}{t - t_0}} = \underbrace{\dfrac{f(\mk{\gamma(t)}) - f(\mk{\gamma(t_0)}) - Df(\gamma(t_0))(\gamma(t) - \gamma(t_0))}{\lVert \gamma(t) - \gamma(t_0) \rVert}}_{\substack{\longrightarrow 0 \text{ since } \gamma \text{ continuous at } t_0\\ \text{and } f \text{ differentiable at } \vec{a} = \gamma(t_0)}} \, \underbrace{\dfrac{\lVert \gamma(t) - \gamma(t_0) \rVert}{t - t_0}}_{\substack{\longrightarrow \pm \lVert \gamma'(t_0) \rVert\\ \text{not } +\infty}}\rule[-2.4em]{0pt}{0pt}$",
                r"$\gamma(t) = \vec{x}$, $\gamma(t_0) = \vec{a}$",
            ),
            r"$\phantom{\dfrac{g(t) - g(t_0)}{t - t_0} =} \quad {} + \underbrace{Df(\gamma(t_0))}_{\text{constant matrix}} \;\; \underbrace{\left( \dfrac{\gamma(t) - \gamma(t_0)}{t - t_0} \right)}_{\longrightarrow \gamma'(t_0)}\rule[-1.8em]{0pt}{0pt}$",
            lk.gap(),
            r"""
            $$
            \begin{aligned}
            \Longrightarrow \quad \lim_{t \to t_0} \frac{g(t) - g(t_0)}{t - t_0} &= 0 + Df(\gamma(t_0))(\gamma'(t_0))\\[4pt]
            &= \begin{bmatrix} {\large\tfrac{\partial f}{\partial x^1}}(\gamma(t_0)) & \cdots & {\large\tfrac{\partial f}{\partial x^n}}(\gamma(t_0)) \end{bmatrix} \begin{bmatrix} (\gamma^1)'(t_0) \\ \vdots \\ (\gamma^n)'(t_0) \end{bmatrix}\\[4pt]
            &= \frac{\partial f}{\partial x^1}(\gamma(t_0)) \, (\gamma^1)'(t_0) + \dots + \frac{\partial f}{\partial x^n}(\gamma(t_0)) \, (\gamma^n)'(t_0)
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $\therefore$ &nbsp; <span class="lk-tab" style="--lk-tab: 7.4em">$\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$</span>differentiable at $t = t_0$.

            <span class='lk-ghost'>$\therefore$ &nbsp; </span><span class="lk-tab" style="--lk-tab: 7.4em">$f : \mathbb{R}^n \longrightarrow \mathbb{R}$</span>differentiable at $\vec{x} = \vec{a} = \gamma(t_0)$

            > then $g = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$ differentiable at $t = t_0$

            > with $g'(t_0) = (f \circ \gamma)'(t_0) = \displaystyle\sum_{i=1}^{n} \frac{\partial f}{\partial x^i}(\gamma(t_0)) \, (\gamma^i)'(t_0)$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule along a path
    # example: gamma(t) = (t^2, t^3), f = x^1 x^2
    lk.example(
        [
            r"""
            $\gamma(t) = \begin{bmatrix} t^2 \\ t^3 \end{bmatrix}$, $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 x^2$

            > $\gamma'(t_0) = \begin{bmatrix} 2t_0 \\ 3t_0^2 \end{bmatrix}$
            """,
            lk.aside(
                r"> $Df(\vec{a}) = \begin{bmatrix} a^2 & a^1 \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; $Df(\mk{\gamma(t_0)}) = \begin{bmatrix} t_0^3 & t_0^2 \end{bmatrix}$",
                r"$\gamma(t_0) = \vec{a}$",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $g(t) = f \circ \gamma(t) = f\left( \begin{bmatrix} t^2 \\ t^3 \end{bmatrix} \right) = t^2 \cdot t^3 = t^5$

            > > also differentiable at $t = t_0$

            > > with $g'(t_0) = Df(\gamma(t_0))(\gamma'(t_0)) = \begin{bmatrix} t_0^3 & t_0^2 \end{bmatrix} \begin{bmatrix} 2t_0 \\ 3t_0^2 \end{bmatrix} = 2t_0^4 + 3t_0^4 = 5t_0^4$
            """,
        ],
        label="ex-chain-t5",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule along a path
    # example: helix and f = (x^2)^2 + (x^3)^2
    lk.example(
        r"""
        $\gamma(t) = \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix}$, $f\left( \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \right) = (x^2)^2 + (x^3)^2$

        > $\Longrightarrow$ &nbsp; $f \circ \gamma(t) = 1$ &nbsp; $\Longrightarrow$ &nbsp; $(f \circ \gamma)'(t) = 0$

        > $\gamma'(t) = \begin{bmatrix} 1 \\ -\sin(t) \\ \cos(t) \end{bmatrix}$, $Df(\vec{a}) = \begin{bmatrix} 0 & 2a^2 & 2a^3 \end{bmatrix}$

        $$
        \begin{aligned}
        \Longrightarrow \quad Df(\gamma(t))(\gamma'(t)) &= \begin{bmatrix} 0 & 2\cos(t) & 2\sin(t) \end{bmatrix} \begin{bmatrix} 1 \\ -\sin(t) \\ \cos(t) \end{bmatrix}\\[4pt]
        &= 0 \cdot 1 + 2\cos(t)(-\sin(t)) + 2\sin(t)\cos(t) = 0.
        \end{aligned}
        $$
        """,
        label="ex-chain-helix",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule along a path
    # corollary: gradient perpendicular to level sets
    lk.corollary(
        [
            r"""
            For $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, $\vec{\nabla} f(\vec{a})$ is perpendicular to level set through $\vec{a}$.
            """,
            lk.gap(),
            lk.aside(
                r"$\leadsto$ &nbsp; suppose $f(\vec{a}) = b$ and suppose $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^n$ has $\gamma(t_0) = \vec{a}$ and $\mk{\mathrm{Im}(\gamma) \subset f^{-1}(b)}$",
                r"that is $f \circ \gamma(t) = b \ \ \forall \, t$",
            ),
            r"> $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a}) \cdot \gamma'(t_0) = Df(\vec{a})(\gamma'(t_0)) = (f \circ \gamma)'(t_0) = 0$",
        ],
        label="cor-gradient-level",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule
    # theorem: chain rule for g o f
    lk.theorem(
        [
            r"""
            <span class="lk-tab" style="--lk-tab: 6.4em">$f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$</span>differentiable at $\vec{x} = \vec{a}$

            <span class="lk-tab" style="--lk-tab: 6.4em">$g : \mathbb{R}^m \longrightarrow \mathbb{R}^p$</span>differentiable at $\vec{y} = \vec{b} = f(\vec{a})$

            > $\Longrightarrow$ &nbsp; $g \circ f : \mathbb{R}^n \longrightarrow \mathbb{R}^p$ differentiable at $\vec{x} = \vec{a}$

            > <span class='lk-ghost'>$\Longrightarrow$ &nbsp; </span>with
            """,
            lk.aside(
                r"""
                $$
                \underbrace{D(g \circ f)(\vec{a})}_{\mathrm{Mat}(p \times n)} = \mk{\underbrace{Dg(f(\vec{a}))}_{\mathrm{Mat}(p \times m)} \, \underbrace{Df(\vec{a})}_{\mathrm{Mat}(m \times n)}}
                $$
                """,
                "matrix multiplication!",
            ),
        ],
        label="thm-chain",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule
    # proof: chain rule for g o f
    lk.proof(
        [
            "Similar idea as the previous theorem",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                &\frac{g \circ f(\vec{x}) - g \circ f(\vec{a}) - Dg(f(\vec{a})) Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert}\\[4pt]
                &= \underbrace{\frac{g \circ f(\vec{x}) - g \circ f(\vec{a}) - Dg(f(\vec{a}))(f(\vec{x}) - f(\vec{a}))}{\lVert f(\vec{x}) - f(\vec{a}) \rVert}}_{\longrightarrow 0} \, \mk{\underbrace{\frac{\lVert f(\vec{x}) - f(\vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert}}_{\substack{\text{does not go}\\ \text{to } +\infty}}}\\[4pt]
                &\qquad + Dg(f(\vec{a})) \left( \underbrace{\frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert}}_{\longrightarrow 0} \right).
                \end{aligned}
                $$
                """,
                "this needs some care…<br>(not here!)",
                rows=3,
                at=2,
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $D(g \circ f)(\vec{a}) = Dg(f(\vec{a})) Df(\vec{a})$ defines a good affine approximation to $g \circ f$ at $\vec{a}$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: chain rule
    # example: g o f with f(x) = (x^1 x^2, x^1 + x^2), g(y) = (y^1)^2 - y^2
    lk.example(
        r"""
        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \end{bmatrix}$, $g\left( \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \right) = (y^1)^2 - y^2$

        > $\Longrightarrow$ &nbsp; $g \circ f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = g\left( \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \end{bmatrix} \right) = (x^1 x^2)^2 - (x^1 + x^2)$

        > $Df(\vec{x}) = \begin{bmatrix} x^2 & x^1 \\ 1 & 1 \end{bmatrix}$, $Dg(\vec{y}) = \begin{bmatrix} 2y^1 & -1 \end{bmatrix}$

        $$
        \begin{aligned}
        \Longrightarrow \quad Dg(f(\vec{x})) Df(\vec{x}) &= \begin{bmatrix} 2x^1 x^2 & -1 \end{bmatrix} \begin{bmatrix} x^2 & x^1 \\ 1 & 1 \end{bmatrix}\\[4pt]
        &= \begin{bmatrix} 2x^1 (x^2)^2 - 1 & 2(x^1)^2 x^2 - 1 \end{bmatrix}.
        \end{aligned}
        $$

        > $D(g \circ f)(\vec{x}) = \begin{bmatrix} 2(x^1 x^2) x^2 - 1 & 2(x^1 x^2) x^1 - 1 \end{bmatrix}$
        """,
        label="ex-chain-matrices",
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
    # exercise: chain rule for an ellipse and a spiral
    lk.exercise(
        r"""
        Consider $\gamma(t) = \begin{bmatrix} 3\cos(t) \\ 2\sin(t) \end{bmatrix}$, $\sigma(t) = t\gamma(t) = \begin{bmatrix} 3t\cos(t) \\ 2t\sin(t) \end{bmatrix}$.

        $f\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = {\large\tfrac{(x^1)^2}{9}} + {\large\tfrac{(x^2)^2}{4}}$ and $g\left( \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \right) = \begin{bmatrix} y^1 \cos(y^2) \\ y^1 \sin(y^2) \end{bmatrix}$

        a) Compute $\gamma'(t)$, $\sigma'(t)$, $\vec{\nabla} f(\vec{x})$ and $Dg(\vec{y})$

        b) Compute $(f \circ \gamma)'(t)$, $(f \circ \sigma)'(t)$ and $D(f \circ g)(\vec{y})$

        > i) via the chain rule

        > ii) directly as maps $f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}$, $f \circ \sigma : \mathbb{R} \longrightarrow \mathbb{R}$, $f \circ g : \mathbb{R}^2 \longrightarrow \mathbb{R}$
        """,
        label="ex-practice",
    )
    return


if __name__ == "__main__":
    app.run()
