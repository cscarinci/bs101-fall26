import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 20 • Double integrals", css_file="bs101.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

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

    return BLUE, GREEN, GREY, LIGHT, ORANGE, RED, arrow, definition, header, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 20", "Week 12", "Lecture 20 • Double integrals")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, ORANGE, RED, arrow, math, np):
    # ---- Helpers of this lecture ----------------------------------------
    def sketch(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges;
        the scale never changes with a slider (names are kept inside the ranges)."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def beside(ax, at, angle, text, color, w, h, gap=4, fontsize=13):
        """Name centred beside the point `at`, in the direction `angle` (degrees), far enough for a
        w x h box (points) to clear it."""
        c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        d = w / 2 * abs(c) + h / 2 * abs(s) + gap
        ax.annotate(text, at, textcoords="offset points", xytext=(d * c, d * s), ha="center", va="center", color=color, fontsize=fontsize, zorder=8, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    def plane(xlim, ylim, width):
        """A sketch of the xy-plane: the two axes as arrows, named at their tips."""
        fig, ax = sketch(xlim, ylim, width)
        arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, "$x$", "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, "$y$", "black", 10, 12)
        return fig, ax

    def bracket(ax, lo, hi, color, vertical=False, h=0.09):
        """The interval [lo, hi] of the x axis (of the y axis if `vertical`), drawn over the axis between two square brackets."""

        def line(u, v):
            ax.plot(*((v, u) if vertical else (u, v)), color=color, lw=1.6, solid_capstyle="butt", zorder=4)

        line([lo, hi], [0, 0])
        for e, d in ((lo, 1), (hi, -1)):
            line([e + d * 0.6 * h, e, e, e + d * 0.6 * h], [h, h, -h, -h])

    def parabola():
        """The region D of the example of p. 6, between the parabola y = x^2 and the line y = 1."""
        fig, ax = plane((-1.8, 2.25), (-0.5, 2.05), 4.6)
        s, d = np.linspace(-1.28, 1.28, 200), np.linspace(-1, 1, 200)
        ax.fill_between(d, d**2, 1, color=LIGHT, lw=0, zorder=0)
        ax.plot(s, s**2, color=RED, lw=1.8)
        ax.plot([-1.5, 1.5], [1, 1], color=ORANGE, lw=1.8)
        beside(ax, (1.28, 1.28**2), 0, "$y = x^2$", RED, 46, 16)
        beside(ax, (1.5, 1), 0, "$y = 1$", ORANGE, 36, 16)
        ax.text(-0.45, 0.72, "$D$", color=BLUE, fontsize=13, ha="center", va="center", zorder=1)
        return fig, ax

    return beside, bracket, parabola, plane, sketch


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
        if (window.katex) window.typeset(); else { fit(); draw(); }
      }).observe(box.querySelector("[data-scene]") ? box : P.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["data-scene"] });
    }
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

    return frame, panel, sheet, turntable


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Integration of functions and vector fields along 1-dimensional curves in $\mathbb{R}^3$

    $$
    f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R} \quad \text{or} \quad \vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3
    $$

    $C = \gamma([a, b]) \subset D$ &nbsp; parameterized by &nbsp; $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$

    Path integral of $f$ over $C$

    $$
    \int_C f \, ds = \int_a^b \underbrace{f(\gamma(t))}_{\footnotesize f} \, \underbrace{\lVert \gamma'(t) \rVert \, dt}_{\footnotesize ds}
    $$

    Line integral of $\vec{F}$ over $\vec{C}$ (oriented from $\gamma(a)$ to $\gamma(b)$)

    $$
    \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_a^b \underbrace{\vec{F}(\gamma(t))}_{\footnotesize \vec{F}} \cdot \underbrace{\gamma'(t) \, dt}_{\footnotesize d\vec{s}}
    $$

    $\leadsto$ &nbsp; independent of parameterization: given a change of variables

    $$
    t = \varphi(\tilde{t}) \in [a, b] \ \text{ for } \ \tilde{t} \in [c, d], \quad \varphi'(\tilde{t}) \neq 0
    $$

    $$
    \int_c^d f(\gamma(\varphi(\tilde{t}))) \lVert \gamma'(\varphi(\tilde{t})) \varphi'(\tilde{t}) \rVert \, d\tilde{t} = \int_a^b f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt
    $$

    $$
    \int_c^d \vec{F}(\gamma(\varphi(\tilde{t}))) \cdot \gamma'(\varphi(\tilde{t})) \varphi'(\tilde{t}) \, d\tilde{t} = \pm \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt
    $$

    $$
    \begin{cases} + & \text{if } \varphi'(\tilde{t}) > 0 \quad (\varphi \text{ preserves orientation}) \\ - & \text{if } \varphi'(\tilde{t}) < 0 \quad (\varphi \text{ reverses orientation}) \end{cases}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    If $\vec{F} = \vec{\nabla} f$, then

    $$
    \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt = \overset{\mathclap{\footnotesize \begin{matrix} \text{end} \\ \downarrow \end{matrix}}}{f(\gamma(b))} - \overset{\mathclap{\footnotesize \begin{matrix} \text{start} \\ \downarrow \end{matrix}}}{f(\gamma(a))}
    $$

    only depends on the (oriented) end points of $\vec{C}$

    (in particular, $\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = 0$ over closed curves)
    """,
        "Line integrals of gradient vector fields",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; in this case, we call $\vec{F} = \vec{\nabla} f$ a **conservative vector field** and $f$ a **potential function** for $\vec{F}$

    **In this lecture:** Multivariable integrals in $\mathbb{R}^n$ ($n = 2$)

    $\leadsto$ &nbsp; to be able to define integrals of vector fields $\underbrace{\text{over surfaces in } \mathbb{R}^3}_{\mathclap{\footnotesize \text{in a few weeks…}}\vphantom{\footnotesize \text{in a few weeks…}}}$

    **References:** MT 5.1, 5.2, 5.3, 5.4

    ## IV.4 &nbsp; Double integrals

    **Recall:** for $f : [a, b] \longrightarrow \mathbb{R}$

    $$
    \int_a^b f(t) \, dt = \lim_{N \to \infty} \sum_{i=1}^N f(t_i) \Delta t
    $$

    where, for each $N \in \mathbb{N}_{>0}$,

    - divide $\displaystyle [a, b] = \bigcup_{i=1}^N [a_i, b_i]$, with

    $$
    a = a_1, \ b_1 = a_2, \ \ldots, \ b_{N-1} = a_N, \ b_N = b, \quad b_i - a_i = \frac{b - a}{N} = \Delta t
    $$

    - choose $t_i \in [a_i, b_i]$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, arrow, beside, mo, sketch):
    # the interval [a, b] cut into N intervals [a_i, b_i] (p. 2): the left end points a_1, ..., a_N named above the axis, the
    # right end points b_1, ..., b_N below it, and one point t_i (blue) chosen in each interval
    _fig, _ax = sketch((-0.7, 6.3), (-0.95, 0.7), 6.2)
    arrow(_ax, (-0.5, 0), (6.1, 0), "black", lw=0.9)
    for _e, _d in ((0, 1), (5, -1)):
        _ax.plot([_e + 0.08 * _d, _e, _e, _e + 0.08 * _d], [0.16, 0.16, -0.16, -0.16], color="black", lw=1.6, zorder=4)
    for _e in (1, 2, 3, 4):
        _ax.plot([_e, _e], [-0.07, 0.07], color="black", lw=1.0)
    for _e, _name in ((0, "$a_1$"), (1, "$a_2$"), (2, "$a_3$"), (3, r"$\cdots$"), (4, "$a_N$"), (5, "$b$")):
        beside(_ax, (_e, 0.16), 90, _name, "black", 24, 16)
    for _e, _name in ((0, "$a$"), (1, "$b_1$"), (2, "$b_2$"), (3, r"$\cdots$"), (4, "$b_{N-1}$"), (5, "$b_N$")):
        beside(_ax, (_e, -0.5), -90, _name, "black", 24, 16, gap=0)
    for _e, _name in ((0.45, "$t_1$"), (1.6, "$t_2$"), (4.55, "$t_N$")):
        _ax.plot(_e, 0, "o", color=BLUE, ms=4.5, zorder=6)
        beside(_ax, (_e, 0), -90, _name, BLUE, 16, 14)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \Longrightarrow \quad \sum_{i=1}^N \underbrace{f(t_i)}_{\footnotesize \text{height}} \, \underbrace{\Delta t}_{\footnotesize \text{base}} \ \approx \ \begin{matrix} \text{signed area between} \\ \mathrm{graph}(f) \text{ and the } t\text{-axis} \end{matrix}
    $$

    How do we integrate functions in $\mathbb{R}^2$?
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, LIGHT, beside, bracket, mo, plane):
    # the rectangle R = [a, b] x [c, d] (p. 3), with [a, b] marked on the x axis and [c, d] on the y axis
    _a, _b, _c, _d = 1.0, 3.4, 0.8, 2.2
    _fig, _ax = plane((-0.7, 4.6), (-0.6, 3.1), 4.2)
    _ax.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=LIGHT, lw=0, zorder=0)
    _ax.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=BLUE, lw=1.8)
    for _e in (_a, _b):
        _ax.plot([_e, _e], [0, _d], "--", color=GREY, lw=0.9, zorder=1)
    for _e in (_c, _d):
        _ax.plot([0, _b], [_e, _e], "--", color=GREY, lw=0.9, zorder=1)
    bracket(_ax, _a, _b, "black")
    bracket(_ax, _c, _d, "black", vertical=True)
    for _e, _name in ((_a, "$a$"), (_b, "$b$")):
        beside(_ax, (_e, 0), -90, _name, "black", 10, 14, gap=7)
    for _e, _name in ((_c, "$c$"), (_d, "$d$")):
        beside(_ax, (0, _e), 180, _name, "black", 10, 14, gap=7)
    beside(_ax, (_b, (_c + _d) / 2), 0, "$R$", BLUE, 12, 14, gap=6)
    mo.hstack([_fig], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose $f : R = [a, b] \times [c, d] \longrightarrow \mathbb{R}$

    - divide $\displaystyle [a, b] = \bigcup_{i=1}^N [a_i, b_i]$ and $\displaystyle [c, d] = \bigcup_{j=1}^N [c_j, d_j]$

    $$
    \begin{aligned} a = a_1, \ b_1 = a_2, \ \ldots, \ b_{N-1} = a_N, \ b_N = b, \quad & b_i - a_i = \frac{b - a}{N} = \Delta x \\ c = c_1, \ d_1 = c_2, \ \ldots, \ d_{N-1} = c_N, \ d_N = d, \quad & d_j - c_j = \frac{d - c}{N} = \Delta y \end{aligned}
    $$

    - choose $(x_i, y_j) \in [a_i, b_i] \times [c_j, d_j]$

    $$
    \iint_R f(x, y) \, dxdy = \lim_{N \to \infty} \sum_{j=1}^N \sum_{i=1}^N f(x_i, y_j) \Delta x \Delta y
    $$

    if the limit exists for every choice $(x_i, y_j)$ and is independent of that choice

    $$
    \Longrightarrow \quad \iint_R f(x, y) \, dxdy = \begin{matrix} \text{signed volume between} \\ \mathrm{graph}(f) \text{ and the } xy\text{-plane} \end{matrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    If $f : R \subset \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous, then $\displaystyle \iint_R f(x, y) \, dxdy$ is well-defined
    """,
        "Double integrals of continuous functions",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof (idea).**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sy = mo.ui.slider(0.6, 2.6, 0.05, value=1.6, label="$y$", show_value=True)
    return (sy,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, mo, np, panel, sheet, sy, turntable):
    # the solid between the rectangle R = [a, b] x [c, d] of the xy-plane and the graph z = f(x, y) (p. 3); its slice at y
    # (green) has the area A(y), and y moves with the slider
    _a, _b, _c, _d = 0.6, 2.4, 0.6, 2.6

    def _f(x, y):
        return 1.3 + 0.25 * np.sin(1.6 * x) + 0.2 * y

    _y = round(sy.value, 10)
    _x1, _x2 = np.meshgrid(np.linspace(_a, _b, 19), np.linspace(_c, _d, 21), indexing="ij")
    _u, _v = np.meshgrid(np.linspace(0, 1, 19), np.linspace(0, 1, 9), indexing="ij")
    _xs, _ys = _a + (_b - _a) * _u, _c + (_d - _c) * _u
    _walls = [sheet(_xs, _q + 0 * _u, _v * _f(_xs, _q), flat=LIGHT, alpha=0.45) for _q in (_c, _d)]
    _walls += [sheet(_q + 0 * _u, _ys, _v * _f(_q, _ys), flat=LIGHT, alpha=0.45) for _q in (_a, _b)]
    _top = sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 6, BLUE, 0.5), (1, 5, BLUE, 0.5)], alpha=0.75)
    _slice = sheet(_xs, _y + 0 * _u, _v * _f(_xs, _y), flat="#a8c6ae", alpha=0.9)
    _s, _t = np.linspace(_a, _b, 60), np.linspace(_c, _d, 60)
    _edges = [(_s, _q + 0 * _s, _f(_s, _q), BLUE, 1.2) for _q in (_c, _d)] + [(_q + 0 * _t, _t, _f(_q, _t), BLUE, 1.2) for _q in (_a, _b)]
    _edges += [(_s, _q + 0 * _s, 0 * _s, BLUE, 1.2) for _q in (_c, _d)] + [(_q + 0 * _t, _t, 0 * _t, BLUE, 1.2) for _q in (_a, _b)]
    _edges += [([_p, _p], [_q, _q], [0, float(_f(_p, _q))], BLUE, 1.2) for _p in (_a, _b) for _q in (_c, _d)]
    _cut = [(_s, _y + 0 * _s, _f(_s, _y), GREEN, 2.2), (_s, _y + 0 * _s, 0 * _s, GREEN, 2.2)]
    _cut += [([_p, _p], [_y, _y], [0, float(_f(_p, _y))], GREEN, 2.2) for _p in (_a, _b)]
    _guides = [([_p, _p], [0, _c], [0, 0], GREY, 1.0, [4, 3]) for _p in (_a, _b)] + [([0, _a], [_q, _q], [0, 0], GREY, 1.0, [4, 3]) for _q in (_c, _d)]
    _guides += [([0, _a], [_y, _y], [0, 0], GREEN, 1.0, [4, 3])]
    _fig = turntable(
        35,
        25,
        "the solid between the rectangle R = [a, b] x [c, d] and the graph z = f(x, y), with its slice at y, of area A(y)",
        [
            panel(
                1.0,
                surfaces=_walls + [_top, _slice],
                lines=_edges + _cut + _guides,
                points=[((0, _y, 0), GREEN, 4.0)],
                axes=[((0, 0, 0), (3.4, 0, 0), "x", -150), ((0, 0, 0), (0, 3.4, 0), "y", 0), ((0, 0, 0), (0, 0, 2.8), "z", 90)],
                texts=[
                    ((_a, 0, 0), "a", "#000000", 180, 4),
                    ((_b, 0, 0), "b", "#000000", 180, 4),
                    ((0, _c, 0), "c", "#000000", -90, 4),
                    ((0, _d, 0), "d", "#000000", -90, 4),
                    ((0, _y, 0), "y", GREEN, 90, 4),
                    (((_a + _b) / 2, _y, float(_f((_a + _b) / 2, _y)) / 2), "A(y)", GREEN, 0, 0),
                    ((_a, _d, float(_f(_a, _d))), "z = f(x, y)", BLUE, 45, 6),
                ],
                box=((0, 3.4), (0, 3.4), (0, 2.8)),
            )
        ],
        height=400,
        key="L20-volume",
        apart=True,
    )
    mo.vstack([mo.hstack([sy], justify="start"), _fig])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("L20-volume", 400)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \text{area} = A(y) = \int_a^b f(x, y) \, dx \qquad \qquad \text{vol} = \int_c^d A(y) \, dy
    $$

    $$
    f(x, y) \text{ continuous} \quad \Longrightarrow \quad A(y) \text{ continuous} \quad \Longrightarrow \quad \text{integrable}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    If $f : R = [a, b] \times [c, d] \longrightarrow \mathbb{R}$ is $\underbrace{\text{continuous}}_{\mathclap{\footnotesize \begin{matrix} \text{also works if discontinuities} \\ \text{are not too bad} \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{also works if discontinuities} \\ \text{are not too bad} \end{matrix}}}$, then

    $$
    \begin{aligned} \iint_R f(x, y) \, dxdy &= \int_c^d \left( \int_a^b f(x, y) \, dx \right) dy \\ &= \int_a^b \left( \int_c^d f(x, y) \, dy \right) dx \end{aligned}
    $$
    """,
        "Fubini",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $f(x, y) = x^2 + y$, &nbsp; $R = [0, 2] \times [0, 3]$

    <span class="chain">$\displaystyle \int_0^3 \left( \int_0^2 (x^2 + y) \, dx \right) dy = \int_0^3 \left( \frac{x^3}{3} + xy \right) \bigg|_{x=0}^{x=2} dy$ $\displaystyle = \int_0^3 \left( \frac{8}{3} + 2y \right) dy = 8 + 9 = 17$</span>

    <span class="chain">$\displaystyle \int_0^2 \left( \int_0^3 (x^2 + y) \, dy \right) dx = \int_0^2 \left( x^2 y + \frac{y^2}{2} \right) \bigg|_{y=0}^{y=3} dx$ $\displaystyle = \int_0^2 \left( 3x^2 + \frac{9}{2} \right) dx = 8 + 9 = 17$</span>

    $$
    \Longrightarrow \quad \iint_R f(x, y) \, dxdy = 17
    $$

    $\leadsto$ &nbsp; double integrals over rectangles = iterated integrals over intervals are independent of the order of integration!

    $\leadsto$ &nbsp; how about $\underbrace{\text{more general regions}}_{\mathclap{\footnotesize \begin{matrix} \text{how to describe them?} \\ \text{how to integrate over them?} \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{how to describe them?} \\ \text{how to integrate over them?} \end{matrix}}}$ ?
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    A region $D \subseteq \mathbb{R}^2$ is called **$y$-simple** if

    $$
    D = \left\{ (x, y) \in \mathbb{R}^2 \mid a \leq x \leq b, \ \varphi_1(x) \leq y \leq \varphi_2(x) \right\}
    $$

    for continuous functions $\varphi_1, \varphi_2 : [a, b] \longrightarrow \mathbb{R}$
    """,
        "y-simple region",
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, ORANGE, RED, beside, bracket, mo, np, plane):
    # the two sketches of p. 5. Left: a y-simple region D between the graphs y = phi_1(x) and y = phi_2(x) over [a, b]; over the
    # point x (green), y runs from phi_1(x) to phi_2(x). Right: an x-simple region D between x = psi_1(y) and x = psi_2(y) over
    # [c, d]; at the height y (green), x runs from psi_1(y) to psi_2(y)
    _s = np.linspace(0.7, 3.2, 200)
    _lo, _hi = 0.8 + 0.18 * np.sin(4 * _s), 2.2 + 0.2 * np.sin(3 * _s)
    _k = 85
    _left, _ax = plane((-1.3, 5.05), (-0.8, 3.75), 3.6)
    _ax.fill_between(_s, _lo, _hi, color=LIGHT, lw=0, zorder=0)
    for _e in (0, -1):
        _ax.plot([_s[_e], _s[_e]], [_lo[_e], _hi[_e]], "--", color=GREY, lw=1.0)
    for _g, _c in ((_lo, RED), (_hi, ORANGE)):
        _ax.plot(_s, _g, color=_c, lw=1.8)
        _ax.plot(_s[[0, -1]], _g[[0, -1]], "o", color=_c, ms=4.5, zorder=6)
    bracket(_ax, _s[0], _s[-1], "black")
    beside(_ax, (_s[0], 0), -90, "$a$", "black", 10, 14, gap=7)
    beside(_ax, (_s[-1], 0), -90, "$b$", "black", 10, 14, gap=7)
    _ax.plot([_s[_k], _s[_k]], [_lo[_k], _hi[_k]], color=GREEN, lw=1.8)
    _ax.plot([0, 0], [_lo[_k], _hi[_k]], color=GREEN, lw=1.8, zorder=5)
    for _p in ((_s[_k], _lo[_k]), (_s[_k], _hi[_k]), (_s[_k], 0), (0, _lo[_k]), (0, _hi[_k])):
        _ax.plot(*_p, "o", color=GREEN, ms=4.5, zorder=7)
    beside(_ax, (_s[_k], 0), -90, "$x$", GREEN, 10, 14, gap=7)
    beside(_ax, (0, _lo[_k]), 180, r"$\varphi_1(x)$", GREEN, 40, 16)
    beside(_ax, (0, _hi[_k]), 180, r"$\varphi_2(x)$", GREEN, 40, 16)
    beside(_ax, (_s[-1], _lo[-1]), 0, r"$y = \varphi_1(x)$", RED, 72, 16, gap=6)
    beside(_ax, (_s[-1], _hi[-1]), 0, r"$y = \varphi_2(x)$", ORANGE, 72, 16, gap=6)
    _ax.text(4.2, (_lo[-1] + _hi[-1]) / 2, "$y$-simple\nregion $D$", color=BLUE, fontsize=13, ha="center", va="center")

    _t = np.linspace(0.6, 2.9, 200)
    _l, _r = 1.5 + 0.18 * np.sin(4 * _t), 2.9 + 0.2 * np.sin(3 * _t)
    _right, _ax = plane((-0.9, 5.45), (-0.8, 3.75), 3.6)
    _ax.fill_betweenx(_t, _l, _r, color=LIGHT, lw=0, zorder=0)
    for _e in (0, -1):
        _ax.plot([_l[_e], _r[_e]], [_t[_e], _t[_e]], "--", color=GREY, lw=1.0)
    for _g, _c in ((_l, RED), (_r, ORANGE)):
        _ax.plot(_g, _t, color=_c, lw=1.8)
        _ax.plot(_g[[0, -1]], _t[[0, -1]], "o", color=_c, ms=4.5, zorder=6)
    bracket(_ax, _t[0], _t[-1], "black", vertical=True)
    beside(_ax, (0, _t[0]), 180, "$c$", "black", 10, 14, gap=7)
    beside(_ax, (0, _t[-1]), 180, "$d$", "black", 10, 14, gap=7)
    _ax.plot([_l[_k], _r[_k]], [_t[_k], _t[_k]], color=GREEN, lw=1.8)
    _ax.plot([_l[_k], _r[_k]], [0, 0], color=GREEN, lw=1.8, zorder=5)
    for _p in ((_l[_k], _t[_k]), (_r[_k], _t[_k]), (0, _t[_k]), (_l[_k], 0), (_r[_k], 0)):
        _ax.plot(*_p, "o", color=GREEN, ms=4.5, zorder=7)
    beside(_ax, (0, _t[_k]), 180, "$y$", GREEN, 10, 14, gap=7)
    beside(_ax, (_l[_k], 0), -90, r"$\psi_1(y)$", GREEN, 40, 16)
    beside(_ax, (_r[_k], 0), -90, r"$\psi_2(y)$", GREEN, 40, 16)
    beside(_ax, (_l[-1], _t[-1]), 100, r"$x = \psi_1(y)$", RED, 72, 16, gap=6)
    beside(_ax, (_r[150], _t[150]), 0, r"$x = \psi_2(y)$", ORANGE, 72, 16, gap=6)
    _ax.text(4.45, 1.0, "$x$-simple\nregion $D$", color=BLUE, fontsize=13, ha="center", va="center")
    mo.hstack([_left, _right], justify="center", gap=1)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Similarly, $D \subseteq \mathbb{R}^2$ is called **$x$-simple** if

    $$
    D = \left\{ (x, y) \in \mathbb{R}^2 \mid c \leq y \leq d, \ \psi_1(y) \leq x \leq \psi_2(y) \right\}
    $$

    for continuous functions $\psi_1, \psi_2 : [c, d] \longrightarrow \mathbb{R}$
    """,
        "x-simple region",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Integration over $y$-simple / $x$-simple regions:

    Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ continuous over $D$ $y$-simple

    $$
    \leadsto \quad \text{take } R = [a, b] \times \underbrace{[c, d]}_{\mathclap{\footnotesize c = \min\limits_{[a, b]} (\varphi_1), \quad d = \max\limits_{[a, b]} (\varphi_2)}} \supseteq D
    $$

    $\leadsto$ &nbsp; define $f^* : R \longrightarrow \mathbb{R}$ via

    $$
    f^*(x, y) = \begin{cases} f(x, y) & \text{if } (x, y) \in D \\ 0 & \text{if } (x, y) \notin D \end{cases}
    $$

    <span class="chain">$\displaystyle \leadsto \quad \iint_D f(x, y) \, dxdy = \iint_R \underbrace{f^*(x, y)}_{\mathclap{\footnotesize \begin{matrix} \text{discontinuous, but} \\ \text{Fubini still works} \end{matrix}}} \, dxdy$ $\displaystyle = \int_a^b \left( \int_c^d f^*(x, y) \, dy \right) dx$ $\displaystyle = \int_a^b \left( \int_{\varphi_1(x)}^{\varphi_2(x)} f(x, y) \, dy \right) dx$</span>

    Similarly, if $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over $D$ $x$-simple

    $$
    \iint_D f(x, y) \, dxdy = \int_c^d \left( \int_{\psi_1(y)}^{\psi_2(y)} f(x, y) \, dx \right) dy
    $$

    **Example.** &nbsp; $D = \left\{ (x, y) \mid x^2 \leq y \leq 1 \right\} = \left\{ (x, y) \mid -1 \leq x \leq 1, \ x^2 \leq y \leq 1 \right\}$ &nbsp; $\leadsto$ &nbsp; $y$-simple
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    xs = mo.ui.slider(-1.0, 1.0, 0.02, value=0.5, label="$x$", show_value=True)
    return (xs,)


@app.cell(hide_code=True)
def _(GREEN, GREY, beside, mo, parabola, xs):
    # the region D of the example as a y-simple region: over the point x (green), y runs from x^2 to 1
    _x = round(xs.value, 10)
    _fig, _ax = parabola()
    _ax.plot([_x, _x], [0, _x**2], ":", color=GREY, lw=0.9)
    _ax.plot([_x, _x], [_x**2, 1], color=GREEN, lw=1.8)
    for _y in (0, _x**2, 1):
        _ax.plot(_x, _y, "o", color=GREEN, ms=4.5, zorder=6)
    beside(_ax, (_x, 0), -90, "$x$", GREEN, 10, 14, gap=6)
    mo.vstack([mo.hstack([xs], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \Longrightarrow \quad \iint_D (xy - 2y) \, dxdy = \int_{-1}^1 \left( \int_{x^2}^1 (xy - 2y) \, dy \right) dx$ $\displaystyle = \int_{-1}^1 \left( x \frac{y^2}{2} - y^2 \right) \bigg|_{y=x^2}^{y=1} dx = \int_{-1}^1 \left( \frac{x}{2} - 1 - \frac{x^5}{2} + x^4 \right) dx$ $\displaystyle = \left( \frac{x^2}{4} - x - \frac{x^6}{12} + \frac{x^5}{5} \right) \bigg|_{x=-1}^{x=1} = -2 + \frac{2}{5} = -\frac{8}{5}$</span>

    Is $D$ $x$-simple? Yes

    $$
    D = \left\{ (x, y) \mid 0 \leq y \leq 1, \ -\sqrt{y} \leq x \leq \sqrt{y} \right\}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ys = mo.ui.slider(0.0, 1.0, 0.02, value=0.5, label="$y$", show_value=True)
    return (ys,)


@app.cell(hide_code=True)
def _(GREEN, beside, math, mo, parabola, ys):
    # the same region D as an x-simple region: at the height y (green), x runs from -sqrt(y) to sqrt(y)
    _y = round(ys.value, 10)
    _r = math.sqrt(_y)
    _fig, _ax = parabola()
    _ax.plot([-_r, _r], [_y, _y], color=GREEN, lw=1.8)
    for _x in (-_r, 0, _r):
        _ax.plot(_x, _y, "o", color=GREEN, ms=4.5, zorder=6)
    beside(_ax, (-_r, _y), 180, "$y$", GREEN, 10, 14, gap=6)
    mo.vstack([mo.hstack([ys], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \Longrightarrow \quad \iint_D (xy - 2y) \, dxdy = \int_0^1 \left( \int_{-\sqrt{y}}^{\sqrt{y}} (xy - 2y) \, dx \right) dy$ $\displaystyle = \int_0^1 \left( \frac{x^2 y}{2} - 2xy \right) \bigg|_{x=-\sqrt{y}}^{x=\sqrt{y}} dy = \int_0^1 -4 \sqrt{y} \, y \, dy$ $\displaystyle = \int_0^1 -4 (y)^{3/2} \, dy = -4 \, \frac{2}{5} \, y^{5/2} \, \bigg|_{y=0}^{y=1} = -\frac{8}{5}$</span>

    $\leadsto$ &nbsp; $D$ is called **simple** if it is both $y$-simple and $x$-simple
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    If $D$ is $y$-simple or $x$-simple and $f : D \longrightarrow \mathbb{R}$ is continuous, then there exists $(x_0, y_0) \in D$ such that

    $$
    \iint_D f(x, y) \, dxdy = f(x_0, y_0) \underbrace{\iint_D dxdy}_{\footnotesize \text{area of } D}
    $$
    """,
        "Average of a function",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; $f(x_0, y_0)$ is the average of $f$ over $D$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ① &nbsp; $D$ is the triangle with corners $(0, 0)$, $(2, 0)$, $(1, 1)$

    a) &nbsp; Describe $D$ as a $y$-simple region.

    b) &nbsp; Describe $D$ as an $x$-simple region.

    c) &nbsp; Compute $\displaystyle \iint_D y \, dxdy$.

    ② &nbsp; Compute $\displaystyle \int_0^1 \left( \int_y^1 \frac{\sin(x)}{x} \, dx \right) dy$.
    """)
    return


if __name__ == "__main__":
    app.run()
