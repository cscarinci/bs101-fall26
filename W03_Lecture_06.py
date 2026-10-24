import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 06 · Multivariable functions", css_file="bs101.css")


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
            return "correct" if abs(float(s) - answer) < 1e-6 else "try again"
        except ValueError:
            return "enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 06", "Week 03", "Lecture 06 · Multivariable functions")
    return


@app.cell(hide_code=True)
def _():
    def legend_box(fig, entries, loc="outside right center", ncols=1):
        """A legend box for the figure, so that no label covers the drawing: entries (kind, colour, label[, style])
        with kind "dot", "ring", "line" (style: line style) or "area" (style: edge colour)."""
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch

        handles = []
        for kind, c, _label, *style in entries:
            if kind == "dot":
                handles.append(Line2D([], [], ls="none", marker="o", ms=6, color=c))
            elif kind == "ring":
                handles.append(Line2D([], [], ls="none", marker="o", ms=6, mfc="white", mec=c, mew=1.3))
            elif kind == "line":
                handles.append(Line2D([], [], color=c, lw=1.6, ls=style[0] if style else "-"))
            else:
                handles.append(Patch(facecolor=c, edgecolor=style[0] if style else c, lw=1.0))
        fig.legend(handles, [e[2] for e in entries], loc=loc, ncols=ncols, fontsize=12, frameon=True, fancybox=False, edgecolor="#c8c8c8")

    return (legend_box,)


