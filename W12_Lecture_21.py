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
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False, "savefig.format": "svg"})

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
            arrowprops={"arrowstyle": f"->,head_length={2 * lw:g},head_width={0.87 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    return corollary, LIGHT, BLUE, GREEN, GREY, ORANGE, RED, arrow, definition, header, theorem

@app.cell(hide_code=True)
def _(header):
    header("Lecture 21","Week 12","Lecture 21 • Green's theorem")
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, Figure, arrow, np):
    def lecture_sketch(kind, value=0.5):
        fig = Figure(figsize=(6.6, 3.5))
        ax = fig.add_axes((0.07, 0.08, 0.85, 0.84))
        ax.set_aspect('equal')
        ax.axis('off')
        def label(p, text, color='black', offset=(5,5), ha='left', va='bottom'):
            ax.annotate(text,p,xytext=offset,textcoords='offset points',color=color,fontsize=13,ha=ha,va=va,zorder=10,clip_on=False)
        def axes(xlim,ylim,x='$x$',y='$y$'):
            ax.set_xlim(*xlim);ax.set_ylim(*ylim)
            arrow(ax,(xlim[0],0),(xlim[1]-0.1,0),'black',lw=0.9)
            arrow(ax,(0,ylim[0]),(0,ylim[1]-0.1),'black',lw=0.9)
            label((xlim[1]-0.1,0),x,offset=(0,-18),ha='right')
            label((0,ylim[1]-0.1),y,offset=(-12,0))
        if kind=='partition':
            ax.set_xlim(-0.4,5.5);ax.set_ylim(-0.6,0.7)
            arrow(ax,(-0.2,0),(5.3,0),'black',lw=0.9)
            for i in range(6):
                ax.plot([i,i],[-0.05,0.05],color=GREY,lw=1)
            for i in range(5):
                ax.plot(i+0.4,0,'o',color=BLUE,zorder=5,ms=4)
            for x,t in [(0,'$a=a_1$'),(1,'$b_1=a_2$'),(4,'$a_N$'),(5,'$b_N=b$')]:label((x,0),t,offset=(0,14),ha='center')
            for x,t in [(0.4,'$t_1$'),(1.4,'$t_2$'),(4.4,'$t_N$')]:label((x,0),t,BLUE,offset=(0,-24),ha='center')
            fig.set_size_inches(6.6,1.6)
        elif kind=='rectangle':
            axes((-0.4,4.0),(-0.4,2.9))
            ax.fill([0.7,3,3,0.7],[0.6,0.6,2.2,2.2],color=LIGHT)
            ax.plot([0.7,3,3,0.7,0.7],[0.6,0.6,2.2,2.2,0.6],color=BLUE,lw=1.4)
            for x,t in [(0.7,'$a$'),(3,'$b$')]:
                ax.plot([x,x],[0,2.2],':',color=GREY);label((x,0),t,offset=(0,-18),ha='center')
            for y,t in [(0.6,'$c$'),(2.2,'$d$')]:
                ax.plot([0,3],[y,y],':',color=GREY);label((0,y),t,offset=(-15,0))
            label((2.7,1.3),'$R$',BLUE)
        elif kind in ('simple_regions','green_y','green_x'):
            # Vertical/horizontal slices and the four oriented boundary pieces.
            def region(ax, swap=False, orient=False):
                x=np.linspace(0.7,3.2,180);lo=0.8+0.18*np.sin(4*x);hi=2.2+0.2*np.sin(3*x)
                conv=lambda x,y:(y,x) if swap else (x,y)
                ax.fill(*conv(np.r_[x,x[::-1]],np.r_[lo,hi[::-1]]),color=LIGHT)
                ax.plot(*conv(x,lo),color=BLUE,lw=1.4);ax.plot(*conv(x,hi),color=BLUE,lw=1.4)
                for i in (0,-1):ax.plot(*conv([x[i],x[i]],[lo[i],hi[i]]),color=RED,lw=1.4)
                if orient:
                    for xs,ys,rev,c in [(x,lo,False,BLUE),(x,hi,True,BLUE)]:
                        a,b=85,95
                        if rev:a,b=b,a
                        tail,tip=conv(xs[a],ys[a]),conv(xs[b],ys[b])
                        if swap:tail,tip=tip,tail
                        arrow(ax,tail,tip,c,mutation_scale=2.5)
                    for i,sign in [(0,-1),(-1,1)]:
                        mid=(lo[i]+hi[i])/2
                        a,b=conv(x[i],mid-0.13*sign),conv(x[i],mid+0.13*sign)
                        if swap:a,b=b,a
                        arrow(ax,a,b,RED,mutation_scale=2.5)
                else:
                    k=85
                    ax.plot(*conv([x[k],x[k]],[lo[k],hi[k]]),color=GREEN,lw=1.5)
                    for yy,txt in [(lo[k],r'$\psi_1(y)$' if swap else r'$\varphi_1(x)$'),(hi[k],r'$\psi_2(y)$' if swap else r'$\varphi_2(x)$')]:
                        ax.plot(*conv([0,x[k]],[yy,yy]),':',color=GREY,lw=0.7)
                        ax.plot(*conv(x[k],yy),'o',color=GREEN,zorder=5,ms=3)
                        label(conv(0,yy),txt,GREEN,offset=(0,-23) if swap else (-9,0),ha='center' if swap else 'right')
                    label(conv(x[k],0),'$y$' if swap else '$x$',GREEN,offset=(-14,0) if swap else (0,-20),ha='center')
                if swap:
                    label((1.0,3.4),r'$x=\psi_1(y)$',BLUE,offset=(0,0),ha='center')
                    label((2.7,3.4),r'$x=\psi_2(y)$',BLUE,offset=(0,0),ha='center')
                else:
                    label((1.6,0.25),r'$y=\varphi_1(x)$',BLUE,offset=(0,2),ha='center')
                    label((1.6,2.45),r'$y=\varphi_2(x)$',BLUE,offset=(0,2),ha='center')
                label(conv(2.4,1.4),'$D$',BLUE)
                for p,t in [(conv(0.7,0), '$c$' if swap else '$a$'),(conv(3.2,0),'$d$' if swap else '$b$')]:label(p,t,offset=(-14,0) if swap else (0,-20),ha='center')
            if kind=='simple_regions':
                fig=Figure(figsize=(7.4,3.5));ax=fig.add_axes((0.04,0.12,0.42,0.8));ax.axis('off');ax.set_aspect('equal')
                axes((-0.3,3.8),(-0.3,3.7));region(ax)
                ax=fig.add_axes((0.55,0.12,0.42,0.8));ax.axis('off');ax.set_aspect('equal')
                axes((-0.3,3.8),(-0.3,3.7));region(ax,True)
            else:
                axes((-0.3,3.9),(-0.3,3.9));region(ax,kind=='green_x',True)
        elif kind in ('parabola','parabola_boundary'):
            axes((-1.65,1.65),(-0.25,1.65));x=np.linspace(-1,1,240)
            ax.fill_between(x,x*x,1,color=LIGHT)
            ax.plot(x,x*x,color=BLUE,lw=1.4);ax.plot([-1,1],[1,1],color=RED,lw=1.4)
            label((0.8,0.5),r'$y=x^2$' if kind=='parabola' else r'$\vec C_1$',BLUE)
            label((-0.7,1.04),'$y=1$' if kind=='parabola' else r'$\vec C_2$',RED)
            label((-0.42,0.72),'$D$',BLUE)
            if kind=='parabola_boundary':
                arrow(ax,(0.4,0.16),(0.55,0.55**2),BLUE,mutation_scale=2.5);arrow(ax,(0.4,1),(0.15,1),RED,mutation_scale=2.5)
            else:
                y=value;ax.plot([-np.sqrt(y),np.sqrt(y)],[y,y],color=GREEN,lw=1.4)
        elif kind in ('line_integral','parallel_path'):
            ax.set_xlim(-0.3,5.8);ax.set_ylim(-0.5,3.1)
            t=np.linspace(0,4.8,200);y=0.3*t+0.35*np.sin(1.5*t)
            ax.plot(t,y,color=BLUE,lw=1.4)
            for x,text in [(0,r'$\gamma(a)$'),(4.8,r'$\gamma(b)$')]:
                p=(x,0.3*x+0.35*np.sin(1.5*x));ax.plot(*p,'o',color=BLUE,zorder=5,ms=4);label(p,text,offset=(0,-24),ha='center')
            if kind=='line_integral':
                p=np.array([2.,0.6+0.35*np.sin(3)])
                tangent=p+1.6*np.array([1.,0.3+0.525*np.cos(3)])
                arrow(ax,p,tangent,GREEN,lw=1.7,mutation_scale=2.2)
                label(tangent,r"$\gamma'(t)$",GREEN,offset=(5,-12),va='top')
                arrow(ax,p,p+[0.1,1.3],RED,lw=1.7,mutation_scale=2.2)
                label(p+[0.1,1.3],r'$\vec F(\gamma(t))$',RED,offset=(5,8))
                label(p,r'$\gamma(t)$',BLUE,offset=(0,-25),ha='center')
            else:
                for x,c,txt in [(0,BLUE,'$X_0$'),(2.2,RED,r'$X_{\gamma(t)}$'),(4.8,GREEN,r'$P^\gamma_{a,b}(X_0)$')]:
                    p=np.array([x,0.3*x+0.35*np.sin(1.5*x)])
                    tip=p+[-0.18+0.15*x,0.95]
                    arrow(ax,p,tip,c);label(tip,txt,c,offset=(0,7),ha='center')
        elif kind=='orientation':
            axes((-0.4,3.7),(-0.3,2.7));t=np.linspace(0,2*np.pi,240)
            x=1.7+1.05*np.cos(t);y=1.3+0.85*np.sin(t)
            ax.fill(x,y,color=LIGHT);ax.plot(x,y,color=BLUE,lw=1.4)
            for k in (25,145):arrow(ax,(x[k],y[k]),(x[k+10],y[k+10]),BLUE,mutation_scale=2.5)
            label((1.55,1.2),'$D$',BLUE);label((2.4,2.1),r'$\vec C$',BLUE)
        elif kind=='ellipse':
            axes((-2.8,2.8),(-1.8,1.8));t=np.linspace(0,2*np.pi,250)
            ax.fill(2*np.cos(t),np.sin(t),color=LIGHT);ax.plot(2*np.cos(t),np.sin(t),color=BLUE,lw=1.4)
            for p,txt,off,ha,va in [((2,0),'$a$',(7,5),'left','bottom'),((-2,0),'$-a$',(-7,5),'right','bottom'),((0,1),'$b$',(5,7),'left','bottom'),((0,-1),'$-b$',(5,-7),'left','top')]:
                label(p,txt,BLUE,offset=off,ha=ha,va=va)
        elif kind=='potential_rectangle':
            axes((-0.5,3.4),(-0.4,2.6));ax.fill([0,2.5,2.5,0],[0,0,1.7,1.7],color=LIGHT)
            arrow(ax,(0,0),(2.5,0),BLUE,mutation_scale=2.5);arrow(ax,(2.5,0),(2.5,1.7),BLUE,mutation_scale=2.5)
            arrow(ax,(2.5,1.7),(0,1.7),RED,mutation_scale=2.5);arrow(ax,(0,1.7),(0,0),RED,mutation_scale=2.5)
            for p,t,off,ha,va in [((0,0),'$(0,0)$',(-6,-7),'right','top'),((2.5,0),'$(x,0)$',(6,-7),'left','top'),((2.5,1.7),'$(x,y)$',(6,7),'left','bottom'),((0,1.7),'$(0,y)$',(-6,7),'right','bottom')]:
                label(p,t,offset=off,ha=ha,va=va)
            label((1,-0.3),r'$\vec C_1$',BLUE,offset=(0,-6));label((0.8,1.85),r'$\vec C_2$',RED);label((1.1,0.8),'$R$',BLUE)
        elif kind in ('fixed_interval','moving_interval'):
            fig.set_size_inches(6.6,1.7);ax.set_aspect('auto');ax.set_xlim(-10,110);ax.set_ylim(-0.6,0.7)
            arrow(ax,(-5,0),(105,0),'black',lw=0.9)
            centre=50 if kind=='fixed_interval' else value
            for x in (centre-19.6,centre+19.6):ax.plot([x,x],[-0.08,0.08],color=BLUE,lw=1.4)
            ax.plot([centre-19.6,centre+19.6],[0,0],color=BLUE,lw=2)
            mean=56 if kind=='fixed_interval' else value
            ax.plot(mean,0,'o',color=GREEN,zorder=5,ms=5);ax.plot(50,0,'o',color=RED,zorder=5,ms=4)
            for x,t,c in [(50,r'$\mu$',RED),(mean,r'$M_4$',GREEN)]:label((x,0),t,c,offset=(0,-26 if c==RED else 16),ha='center')
            for sign in (-1,1):label((centre+sign*19.6,0),('$\\mu' if kind=='fixed_interval' else '$M_4')+(' - ' if sign<0 else ' + ')+r'\varepsilon$',BLUE,offset=(0,16),ha='center')
        elif kind in ('schwarzschild_domain','static_clock','newton_force'):
            axes((-1.8,4.3),(-0.7,3.9),x='$r$',y=r'$\tau$' if kind=='newton_force' else '$t$')
            if kind=='static_clock':
                ax.plot([0.9,0.9],[-0.2,3.5],':',color=GREY)
                ax.plot([1.7,1.7],[-0.2,3.5],color=BLUE,lw=1.4)
                arrow(ax,(3,0.6),(3,3),GREEN)
                for p,t,c in [((0.9,0),'$2M$',GREY),((1.7,0),'$r_0$',BLUE),((3,0),'$r$',GREEN)]:label(p,t,c,offset=(0,-22),ha='center')
                for p,t in [((3,0.6),r'$\gamma(a)$'),((3,2.7),r'$\gamma(b)$')]:ax.plot(*p,'o',color=GREEN,zorder=5,ms=4);label(p,t,GREEN)
            else:
                for x in (-1.2,1.2):ax.plot([x,x],[-0.4,3.6],color=BLUE,lw=1.2)
                t=np.linspace(0,2*np.pi,160);ax.plot(1.2*np.cos(t),0.35*np.sin(t),color=BLUE,lw=1.2)
                label((1.2,0),'$r_0$',BLUE,offset=(0,-22));label((-1.2,-0.3),r'$\mathbb{S}^2$' if kind=='schwarzschild_domain' else r'$\sigma(\tau)=o+\tau e_0$',BLUE,offset=(-5,-20))
                if kind=='newton_force':
                    t=np.linspace(-0.3,3.5,140);r=2.1+0.6*np.sin(1.2*t);ax.plot(r,t,color=RED,lw=1.4)
                    arrow(ax,(2.7,1.3),(1.7,1.3),GREEN,r'$F(\gamma(\tau))$',at_tip=True)
                    label((2.5,3),r'$\gamma(\tau)$',RED)
                else:label((2.7,2.7),'$M$',BLUE)
        elif kind in ('newton_orbits','precession'):
            axes((-3,2) if kind=='newton_orbits' else (-2.6,2.6),(-2.4,2.4) if kind=='newton_orbits' else (-2.6,2.6),x='',y='');ax.plot(0,0,'o',color=GREY,zorder=5,ms=13)
            if kind=='newton_orbits':
                for e,c in [(0.55,BLUE),(1.,RED),(1.4,GREEN)]:
                    t=np.linspace(-np.pi,np.pi,1600);den=1+e*np.cos(t);ok=den>0.06;r=1/den[ok];t=t[ok]
                    xx,yy=r*np.cos(t),r*np.sin(t); visible=(xx>=-3)&(xx<=2)&(abs(yy)<=2.4)
                    ax.plot(np.where(visible,xx,np.nan),np.where(visible,yy,np.nan),color=c,lw=1.4,label=f'$e={e:g}$')
                ax.legend(loc='upper left',bbox_to_anchor=(1.0,1.0),fontsize=12,frameon=True,fancybox=False,edgecolor='#c8c8c8')
            else:
                fig.set_size_inches(6.6,4.4);ax.set_xlim(-2.6,2.6);ax.set_ylim(-2.6,2.6)
                t=np.linspace(0,16*np.pi/(1-3*value**2),6000);r=1/(1+0.55*np.cos((1-3*value**2)*t))
                ax.plot(r*np.cos(t),r*np.sin(t),color=BLUE,lw=1.4)
                peri=2*np.pi*np.arange(9)/(1-3*value**2)
                ax.plot(np.cos(peri)/1.55,np.sin(peri)/1.55,'o',color=BLUE,zorder=5,ms=3)
                theta=0.8;r0=1/(1+0.55*np.cos((1-3*value**2)*theta));tip=(r0*np.cos(theta),r0*np.sin(theta))
                arrow(ax,(0,0),tip,GREEN,mutation_scale=1)
                label(tip,r'$r(\theta)$',GREEN,offset=(8,9))
        elif kind=='light_bending':
            axes((-3.5,3.5),(-1,2),x='',y='');ax.plot(0,0,'o',color=GREY,zorder=5,ms=16)
            ax.plot([-3.2,3.2],[1,1],color=RED,lw=1.4);label((2.2,1.05),'$M=0$',RED)
            q=0.06;t=np.linspace(-0.08,np.pi+0.08,1500);r=1/(np.sin(t)+q*(1+np.cos(t)**2));x=r*np.cos(t);y=r*np.sin(t);ok=abs(x)<3.2
            ax.plot(x[ok],y[ok],color=BLUE,lw=1.4);label((3.2,float(y[ok][np.argmax(x[ok])])),'$M>0$',BLUE,offset=(0,8),ha='right')
            arrow(ax,(-2.3,1),(-1.8,1),RED,mutation_scale=1)
            _ix=np.argsort(x[ok]);_xx=x[ok][_ix];_yy=y[ok][_ix]
            arrow(ax,(-2.3,float(np.interp(-2.3,_xx,_yy))),(-1.9,float(np.interp(-1.9,_xx,_yy))),BLUE,mutation_scale=1)
            ax.plot([0.18,0.18],[0,1],':',color=GREEN,lw=1)
            label((0.18,0.42),'$L/E$',GREEN,offset=(7,0))
            for x,t in [((-2.5,0.2),r'$2ME/L$'),((2.5,0.2),r'$-2ME/L$')]:label(x,t,BLUE,offset=(0,0),ha='center')
        elif kind=='loop':
            ax.set_xlim(-1,4.8);ax.set_ylim(-0.5,3.6)
            p=np.array([0.,0.]);q=np.array([2.6,0.]);r=np.array([3.5,2.]);s=np.array([0.9,2.])
            pts=[p,q,r,s,p]
            for i in range(4):
                arrow(ax,pts[i],pts[i+1],GREY,mutation_scale=1)
                label((pts[i]+pts[i+1])/2,f'$\\gamma_{i+1}$',GREY,offset=[(0,-22),(15,0),(0,12),(-34,12)][i],ha=['center','left','center','right'][i])
            for pt,delta,txt,c in [(p,[0.15,0.8],'$Z_p$',RED),(q,[0.05,0.9],'$Z_1$',RED),(r,[-0.1,0.8],'$Z_2$',RED),(s,[-0.35,0.72],'$Z_3$',RED),(p,[-0.5,0.65],'$Z_4$',BLUE)]:
                tip=pt+delta;arrow(ax,pt,tip,c);label(tip,txt,c,offset=(0,6),ha='center')
            for pt,txt,off in [(p,'$p$',(-12,-14)),(q,r'$\varepsilon X$',(3,-18)),(r,r'$\varepsilon X+\delta Y$',(3,-18)),(s,r'$\delta Y$',(-24,-18))]:label(pt,txt,offset=off)
        else:
            raise ValueError(kind)
        return fig
    return (lecture_sketch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Double integration over simple regions in $\mathbb R^2$.

    A region $D\subseteq\mathbb R^2$ is called $y$-simple if

    $$
    D=\{(x,y)\in\mathbb R^2\mid a\le x\le b,\ \varphi_1(x)\le y\le\varphi_2(x)\}
    $$

    for $\varphi_1,\varphi_2:[a,b]\to\mathbb R$ continuous, with $\varphi_1\le\varphi_2$.

    $$
    \leadsto\quad\iint_D f(x,y)\,dx\,dy
    =\int_a^b\left(\int_{\varphi_1(x)}^{\varphi_2(x)}f(x,y)\,dy\right)dx.
    $$

    $D$ is $x$-simple if

    $$
    D=\{(x,y)\in\mathbb R^2\mid c\le y\le d,\ \psi_1(y)\le x\le\psi_2(y)\}
    $$

    for $\psi_1,\psi_2:[c,d]\to\mathbb R$ continuous, with $\psi_1\le\psi_2$.

    $$
    \leadsto\quad\iint_D f(x,y)\,dx\,dy
    =\int_c^d\left(\int_{\psi_1(y)}^{\psi_2(y)}f(x,y)\,dx\right)dy.
    $$

    Earlier: line integrals of vector fields over curves

    $$
    \int_{\vec C}\vec F\cdot d\vec s
    =\int_a^b\vec F(\gamma(t))\cdot\gamma'(t)\,dt,
    \qquad C=\gamma([a,b]).
    $$
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('line_integral')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \text{FTC}\quad\Longrightarrow\quad
    \int_{\vec C}\nabla f\cdot d\vec s=f(\gamma(b))-f(\gamma(a)).
    $$

    **In this lecture:** Green's theorem

    $\leadsto$ &nbsp; relation between double integrals over simple regions and line integrals over their boundary curve!

    ## IV.5 &nbsp; Green's theorem
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    Given $D\subseteq\mathbb R^2$ a simple region, let $C=\operatorname{Bd}(D)$ denote its boundary points. We denote by $\vec C$ the curve $C$ with the **counterclockwise orientation**.

    $\leadsto$ &nbsp; walking around $\vec C$, $D$ is always on the left.

    We denote by $\vec C^{\mathrm{op}}$ the curve $C$ with the opposite orientation (clockwise).

    $\leadsto$ &nbsp; $D$ is always on the right.

    We also call counterclockwise orientation **positive orientation**, and clockwise orientation **negative orientation**.
    """,'')
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('orientation')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    Given a simple region $D\subset\mathbb R^2$ (both $y$-simple and $x$-simple) with piecewise smooth boundary, $\vec C=\operatorname{Bd}(D)$ with positive orientation, and

    $$
    \vec F(x,y)=\begin{bmatrix}P(x,y)\\Q(x,y)\end{bmatrix}
    $$

    a $C^1$-smooth vector field on a neighborhood of $D$,

    $$
    \int_{\vec C}\vec F\cdot d\vec s
    =\iint_D\left(\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)\right)dx\,dy.
    $$

    <span class="math-notes"><span>$\displaystyle \text{line integral over the boundary} = \text{double integral of the scalar curl of }\vec F$</span></span>

    $\leadsto$ &nbsp; generalization of FTC!
    """,'Green')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.**

    $$
    D=\{(x,y)\mid x^2\le y\le1\},\qquad
    \vec F(x,y)=\begin{bmatrix}-y^2\\xy\end{bmatrix}.
    $$

    $$
    \begin{aligned}
    C=\operatorname{Bd}(D)
    &=\{(x,y)\mid-1\le x\le1,\ y=x^2\}\\
    &\qquad\cup\{(x,y)\mid-1\le x\le1,\ y=1\}.
    \end{aligned}
    $$

    <span class="math-notes"><span>$\displaystyle \{(x,y)\mid-1\le x\le1,\ y=x^2\}=C_1$</span><span>$\displaystyle \{(x,y)\mid-1\le x\le1,\ y=1\}=C_2$</span></span>

    $$
    \vec C:\quad(t,t^2),\ t\in[-1,1],
    \qquad\text{then}\qquad(-t,1),\ t\in[-1,1].
    $$

    <span class="math-notes"><span>$\displaystyle (t,t^2)=\gamma_1(t)$</span><span>$\displaystyle (-t,1)=\gamma_2(t)$</span></span>
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('parabola_boundary')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \int_{\vec C}\vec F\cdot d\vec s
    =\int_{\vec C_1}\vec F\cdot d\vec s+\int_{\vec C_2}\vec F\cdot d\vec s$ $\displaystyle =\int_{-1}^1\begin{bmatrix}-t^4\\t^3\end{bmatrix}\cdot\begin{bmatrix}1\\2t\end{bmatrix}dt
    +\int_{-1}^1\begin{bmatrix}-1\\-t\end{bmatrix}\cdot\begin{bmatrix}-1\\0\end{bmatrix}dt$ $\displaystyle =\int_{-1}^1(-t^4+2t^4)\,dt+\int_{-1}^1(1+0)\,dt
    =\frac25+2=\frac{12}{5}.$</span>

    <span class="chain">$\displaystyle \iint_D\Bigl(\frac{\partial Q}{\partial x}(x,y)
    -\frac{\partial P}{\partial y}(x,y)\Bigr)dx\,dy
    =\iint_D3y\,dx\,dy$ $\displaystyle =3\int_{-1}^1\left(\int_{x^2}^1y\,dy\right)dx
    =3\int_{-1}^1\left(\frac12-\frac{x^4}{2}\right)dx$ $\displaystyle =3\left[\frac x2-\frac{x^5}{10}\right]_{x=-1}^{x=1}
    =3\left(\frac22-\frac2{10}\right)=3\cdot\frac45.$</span>

    <span class="math-notes"><span>$\displaystyle \frac{\partial Q}{\partial x}(x,y)=y$</span><span>$\displaystyle \frac{\partial P}{\partial y}(x,y)=-2y$</span></span>

    **Proof.** Write

    $$
    \vec F(x,y)=\begin{bmatrix}P(x,y)\\Q(x,y)\end{bmatrix}
    =\begin{bmatrix}P(x,y)\\0\end{bmatrix}
    +\begin{bmatrix}0\\Q(x,y)\end{bmatrix}.
    $$

    <span class="math-notes"><span>$\displaystyle \begin{bmatrix}P(x,y)\\0\end{bmatrix}=\vec F_1(x,y)$</span><span>$\displaystyle \begin{bmatrix}0\\Q(x,y)\end{bmatrix}=\vec F_2(x,y)$</span></span>

    $$
    \Longrightarrow\quad\int_{\vec C}\vec F\cdot d\vec s
    =\int_{\vec C}\vec F_1\cdot d\vec s+\int_{\vec C}\vec F_2\cdot d\vec s.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For $\vec F_1=\begin{bmatrix}P\\0\end{bmatrix}$, treat $D$ as a $y$-simple region:

    $$
    D=\{(x,y)\mid a\le x\le b,\ \varphi_1(x)\le y\le\varphi_2(x)\}.
    $$

    <span class="chain">
    $\displaystyle\operatorname{Bd}(D)=\{(x,\varphi_1(x))\mid x\in[a,b]\}\ \cup\{(b,y)\mid y\in[\varphi_1(b),\varphi_2(b)]\}$
    $\displaystyle\cup\{(x,\varphi_2(x))\mid x\in[a,b]\}\ \cup\{(a,y)\mid y\in[\varphi_1(a),\varphi_2(a)]\}.$
    </span>
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('green_y')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{aligned}
    \int_{\vec C}\vec F_1\cdot d\vec s
    &=\int_a^b\begin{bmatrix}P(t,\varphi_1(t))\\0\end{bmatrix}\cdot\begin{bmatrix}1\\\varphi'_1(t)\end{bmatrix}dt
    +\int_{\varphi_1(b)}^{\varphi_2(b)}\begin{bmatrix}P(b,t)\\0\end{bmatrix}\cdot\begin{bmatrix}0\\1\end{bmatrix}dt\\[4pt]
    &\quad-\int_a^b\begin{bmatrix}P(t,\varphi_2(t))\\0\end{bmatrix}\cdot\begin{bmatrix}1\\\varphi'_2(t)\end{bmatrix}dt
    -\int_{\varphi_1(a)}^{\varphi_2(a)}\begin{bmatrix}P(a,t)\\0\end{bmatrix}\cdot\begin{bmatrix}0\\1\end{bmatrix}dt.
    \end{aligned}
    $$

    Here we need $\varphi_1,\varphi_2$ piecewise differentiable; the last two parametrizations have opposite orientation.

    <span class="chain">$\displaystyle \Longrightarrow\quad\int_{\vec C}\vec F_1\cdot d\vec s
    =\int_a^b\bigl(P(x,\varphi_1(x))-P(x,\varphi_2(x))\bigr)dx$ $\displaystyle =\int_a^b\left(\int_{\varphi_2(x)}^{\varphi_1(x)}\frac{\partial P}{\partial y}(x,y)\,dy\right)dx$ $\displaystyle =-\int_a^b\left(\int_{\varphi_1(x)}^{\varphi_2(x)}\frac{\partial P}{\partial y}(x,y)\,dy\right)dx$ $\displaystyle =-\iint_D\frac{\partial P}{\partial y}(x,y)\,dx\,dy.$</span>

    Similarly, for $\vec F_2=\begin{bmatrix}0\\Q\end{bmatrix}$, treat $D$ as $x$-simple:

    $$
    D=\{(x,y)\mid c\le y\le d,\ \psi_1(y)\le x\le\psi_2(y)\}.
    $$

    <span class="chain">
    $\displaystyle\operatorname{Bd}(D)=\{(x,c)\mid x\in[\psi_1(c),\psi_2(c)]\}\ \cup\{(\psi_2(y),y)\mid y\in[c,d]\}$
    $\displaystyle\cup\{(x,d)\mid x\in[\psi_1(d),\psi_2(d)]\}\ \cup\{(\psi_1(y),y)\mid y\in[c,d]\}.$
    </span>
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('green_x')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \Longrightarrow\quad\int_{\vec C}\vec F_2\cdot d\vec s
    =\int_c^d\bigl(Q(\psi_2(y),y)-Q(\psi_1(y),y)\bigr)dy$ $\displaystyle =\int_c^d\left(\int_{\psi_1(y)}^{\psi_2(y)}\frac{\partial Q}{\partial x}(x,y)\,dx\right)dy$ $\displaystyle =\iint_D\frac{\partial Q}{\partial x}(x,y)\,dx\,dy.$</span>

    $$
    \Longrightarrow\quad\int_{\vec C}\vec F\cdot d\vec s
    =\int_{\vec C}(\vec F_1+\vec F_2)\cdot d\vec s
    =\iint_D\left(\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)\right)dx\,dy.\quad\square
    $$

    **Example.** $D=\{(x,y)\mid x^2/a^2+y^2/b^2\le1\}$, $a,b>0$ &nbsp; $\leadsto$ &nbsp; inside an ellipse.
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('ellipse')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \iint_D1\,dx\,dy
    =\int_{-a}^a\left(\int_{-b\sqrt{1-x^2/a^2}}^{b\sqrt{1-x^2/a^2}}1\,dy\right)dx$ $\displaystyle =\int_{-a}^a2b\sqrt{1-x^2/a^2}\,dx=\cdots\quad\text{trig. substitution}.$</span>

    $$
    =\iint_D\left(\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)\right)dx\,dy
    \qquad\leadsto\quad\text{might make life easier!}
    $$

    <span class="math-notes"><span>$\displaystyle \left(\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)\right)=1\text{ for some }\vec F=\left[\begin{smallmatrix}P\\Q\end{smallmatrix}\right]$</span></span>

    Consider $\vec F(x,y)=\dfrac12\begin{bmatrix}-y\\x\end{bmatrix}$.

    $$
    \Longrightarrow\quad\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}
    =\frac12(1+1)=1!
    $$

    $$
    \Longrightarrow\quad\iint_D1\,dx\,dy=\int_{\vec C}\vec F\cdot d\vec s,
    \qquad\gamma(t)=\begin{bmatrix}a\cos t\\b\sin t\end{bmatrix},\quad t\in[0,2\pi].
    $$

    <span class="chain">$\displaystyle =\int_0^{2\pi}\frac12\begin{bmatrix}-b\sin t\\a\cos t\end{bmatrix}\cdot\begin{bmatrix}-a\sin t\\b\cos t\end{bmatrix}dt$ $\displaystyle =\frac12\int_0^{2\pi}ab\,dt=ab\pi.$</span>

    $\leadsto$ &nbsp; if $a=b=r$, then $\displaystyle\iint_Ddx\,dy=r^2\pi$!

    $\leadsto$ &nbsp; consequence for gradient vector fields.
    """)
    return


@app.cell(hide_code=True)
def _(corollary):
    corollary(r"""
    Given a vector field $\vec F(x,y)=\begin{bmatrix}P(x,y)\\Q(x,y)\end{bmatrix}$, $C^1$-smooth over the whole plane $\mathbb R^2$, and with zero scalar curl

    $$
    \frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)=0,
    $$

    then $\vec F(x,y)$ is a conservative vector field with potential function

    $$
    f(x,y)=\int_0^xP(t,0)\,dt+\int_0^yQ(x,t)\,dt.
    $$
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof.** Consider a rectangle $R=[0,x]\times[0,y]$ (first $x,y>0$).
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('potential_rectangle')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \text{Green}\quad\Longrightarrow\quad
    \int_{\vec C}\vec F\cdot d\vec s
    =\iint_R\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dx\,dy
    =0=\int_{\vec C_1}\vec F\cdot d\vec s+\int_{\vec C_2}\vec F\cdot d\vec s.
    $$

    $$
    C=\operatorname{Bd}(R)=C_1\cup C_2.
    $$

    <span class="chain">$\displaystyle \int_{\vec C_1}\vec F\cdot d\vec s
    =\int_0^x\begin{bmatrix}P(t,0)\\Q(t,0)\end{bmatrix}\cdot\begin{bmatrix}1\\0\end{bmatrix}dt
    +\int_0^y\begin{bmatrix}P(x,t)\\Q(x,t)\end{bmatrix}\cdot\begin{bmatrix}0\\1\end{bmatrix}dt$ $\displaystyle =\int_0^xP(t,0)\,dt+\int_0^yQ(x,t)\,dt=f(x,y),$</span>

    <span class="chain">$\displaystyle \int_{\vec C_2}\vec F\cdot d\vec s
    =-\int_0^y\begin{bmatrix}P(0,t)\\Q(0,t)\end{bmatrix}\cdot\begin{bmatrix}0\\1\end{bmatrix}dt
    -\int_0^x\begin{bmatrix}P(t,y)\\Q(t,y)\end{bmatrix}\cdot\begin{bmatrix}1\\0\end{bmatrix}dt$ $\displaystyle =-\int_0^yQ(0,t)\,dt-\int_0^xP(t,y)\,dt=-f(x,y).$</span>

    $$
    \leadsto\quad\text{FTC}:\qquad\frac{\partial f}{\partial x}(x,y)=P(x,y),\qquad\frac{\partial f}{\partial y}(x,y)=Q(x,y).
    $$

    For other signs of $x,y$, use oriented integration limits. $\square$

    **Example.**

    $$
    \vec F(x,y)=\begin{bmatrix}2xy\\x^2+3y^2\end{bmatrix}
    \quad\leadsto\quad\frac{\partial Q}{\partial x}(x,y)-\frac{\partial P}{\partial y}(x,y)=2x-2x=0.
    $$

    $C^1$-smooth everywhere!

    $$
    \Longrightarrow\quad\vec F(x,y)=\nabla f(x,y)\quad\text{for}
    $$

    <span class="chain">$\displaystyle f(x,y)=\int_0^xP(t,0)\,dt+\int_0^yQ(x,t)\,dt$ $\displaystyle =\int_0^x2t\cdot0\,dt+\int_0^y(x^2+3t^2)\,dt=x^2y+y^3,$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    or

    <span class="chain">$\displaystyle f(x,y)=\int_0^yQ(0,t)\,dt+\int_0^xP(t,y)\,dt$ $\displaystyle =\int_0^y(0+3t^2)\,dt+\int_0^x2ty\,dt=y^3+x^2y!$</span>

    **Remark.** $\displaystyle\vec H(x,y)=\frac1{x^2+y^2}\begin{bmatrix}-y\\x\end{bmatrix}$ has zero scalar curl, but is not a gradient!

    Not $C^1$-smooth at $(0,0)$ &nbsp; $\Longrightarrow$ &nbsp; Green's theorem does not apply across the origin!

    ### Practice

    ① &nbsp; $D$ is the triangle with corners $(0,0),(2,0),(1,1)$.

     a) Parametrize $\operatorname{Bd}(D)$ with positive orientation.

     b) Compute the line integral of $\vec F(x,y)=\begin{bmatrix}y^2\\3xy\end{bmatrix}$ over $\operatorname{Bd}(D)$.

     c) Compute $\displaystyle\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dx\,dy$ with Fubini's theorem.

    ② &nbsp; Let $\vec G(x,y)=\begin{bmatrix}e^y\\xe^y+2y\end{bmatrix}$.

     a) Check that the scalar curl is zero.

     b) Compute a potential function for $\vec G(x,y)$.
    """)
    return


if __name__ == "__main__":
    app.run()
