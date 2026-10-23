import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 07 · Local properties of paths", css_file="bs101.css")


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
    header("Lecture 07", "Week 04", "Lecture 07 · Local properties of paths")
    return


@app.cell(hide_code=True)
def _(np):
    def angle_mark(ax, angle, name, color):
        """The angle `angle` (radians, from the first axis) as an arc about the origin, which spirals outwards after a
        full turn; its `name` sits in the widest quadrant the last turn sweeps, so that it never lies on an axis."""
        th = np.linspace(0, angle, max(2, int(40 * angle)))
        r = 0.3 + 0.2 * np.maximum(th - 2 * np.pi, 0) / (2 * np.pi)
        ax.plot(r * np.cos(th), r * np.sin(th), color=color, lw=1.0)
        if angle < 0.5:
            return
        lo = max(0.0, angle - 2 * np.pi)
        a, b = max(((max(lo, k * np.pi / 2), min(angle, (k + 1) * np.pi / 2)) for k in range(8)), key=lambda p: p[1] - p[0])
        m = (a + b) / 2
        d = 0.5 + 0.2 * max(m - 2 * np.pi, 0) / (2 * np.pi)
        ax.text(d * np.cos(m), d * np.sin(m), name, color=color, fontsize=12, ha="center", va="center", bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

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

    return angle_mark, legend_box


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

    - multivariable functions $f : A \subseteq \mathbb{R}^n \longrightarrow B \subseteq \mathbb{R}^m$
    - $\leadsto$ &nbsp; global properties (image, graph, level sets)

    **In this lecture:** local properties of paths $\gamma : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}^m$: how a function behaves at a point (limits, continuity, differentiability)

    **References:** MT 2.2, 2.4
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.2 &nbsp; Local properties of paths

    ### Paths
    """
            ),
            definition(
                r"""
    A **path** in $\mathbb{R}^m$ is a function

    $$
    \begin{aligned}
    \gamma : A \subseteq \mathbb{R} &\longrightarrow \mathbb{R}^m \\
    t &\longmapsto \gamma(t) = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \\ \vdots \\ \gamma^m(t) \end{bmatrix}
    \end{aligned}
    $$
    """,
                "Path",
            ),
            mo.md(
                r"""
    **Remark.** Each component $\gamma^i : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}$ is a usual single variable real valued function!

    $\Longrightarrow$ &nbsp; paths are ordered lists of single variable scalar functions, like vectors were ordered lists of scalars!

    **Example.** $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^2$ an affine parameterization of a line

    $$
    \gamma(t) = \vec{x} + t\vec{v} = \begin{bmatrix} x^1 + t v^1 \\ x^2 + t v^2 \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
    \qquad \leadsto \qquad
    \underbrace{\gamma^1(t) = x^1 + t v^1, \quad \gamma^2(t) = x^2 + t v^2}_{\text{pair of affine single variable functions}}
    $$

    **Example.**

    $$
    \begin{aligned}
    \gamma : \mathbb{R} &\longrightarrow \mathbb{R}^2 \\
    t &\longmapsto \gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} = \begin{bmatrix} \gamma^1(t) \\ \gamma^2(t) \end{bmatrix}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; $\gamma^1 : \mathbb{R} \longrightarrow \mathbb{R}$, $t \longmapsto \cos(t)$ is the cosine function

    $\leadsto$ &nbsp; $\gamma^2 : \mathbb{R} \longrightarrow \mathbb{R}$, $t \longmapsto \sin(t)$ is the sine function

    $$
    \begin{aligned}
    \mathrm{Im}(\gamma) &= \left\{\, \begin{bmatrix} y^1 \\ y^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; \exists\, t \in \mathbb{R},\ y^1 = \gamma^1(t),\ y^2 = \gamma^2(t) \,\right\} \\
    &= \underbrace{\left\{\, \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; t \in \mathbb{R} \,\right\}}_{\text{unit circle } (y^1)^2 + (y^2)^2 = 1}
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \mathrm{graph}(\gamma) &= \left\{\, \begin{bmatrix} t \\ y^1 \\ y^2 \end{bmatrix} \in \mathbb{R} \times \mathbb{R}^2 = \mathbb{R}^3 \;\middle|\; t \in \mathbb{R},\ y^1 = \gamma^1(t),\ y^2 = \gamma^2(t) \,\right\} \\
    &= \underbrace{\left\{\, \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix} \in \mathbb{R}^3 \;\middle|\; t \in \mathbb{R} \,\right\}}_{\text{helix}}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_circle = mo.ui.slider(0, 12.5, 0.1, value=0.7, label="$t$", show_value=True)
    return (t_circle,)