@app.cell(hide_code=True)
def _(mo, np):
    # ---- Interactive 3D figures ------------------------------------------
    # Drawn in the browser on canvases, in the style of the static figures: orthographic views of
    # R^3 = R^2 x R (x^1 towards the viewer, x^2 to the right, y up), surfaces drawn back to front.
    # Dragging turns the view at a fixed scale (all panels of a figure together) and a double click restores
    # it; a figure redrawn by a slider keeps its view. A legend box explains points, curves and surfaces, so
    # that no label covers the drawing; only the axes carry labels. Typesetting is done by KaTeX.
    import html as _html
    import json as _json

    _PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" onload="window.typeset && typeset()"></script>
    <style>
      html, body { margin: 0; padding: 0; background: transparent; overflow: hidden;
                   font-family: KaTeX_Main, "Latin Modern Roman", Georgia, serif; }
      #o { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 4px 16px; }
      #g { position: relative; flex: 1 1 300px; min-width: 240px; max-width: __MAXW__px; display: grid;
           grid-template-columns: repeat(__COLS__, minmax(0, 1fr)); gap: 6px 14px; touch-action: none; cursor: grab;
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
    <div id="o"><div id="g" role="img" aria-label="__ALT__"><div id="hint">&#10227;</div></div><div id="lg"></div></div>
    <script>
    (function () {
      const S = __SCENE__;
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
              if (![ln.p[3 * k], ln.p[3 * k + 3]].some(isNaN)) segs.push({ a: idx[k], b: idx[k + 1], c: ln.c, lw: ln.w, line, k, e: ln.e || 0 });
            return line;
          });
          for (const d of spec.points) this.dots.push({ i: add(...d.p), c: d.c, r: d.r, h: d.h });
          for (const h of spec.heads) this.heads.push({ i: add(...h.p), j: add(...h.q), c: h.c });
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
          for (const [, kind, o] of items) {
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
              g.beginPath();
              g.moveTo(X[o.a], Y[o.a]);
              g.lineTo(X[o.b], Y[o.b]);
              g.strokeStyle = o.c;
              g.lineWidth = o.lw;
              const dash = o.line && o.line.dash;
              g.lineCap = dash ? "butt" : "round";
              g.setLineDash(dash || []);
              g.lineDashOffset = dash ? -o.line.cum[o.k] : 0;
              g.stroke();
            } else if (kind === 2) {
              let vx = X[o.i] - X[o.j], vy = Y[o.i] - Y[o.j];
              const len = Math.hypot(vx, vy) || 1;
              vx /= len; vy /= len;
              const bx = X[o.i] - 9 * vx, by = Y[o.i] - 9 * vy;
              g.beginPath();
              g.moveTo(X[o.i], Y[o.i]);
              g.lineTo(bx - 3.4 * vy, by + 3.4 * vx);
              g.lineTo(bx + 3.4 * vy, by - 3.4 * vx);
              g.closePath();
              g.fillStyle = o.c;
              g.fill();
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
      const scenes = S.panels.map((p) => new Scene(p, grid));
      const Rmax = Math.max(...scenes.map((s) => s.R));
      const lg = document.getElementById("lg");
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
    })();
    </script></body></html>"""

    def _flat(*xyz):
        return np.round(np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in xyz)), -1).ravel(), 3).tolist()

    def sheet(x1, x2, y, wire=(), tint=None, clear=False, flat=None, alpha=1.0, tone=None):
        """A surface through the grid points (x1, x2, y) (2D arrays). `wire` lists grid lines to draw, as
        (axis, every, colour, width): every `every`-th row (axis 0) or column (axis 1), and the last one.
        Faces whose centre lies in tint = (x^1 lo, x^1 hi, x^2 lo, x^2 hi) (lo excluded) take deeper tones and
        stay opaque, without wire there when `clear`; the other faces have the opacity `alpha`.
        `flat` is one colour instead of the shading, and `tone` (a colour such as RED) shades the surface in
        light tones of that colour instead of the light blue ones."""
        n, m = np.shape(x1)
        rgb = [int(tone[k : k + 2], 16) for k in (1, 3, 5)] if tone else None
        return {"n": n, "m": m, "v": _flat(x1, x2, y), "wire": [list(t) for t in wire], "tint": tint, "clear": clear, "flat": flat, "alpha": alpha, "tone": rgb}

    def patch(corners, colour, alpha=1.0, n=6):
        """The flat parallelogram (or quadrilateral) with the four `corners` (in order), one colour, opacity `alpha`;
        cut into n x n faces, so that it is drawn in the right order among other surfaces."""
        c = [np.asarray(q, float) for q in corners]
        s, t = np.meshgrid(np.linspace(0, 1, n + 1), np.linspace(0, 1, n + 1), indexing="ij")
        p = (1 - s)[..., None] * (1 - t)[..., None] * c[0] + s[..., None] * (1 - t)[..., None] * c[1] + (s * t)[..., None] * c[2] + ((1 - s) * t)[..., None] * c[3]
        return sheet(p[..., 0], p[..., 1], p[..., 2], flat=colour, alpha=alpha)

    def panel(ys, surfaces=(), lines=(), points=(), axes=(), arrows=(), arcs=(), texts=(), caption=None, box=None):
        """One drawing of a 3D figure, with heights at the scale `ys`.
        lines: (x1, x2, y, colour, width[, dash, depth offset]); points: ((x^1, x^2, y), colour[, radius, hollow]);
        axes: (tail, tip, TeX label, direction of the label in degrees), drawn black;
        arrows: (tail, tip, colour[, width, dash]), vectors with a head in their colour;
        arcs: (x1, x2, y, colour[, width]), curves ending in a head, such as a turning arrow;
        texts: ((x^1, x^2, y), TeX, colour, direction[, distance]), short labels such as tick values (names of
        points and objects go in the legend instead); caption: TeX below the drawing;
        box: ((x^1 lo, hi), (x^2 lo, hi), (y lo, hi)) to size the drawing by, instead of its own points."""
        p = {"ys": ys, "surfaces": list(surfaces), "lines": [], "points": [], "heads": [], "labels": [], "caption": caption, "box": box}
        for ln in lines:
            p["lines"].append({"p": _flat(*ln[:3]), "c": ln[3], "w": ln[4], "d": ln[5] if len(ln) > 5 else None, "e": ln[6] if len(ln) > 6 else 0})
        for tail, tip, label, d in axes:
            a, b = np.asarray(tail, float), np.asarray(tip, float)
            seg = a + np.linspace(0, 0.96, 60)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": "#000000", "w": 1.1, "d": None})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": "#000000"})
            p["labels"].append({"p": b.tolist(), "t": label, "c": "#000000", "a": d, "r": 5})
        for q in points:
            p["points"].append({"p": [float(c) for c in q[0]], "c": q[1], "r": q[2] if len(q) > 2 else 4.0, "h": bool(q[3]) if len(q) > 3 else False})
        for ar in arrows:
            a, b = np.asarray(ar[0], float), np.asarray(ar[1], float)
            seg = a + np.linspace(0, 0.96, 40)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8, "d": ar[4] if len(ar) > 4 else None, "e": 0})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": ar[2]})
        for arc in arcs:
            c = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in arc[:3])), -1)
            p["lines"].append({"p": _flat(*c[:-1].T), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8, "d": None, "e": 0})
            p["heads"].append({"p": c[-1].tolist(), "q": c[max(0, len(c) - 4)].tolist(), "c": arc[3]})
        for tx in texts:
            p["labels"].append({"p": [float(c) for c in tx[0]], "t": tx[1], "c": tx[2], "a": tx[3], "r": tx[4] if len(tx) > 4 else 5})
        return p

    def turntable(az, el, alt, panels, legend=(), height=360, width=None, cols=1, key=None, shared=True, bias=0.03):
        """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
        from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
        at most `width` wide, with a legend box beside them (below them on narrow screens). `key` names the view
        so that it survives a redraw; with `shared`, all panels have one scale.
        legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area"."""
        scene = {"az": az, "el": el, "h": height, "bias": bias, "panels": list(panels), "legend": [], "key": key, "shared": shared}
        for e in legend:
            item = {"k": e[0], "c": e[1], "t": e[2]}
            if len(e) > 3:
                item["e" if e[0] == "area" else "w"] = e[3]
            if len(e) > 4:
                item["o" if e[0] == "area" else "d"] = e[4]
            scene["legend"].append(item)
        page = (_PAGE.replace("__MAXW__", str(width or cols * height + (cols - 1) * 14)).replace("__COLS__", str(cols))
                .replace("__ALT__", _html.escape(alt)).replace("__SCENE__", _json.dumps(scene, separators=(",", ":"))))
        return mo.Html(f'<iframe srcdoc="{_html.escape(page)}" title="{_html.escape(alt)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>')

    return panel, patch, sheet, turntable


