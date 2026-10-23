import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 05 · Lines and planes and the cross-product in R³", css_file="bs101.css")


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
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 05", "Week 03", "Lecture 05 · Lines and planes and the cross-product in R³")
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
    <div id="o"><div id="g" role="img" aria-label="__ALT__"><div id="hint" title="drag to turn the view, double click to restore it">&#10227;</div></div><div id="lg"></div></div>
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
def _(mo):
    mo.md(r"""
    ## Last time

    - determinants

        $$
        \begin{aligned}
        A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \qquad \Longrightarrow \qquad
        \det A &= ad - bc \\[4pt]
        &= \text{signed area of parallelogram spanned by } \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix},\ \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix}
        \end{aligned}
        $$

        $$
        A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \quad \Longrightarrow \quad
        \det A = a(ei - fh) - b(di - fg) + c(dh - eg) = \text{signed volume}
        $$

    - $\leadsto$ &nbsp; need to interpret sign
    - $\leadsto$ &nbsp; need to understand angle between vectors and planes

    **In this lecture:** lines and planes in $\mathbb{R}^3$, and the cross-product

    **References:** MT 1.1, 1.3
    """)
    return


@app.cell(hide_code=True)
def _(HALF, ORANGE, RED, arrow, blank, definition, legend_box, mo):
    _fig, _ax = blank(HALF + 0.9, 1.75, (-0.6, 4.7), (-0.5, 1.95))
    _x, _v, _t = (0.4, 1.4), (1.6, 0.0), 1.7
    _g = (_x[0] + _t * _v[0], _x[1])
    _ax.plot([-0.5, 4.2], [1.4, 1.4], color="black", lw=1.0)
    arrow(_ax, (0, 0), _g, ORANGE)
    arrow(_ax, (0, 0), _x, "black")
    arrow(_ax, (0, 0), _v, RED)
    arrow(_ax, _x, _g, RED)
    _ax.plot(0, 0, "o", color="black", ms=4, zorder=4)
    _ax.text(0.08, 0.78, r"$\vec{x}$", fontsize=13, ha="right", va="center")
    _ax.text(0.8, -0.1, r"$\vec{v}$", color=RED, fontsize=13, ha="center", va="top")
    _ax.text((_x[0] + _g[0]) / 2, 1.52, r"$t\vec{v}$", color=RED, fontsize=13, ha="center", va="bottom")
    _ax.text(1.95, 0.62, r"$\vec{x} + t\vec{v}$", color=ORANGE, fontsize=13, ha="left", va="top")
    _ax.text(4.32, 1.4, "$L$", fontsize=13, ha="left", va="center")
    legend_box(_fig, [("dot", "black", r"$\vec{0}$")])

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.5 &nbsp; Lines and planes and the cross-product in $\mathbb{R}^3$

    ### Lines
    """
            ),
            definition(
                r"""
    Given vectors $\vec{x}$ and $\vec{v}$ in $\mathbb{R}^3$, with $\vec{v}$ non-zero, the **line** through $\vec{x}$ in the direction of $\vec{v}$ is the set

    $$
    L = \left\{\, \gamma(t) = \vec{x} + t\vec{v} \in \mathbb{R}^3 \;\middle|\; t \in \mathbb{R} \,\right\}
    $$

    We call the function

    $$
    \begin{aligned}
    \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^3 \\
    t &\longmapsto \gamma(t) = \vec{x} + t\vec{v}
    \end{aligned}
    $$

    an **affine parameterization** of the line $L$ (just a name for “linear plus constant”).
    """,
                "Line and affine parameterization",
            ),
            _fig,
            mo.md(
                r"""
    **Example.**

    $$
    \vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}
    \qquad \leadsto \qquad
    \gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} t \\ 1 + 2t \\ 1 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_line = mo.ui.slider(-1.5, 1.5, 0.25, value=1, label="$t$", show_value=True)
    return (t_line,)


