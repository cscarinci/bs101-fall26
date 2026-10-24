import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 04 · Determinants, areas and volumes", css_file="bs101.css")


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
    header("Lecture 04", "Week 02", "Lecture 04 · Determinants, areas and volumes")
    return


@app.cell(hide_code=True)
def _(arrow, math):
    def vector(ax, tail, tip, color, label=None, turn=0, r=15, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip on a white box;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            arrow(ax, tail, tip, color, **kw)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

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

    return legend_box, vector


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
def _(mo):
    mo.md(r"""
    ## Last time

    - matrices $A \in \mathrm{Mat}(m \times n)$ &nbsp; $\leadsto$ &nbsp; linear transformation $A : \mathbb{R}^n \longrightarrow \mathbb{R}^m$, $\vec{x} \longmapsto A\vec{x}$ via matrix multiplication

        $$
        A = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \in \mathrm{Mat}(3 \times 2), \quad
        \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2
        \quad \Longrightarrow \quad A\vec{x}
        = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \\ e x^1 + f x^2 \end{bmatrix}
        = \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \in \mathbb{R}^3
        $$

    - standard basis vectors of $\mathbb{R}^2$: &nbsp; $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \ \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

        $$
        A\vec{e}_1 = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix}
        = \underbrace{\begin{bmatrix} a \\ c \\ e \end{bmatrix}}_{\text{1st column of } A} \in \mathbb{R}^3
        \qquad \qquad
        A\vec{e}_2 = \begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix}
        = \underbrace{\begin{bmatrix} b \\ d \\ f \end{bmatrix}}_{\text{2nd column of } A} \in \mathbb{R}^3
        $$

    - in general, $A \in \mathrm{Mat}(m \times n)$: &nbsp; $A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix}$, &nbsp; $\vec{A}_i = A\vec{e}_i \in \mathbb{R}^m$, where $\vec{e}_i \in \mathbb{R}^n$ is the standard basis of $\mathbb{R}^n$ (only one non-zero entry)
    - $\leadsto$ &nbsp; columns of $A$ are the images of the standard basis vectors via $A$!

    **In this lecture:** determinants of square matrices: areas, volumes, inverses and orientation

    **References:** MT 1.3, 1.5
    """)
    return


@app.cell(hide_code=True)
def _(Arc, BLUE, GREEN, GREY, HALF, LIGHT, RED, arrow, blank, definition, math, mo, theorem):
    _fig, _ax = blank(HALF, 2.1, (-0.5, 5.3), (-1.1, 2.0))
    _a1, _a2 = (2.6, -0.5), (2.0, 1.3)
    _ax.fill([0, _a1[0], _a1[0] + _a2[0], _a2[0]], [0, _a1[1], _a1[1] + _a2[1], _a2[1]], color=LIGHT, lw=0)
    _ax.plot([_a1[0], _a1[0] + _a2[0], _a2[0]], [_a1[1], _a1[1] + _a2[1], _a2[1]], color="black", lw=1.0)
    # the height: from the tip of A2 to its foot on the A1 direction, with a right-angle mark
    _t = (_a1[0] * _a2[0] + _a1[1] * _a2[1]) / (_a1[0] ** 2 + _a1[1] ** 2)
    _foot = (_t * _a1[0], _t * _a1[1])
    _ax.plot([_a2[0], _foot[0]], [_a2[1], _foot[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _n1 = math.hypot(*_a1)
    _u, _v = (_a1[0] / _n1, _a1[1] / _n1), (-_a1[1] / _n1, _a1[0] / _n1)
    _s = 0.14
    _ax.plot(
        [_foot[0] - _s * _u[0], _foot[0] - _s * _u[0] + _s * _v[0], _foot[0] + _s * _v[0]],
        [_foot[1] - _s * _u[1], _foot[1] - _s * _u[1] + _s * _v[1], _foot[1] + _s * _v[1]],
        color=GREY,
        lw=0.8,
    )
    arrow(_ax, (0, 0), _a1, BLUE)
    arrow(_ax, (0, 0), _a2, RED)
    _ax.text(_a1[0] / 2, _a1[1] / 2 - 0.16, r"$\vec{A}_1$", color=BLUE, fontsize=13, ha="center", va="top")
    _ax.text(_a2[0] / 2 - 0.12, _a2[1] / 2 + 0.14, r"$\vec{A}_2$", color=RED, fontsize=13, ha="right", va="bottom")
    _th1, _th2 = math.degrees(math.atan2(_a1[1], _a1[0])), math.degrees(math.atan2(_a2[1], _a2[0]))
    _ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=_th1, theta2=_th2, color=GREEN, lw=1.4))
    _ax.text(0.82, 0.12, r"$\theta$", color=GREEN, fontsize=13, ha="left", va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.4 &nbsp; Determinants, areas and volumes

    Let's focus, for now, on square matrices $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; linear transformations $A : \mathbb{R}^n \longrightarrow \mathbb{R}^n$ &nbsp; (mainly for $n = 2$ and $n = 3$)

    ### $n = 2$: determinants and areas
    """
            ),
            definition(
                r"""
    Given a $2 \times 2$ matrix

    $$
    A = \begin{bmatrix} A^1{}_1 & A^1{}_2 \\ A^2{}_1 & A^2{}_2 \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    $$

    the **determinant** of $A$ is the real number

    $$
    \det A = A^1{}_1 A^2{}_2 - A^1{}_2 A^2{}_1 = ad - bc
    $$
    """,
                r"Determinant of a $2 \times 2$ matrix",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; one of the main characteristics of a matrix

    $\leadsto$ &nbsp; used to determine if $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ admits an inverse

    $\leadsto$ &nbsp; measure of how $A$ “deforms” areas in $\mathbb{R}^2$
    """
            ),
            theorem(
                r"""
    For $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

    $$
    \lvert \det A \rvert = \text{area of parallelogram spanned by the columns of } A
    $$
    """,
                "Determinant and area",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$
    """
            ),
            _fig,
            mo.md(
                r"""
    If either column is zero, both the area and determinant are zero. Otherwise

    $$
    \begin{aligned}
    \text{area} &= (\text{base length}) \times (\text{height}) = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big) \qquad (\theta \in [0, \pi]) \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \Big( 1 - \cos\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \Big)^{1/2}
    = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \left( 1 - \left( \frac{\vec{A}_1 \cdot \vec{A}_2}{\lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert} \right)^{\!2} \right)^{1/2} \\
    &= \Big( \lVert \vec{A}_1 \rVert^2 \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2 \Big)^{1/2}
    = \Big( (a^2 + c^2)(b^2 + d^2) - (ab + cd)^2 \Big)^{1/2} \\
    &= \Big( \cancel{a^2 b^2} + a^2 d^2 + c^2 b^2 + \cancel{c^2 d^2} - \cancel{a^2 b^2} - \cancel{c^2 d^2} - 2abcd \Big)^{1/2} \\
    &= \big( a^2 d^2 - 2abcd + b^2 c^2 \big)^{1/2} = \big( (ad - bc)^2 \big)^{1/2} = \lvert \det A \rvert \qquad \square
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, ORANGE, RED, definition, mo, np, panel, patch, theorem, turntable):
    # The parallelepiped spanned by the columns: translucent faces, edges, the height of A3 over the base and the two angles
    _A = [np.array(v) for v in ((2.0, 0.0, 0.0), (0.3, 2.4, 0.0), (0.2, -1.0, 1.5))]
    _faces, _edges = [], []
    for _k in range(3):
        _p, _q, _r = _A[_k], _A[(_k + 1) % 3], _A[(_k + 2) % 3]
        _faces += [patch([_c, _c + _p, _c + _p + _q, _c + _q], LIGHT, 0.35) for _c in (0 * _r, _r)]
        _edges += [np.array([_c, _c + _p]) for _c in (_q, _r, _q + _r)]  # the edge along p at the origin is an arrow
    _foot = np.array([_A[2][0], _A[2][1], 0.0])

    def _arc(a, b, r):
        """The circular arc of radius r about the origin from the direction of a to the direction of b."""
        a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
        w = np.arccos(a @ b)
        s = np.linspace(0, 1, 40)[:, None]
        return r * (np.sin((1 - s) * w) * a + np.sin(s * w) * b) / np.sin(w)

    _theta, _phi = _arc(_A[0], _A[1], 0.5), _arc(_foot, _A[2], 0.8)
    _fig = turntable(
        -130,
        30,
        "parallelepiped spanned by the columns A1, A2, A3 of A, with the height of A3 over the base, the angle theta between A1 and A2 and the angle phi between A3 and the base",
        [
            panel(
                1.0,
                surfaces=_faces,
                lines=[(_e[:, 0], _e[:, 1], _e[:, 2], "#000000", 1.0) for _e in _edges]
                + [
                    ((_A[2][0], _foot[0]), (_A[2][1], _foot[1]), (_A[2][2], 0), GREY, 1.0, [4, 3]),
                    ((0, _foot[0]), (0, _foot[1]), (0, 0), GREY, 1.0, [4, 3]),
                    (_theta[:, 0], _theta[:, 1], _theta[:, 2], GREEN, 1.4),
                    (_phi[:, 0], _phi[:, 1], _phi[:, 2], GREEN, 1.4),
                ],
                arrows=[((0, 0, 0), tuple(_v), _c) for _v, _c in zip(_A, (BLUE, RED, ORANGE))],
                texts=[(tuple(_theta[28]), r"\theta", GREEN, 100, 3), (tuple(_phi[16]), r"\varphi", GREEN, -10, 4)],
            )
        ],
        legend=[
            ("line", BLUE, r"\vec{A}_1"),
            ("line", RED, r"\vec{A}_2"),
            ("line", ORANGE, r"\vec{A}_3"),
            ("area", LIGHT, r"\text{parallelepiped}", "#000000"),
        ],
        height=320,
        bias=0.15,
    )

    mo.vstack(
        [
            mo.md(r"""### $n = 3$: determinants and volumes"""),
            definition(
                r"""
    Given a $3 \times 3$ matrix

    $$
    A = \begin{bmatrix} A^1{}_1 & A^1{}_2 & A^1{}_3 \\ A^2{}_1 & A^2{}_2 & A^2{}_3 \\ A^3{}_1 & A^3{}_2 & A^3{}_3 \end{bmatrix}
    = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \in \mathrm{Mat}(3 \times 3)
    $$

    the **determinant** of $A$ is the real number

    $$
    \det A = a \det \begin{bmatrix} e & f \\ h & i \end{bmatrix} \underbrace{{} - b \det \begin{bmatrix} d & f \\ g & i \end{bmatrix}}_{\text{note the negative sign!}} + c \det \begin{bmatrix} d & e \\ g & h \end{bmatrix}
    $$
    """,
                r"Determinant of a $3 \times 3$ matrix",
            ),
            mo.md(
                r"""
    $$
    \begin{bmatrix} a & - & - \\ | & e & f \\ | & h & i \end{bmatrix}
    \qquad
    \begin{bmatrix} - & b & - \\ d & | & f \\ g & | & i \end{bmatrix}
    \qquad
    \begin{bmatrix} - & - & c \\ d & e & | \\ g & h & | \end{bmatrix}
    $$
    """
            ),
            theorem(
                r"""
    For $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leadsto$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

    $$
    \lvert \det A \rvert = \text{volume of the parallelepiped spanned by the columns of } A
    $$
    """,
                "Determinant and volume",
            ),
            mo.md(
                r"""
    **Proof** (sketch).

    $$
    A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \vec{A}_3 \end{bmatrix}, \quad
    \vec{A}_1 = \begin{bmatrix} a \\ d \\ g \end{bmatrix}, \
    \vec{A}_2 = \begin{bmatrix} b \\ e \\ h \end{bmatrix}, \
    \vec{A}_3 = \begin{bmatrix} c \\ f \\ i \end{bmatrix}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \begin{aligned}
    \text{volume} &= (\text{base area}) \times \text{height} = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\theta \times \lVert \vec{A}_3 \rVert \sin\varphi \\
    &= \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert\, \lVert \vec{A}_3 \rVert \sin\theta \sin\varphi = \cdots = \lvert \det A \rvert \qquad \square
    \end{aligned}
    $$

    ($\varphi$ = angle between a vector and a plane: we will need to define this more precisely!)

    **Remark.** We can continue up in dimension!

    - $A \in \mathrm{Mat}(n \times n)$ &nbsp; $\leadsto$ &nbsp; $\det A$ gets complicated quickly, but it can be defined!
    - $\lvert \det A \rvert = n$-volume of the $n$-parallelepiped spanned by its $n$ columns!
    - let's not do this explicitly!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Determinants and inverses"""),
            theorem(
                r"""
    $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear admits an **inverse** if and only if $\det A \neq 0$.

    - as a function: $\exists\, B : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ such that $A \circ B = B \circ A = \mathrm{id}_{\mathbb{R}^2}$, that is, $A \circ B(\vec{x}) = B \circ A(\vec{x}) = \vec{x} \quad \forall\, \vec{x} \in \mathbb{R}^2$
    - as a matrix: $\exists\, B \in \mathrm{Mat}(2 \times 2)$ such that $AB = BA = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$
    """,
                r"Invertible $2 \times 2$ matrices",
            ),
            mo.md(
                r"""
    **Proof** (brute force!). &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \quad B = \begin{bmatrix} e & f \\ g & h \end{bmatrix}$

    $$
    AB = \begin{bmatrix} ae + bg & af + bh \\ ce + dg & cf + dh \end{bmatrix}
    = BA = \begin{bmatrix} ea + fc & eb + fd \\ ga + hc & gb + hd \end{bmatrix}
    = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
    $$

    $$
    \Longleftrightarrow \qquad ad - bc \neq 0 \quad \text{and} \quad e = \frac{d}{ad - bc}, \quad f = -\frac{b}{ad - bc}, \quad g = -\frac{c}{ad - bc}, \quad h = \frac{a}{ad - bc}
    $$

    $\therefore$ &nbsp; $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ admits inverse if and only if $\det A = ad - bc \neq 0$ &nbsp; $\leadsto$ &nbsp; the inverse is

    $$
    B = A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \qquad \square
    $$

    $\leadsto$ &nbsp; key intuition:

    $$
    A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \qquad \Longrightarrow \qquad
    \vec{A}_1 = \begin{bmatrix} a \\ c \end{bmatrix} = A\vec{e}_1, \quad
    \vec{A}_2 = \begin{bmatrix} b \\ d \end{bmatrix} = A\vec{e}_2
    $$

    $\Longrightarrow$ &nbsp; parallelogram spanned by $\vec{A}_1, \vec{A}_2$ is the image of the unit square spanned by $\vec{e}_1, \vec{e}_2$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ma = mo.ui.slider(-3, 3, 0.5, value=2, label="$a$", show_value=True)
    mb = mo.ui.slider(-3, 3, 0.5, value=1, label="$b$", show_value=True)
    mc = mo.ui.slider(-3, 3, 0.5, value=0.5, label="$c$", show_value=True)
    md = mo.ui.slider(-3, 3, 0.5, value=2, label="$d$", show_value=True)
    return ma, mb, mc, md


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, RED, arrow, legend_box, ma, math, mb, mc, md, mo, plane, table, vector):
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c + 0.0

    def _turn(ax, p, q, ccw, radius):
        """Curved arrow from the direction of p to the direction of q."""
        t1, t2 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
        start = (radius * math.cos(t1), radius * math.sin(t1))
        end = (radius * math.cos(t2), radius * math.sin(t2))
        arrow(ax, start, end, GREEN, connectionstyle=f"arc3,rad={0.35 if ccw else -0.35}")

    _fig = Figure(figsize=(FULL, 4.4), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    plane(_left, 2.2)
    _left.set_xticks(range(-2, 3))
    _left.set_yticks(range(-2, 3))
    _left.fill([0, 1, 1, 0], [0, 0, 1, 1], color=LIGHT, lw=0)
    _left.plot([1, 1, 0], [0, 1, 1], color=GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_left, (0, 0), (1, 0), BLUE)
    vector(_left, (0, 0), (0, 1), RED)
    _turn(_left, (1, 0), (0, 1), True, 0.45)

    _small = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_a + _b), abs(_c + _d)) <= 3
    plane(_right, 4.4 if _small else 7.6)  # the frame follows the parallelogram: nothing is clipped
    _ticks = range(-4, 5, 2) if _small else range(-6, 7, 3)
    _right.set_xticks(_ticks)
    _right.set_yticks(_ticks)
    _right.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=LIGHT, lw=0)
    _right.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_right, (0, 0), (_a, _c), BLUE)
    vector(_right, (0, 0), (_b, _d), RED)
    legend_box(
        _fig,
        [
            ("line", BLUE, r"$\vec{e}_1$, $\vec{A}_1 = A\vec{e}_1$"),
            ("line", RED, r"$\vec{e}_2$, $\vec{A}_2 = A\vec{e}_2$"),
            ("area", LIGHT, r"unit square, $A$ (unit square)", GREY),
            ("line", GREEN, r"turn from $\vec{e}_1$ to $\vec{e}_2$, from $\vec{A}_1$ to $\vec{A}_2$"),
        ],
        loc="outside lower center",
        ncols=2,
    )
    if _det != 0:
        _r = 0.45 * min(math.hypot(_a, _c), math.hypot(_b, _d), 2.0)
        _turn(_right, (_a, _c), (_b, _d), _det > 0, max(_r, 0.3))
        _direction = rf"$\textcolor{{{GREEN}}}{{\text{{{'counter-clockwise' if _det > 0 else 'clockwise'}}}}}$"
    else:
        _direction = r"need $\det A \neq 0$"

    mo.vstack(
        [
            mo.hstack([ma, mb, mc, md], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$A = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 \end{bmatrix}$", rf"$\begin{{bmatrix}} \textcolor{{{BLUE}}}{{{_a:g}}} & \textcolor{{{RED}}}{{{_b:g}}} \\ \textcolor{{{BLUE}}}{{{_c:g}}} & \textcolor{{{RED}}}{{{_d:g}}} \end{{bmatrix}}$"),
                    (r"$\det A = ad - bc$", rf"$({_a:g})({_d:g}) - ({_b:g})({_c:g}) = {_det:g}$"),
                    (r"area of $A$ (unit square) $= \lvert \det A \rvert$", rf"${abs(_det):g}$"),
                    (r"turn from $\vec{A}_1$ to $\vec{A}_2$", _direction),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(GREEN, mo, np, panel, theorem, turntable):
    # The standard basis of R^3 as axes, with the turn of the fingers from e1 to e2 (right-hand rule)
    _s = np.radians(np.linspace(12, 78, 40))
    _fig = turntable(
        24,
        26,
        "the standard basis vectors e1, e2, e3 of R^3 as axes, with the turn from e1 to e2",
        [
            panel(
                1.0,
                axes=[((-0.4, 0, 0), (1.5, 0, 0), r"\vec{e}_1", -135), ((0, -0.4, 0), (0, 1.3, 0), r"\vec{e}_2", 0), ((0, 0, -0.4), (0, 0, 1.3), r"\vec{e}_3", 90)],
                arcs=[(0.75 * np.cos(_s), 0.75 * np.sin(_s), 0 * _s, GREEN)],
            )
        ],
        legend=[("line", GREEN, r"\text{turn from } \vec{e}_1 \text{ to } \vec{e}_2")],
        height=260,
    )

    mo.vstack(
        [
            mo.md(
                r"""
    If $\det A = 0$ &nbsp; $\Longrightarrow$ &nbsp; $A$ “collapses” the unit square into a line segment (or zero) &nbsp; $\leadsto$ &nbsp; a parallelogram of area zero

    $\Longrightarrow$ &nbsp; $A$ cannot be invertible &nbsp; $\leadsto$ &nbsp; we cannot “recover” the square from a line segment! (not bijective)

    If $\det A \neq 0$ &nbsp; $\Longrightarrow$ &nbsp; $A$ deforms the unit square without “collapse” &nbsp; $\leadsto$ &nbsp; linearity is then enough for us to find the inverse!
    """
            ),
            theorem(
                r"""
    For every $n \in \mathbb{Z}_{>0}$

    $$
    A \in \mathrm{Mat}(n \times n) \quad \leftrightsquigarrow \quad A : \mathbb{R}^n \longrightarrow \mathbb{R}^n \ \text{ linear}
    $$

    admits an inverse if and only if $\det A \neq 0$!
    """,
                r"Invertible $n \times n$ matrices",
            ),
            mo.md(
                r"""
    ### The sign of the determinant

    $\leadsto$ &nbsp; what about the sign of the determinant?
    """
            ),
            theorem(
                r"""
    $A \in \mathrm{Mat}(2 \times 2)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ linear

    - if $\det A > 0$, $A$ preserves the direction of rotations around the origin
    - if $\det A < 0$, $A$ reverses the direction of rotations around the origin

    $A \in \mathrm{Mat}(3 \times 3)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $A : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ linear

    - if $\det A > 0$, $A$ preserves “handedness” of orthogonal frames (triples of pairwise orthogonal vectors)
    - if $\det A < 0$, $A$ reverses “handedness”
    """,
                "Sign of the determinant",
            ),
            mo.md(
                r"""
    **Right-hand rule:** $\vec{e}_1, \vec{e}_2, \vec{e}_3$ have positive “handedness” (orientation): if rotating fingers from $\vec{e}_1$ to $\vec{e}_2$, your thumb points to $\vec{e}_3$
    """
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - for $A \in \mathrm{Mat}(2 \times 2)$, $\det A = ad - bc$ and $\lvert \det A \rvert$ = area of the parallelogram spanned by the columns of $A$ = area of the image of the unit square
    - for $A \in \mathrm{Mat}(3 \times 3)$, $\det A$ is defined via three $2 \times 2$ determinants (note the negative sign) and $\lvert \det A \rvert$ = volume of the parallelepiped spanned by the columns of $A$
    - $A \in \mathrm{Mat}(n \times n)$ admits an inverse if and only if $\det A \neq 0$
    - $\det A > 0$ preserves, and $\det A < 0$ reverses, the direction of rotations ($n = 2$) or the “handedness” of orthogonal frames ($n = 3$)
    """)
    return


if __name__ == "__main__":
    app.run()
