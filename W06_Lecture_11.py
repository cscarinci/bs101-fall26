import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 11 · Affine approximations and the derivative of general maps", css_file="bs101.css")


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
    header("Lecture 11", "Week 06", "Lecture 11 · Affine approximations and the derivative of general maps")
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

    return (vector,)


@app.cell(hide_code=True)
def _(arrow, math):
    # ---- Helpers of this lecture ----------------------------------------
    def cross_axes(ax, xr, yr, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin, drawn over the ranges xr and yr."""
        arrow(ax, (xr[0], 0), (xr[1], 0), "black", lw=0.9)
        arrow(ax, (0, yr[0]), (0, yr[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xr[1], 0), textcoords="offset points", xytext=(0, -6), ha="right", va="top", fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, yr[1]), textcoords="offset points", xytext=(6, 0), ha="left", va="top", fontsize=13)

    def tip_label(ax, at, angle, text, color, r=7, fontsize=13):
        """Label next to the point `at`, pushed away from it in the direction `angle` (degrees);
        the text is anchored on the side facing the point, so that long labels never run back over it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ha = "left" if c > 0.35 else "right" if c < -0.35 else "center"
        va = "bottom" if s > 0.35 else "top" if s < -0.35 else "center"
        ax.annotate(text, at, textcoords="offset points", xytext=(r * c, r * s), ha=ha, va=va, color=color, fontsize=fontsize, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    def num(v, digits=2):
        """Fixed-point number for the readout tables (never prints a negative zero)."""
        return f"{round(v, digits) + 0.0:.{digits}f}"

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

    return cross_axes, legend_box, num, tip_label


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
    phi = mo.ui.slider(0, 355, 5, value=40, label=r"parameter $\varphi$ of $\vec{a} = (3\cos\varphi, 2\sin\varphi)$ on the ellipse (degrees)", show_value=True)
    return (phi,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, arrow, blank, cross_axes, math, mo, np, num, phi, table, tip_label):
    _p = math.radians(phi.value)
    _a = (3 * math.cos(_p), 2 * math.sin(_p))
    _grad = (2 * _a[0] / 9, 2 * _a[1] / 4)
    _tip = (_a[0] + _grad[0], _a[1] + _grad[1])
    _dir = math.degrees(math.atan2(_grad[1], _grad[0]))

    _fig, _ax = blank(FULL, 5.5, (-4.75, 5.0), (-3.55, 3.7))
    cross_axes(_ax, (-4.5, 4.9), (-3.4, 3.6), "$x^1$", "$x^2$")
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(3 * np.cos(_th), 2 * np.sin(_th), color=BLUE, lw=1.4)
    _q = _p + math.pi + 0.6  # the name of the level set sits on the ellipse, away from a and its gradient
    tip_label(_ax, (3 * math.cos(_q), 2 * math.sin(_q)), math.degrees(math.atan2(math.sin(_q) / 2, math.cos(_q) / 3)), "$f^{-1}(r^2)$", BLUE)
    arrow(_ax, (0, 0), _a, "black")
    tip_label(_ax, (_a[0] / 2, _a[1] / 2), math.degrees(_p) + 90, r"$\vec{a}$", "black")
    arrow(_ax, _a, _tip, GREEN)
    tip_label(_ax, _tip, _dir + 40, r"$\vec{\nabla} f(\vec{a})$", GREEN)
    _ax.plot(*_a, "o", color="black", ms=4, zorder=4)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    The derivative and the gradient

    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$ &nbsp; $\Longleftrightarrow$ &nbsp; $Df(\vec{a}) = \begin{bmatrix} \frac{\partial f}{\partial x^1}(\vec{a}) & \cdots & \frac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)$ defines a good affine approximation for $f$ at $\vec{a}$ in the sense that

        $$
        \lim_{\vec{x} \to \vec{a}} \frac{f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a})}{\lVert \vec{x} - \vec{a} \rVert} = 0
        $$

    - $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}$ is the **derivative** of $f$ at $\vec{a}$ (linear function taking vectors to directional derivatives)
    - $\vec{\nabla} f(\vec{a}) \in \mathbb{R}^n$, the column of the partial derivatives $\frac{\partial f}{\partial x^1}(\vec{a}), \dots, \frac{\partial f}{\partial x^n}(\vec{a})$, is the **gradient** of $f$ at $\vec{a}$ (vector pointing in some direction with some length)
    - theorem: $\vec{\nabla} f(\vec{a})$ (if not $\vec{0}$) points in the direction of steepest ascent of $f$ at $\vec{a}$, and it is perpendicular to the level set of $f$ through $\vec{a}$ (containing $\vec{a}$)
    - example: $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \dfrac{(x^1)^2}{9} + \dfrac{(x^2)^2}{4}$ &nbsp; $\leadsto$ &nbsp; level sets and gradient

        $$
        f^{-1}(r^2) = \underbrace{\left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; \frac{(x^1)^2}{9 r^2} + \frac{(x^2)^2}{4 r^2} = 1 \,\right\}}_{\text{horizontal ellipse centered at } \vec{0} \text{ with semi-axes } 3r \text{ and } 2r} \quad (r > 0),
        \qquad
        \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \frac{2}{9} a^1 \\[4pt] \frac{2}{4} a^2 \end{bmatrix}
        $$
    """
            ),
            mo.hstack([phi], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"semi-axes $3r$ and $2r$ of the level set $\textcolor{" + BLUE + r"}{f^{-1}(r^2)}$, with $r = 1$", r"$3$ and $2$"),
                    (r"$\vec{a}$", rf"$\begin{{bmatrix}} {num(_a[0])} \\ {num(_a[1])} \end{{bmatrix}}$"),
                    (r"$\vec{\nabla} f(\vec{a})$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} {num(_grad[0])} \\ {num(_grad[1])} \end{{bmatrix}}}}$"),
                ]
            ),
            _fig,
            mo.md(
                r"""
    **In this lecture:** affine approximations and their graphs; derivative for general maps $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$

    **References:** MT 2.3
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.6 &nbsp; Affine approximations and the derivative of general maps

    ### Affine approximations
    """
            ),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ differentiable at $\vec{a} \in \mathbb{R}^n$, the **affine approximation** of $f$ at $\vec{a}$ is the affine function (linear plus constant) $g : \mathbb{R}^n \longrightarrow \mathbb{R}$

    $$
    g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})
    = f(\vec{a}) + \frac{\partial f}{\partial x^1}(\vec{a})\, (x^1 - a^1) + \dots + \frac{\partial f}{\partial x^n}(\vec{a})\, (x^n - a^n)
    $$
    """,
                "Affine approximation",
            ),
            mo.md(
                r"""
    **Remark.** For $n = 1$, $f : \mathbb{R} \longrightarrow \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $g : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    g(x) = f(a) + f'(a)(x - a)
    $$

    is the affine function whose graph is the tangent line to the graph of $f$ at $\begin{bmatrix} a \\ f(a) \end{bmatrix}$

    $$
    y = f(a) + f'(a)(x - a) \qquad \leadsto \qquad \begin{bmatrix} a \\ f(a) \end{bmatrix} + (x - a) \underbrace{\begin{bmatrix} 1 \\ f'(a) \end{bmatrix}}_{\substack{\text{velocity vector of} \\ \text{the tangent line}}}
    \qquad \qquad
    \underbrace{\vec{n} = \begin{bmatrix} -f'(a) \\ 1 \end{bmatrix}}_{\substack{\text{normal to the} \\ \text{tangent line}}}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_line = mo.ui.slider(0.4, 3.4, 0.1, value=0.7, label="$a$", show_value=True)
    return (a_line,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, ORANGE, a_line, arrow, blank, cross_axes, legend_box, math, mo, np, num, table, tip_label):
    _a = a_line.value
    _fa = 4 * _a * math.exp(-_a)
    _d = 4 * (1 - _a) * math.exp(-_a)
    _slope = math.degrees(math.atan2(_d, 1))

    _fig, _ax = blank(FULL, 3.9, (-1.75, 6.25), (-0.6, 3.1))
    cross_axes(_ax, (-1.7, 6.2), (-0.5, 3.0), "$x$", "$y$")
    _x = np.linspace(-0.1, 5.1, 300)
    _ax.plot(_x, 4 * _x * np.exp(-_x), color=BLUE, lw=1.4)
    _ax.text(5.2, 0.34, "$y = f(x)$", color=BLUE, fontsize=13, ha="left", va="center")
    # the tangent line, as far as it stays inside the frame
    _s = np.linspace(-1.7, 5.2, 400)
    _t = _fa + _d * (_s - _a)
    _in = (_t > -0.5) & (_t < 3.0)
    _ax.plot(_s[_in], _t[_in], color=GREEN, lw=1.0)
    arrow(_ax, (0, 0), (_a, _fa), "black")
    arrow(_ax, (_a, _fa), (_a + 1, _fa + _d), GREEN)
    arrow(_ax, (_a, _fa), (_a - _d, _fa + 1), ORANGE)
    _nx = _a - _d  # the label of the normal steps aside when its tip comes close to the y-axis
    tip_label(_ax, (_nx, _fa + 1), _slope + 90 + (-70 if -0.05 < _nx < 0.5 else 70 if -0.5 < _nx <= -0.05 else 0), r"$\vec{n}$", ORANGE)
    _ax.plot(_a, _fa, "o", color="black", ms=4, zorder=4)
    legend_box(_fig, [("dot", "black", r"$\genfrac{[}{]}{0}{0}{a}{f(a)}$"), ("line", GREEN, r"$y = f(a) + f'(a)(x - a)$")], loc="outside lower center", ncols=2)

    mo.vstack(
        [
            mo.hstack([a_line], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(x) = 4x\,e^{-x}$ at $x = a$: &nbsp; $f(a)$", rf"${num(_fa)}$"),
                    (r"$f'(a)$", rf"${num(_d)}$"),
                    (r"velocity vector of the tangent line $\begin{bmatrix} 1 \\ f'(a) \end{bmatrix}$", rf"$\textcolor{{{GREEN}}}{{\begin{{bmatrix}} 1 \\ {num(_d)} \end{{bmatrix}}}}$"),
                    (r"normal to the tangent line $\vec{n} = \begin{bmatrix} -f'(a) \\ 1 \end{bmatrix}$", rf"$\textcolor{{{ORANGE}}}{{\begin{{bmatrix}} {num(-_d)} \\ 1 \end{{bmatrix}}}}$"),
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
            mo.md(r"""### The tangent plane"""),
            theorem(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable at $\vec{a} = \begin{bmatrix} a^1 \\ a^2 \end{bmatrix}$

    The graph of the affine approximation of $f$ at $\vec{a}$ is a plane in $\mathbb{R}^3 = \mathbb{R}^2 \times \mathbb{R}$ through $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$ with normal vector

    $$
    \vec{n} = \begin{bmatrix} -\dfrac{\partial f}{\partial x^1}(\vec{a}) \\[8pt] -\dfrac{\partial f}{\partial x^2}(\vec{a}) \\[8pt] 1 \end{bmatrix}
    $$

    $\leadsto$ &nbsp; the **tangent plane** to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}$
    """,
                "Tangent plane",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    \mathrm{graph}(g) &= \left\{\, \begin{bmatrix} x^1 \\ x^2 \\ f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\} \\[6pt]
    &= \left\{\, \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \begin{bmatrix} x^1 - a^1 \\ x^2 - a^2 \\ Df(\vec{a})(\vec{x} - \vec{a}) \end{bmatrix} \;\middle|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\right\} \\[6pt]
    &= \Bigg\{\, \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + \underbrace{(x^1 - a^1)}_{t} \underbrace{\begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix}}_{\text{velocity vector}} + \underbrace{(x^2 - a^2)}_{s} \underbrace{\begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\text{velocity vector}} \;\Bigg|\; \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \,\Bigg\}
    \end{aligned}
    $$

    $$
    \begin{gathered}
    \vec{n} = \begin{bmatrix} n^1 \\ n^2 \\ n^3 \end{bmatrix} \ \text{ such that } \
    \vec{n} \cdot \underbrace{\begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix}}_{\vec{u}} = 0 = \vec{n} \cdot \underbrace{\begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}}_{\vec{v}} \\[8pt]
    \leadsto \qquad \vec{n} = \vec{u} \times \vec{v} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 0 & \frac{\partial f}{\partial x^1}(\vec{a}) \\ 0 & 1 & \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} \qquad \square
    \end{gathered}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, ORANGE, mo, np, panel, patch, sheet, turntable):
    # graph(f) with its tangent plane at (a, f(a)), spanned by the velocity vectors (1, 0, d1) and (0, 1, d2)
    def _f(x1, x2):
        return 2.4 - 0.2 * ((x1 - 1.9) ** 2 + (x2 - 1.7) ** 2)

    _a = (1.5, 1.1)
    _d1, _d2 = -0.4 * (_a[0] - 1.9), -0.4 * (_a[1] - 1.7)
    _fa = float(_f(*_a))
    _lo, _hi, _k, _v = 0.5, 3.1, 1.0, 0.8  # the graph over [lo, hi]^2, the plane over a + [-k, k]^2, velocity vectors of length v
    _x1, _x2 = np.meshgrid(np.linspace(_lo, _hi, 25), np.linspace(_lo, _hi, 25), indexing="ij")
    _w = np.linspace(_lo, _hi, 25)
    _rim = [(_c + 0 * _w, _w) for _c in (_lo, _hi)] + [(_w, _c + 0 * _w) for _c in (_lo, _hi)]

    def _g(x1, x2):
        return _fa + _d1 * (x1 - _a[0]) + _d2 * (x2 - _a[1])

    _corners = [(_a[0] + _k * _i, _a[1] + _k * _j) for _i, _j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    _s = np.linspace(0, 1, 30)
    _edges = [(_p[0] + _s * (_q[0] - _p[0]), _p[1] + _s * (_q[1] - _p[1])) for _p, _q in zip(_corners, _corners[1:] + _corners[:1])]
    _graph = turntable(
        28,
        32,
        "graph of f with its tangent plane at the point above a, the two velocity vectors spanning the plane and the normal vector n",
        [
            panel(
                1.0,
                surfaces=[
                    sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, BLUE, 0.5), (1, 4, BLUE, 0.5)]),
                    patch([(_c[0], _c[1], _g(*_c)) for _c in _corners], "#c8e6c9", 0.6),
                ],
                lines=[(_c1, _c2, _f(_c1, _c2), BLUE, 1.2) for _c1, _c2 in _rim]
                + [(_c1, _c2, _g(_c1, _c2), GREEN, 1.2) for _c1, _c2 in _edges]
                + [
                    (_a[0] + 0 * _s, _a[1] * _s, 0 * _s, GREY, 1.0, [4, 3]),
                    (_a[0] * _s, _a[1] + 0 * _s, 0 * _s, GREY, 1.0, [4, 3]),
                    (_a[0] + 0 * _s, _a[1] + 0 * _s, _fa * _s, GREY, 1.0, [4, 3]),
                ],
                points=[((_a[0], _a[1], _fa), "#000000"), ((_a[0], _a[1], 0), GREY, 3.4)],
                arrows=[
                    ((_a[0], _a[1], _fa), (_a[0] + _v, _a[1], _fa + _v * _d1), GREEN),
                    ((_a[0], _a[1], _fa), (_a[0], _a[1] + _v, _fa + _v * _d2), GREEN),
                    ((_a[0], _a[1], _fa), (_a[0] - _d1, _a[1] - _d2, _fa + 1), ORANGE),
                ],
                axes=[((0, 0, 0), (3.6, 0, 0), "x^1", -150), ((0, 0, 0), (0, 3.6, 0), "x^2", -20), ((0, 0, 0), (0, 0, 3.6), "y", 90)],
            )
        ],
        legend=[
            ("area", "#dbe8f6", r"y = f(\vec{x})", BLUE),
            ("area", "#c8e6c9", r"y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})", GREEN, 0.6),
            ("line", GREEN, r"\text{velocity vectors}", 1.8),
            ("line", ORANGE, r"\vec{n}", 1.8),
            ("dot", "#000000", r"\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix}"),
            ("dot", GREY, r"\vec{a}"),
        ],
        height=420,
        bias=0.16,  # the point and the vectors at the tangency lie on both surfaces: draw them in front
    )

    mo.vstack(
        [
            _graph,
            mo.md(
                r"""
    $$
    y = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) \qquad \leadsto \qquad
    \begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} + (x^1 - a^1) \begin{bmatrix} 1 \\ 0 \\ \frac{\partial f}{\partial x^1}(\vec{a}) \end{bmatrix} + (x^2 - a^2) \begin{bmatrix} 0 \\ 1 \\ \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix}
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = x^1 e^{x^2}, \quad \vec{a} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$

    $$
    \leadsto \qquad \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \frac{\partial f}{\partial x^1}(\vec{a}) \\[4pt] \frac{\partial f}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} e^{a^2} \\ a^1 e^{a^2} \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}
    \qquad \leadsto \qquad \vec{n} = \begin{bmatrix} -\frac{\partial f}{\partial x^1}(\vec{a}) \\[4pt] -\frac{\partial f}{\partial x^2}(\vec{a}) \\[4pt] 1 \end{bmatrix} = \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    & \leadsto \qquad \text{plane through } \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} \text{ normal to } \begin{bmatrix} -1 \\ -1 \\ 1 \end{bmatrix} \\
    & \phantom{\leadsto \qquad \text{plane }} = \left\{\, \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; -1 \cdot (y^1 - 1) - 1 \cdot (y^2 - 0) + 1 \cdot (y^3 - 1) = 0 \,\right\} \\
    & \phantom{\leadsto \qquad \text{plane }} = \left\{\, \begin{bmatrix} y^1 \\ y^2 \\ y^3 \end{bmatrix} \;\middle|\; y^3 = y^1 + y^2 \,\right\} = \mathrm{graph}(g)
    \end{aligned}
    $$

    $$
    \leadsto \qquad \text{affine approximation} \quad g(\vec{x}) = 1 + \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x^1 - 1 \\ x^2 \end{bmatrix} = 1 + (x^1 - 1) + x^2
    $$

    **Remark.**

    $$
    \vec{x} = \begin{bmatrix} 1.1 \\ -0.1 \end{bmatrix} \qquad \Longrightarrow \qquad
    \begin{aligned} f(\vec{x}) &= 1.1\, e^{-0.1} \approx 0.995 \\ g(\vec{x}) &= 1.1 - 0.1 = 1 \end{aligned}
    \qquad \Longrightarrow \qquad f(\vec{x}) - g(\vec{x}) \approx -0.005
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    px1 = mo.ui.slider(0, 2, 0.05, value=1.1, label="$x^1$", show_value=True)
    px2 = mo.ui.slider(-1, 1, 0.05, value=-0.1, label="$x^2$", show_value=True)
    return px1, px2


