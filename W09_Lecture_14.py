import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 14 • Local extrema and the second derivative test", css_file="bs101.css")


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
    #   GREEN  a result made from them (sum, multiple, angle, tangent vector, gradient)
    #   ORANGE (ochre) a third object, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
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
        One line weight for every figure; the head is open and sized in points from the line width,
        so arrows look alike across lectures at any axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={3 * lw:g},head_width={1.3 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 14", "Week 09", "Lecture 14 • Local extrema and the second derivative test")
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
        """Number for the readout tables: exact when a multiple of 1/2, otherwise fixed-point (never a negative zero)."""
        if abs(2 * v - round(2 * v)) < 1e-9:
            return f"{round(2 * v) / 2 + 0.0:g}"
        return f"{round(v, digits) + 0.0:.{digits}f}"

    return cross_axes, num, tip_label


@app.cell(hide_code=True)
def _(mo, np):
    # ---- Interactive 3D figures ------------------------------------------
    # Drawn in the browser on canvases, in the style of the static figures: orthographic views of
    # R^3 = R^2 x R (x^1 towards the viewer, x^2 to the right, y up), surfaces drawn back to front.
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

    Higher derivatives of $f : \mathbb{R}^n \longrightarrow \mathbb{R}$

    - if $f$ is $C^2$-smooth at $\vec{x} = \vec{a}$ (continuous 2nd order partial derivatives at $\vec{a}$), then

        $$
        f(\vec{x}) = \underbrace{f(\vec{a}) + Df(\vec{a})(\vec{x} - \vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}_{\mathclap{\footnotesize \text{good quadratic approximation}}\vphantom{\footnotesize \text{good quadratic approximation}}} + \underbrace{o\big( \lVert \vec{x} - \vec{a} \rVert^2 \big)}_{\mathclap{\footnotesize \begin{matrix}\text{error goes to zero} \\ \text{faster than } \lVert \vec{x} - \vec{a} \rVert^2\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{error goes to zero} \\ \text{faster than } \lVert \vec{x} - \vec{a} \rVert^2\end{matrix}}}
        $$

    - where

        $$
        \underbrace{Df(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) & \cdots & \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} \in \mathrm{Mat}(1 \times n)}_{\mathclap{\footnotesize \text{derivative matrix}}\vphantom{\footnotesize \text{derivative matrix}}},
        \qquad
        \underbrace{Hf(\vec{a}) = \begin{bmatrix}
        \dfrac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^1 \partial x^n}(\vec{a}) \\
        \vdots & \ddots & \vdots \\
        \dfrac{\partial^2 f}{\partial x^n \partial x^1}(\vec{a}) & \cdots & \dfrac{\partial^2 f}{\partial x^n \partial x^n}(\vec{a})
        \end{bmatrix} \in \mathrm{Mat}(n \times n)}_{\mathclap{\footnotesize \text{Hessian matrix}}\vphantom{\footnotesize \text{Hessian matrix}}}
        $$

    **In this lecture:** application to optimization: finding maximal / minimal values of scalar valued functions

    **References:** MT 3.3
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""## III.1 &nbsp; Local extrema and the second derivative test"""),
            definition(
                r"""
    Given $f : \mathbb{R}^n \longrightarrow \mathbb{R}$, a point $\vec{a} \in \mathbb{R}^n$ is

    - a **local maximum** of $f$ if there is some open ball $B(\vec{a}, \delta)$ centered at $\vec{a}$ such that

        $$
        f(\vec{x}) \leq f(\vec{a}) \qquad \forall\, \vec{x} \in B(\vec{a}, \delta)
        $$

        (the value of $f$ at $\vec{a}$ is the largest value nearby $\vec{x} = \vec{a}$)

    - a **local minimum** of $f$ if there is some open ball $B(\vec{a}, \delta)$ centered at $\vec{a}$ such that

        $$
        f(\vec{x}) \geq f(\vec{a}) \qquad \forall\, \vec{x} \in B(\vec{a}, \delta)
        $$
    """,
                "Local maximum and local minimum",
            ),
            theorem(
                r"""
    If $f$ is differentiable at $\vec{x} = \vec{a}$ and $\vec{x} = \vec{a}$ is a local maximum or a local minimum of $f$ (a **local extremum** of $f$), then

    $$
    \vec{\nabla} f(\vec{a}) = \vec{0} \in \mathbb{R}^n
    $$

    (equivalently, $Df(\vec{a}) \in \mathrm{Mat}(1 \times n)$ is the zero matrix)
    """,
                "Derivative at a local extremum",
            ),
            mo.md(
                r"""
    **Proof.** Let's assume $\vec{a}$ is a local maximum of $f$. Consider

    $$
    g : \mathbb{R} \longrightarrow \mathbb{R}, \qquad t \longmapsto g(t) = f(\vec{a} + t\vec{e}_1)
    $$

    Since $\vec{x} = \vec{a}$ is a local maximum of $f$, $t = 0$ is a local maximum of $g$:

    $$
    f(\vec{a}) \geq f(\vec{x}) \quad \forall\, \vec{x} \in B(\vec{a}, \delta)
    \qquad \Longrightarrow \qquad
    g(0) = f(\vec{a}) \geq g(t) = f(\vec{a} + t\vec{e}_1) \quad \forall\, t \in (-\delta, \delta)
    $$

    Since $f$ is differentiable at $\vec{x} = \vec{a}$, $g$ is differentiable at $t = 0$:

    $$
    g'(0) = \lim_{t \to 0} \frac{g(t) - g(0)}{t} = \lim_{t \to 0} \frac{f(\vec{a} + t\vec{e}_1) - f(\vec{a})}{t} = \frac{\partial f}{\partial x^1}(\vec{a})
    $$

    From single variable calculus

    $$
    \Longrightarrow \qquad g'(0) = \frac{\partial f}{\partial x^1}(\vec{a}) = 0
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, definition, mo, np, panel, sheet, turntable):
    # f has a local maximum at a (but larger values further along e_1); its restrictions to a + t e_1 and a + t e_2
    _a = (1.4, 1.3)

    def _f(x1, x2):
        u, w = x1 - _a[0], x2 - _a[1]
        return 0.2 + 1.3 * np.exp(-(u**2 + 1.6 * w**2)) + 1.8 * np.exp(-2 * ((u - 2.3) ** 2 + w**2))

    _fa = float(_f(*_a))
    _u1, _u2 = np.meshgrid(np.linspace(_a[0] - 1.3, _a[0] + 3.2, 91), np.linspace(_a[1] - 1.2, _a[1] + 1.2, 49), indexing="ij")
    _t1, _t2 = np.linspace(-1.3, 3.2, 181), np.linspace(-1.2, 1.2, 97)
    _k = np.array([-0.9, 0.9])
    _graph = turntable(
        28,
        24,
        "graph of f near its local maximum at a, with the restrictions of f to the lines through a in the directions e1 and e2",
        [
            panel(
                0.8,
                surfaces=[sheet(_u1, _u2, _f(_u1, _u2), wire=[(0, 5, BLUE, 0.5), (1, 6, BLUE, 0.5)])],
                lines=[
                    (_a[0] + _t1, _a[1] + 0 * _t1, _f(_a[0] + _t1, _a[1]), BLUE, 2.4),
                    (_a[0] + 0 * _t2, _a[1] + _t2, _f(_a[0], _a[1] + _t2), RED, 2.4),
                    (_a[0] + _t1, _a[1] + 0 * _t1, 0 * _t1, BLUE, 1.0, [4, 3]),
                    (_a[0] + 0 * _t2, _a[1] + _t2, 0 * _t2, RED, 1.0, [4, 3]),
                    (_a[0] + _k, _a[1] + 0 * _k, _fa + 0 * _k, GREEN, 2.2),
                    (_a[0] + 0 * _k, _a[1] + _k, _fa + 0 * _k, GREEN, 2.2),
                ],
                points=[((_a[0], _a[1], _fa), "#000000")],
                axes=[((0, 0, 0), (5.0, 0, 0), "x^1", -150), ((0, 0, 0), (0, 2.9, 0), "x^2", -20), ((0, 0, 0), (0, 0, 2.5), "y", 90)],
                texts=[
                    ((_a[0] + 2.3, _a[1], _f(_a[0] + 2.3, _a[1])), r"y = f(\vec{a} + t\vec{e}_1)", BLUE, 150, 6),
                    ((_a[0], _a[1] + 0.35, _f(_a[0], _a[1] + 0.35)), r"y = f(\vec{a} + t\vec{e}_2)", RED, 45, 45),
                    ((_a[0] + _t1[-1], _a[1], 0), r"\vec{a} + t\vec{e}_1", BLUE, -60, 6),
                    ((_a[0], _a[1] + _t2[-1], 0), r"\vec{a} + t\vec{e}_2", RED, -20, 6),
                ],
            )
        ],
        height=440,
    )


    mo.vstack(
        [
            _graph,
            mo.md(
                r"""
    Repeat with $g(t) = f(\vec{a} + t\vec{e}_i)$ for each $i = 1, \dots, n$

    $$
    \Longrightarrow \qquad \vec{\nabla} f(\vec{a}) = \begin{bmatrix} \dfrac{\partial f}{\partial x^1}(\vec{a}) \\ \vdots \\ \dfrac{\partial f}{\partial x^n}(\vec{a}) \end{bmatrix} = \begin{bmatrix} 0 \\ \vdots \\ 0 \end{bmatrix} = \vec{0} \tag*{$\square$}
    $$
    """
            ),
            definition(
                r"""
    A point $\vec{a} \in \mathbb{R}^n$ such that $\vec{\nabla} f(\vec{a}) = \vec{0}$ is called a **critical point** of $f$.
    """,
                "Critical point",
            ),
            mo.md(
                r"""
    **Remark.** Local extremum where $f$ is differentiable &nbsp; $\Longrightarrow$ &nbsp; critical point!

    Critical point &nbsp; $\nRightarrow$ &nbsp; local extremum!
    """
            ),
            definition(
                r"""
    A critical point of $f$ that is not a local extremum is called a **saddle point**.
    """,
                "Saddle point",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = -(x^1)^2 + (x^2)^2$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} -2x^1 \\ 2x^2 \end{bmatrix} \qquad \Longrightarrow \qquad \vec{x} = \vec{0} \text{ is a critical point!}
    $$

    $f(\vec{0}) = -0^2 + 0^2 = 0$, but

    $$
    \begin{aligned}
    f(\vec{x}) &= -t^2 < 0 \quad \text{for } \vec{x} = t\vec{e}_1 = \begin{bmatrix} t \\ 0 \end{bmatrix}, \text{ with } t \neq 0 &&\leadsto \quad \vec{0} \text{ not min!} \\[6pt]
    f(\vec{x}) &= s^2 > 0 \quad \text{for } \vec{x} = s\vec{e}_2 = \begin{bmatrix} 0 \\ s \end{bmatrix}, \text{ with } s \neq 0 &&\leadsto \quad \vec{0} \text{ not max!}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    theta = mo.ui.slider(0, 180, 5, value=30, label=r"$\theta$", show_value=True)
    return (theta,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, ORANGE, RED, math, mo, np, num, panel, sheet, table, theta, turntable):
    _th = math.radians(theta.value)
    _u = (round(math.cos(_th), 12) + 0.0, round(math.sin(_th), 12) + 0.0)
    _c = round(-math.cos(2 * _th), 12) + 0.0  # f(t u) = c t^2

    def _f(x1, x2):
        return -(x1**2) + x2**2

    # graph(f) over the square |x^1|, |x^2| <= 1, with the sections along e_1, e_2 and u
    _R = 1.0
    _g1, _g2 = np.meshgrid(np.linspace(-_R, _R, 41), np.linspace(-_R, _R, 41), indexing="ij")
    _t = np.linspace(-_R, _R, 161)
    _s = np.linspace(-1, 1, 161) * _R / max(abs(_u[0]), abs(_u[1]))
    _edges = [(_t, _k + 0 * _t, _f(_t, _k), BLUE, 1.2) for _k in (-_R, _R)] + [(_k + 0 * _t, _t, _f(_k, _t), BLUE, 1.2) for _k in (-_R, _R)]
    _graph = turntable(
        35,
        28,
        "graph of f, a horse saddle, with its sections along e1, e2 and u",
        [
            panel(
                0.55,
                surfaces=[sheet(_g1, _g2, _f(_g1, _g2), wire=[(0, 5, BLUE, 0.5), (1, 5, BLUE, 0.5)])],
                lines=_edges + [(_t, 0 * _t, _f(_t, 0), GREEN, 1.6), (0 * _t, _t, _f(0, _t), ORANGE, 1.6), (_s * _u[0], _s * _u[1], _c * _s**2, RED, 2.4)],
                points=[((0, 0, 0), "#000000")],
                axes=[((0, 0, 0), (1.7, 0, 0), "x^1", -90), ((0, 0, 0), (0, 1.7, 0), "x^2", -60), ((0, 0, 0), (0, 0, 1.4), "y", 90)],
                texts=[
                    ((_R, 0, _f(_R, 0)), r"y = f(t\vec{e}_1)", GREEN, -150, 10),
                    ((0, -_R, _f(0, -_R)), r"y = f(t\vec{e}_2)", ORANGE, 160, 6),
                    ((0, 0, 1.1), r"y = f(t\vec{u})", RED, 0, 8),
                    ((0, 0, 0), r"\vec{0}", "#000000", 60, 25),
                ],
                box=((-1, 1.7), (-1, 1.7), (-1, 1.4)),
            )
        ],
        height=420,
        key="lecture-14-saddle",
    )

    mo.vstack(
        [
            mo.hstack([theta], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f(t\vec{u}) = \big( \sin^2\theta - \cos^2\theta \big)\, t^2$ for $\vec{u} = \begin{bmatrix} \cos\theta \\ \sin\theta \end{bmatrix}$", rf"${num(_c)}\, t^2$"),
                ]
            ),
            _graph,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; $\mathrm{graph}(f)$ looks like a horse saddle

    Given a critical point, how do we distinguish its type (local max, local min, saddle)?

    $\leadsto$ &nbsp; look at the Hessian matrix!

    $\leadsto$ &nbsp; if $\vec{a}$ is a critical point of $f$ ($Df(\vec{a}) = 0 \in \mathrm{Mat}(1 \times n)$)

    $$
    \underbrace{f(\vec{x}) \approx f(\vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a})}_{\mathclap{\footnotesize \text{near } \vec{x} = \vec{a}}\vphantom{\footnotesize \text{near } \vec{x} = \vec{a}}}
    \quad \left( \begin{matrix} \dfrac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a}) \\[4pt] \text{determines the behavior} \\ \text{of } f \text{ near } \vec{x} = \vec{a}! \end{matrix} \right)
    $$

    **Recall:** $f : \mathbb{R} \longrightarrow \mathbb{R}$ $C^2$-smooth with $f'(a) = 0$

    - $f''(a) < 0$ &nbsp; $\Longrightarrow$ &nbsp; local maximum
    - $f''(a) > 0$ &nbsp; $\Longrightarrow$ &nbsp; local minimum
    - $f''(a) = 0$ &nbsp; $\Longrightarrow$ &nbsp; need more information

    because near $x = a$

    $$
    f(x) = f(a) + f'(a)(x - a) + \frac{1}{2} f''(a)(x - a)^2 + \underbrace{o\big( (x - a)^2 \big)}_{\mathclap{\footnotesize \begin{matrix}\text{error goes to zero} \\ \text{faster than } (x - a)^2\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{error goes to zero} \\ \text{faster than } (x - a)^2\end{matrix}}}
    $$

    and if $a$ is a critical point

    $$
    \Longrightarrow \qquad f(x) \approx f(a) + \frac{1}{2} f''(a)(x - a)^2
    $$

    - if $f''(a) < 0$ &nbsp; $\leadsto$ &nbsp; parabola opens downwards &nbsp; $\Longrightarrow$ &nbsp; $a$ is local max
    - if $f''(a) > 0$ &nbsp; $\leadsto$ &nbsp; parabola opens upwards &nbsp; $\Longrightarrow$ &nbsp; $a$ is local min
    - if $f''(a) = 0$ &nbsp; $\leadsto$ &nbsp; parabola degenerates to a horizontal line … &nbsp; $\Longrightarrow$ &nbsp; not sufficient info
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, Figure, GREY, cross_axes, mo, np):
    # the three cases, one panel each, with a critical point at a
    _a = 1.3
    _cases = (
        (r"$f''(a) < 0$", lambda x: 0.75 + 0.55 * np.cos(1.5 * (x - _a)), -0.55 * 1.5**2),
        (r"$f''(a) > 0$", lambda x: 1.25 - 0.55 * np.cos(1.5 * (x - _a)), 0.55 * 1.5**2),
        (r"$f''(a) = 0$", lambda x: 0.95 + 0.22 * (x - _a) ** 3, 0.0),
    )
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 2.7), layout="constrained")
    _x = np.linspace(_a - 1.45, _a + 1.45, 200)
    _w = np.linspace(_a - 1.1, _a + 1.1, 100)
    for _i, (_ax, (_name, _f, _d2)) in enumerate(zip(_fig.subplots(1, 3), _cases)):
        _ax.set_xlim(-0.35, 3.0)
        _ax.set_ylim(-0.3, 2.05)
        _ax.set_aspect("equal")
        _ax.axis("off")
        cross_axes(_ax, (-0.3, 2.95), (-0.25, 2.0), "$x$", "$y$")
        _ax.plot(_x, _f(_x), color=BLUE, lw=1.6)
        if _d2 != 0:
            _ax.plot(_w, np.full_like(_w, _f(_a)), color=GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.plot(_w, _f(_a) + 0.5 * _d2 * (_w - _a) ** 2, color=GREEN, lw=1.4)
        if _i == 0:
            _ax.text(2.3, 0.97, "$y = f(x)$", color=BLUE, fontsize=11, ha="left", va="bottom")
            _ax.text(_w[0] + 0.05, _f(_a) + 0.06, "$y = f(a)$", color="#6b6b6b", fontsize=11, ha="left", va="bottom")
            _ax.text(1.4, 0.42, r"$y = f(a) + \dfrac{1}{2} f''(a)(x - a)^2$", color=GREEN, fontsize=11, ha="center", va="top")
        _ax.plot(_a, _f(_a), "o", color="black", ms=4, zorder=5)
        _ax.plot([_a, _a], [-0.05, 0.05], color="black", lw=0.9)
        _ax.text(_a, -0.1, "$a$", ha="center", va="top", fontsize=12, bbox=_box)
        _ax.set_title(_name, fontsize=13, y=-0.16)

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; we will generalize this for $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$

    $\leadsto$ &nbsp; for $n > 2$ we need tools from Linear Algebra
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ $C^2$-smooth at a critical point $\vec{x} = \vec{a}$

    $$
    f(\vec{x}) \approx f(\vec{a}) + \frac{1}{2}\, (\vec{x} - \vec{a}) \cdot Hf(\vec{a})(\vec{x} - \vec{a}) = q(\vec{x})
    $$

    Let's write $Hf(\vec{a}) = \begin{bmatrix} A & B \\ C & D \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$, that is, let

    $$
    A = \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{a}), \qquad
    B = \frac{\partial^2 f}{\partial x^1 \partial x^2}(\vec{a}), \qquad
    C = \frac{\partial^2 f}{\partial x^2 \partial x^1}(\vec{a}) = B, \qquad
    D = \frac{\partial^2 f}{\partial x^2 \partial x^2}(\vec{a})
    $$

    $$
    \Longrightarrow \qquad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} \Big( A \underbrace{(x^1 - a^1)^2}_{\mathclap{\footnotesize (v^1)^2}\vphantom{\footnotesize (v^1)^2}} + 2B \underbrace{(x^1 - a^1)(x^2 - a^2)}_{\mathclap{\footnotesize v^1 v^2}\vphantom{\footnotesize v^1 v^2}} + D \underbrace{(x^2 - a^2)^2}_{\mathclap{\footnotesize (v^2)^2}\vphantom{\footnotesize (v^2)^2}} \Big)
    $$

    ① &nbsp; if $A \neq 0$ &nbsp; $\leadsto$ &nbsp; complete the square

    $$
    \Longrightarrow \qquad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} \left( A \left( v^1 + \frac{B}{A} v^2 \right)^2 + \frac{AD - B^2}{A} (v^2)^2 \right)
    $$

    - if $\underbrace{A < 0 \text{ and } AD - B^2 > 0}_{\footnotesize \text{negative definite}}$, then $\mathrm{graph}(q)$ is a paraboloid opening downwards
    - if $\underbrace{A > 0 \text{ and } AD - B^2 > 0}_{\footnotesize \text{positive definite}}$, then $\mathrm{graph}(q)$ is a paraboloid opening upwards
    - if $\underbrace{A \neq 0 \text{ and } AD - B^2 < 0}_{\footnotesize \text{indefinite}}$, then $\mathrm{graph}(q)$ is a horse saddle
    - if $A \neq 0$ and $\underbrace{AD - B^2 = 0}_{\footnotesize \text{degenerate}}$

        $$
        \Longrightarrow \qquad q(\vec{x}) = f(\vec{a}) + \frac{1}{2} A \left( v^1 + \frac{B}{A} v^2 \right)^2
        \qquad \Longrightarrow \qquad \mathrm{graph}(q) \text{ contains a horizontal line …} \quad (\text{is degenerate})
        $$

    ② &nbsp; if $A = 0$

    - $B \neq 0$ &nbsp; ($\Longleftrightarrow$ &nbsp; $AD - B^2 < 0$) &nbsp; $\Longrightarrow$ &nbsp; $q(\vec{x}) = f(\vec{a}) + \dfrac{1}{2} (2B v^1 + D v^2) v^2$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ is a horse saddle
    - $B = 0$ &nbsp; ($\Longleftrightarrow$ &nbsp; $AD - B^2 = 0$) &nbsp; $\Longrightarrow$ &nbsp; $q(\vec{x}) = f(\vec{a}) + \dfrac{1}{2} D (v^2)^2 \rule{0pt}{1.9em}$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{graph}(q)$ contains a horizontal line
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, np, panel, sheet, turntable):
    # graph(q) near a in the four cases, with the point (a, f(a)): over a disc, or over a square
    _a = (1.0, 1.8)
    _cases = (
        ("negative definite", -2.4, 0.5, -2.0, 2.2, False),
        ("positive definite", 2.4, 0.5, 2.0, 0.4, False),
        ("indefinite", -1.4, 0.3, 1.8, 1.2, True),
        ("degenerate", 1.6, 0.0, 0.0, 0.7, True),
    )
    _w = np.linspace(-1, 1, 121)
    _s = np.linspace(0, 1, 40)
    _phi = np.linspace(0, 2 * np.pi, 241)
    _panels = []
    for _name, _A, _B, _D, _fa, _square in _cases:

        def _q(x1, x2, A=_A, B=_B, D=_D, fa=_fa):
            v1, v2 = x1 - _a[0], x2 - _a[1]
            return fa + 0.5 * (A * v1**2 + 2 * B * v1 * v2 + D * v2**2)

        if _square:
            _x1, _x2 = np.meshgrid(_a[0] + 0.85 * np.linspace(-1, 1, 35), _a[1] + 0.85 * np.linspace(-1, 1, 35), indexing="ij")
            _wire = [(0, 5, BLUE, 0.5), (1, 5, BLUE, 0.5)]
            _rim = [(_a[0] + 0.85 * _k + 0 * _w, _a[1] + 0.85 * _w) for _k in (-1, 1)] + [(_a[0] + 0.85 * _w, _a[1] + 0.85 * _k + 0 * _w) for _k in (-1, 1)]
        else:
            _r, _p = np.meshgrid(np.linspace(0, 1, 13), np.linspace(0, 2 * np.pi, 73), indexing="ij")
            _x1, _x2 = _a[0] + _r * np.cos(_p), _a[1] + _r * np.sin(_p)
            _wire = [(0, 4, BLUE, 0.5), (1, 6, BLUE, 0.5)]
            _rim = [(_a[0] + np.cos(_phi), _a[1] + np.sin(_phi))]
        _rr, _bk = (0.85, 0.85) if _square else (1.0, 0.0)  # the point of the rim beside which the name of the graph goes
        _lines = [(_c1, _c2, _q(_c1, _c2), BLUE, 1.2) for _c1, _c2 in _rim]
        _lines.append((_a[0] + 0 * _s, _a[1] + 0 * _s, _fa * _s, GREY, 1.0, [3, 3]))
        _lines.append((_a[0] * _s, _a[1] * _s, _fa + 0 * _s, GREY, 1.0, [3, 3]))  # from f(a) on the y axis to the point
        if _name == "degenerate":  # the horizontal line v^1 + (B / A) v^2 = 0 at height f(a)
            _d = np.array([-_B, _A]) / np.hypot(_A, _B)
            _lines.append((_a[0] + 0.85 * _w * _d[0], _a[1] + 0.85 * _w * _d[1], _fa + 0 * _w, GREEN, 2.2))
        _panels.append(
            panel(
                0.6,
                surfaces=[sheet(_x1, _x2, _q(_x1, _x2), wire=_wire, alpha=0.6 if _name == "positive definite" else 1.0)],
                lines=_lines,
                points=[((_a[0], _a[1], _fa), "#000000"), ((_a[0], _a[1], 0), GREY, 3.4)],
                axes=[((0, 0, 0), (2.2, 0, 0), "x^1", -150), ((0, 0, 0), (0, 3.2, 0), "x^2", -20), ((0, 0, 0), (0, 0, 2.9), "y", 90)],
                texts=[
                    ((_a[0], _a[1], 0), r"\vec{x} = \vec{a}", "#000000", -30, 6),
                    ((0, 0, _fa), r"f(\vec{a})", "#000000", 180, 6),
                    ((_a[0] - _bk, _a[1] + _rr, _q(_a[0] - _bk, _a[1] + _rr)), r"y = q(\vec{x})", BLUE, 20 if _square else 10, 6),
                ],
                caption=rf"\text{{{_name}}}",
                box=((-0.2, 2.2), (-0.2, 3.2), (-0.2, 2.9)),
            )
        )
    turntable(
        28,
        24,
        "graph of q near a critical point a in the four cases: negative definite, positive definite, indefinite, degenerate",
        _panels,
        height=260,
        cols=2,
    )
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    $H = \begin{bmatrix} A & B \\ B & D \end{bmatrix} \in \mathrm{Mat}(2 \times 2)$ is called

    - **negative definite** if $\det H > 0$ and $A < 0$
    - **positive definite** if $\det H > 0$ and $A > 0$
    - **indefinite** if $\det H < 0$
    - **degenerate** if $\det H = 0$
    """,
        "Definite, indefinite and degenerate matrices",
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ $C^2$-smooth at a critical point $\vec{x} = \vec{a}$

    - if $Hf(\vec{a})$ is negative definite &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is local max
    - if $Hf(\vec{a})$ is positive definite &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is local min
    - if $Hf(\vec{a})$ is indefinite &nbsp; $\Longrightarrow$ &nbsp; $\vec{a}$ is a saddle
    - if $Hf(\vec{a})$ is degenerate &nbsp; $\Longrightarrow$ &nbsp; not sufficient info …
    """,
                "Second derivative test",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $f\!\left( \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \right) = (x^1)^3 - 3x^1 x^2 + (x^2)^3$

    $\leadsto$ &nbsp; critical points:

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 3(x^1)^2 - 3x^2 \\ -3x^1 + 3(x^2)^2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    \quad \Longleftrightarrow \quad
    \begin{cases} x^2 = (x^1)^2 \\ x^1 = (x^2)^2 \end{cases}
    \quad \Longleftrightarrow \quad
    \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} = \underbrace{\begin{bmatrix} 0 \\ 0 \end{bmatrix}}_{\mathclap{\footnotesize \vec{a}}\vphantom{\footnotesize \vec{a}}} \text{ or } \underbrace{\begin{bmatrix} 1 \\ 1 \end{bmatrix}}_{\mathclap{\footnotesize \vec{b}}\vphantom{\footnotesize \vec{b}}}
    $$

    $\leadsto$ &nbsp; Hessian matrix:

    $$
    Hf(\vec{x}) = \begin{bmatrix} 6x^1 & -3 \\ -3 & 6x^2 \end{bmatrix}
    $$

    At $\vec{a} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$:

    $$
    Hf(\vec{a}) = \begin{bmatrix} 0 & -3 \\ -3 & 0 \end{bmatrix}
    \qquad \Longrightarrow \qquad \underbrace{\det Hf(\vec{a}) = -9 < 0}_{\mathclap{\footnotesize \text{indefinite}}\vphantom{\footnotesize \text{indefinite}}}
    \qquad \Longrightarrow \qquad \vec{a} \text{ is a saddle}
    $$

    At $\vec{b} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$:

    $$
    Hf(\vec{b}) = \begin{bmatrix} 6 & -3 \\ -3 & 6 \end{bmatrix}
    \qquad \Longrightarrow \qquad \underbrace{\det Hf(\vec{b}) = 27 > 0, \quad \frac{\partial^2 f}{\partial x^1 \partial x^1}(\vec{b}) = 6 > 0}_{\mathclap{\footnotesize \text{positive definite}}\vphantom{\footnotesize \text{positive definite}}}
    \qquad \Longrightarrow \qquad \vec{b} \text{ is local min}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    level = mo.ui.slider(-1.2, 0.8, 0.1, value=-0.5, label="$c$", show_value=True)
    return (level,)


@app.cell(hide_code=True)
def _(BLUE, GREY, RED, level, mo, np, panel, sheet, turntable):
    import contourpy

    # graph(f) over a disc around the saddle a and the local minimum b, cut by the plane y = c
    def _f(x1, x2):
        return x1**3 - 3 * x1 * x2 + x2**3

    _lc = level.value
    _o, _R = (0.5, 0.5), 1.0
    _r, _p = np.meshgrid(np.linspace(0, _R, 21), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _x1, _x2 = _o[0] + _r * np.cos(_p), _o[1] + _r * np.sin(_p)
    _phi = np.linspace(0, 2 * np.pi, 241)
    _rim = (_o[0] + _R * np.cos(_phi), _o[1] + _R * np.sin(_phi))
    _top = (_o[0] + _R * np.cos(-np.pi / 4), _o[1] + _R * np.sin(-np.pi / 4))  # the highest point of the rim

    # the level set f = c inside the disc, in pieces
    _g = np.linspace(-_R, _R, 241)
    _G1, _G2 = np.meshgrid(_o[0] + _g, _o[1] + _g)
    _pieces = []
    for _ln in contourpy.contour_generator(_G1, _G2, _f(_G1, _G2)).lines(_lc):
        _in = np.hypot(_ln[:, 0] - _o[0], _ln[:, 1] - _o[1]) <= _R
        _cut = np.flatnonzero(np.diff(_in.astype(int))) + 1
        for _seg, _keep in zip(np.split(_ln, _cut), np.split(_in, _cut)):
            if _keep[0] and len(_seg) > 1:
                _pieces.append(_seg)
    _plane = [(_o[0] - _R, _o[1] - _R, _lc), (_o[0] + _R, _o[1] - _R, _lc), (_o[0] + _R, _o[1] + _R, _lc), (_o[0] - _R, _o[1] + _R, _lc)]

    _graph = turntable(
        -135,
        30,
        "graph of f over a disc around the saddle a and the local minimum b, cut by the plane y = c along the level set f = c",
        [
            panel(
                0.45,
                surfaces=[sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, BLUE, 0.5), (1, 8, BLUE, 0.5)])],
                lines=[(_rim[0], _rim[1], _f(*_rim), BLUE, 1.2)] + [(_q[:, 0], _q[:, 1], _lc + 0 * _q[:, 0], RED, 2.4) for _q in _pieces]
                + [(np.linspace(_e0[0], _e1[0], 60), np.linspace(_e0[1], _e1[1], 60), np.full(60, _lc), GREY, 1.2) for _e0, _e1 in zip(_plane, _plane[1:] + _plane[:1])],  # the edge of the plane y = c
                points=[((0, 0, 0), "#000000"), ((1, 1, -1), "#000000")],
                axes=[((0, 0, 0), (2.4, 0, 0), "x^1", 90), ((0, 0, 0), (0, 2.4, 0), "x^2", 90), ((0, 0, 0), (0, 0, 2.6), "y", 90)],
                texts=[
                    ((0, 0, 0), r"\vec{a}", "#000000", -90, 8),
                    ((1, 1, -1), r"\vec{b}", "#000000", 0, 9),
                    ((_top[0], _top[1], _f(*_top)), r"y = f(\vec{x})", BLUE, 0, 6),
                    (_plane[3], r"y = c", GREY, 180, 6),
                ],
                box=((_o[0] - _R, 2.4), (_o[1] - _R, 2.4), (-1.2, 2.6)),
            )
        ],
        height=420,
        key="lecture-14-level",
    )
    mo.vstack([mo.hstack([level], justify="start"), _graph])
    return


if __name__ == "__main__":
    app.run()
