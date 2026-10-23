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
    header("Lecture 01", "Week 01", "Lecture 01 · The Cartesian n-space")
    return


@app.cell(hide_code=True)
def _():
    # ---- Helpers of this lecture ----------------------------------------
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
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## I.1 &nbsp; The Cartesian $n$-space

    **References:** MT 1.1, 1.5

    ### Points in $n$-space

    **Recall:** $\mathbb{R}$ (the line of real numbers) has two algebraic operations

    | addition | multiplication |
    |:---:|:---:|
    | $+ : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}$ | $\cdot : \mathbb{R} \times \mathbb{R} \longrightarrow \mathbb{R}$ |
    | $(\alpha, \beta) \longmapsto \alpha + \beta$ | $(\alpha, \beta) \longmapsto \alpha \cdot \beta$ |

    $\leadsto$ &nbsp; allow us to perform calculations with real numbers and real-valued functions and, eventually, allow us to define Calculus

    $\leadsto$ &nbsp; our first goal is to extend these operations from real numbers to collections of real numbers
    """
            ),
            definition(
                r"""
    For each $n \in \mathbb{Z}_{>0} = \{1, 2, 3, \dots\}$ (positive integers), we define the **Cartesian $n$-space** $\mathbb{R}^n$ as the set of all ordered lists of $n$ real numbers ($n$-tuples of real numbers)

    $$
    \mathbb{R}^n = \left\{\, \vec{x} = (x^1, x^2, \dots, x^n) \;\middle|\; x^i \in \mathbb{R},\ \forall\, i = 1, 2, \dots, n \,\right\}
    $$
    """,
                "Cartesian $n$-space",
            ),
            mo.md(
                r"""
    **Example.**

    | | | |
    |:--|:--|:--|
    | ${n = 1}$ | ${\mathbb{R}^1 = \mathbb{R} \ni x = (x^1)}$ | list of a single number (no need for arrows here) |
    | ${n = 2}$ | ${\mathbb{R}^2 = \mathbb{R} \times \mathbb{R} \ni \vec{x} = (x^1, x^2)}$ | ordered pairs of numbers (order matters! ${(x^1, x^2) \neq (x^2, x^1)}$ unless ${x^1 = x^2}$) |
    | ${n = 3}$ | ${\mathbb{R}^3 \ni \vec{x} = (x^1, x^2, x^3)}$ | ordered triples |
    | $\;\vdots$ | | |
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, arrow, legend_box, mo, panel, turntable):
    def _column(ax, x, y, entries, color, dy=0.3, w=0.2):
        """A column vector drawn by hand at (x, y): stacked entries between two square brackets."""
        n = len(entries)
        top, bot = y + dy * n / 2, y - dy * n / 2
        for k, e in enumerate(entries):
            ax.text(x, top - dy * (k + 0.5), e, color=color, fontsize=11, ha="center", va="center")
        for s in (-1, 1):
            ax.plot([x + s * (w - 0.07), x + s * w, x + s * w, x + s * (w - 0.07)], [top, top, bot, bot], color=color, lw=0.9)

    def spaces_figure(arrows):
        """R^1 and R^2 (drawn flat) beside R^3 (a rotatable view), with a point (arrows=False) or the arrow from
        the origin to it (arrows=True)."""
        fig = Figure(figsize=(4.6, 3.5 if not arrows else 2.9), layout="constrained")
        s1, s2 = fig.subfigures(1, 2)
        a1, a2 = s1.subplots(), s2.subplots()
        lo = -1.25 if not arrows else -0.6
        for ax in (a1, a2):
            ax.set_xlim(-0.5, 2.9)
            ax.set_ylim(lo, 2.75)
            ax.set_aspect("equal")
            ax.set_anchor("N")  # the two drawings start level, above legends of different heights
            ax.axis("off")

        # n = 1
        arrow(a1, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        a1.text(2.6, 0, r"$\mathbb{R}$", fontsize=12, va="center")
        if arrows:
            arrow(a1, (0, 0), (1.4, 0), BLUE)
            a1.text(0.7, 0.14, "$x$", color=BLUE, fontsize=12, ha="center")
        a1.plot(0, 0, "o", color="black", ms=5, zorder=4)
        a1.plot(1.4, 0, "o", color=BLUE, ms=5, zorder=4)
        legend_box(s1, [("dot", "black", "$0$"), ("dot", BLUE, "$x$")], loc="outside lower center")

        # n = 2
        p = (1.4, 1.5)
        arrow(a2, (-0.5, 0), (2.5, 0), "black", lw=0.9)
        arrow(a2, (0, -0.5), (0, 2.4), "black", lw=0.9)
        a2.text(2.6, 0, r"$\mathbb{R}$", fontsize=12, va="center")
        a2.text(0, 2.48, r"$\mathbb{R}$", fontsize=12, ha="center", va="bottom")
        if arrows:
            arrow(a2, (0, 0), p, BLUE)
            _column(a2, 1.3, 0.62, ("$x^1$", "$x^2$"), BLUE)
        else:
            a2.plot([p[0], p[0], 0], [0, p[1], p[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
            a2.text(p[0], -0.14, "$x^1$", fontsize=12, ha="center", va="top")
            a2.text(-0.12, p[1], "$x^2$", fontsize=12, ha="right", va="center")
        a2.plot(0, 0, "o", color="black", ms=5, zorder=4)
        a2.plot(*p, "o", color=BLUE, ms=5, zorder=4)
        legend_box(s2, [("dot", "black", "$(0, 0)$"), ("dot", BLUE, "$(x^1, x^2)$" if arrows else r"$\vec{x} = (x^1, x^2)$")], loc="outside lower center")

        if not arrows:
            for ax, n, name in ((a1, 1, "the real line"), (a2, 2, "the real plane")):
                ax.text(1.2, -0.72, f"$n = {n}$\n{name}", fontsize=12, ha="center", va="top", linespacing=1.4)

        # n = 3
        q = (1.0, 1.8, 1.6)
        axes = [((0 if arrows else -0.5, 0, 0), (2.1, 0, 0), r"\mathbb{R}", -150), ((0, -0.4, 0), (0, 2.3, 0), r"\mathbb{R}", 0), ((0, 0, -0.4), (0, 0, 2.1), r"\mathbb{R}", 90)]
        dots = [((0, 0, 0), "#000000"), (q, BLUE)]
        if arrows:
            space = panel(1.0, arrows=[((0, 0, 0), q, BLUE)], points=dots, axes=axes)
            legend = [("dot", "#000000", "(0, 0, 0)"), ("dot", BLUE, "(x^1, x^2, x^3)"), ("line", BLUE, r"\begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix}")]
            alt = "the arrow from the origin to the point (x1, x2, x3) in R3, written as a column vector"
        else:
            floor = (q[0], q[1], 0)
            guides = [(q, floor), (floor, (q[0], 0, 0)), (floor, (0, q[1], 0)), (q, (0, 0, q[2]))]
            space = panel(
                1.0,
                lines=[([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], GREY, 1.0, [4, 3]) for a, b in guides],
                points=dots,
                axes=axes,
                texts=[((q[0], 0, 0), "x^1", "#000000", 150), ((0, q[1], 0), "x^2", "#000000", 60), ((0, 0, q[2]), "x^3", "#000000", 180)],
                caption=r"\begin{gathered} n = 3 \\ \text{the real space} \end{gathered}",
            )
            legend = [("dot", "#000000", "(0, 0, 0)"), ("dot", BLUE, r"\vec{x} = (x^1, x^2, x^3)")]
            alt = "the real space R3: three axes through the origin and a point x = (x1, x2, x3), with dashed lines to its coordinates on the axes"
        view = turntable(30, 22, alt, [space], legend=legend, height=300)
        return mo.Html(
            '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem 1rem;">'
            f'<div style="flex: 1 1 300px; min-width: 260px;">{mo.as_html(fig).text}</div>'
            f'<div style="flex: 1 1 320px; min-width: 260px;">{view.text}</div></div>'
        )

    return (spaces_figure,)


@app.cell(hide_code=True)
def _(mo, spaces_figure):
    mo.vstack(
        [
            spaces_figure(False),
            mo.md(
                r"""
    $\leadsto$ &nbsp; geometrically, elements in $\mathbb{R}^n$ are points in an “$n$-dimensional” space with $n$ “orthogonal axes” intersecting at a single point (the origin)

    $\leadsto$ &nbsp; to extend the operations $+$ and $\cdot$ to $\mathbb{R}^n$, we need yet another way to think about its elements!

    ### Arrows from the origin
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

    $\leadsto$ &nbsp; in this course there is no fundamental difference between “points in space” and “arrows from the origin”

    $\leadsto$ &nbsp; we can think of it as a change in perspective

    $\leadsto$ &nbsp; when the distinction matters, we will use

    $$
    \vec{x} = (x^1, \dots, x^n) \ \text{ for points} \qquad \text{and} \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \ \text{ for arrows from the origin}
    $$

    ### Vector addition and scalar–vector multiplication
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
    \underbrace{\begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} + \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} = \begin{bmatrix} x^1 + y^1 \\ x^2 + y^2 \\ \vdots \\ x^n + y^n \end{bmatrix}}_{\text{component-wise addition}}
    \qquad \qquad
    \underbrace{\alpha \cdot \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \alpha x^2 \\ \vdots \\ \alpha x^n \end{bmatrix}}_{\text{component-wise multiplication}}
    $$
    """,
                "Vector addition and scalar–vector multiplication",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; note that multiplication is defined between real numbers (**scalars**) and elements in $\mathbb{R}^n$ (**$n$-vectors**)

    $\leadsto$ &nbsp; and the reason to use $n$-vectors (arrows from origin) here, instead of $n$-tuples (points in $n$-space), has to do with geometric interpretation
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
def _(BLUE, FULL, Figure, GREEN, GREY, ORANGE, RED, alpha, arrow, legend_box, mo, plane, table, x1, x2, y1, y2):
    _x = (x1.value, x2.value)
    _y = (y1.value, y2.value)
    _s = (_x[0] + _y[0], _x[1] + _y[1])
    _a = alpha.value
    _ax_ = (_a * _x[0], _a * _x[1])

    def _vector(ax, tip, color):
        """Arrow from the origin (a dot when the vector is zero)."""
        if tip[0] == 0 and tip[1] == 0:
            ax.plot(0, 0, "o", color=color, ms=4, zorder=4)
        else:
            arrow(ax, (0, 0), tip, color)

    _fig = Figure(figsize=(FULL, 4.1), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    plane(_left, 12)
    _left.plot([_x[0], _s[0], _y[0]], [_x[1], _s[1], _y[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _vector(_left, _s, GREEN)
    _vector(_left, _x, BLUE)
    _vector(_left, _y, RED)

    plane(_right, 12)
    _vector(_right, _ax_, ORANGE)
    _vector(_right, _x, BLUE)
    for _ax in (_left, _right):
        _ax.set_xticks(range(-8, 9, 4))
        _ax.set_yticks(range(-8, 9, 4))
    legend_box(_fig, [("line", BLUE, r"$\vec{x}$"), ("line", RED, r"$\vec{y}$"), ("line", GREEN, r"$\vec{x}+\vec{y}$"), ("line", ORANGE, r"$\alpha \cdot \vec{x}$")], loc="outside lower center", ncols=4)

    def _col(v, color):
        return rf"\textcolor{{{color}}}{{\begin{{bmatrix}} {v[0] + 0.0:g} \\ {v[1] + 0.0:g} \end{{bmatrix}}}}"

    mo.vstack(
        [
            mo.hstack([x1, x2, y1, y2, alpha], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{x} + \vec{y}$", rf"${_col(_x, BLUE)} + {_col(_y, RED)} = {_col(_s, GREEN)}$"),
                    (r"$\alpha \cdot \vec{x}$", rf"$({_a:g}) \cdot {_col(_x, BLUE)} = {_col(_ax_, ORANGE)}$"),
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
    $\leadsto$ &nbsp; we can interpret the operations in terms of arrows from the origin, not in terms of points

    $\leadsto$ &nbsp; these carry most of the properties of the usual addition and multiplication in $\mathbb{R}$
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
    """,
                "Properties of the operations",
            ),
            mo.md(r"**Proof.** Exercise! $\square$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $\mathbb{R}^n$ is the set of ordered lists $\vec{x} = (x^1, \dots, x^n)$ of $n$ real numbers: points in an $n$-dimensional space
    - every point is also a unique arrow from the origin, the $n$-vector $\vec{x}$ (a column matrix of size $n$)
    - vector addition and scalar–vector multiplication are defined component-wise, and are interpreted in terms of arrows from the origin
    - they are associative, distributive and commutative, with neutral and null operations, as in $\mathbb{R}$

    **Next:** the Euclidean inner product (the dot product)
    """)
    return


if __name__ == "__main__":
    app.run()