@app.cell(hide_code=True)
def _(math, mo, num, px1, px2, table):
    _f = px1.value * math.exp(px2.value)
    _g = px1.value + px2.value
    mo.vstack(
        [
            mo.hstack([px1, px2], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(\vec{x}) = x^1 e^{x^2}$", rf"${num(_f, 4)}$"),
                    (r"$g(\vec{x}) = 1 + (x^1 - 1) + x^2$", rf"${num(_g, 4)}$"),
                    (r"$f(\vec{x}) - g(\vec{x})$", rf"${num(_f - _g, 4)}$"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### The derivative of general maps

    **Remark.** &nbsp; $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} \right) = \begin{bmatrix} f^1(\vec{x}) \\ \vdots \\ f^m(\vec{x}) \end{bmatrix}$ &nbsp; with each $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ a scalar function on $\mathbb{R}^n$
    """
            ),
            definition(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is **differentiable** at $\vec{x} = \vec{a} = \begin{bmatrix} a^1 \\ \vdots \\ a^n \end{bmatrix}$ if each component $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ is differentiable at $\vec{a}$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} Df^1(\vec{a}) \\ \vdots \\ Df^m(\vec{a}) \end{bmatrix}
    = \begin{bmatrix} \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f^1}{\partial x^n}(\vec{a}) \\ \vdots & \ddots & \vdots \\ \dfrac{\partial f^m}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f^m}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(m \times n)
    $$

    defines an affine approximation of $f$ at $\vec{a}$ in the sense

    $$
    \lim_{\vec{x} \to \vec{a}} \frac{\overbrace{f(\vec{x})}^{\mathbb{R}^m} - \overbrace{f(\vec{a})}^{\mathbb{R}^m} - \overbrace{Df(\vec{a})}^{\mathrm{Mat}(m \times n)} \overbrace{(\vec{x} - \vec{a})}^{\mathbb{R}^n}}{\lVert \vec{x} - \vec{a} \rVert} = \vec{0} \in \mathbb{R}^m
    $$

    If $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$, the linear transformation $Df(\vec{a}) : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called the **derivative** of $f$ at $\vec{a}$ or the **Jacobian matrix** of $f$ at $\vec{a}$, $Df(\vec{a}) \in \mathrm{Mat}(m \times n)$.
    """,
                "Differentiability and the Jacobian matrix",
            ),
            theorem(
                r"""
    $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$ if and only if

    $$
    \lim_{\vec{x} \to \vec{a}} \underbrace{\frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert}}_{\text{scalar valued function on } \mathbb{R}^n} = 0
    $$

    $\leadsto$ &nbsp; we only need to compute 1 limit instead of $m$
    """,
                "Differentiability with a single limit",
            ),
            theorem(
                r"""
    If all components $f^j : \mathbb{R}^n \longrightarrow \mathbb{R}$ of $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ have well-defined partial derivatives in an open ball centered at $\vec{a}$, and they are all continuous at $\vec{x} = \vec{a}$ ($f$ is $C^1$-smooth at $\vec{a}$), then $f$ is differentiable at $\vec{x} = \vec{a}$.
    """,
                r"$C^1$-smooth implies differentiable",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \underbrace{\begin{bmatrix} a & b \\ c & d \end{bmatrix}}_{A \,\in\, \mathrm{Mat}(2 \times 2)} \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} a x^1 + b x^2 \\ c x^1 + d x^2 \end{bmatrix} = \begin{bmatrix} f^1(\vec{x}) \\ f^2(\vec{x}) \end{bmatrix}
    $$

    $f^1(\vec{x})$, $f^2(\vec{x})$ are $C^1$-smooth everywhere in $\mathbb{R}^2$ (linear combination of elementary functions) &nbsp; $\Longrightarrow$ &nbsp; $f$ is differentiable at any $\vec{a} \in \mathbb{R}^2$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f^1}{\partial x^1}(\vec{a}) & \dfrac{\partial f^1}{\partial x^2}(\vec{a}) \\[8pt] \dfrac{\partial f^2}{\partial x^1}(\vec{a}) & \dfrac{\partial f^2}{\partial x^2}(\vec{a}) \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} = A\,!
    $$

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 \cos(x^2) \\ x^1 \sin(x^2) \end{bmatrix}, \quad \vec{a} = \begin{bmatrix} 2 \\ \pi/3 \end{bmatrix}$

    $$
    \Longrightarrow \qquad Df(\vec{a}) = \begin{bmatrix} \cos(a^2) & -a^1 \sin(a^2) \\ \sin(a^2) & a^1 \cos(a^2) \end{bmatrix} = \begin{bmatrix} \frac{\sqrt{1}}{2} & -\sqrt{3} \\[4pt] \frac{\sqrt{3}}{2} & \sqrt{1} \end{bmatrix}
    $$

    $$
    f(\vec{a}) = \begin{bmatrix} 2 \cos(\pi/3) \\ 2 \sin(\pi/3) \end{bmatrix} = \begin{bmatrix} \sqrt{1} \\ \sqrt{3} \end{bmatrix}, \qquad
    Df(\vec{a})(\vec{e}_1) = \begin{bmatrix} \frac{\sqrt{1}}{2} \\[4pt] \frac{\sqrt{3}}{2} \end{bmatrix}, \qquad
    Df(\vec{a})(\vec{e}_2) = \begin{bmatrix} -\sqrt{3} \\ \sqrt{1} \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pa1 = mo.ui.slider(0.5, 2.5, 0.25, value=2, label="$a^1$", show_value=True)
    pk = mo.ui.slider(0, 12, 1, value=4, label=r"$k$, with $a^2 = k\pi/12$", show_value=True)
    return pa1, pk