@app.cell(hide_code=True)
def _(BLUE, GREY, HALF, angle_mark, arrow, blank, legend_box, math, mo, np, panel, t_circle, table, turntable):
    _t = t_circle.value
    _p = (math.cos(_t), math.sin(_t))
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    # Im(gamma): the unit circle, with the position gamma(t) in black as in every figure of the lecture
    _fig, _ax = blank(HALF + 1.2, 3.3, (-1.6, 2.0), (-1.6, 1.8))
    arrow(_ax, (-1.5, 0), (1.75, 0), "black", lw=0.9)
    arrow(_ax, (0, -1.5), (0, 1.6), "black", lw=0.9)
    _ax.text(1.8, -0.06, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.1, 1.62, "$y^2$", fontsize=13, ha="right", va="center")
    _th = np.linspace(0, 2 * np.pi, 361)
    _ax.plot(np.cos(_th), np.sin(_th), color=BLUE, lw=1.5)
    angle_mark(_ax, _t, "$t$", GREY)
    arrow(_ax, (0, 0), _p, "black")
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    legend_box(_fig, [("line", BLUE, r"$\mathrm{Im}(\gamma)$"), ("dot", "black", r"$\gamma(t)$")])

    # graph(gamma): the helix {(t, cos t, sin t)}, t to the right at a quarter of its length (so that two turns fit), y^1 towards the viewer
    _c = 0.25
    _s = np.linspace(-0.8, 13.0, 900)
    _ticks = [(_k * math.pi, _name) for _k, _name in ((1, r"\pi"), (2, r"2\pi"), (3, r"3\pi"), (4, r"4\pi"))]
    _graph = turntable(
        30,
        18,
        "graph of gamma, a helix in R x R^2 with the t-axis to the right, and its point (t, gamma(t))",
        [
            panel(
                1.0,
                lines=[(np.cos(_s), _c * _s, np.sin(_s), BLUE, 2.0)],
                points=[((_p[0], _c * _t, _p[1]), "#000000")] + [((0, _c * _k, 0), "#000000", 2.2) for _k, _ in _ticks],
                axes=[((0, -0.5, 0), (0, _c * 13.8, 0), "t", 0), ((-1.2, 0, 0), (1.5, 0, 0), "y^1", -120), ((0, 0, -1.2), (0, 0, 1.4), "y^2", 90)],
                texts=[((0, _c * _k, 0), _name, "#000000", -90) for _k, _name in _ticks],
            )
        ],
        legend=[("line", BLUE, r"\mathrm{graph}(\gamma)", 2.0), ("dot", "#000000", r"(t, \gamma(t))")],
        height=400,
        key="lecture-07-helix",
    )

    def _f(v):
        return f"{round(v, 2) + 0.0:.2f}"

    mo.vstack(
        [
            mo.hstack([t_circle], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\gamma(t)$", rf"$\begin{{bmatrix}} {_f(_p[0])} \\ {_f(_p[1])} \end{{bmatrix}}$"),
                    (r"$(t, \gamma(t))$", rf"$\begin{{bmatrix}} {_t:.1f} \\ {_f(_p[0])} \\ {_f(_p[1])} \end{{bmatrix}}$"),
                ]
            ),
            _fig,
            _graph,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** We can extend vector operations to paths. Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^m$, and $\lambda : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    \begin{aligned}
    \underbrace{(\gamma + \sigma)(t)}_{\text{addition of paths}} &= \underbrace{\gamma(t) + \sigma(t)}_{\text{addition of vectors}} && \leadsto \qquad \gamma + \sigma : \mathbb{R} \longrightarrow \mathbb{R}^m \\[26pt]
    \underbrace{(\lambda \gamma)(t)}_{\substack{\text{multiplication of scalar} \\ \text{function and a path}}} &= \underbrace{\lambda(t)\, \gamma(t)}_{\substack{\text{multiplication of} \\ \text{scalar and vector}}} && \leadsto \qquad \lambda \gamma : \mathbb{R} \longrightarrow \mathbb{R}^m \\[26pt]
    \underbrace{(\gamma \cdot \sigma)(t)}_{\text{dot product of paths}} &= \underbrace{\gamma(t) \cdot \sigma(t)}_{\text{dot product of vectors}} && \leadsto \qquad \gamma \cdot \sigma : \mathbb{R} \longrightarrow \mathbb{R} \\[26pt]
    \underbrace{(\gamma \times \sigma)(t)}_{\text{cross-product of paths in } \mathbb{R}^3} &= \underbrace{\gamma(t) \times \sigma(t)}_{\text{cross-product of vectors in } \mathbb{R}^3} && \leadsto \qquad \gamma \times \sigma : \mathbb{R} \longrightarrow \mathbb{R}^3 \quad (\text{if } m = 3) \\[10pt]
    \end{aligned}
    $$

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, \quad \sigma(t) = \begin{bmatrix} at + b \\ ct + d \end{bmatrix}, \quad \lambda(t) = \cos(t)$

    $$
    \begin{aligned}
    &\leadsto \qquad (\gamma + \sigma)(t) = \begin{bmatrix} \cos(t) + at + b \\ \sin(t) + ct + d \end{bmatrix} \\[4pt]
    &\leadsto \qquad (\gamma \cdot \sigma)(t) = \cos(t)(at + b) + \sin(t)(ct + d) \\[4pt]
    &\leadsto \qquad \lVert \gamma \rVert^2(t) = (\gamma \cdot \gamma)(t) = \cos(t)^2 + \sin(t)^2 = 1 \\[4pt]
    &\leadsto \qquad (\lambda \gamma)(t) = \begin{bmatrix} \cos(t)^2 \\ \cos(t) \sin(t) \end{bmatrix}
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Limits

    (how does a path behave as we “approach” a certain input?)
    """
            ),
            definition(
                r"""
    Given $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$, $a \in \mathbb{R}$ and $\vec{b} \in \mathbb{R}^m$ we say

    $$
    \lim_{t \to a} \gamma(t) = \vec{b} \qquad (\text{the limit of } \gamma \text{ as } t \text{ approaches } a \text{ is equal to } \vec{b})
    $$

    if we can make $\gamma(t)$ **arbitrarily** close to $\vec{b}$ (as close as we want) by taking $t$ **sufficiently** close to $a$ (as close as we need), but different from $a$ (we don't even need $\gamma$ to be defined at $t = a$ to talk about limits).
    """,
                "Limit of a path",
            ),
            mo.md(
                r"""
    Choose how close to $\vec{b}$ you would like &nbsp; $\leadsto$ &nbsp; want $\lVert \gamma(t) - \vec{b} \rVert < \varepsilon$, for $\varepsilon > 0$.

    Can we achieve this, by taking $t$ close enough to $a$? &nbsp; $\leadsto$ &nbsp; can we find $\delta > 0$ such that

    $$
    0 < \lvert t - a \rvert < \delta \qquad \Longrightarrow \qquad \lVert \gamma(t) - \vec{b} \rVert < \varepsilon \ ?
    $$

    Can we do this for every $\varepsilon > 0$? If yes, then $\displaystyle \lim_{t \to a} \gamma(t) = \vec{b}$!
    """
            ),
            theorem(
                r"""
    Limit of paths can be calculated componentwise

    $$
    \lim_{t \to a} \gamma(t) = \vec{b} \qquad \Longleftrightarrow \qquad \lim_{t \to a} \gamma^i(t) = b^i \quad \forall\, i = 1, 2, \dots, m
    $$
    """,
                "Limits componentwise",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

    $$
    \lim_{t \to \pi/2} \gamma(t) = \begin{bmatrix} \displaystyle \lim_{t \to \pi/2} \cos(t) \\[8pt] \displaystyle \lim_{t \to \pi/2} \sin(t) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    $$

    **Remark.** Limits are unique, provided they exist!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, definition, math, mo, np, panel, theorem, turntable):
    # graph(gamma) as above, with a gap at t = 0: its limit point (1, 0) is not gamma(0) = (0, 1)
    _c = 0.25
    _ticks = [(_k * math.pi, _name) for _k, _name in ((-1, r"-\pi"), (1, r"\pi"), (2, r"2\pi"))]
    _lines = [(np.cos(_s), _c * _s, np.sin(_s), BLUE, 2.0) for _s in (np.linspace(-4.2, -0.1, 300), np.linspace(0.1, 8.6, 600))]
    _fig = turntable(
        30,
        18,
        "graph of gamma, a helix in R x R^2 with a gap at t = 0, the limit point (0, (1, 0)) and the point (0, gamma(0)) = (0, (0, 1))",
        [
            panel(
                1.0,
                lines=_lines,
                points=[((1, 0, 0), "#000000", 4.5, True), ((0, 0, 1), "#000000")] + [((0, _c * _k, 0), "#000000", 2.2) for _k, _ in _ticks],
                axes=[((0, _c * -4.8, 0), (0, _c * 9.2, 0), "t", 0), ((-1.2, 0, 0), (1.5, 0, 0), "y^1", -120), ((0, 0, -1.2), (0, 0, 1.4), "y^2", 90)],
                texts=[((0, _c * _k, 0), _name, "#000000", -90) for _k, _name in _ticks],
            )
        ],
        legend=[("line", BLUE, r"\mathrm{graph}(\gamma)", 2.0), ("ring", "#000000", r"(0, \lim_{t \to 0} \gamma(t))"), ("dot", "#000000", r"(0, \gamma(0))")],
        height=400,
    )

    mo.vstack(
        [
            mo.md(r"""### Continuity"""),
            definition(
                r"""
    A path $\gamma$ is **continuous** at $t = a$ if

    $$
    \lim_{t \to a} \gamma(t) = \gamma(a)
    $$

    $\gamma$ is continuous in $(a_1, a_2) \subset \mathbb{R}$ if it is continuous at every $t \in (a_1, a_2)$.
    """,
                "Continuity of a path",
            ),
            theorem(
                r"""
    A path is continuous if and only if all of its components are continuous

    $$
    \lim_{t \to a} \gamma(t) = \gamma(a) \qquad \Longleftrightarrow \qquad \lim_{t \to a} \gamma^i(t) = \gamma^i(a) \quad \forall\, i = 1, 2, \dots, m
    $$
    """,
                "Continuity componentwise",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    \gamma(t) = \begin{cases}
    \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}, & t \neq 0 \\[12pt]
    \begin{bmatrix} 0 \\ 1 \end{bmatrix}, & t = 0
    \end{cases}
    $$
    """
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Differentiability"""),
            definition(
                r"""
    A path $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is **differentiable** at $t = a$ if

    $$
    \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} \quad \text{exists.}
    $$

    $\leadsto$ &nbsp; if it exists we call it the **derivative** of $\gamma$ at $t = a$ and denote it $\gamma'(a)$
    """,
                "Derivative of a path",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; we also call $\gamma'(a)$ the **velocity** of the path $\gamma$ at $t = a$ &nbsp; ($\gamma(a)$ is the **position** of $\gamma$ at $t = a$)

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$

    $$
    \begin{aligned}
    \gamma'(a) &= \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a} = \lim_{t \to a} \begin{bmatrix} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix}
    = \begin{bmatrix} \displaystyle \lim_{t \to a} \dfrac{\gamma^1(t) - \gamma^1(a)}{t - a} \\[10pt] \displaystyle \lim_{t \to a} \dfrac{\gamma^2(t) - \gamma^2(a)}{t - a} \end{bmatrix} \\[6pt]
    &= \begin{bmatrix} \dfrac{d}{dt} \cos(t) \Big|_{t = a} \\[10pt] \dfrac{d}{dt} \sin(t) \Big|_{t = a} \end{bmatrix} = \begin{bmatrix} -\sin(a) \\ \cos(a) \end{bmatrix}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_circle = mo.ui.slider(0, 6.25, 0.05, value=0.8, label="$a$", show_value=True)
    return (a_circle,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, a_circle, angle_mark, arrow, blank, legend_box, math, mo, np, table):
    _a = a_circle.value
    _p = (math.cos(_a), math.sin(_a))
    _v = (-math.sin(_a), math.cos(_a))
    _tip = (_p[0] + _v[0], _p[1] + _v[1])

    _fig, _ax = blank(HALF + 1.3, 3.4, (-2.0, 2.25), (-2.1, 2.15))
    arrow(_ax, (-1.9, 0), (1.95, 0), "black", lw=0.9)
    arrow(_ax, (0, -1.9), (0, 1.95), "black", lw=0.9)
    _ax.text(2.0, -0.08, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(0.1, 1.98, "$y^2$", fontsize=13, ha="left", va="center")
    _th = np.linspace(0, 2 * np.pi, 361)
    _ax.plot(np.cos(_th), np.sin(_th), color=BLUE, lw=1.5)
    angle_mark(_ax, _a, "$a$", GREY)
    arrow(_ax, (0, 0), _p, "black")
    arrow(_ax, _p, _tip, GREEN)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    legend_box(_fig, [("line", BLUE, r"$\mathrm{Im}(\gamma)$"), ("dot", "black", r"$\gamma(a)$"), ("line", GREEN, r"$\gamma'(a)$")])

    def _f(v):
        return f"{round(v, 2) + 0.0:.2f}"

    mo.vstack(
        [
            mo.hstack([a_circle], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"position $\gamma(a)$", rf"$\begin{{bmatrix}} {_f(_p[0])} \\ {_f(_p[1])} \end{{bmatrix}}$"),
                    (r"velocity $\gamma'(a)$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_f(_v[0])} \\ {_f(_v[1])} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Derivatives of paths can be computed componentwise

    $$
    \gamma'(a) = \vec{v} \qquad \Longleftrightarrow \qquad \frac{d}{dt} \gamma^i(t) \Big|_{t = a} = v^i \quad \forall\, i = 1, 2, \dots, m
    $$
    """,
                "Derivatives componentwise",
            ),
            definition(
                r"""
    If $\gamma : \mathbb{R} \longrightarrow \mathbb{R}^m$ is differentiable at $t = a$ with velocity vector $\gamma'(a) \neq \vec{0}$, we call the line through $\vec{x} = \gamma(a)$ in the direction of $\vec{v} = \gamma'(a)$ the **tangent line** to $\gamma$ at $t = a$

    $$
    T_a \gamma = \left\{\, \vec{y} = \gamma(a) + s\, \gamma'(a) \;\middle|\; s \in \mathbb{R} \,\right\}
    $$
    """,
                "Tangent line",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} t^2 \\ t \end{bmatrix} \quad \leadsto \quad \gamma'(t) = \begin{bmatrix} 2t \\ 1 \end{bmatrix}$

    $$
    T_a \gamma = \left\{\, \vec{y} = \begin{bmatrix} a^2 \\ a \end{bmatrix} + s \begin{bmatrix} 2a \\ 1 \end{bmatrix} \;\middle|\; s \in \mathbb{R} \,\right\}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_parabola = mo.ui.slider(-1.5, 1.5, 0.1, value=0.7, label="$a$", show_value=True)
    return (a_parabola,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, ORANGE, a_parabola, arrow, blank, legend_box, mo, np, table):
    _a = a_parabola.value
    _p, _v = (_a**2, _a), (2 * _a, 1.0)
    _tip = (_p[0] + _v[0], _p[1] + _v[1])

    _fig, _ax = blank(FULL, 4.6, (-3.6, 6.4), (-2.7, 3.0))
    arrow(_ax, (-3.4, 0), (6.1, 0), "black", lw=0.9)
    arrow(_ax, (0, -2.6), (0, 2.8), "black", lw=0.9)
    _ax.text(6.15, -0.1, "$y^1$", fontsize=13, ha="center", va="top")
    _ax.text(-0.12, 2.8, "$y^2$", fontsize=13, ha="right", va="center")
    _t = np.linspace(-2.45, 2.45, 300)
    _ax.plot(_t**2, _t, color=BLUE, lw=1.5)
    _s = np.array([-12.0, 12.0])
    _ax.plot(_p[0] + _s * _v[0], _p[1] + _s * _v[1], color=ORANGE, lw=1.0 if _a != 0 else 2.0, zorder=2 if _a != 0 else 3)  # at a = 0 it lies on the y^2-axis: drawn wider, over it
    arrow(_ax, _p, _tip, GREEN)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=4)
    legend_box(
        _fig,
        [("line", BLUE, r"$\mathrm{Im}(\gamma)$"), ("dot", "black", r"$\gamma(a)$"), ("line", GREEN, r"$\gamma'(a)$"), ("line", ORANGE, r"$T_a\gamma$")],
        loc="outside lower center",
        ncols=4,
    )

    mo.vstack(
        [
            mo.hstack([a_parabola], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"position $\gamma(a)$", rf"$\begin{{bmatrix}} {_p[0] + 0.0:.2f} \\ {_p[1] + 0.0:g} \end{{bmatrix}}$"),
                    (r"velocity $\gamma'(a)$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {_v[0] + 0.0:g} \\ 1 \end{{bmatrix}}}}$"),
                    (
                        r"tangent line $T_a \gamma$",
                        rf"$\textcolor{{{ORANGE}}}{{\left\{{\, \vec{{y}} = \begin{{bmatrix}} {_p[0] + 0.0:.2f} \\ {_p[1] + 0.0:g} \end{{bmatrix}} + s \begin{{bmatrix}} {_v[0] + 0.0:g} \\ 1 \end{{bmatrix}} \;\middle\vert\; s \in \mathbb{{R}} \,\right\}}}}$",
                    ),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q1_a, q1_b = _field(), _field()
    return q1_a, q1_b


@app.cell(hide_code=True)
def _(check, mo, q1_a, q1_b):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let

    $$
    \gamma(t) = \begin{cases}
    \begin{bmatrix} t \\ \dfrac{\sin(t)}{t} \end{bmatrix}, & t \neq 0 \\[14pt]
    \begin{bmatrix} a \\ b \end{bmatrix}, & t = 0
    \end{cases}
    $$

    (a) Find $\displaystyle \lim_{t \to 0} \gamma(t)$.

    (b) Find $a, b \in \mathbb{R}$ such that $\gamma$ is continuous at $t = 0$.
    """
            ),
            _ask(r"$a =$", q1_a, 0),
            _ask(r"$b =$", q1_b, 1),
            mo.md(
                r"""
    ### Question 2

    Consider $\sigma : \mathbb{R} \longrightarrow \mathbb{R}^3$, $\sigma(t) = \begin{bmatrix} t \\ \cos(t) \\ \sin(t) \end{bmatrix}$ and $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$, $f(\vec{x}) = (x^2)^2 + (x^3)^2$.

    (a) Show that $\mathrm{Im}(\sigma) \subseteq f^{-1}(1)$.

    (b) Compute $\sigma'(t)$, and find an affine parameterization of the tangent line to $\sigma$ at $t = 0$.

    (c) Is the entire tangent line contained in $f^{-1}(1)$? Justify your answers!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a path $\gamma : A \subseteq \mathbb{R} \longrightarrow \mathbb{R}^m$ is an ordered list of single variable functions $\gamma^1, \dots, \gamma^m$; vector operations extend to paths
    - $\lim_{t \to a} \gamma(t) = \vec{b}$: we can make $\gamma(t)$ arbitrarily close to $\vec{b}$ by taking $t$ sufficiently close to $a$ (but different from $a$); $\gamma$ is continuous at $t = a$ if

        $$
        \lim_{t \to a} \gamma(t) = \gamma(a)
        $$
    - the derivative (velocity)

        $$
        \gamma'(a) = \lim_{t \to a} \frac{\gamma(t) - \gamma(a)}{t - a}
        $$

        $\gamma(a)$ is the position
    - limits, continuity and derivatives of paths can be computed componentwise
    - if $\gamma'(a) \neq \vec{0}$, the tangent line to $\gamma$ at $t = a$ is

        $$
        T_a \gamma = \{\, \vec{y} = \gamma(a) + s\, \gamma'(a) \mid s \in \mathbb{R} \,\}
        $$

    **Next:** local properties of scalar functions and maps: limits
    """)
    return


if __name__ == "__main__":
    app.run()