@app.cell(hide_code=True)
def _(GREY, LIGHT, ORANGE, RED, mo, np, panel, patch, t_line, table, turntable):
    _t = t_line.value
    _x, _v = np.array((0.0, 1.0, 1.0)), np.array((1.0, 2.0, 0.0))
    _g = _x + _t * _v + 0.0
    # the plane x^3 = 1 and the line L inside it
    _plane = [(-1.8, -2.4, 1), (-1.8, 4.6, 1), (1.8, 4.6, 1), (1.8, -2.4, 1)]
    _rim = np.array(_plane + _plane[:1])
    _L = np.array([_x + _s * _v for _s in (-1.7, 1.8)])
    _fig = turntable(
        24,
        26,
        "the plane x3 = 1 containing the line L through x in the direction of v, with the point gamma(t) = x + t v of L",
        [
            panel(
                1.0,
                surfaces=[patch(_plane, LIGHT, 0.35, n=12)],
                lines=[(_rim[:, 0], _rim[:, 1], _rim[:, 2], GREY, 1.0), (_L[:, 0], _L[:, 1], _L[:, 2], "#000000", 1.2)],
                points=[(tuple(_g), ORANGE)],
                axes=[((-0.5, 0, 0), (2.4, 0, 0), "x^1", -135), ((0, -0.5, 0), (0, 4.9, 0), "x^2", 0), ((0, 0, -0.5), (0, 0, 2.15), "x^3", 90)],
                arrows=[((0, 0, 0), tuple(_x), "#000000"), ((0, 0, 0), tuple(_v), RED), ((0, 0, 0), tuple(_g), ORANGE)],
                box=((-1.8, 2.4), (-2.4, 4.9), (-0.5, 2.15)),
            )
        ],
        legend=[
            ("area", LIGHT, r"x^3 = 1", GREY, 0.35),
            ("line", "#000000", "L", 1.2),
            ("line", "#000000", r"\vec{x}"),
            ("line", RED, r"\vec{v}"),
            ("dot", ORANGE, r"\gamma(t)"),
        ],
        height=380,
        key="lecture-05-line",
        bias=0.25,
    )

    mo.vstack(
        [
            mo.hstack([t_line], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$t$", rf"${_t:g}$"),
                    (r"$\gamma(t) = \vec{x} + t\vec{v}$", rf"$\begin{{bmatrix}} 0 \\ 1 \\ 1 \end{{bmatrix}} + ({_t:g}) \textcolor{{{RED}}}{{\begin{{bmatrix}} 1 \\ 2 \\ 0 \end{{bmatrix}}}} = \textcolor{{{ORANGE}}}{{\begin{{bmatrix}} {_g[0]:g} \\ {_g[1]:g} \\ {_g[2]:g} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Given a line $L$ with an affine parameterization

    $$
    \gamma(t) = \vec{x} + t\vec{v}
    $$

    we call $\vec{x}$ the **starting point** and $\vec{v}$ the **velocity** of $L$ with respect to the parameterization $\gamma$.
    """,
                "Starting point and velocity",
            ),
            mo.md(
                r"""
    **Remark.** There exists a unique line through $\vec{x}, \vec{y} \in \mathbb{R}^3$ if and only if $\vec{y} - \vec{x}$ is non-zero.

    However, parameterizations are not unique!

    $$
    \begin{aligned}
    \leadsto \qquad L &= \left\{\, \gamma(t) = \vec{x} + t(\vec{y} - \vec{x}) \;\middle|\; t \in \mathbb{R} \,\right\}
    = \left\{\, \tilde{\gamma}(t) = \vec{y} + 2t(\vec{x} - \vec{y}) \;\middle|\; t \in \mathbb{R} \,\right\} \\
    &= \left\{\, \hat{\gamma}(t) = \tfrac{1}{2}(\vec{x} + \vec{y}) + t(\vec{x} - \vec{y}) \;\middle|\; t \in \mathbb{R} \,\right\}
    \end{aligned}
    $$

    **Remark.** For any pair of affine parameterizations $\gamma, \tilde{\gamma}$ of a line $L$, the velocity vectors are proportional!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, LIGHT, ORANGE, RED, definition, mo, np, panel, patch, turntable):
    _x, _u, _v = np.array((0.0, 1.0, 1.0)), np.array((1.0, 2.0, 0.0)), np.array((-1.0, 3.0, 0.0))
    _p = _x + 0.6 * _u + 0.4 * _v  # phi(s, t) at s = 0.6, t = 0.4
    _plane = [(-1.6, -0.6, 1), (-1.6, 6.8, 1), (1.6, 6.8, 1), (1.6, -0.6, 1)]
    _rim = np.array(_plane + _plane[:1])
    # phi(1, 1) = x + u + v completes the parallelogram
    _par = np.array([_x + _u, _x + _u + _v, _x + _v])
    # x = (0, 1, 1): drop lines to the unit marks on the axes
    _guides = [((0, 0), (1, 1), (1, 0)), ((0, 0), (1, 0), (1, 1))]
    _marks = [((-0.1, 0.1), (1, 1), (0, 0)), ((-0.1, 0.1), (0, 0), (1, 1))]
    _fig = turntable(
        24,
        26,
        "the plane P through x in the directions of u and v, with the parallelogram spanned by u and v at x and a point phi(s, t) of P",
        [
            panel(
                1.0,
                surfaces=[patch(_plane, LIGHT, 0.35, n=12)],
                lines=[(_rim[:, 0], _rim[:, 1], _rim[:, 2], GREY, 1.0), (_par[:, 0], _par[:, 1], _par[:, 2], GREY, 1.0, [4, 3])]
                + [(*_g, GREY, 1.0, [4, 3]) for _g in _guides]
                + [(*_m, "#000000", 1.0) for _m in _marks],
                points=[(tuple(_p), ORANGE)],
                axes=[((-0.5, 0, 0), (2.2, 0, 0), "x^1", -135), ((0, -0.5, 0), (0, 7.2, 0), "x^2", 0), ((0, 0, -0.5), (0, 0, 2.1), "x^3", 90)],
                arrows=[((0, 0, 0), tuple(_x), "#000000"), (tuple(_x), tuple(_x + _u), BLUE), (tuple(_x), tuple(_x + _v), RED)],
                texts=[((0, 1, 0), "1", "#000000", -60, 6), ((0, 0, 1), "1", "#000000", 180, 6)],
            )
        ],
        legend=[
            ("area", LIGHT, "P", GREY, 0.35),
            ("line", "#000000", r"\vec{x}"),
            ("line", BLUE, r"\vec{u}"),
            ("line", RED, r"\vec{v}"),
            ("dot", ORANGE, r"\varphi(s, t)"),
        ],
        height=380,
        bias=0.25,
    )

    mo.vstack(
        [
            mo.md(r"""### Planes"""),
            definition(
                r"""
    Given $\vec{x}, \vec{u}, \vec{v} \in \mathbb{R}^3$, with $\vec{u}, \vec{v}$ not proportional, the **plane** through $\vec{x}$ in the directions of $\vec{u}$ and $\vec{v}$ is the set

    $$
    P = \left\{\, \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v} \;\middle|\; s, t \in \mathbb{R} \,\right\}
    $$

    ($\varphi : \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ is an **affine parameterization** of the plane).
    """,
                "Plane and affine parameterization",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    \vec{x} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \quad
    \vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad
    \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}
    \qquad \leadsto \qquad
    \varphi(s, t) = \begin{bmatrix} s - t \\ 1 + 2s + 3t \\ 1 \end{bmatrix}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** There exists a unique plane through $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^3$ if and only if $\vec{y} - \vec{x}$, $\vec{z} - \vec{x}$ are not proportional.

    $$
    P = \left\{\, \varphi(s, t) = \vec{x} + s(\vec{y} - \vec{x}) + t(\vec{z} - \vec{x}) \;\middle|\; s, t \in \mathbb{R} \,\right\}
    $$

    $\leadsto$ &nbsp; different parameterizations are also possible, with different starting points and directions
    """
            ),
            definition(
                r"""
    Given a plane $P = \left\{\, \vec{x} + s\vec{u} + t\vec{v} \;\middle|\; s, t \in \mathbb{R} \,\right\}$, a vector $\vec{n} \in \mathbb{R}^3$ is called **normal** to $P$ if

    $$
    \vec{n} \cdot \vec{u} = \vec{n} \cdot \vec{v} = 0 \qquad (\vec{n} \text{ is orthogonal to both directions in } P)
    $$
    """,
                "Normal vector",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, definition, mo, np, panel, patch, turntable):
    # u, v, w = u x v and -w, with the turn from u to v
    _u, _v = np.array((0.7, 1.3, 0.0)), np.array((-1.0, 1.0, 0.0))
    _w = np.cross(_u, _v)
    _a, _b = _u / np.linalg.norm(_u), _v / np.linalg.norm(_v)
    _om = np.arccos(_a @ _b)
    _s = np.linspace(0.1, 0.9, 40)[:, None] * _om
    _turn = 0.75 * (np.sin(_om - _s) * _a + np.sin(_s) * _b) / np.sin(_om)
    _fig = turntable(
        24,
        26,
        "the vectors u and v, their cross-product w = u x v orthogonal to both, minus w, and the turn from u to v through the angle theta",
        [
            panel(
                1.0,
                arrows=[((0, 0, 0), tuple(-_w), GREY, 1.8, [5, 4]), ((0, 0, 0), tuple(_w), GREEN), ((0, 0, 0), tuple(_u), BLUE), ((0, 0, 0), tuple(_v), RED)],
                arcs=[(_turn[:, 0], _turn[:, 1], _turn[:, 2], "#000000", 1.2)],
                texts=[(tuple(_turn[20]), r"\theta", "#000000", -60, 4)],
            )
        ],
        legend=[
            ("line", BLUE, r"\vec{u}"),
            ("line", RED, r"\vec{v}"),
            ("line", GREEN, r"\vec{w} = \vec{u} \times \vec{v}"),
            ("line", GREY, r"-\vec{w}", 1.8, [5, 4]),
        ],
        height=300,
    )

    # a plane through x with directions u, v and a normal vector
    _x, _n = np.array((0.4, 0.6, 1.4)), 0.7 * _w
    _plane = [_x + (_d1, _d2, 0) for _d1, _d2 in ((-1.5, -1.0), (-1.5, 1.9), (1.4, 1.9), (1.4, -1.0))]
    _rim = np.array(_plane + _plane[:1])
    _fig2 = turntable(
        24,
        26,
        "a plane P through x with the directions u and v, a normal vector n = alpha u x v, and the vector x from the origin",
        [
            panel(
                1.0,
                surfaces=[patch(_plane, LIGHT, 0.35, n=12)],
                lines=[(_rim[:, 0], _rim[:, 1], _rim[:, 2], GREY, 1.0)],
                points=[((0, 0, 0), "#000000")],
                arrows=[((0, 0, 0), tuple(_x), "#000000"), (tuple(_x), tuple(_x + _u), BLUE), (tuple(_x), tuple(_x + _v), RED), (tuple(_x), tuple(_x + _n), GREEN)],
            )
        ],
        legend=[
            ("area", LIGHT, "P", GREY, 0.35),
            ("dot", "#000000", r"\vec{0}"),
            ("line", "#000000", r"\vec{x}"),
            ("line", BLUE, r"\vec{u}"),
            ("line", RED, r"\vec{v}"),
            ("line", GREEN, r"\vec{n} = \alpha\, \vec{u} \times \vec{v}"),
        ],
        height=300,
        bias=0.25,
    )

    mo.vstack(
        [
            mo.md(r"""### The cross-product"""),
            definition(
                r"""
    Given two vectors $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}, \ \vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix} \in \mathbb{R}^3$, the **cross-product** of $\vec{u}$ and $\vec{v}$ is the unique vector $\vec{w} = \vec{u} \times \vec{v} \in \mathbb{R}^3$ such that

    $$
    \vec{u} \cdot \vec{w} = 0, \quad \vec{v} \cdot \vec{w} = 0 \qquad (\text{orthogonal to both } \vec{u}, \vec{v})
    $$

    $$
    \lVert \vec{w} \rVert^2 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2
    = \Big(\underbrace{\lVert \vec{u} \rVert\, \lVert \vec{v} \rVert \sin\!\big(\theta(\vec{u}, \vec{v})\big)}_{\text{area of parallelogram spanned by } \vec{u} \text{ and } \vec{v}}\Big)^2
    $$

    (if $\vec{u}, \vec{v}$ are proportional this forces $\vec{w} = \vec{0}$) and $\vec{u}, \vec{v}, \vec{w}$ is **right-handed** (positively oriented).
    """,
                "Cross-product",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; with your right hand: rotating your fingers from $\vec{u}$ to $\vec{v}$ points your thumb towards $\vec{w}$
    """
            ),
            _fig,
            mo.md(
                r"""
    Algebraically: $\vec{u}, \vec{v}, \vec{w}$ is right-handed if

    $$
    \det \begin{bmatrix} \vec{u} & \vec{v} & \vec{w} \end{bmatrix} > 0
    $$

    **Remark.** Given a parameterization

    $$
    \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}
    $$

    of a plane $P$, every normal vector to $P$ is proportional to the cross-product $\vec{u} \times \vec{v}$.
    """
            ),
            _fig2,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Computing the cross-product"""),
            theorem(
                r"""
    Given $\vec{u} = \begin{bmatrix} u^1 \\ u^2 \\ u^3 \end{bmatrix}$ and $\vec{v} = \begin{bmatrix} v^1 \\ v^2 \\ v^3 \end{bmatrix}$ in $\mathbb{R}^3$

    $$
    \begin{aligned}
    \vec{u} \times \vec{v} &= \underbrace{\det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ u^1 & u^2 & u^3 \\ v^1 & v^2 & v^3 \end{bmatrix}}_{\substack{\text{not an honest determinant!} \\ \text{1st row is made of vectors…}}}
    = \vec{e}_1 \det \begin{bmatrix} u^2 & u^3 \\ v^2 & v^3 \end{bmatrix} - \vec{e}_2 \det \begin{bmatrix} u^1 & u^3 \\ v^1 & v^3 \end{bmatrix} + \vec{e}_3 \det \begin{bmatrix} u^1 & u^2 \\ v^1 & v^2 \end{bmatrix} \\
    &= \vec{e}_1 (u^2 v^3 - u^3 v^2) - \vec{e}_2 (u^1 v^3 - u^3 v^1) + \vec{e}_3 (u^1 v^2 - u^2 v^1)
    = \begin{bmatrix} u^2 v^3 - u^3 v^2 \\ u^3 v^1 - u^1 v^3 \\ u^1 v^2 - u^2 v^1 \end{bmatrix} = \vec{w}
    \end{aligned}
    $$
    """,
                "Cross-product formula",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \vec{u} \cdot \vec{w} = u^1 (\cancel{u^2 v^3} - \bcancel{u^3 v^2}) + u^2 (\xcancel{u^3 v^1} - \cancel{u^1 v^3}) + u^3 (\bcancel{u^1 v^2} - \xcancel{u^2 v^1}) = 0, \qquad \vec{v} \cdot \vec{w} = 0
    $$

    $$
    \begin{aligned}
    \lVert \vec{w} \rVert^2 &= (u^2 v^3 - u^3 v^2)^2 + (u^3 v^1 - u^1 v^3)^2 + (u^1 v^2 - u^2 v^1)^2 \\
    &= \big( (u^1)^2 + (u^2)^2 + (u^3)^2 \big) \big( (v^1)^2 + (v^2)^2 + (v^3)^2 \big) - \big( u^1 v^1 + u^2 v^2 + u^3 v^3 \big)^2 \qquad (\text{check!}) \\
    &= \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2
    \end{aligned}
    $$

    $$
    \det \begin{bmatrix} u^1 & v^1 & (u^2 v^3 - u^3 v^2) \\ u^2 & v^2 & (u^3 v^1 - u^1 v^3) \\ u^3 & v^3 & (u^1 v^2 - u^2 v^1) \end{bmatrix} = \lVert \vec{w} \rVert^2 \geq 0 \qquad (\text{check!})
    $$

    This is strictly positive when $\vec{u}, \vec{v}$ are not proportional; otherwise $\vec{w} = \vec{0}$. $\square$

    **Example.** &nbsp; $\vec{u} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \quad \vec{v} = \begin{bmatrix} -1 \\ 3 \\ 0 \end{bmatrix}$

    $$
    \leadsto \qquad \vec{u} \times \vec{v} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 2 & 0 \\ -1 & 3 & 0 \end{bmatrix}
    = 0\, \vec{e}_1 + 0\, \vec{e}_2 + \big( 1 \cdot 3 - 2 \cdot (-1) \big)\, \vec{e}_3 = 5\, \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 5 \end{bmatrix}
    $$

    $$
    \vec{u} \cdot (\vec{u} \times \vec{v}) = 1 \cdot 0 + 2 \cdot 0 + 0 \cdot 5 = 0, \qquad
    \vec{v} \cdot (\vec{u} \times \vec{v}) = (-1) \cdot 0 + 3 \cdot 0 + 0 \cdot 5 = 0
    $$

    $$
    \lVert \vec{u} \times \vec{v} \rVert^2 = 25 = \lVert \vec{u} \rVert^2 \lVert \vec{v} \rVert^2 - (\vec{u} \cdot \vec{v})^2 = (1 + 4)(1 + 9) - (-1 + 6)^2 = 50 - 25
    $$

    $$
    \det \begin{bmatrix} 1 & -1 & 0 \\ 2 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix}
    = 1\, (3 \cdot 5 - 0 \cdot 0) - (-1)\, (2 \cdot 5 - 0 \cdot 0) + 0\, (2 \cdot 0 - 3 \cdot 0) = \underbrace{25}_{\lVert \vec{u} \times \vec{v} \rVert^2\,!} > 0
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _s(label, value):
        return mo.ui.slider(-3, 3, 0.5, value=value, label=label, show_value=True)

    u1, u2, u3 = _s("$u^1$", 1), _s("$u^2$", 2), _s("$u^3$", 0)
    v1, v2, v3 = _s("$v^1$", -1), _s("$v^2$", 3), _s("$v^3$", 0)
    return u1, u2, u3, v1, v2, v3


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, math, mo, np, panel, patch, table, turntable, u1, u2, u3, v1, v2, v3):
    _u = np.array((u1.value, u2.value, u3.value), float)
    _v = np.array((v1.value, v2.value, v3.value), float)
    _w = np.cross(_u, _v) + 0.0
    _norm = math.sqrt(_w @ _w)

    # the frame comes in three sizes (radius of the ball holding the scene, tick step), the smallest holding all
    # vectors: the scale stays fixed while the sliders move within it (|u x v| <= 25.5 for all slider values)
    _far = max(np.linalg.norm(_p) for _p in (_u, _v, _u + _v, _w))
    _R, _step = next(((_r, _k) for _r, _k in ((7, 1), (14, 2), (28, 5)) if _far <= 0.92 * _r), (28, 5))
    _len, _d = 0.8 * _R, 0.025 * _R
    # axis shafts drawn beneath vectors lying along them; heads and names by the axes primitive
    _shafts, _axes = [], []
    for _i, (_e, _deg) in enumerate(zip(np.eye(3), (180, -60, 90))):
        _s = np.array([-0.3 * _len * _e, 0.9 * _len * _e])
        _shafts.append((_s[:, 0], _s[:, 1], _s[:, 2], "#000000", 1.1, None, -0.1 * _R))
        _axes.append((tuple(0.9 * _len * _e), tuple(_len * _e), f"x^{_i + 1}", _deg))
    _marks, _ticks = [], []
    for _k in range(_step, int(0.85 * _len) + 1, _step):  # axis marks every `_step` units, every other one with its value
        for _i, (_across, _deg) in enumerate(((1, 180), (0, -90), (1, 180))):
            _c = _k * np.eye(3)[_i]
            _m = np.array([_c - _d * np.eye(3)[_across], _c + _d * np.eye(3)[_across]])
            _marks.append((_m[:, 0], _m[:, 1], _m[:, 2], "#000000", 1.0, None, -0.1 * _R))
            if _k % (2 * _step) == 0:
                _ticks.append((tuple(_c), f"{_k}", "#000000", _deg, 6))
    _arrows, _dots = [], []
    for _p, _colour in ((_w, GREEN), (_u, BLUE), (_v, RED)):
        if _p @ _p > 0:
            _arrows.append(((0, 0, 0), tuple(_p), _colour))
        else:  # a zero vector is a dot at the origin
            _dots.append(((0, 0, 0), _colour))
    _par = np.array([_u, _u + _v, _v])
    _b = _R / math.sqrt(3)
    _fig = turntable(
        35,
        24,
        "the vectors u and v, their cross-product u x v and the parallelogram spanned by u and v",
        [
            panel(
                1.0,
                surfaces=[patch([np.zeros(3), _u, _u + _v, _v], LIGHT, 0.7)],
                lines=[(_par[:, 0], _par[:, 1], _par[:, 2], GREY, 1.0, [4, 3])] + _shafts + _marks,
                points=_dots,
                axes=_axes,
                arrows=_arrows,
                texts=_ticks,
                box=((-_b, _b), (-_b, _b), (-_b, _b)),
            )
        ],
        legend=[
            ("line", BLUE, r"\vec{u}"),
            ("line", RED, r"\vec{v}"),
            ("line", GREEN, r"\vec{u} \times \vec{v}"),
            ("area", LIGHT, r"\text{parallelogram spanned by } \vec{u} \text{ and } \vec{v}", GREY, 0.7),
        ],
        height=420,
        key="lecture-05-cross",
    )

    def _col(vec, color):
        return rf"$\textcolor{{{color}}}{{\begin{{bmatrix}} {vec[0]:g} \\ {vec[1]:g} \\ {vec[2]:g} \end{{bmatrix}}}}$"

    mo.vstack(
        [
            mo.vstack(
                [
                    mo.hstack([u1, u2, u3], justify="start", gap=2, wrap=True),
                    mo.hstack([v1, v2, v3], justify="start", gap=2, wrap=True),
                ]
            ),
            table(
                [
                    (r"$\vec{u}, \ \vec{v}$", _col(_u, BLUE) + r", &nbsp; " + _col(_v, RED)),
                    (r"$\vec{u} \times \vec{v}$", _col(_w, GREEN)),
                    (r"$\lVert \vec{u} \times \vec{v} \rVert$ = area of the parallelogram", rf"${_norm:.3f}$"),
                ]
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
    **Remark.** The cross-product in $\mathbb{R}^3$ defines

    $$
    \times : \mathbb{R}^3 \times \mathbb{R}^3 \longrightarrow \mathbb{R}^3
    $$

    another extension of multiplication of vectors, now taking values in vectors!

    $\leadsto$ &nbsp; this **cannot** be extended to other $\mathbb{R}^n$ with $n \neq 3, 7$

    ### Properties of the cross-product
    """
            ),
            theorem(
                r"""
    Given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$, $\alpha, \beta \in \mathbb{R}$

    - $\vec{u} \times \vec{v} = -\vec{v} \times \vec{u}$ &nbsp; (**anti-commutativity**)
    - $\vec{u} \times (\alpha \vec{v} + \beta \vec{w}) = \alpha (\vec{u} \times \vec{v}) + \beta (\vec{u} \times \vec{w})$ and
      $(\alpha \vec{u} + \beta \vec{v}) \times \vec{w} = \alpha (\vec{u} \times \vec{w}) + \beta (\vec{v} \times \vec{w})$ &nbsp; (**bilinearity**)
    """,
                "Properties of the cross-product",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q2_1, q2_2, q2_3, q3_vol = (_field() for _ in range(4))
    return q2_1, q2_2, q2_3, q3_vol


@app.cell(hide_code=True)
def _(check, mo, q2_1, q2_2, q2_3, q3_vol):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $\vec{x} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 2 \\ -1 \\ 4 \end{bmatrix}, \; \gamma(t) = \vec{x} + t\vec{v}$.

    (a) Compute $\gamma(0)$, $\gamma(1)$, $\gamma(2)$.

    (b) Compute $\gamma(2) - \gamma(1)$.

    (c) Is $\vec{y} = \begin{bmatrix} 7 \\ -1 \\ 12 \end{bmatrix}$ in the line $L = \{\, \gamma(t) \mid t \in \mathbb{R} \,\}$?

    ### Question 2

    Let $\vec{u} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}, \; \vec{x} = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix}, \; \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v}$.

    (a) Compute $\vec{n} = \vec{u} \times \vec{v}$.
    """
            ),
            _ask(r"$n^1 =$", q2_1, 1),
            _ask(r"$n^2 =$", q2_2, -1),
            _ask(r"$n^3 =$", q2_3, 1),
            mo.md(
                r"""
    (b) Verify that every vector $\vec{y} \in P = \{\, \varphi(s, t) \mid s, t \in \mathbb{R} \,\}$ satisfies $(\vec{y} - \vec{x}) \cdot \vec{n} = 0$.

    (c) Write $(\vec{y} - \vec{x}) \cdot \vec{n} = 0$ as equations on $y^1, y^2, y^3$ and decide if $\vec{y} = \begin{bmatrix} 2 \\ 1 \\ 2 \end{bmatrix}$ and $\vec{y} = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$ are in $P$.

    ### Question 3

    Let $A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 1 \end{bmatrix}$.

    (a) Is $A$ invertible?

    (b) What is the volume of the parallelepiped spanned by the columns of $A$?
    """
            ),
            _ask(r"volume $=$", q3_vol, 2),
            mo.md(r"(c) Is $\vec{A}_1, \vec{A}_2, \vec{A}_3$ right-handed (positively oriented)?"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a line in $\mathbb{R}^3$ is $L = \{\, \gamma(t) = \vec{x} + t\vec{v} \mid t \in \mathbb{R} \,\}$ with $\vec{v}$ non-zero: starting point $\vec{x}$, velocity $\vec{v}$; parameterizations are not unique, but their velocities are proportional
    - a plane in $\mathbb{R}^3$ is $P = \{\, \varphi(s, t) = \vec{x} + s\vec{u} + t\vec{v} \mid s, t \in \mathbb{R} \,\}$ with $\vec{u}, \vec{v}$ not proportional; $\vec{n}$ is normal to $P$ if $\vec{n} \cdot \vec{u} = \vec{n} \cdot \vec{v} = 0$
    - the cross-product $\vec{w} = \vec{u} \times \vec{v}$ is orthogonal to both $\vec{u}, \vec{v}$, has $\lVert \vec{w} \rVert$ = area of the parallelogram spanned by $\vec{u}$ and $\vec{v}$, and $\vec{u}, \vec{v}, \vec{w}$ is right-handed: $\det \begin{bmatrix} \vec{u} & \vec{v} & \vec{w} \end{bmatrix} > 0$
    - $\vec{u} \times \vec{v}$ is computed as a formal $3 \times 3$ determinant with first row $\vec{e}_1, \vec{e}_2, \vec{e}_3$; every normal vector to $P$ is proportional to $\vec{u} \times \vec{v}$
    - the cross-product is anti-commutative and bilinear

    **Next:** multivariable functions
    """)
    return


if __name__ == "__main__":
    app.run()
