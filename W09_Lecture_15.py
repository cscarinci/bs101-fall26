import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 · Lecture 15 · Global extrema on closed and bounded domains", css_file="bs101.css")


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
    header("Lecture 15", "Week 09", "Lecture 15 · Global extrema on closed and bounded domains")
    return


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
        ax.annotate(text, at, textcoords="offset points", xytext=(r * c, r * s), ha=ha, va=va, color=color, fontsize=fontsize, zorder=6, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

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
def _(BLUE, GREEN, ORANGE, mo, np, panel, sheet, theorem, turntable):
    def _f(x1, x2):
        return x1**2 * np.exp(-(x1**2)) + x2**2

    _L, _W = 2.2, 0.7
    _u1, _u2 = np.meshgrid(np.linspace(-_L, _L, 89), np.linspace(-_W, _W, 29), indexing="ij")
    _s1, _s2 = np.linspace(-_L, _L, 177), np.linspace(-_W, _W, 57)
    _edges = [(_s1, np.full_like(_s1, _k), _f(_s1, _k), BLUE, 1.4) for _k in (-_W, _W)]
    _edges += [(np.full_like(_s2, _k), _s2, _f(_k, _s2), BLUE, 1.4) for _k in (-_L, _L)]
    _fig = turntable(
        -70,
        42,
        "graph of f with its two saddle points and its global minimum",
        [
            panel(
                1.0,
                surfaces=[sheet(_u1, _u2, _f(_u1, _u2), wire=[(0, 8, BLUE, 0.6), (1, 4, BLUE, 0.6)])],
                lines=_edges + [(_s1, 0 * _s1, _f(_s1, 0), BLUE, 2.0)],
                points=[((-1, 0, _f(-1, 0)), ORANGE), ((1, 0, _f(1, 0)), ORANGE), ((0, 0, 0), GREEN)],
                axes=[((-2.35, 0, 0), (2.6, 0, 0), "x^1", -60), ((0, 0, 0), (0, 0.95, 0), "x^2", 60), ((0, 0, 0), (0, 0, 1.15), "y", 90)],
            )
        ],
        legend=[("dot", ORANGE, r"\text{saddle points } \vec{a}, \vec{b}"), ("dot", GREEN, r"\text{global minimum } \vec{0}")],
        height=460,
    )

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Local extrema via 2nd derivative test
    """
            ),
            theorem(
                r"""
    If $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ is $C^2$-smooth at a critical point $\vec{x} = \vec{a}$ &nbsp; ($\vec{\nabla} f(\vec{a}) = \vec{0}$)

    - if $Hf(\vec{a})$ is **negative definite**, then $\vec{a}$ is local max

        $\Big( \det Hf(\vec{a}) > 0$ and $\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) < 0 \Big)$

    - if $Hf(\vec{a})$ is **positive definite**, then $\vec{a}$ is local min

        $\Big( \det Hf(\vec{a}) > 0$ and $\dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) > 0 \Big)$

    - if $Hf(\vec{a})$ is **indefinite**, then $\vec{a}$ is a saddle point &nbsp; $\big( \det Hf(\vec{a}) < 0 \big)$
    - if $Hf(\vec{a})$ is **degenerate**, we need more info &nbsp; $\big( \det Hf(\vec{a}) = 0 \big)$

        (could be local max, local min, or saddle …)
    """,
                "Second derivative test",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 e^{-(x^1)^2} + (x^2)^2$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 e^{-(x^1)^2} - 2(x^1)^3 e^{-(x^1)^2} \\ 2x^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    $$

    $$
    \Longleftrightarrow \qquad x^2 = 0, \quad x^1 \big( 1 - (x^1)^2 \big) e^{-(x^1)^2} = 0
    \qquad \Longleftrightarrow \qquad x^2 = 0, \quad x^1 \in \{ -1, 0, 1 \}
    $$

    $$
    Hf(\vec{x}) = \begin{bmatrix} \big( 4(x^1)^4 - 10(x^1)^2 + 2 \big) e^{-(x^1)^2} & 0 \\ 0 & 2 \end{bmatrix}
    $$

    At $\vec{a} = \begin{bmatrix} -1 \\ 0 \end{bmatrix}$ and $\vec{b} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$:

    $$
    Hf(\vec{a}) = Hf(\vec{b}) = \begin{bmatrix} -4e^{-1} & 0 \\ 0 & 2 \end{bmatrix} \qquad \text{indefinite} \quad \Longrightarrow \quad \text{saddle}
    $$

    At $\vec{0} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$:

    $$
    Hf(\vec{0}) = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix} \qquad \text{positive definite} \quad \Longrightarrow \quad \text{minimum}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; global minimum: &nbsp; $f(\vec{0}) = 0 < f(\vec{x}) \quad \forall\, \vec{x} \neq \vec{0}$!

    **In this lecture:** global extrema

    **References:** MT 3.3
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""## III.2 &nbsp; Global extrema on closed and bounded domains"""),
            definition(
                r"""
    Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, a point $\vec{a} \in D$ is

    - a **global maximum** of $f$ if

        $$
        f(\vec{x}) \leq f(\vec{a}) \qquad \forall\, \vec{x} \in D
        $$

    - a **global minimum** of $f$ if

        $$
        f(\vec{x}) \geq f(\vec{a}) \qquad \forall\, \vec{x} \in D
        $$
    """,
                "Global maximum and global minimum",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; to determine global extrema, we will also need to look at properties of the domain of $f$!

    **Example.** &nbsp; $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$

    $\Longrightarrow$ &nbsp; $\begin{bmatrix} 0 \\ 0 \end{bmatrix}$ is global minimum and there is no global maximum

    $g : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$, &nbsp; $g\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ &nbsp; for

    $$
    D = \left\{\, \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \in \mathbb{R}^2 \;\middle|\; 0 < x^1 \leq 1,\ 0 < x^2 \leq 1 \,\right\}
    $$

    $\Longrightarrow$ &nbsp; there is no global minimum; &nbsp; $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ is the global maximum!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, ORANGE, RED, cross_axes, legend_box, mo, np, panel, sheet, turntable):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(HALF, 3.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.2, 1.45)
    _ax.set_ylim(-0.2, 1.35)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.15, 1.4), (-0.15, 1.3), "$x^1$", "$x^2$")
    # D = (0, 1] x (0, 1]: the edges on the axes are not in D (a white band lifts them off the axes)
    _ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color=LIGHT, lw=0, zorder=0)
    _ax.plot([1, 1, 0], [0, 1, 1], color=BLUE, lw=1.4, zorder=4)
    _ax.plot([0, 0, 1], [1, 0, 0], color="white", lw=4, zorder=4)
    _ax.plot([0, 0, 1], [1, 0, 0], color=BLUE, lw=1.4, ls=(0, (3, 2)), zorder=5)
    for _c in ((0, 0), (1, 0), (0, 1)):
        _ax.plot(*_c, "o", ms=5, mfc="white", mec=BLUE, mew=1.2, zorder=6)
    _ax.plot(1, 1, "o", ms=5, color=BLUE, zorder=6)
    _a = (0.55, 0.75)
    _ax.plot([0, _a[0] / _a[1]], [0, 1], color=GREY, lw=0.9, ls=(0, (4, 3)), zorder=1)
    _ax.plot(*_a, "o", color=RED, ms=5, zorder=6)
    _ax.plot(_a[0] / 2, _a[1] / 2, "o", color=ORANGE, ms=5, zorder=6)
    _ax.text(1, -0.05, "$1$", ha="center", va="top", fontsize=12, bbox=_box)
    _ax.text(-0.05, 1, "$1$", ha="right", va="center", fontsize=12, bbox=_box)
    legend_box(_fig, [("area", LIGHT, "$D$", BLUE), ("dot", RED, r"$\vec{a}$"), ("dot", ORANGE, r"$\vec{x}$")], loc="outside lower center", ncols=3)

    # graph(f) over a disc, faint, with graph(g) above D
    def _f(x1, x2):
        return x1**2 + x2**2

    _R = 1.5
    _r, _p = np.meshgrid(np.linspace(0, _R, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _b1, _b2 = np.meshgrid(np.linspace(0, 1, 11), np.linspace(0, 1, 11), indexing="ij")
    _s = np.linspace(0, 1, 41)
    _z, _o = 0 * _s, 1 + 0 * _s
    _phi = np.linspace(0, 2 * np.pi, 241)
    _dash, _faint = [4, 3], "#c4c4c4"
    _lines = [(_R * np.cos(_phi), _R * np.sin(_phi), _R**2 + 0 * _phi, _faint, 1.0)]
    for _k in (0.25, 0.5, 0.75):
        _lines += [(_k + _z, _s, _f(_k, _s), BLUE, 0.8), (_s, _k + _z, _f(_s, _k), BLUE, 0.8)]
    _lines += [(_o, _s, _f(1, _s), BLUE, 1.6), (_s, _o, _f(_s, 1), BLUE, 1.6)]
    _lines += [(_z, _s, _f(0, _s), BLUE, 1.6, _dash), (_s, _z, _f(_s, 0), BLUE, 1.6, _dash)]
    # D in the plane: its edges on the axes dashed, on white bands drawn over the axes
    _lines += [(_o, _s, _z, BLUE, 1.6), (_s, _o, _z, BLUE, 1.6)]
    _lines += [(_z, _s, _z, "#ffffff", 4.5, None, 0.01), (_s, _z, _z, "#ffffff", 4.5, None, 0.01)]
    _lines += [(_z, _s, _z, BLUE, 1.6, _dash, 0.02), (_s, _z, _z, BLUE, 1.6, _dash, 0.02)]
    _open = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1)]
    _graph = turntable(
        45,
        14,
        "graph of g over D, with the graph of f over the plane in a faint tone, and the global maximum of g",
        [
            panel(
                0.55,
                surfaces=[
                    sheet(_r * np.cos(_p), _r * np.sin(_p), _f(_r * np.cos(_p), _r * np.sin(_p)), wire=[(0, 4, _faint, 0.5), (1, 8, _faint, 0.5)], tint=(0, 1, 0, 1), clear=True, alpha=0.3),
                    sheet(_b1, _b2, 0 * _b1, flat=LIGHT),
                ],
                lines=_lines,
                points=[(_q, BLUE, 3.6, True) for _q in _open] + [((1, 1, 0), BLUE, 3.6), ((1, 1, 2), RED)],
                axes=[((0, 0, 0), (1.75, 0, 0), "x^1", -150), ((0, 0, 0), (0, 1.75, 0), "x^2", -30), ((0, 0, 0), (0, 0, 2.6), "y", 90)],
            )
        ],
        legend=[
            ("area", "#a9c3e6", r"y = g(\vec{x}), \ \vec{x} \in D", BLUE),
            ("area", LIGHT, r"y = f(\vec{x}), \ \vec{x} \in \mathbb{R}^2", _faint, 0.35),
            ("area", LIGHT, "D", BLUE),
            ("dot", RED, r"\text{global maximum: } g\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right) = 2"),
            ("ring", BLUE, r"\text{points left out}"),
        ],
        height=380,
    )

    mo.vstack(
        [
            mo.Html(
                '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem 1rem;">'
                f'<div style="flex: 1 1 240px; min-width: 220px;">{mo.as_html(_fig).text}</div>'
                f'<div style="flex: 1.45 1 300px; min-width: 260px;">{_graph.text}</div></div>'
            ),
            mo.md(
                r"""
    Starting from any $\vec{a} \in D$,

    - can make $g(\vec{x}) < g(\vec{a})$ moving towards $\vec{0}$, but never reach $g(\vec{x}) = 0$ since $\vec{0} \notin D$

        $\Longrightarrow$ &nbsp; no $\vec{a} \in D$ can be a minimum!

    - can make $g(\vec{x}) > g(\vec{a})$ moving away from $\vec{0}$, unless $a^1 = 1$ or $a^2 = 1$
    - if $a^2 = 1$, can make $g(\vec{x}) > g(\vec{a})$ moving right, unless $a^1 = 1$ (likewise, if $a^1 = 1$, moving up, unless $a^2 = 1$)

        $\Longrightarrow$ &nbsp; $\vec{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix} \in D$ is the maximum!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, RED, cross_axes, definition, legend_box, mo, np):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _th = np.linspace(0, 2 * np.pi, 241)

    def _panel():
        fig = Figure(figsize=(HALF + 1.6, 2.75), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(-2.3, 2.3)
        ax.set_ylim(-1.6, 2.0)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    # the rectangle 0 <= x^1 <= a, 0 <= x^2 <= b inside B(0, r)
    _a, _b, _r = 1.2, 0.8, 1.55
    _bounded, _ax = _panel()
    _ax.fill(_r * np.cos(_th), _r * np.sin(_th), color=RED, alpha=0.06, lw=0)
    _ax.plot(_r * np.cos(_th), _r * np.sin(_th), color=RED, lw=1.2)
    _ax.fill([0, _a, _a, 0], [0, 0, _b, _b], color=LIGHT, lw=0)
    _ax.plot([0, _a, _a, 0, 0], [0, 0, _b, _b, 0], color=BLUE, lw=1.4)
    cross_axes(_ax, (-2.0, 2.2), (-1.5, 1.95), "$x^1$", "$x^2$")
    _ax.text(_a, -0.06, "$a$", ha="center", va="top", fontsize=12, bbox=_box)
    _ax.text(-0.06, _b, "$b$", ha="right", va="center", fontsize=12, bbox=_box)
    legend_box(_bounded, [("area", LIGHT, "$D$", BLUE), ("line", RED, r"$B(\vec{0}, r)$")])

    # the strip a <= x^2 <= b leaves every ball
    _a, _b, _r = 0.4, 1.0, 1.3
    _unbounded, _ax = _panel()
    _ax.fill([-2.3, 2.3, 2.3, -2.3], [_a, _a, _b, _b], color=LIGHT, lw=0)
    for _h in (_a, _b):
        _ax.plot([-2.3, 2.3], [_h, _h], color=BLUE, lw=1.4)
    _ax.fill(_r * np.cos(_th), _r * np.sin(_th), color=RED, alpha=0.06, lw=0)
    _ax.plot(_r * np.cos(_th), _r * np.sin(_th), color=RED, lw=1.2)
    cross_axes(_ax, (-2.25, 2.25), (-1.5, 1.95), "$x^1$", "$x^2$")
    _ax.text(-0.06, _a, "$a$", ha="right", va="top", fontsize=12, bbox=_box)
    _ax.text(-0.06, _b, "$b$", ha="right", va="bottom", fontsize=12, bbox=_box)
    legend_box(_unbounded, [("area", LIGHT, "$D$", BLUE), ("line", RED, r"$B(\vec{0}, r)$")])

    mo.vstack(
        [
            definition(
                r"""
    $D \subseteq \mathbb{R}^2$ is called **bounded** if “we cannot take its points to infinity”

    $\Longleftrightarrow$ &nbsp; it is contained in some ball of finite radius

    $\Longleftrightarrow$ &nbsp; there exists $B(\vec{0}, r) \supseteq D$

    $D \subseteq \mathbb{R}^2$ is **unbounded** if it cannot be contained in any ball of finite radius.
    """,
                "Bounded and unbounded sets",
            ),
            mo.md(r"""$D = \left\{\, 0 \leq x^1 \leq a,\ 0 \leq x^2 \leq b \,\right\}$ is bounded: &nbsp; $B(\vec{0}, r) \supseteq D$ for $r^2 > a^2 + b^2$"""),
            _bounded,
            mo.md(r"""$D = \left\{\, -\infty < x^1 < +\infty,\ a \leq x^2 \leq b \,\right\}$ is unbounded"""),
            _unbounded,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Given $D \subseteq \mathbb{R}^2$, the **boundary** of $D$ is the set $\mathrm{Bd}(D)$ of points $\vec{a} \in \mathbb{R}^2$ such that any ball centered at $\vec{a}$ contains both points in $D$ *and* points not in $D$.
    """,
                "Boundary",
            ),
            mo.md(
                r"""
    $$
    D = \left\{\, -\infty < x^1 < +\infty,\ a \leq x^2 \leq b \,\right\}
    \qquad \Longrightarrow \qquad
    \mathrm{Bd}(D) = \left\{\, x^2 = a \,\right\} \cup \left\{\, x^2 = b \,\right\}
    $$

    $$
    D = \left\{\, x^1 > 0,\ x^2 > 0,\ (x^1)^2 + (x^2)^2 < 1 \,\right\}
    \qquad \Longrightarrow \qquad
    \begin{aligned}
    \mathrm{Bd}(D) = {} & \left\{\, x^1 \geq 0,\ x^2 \geq 0,\ (x^1)^2 + (x^2)^2 = 1 \,\right\} \\
    & \cup \left\{\, 0 \leq x^1 \leq 1,\ x^2 = 0 \,\right\} \cup \left\{\, x^1 = 0,\ 0 \leq x^2 \leq 1 \,\right\}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    bp1 = mo.ui.slider(-0.4, 1.4, 0.05, value=0.6, label="$p^1$", show_value=True)
    bp2 = mo.ui.slider(-0.4, 1.4, 0.05, value=0.8, label="$p^2$", show_value=True)
    br = mo.ui.slider(0.05, 0.5, 0.05, value=0.2, label="$r$", show_value=True)
    return bp1, bp2, br


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, RED, bp1, bp2, br, cross_axes, legend_box, math, mo, np, table):
    _p = (round(bp1.value, 10) + 0.0, round(bp2.value, 10) + 0.0)
    _r = round(br.value, 10)
    _eps = 1e-9
    # the point of the closure of D nearest to p, and the distance from p to the outside of D
    _q = (max(_p[0], 0.0), max(_p[1], 0.0))
    _n = math.hypot(*_q)
    if _n > 1:
        _q = (_q[0] / _n, _q[1] / _n)
    _to_D = math.hypot(_p[0] - _q[0], _p[1] - _q[1])
    _in_D = _p[0] > _eps and _p[1] > _eps and math.hypot(*_p) < 1 - _eps
    _to_out = min(_p[0], _p[1], 1 - math.hypot(*_p)) if _in_D else 0.0
    _meets_D = _to_D < _r - _eps
    _meets_out = not (_in_D and _r <= _to_out + _eps)
    _on_Bd = _to_D < _eps and not _in_D

    def _yes(b):
        return "yes" if b else "no"

    _fig = Figure(figsize=(HALF + 2.2, HALF + 0.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.6, 1.75)
    _ax.set_ylim(-0.6, 1.6)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _th = np.linspace(0, np.pi / 2, 120)
    _ax.fill(np.r_[0, np.cos(_th)], np.r_[0, np.sin(_th)], color=LIGHT, lw=0, zorder=0)
    cross_axes(_ax, (-0.55, 1.7), (-0.55, 1.55), "$x^1$", "$x^2$")
    _ax.plot(np.r_[0, np.cos(_th), 0], np.r_[0, np.sin(_th), 0], color="white", lw=4, zorder=4)
    _ax.plot(np.r_[0, np.cos(_th), 0], np.r_[0, np.sin(_th), 0], color=BLUE, lw=1.6, ls=(0, (4, 2)), zorder=5)
    _c = np.linspace(0, 2 * np.pi, 200)
    _ax.fill(_p[0] + _r * np.cos(_c), _p[1] + _r * np.sin(_c), color=RED, alpha=0.12, lw=0, zorder=6)
    _ax.plot(_p[0] + _r * np.cos(_c), _p[1] + _r * np.sin(_c), color=RED, lw=1.2, zorder=6)
    _ax.plot(*_p, "o", color="black", ms=4, zorder=7)
    legend_box(_fig, [("area", LIGHT, "$D$", BLUE), ("line", BLUE, r"$\mathrm{Bd}(D)$", (0, (4, 2))), ("area", (0.70, 0.15, 0.12, 0.15), r"$B(\vec{p}, r)$", RED), ("dot", "black", r"$\vec{p}$")])

    mo.vstack(
        [
            mo.hstack([bp1, bp2, br], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\vec{p}$", rf"$\begin{{bmatrix}} {_p[0]:g} \\ {_p[1]:g} \end{{bmatrix}}$"),
                    (r"$\textcolor{" + RED + r"}{B(\vec{p}, r)}$ contains points in $D$", _yes(_meets_D)),
                    (r"$\textcolor{" + RED + r"}{B(\vec{p}, r)}$ contains points not in $D$", _yes(_meets_out)),
                    (r"$\vec{p} \in D$", _yes(_in_D)),
                    (r"$\vec{p} \in \textcolor{" + BLUE + r"}{\mathrm{Bd}(D)}$", _yes(_on_Bd)),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, RED, cross_axes, definition, legend_box, mo, np):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _a, _b, _c, _d = 0.5, 1.7, 0.45, 1.3

    def _panel(closed):
        fig = Figure(figsize=(HALF + 2.0, 2.3), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(-0.3, 2.3)
        ax.set_ylim(-0.3, 1.65)
        ax.set_aspect("equal")
        ax.axis("off")
        cross_axes(ax, (-0.2, 2.25), (-0.2, 1.6), "$x^1$", "$x^2$")
        ax.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=LIGHT, lw=0)
        ax.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=BLUE, lw=1.4, ls="-" if closed else (0, (3, 2)))
        for x in (_a, _b):
            for y in (_c, _d):
                if closed:
                    ax.plot(x, y, "o", ms=5, color=BLUE, zorder=3)
                else:
                    ax.plot(x, y, "o", ms=5, mfc="white", mec=BLUE, mew=1.2, zorder=3)
        for x, name in ((_a, "$a$"), (_b, "$b$")):
            ax.text(x, -0.05, name, ha="center", va="top", fontsize=12, bbox=_box)
        for y, name in ((_c, "$c$"), (_d, "$d$")):
            ax.text(-0.05, y, name, ha="right", va="center", fontsize=12, bbox=_box)
        return fig, ax

    # the open rectangle misses its corner (a, c), which is in its boundary
    _open, _ax = _panel(False)
    _t = np.linspace(0, 2 * np.pi, 120)
    _ax.fill(_a + 0.16 * np.cos(_t), _c + 0.16 * np.sin(_t), color=RED, alpha=0.12, lw=0, zorder=2)
    _ax.plot(_a + 0.16 * np.cos(_t), _c + 0.16 * np.sin(_t), color=RED, lw=1.0, zorder=2)
    legend_box(_open, [("area", LIGHT, "$D$", BLUE), ("area", (0.70, 0.15, 0.12, 0.15), r"a ball centred at $\genfrac{[}{]}{0}{0}{a}{c}$", RED)])
    _closed, _ax = _panel(True)
    legend_box(_closed, [("area", LIGHT, "$D$", BLUE)])

    mo.vstack(
        [
            definition(
                r"""
    A set $D \subseteq \mathbb{R}^2$ is called **closed** if it contains all of its boundary, &nbsp; $\mathrm{Bd}(D) \subseteq D$.
    """,
                "Closed set",
            ),
            mo.md(
                r"""
    $D = \left\{\, a < x^1 < b,\ c < x^2 < d \,\right\}$ is not closed! &nbsp; $\begin{bmatrix} a \\ c \end{bmatrix} \in \mathrm{Bd}(D)$, but $\begin{bmatrix} a \\ c \end{bmatrix} \notin D$ &nbsp; (one missing point is enough!)
    """
            ),
            _open,
            mo.md(r"""$D = \left\{\, a \leq x^1 \leq b,\ c \leq x^2 \leq d \,\right\}$ is closed!"""),
            _closed,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, LIGHT, RED, cross_axes, legend_box, mo, theorem):
    _fig = Figure(figsize=(HALF + 2.2, 2.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.35, 1.55)
    _ax.set_ylim(-0.3, 1.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.2, 1.5), (-0.2, 1.4), "$x^1$", "$x^2$")
    _ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color=LIGHT, lw=0)
    _ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=BLUE, lw=1.4, zorder=4)
    _ax.plot(0, 0, "o", color=GREEN, ms=6, zorder=5)
    _ax.plot(1, 1, "o", color=RED, ms=6, zorder=5)
    legend_box(
        _fig,
        [
            ("area", LIGHT, r"$\bar{D}$", BLUE),
            ("dot", GREEN, r"global minimum: $h\left(\genfrac{[}{]}{0}{0}{0}{0}\right) = 0$"),
            ("dot", RED, r"global maximum: $h\left(\genfrac{[}{]}{0}{0}{1}{1}\right) = 2$"),
        ],
    )

    mo.vstack(
        [
            theorem(
                r"""
    If $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a closed and bounded domain $D$, then $f$ must have both points of global maximum and global minimum!
    """,
                "Extreme value theorem",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; functions defined on unbounded domains or on non-closed domains might not admit any global extrema!

    **Remark.** $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ over $\mathbb{R}^2$ has no global maximum, which is possible because $\mathbb{R}^2$ is unbounded

    $g\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ over $D = (0, 1] \times (0, 1]$ has no global minimum, which is possible because $D$ is not closed

    $h\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2$ over $\bar{D} = [0, 1] \times [0, 1]$ has both global extrema!
    """
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a closed bounded domain $D$.

    How can we find the global extrema?

    If $\vec{a} \in D$ is a global extremum:

    - $\vec{a} \in \mathrm{Bd}(D) \subseteq D$

    or

    - $\vec{a} \notin \mathrm{Bd}(D) \subseteq D$ &nbsp; $\Longrightarrow$ &nbsp; there is some open ball $B(\vec{a}, r)$ which only contains points of $D$

        $\Longrightarrow$ &nbsp; there exists $B(\vec{a}, r) \subseteq D$ with

        $$
        f(\vec{x}) \leq f(\vec{a}) \quad \forall\, \vec{x} \in B(\vec{a}, r) \qquad (\vec{a} \text{ is local maximum})
        $$

        or

        $$
        f(\vec{x}) \geq f(\vec{a}) \quad \forall\, \vec{x} \in B(\vec{a}, r) \qquad (\vec{a} \text{ is local minimum})
        $$

    $\Longrightarrow$ &nbsp; for differentiable functions defined over closed and bounded domains we get a well-defined strategy to find global extrema!

    ### Strategy to find global extrema

    ① &nbsp; find critical points on the interior $D \setminus \mathrm{Bd}(D)$ (not on the boundary)

    ② &nbsp; find global extrema in $\mathrm{Bd}(D)$ (optimization problem in lower dimension &nbsp; $\Longrightarrow$ &nbsp; easier once we have a parameterization of the boundary)

    ③ &nbsp; compare the values of all candidate points

    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^2 + (x^2)^2 - 2x^1$ &nbsp; on &nbsp; $D = \left\{\, (x^1)^2 + (x^2)^2 \leq 4 \,\right\}$

    $$
    \mathrm{Bd}(D) = \left\{\, (x^1)^2 + (x^2)^2 = 4 \,\right\} = \underbrace{\left\{\, \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \;\middle|\; t \in [0, 2\pi] \,\right\}}_{\text{parameterization of } \mathrm{Bd}(D)},
    \qquad
    D \setminus \mathrm{Bd}(D) = \left\{\, (x^1)^2 + (x^2)^2 < 4 \,\right\}
    $$

    ① &nbsp; Critical points in $D \setminus \mathrm{Bd}(D)$:

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 - 2 \\ 2x^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    \qquad \Longleftrightarrow \qquad
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \vec{a}
    \qquad (\text{interior candidate for global extremum})
    $$

    ② &nbsp; Restrict $f$ to $\mathrm{Bd}(D)$:

    $$
    f\!\left( \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \right) = 4 - 4\cos(t) = g(t)
    \qquad \leadsto \qquad g'(t) = 4\sin(t) = 0 \quad \Longleftrightarrow \quad t = 0 \text{ or } t = \pi
    \quad (t = 2\pi \text{ gives the same point as } t = 0)
    $$

    $$
    \Longrightarrow \qquad
    \vec{b} = \begin{bmatrix} 2\cos(0) \\ 2\sin(0) \end{bmatrix} = \begin{bmatrix} 2 \\ 0 \end{bmatrix},
    \qquad
    \vec{c} = \begin{bmatrix} 2\cos(\pi) \\ 2\sin(\pi) \end{bmatrix} = \begin{bmatrix} -2 \\ 0 \end{bmatrix}
    \qquad (\text{boundary candidates})
    $$

    ③ &nbsp; Compare:

    $$
    f(\vec{a}) = -1 \ \ (\text{min}), \qquad f(\vec{b}) = 0, \qquad f(\vec{c}) = 8 \ \ (\text{max})
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    st = mo.ui.slider(0, 24, 1, value=4, label=r"$k$, with $t = k\pi/12$", show_value=True)
    return (st,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, ORANGE, RED, cross_axes, legend_box, math, mo, np, num, st, table, tip_label):
    _t = st.value * math.pi / 12
    _pt = (2 * math.cos(_t), 2 * math.sin(_t))
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    def _g(t):
        return 4 - 4 * np.cos(t)

    _fig = Figure(figsize=(FULL, 3.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2, width_ratios=[1, 1.35])

    # D with the level sets of f (circles about a), the candidates and the point of Bd(D) at time t
    _left.set_xlim(-2.6, 2.75)
    _left.set_ylim(-2.45, 2.6)
    _left.set_aspect("equal")
    _left.axis("off")
    _th = np.linspace(0, 2 * np.pi, 241)
    _left.fill(2 * np.cos(_th), 2 * np.sin(_th), color=LIGHT, lw=0, zorder=0)
    _disc = _left.fill(2 * np.cos(_th), 2 * np.sin(_th), color="none", lw=0)[0]
    for _c in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        (_ring,) = _left.plot(1 + math.sqrt(_c + 1) * np.cos(_th), math.sqrt(_c + 1) * np.sin(_th), color=GREY, lw=0.6, zorder=1)
        _ring.set_clip_path(_disc)
    _left.plot(2 * np.cos(_th), 2 * np.sin(_th), color=BLUE, lw=1.4, zorder=2)
    cross_axes(_left, (-2.5, 2.7), (-2.4, 2.55), "$x^1$", "$x^2$")
    for _p, _col in (((1, 0), GREEN), ((2, 0), ORANGE), ((-2, 0), RED)):
        _left.plot(*_p, "o", color=_col, ms=6, zorder=5)
    _left.plot(*_pt, "o", color="black", ms=6, zorder=6)
    tip_label(_left, (-1.45, -1.45), -135, r"$\mathrm{Bd}(D)$", BLUE, r=4, fontsize=12)

    # g(t) = f on Bd(D), with the value of f at the interior candidate
    _right.set_xlim(-0.6, 7.6)
    _right.set_ylim(-1.8, 9.2)
    _right.set_aspect(0.55)
    _right.axis("off")
    cross_axes(_right, (-0.4, 7.2), (-1.6, 9.1), "$t$", "$y$")
    _s = np.linspace(0, 2 * math.pi, 300)
    _right.plot(_s, _g(_s), color=BLUE, lw=1.6)
    _right.plot([0, 2 * math.pi], [-1, -1], color=GREEN, lw=1.0, ls=(0, (4, 3)))
    for _x, _name in ((math.pi, r"$\pi$"), (2 * math.pi, r"$2\pi$")):
        _right.plot([_x, _x], [-0.15, 0.15], color="black", lw=0.9)
        _right.text(_x, 0.35, _name, ha="center", va="bottom", fontsize=12, bbox=_box)
    for _x, _col in ((0, ORANGE), (math.pi, RED), (2 * math.pi, ORANGE)):
        _right.plot(_x, _g(_x), "o", color=_col, ms=6, zorder=5)
    _right.text(4.9, 7.9, r"$g(t) = 4 - 4\cos(t)$", color=BLUE, fontsize=12, ha="left", va="center")
    _right.plot(_t, _g(_t), "o", color="black", ms=6, zorder=6)
    legend_box(
        _fig,
        [
            ("dot", GREEN, r"$\vec{a}$"),
            ("dot", ORANGE, r"$\vec{b}$"),
            ("dot", RED, r"$\vec{c}$"),
            ("dot", "black", r"$\genfrac{[}{]}{0}{0}{2\cos(t)}{2\sin(t)}$ (left), $\genfrac{[}{]}{0}{0}{t}{g(t)}$ (right)"),
            ("line", GREY, r"level sets of $f$"),
            ("line", GREEN, r"$y = f(\vec{a}) = -1$", (0, (4, 3))),
        ],
        loc="outside lower center",
        ncols=3,
    )

    mo.vstack(
        [
            mo.hstack([st], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$t = k\pi/12$", rf"${num(_t)}$"),
                    (r"$\begin{bmatrix} 2\cos(t) \\ 2\sin(t) \end{bmatrix} \in \mathrm{Bd}(D)$", rf"$\begin{{bmatrix}} {num(_pt[0])} \\ {num(_pt[1])} \end{{bmatrix}}$"),
                    (r"$g(t) = 4 - 4\cos(t)$", rf"${num(4 - 4 * math.cos(_t))}$"),
                    (r"$g'(t) = 4\sin(t)$", rf"${num(4 * math.sin(_t))}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, LIGHT, ORANGE, RED, np, panel, sheet, turntable):
    # graph(f) over D, the same rule outside D in a faint tone, f restricted to Bd(D), and the three candidates
    def _f(x1, x2):
        return x1**2 + x2**2 - 2 * x1

    _r, _p = np.meshgrid(np.linspace(0, 2, 21), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _q, _w = np.meshgrid(np.linspace(2, 2.6, 7), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _t = np.linspace(0, 2 * np.pi, 241)
    _c1, _c2 = 2 * np.cos(_t), 2 * np.sin(_t)
    _faint = "#c4c4c4"
    turntable(
        -75,
        48,
        "graph of f over the disc D, the same rule outside D in a faint tone, f restricted to the boundary of D, and the three candidates",
        [
            panel(
                0.3,
                surfaces=[
                    sheet(_r * np.cos(_p), _r * np.sin(_p), _f(_r * np.cos(_p), _r * np.sin(_p)), wire=[(0, 5, BLUE, 0.6), (1, 8, BLUE, 0.6)]),
                    sheet(_q * np.cos(_w), _q * np.sin(_w), _f(_q * np.cos(_w), _q * np.sin(_w)), wire=[(0, 6, _faint, 0.5), (1, 8, _faint, 0.5)], alpha=0.3),
                ],
                lines=[(_c1, _c2, _f(_c1, _c2), BLUE, 2.2), (_c1, _c2, 0 * _t, BLUE, 1.0, [4, 3])],
                points=[((1, 0, -1), GREEN), ((2, 0, 0), ORANGE), ((-2, 0, 8), RED)],
                axes=[((0, 0, 0), (2.9, 0, 0), "x^1", -30), ((0, 0, 0), (0, 2.9, 0), "x^2", 30), ((0, 0, 0), (0, 0, 9), "y", 90)],
            )
        ],
        legend=[
            ("area", LIGHT, r"y = f(\vec{x}), \ \vec{x} \in D", BLUE),
            ("area", LIGHT, r"\text{the same rule outside } D", _faint, 0.35),
            ("line", BLUE, r"f \text{ restricted to } \mathrm{Bd}(D)", 2.2),
            ("line", BLUE, r"\mathrm{Bd}(D)", 1.0, [4, 3]),
            ("dot", GREEN, r"\vec{a}: \ f(\vec{a}) = -1 \ (\text{min})"),
            ("dot", ORANGE, r"\vec{b}: \ f(\vec{b}) = 0"),
            ("dot", RED, r"\vec{c}: \ f(\vec{c}) = 8 \ (\text{max})"),
        ],
        height=400,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    q1_max, q1_min = _field(), _field()
    return q1_max, q1_min


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, check, cross_axes, legend_box, mo, q1_max, q1_min):
    def _ask(label, field, answer):
        return mo.hstack([mo.md(label), field, mo.md(check(field, answer))], justify="start", align="center")

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(HALF + 0.4, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.6, 3.1)
    _ax.set_ylim(-0.6, 3.75)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-0.4, 3.0), (-0.4, 3.7), "$x^1$", "$x^2$")
    _ax.fill([0, 2, 2, 0], [0, 0, 3, 3], color=LIGHT, lw=0)
    _ax.plot([0, 2, 2, 0, 0], [0, 0, 3, 3, 0], color=BLUE, lw=1.4)
    for _c in ((0, 0), (2, 0), (2, 3), (0, 3)):
        _ax.plot(*_c, "o", ms=4, color=BLUE, zorder=3)
    _ax.text(2, -0.1, "$2$", ha="center", va="top", fontsize=12, bbox=_box)
    _ax.text(-0.1, 3, "$3$", ha="right", va="center", fontsize=12, bbox=_box)
    legend_box(_fig, [("area", LIGHT, "$D$", BLUE)])

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    $$
    f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^3 + (x^2)^2 - 3x^1 - 2x^2
    $$

    (a) Find all critical points in $\mathbb{R}^2$.

    (b) Decide their type (via 2nd derivative test).

    (c) Find the global maximum and global minimum over

    $$
    D = [0, 2] \times [0, 3] = \left\{\, 0 \leq x^1 \leq 2,\ 0 \leq x^2 \leq 3 \,\right\}
    $$
    """
            ),
            _fig,
            mo.md(r"""$\leadsto$ &nbsp; parameterize the boundary with 4 different line segments"""),
            _ask(r"global maximum value of $f$ over $D$ $=$", q1_max, 5),
            _ask(r"global minimum value of $f$ over $D$ $=$", q1_min, -3),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $\vec{a} \in D$ is a global maximum (minimum) of $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ if $f(\vec{x}) \leq f(\vec{a})$ ($f(\vec{x}) \geq f(\vec{a})$) for all $\vec{x} \in D$
    - $D$ is bounded if it is contained in some ball $B(\vec{0}, r)$; its boundary $\mathrm{Bd}(D)$ is the set of points $\vec{a}$ such that any ball centered at $\vec{a}$ contains both points in $D$ and points not in $D$; $D$ is closed if $\mathrm{Bd}(D) \subseteq D$
    - a continuous $f$ over a closed and bounded domain $D$ has both a global maximum and a global minimum
    - a global extremum lies in $\mathrm{Bd}(D)$, or it is a local extremum in $D \setminus \mathrm{Bd}(D)$
    - strategy: find the critical points in $D \setminus \mathrm{Bd}(D)$; find the global extrema of $f$ on $\mathrm{Bd}(D)$, via a parameterization of the boundary; compare the values of all candidate points
    """)
    return


if __name__ == "__main__":
    app.run()