@app.cell(hide_code=True)
def _(Arc, BLUE, FULL, Figure, GREEN, GREY, RED, arrow, cross_axes, legend_box, math, mo, num, pa1, pk, table, tip_label):
    from fractions import Fraction as _Fraction

    _a1, _a2 = pa1.value, pk.value * math.pi / 12
    _k = _Fraction(pk.value, 12)  # a^2 = k pi / 12, written in lowest terms
    _frac = "0" if _k == 0 else (r"\pi" if _k.numerator == 1 else rf"{_k.numerator}\pi") + ("" if _k.denominator == 1 else rf"/{_k.denominator}")
    _c, _s = math.cos(_a2), math.sin(_a2)
    _fa = (_a1 * _c, _a1 * _s)
    _deg = math.degrees(_a2)
    _dash = (0, (4, 3))

    # both panels are drawn at the same scale
    _fig = Figure(figsize=(FULL, 4.2), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[5.6, 12.6])
    for _ax, _xlim in ((_left, (-0.8, 4.8)), (_right, (-6.3, 6.3))):
        _ax.set_xlim(*_xlim)
        _ax.set_ylim(-3.5, 5.3)
        _ax.set_aspect("equal")
        _ax.axis("off")

    cross_axes(_left, (-0.6, 4.7), (-0.6, 5.2), "$x^1$", "$x^2$")
    _left.plot([_a1, _a1, 0], [0, _a2, _a2], color=GREY, lw=0.9, ls=_dash)
    arrow(_left, (0, 0), (_a1, _a2), "black")
    arrow(_left, (_a1, _a2), (_a1 + 1, _a2), BLUE)
    arrow(_left, (_a1, _a2), (_a1, _a2 + 1), RED)
    tip_label(_left, (_a1 + 1, _a2), 0, r"$\vec{e}_1$", BLUE)
    tip_label(_left, (_a1, _a2 + 1), 90, r"$\vec{e}_2$", RED)
    _left.plot(_a1, _a2, "o", color="black", ms=4, zorder=4)

    cross_axes(_right, (-6.2, 6.2), (-3.4, 5.2), "$y^1$", "$y^2$")
    _right.plot([_fa[0], _fa[0], 0], [0, _fa[1], _fa[1]], color=GREY, lw=0.9, ls=_dash)
    if _deg > 0:
        _right.add_patch(Arc((0, 0), 0.8, 0.8, theta1=0, theta2=_deg, color=GREEN, lw=1.4))
    arrow(_right, (0, 0), _fa, "black")
    _t1 = (_fa[0] + _c, _fa[1] + _s)
    _t2 = (_fa[0] - _a1 * _s, _fa[1] + _a1 * _c)
    arrow(_right, _fa, _t1, BLUE)
    arrow(_right, _fa, _t2, RED)
    tip_label(_right, _t1, _deg, r"$Df(\vec{a})(\vec{e}_1)$", BLUE, fontsize=12)
    tip_label(_right, _t2, _deg + 90, r"$Df(\vec{a})(\vec{e}_2)$", RED, fontsize=12)
    _right.plot(*_fa, "o", color="black", ms=4, zorder=4)
    legend_box(_fig, [("dot", "black", r"$\vec{a}$, $f(\vec{a})$")], loc="outside lower center")

    mo.vstack(
        [
            mo.hstack([pa1, pk], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{a}$", rf"$\begin{{bmatrix}} {num(_a1)} \\ {num(_a2)} \end{{bmatrix}}$"),
                    (r"angle $a^2$ of $f(\vec{a})$", rf"$\textcolor{{{GREEN}}}{{{_frac}}}$"),
                    (r"$f(\vec{a})$", rf"$\begin{{bmatrix}} {num(_fa[0])} \\ {num(_fa[1])} \end{{bmatrix}}$"),
                    (
                        r"$Df(\vec{a}) = \begin{bmatrix} Df(\vec{a})(\vec{e}_1) & Df(\vec{a})(\vec{e}_2) \end{bmatrix}$",
                        rf"$\begin{{bmatrix}} \textcolor{{{BLUE}}}{{{num(_c)}}} & \textcolor{{{RED}}}{{{num(-_a1 * _s)}}} \\ \textcolor{{{BLUE}}}{{{num(_s)}}} & \textcolor{{{RED}}}{{{num(_a1 * _c)}}} \end{{bmatrix}}$",
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

    q1_d1, q1_d2, q1_est = _field(), _field(), _field()
    return q1_d1, q1_d2, q1_est


@app.cell(hide_code=True)
def _(check, mo, q1_d1, q1_d2, q1_est):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 x^2, \qquad \vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
    $$

    (a) Write the derivative and the gradient of $f$ at $\vec{a}$.
    """
            ),
            _ask(r"$\dfrac{\partial f}{\partial x^1}(\vec{a}) =$", q1_d1, 4),
            _ask(r"$\dfrac{\partial f}{\partial x^2}(\vec{a}) =$", q1_d2, 1),
            mo.md(
                r"""
    (b) Write the equation for the tangent plane to $\mathrm{graph}(f)$ at $\begin{bmatrix} a^1 \\ a^2 \\ f(\vec{a}) \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$.

    (c) Estimate $f\!\left( \begin{bmatrix} 1.1 \\ 1.9 \end{bmatrix} \right)$ and compare with the exact value.
    """
            ),
            _ask(r"estimate $=$", q1_est, 2.3),
            mo.md(
                r"""
    ### Question 2

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = \begin{bmatrix} x^1 x^2 \\ x^1 + x^2 \\ (x^2)^2 \end{bmatrix}
    $$

    (a) Compute the derivative of $f$ at $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix}$.

    (b) Write the affine approximation of $f$ at $\vec{a} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$.

    (c) Write the affine approximation of $f$ at $\vec{b} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$.

    (d) How do the images of these approximations differ?
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - the affine approximation of $f : \mathbb{R}^n \longrightarrow \mathbb{R}$ at $\vec{a}$ is

        $$
        g(\vec{x}) = f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a})
        $$

        (linear plus constant)
    - $n = 1$: $\mathrm{graph}(g)$ is the tangent line to the graph of $f$

        $n = 2$: $\mathrm{graph}(g)$ is the tangent plane to $\mathrm{graph}(f)$, through $(a^1, a^2, f(\vec{a}))$ with normal vector

        $$
        \vec{n} = \Big( {-\frac{\partial f}{\partial x^1}(\vec{a})},\ {-\frac{\partial f}{\partial x^2}(\vec{a})},\ 1 \Big)
        $$
    - $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is differentiable at $\vec{a}$ if each component $f^j$ is; the rows of the Jacobian matrix $Df(\vec{a}) \in \mathrm{Mat}(m \times n)$ are the derivatives $Df^j(\vec{a})$
    - $f$ is differentiable at $\vec{a}$ if and only if

        $$
        \frac{\lVert f(\vec{x}) - f(\vec{a}) - Df(\vec{a})(\vec{x} - \vec{a}) \rVert}{\lVert \vec{x} - \vec{a} \rVert} \longrightarrow 0 \quad \text{as } \vec{x} \to \vec{a}
        $$

        $C^1$-smooth at $\vec{a}$ $\Longrightarrow$ differentiable at $\vec{a}$
    - a linear map $f(\vec{x}) = A\vec{x}$ has $Df(\vec{a}) = A$ at every $\vec{a}$
    """)
    return


if __name__ == "__main__":
    app.run()
