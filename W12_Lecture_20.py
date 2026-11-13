import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title='BS101 • Lecture 20 • Double integrals', css_file="bs101.css")

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
    header("Lecture 20","Week 12","Lecture 20 • Double integrals")
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
def _(mo, np):
    # ---- Interactive 3D figures ------------------------------------------
    # Drawn in the browser on canvases, in the style of the static figures: orthographic views of
    # R^3 (x towards the viewer, y to the right, z up), surfaces drawn back to front.
    # Dragging turns the view at a fixed scale (all panels of a figure together) and a double click restores
    # it; a figure redrawn by a slider keeps its view. Names sit beside the objects they name. Typesetting is done
    # by KaTeX.
    import html as _html
    import json as _json

    _PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" onload="window.typeset && typeset()"></script>
    <style>
      html, body { margin: 0; padding: 0; background: transparent; overflow: hidden;
                   font-family: KaTeX_Main, "Latin Modern Roman", Georgia, serif; }
      #o { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 4px 16px; }
      #g { position: relative; flex: 1 1 300px; min-width: 240px; max-width: var(--maxw); display: grid;
           grid-template-columns: repeat(var(--cols), minmax(0, 1fr)); gap: 6px 14px; touch-action: none; cursor: grab;
           user-select: none; -webkit-user-select: none; }
      @media (max-width: 520px) { #g { grid-template-columns: minmax(0, 1fr); } }
      #g.drag { cursor: grabbing; }
      .p { position: relative; }
      .p canvas { display: block; width: 100%; }
      .cap { text-align: center; font-size: 14px; }
      .lab { position: absolute; left: 0; top: 0; white-space: nowrap; line-height: 1.1; pointer-events: none; font-size: 15px; }
      .katex { font-size: 1em; }
      #lg { flex: 0 0 auto; border: 1px solid #c8c8c8; border-radius: 4px; padding: 4px 10px; background: #fff; font-size: 14px; }
      #lg:empty { display: none; }
      .it { display: flex; align-items: center; gap: 8px; margin: 4px 0; white-space: nowrap; }
      .it svg { flex: 0 0 24px; }
      #hint { position: absolute; right: 0; bottom: 0; color: #888; opacity: 0.7; font: 15px Georgia, serif; }
    </style></head><body>
    <div id="o"><div id="g" role="img"><div id="hint">&#10227;</div></div><div id="lg"></div></div>
    <script>
    // the scene is not in this page but in an element of the notebook beside the frame (or, for a figure with a slider,
    // in the slider's cell), which a slider changes: the page then redraws in place and the frame is never rebuilt
    const box = window.frameElement.closest(".bs3d"), P = window.parent.document;
    const find = () => box.querySelector("[data-scene]") || P.querySelector('[data-bs3d="' + window.frameElement.dataset.bs3d + '"]');
    (function start() { const h = find(); if (h) main(h.dataset.scene); else setTimeout(start, 50); })();
    function main(shown) {
      let S = JSON.parse(shown);
      const RAD = Math.PI / 180, L = [0.3, -0.4, 0.87];
      const lit = [247, 251, 255], dark = [201, 223, 244], lit2 = [219, 235, 251], dark2 = [163, 194, 230];
      const rgb = (a, b, k) => "rgb(" + [0, 1, 2].map((i) => Math.round(a[i] + (b[i] - a[i]) * k)).join(",") + ")";
      const texs = [];
      const tex = (el, t) => { el.dataset.tex = t; el.textContent = t.replace(/\\[a-z]+\{?|[{}$^_]/gi, ""); texs.push(el); };
      const dot3 = (u, p) => u[0] * p[0] + u[1] * p[1] + u[2] * p[2];

      class Scene {
        constructor(spec, host) {
          const ys = (this.ys = spec.ys);
          this.box = document.createElement("div");
          this.box.className = "p";
          this.cv = document.createElement("canvas");
          this.box.appendChild(this.cv);
          this.g = this.cv.getContext("2d");
          host.appendChild(this.box);
          if (spec.caption) {
            const c = document.createElement("div");
            c.className = "cap";
            tex(c, spec.caption);
            this.box.appendChild(c);
          }
          const pts = (this.pts = []), quads = (this.quads = []), segs = (this.segs = []);
          this.dots = []; this.heads = []; this.labs = [];
          const add = (x, y, z) => (pts.push(x, y, z), pts.length / 3 - 1);
          for (const s of spec.surfaces) {
            const base = pts.length / 3, n = s.n, m = s.m, id = (i, j) => base + i * m + j;
            for (const v of s.v) pts.push(v);
            const P = (k) => [pts[3 * k], pts[3 * k + 1], pts[3 * k + 2]];
            const inTint = (x1, x2) => s.tint && x1 > s.tint[0] && x1 <= s.tint[1] && x2 > s.tint[2] && x2 <= s.tint[3];
            const sLit = s.tone ? s.tone.map((c) => Math.round(0.06 * c + 0.94 * 255)) : lit;
            const sDark = s.tone ? s.tone.map((c) => Math.round(0.3 * c + 0.7 * 255)) : dark;
            for (let i = 0; i < n - 1; i++) for (let j = 0; j < m - 1; j++) {
              const q = [id(i, j), id(i + 1, j), id(i + 1, j + 1), id(i, j + 1)];
              const v = q.map(P);
              if (v.some((p) => p.some(isNaN))) continue;
              const deep = inTint((v[0][0] + v[2][0]) / 2, (v[0][1] + v[2][1]) / 2);
              let col = s.flat;
              if (!col) {
                const a = [0, 1, 2].map((t) => v[2][t] - v[0][t]), b = [0, 1, 2].map((t) => v[3][t] - v[1][t]);
                const nn = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
                const len = Math.hypot(...nn) || 1;
                const k = Math.min(1, Math.abs((nn[0] * L[0] + nn[1] * L[1] + nn[2] * L[2]) / len) / 1.0034);
                col = deep ? rgb(dark2, lit2, k) : rgb(sDark, sLit, k);
              }
              quads.push([q, col, deep ? 1 : s.alpha]);
            }
            for (const [axis, every, c, lw] of s.wire || []) {
              const rows = axis === 0 ? n : m, cols = axis === 0 ? m : n;
              for (let r = 0; r < rows; r++) {
                if (r % every !== 0 && r !== rows - 1) continue;
                for (let t = 0; t < cols - 1; t++) {
                  const a = axis === 0 ? id(r, t) : id(t, r), b = axis === 0 ? id(r, t + 1) : id(t + 1, r);
                  const pa = P(a), pb = P(b);
                  if (pa.concat(pb).some(isNaN)) continue;
                  if (s.clear && inTint((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)) continue;
                  segs.push({ a, b, c, lw, line: null });
                }
              }
            }
          }
          this.lines = spec.lines.map((ln) => {
            const idx = [];
            for (let k = 0; k < ln.p.length; k += 3) idx.push(add(ln.p[k], ln.p[k + 1], ln.p[k + 2]));
            const line = { idx, dash: ln.d, cum: new Float64Array(idx.length) };
            for (let k = 0; k < idx.length - 1; k++)
              if (![ln.p[3 * k], ln.p[3 * k + 3]].some(isNaN)) segs.push({ a: idx[k], b: idx[k + 1], c: ln.c, lw: ln.w, line, k, e: ln.e || 0, flat: ln.b });
            return line;
          });
          for (const d of spec.points) this.dots.push({ i: add(...d.p), c: d.c, r: d.r, h: d.h });
          for (const h of spec.heads) this.heads.push({ i: add(...h.p), j: add(...h.q), c: h.c, w: h.w, d: h.d });
          // the centre of the scene and the radius of a ball holding it, heights at their drawing scale
          let src = pts;
          if (spec.box) {
            src = [];
            for (const p of [0, 1]) for (const q of [0, 1]) for (const t of [0, 1]) src.push(spec.box[0][p], spec.box[1][q], spec.box[2][t]);
          }
          const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
          for (let k = 0; k < src.length; k++) {
            const t = k % 3, v = src[k] * (t === 2 ? ys : 1);
            if (!isNaN(v)) { lo[t] = Math.min(lo[t], v); hi[t] = Math.max(hi[t], v); }
          }
          const C = [0, 1, 2].map((t) => (lo[t] + hi[t]) / 2);
          let R = 0;
          for (let k = 0; k < src.length; k += 3) {
            const d = Math.hypot(src[k] - C[0], src[k + 1] - C[1], src[k + 2] * ys - C[2]);
            if (!isNaN(d)) R = Math.max(R, d);
          }
          C[2] /= ys;
          this.C = C;
          this.R = R;
          for (const l of spec.labels) {
            const el = document.createElement("div");
            el.className = "lab";
            el.style.color = l.c;
            tex(el, l.t);
            this.box.appendChild(el);
            this.labs.push({ el, i: add(...l.p), a: l.a * RAD, r: l.r });
          }
          const M = pts.length / 3;
          this.X = new Float64Array(M); this.Y = new Float64Array(M); this.Z = new Float64Array(M);
        }

        size(W, H, R) {
          this.W = W; this.H = H;
          this.sc = 0.94 * Math.min(W, H) / (2 * R);
          const dpr = window.devicePixelRatio || 1;
          this.cv.width = Math.round(W * dpr);
          this.cv.height = Math.round(H * dpr);
          this.cv.style.height = H + "px";
          this.g.setTransform(dpr, 0, 0, dpr, 0, 0);
        }

        draw(az, el) {
          const { g, pts, X, Y, Z, W, H, sc, ys } = this;
          if (!W) return;
          const a = az * RAD, e = el * RAD;
          const r = [-Math.sin(a), Math.cos(a), 0];
          const u = [-Math.sin(e) * Math.cos(a), -Math.sin(e) * Math.sin(a), Math.cos(e) * ys];
          const d = [Math.cos(e) * Math.cos(a), Math.cos(e) * Math.sin(a), Math.sin(e) * ys];
          const tx = W / 2 - dot3(r, this.C) * sc, ty = H / 2 + dot3(u, this.C) * sc;
          for (let k = 0; k < X.length; k++) {
            const x = pts[3 * k], y = pts[3 * k + 1], z = pts[3 * k + 2];
            X[k] = (x * r[0] + y * r[1] + z * r[2]) * sc + tx;
            Y[k] = ty - (x * u[0] + y * u[1] + z * u[2]) * sc;
            Z[k] = x * d[0] + y * d[1] + z * d[2];
          }
          for (const ln of this.lines) {  // screen length along each line, so that dashes run on across segments
            ln.cum[0] = 0;
            for (let k = 1; k < ln.idx.length; k++) {
              const p = ln.idx[k - 1], q = ln.idx[k];
              ln.cum[k] = ln.cum[k - 1] + (isNaN(X[p] + X[q]) ? 0 : Math.hypot(X[q] - X[p], Y[q] - Y[p]));
            }
          }
          const items = [], bias = S.bias;
          for (const q of this.quads) items.push([(Z[q[0][0]] + Z[q[0][1]] + Z[q[0][2]] + Z[q[0][3]]) / 4, 0, q]);
          for (const s of this.segs) items.push([(Z[s.a] + Z[s.b]) / 2 + bias + (s.e || 0), 1, s]);
          for (const h of this.heads) items.push([Z[h.i] + bias, 2, h]);
          for (const p of this.dots) items.push([Z[p.i] + 2 * bias, 3, p]);
          items.sort((p, q) => p[0] - q[0]);
          g.clearRect(0, 0, W, H);
          g.lineJoin = "round";
          for (let n = 0; n < items.length; n++) {
            const [, kind, o] = items[n];
            if (kind === 0) {
              const q = o[0];
              g.beginPath();
              g.moveTo(X[q[0]], Y[q[0]]);
              for (let t = 1; t < 4; t++) g.lineTo(X[q[t]], Y[q[t]]);
              g.closePath();
              g.fillStyle = g.strokeStyle = o[1];
              g.globalAlpha = o[2];
              g.fill();
              if (o[2] === 1) { g.lineWidth = 0.6; g.setLineDash([]); g.stroke(); }
              g.globalAlpha = 1;
            } else if (kind === 1) {
              if (o.done) { o.done = false; continue; }
              let p0 = o, p1 = o;
              if (o.flat) {  // the pieces of a straight line up to the next surface go in one stroke, so no seams show
                let grew = true;
                while (grew) {
                  grew = false;
                  for (let m = n + 1; m < items.length && items[m][1] !== 0; m++) {
                    const q = items[m][2];
                    if (items[m][1] !== 1 || q.line !== o.line || q.done) continue;
                    if (q.k === p1.k + 1) { p1 = q; q.done = true; grew = true; }
                    else if (q.k === p0.k - 1) { p0 = q; q.done = true; grew = true; }
                  }
                }
              }
              g.beginPath();
              g.moveTo(X[p0.a], Y[p0.a]);
              g.lineTo(X[p1.b], Y[p1.b]);
              g.strokeStyle = o.c;
              g.lineWidth = o.lw;
              const dash = o.line && o.line.dash;
              g.lineCap = dash || o.flat ? "butt" : "round";
              g.setLineDash(dash || []);
              g.lineDashOffset = dash ? -o.line.cum[p0.k] : 0;
              g.stroke();
            } else if (kind === 2) {
              let vx = X[o.i] - X[o.j], vy = Y[o.i] - Y[o.j];
              const len = Math.hypot(vx, vy) || 1;
              vx /= len; vy /= len;
              const hl = Math.max(3.5 * o.w, 6), hw = Math.max(1.5 * o.w, 2.6), bx = X[o.i] - hl * vx, by = Y[o.i] - hl * vy;  // open head, as on the page
              g.strokeStyle = o.c;
              g.lineWidth = o.w;
              g.setLineDash([]);
              g.lineCap = "round";
              if (!o.d) { g.beginPath(); g.moveTo(X[o.j], Y[o.j]); g.lineTo(X[o.i], Y[o.i]); g.stroke(); }
              g.beginPath();
              g.moveTo(bx - hw * vy, by + hw * vx);
              g.lineTo(X[o.i], Y[o.i]);
              g.lineTo(bx + hw * vy, by - hw * vx);
              g.stroke();
            } else {
              g.beginPath();
              g.arc(X[o.i], Y[o.i], o.r, 0, 2 * Math.PI);
              g.setLineDash([]);
              g.fillStyle = o.h ? "#fff" : o.c;
              g.fill();
              g.strokeStyle = o.h ? o.c : "#fff";
              g.lineWidth = o.h ? 1.5 : 1;
              g.stroke();
            }
          }
          for (const l of this.labs) {  // beside its point, on the side given by its direction
            const c = Math.cos(l.a), s = Math.sin(l.a);
            const hx = c > 0.35 ? 0 : c < -0.35 ? -100 : -50, vy = s > 0.35 ? -100 : s < -0.35 ? 0 : -50;
            l.el.style.transform = `translate(${X[l.i] + l.r * c}px, ${Y[l.i] - l.r * s}px) translate(${hx}%, ${vy}%)`;
          }
        }
      }

      const grid = document.getElementById("g"), out = document.getElementById("o");
      const lg = document.getElementById("lg");
      let scenes = [], Rmax = 0;
      function build() {  // the drawings and the legend of the scene S
        if (scenes.length === S.panels.length && scenes.length) {
          const oldTexCount = texs.length;
          S.panels.forEach((p, i) => {
            const old = scenes[i], fresh = new Scene(p, document.createElement("div"));
            fresh.labs.forEach((l, j) => { l.el = old.labs[j].el; });
            for (const k of Object.keys(fresh)) if (!["box", "cv", "g"].includes(k)) old[k] = fresh[k];
          });
          texs.length = oldTexCount;
          Rmax = Math.max(...scenes.map(s => s.R));
          return;
        }
        for (const s of scenes) s.box.remove();
        texs.length = 0;
        lg.replaceChildren();
        grid.style.setProperty("--maxw", S.maxw + "px");
        grid.style.setProperty("--cols", S.cols);
        grid.setAttribute("aria-label", S.alt);
        window.frameElement.title = S.alt;
        scenes = S.panels.map((p) => new Scene(p, grid));
        Rmax = Math.max(...scenes.map((s) => s.R));
        for (const e of S.legend) {
          const it = document.createElement("div"), t = document.createElement("span");
          it.className = "it";
          const dash = e.d ? ` stroke-dasharray="${e.d.join(" ")}"` : "";
          it.innerHTML = {
            dot: `<svg width="24" height="14"><circle cx="12" cy="7" r="4.2" fill="${e.c}"/></svg>`,
            ring: `<svg width="24" height="14"><circle cx="12" cy="7" r="3.8" fill="#fff" stroke="${e.c}" stroke-width="1.5"/></svg>`,
            line: `<svg width="24" height="14"><line x1="1" y1="7" x2="23" y2="7" stroke="${e.c}" stroke-width="${e.w || 2}"${dash}/></svg>`,
            area: `<svg width="24" height="14"><rect x="2" y="1.5" width="20" height="11" fill="${e.c}" fill-opacity="${e.o || 1}" stroke="${e.e || e.c}" stroke-width="1.2"/></svg>`,
          }[e.k];
          tex(t, e.t);
          it.appendChild(t);
          lg.appendChild(it);
        }
      }
      build();

      // the view, shared by all panels and kept by the page when a slider redraws the figure
      let store = {};
      try { store = window.parent.__bs3d || (window.parent.__bs3d = {}); } catch (e) {}
      let view = S.key && store[S.key] ? { ...store[S.key] } : { az: S.az, el: S.el };
      const keep = () => { if (S.key) store[S.key] = { ...view }; };

      function fit() {  // square-ish canvases holding their balls, so that the scale never changes while turning
        for (const s of scenes) {
          const W = s.box.clientWidth;
          s.size(W, Math.min(S.h, W), S.shared ? Rmax : s.R);
        }
        if (window.frameElement) window.frameElement.style.height = out.offsetHeight + "px";
      }
      const draw = () => { for (const s of scenes) s.draw(view.az, view.el); };
      window.typeset = () => {
        for (const el of texs) try { katex.render(el.dataset.tex, el, { throwOnError: false }); } catch (e) {}
        fit();
        draw();
      };

      let pending = false;
      const redraw = () => { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; draw(); }); } };
      let grab = null;
      grid.addEventListener("pointerdown", (e) => { grab = { x: e.clientX, y: e.clientY, ...view }; grid.setPointerCapture(e.pointerId); grid.classList.add("drag"); });
      grid.addEventListener("pointermove", (e) => {
        if (!grab) return;
        view = { az: grab.az - (e.clientX - grab.x) * 0.45, el: Math.max(-89, Math.min(89, grab.el + (e.clientY - grab.y) * 0.45)) };
        keep();
        redraw();
      });
      const drop = () => { grab = null; grid.classList.remove("drag"); };
      grid.addEventListener("pointerup", drop);
      grid.addEventListener("pointercancel", drop);
      grid.addEventListener("dblclick", () => { view = { az: S.az, el: S.el }; if (S.key) delete store[S.key]; redraw(); });
      new ResizeObserver(() => { fit(); draw(); }).observe(out);
      if (window.katex) window.typeset();
      new MutationObserver(() => {
        const h = find();
        if (!h || h.dataset.scene === shown) return;
        shown = h.dataset.scene;
        S = JSON.parse(shown);
        build();
        fit(); draw();
      }).observe(box.querySelector("[data-scene]") ? box : P.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["data-scene"] });
    }
    </script></body></html>"""

    def _flat(*xyz):
        return np.round(np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in xyz)), -1).ravel(), 3).tolist()

    def panel(ys, surfaces=(), lines=(), points=(), axes=(), arrows=(), arcs=(), texts=(), caption=None, box=None):
        """One drawing of a 3D figure, with heights at the scale `ys`.
        lines: (x1, x2, y, colour, width[, dash, depth offset]); points: ((x^1, x^2, y), colour[, radius, hollow]);
        axes: (tail, tip, TeX label, direction of the label in degrees), drawn black;
        arrows: (tail, tip, colour[, width, dash]), vectors with a head in their colour;
        arcs: (x1, x2, y, colour[, width]), curves ending in a head, such as a turning arrow;
        texts: ((x^1, x^2, y), TeX, colour, direction[, distance]), names of points and objects and tick values,
        each beside its point; caption: TeX below the drawing;
        box: ((x^1 lo, hi), (x^2 lo, hi), (y lo, hi)) to size the drawing by, instead of its own points."""
        p = {"ys": ys, "surfaces": list(surfaces), "lines": [], "points": [], "heads": [], "labels": [], "caption": caption, "box": box}
        for ln in lines:
            p["lines"].append({"p": _flat(*ln[:3]), "c": ln[3], "w": ln[4], "d": ln[5] if len(ln) > 5 else None, "e": ln[6] if len(ln) > 6 else 0})
        for tail, tip, label, d in axes:
            a, b = np.asarray(tail, float), np.asarray(tip, float)
            seg = a + np.linspace(0, 0.96, 60)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": "#000000", "w": 1.1, "d": None, "b": 1})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": "#000000", "w": 1.1})
            p["labels"].append({"p": b.tolist(), "t": label, "c": "#000000", "a": d, "r": 5})
        for q in points:
            p["points"].append({"p": [float(c) for c in q[0]], "c": q[1], "r": q[2] if len(q) > 2 else 4.0, "h": bool(q[3]) if len(q) > 3 else False})
        for ar in arrows:
            a, b = np.asarray(ar[0], float), np.asarray(ar[1], float)
            seg = a + np.linspace(0, 0.96, 40)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8, "d": ar[4] if len(ar) > 4 else None, "e": 0, "b": 1})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8, "d": ar[4] if len(ar) > 4 else None})
        for arc in arcs:
            c = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in arc[:3])), -1)
            p["lines"].append({"p": _flat(*c[:-1].T), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8, "d": None, "e": 0})
            p["heads"].append({"p": c[-1].tolist(), "q": c[max(0, len(c) - 4)].tolist(), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8})
        for tx in texts:
            p["labels"].append({"p": [float(c) for c in tx[0]], "t": tx[1], "c": tx[2], "a": tx[3], "r": tx[4] if len(tx) > 4 else 5})
        return p

    def turntable(az, el, alt, panels, legend=(), height=360, width=None, cols=1, key=None, shared=True, bias=0.03, apart=False):
        """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
        from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
        at most `width` wide, with a legend box beside them (below them on narrow screens). `key` names the view
        so that it survives a redraw; with `shared`, all panels have one scale.
        legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area".
        apart: only the scene, for a figure with a slider, whose frame, frame(key, height), is shown by the next cell,
        so that moving the slider redraws the figure without rebuilding its frame."""
        scene = {"az": az, "el": el, "h": height, "bias": bias, "panels": list(panels), "legend": [], "key": key, "shared": shared,
                 "maxw": width or cols * height + (cols - 1) * 14, "cols": cols, "alt": alt}
        for e in legend:
            item = {"k": e[0], "c": e[1], "t": e[2]}
            if len(e) > 3:
                item["e" if e[0] == "area" else "w"] = e[3]
            if len(e) > 4:
                item["o" if e[0] == "area" else "d"] = e[4]
            scene["legend"].append(item)
        data = _html.escape(_json.dumps(scene, separators=(",", ":")))
        if apart:
            return mo.Html(f'<div hidden data-bs3d="{_html.escape(key)}" data-scene="{data}"></div>')
        return mo.Html(f'<div class="bs3d">{_frame(height)}<div hidden data-scene="{data}"></div></div>')

    def _frame(height, key=""):
        return f'<iframe srcdoc="{_html.escape(_PAGE)}" data-bs3d="{_html.escape(key)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>'

    def frame(key, height=360):
        """The frame of the figure turntable(..., key=key, height=height, apart=True) of the cell above."""
        return mo.Html(f'<div class="bs3d">{_frame(height, key)}</div>')

    return frame, panel, turntable

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Integration of functions and vector fields along 1-dimensional curves in $\mathbb R^3$

    $$
    f:D\subseteq\mathbb R^3\longrightarrow\mathbb R
    \qquad\text{or}\qquad
    \vec F:D\subseteq\mathbb R^3\longrightarrow\mathbb R^3
    $$

    $C=\gamma([a,b])\subset D$, parametrized by $\gamma:I\subseteq\mathbb R\to\mathbb R^3$.

    Path integral of $f$ over $C$:

    $$
    \int_C f\,ds=\int_a^bf(\gamma(t))\,\|\gamma'(t)\|\,dt.
    $$

    <span class="math-notes"><span>$\displaystyle f(\gamma(t))\quad(f)$</span><span>$\displaystyle \|\gamma'(t)\|\,dt\quad(ds)$</span></span>

    Line integral of $\vec F$ over $\vec C$ (oriented from $a$ to $b$):

    $$
    \int_{\vec C}\vec F\cdot d\vec s
    =\int_a^b\vec F(\gamma(t))\cdot\gamma'(t)\,dt.
    $$

    <span class="math-notes"><span>$\displaystyle \vec F(\gamma(t))\quad(\vec F)$</span><span>$\displaystyle \gamma'(t)\,dt\quad(d\vec s)$</span></span>

    $\leadsto$ &nbsp; independent of parametrization: given a change of variables

    $$
    t=\varphi(\tilde t)\in[a,b],\qquad\tilde t\in[c,d],\qquad\varphi'(\tilde t)\neq0,
    $$

    $$
    \int_c^d f(\gamma(\varphi(\tilde t)))\,
    \|\gamma'(\varphi(\tilde t))\varphi'(\tilde t)\|\,d\tilde t
    =\int_a^b f(\gamma(t))\|\gamma'(t)\|\,dt,
    $$

    $$
    \int_c^d\vec F(\gamma(\varphi(\tilde t)))\cdot
    \gamma'(\varphi(\tilde t))\varphi'(\tilde t)\,d\tilde t
    =\pm\int_a^b\vec F(\gamma(t))\cdot\gamma'(t)\,dt,
    $$

    $$
    \begin{cases}
    +&\text{if }\varphi'(\tilde t)>0\quad(\varphi\text{ preserves orientation}),\\
    -&\text{if }\varphi'(\tilde t)<0\quad(\varphi\text{ reverses orientation}).
    \end{cases}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $\vec F=\nabla f$, then

    $$
    \int_{\vec C}\vec F\cdot d\vec s
    =\int_a^b\vec F(\gamma(t))\cdot\gamma'(t)\,dt
    =f(\gamma(b))-f(\gamma(a))
    $$

    <span class="math-notes"><span>$\displaystyle f(\gamma(b))\quad(\text{end})$</span><span>$\displaystyle f(\gamma(a))\quad(\text{start})$</span></span>

    only depends on the (oriented) endpoints of $\vec C$.

    In particular, $\displaystyle\int_{\vec C}\vec F\cdot d\vec s=0$ over closed curves!
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; in this case, we call $\vec F=\nabla f$ a **conservative vector field** and $f$ a **potential function** for $\vec F$.

    **In this lecture:** multivariable integrals in $\mathbb R^n$ ($n=2$)

    $\leadsto$ &nbsp; to be able to define integrals of vector fields over surfaces in $\mathbb R^3$ (in a few weeks…).

    ## IV.4 &nbsp; Double integrals

    **Recall.** For $f:[a,b]\to\mathbb R$,

    $$
    \int_a^b f(t)\,dt=\lim_{N\to\infty}\sum_{i=1}^N f(t_i)\Delta t,
    $$

    where, for each $N\in\mathbb N_{>0}$:

    - divide $[a,b]=\bigcup_{i=1}^N[a_i,b_i]$, with

    $$
    a=a_1,\quad b_1=a_2,\quad\ldots,\quad b_{N-1}=a_N,\quad b_N=b,
    \qquad b_i-a_i=\frac{b-a}{N}=\Delta t;
    $$

    - choose $t_i\in[a_i,b_i]$.
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('partition')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \Longrightarrow\quad \sum_{i=1}^Nf(t_i)\,\Delta t$ $\displaystyle \approx\text{signed area between }\operatorname{graph}(f)\text{ and the }t\text{-axis}.$</span>

    <span class="math-notes"><span>$\displaystyle f(t_i)\quad(\text{height})$</span><span>$\displaystyle \Delta t\quad(\text{base})$</span></span>

    How do we integrate functions in $\mathbb R^2$?

    Suppose $f:R=[a,b]\times[c,d]\longrightarrow\mathbb R$.

    - Divide $[a,b]=\bigcup_{i=1}^N[a_i,b_i]$ and $[c,d]=\bigcup_{j=1}^N[c_j,d_j]$:

    $$
    \begin{aligned}
    a=a_1,\ b_1=a_2,\ldots,b_{N-1}=a_N,\ b_N=b,
    &\qquad b_i-a_i=\frac{b-a}{N}=\Delta x,\\
    c=c_1,\ d_1=c_2,\ldots,d_{N-1}=c_N,\ d_N=d,
    &\qquad d_j-c_j=\frac{d-c}{N}=\Delta y.
    \end{aligned}
    $$

    - Choose $(x_i,y_j)\in[a_i,b_i]\times[c_j,d_j]$.

    $$
    \iint_R f(x,y)\,dx\,dy
    =\lim_{N\to\infty}\sum_{j=1}^N\sum_{i=1}^N
    f(x_i,y_j)\Delta x\Delta y,
    $$

    if the limit exists for every choice $(x_i,y_j)$ and is independent of that choice!
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('rectangle')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \Longrightarrow\quad\iint_R f(x,y)\,dx\,dy
    =\text{signed volume between }\operatorname{graph}(f)\text{ and the }xy\text{-plane}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $f:R\subset\mathbb R^2\to\mathbb R$ is continuous, then $\displaystyle\iint_R f(x,y)\,dx\,dy$ is well-defined!
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof idea.**

    $$
    \operatorname{area}=A(y)=\int_a^b f(x,y)\,dx,
    \qquad\operatorname{vol}=\int_c^d A(y)\,dy.
    $$

    $$
    f(x,y)\text{ continuous}\quad\Longrightarrow\quad A(y)\text{ continuous}
    \quad\Longrightarrow\quad\text{integrable}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    slice_y = mo.ui.slider(0,2,step=0.05,value=1,label=r"$y$",show_value=True)
    return (slice_y,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, mo, np, panel, slice_y, turntable):
    _x,_y = np.meshgrid(np.linspace(0,2,18),np.linspace(0,2,18),indexing='ij')
    _z = 1.3+0.25*np.sin(1.6*_x)+0.2*_y
    def _surface(x,y,z,alpha=0.4,flat=None):
        return {'n':x.shape[0],'m':x.shape[1],'v':np.stack([x,y,z],-1).ravel().tolist(),'wire':[],'alpha':alpha,'flat':flat,'tone':None,'tint':None,'clear':False,'edge':None}
    _surf = _surface(_x,_y,_z,0.7)
    _sy = slice_y.value
    _xs=np.linspace(0,2,120);_zs=1.3+0.25*np.sin(1.6*_xs)+0.2*_sy
    _surfaces=[_surface(_x,_y,np.zeros_like(_z),0.4),_surf]
    _u,_v=np.meshgrid(np.linspace(0,2,24),np.linspace(0,1,12),indexing='ij')
    for _side in (0.,2.):
        _surfaces.append(_surface(_u,np.full_like(_u,_side),_v*(1.3+0.25*np.sin(1.6*_u)+0.2*_side)))
        _surfaces.append(_surface(np.full_like(_u,_side),_u,_v*(1.3+0.25*np.sin(1.6*_side)+0.2*_u)))
    _surfaces.append(_surface(_u,np.full_like(_u,_sy),_v*(1.3+0.25*np.sin(1.6*_u)+0.2*_sy),0.65,'#a8c6ae'))
    _scene = panel(1,surfaces=_surfaces,
        axes=[((0,0,0),(2.6,0,0),'x',-90),((0,0,0),(0,2.6,0),'y',0),((0,0,0),(0,0,2.5),'z',90)],
        lines=[(_x[:,0],_y[:,0],_z[:,0],BLUE,1.2),(_x[:,-1],_y[:,-1],_z[:,-1],BLUE,1.2),
               (_x[0,:],_y[0,:],_z[0,:],BLUE,1.2),(_x[-1,:],_y[-1,:],_z[-1,:],BLUE,1.2),
               (_xs,np.full_like(_xs,_sy),_zs,GREEN,2),(_xs,np.full_like(_xs,_sy),np.zeros_like(_xs),GREEN,1.3),
               ([0,0],[_sy,_sy],[0,float(_zs[0])],GREEN,1.3),([2,2],[_sy,_sy],[0,float(_zs[-1])],GREEN,1.3)],
        texts=[((1,_sy,0.95),'A(y)',GREEN,180),((1,1.9,2.3),'z=f(x,y)',BLUE,90)],
        box=((0,2.6),(0,2.6),(0,2.5)))
    mo.vstack([mo.hstack([slice_y],justify='start',gap=2,wrap=True),turntable(35,25,'Cross-sectional area under a graph',[_scene],height=440,key='bs10120-volume',apart=True)],gap=1)
    return


@app.cell(hide_code=True)
def _(frame):
    frame('bs10120-volume',440)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $f:R=[a,b]\times[c,d]\to\mathbb R$ is continuous,

    <span class="chain">$\displaystyle \iint_R f(x,y)\,dx\,dy
    =\int_c^d\left(\int_a^b f(x,y)\,dx\right)dy$ $\displaystyle =\int_a^b\left(\int_c^d f(x,y)\,dy\right)dx.$</span>

    Also works if discontinuities are not too bad!
    """,'Fubini')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** $f(x,y)=x^2+y$, $R=[0,2]\times[0,3]$.

    <span class="chain">$\displaystyle \int_0^3\left(\int_0^2(x^2+y)\,dx\right)dy
    =\int_0^3\left[\frac{x^3}{3}+xy\right]_{x=0}^{x=2}dy$ $\displaystyle =\int_0^3\left(\frac83+2y\right)dy=8+9=17,$</span>

    <span class="chain">$\displaystyle \int_0^2\left(\int_0^3(x^2+y)\,dy\right)dx
    =\int_0^2\left[x^2y+\frac{y^2}{2}\right]_{y=0}^{y=3}dx$ $\displaystyle =\int_0^2\left(3x^2+\frac92\right)dx=8+9=17.$</span>

    $$
    \Longrightarrow\quad\iint_R f(x,y)\,dx\,dy=17.
    $$

    $\leadsto$ &nbsp; double integrals over rectangles = iterated integrals over intervals

    $\leadsto$ &nbsp; independent of the order of integration!

    How about more general regions? How to describe them? How to integrate over them?
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    A region $D\subseteq\mathbb R^2$ is called **$y$-simple** if

    $$
    D=\{(x,y)\in\mathbb R^2\mid a\le x\le b,\ \varphi_1(x)\le y\le\varphi_2(x)\}
    $$

    for continuous functions $\varphi_1,\varphi_2:[a,b]\to\mathbb R$ with $\varphi_1\le\varphi_2$.

    Similarly, $D\subseteq\mathbb R^2$ is called **$x$-simple** if

    $$
    D=\{(x,y)\in\mathbb R^2\mid c\le y\le d,\ \psi_1(y)\le x\le\psi_2(y)\}
    $$

    for continuous functions $\psi_1,\psi_2:[c,d]\to\mathbb R$ with $\psi_1\le\psi_2$.
    """,'')
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('simple_regions')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Integration over $y$-simple / $x$-simple regions:

    Given $f:D\subseteq\mathbb R^2\to\mathbb R$ continuous over $D$ $y$-simple,

    $$
    \leadsto\quad\text{take }R=[a,b]\times[c,d]\supset D,
    \qquad c=\min_{[a,b]}\varphi_1,\quad d=\max_{[a,b]}\varphi_2;
    $$

    $\leadsto$ &nbsp; define $f^*:R\to\mathbb R$ via

    $$
    f^*(x,y)=\begin{cases}f(x,y)&\text{if }(x,y)\in D,\\0&\text{if }(x,y)\notin D.\end{cases}
    $$

    <span class="chain">$\displaystyle \iint_D f(x,y)\,dx\,dy
    =\iint_R f^*(x,y)\,dx\,dy$ $\displaystyle =\int_a^b\left(\int_c^d f^*(x,y)\,dy\right)dx
    =\int_a^b\left(\int_{\varphi_1(x)}^{\varphi_2(x)}f(x,y)\,dy\right)dx.$</span>

    $f^*$ is discontinuous, but Fubini still works!

    Similarly, if $f:D\subseteq\mathbb R^2\to\mathbb R$ is continuous over $D$ $x$-simple,

    $$
    \iint_D f(x,y)\,dx\,dy
    =\int_c^d\left(\int_{\psi_1(y)}^{\psi_2(y)}f(x,y)\,dx\right)dy.
    $$

    **Example.**

    $$
    D=\{(x,y)\mid x^2\le y\le1\}
    =\{(x,y)\mid-1\le x\le1,\ x^2\le y\le1\}
    \qquad\leadsto\quad y\text{-simple!}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    parabola_y = mo.ui.slider(0,1,step=0.05,value=0.5,label=r"$y$",show_value=True)
    return (parabola_y,)


@app.cell(hide_code=True)
def _(lecture_sketch, mo, parabola_y):
    _fig = lecture_sketch('parabola',parabola_y.value)
    mo.vstack([mo.hstack([parabola_y],justify="start",gap=2,wrap=True),mo.hstack([_fig],justify="center")],gap=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \iint_D(xy-2y)\,dx\,dy
    =\int_{-1}^1\left(\int_{x^2}^1(xy-2y)\,dy\right)dx$ $\displaystyle =\int_{-1}^1\left[\frac{xy^2}{2}-y^2\right]_{y=x^2}^{y=1}dx
    =\int_{-1}^1\left(\frac x2-1-\frac{x^5}{2}+x^4\right)dx$ $\displaystyle =\left[\frac{x^2}{4}-x-\frac{x^6}{12}+\frac{x^5}{5}\right]_{x=-1}^{x=1}
    =-2+\frac25=-\frac85.$</span>

    Is $D$ $x$-simple? Yes!

    $$
    D=\{(x,y)\mid0\le y\le1,\ -\sqrt y\le x\le\sqrt y\}.
    $$

    <span class="chain">$\displaystyle \iint_D(xy-2y)\,dx\,dy
    =\int_0^1\left(\int_{-\sqrt y}^{\sqrt y}(xy-2y)\,dx\right)dy$ $\displaystyle =\int_0^1\left[\frac{x^2y}{2}-2xy\right]_{x=-\sqrt y}^{x=\sqrt y}dy
    =\int_0^1-4\sqrt y\,y\,dy$ $\displaystyle =\int_0^1-4y^{3/2}\,dy
    =\left[-4\frac25y^{5/2}\right]_{y=0}^{y=1}=-\frac85.$</span>

    $\leadsto$ &nbsp; $D$ is called **simple** if it is both $y$-simple and $x$-simple.
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $D$ is $y$-simple or $x$-simple and $f:D\to\mathbb R$ is continuous, then there exists $(x_0,y_0)\in D$ such that

    $$
    \iint_D f(x,y)\,dx\,dy
    =f(x_0,y_0)\iint_D dx\,dy.
    $$

    <span class="math-notes"><span>$\displaystyle \iint_D dx\,dy\quad(\text{area of }D)$</span></span>

    $\leadsto$ &nbsp; $f(x_0,y_0)$ is the average of $f$ over $D$ (for positive area).
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Practice

    ① &nbsp; $D$ is the triangle with corners $(0,0),(2,0),(1,1)$.

     a) Describe $D$ as a $y$-simple region.

     b) Describe $D$ as an $x$-simple region.

     c) Compute $\displaystyle\iint_D y\,dx\,dy$.

    ② &nbsp; Compute $\displaystyle\int_0^1\left(\int_y^1\frac{\sin x}{x}\,dx\right)dy$.
    """)
    return


if __name__ == "__main__":
    app.run()