@app.cell(hide_code=True)
def _(np, sheet):
    def quadric(b, zmax, colour, tone=None, alpha=1.0, every=6):
        """The level set (x^1)^2 + (x^2)^2 - (x^3)^2 = b for |x^3| <= zmax, as sheets with circles and meridians
        (one every `every` x 7.5 degrees) in `colour`: one sheet for b > 0, the cone for b = 0, two sheets for b < 0."""
        phi = np.linspace(0, 2 * np.pi, 49)
        if b >= 0:
            z = np.linspace(-zmax, zmax, 25)
            parts = [(np.sqrt(b + z**2), z)]
        else:
            r = np.linspace(0, np.sqrt(zmax**2 + b), 13)
            parts = [(r, s * np.sqrt(r**2 - b)) for s in (1, -1)]
        wire = [(0, 6, colour, 0.6), (1, every, colour, 0.6)]
        return [sheet(r[:, None] * np.cos(phi), r[:, None] * np.sin(phi), z[:, None] + 0 * phi, wire=wire, tone=tone, alpha=alpha) for r, z in parts]

    return (quadric,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## So far

    Euclidean Geometry

    - $\leadsto$ &nbsp; vectors, lines, planes
    - $\leadsto$ &nbsp; dot products and cross-products (in $\mathbb{R}^3$): lengths, angles, areas, volumes

    **In this lecture:** multivariable functions &nbsp; $\leadsto$ &nbsp; objects of interest in Multivariable Calculus

    **References:** MT 2.1
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""## II.1 &nbsp; Multivariable functions"""),
            definition(
                r"""
    A **multivariable function** is a rule

    $$
    f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m
    $$

    that assigns to each element $\vec{x}$ in a set $A \subseteq \mathbb{R}^n$ a unique element $\vec{y} = f(\vec{x})$ in another set $B \subseteq \mathbb{R}^m$.
    """,
                "Multivariable function",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; there are 3 parts to a function

    $$
    \begin{aligned}
    \mathrm{Dom}(f) &= A = \text{set of allowed inputs} \\
    \mathrm{Codom}(f) &= B = \text{set of desired outputs} \\
    \vec{x} &\longmapsto f(\vec{x}) \quad \text{the rule of assignment}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; change any one of these and you have a different function!

    **Remark.** Sometimes we will call

    - $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}$ &nbsp; ($m = 1$) &nbsp; a **scalar function** on $\mathbb{R}^n$ (or scalar-valued function)
    - $f : A \subseteq \mathbb{R} \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; ($n = 1$) &nbsp; a **path** in $\mathbb{R}^m$
    - $f : A \subseteq \mathbb{R}^2 \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; ($n = 2$) &nbsp; a **parameterized surface** in $\mathbb{R}^m$
    - $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ &nbsp; a **map** from $A \subseteq \mathbb{R}^n$ to $B \subseteq \mathbb{R}^m$

    **Example.**

    - lengths

        $$
        \lVert \cdot \rVert : \mathbb{R}^n \longrightarrow \mathbb{R}, \qquad \vec{x} \longmapsto \sqrt{(x^1)^2 + (x^2)^2 + \dots + (x^n)^2}
        $$

    - affine parameterizations

        $$
        \begin{aligned}
        \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^3 \\
        \underbrace{t}_{\text{variable}} &\longmapsto \underbrace{\begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \\ x^3 + t v^3 \end{bmatrix}}_{\vec{x} \text{ and } \vec{v} \text{ fixed here}}
        \end{aligned}
        \qquad \qquad
        \begin{aligned}
        \varphi : \mathbb{R}^2 &\longrightarrow \mathbb{R}^3 \\
        \underbrace{(s, t)}_{\text{variables}} &\longmapsto \underbrace{\begin{bmatrix} x^1 + s u^1 + t v^1 \\ x^2 + s u^2 + t v^2 \\ x^3 + s u^3 + t v^3 \end{bmatrix}}_{\vec{x},\ \vec{u} \text{ and } \vec{v} \text{ fixed here!}}
        \end{aligned}
        $$

    - linear transformations

        $$
        \begin{aligned}
        T : \mathbb{R}^n &\longrightarrow \mathbb{R}^m \\
        \underbrace{\begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix}}_{\text{variables}} &\longmapsto \underbrace{\begin{bmatrix} t^1{}_1 x^1 + \dots + t^1{}_n x^n \\ \vdots \\ t^m{}_1 x^1 + \dots + t^m{}_n x^n \end{bmatrix}}_{t^i{}_j \text{ are fixed}}
        \end{aligned}
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
            mo.md(r"""### Basic properties"""),
            definition(
                r"""
    Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$

    - the **image** of $f$ is

        $$
        \mathrm{Im}(f) = \left\{\, \vec{y} \in \mathbb{R}^m \;\middle|\; \exists\, \vec{x} \in A,\ f(\vec{x}) = \vec{y} \,\right\} \underbrace{\subseteq B}_{\text{not necessarily equal!}} \qquad \big(\mathrm{Im}(f) \subseteq \mathrm{Codom}(f)\big)
        $$

    - the **graph** of $f$ is

        $$
        \mathrm{graph}(f) = \left\{\, (\vec{x}, \vec{y}) \in \mathbb{R}^n \times \mathbb{R}^m \;\middle|\; \vec{x} \in A,\ \vec{y} = f(\vec{x}) \,\right\} \subseteq A \times B
        $$
    """,
                "Image and graph",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ affine parameterization, &nbsp; $\gamma(t) = \vec{x} + t\vec{v}$ &nbsp; (with $\vec{v} \neq \vec{0}$)

    $$
    \leadsto \qquad \mathrm{Im}(\gamma) = \left\{\, \vec{y} \in \mathbb{R}^2 \;\middle|\; \exists\, t \in \mathbb{R},\ \vec{y} = \gamma(t) \,\right\} \qquad \text{line in } \mathbb{R}^2 \text{ through } \vec{x} \text{ in the direction of } \vec{v}
    $$

    $$
    \leadsto \qquad \mathrm{graph}(\gamma) = \left\{\, (t, \vec{y}) \in \mathbb{R} \times \mathbb{R}^2 \;\middle|\; t \in \mathbb{R},\ \vec{y} = \gamma(t) \,\right\} \qquad \text{subset of } \mathbb{R} \times \mathbb{R}^2 \approx \mathbb{R}^3
    $$

    $$
    (0, \vec{x}) = \begin{bmatrix} 0 \\ x^1 \\ x^2 \end{bmatrix}, \qquad
    (t, \vec{x} + t\vec{v}) = \begin{bmatrix} t \\ x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_path = mo.ui.slider(-1, 3, 0.25, value=1.5, label="$t$", show_value=True)
    return (t_path,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, RED, arrow, blank, legend_box, mo, np, panel, t_path, table, turntable):
    _x, _v, _t = (2.0, 2.0), (0.6, 0.2), t_path.value
    _g = (_x[0] + _t * _v[0], _x[1] + _t * _v[1])

    # the t-line, the map gamma, and Im(gamma): a line in R^2 (0 and its image in red, t and its image in blue)
    _fig, _ax = blank(FULL, 3.0, (-6.6, 5.6), (-0.7, 3.7))

    def _at(s):
        return -5.6 + 0.8 * (s + 1)

    arrow(_ax, (-6.2, 1.5), (-1.9, 1.5), "black", lw=0.9)
    _ax.text(-1.9, 1.32, r"$\mathbb{R}$", fontsize=13, ha="right", va="top")
    _ax.plot(_at(0), 1.5, "o", color=RED, ms=6 if _t == 0 else 4.5, zorder=4)
    _ax.plot(_at(_t), 1.5, "o", color=BLUE, ms=4.5, zorder=4)
    _ax.text(_at(0), 1.32, "$0$", fontsize=12, ha="center", va="top")
    _ax.text(_at(_t), 1.68, "$t$", fontsize=13, ha="center", va="bottom", color=BLUE)
    arrow(_ax, (-1.55, 2.2), (-0.45, 2.2), "black", lw=0.9, connectionstyle="arc3,rad=-0.3")
    _ax.text(-1.0, 2.5, r"$\gamma$", fontsize=13, ha="center", va="bottom")

    arrow(_ax, (-0.4, 0), (4.8, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 3.5), "black", lw=0.9)
    _ax.text(4.8, -0.14, "$y^1$", fontsize=13, ha="right", va="top")
    _ax.text(-0.14, 3.5, "$y^2$", fontsize=13, ha="right", va="top")
    _ax.plot([_x[0] + s * _v[0] for s in (-1.5, 3.7)], [_x[1] + s * _v[1] for s in (-1.5, 3.7)], color="black", lw=1.2)
    arrow(_ax, (0, 0), _v, GREEN)
    arrow(_ax, (0, 0), _x, RED)
    arrow(_ax, (0, 0), _g, BLUE)
    _ax.plot(*_x, "o", color=RED, ms=6 if _t == 0 else 4, zorder=4)  # under the blue dot, as a rim, when the two coincide
    _ax.plot(*_g, "o", color=BLUE, ms=4, zorder=4)
    legend_box(
        _fig,
        [("line", "black", r"$\mathrm{Im}(\gamma)$"), ("line", GREEN, r"$\vec{v}$"), ("dot", RED, r"$\vec{x} = \gamma(0)$"), ("dot", BLUE, r"$\gamma(t)$")],
        loc="outside lower center",
        ncols=4,
    )

    # graph(gamma): a line in R x R^2, with t to the right, y^1 towards the viewer and y^2 up; over t, a copy of the (y^1, y^2)-axes
    _s = np.array([-1.5, 3.7])
    _copy = [] if _t == 0 else [((-0.5, _t, 0), (3.8, _t, 0), GREY, 1.2), ((0, _t, -0.5), (0, _t, 2.7), GREY, 1.2)]
    _graph = turntable(
        30,
        20,
        "graph of gamma, a line in R x R^2, with its points (0, x) and (t, gamma(t)), and the axes of {t} x R^2",
        [
            panel(
                1.0,
                lines=[(_x[0] + _s * _v[0], _s, _x[1] + _s * _v[1], "#000000", 1.6)],
                arrows=_copy + [((0, 0, 0), (_x[0], 0, _x[1]), RED), ((0, _t, 0), (_g[0], _t, _g[1]), BLUE)],
                points=[((_x[0], 0, _x[1]), RED, 6.0 if _t == 0 else 4.5), ((_g[0], _t, _g[1]), BLUE, 4.5), ((0, _t, 0), GREY, 3.5)],
                axes=[((-0.5, 0, 0), (4.4, 0, 0), "y^1", -120), ((0, -1.5, 0), (0, 4.0, 0), "t", 0), ((0, 0, -0.5), (0, 0, 3.2), "y^2", 90)],
                texts=[((0, 0, 0), "0", "#000000", -45)],
                box=((-0.3, 4.2), (-1.3, 3.8), (-0.3, 3.0)),
            )
        ],
        legend=[
            ("line", "#000000", r"\mathrm{graph}(\gamma)", 1.6),
            ("dot", RED, r"(0, \vec{x})"),
            ("dot", BLUE, r"(t, \gamma(t))"),
            ("dot", GREY, r"(t, \vec{0})"),
            ("line", GREY, r"\{t\} \times \mathbb{R}^2", 1.2),
        ],
        height=420,
        key="lecture-06-graph-line",
    )

    mo.vstack(
        [
            mo.hstack([t_path], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{x} = \gamma(0)$", rf"$\textcolor{{{RED}}}{{\begin{{bmatrix}} {_x[0]:g} \\ {_x[1]:g} \end{{bmatrix}}}}$"),
                    (r"$\vec{v}$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_v[0]:g} \\ {_v[1]:g} \end{{bmatrix}}}}$"),
                    (r"$\gamma(t) = \vec{x} + t\vec{v}$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_g[0]:g} \\ {_g[1]:g} \end{{bmatrix}}}}$"),
                    (r"$(t, \gamma(t)) \in \mathrm{graph}(\gamma)$", rf"$\textcolor{{{BLUE}}}{{\begin{{bmatrix}} {_t:g} \\ {_g[0]:g} \\ {_g[1]:g} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
            _graph,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, definition, mo, np, panel, sheet, turntable):
    # The sphere of radius 2 with its equator, two of its points and the coordinate axes
    _th, _ph = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 49), indexing="ij")
    _q = [tuple(2 * np.array(_d) / np.linalg.norm(_d)) for _d in ((0.3, 1.0, 1.7), (0.2, 1.3, 1.5))]
    _fig = turntable(
        28,
        22,
        "the sphere of radius 2 about the origin, the level set of f with value 2, with two of its points x and y",
        [
            panel(
                1.0,
                surfaces=[sheet(2 * np.sin(_th) * np.cos(_ph), 2 * np.sin(_th) * np.sin(_ph), 2 * np.cos(_th), wire=[(0, 12, BLUE, 1.4), (1, 12, BLUE, 0.5)], alpha=0.3)],
                arrows=[((0, 0, 0), _q[0], RED), ((0, 0, 0), _q[1], ORANGE)],
                points=[(tuple(2 * _d), "#000000", 2.6) for _d in np.eye(3)],
                axes=[((-1.0, 0, 0), (3.0, 0, 0), "x^1", -120), ((0, -1.0, 0), (0, 3.0, 0), "x^2", 0), ((0, 0, -1.0), (0, 0, 3.0), "x^3", 90)],
                texts=[(tuple(2 * _d), "2", "#000000", _a) for _d, _a in zip(np.eye(3), (120, -60, 150))] + [((0, 0, 0), r"\vec{0}", "#000000", -60)],
            )
        ],
        legend=[("area", LIGHT, "f^{-1}(2)", BLUE), ("line", RED, r"\vec{x}"), ("line", ORANGE, r"\vec{y}")],
        height=360,
    )

    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** $\mathrm{Im}(f)$ and $\mathrm{graph}(f)$ help us visualize $f$ as a set of points (very useful in lower dimensions)

    - $\leadsto$ &nbsp; we might have many functions with same image
    - $\leadsto$ &nbsp; graph essentially determines the function completely! (but it lives in higher dimensions)

    ### Level sets
    """
            ),
            definition(
                r"""
    Given $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$, $\vec{b} \in B$ fixed, the **level set** of $f$ with value $\vec{b}$ is

    $$
    f^{-1}(\vec{b}) = \left\{\, \vec{x} \in \mathbb{R}^n \;\middle|\; \vec{x} \in A \text{ and } f(\vec{x}) = \vec{b} \,\right\}
    $$
    """,
                "Level set",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f : \mathbb{R}^3 \longrightarrow \mathbb{R}, \quad \vec{x} \longmapsto \lVert \vec{x} \rVert$

    $$
    \text{fix } r = 2 \qquad \Longrightarrow \qquad f^{-1}(2) = \left\{\, \vec{x} \in \mathbb{R}^3 \;\middle|\; \lVert \vec{x} \rVert = 2 \,\right\} = \text{sphere centered at } \vec{0} \text{ with radius } r = 2
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** Here $f^{-1}(\vec{b})$ is NOT the value of the inverse function of $f$ (we don't even know if $f$ has an inverse).

    $f^{-1}(\vec{b})$ is the set of points in the domain of $f$ which gives the value “$\vec{b}$” as an output!

    $\leadsto$ &nbsp; if $f$ is invertible then, for each $\vec{b} \in B$,

    $$
    f^{-1}(\vec{b}) = \left\{\, \vec{x} \in A \;\middle|\; f(\vec{x}) = \vec{b} \,\right\} \quad \text{has a single element, which we call ``$f^{-1}(\vec{b})$''}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, HALF, ORANGE, RED, arrow, blank, legend_box, mo, np, panel, quadric, turntable):
    # level sets of f in the plane
    _fig, _ax = blank(HALF + 1.2, 3.3, (-3.6, 3.9), (-3.6, 3.8))
    arrow(_ax, (-3.4, 0), (3.5, 0), "black", lw=0.9)
    arrow(_ax, (0, -3.4), (0, 3.5), "black", lw=0.9)
    _ax.text(3.5, -0.15, "$x^1$", fontsize=13, ha="right", va="top")
    _ax.text(0.15, 3.5, "$x^2$", fontsize=13, ha="left", va="top")
    _s = np.linspace(-2.9, 2.9, 200)
    for _sign in (1, -1):
        _ax.plot(_s, _sign * _s, color=ORANGE, lw=1.4)
        _ax.plot(_sign * np.sqrt(1 + _s[20:-20] ** 2), _s[20:-20], color=BLUE, lw=1.4)
        _ax.plot(_s[35:-35], _sign * np.sqrt(4 + _s[35:-35] ** 2), color=RED, lw=1.4)
    legend_box(_fig, [("line", BLUE, "$f^{-1}(1)$"), ("line", ORANGE, "$f^{-1}(0)$"), ("line", RED, "$f^{-1}(-4)$")])

    # level sets of g in space, one inside the other: g^{-1}(-4) inside the cone g^{-1}(0) inside g^{-1}(1)
    _fig2 = turntable(
        28,
        22,
        "level sets of g in space: the hyperboloid of one sheet g^{-1}(1) around the cone g^{-1}(0) around the hyperboloid of two sheets g^{-1}(-4)",
        [
            panel(
                1.0,
                surfaces=quadric(1, 2.2, BLUE, BLUE, 0.35, 12) + quadric(0, 3.0, ORANGE, ORANGE, 0.35, 12) + quadric(-4, 3.6, RED, RED, 0.5, 12),
                axes=[((-1.2, 0, 0), (4.4, 0, 0), "x^1", -120), ((0, -1.2, 0), (0, 4.0, 0), "x^2", 0), ((0, 0, -1.2), (0, 0, 5.0), "x^3", 90)],
            )
        ],
        legend=[("area", BLUE, "g^{-1}(1)", BLUE, 0.25), ("area", ORANGE, "g^{-1}(0)", ORANGE, 0.25), ("area", RED, "g^{-1}(-4)", RED, 0.25)],
        height=420,
    )

    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** &nbsp; $f : \mathbb{R}^2 \longrightarrow \mathbb{R}, \quad \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \longmapsto (x^1)^2 - (x^2)^2$

    What are the level sets with values $1, 0, -4$?

    $$
    f^{-1}(b) = \left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \;\middle|\; (x^1)^2 - (x^2)^2 = b \,\right\}
    $$

    - $f^{-1}(0) \iff \lvert x^1 \rvert = \lvert x^2 \rvert$ &nbsp; two intersecting lines (a cone)
    - $f^{-1}(1) \iff (x^1)^2 - (x^2)^2 = 1$ &nbsp; a hyperbola
    - $f^{-1}(-4) \iff (x^1)^2 - (x^2)^2 = -4$ &nbsp; also a hyperbola
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    g : \mathbb{R}^3 \longrightarrow \mathbb{R}, \quad \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \longmapsto (x^1)^2 + (x^2)^2 - (x^3)^2
    $$

    - $g^{-1}(0)$ &nbsp; cone
    - $g^{-1}(1)$ &nbsp; hyperboloid of one sheet
    - $g^{-1}(-4)$ &nbsp; hyperboloid of two sheets
    """
            ),
            _fig2,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    b_level = mo.ui.slider(-4, 4, 0.5, value=1, label="$b$", show_value=True)
    return (b_level,)


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, b_level, legend_box, mo, np, panel, plane, quadric, table, turntable):
    _b = b_level.value

    # f^{-1}(b) in the plane
    _fig = Figure(figsize=(HALF + 0.4, 4.2), layout="constrained")
    _left = _fig.subplots()
    plane(_left, 4)
    _left.set_xticks(range(-4, 5, 2))
    _left.set_yticks(range(-4, 5, 2))
    _left.set_xlabel("$x^1$")
    _left.set_ylabel("$x^2$", rotation=0, labelpad=10)
    _s = np.linspace(-4.2, 4.2, 400)
    for _sign in (1, -1):
        if _b > 0:
            _left.plot(_sign * np.sqrt(_b + _s**2), _s, color=BLUE, lw=1.4)
        elif _b < 0:
            _left.plot(_s, _sign * np.sqrt(_s**2 - _b), color=BLUE, lw=1.4)
        else:
            _left.plot(_s, _sign * _s, color=BLUE, lw=1.4)
    legend_box(_fig, [("line", BLUE, "$f^{-1}(b)$")], loc="outside lower center")

    # g^{-1}(b) in space, for -3 <= x^3 <= 3 (the scale holds every b)
    _graph = turntable(
        28,
        22,
        "the level set of g with value b in space, cut at |x3| <= 3: a hyperboloid of one sheet for b > 0, the cone for b = 0, a hyperboloid of two sheets for b < 0",
        [
            panel(
                1.0,
                surfaces=quadric(_b, 3.0, BLUE),
                axes=[((-1.2, 0, 0), (4.6, 0, 0), "x^1", -120), ((0, -1.2, 0), (0, 4.4, 0), "x^2", 0), ((0, 0, -1.2), (0, 0, 4.0), "x^3", 90)],
                box=((-2.8, 2.8), (-2.8, 2.8), (-2.8, 2.8)),
            )
        ],
        legend=[("area", LIGHT, "g^{-1}(b)", BLUE)],
        height=380,
        key="lecture-06-quadric",
    )

    _flat = "two intersecting lines (a cone)" if _b == 0 else "a hyperbola"
    _solid = "cone" if _b == 0 else "hyperboloid of one sheet" if _b > 0 else "hyperboloid of two sheets"

    mo.vstack(
        [
            mo.hstack([b_level], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f^{-1}(b) \subseteq \mathbb{R}^2$", rf"$(x^1)^2 - (x^2)^2 = {_b:g}$ &nbsp; ({_flat})"),
                    (r"$g^{-1}(b) \subseteq \mathbb{R}^3$", rf"$(x^1)^2 + (x^2)^2 - (x^3)^2 = {_b:g}$ &nbsp; ({_solid})"),
                ]
            ),
            mo.Html(
                '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
                f'<div style="flex: 1 1 240px; min-width: 220px;">{mo.as_html(_fig).text}</div>'
                f'<div style="flex: 1.5 1 320px; min-width: 260px;">{_graph.text}</div></div>'
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
    For $p : \mathbb{R}^3 \longrightarrow \mathbb{R}$ an **affine scalar function**

    $$
    p\!\left( \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \right) = a x^1 + b x^2 + c x^3 + d
    $$

    $p^{-1}(r)$ is a plane in $\mathbb{R}^3$ (if $(a, b, c) \neq (0, 0, 0)$)

    $$
    \leadsto \qquad \text{starting point } \begin{bmatrix} (r - d)/a \\ 0 \\ 0 \end{bmatrix} \ (\text{if } a \neq 0), \qquad \text{normal vector } \begin{bmatrix} a \\ b \\ c \end{bmatrix}
    $$

    (if $a = b = c = 0$, then $p^{-1}(r) = \mathbb{R}^3$ when $r = d$, and $\varnothing$ otherwise)

    For $q : \mathbb{R}^3 \longrightarrow \mathbb{R}$ a **quadratic scalar function**

    $$
    \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \longmapsto
    \begin{aligned}
    &a (x^1)^2 + b (x^2)^2 + c (x^3)^2 + d\, x^1 x^2 + e\, x^2 x^3 + f\, x^3 x^1 \\
    &+ g\, x^1 + h\, x^2 + i\, x^3 + j
    \end{aligned}
    $$

    $q^{-1}(r)$ is called a **quadratic surface**.
    """,
                "Affine and quadratic scalar functions",
            ),
            mo.md(
                r"""
    $$
    \begin{aligned}
    \frac{(x^1)^2}{a^2} + \frac{(x^2)^2}{b^2} + \frac{(x^3)^2}{c^2} &= r^2 &&\text{ellipsoids} \rule[-1.5em]{0pt}{3.4em} \\
    \frac{(x^1)^2}{a^2} + \frac{(x^2)^2}{b^2} - \frac{(x^3)^2}{c^2} &= \pm r^2 &&\text{hyperboloids} \rule[-1.5em]{0pt}{3.4em} \\
    \frac{(x^1)^2}{a^2} + \frac{(x^2)^2}{b^2} - \frac{x^3}{c} &= d &&\text{paraboloids} \rule[-1.5em]{0pt}{3.4em} \\
    &\ \,\vdots
    \end{aligned}
    \qquad (\text{here } a, b, c \neq 0 \text{ and } r > 0)
    $$

    **Remark.** Sometimes level sets of a function can be seen as graphs of another function and vice-versa!

    $\Longrightarrow$ &nbsp; geometry of sets in $\mathbb{R}^n$ or $\mathbb{R}^m$ or $\mathbb{R}^n \times \mathbb{R}^m$ is useful to study properties of various functions
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ### Question 1

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \ln\!\big( x^2 - (x^1)^2 \big)
    $$

    (a) Find the largest possible domain and codomain.

    (b) For those, find the image.

    (c) Sketch the level sets $f^{-1}(0)$, $f^{-1}(\ln 4)$.

    ### Question 2

    Let $T : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ be given by

    $$
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \longmapsto \begin{bmatrix} x^1 + x^2 \\ (x^1 + x^2)^2 \end{bmatrix}
    $$

    (a) Sketch $\mathrm{Im}(T)$.

    (b) Describe $T^{-1}\!\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right)$ and $T^{-1}\!\left( \begin{bmatrix} 1 \\ 2 \end{bmatrix} \right)$.

    ### Question 3

    Consider the surface

    $$
    S = \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \in \mathbb{R}^3 \;\middle|\; (x^1)^2 + (x^2)^2 - x^3 = 1 \,\right\}
    $$

    Find

    (a) a function $f$ such that $S$ is a level set of $f$

    (b) a function $g$ such that $S$ is the graph of $g$

    (c) a function $h$ such that $S$ is the image of $h$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a multivariable function $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$ has 3 parts: domain, codomain and rule of assignment; scalar functions ($m = 1$), paths ($n = 1$), parameterized surfaces ($n = 2$)
    - $\mathrm{Im}(f) \subseteq B$ (not necessarily equal) and $\mathrm{graph}(f) \subseteq A \times B$ help us visualize $f$ as a set of points; the graph essentially determines the function
    - the level set $f^{-1}(\vec{b}) = \{\, \vec{x} \in A \mid f(\vec{x}) = \vec{b} \,\}$ is a set of points in the domain, NOT the value of an inverse function
    - level sets of affine scalar functions on $\mathbb{R}^3$ are planes; level sets of quadratic scalar functions are quadratic surfaces (ellipsoids, hyperboloids, paraboloids, …)
    """)
    return


if __name__ == "__main__":
    app.run()
