import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 22 • Surface integrals", css_file="bs101.css")



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
    header("Lecture 22", "Week 13", "Lecture 22 • Surface integrals")
    return


@app.cell(hide_code=True)
def _(Figure, arrow, math, mo, np):
    # ---- Helpers of this lecture ----------------------------------------
    from fractions import Fraction

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

    def plane(xlim, ylim, width, names=("$x$", "$y$")):
        """A sketch of a coordinate plane: the two axes as arrows, named at their tips."""
        fig, ax = sketch(xlim, ylim, width)
        arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.3, 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.3), "black", lw=0.9)
        beside(ax, (xlim[1] - 0.3, 0), 0, names[0], "black", 10, 12)
        beside(ax, (0, ylim[1] - 0.3), 90, names[1], "black", 10, 12)
        return fig, ax

    def pi_tex(k, n=12):
        """k pi / n as a TeX fraction in lowest terms, such as \\frac{\\pi}{4} or 2\\pi."""
        q = Fraction(k, n)
        if q == 0:
            return "0"
        top = r"\pi" if q.numerator == 1 else rf"{q.numerator}\pi"
        return top if q.denominator == 1 else rf"\frac{{{top}}}{{{q.denominator}}}"

    _d, _N = np.array([-0.55, 0.83, 0.0]), np.array([0.83, 0.55, 0.0])

    def curve(u):
        """A curve in R^3 with one loop, for the sketches of a curve C (pp. 1, 3 and 6); u runs over [-3.6, 3.6]. It lies
        near the vertical plane through (1.3, 1.5, 0) in the direction d, so that x, y and z all vary; it leaves that
        plane slowly in the direction N, so that the loop passes over itself and does not cross itself."""
        u = np.asarray(u, float)
        a, h = 0.7 * (0.5 * u - np.sin(u)), 1.5 - 0.9 * np.cos(u) + 0.08 * u
        e = 0.15 * u
        return 1.3 + a * _d[0] + e * _N[0], 1.5 + a * _d[1] + e * _N[1], h

    def curve_velocity(u):
        return 0.7 * (0.5 - math.cos(u)) * _d + 0.15 * _N + np.array([0.0, 0.0, 0.9 * math.sin(u) + 0.08])

    def curve_side(u, sign=1):
        """A unit vector at curve(u), perpendicular to the curve in its plane, on its upper side for sign = 1: names of
        points are put there, in space, so that they turn with the figure."""
        n = np.cross(_N, curve_velocity(u))
        n = n / np.linalg.norm(n)
        return sign * (n if n[2] >= 0 else -n)

    def span(*arrays, pad=0.0):
        """The box ((lo, hi), (lo, hi), (lo, hi)) of the points (x, y, z), with a margin `pad`."""
        return tuple((float(np.nanmin(a)) - pad, float(np.nanmax(a)) + pad) for a in arrays)

    def bracket(ax, lo, hi, color, vertical=False, h=0.09):
        """The interval [lo, hi] of the x axis (of the y axis if `vertical`), drawn over the axis between two square brackets."""

        def line(u, v):
            ax.plot(*((v, u) if vertical else (u, v)), color=color, lw=1.6, solid_capstyle="butt", zorder=4)

        line([lo, hi], [0, 0])
        for e, d in ((lo, 1), (hi, -1)):
            line([e + d * 0.6 * h, e, e, e + d * 0.6 * h], [h, h, -h, -h])

    def row(left, right):
        """A 2D figure beside a 3D one, as in lecture 16 (one above the other on narrow screens); both given as HTML."""
        return mo.Html(
            '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
            f'<div style="flex: 0 1 280px; min-width: 240px; max-width: 300px;">{left}</div>'
            f'<div style="flex: 1 1 440px; min-width: 300px;">{right}</div></div>'
        )

    return beside, bracket, curve, curve_side, curve_velocity, pi_tex, plane, row, sketch, span


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
    // a 2D output beside the figure (turntable(..., beside=...)) travels hidden with the scene; it is copied into the place
    // data-bs2d of the frame's row, and when the slider moves only its attributes change, so it is redrawn in place
    function beside() {
      const h = find(), dst = P.querySelector('[data-bs2d="' + window.frameElement.dataset.bs3d + '"]');
      const a = h && h.firstElementChild;
      if (!dst || !a) return;
      const b = dst.firstElementChild;
      if (b && b.tagName === a.tagName) { for (const n of a.getAttributeNames()) if (b.getAttribute(n) !== a.getAttribute(n)) b.setAttribute(n, a.getAttribute(n)); }
      else dst.replaceChildren(a.cloneNode(true));
    }
    (function start() { const h = find(); if (h) { beside(); main(h.dataset.scene); } else setTimeout(start, 50); })();
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
        beside();
        const h = find();
        if (!h || h.dataset.scene === shown) return;
        shown = h.dataset.scene;
        S = JSON.parse(shown);
        build();
        if (window.katex) window.typeset(); else { fit(); draw(); }
      }).observe(box.querySelector("[data-scene]") ? box : P.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["data-scene", "data-data"] });
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

    def turntable(az, el, alt, panels, legend=(), height=360, width=None, cols=1, key=None, shared=True, bias=0.03, apart=False, beside=None):
        """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
        from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
        at most `width` wide, with a legend box beside them (below them on narrow screens). `key` names the view
        so that it survives a redraw; with `shared`, all panels have one scale.
        legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area".
        apart: only the scene, for a figure with a slider, whose frame, frame(key, height), is shown by the next cell,
        so that moving the slider redraws the figure without rebuilding its frame.
        beside: with apart, a 2D output that the row of the next cell shows beside the frame, in its element data-bs2d="KEY"."""
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
            return mo.Html(f'<div hidden data-bs3d="{_html.escape(key)}" data-scene="{data}">{"" if beside is None else mo.as_html(beside).text}</div>')
        return mo.Html(f'<div class="bs3d">{_frame(height)}<div hidden data-scene="{data}"></div></div>')

    def _frame(height, key=""):
        return f'<iframe srcdoc="{_html.escape(_PAGE)}" data-bs3d="{_html.escape(key)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>'

    def frame(key, height=360):
        """The frame of the figure turntable(..., key=key, height=height, apart=True) of the cell above."""
        return mo.Html(f'<div class="bs3d">{_frame(height, key)}</div>')

    return frame, panel, patch, sheet, turntable


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Green's theorem

    $D \subseteq \mathbb{R}^2$ simple, &nbsp; $\vec{C} = \mathrm{Bd}(D)$ with positive orientation, &nbsp; and &nbsp; $\vec{F} = \begin{bmatrix} P \\ Q \end{bmatrix}$ &nbsp; $C^1$-smooth

    $$
    \Longrightarrow \quad \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \iint_D \bigg( \underbrace{\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}}_{\footnotesize \text{scalar curl}} \bigg) \, dxdy
    $$

    $\leadsto$ &nbsp; can we generalize this to $\mathbb{R}^3$?

    - Stokes &nbsp; $\longrightarrow$ &nbsp; curved surfaces and their boundary curves
    - Gauss &nbsp; $\longrightarrow$ &nbsp; bounded 3d regions and their boundary surfaces
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **In this lecture:** Integration over surfaces in $\mathbb{R}^3$

    **References:** MT 7.3, 7.4, 7.5, 7.6

    ## V.1 &nbsp; Surface integrals

    **Recall:** a path (or parameterized curve) in $\mathbb{R}^3$ is a function

    $$
    \gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3, \quad t \longmapsto \begin{bmatrix} x(t) \\ y(t) \\ z(t) \end{bmatrix}
    $$

    $C = \mathrm{Im}(\gamma) = \gamma(I) \subset \mathbb{R}^3$ is a curve in $\mathbb{R}^3$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, RED, arrow, beside, bracket, curve, curve_side, mo, np, panel, plane, row, sheet, sketch, turntable):
    # a path and a parameterized surface (p. 1), each as a 2D domain beside its 3D image (the layout of lecture 16):
    # the interval I with a point t (blue) and the curve C = Im(gamma) (red) with gamma(t) (blue), drawn as the curves of
    # lecture 19; the region D with a point (s, t) (blue) and the surface S = Im(Phi) with Phi(s, t) (black), drawn as
    # the graph of lecture 11. Curve and surface are chosen for the drawing only
    _fi, _ai = sketch((-0.5, 3.6), (-0.6, 0.6), 2.8)
    arrow(_ai, (-0.4, 0), (3.5, 0), "black", lw=0.9)
    bracket(_ai, 0.6, 2.6, "black")
    _ai.plot(1.5, 0, "o", color=BLUE, ms=4.5, zorder=6)
    beside(_ai, (1.5, 0.09), 90, "$t$", "black", 8, 12)
    beside(_ai, (1.6, -0.09), -90, "$I$", "black", 10, 14)
    _u0 = 2.4
    _pt = np.array(curve(_u0))
    _curve = turntable(
        30,
        20,
        "a curve C = Im(gamma) in R^3 with a loop, and its point gamma(t)",
        [
            panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), RED, 1.8)],
                points=[(tuple(_pt), BLUE, 4.0)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(tuple(_pt + 0.4 * curve_side(_u0)), r"\gamma(t)", "#000000", 0, 0), (tuple(np.array(curve(3.6))), r"C = \mathrm{Im}(\gamma)", RED, 0, 8)],
            )
        ],
        height=400,
        key="L22-curve",
    )
    _fd, _ad = plane((-0.5, 3.4), (-0.4, 2.8), 2.8, names=("$s$", "$t$"))
    _s = np.linspace(0.5, 2.6, 100)
    _lo, _hi = 0.5 + 0.12 * np.sin(4 * (_s - 0.5)), 2.1 + 0.12 * np.sin(3.5 * (_s - 0.5) + 1)
    _ad.fill_between(_s, _lo, _hi, color=LIGHT, lw=0, zorder=0)
    for _y in (_lo, _hi):
        _ad.plot(_s, _y, color=BLUE, lw=1.8)
    for _i in (0, -1):
        _ad.plot([_s[_i], _s[_i]], [_lo[_i], _hi[_i]], color=BLUE, lw=1.8)
    _ad.text(2.3, 1.85, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _ad.plot(1.3, 1.2, "o", color=BLUE, ms=4.5, zorder=6)
    _ad.text(1.4, 1.2, "$(s, t)$", color="black", fontsize=13, ha="left", va="center")

    def _h(x, y):
        return 2.4 - 0.2 * ((x - 1.9) ** 2 + (y - 1.7) ** 2)

    _x1, _x2 = np.meshgrid(np.linspace(0.5, 3.1, 25), np.linspace(0.5, 3.1, 25), indexing="ij")
    _w = np.linspace(0.5, 3.1, 25)
    _rim = [(_c + 0 * _w, _w, _h(_c + 0 * _w, _w), BLUE, 1.2) for _c in (0.5, 3.1)] + [(_w, _c + 0 * _w, _h(_w, _c + 0 * _w), BLUE, 1.2) for _c in (0.5, 3.1)]
    _q = (2.4, 1.3, float(_h(2.4, 1.3)))
    _surface = turntable(
        28,
        32,
        "a surface S = Im(Phi) in R^3, the graph of a function over a rectangle, and its point Phi(s, t)",
        [
            panel(
                1.0,
                surfaces=[sheet(_x1, _x2, _h(_x1, _x2), wire=[(0, 4, BLUE, 0.5), (1, 4, BLUE, 0.5)])],
                lines=_rim,
                points=[(_q, "#000000")],
                axes=[((0, 0, 0), (3.6, 0, 0), "x", -150), ((0, 0, 0), (0, 3.6, 0), "y", -20), ((0, 0, 0), (0, 0, 3.6), "z", 90)],
                texts=[(_q, r"\Phi(s, t)", "#000000", -60, 6), ((3.1, 0.5, float(_h(3.1, 0.5))), r"S = \mathrm{Im}(\Phi)", BLUE, 200, 8)],
            )
        ],
        height=400,
        key="L22-surface",
    )
    mo.vstack([row(mo.as_html(_fi).text, _curve.text), row(mo.as_html(_fd).text, _surface.text)])
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    A **parameterized surface** in $\mathbb{R}^3$ is a function

    $$
    \Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3, \quad (s, t) \longmapsto \begin{bmatrix} x(s, t) \\ y(s, t) \\ z(s, t) \end{bmatrix}
    $$

    $S = \mathrm{Im}(\Phi) = \Phi(D) \subset \mathbb{R}^3$ is a **surface** in $\mathbb{R}^3$
    """,
        "Parameterized surface",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\Phi(s, t) = \begin{bmatrix} 2\cos(t) \\ 2\sin(t) \\ s \end{bmatrix}$, &nbsp; $(s, t) \in [-1, 1] \times [0, 2\pi]$

    <span class="chain">$\displaystyle \Longrightarrow \quad \mathrm{Im}(\Phi) = \left\{ (x, y, z) \mid x^2 + y^2 = 4, \ -1 \leq z \leq 1 \right\}$ $\displaystyle = \text{cylinder of radius } 2 \text{ and height } 2$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    cs = mo.ui.slider(-1, 1, 0.25, value=0, label="$s$", show_value=True)
    ct = mo.ui.slider(0, 24, 1, value=3, label=r"$t \;\; (\times \frac{\pi}{12})$", show_value=True)
    return cs, ct


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, beside, cs, ct, mo, np, panel, pi_tex, plane, sheet, turntable):
    # the cylinder (p. 2), in the layout of lecture 16: the segment s = s0 of D (red) is mapped to the circle at height s0,
    # the segment t = t0 (orange) to the vertical segment at the angle t0; s0 and t0 move with the sliders (in the notes
    # s = 0 and t = pi/4). D is drawn with t / pi on its vertical axis; it stands beside the cylinder, in the row of the
    # next cell. The cylinder as the surfaces of lecture 16: light wire, the curves on it at width 2.4
    _s0, _k = float(cs.value), int(ct.value)
    _t0 = _k * np.pi / 12
    _fig, _ax = plane((-1.8, 2.6), (-0.55, 2.75), 2.8, names=("$s$", "$t$"))
    _ax.fill([-1, 1, 1, -1], [0, 0, 2, 2], color=LIGHT, lw=0, zorder=0)
    _ax.plot([-1, 1, 1, -1, -1], [0, 0, 2, 2, 0], color=BLUE, lw=1.8)
    _ax.plot([_s0, _s0], [0, 2], color=RED, lw=1.8, zorder=3)
    _ax.plot([-1, 1], [_k / 12, _k / 12], color=ORANGE, lw=1.8, zorder=3)
    for _e in (-1, 1):
        beside(_ax, (_e, 0), -90, f"${_e}$", "black", 14, 14, gap=6)
    beside(_ax, (-1, 2), 180, r"$2\pi$", "black", 20, 14)
    beside(_ax, (_s0, 2), 25, f"$s = {_s0:g}$", RED, 50, 14)
    beside(_ax, (1, _k / 12), 0, f"$t = {pi_tex(_k)}$", ORANGE, 44, 20)
    _ax.text(0.75, 1.75, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _s, _t = np.meshgrid(np.linspace(-1, 1, 9), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _scene = turntable(
        30,
        22,
        "the cylinder of radius 2 and height 2, with the circle at height s and the vertical segment at the angle t",
        [
            panel(
                1.0,
                surfaces=[sheet(2 * np.cos(_t), 2 * np.sin(_t), _s, wire=[(0, 2, BLUE, 0.4), (1, 8, BLUE, 0.4)], alpha=0.85)],
                lines=[(2 * np.cos(_T), 2 * np.sin(_T), _s0 + 0 * _T, RED, 2.4), ([2 * np.cos(_t0)] * 2, [2 * np.sin(_t0)] * 2, [-1, 1], ORANGE, 2.4)],
                axes=[((0, 0, 0), (3.3, 0, 0), "x", -150), ((0, 0, 0), (0, 3.3, 0), "y", -20), ((0, 0, 0), (0, 0, 2.3), "z", 90)],
                texts=[((2 * np.cos(1.9), 2 * np.sin(1.9), 1.0), "S", BLUE, 90, 6)],
                box=((-2.0, 3.3), (-2.0, 3.3), (-1.0, 2.3)),
            )
        ],
        height=420,
        key="L22-cylinder",
        apart=True,
        beside=_fig,
    )
    mo.vstack([mo.hstack([cs, ct], justify="start", gap=2), _scene])
    return


@app.cell(hide_code=True)
def _(frame, row):
    row('<div data-bs2d="L22-cylinder"></div>', frame("L22-cylinder", 420).text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \Phi(s, t) = \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix}, \quad (s, t) \in [0, \pi] \times [0, 2\pi]
    $$

    <span class="chain">$\displaystyle \Longrightarrow \quad \mathrm{Im}(\Phi) = \left\{ (x, y, z) \mid x^2 + y^2 + z^2 = 4 \right\}$ $\displaystyle = \text{sphere of radius } 2 \text{ around } \vec{0}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ss = mo.ui.slider(0, 12, 1, value=6, label=r"$s \;\; (\times \frac{\pi}{12})$", show_value=True)
    st = mo.ui.slider(0, 24, 1, value=4, label=r"$t \;\; (\times \frac{\pi}{12})$", show_value=True)
    return ss, st


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, beside, mo, np, panel, pi_tex, plane, sheet, ss, st, turntable):
    # the sphere (p. 2), in the layout of lecture 16: the segment s = s0 of D (red) is mapped to a circle of latitude (the
    # equator for s0 = pi/2), the segment t = t0 (orange) to a meridian; s0 and t0 move with the sliders (in the notes
    # s = pi/2 and t = pi/3). D is drawn with 1.5 s / pi and t / pi on its axes; it stands beside the sphere, in the row of
    # the next cell. The sphere as the surfaces of lecture 16: light wire, the curves on it at width 2.4
    _j, _k = int(ss.value), int(st.value)
    _s0, _t0 = _j * np.pi / 12, _k * np.pi / 12
    _fig, _ax = plane((-0.7, 2.9), (-0.55, 2.75), 2.8, names=("$s$", "$t$"))
    _ax.fill([0, 1.5, 1.5, 0], [0, 0, 2, 2], color=LIGHT, lw=0, zorder=0)
    _ax.plot([0, 1.5, 1.5, 0, 0], [0, 0, 2, 2, 0], color=BLUE, lw=1.8)
    _ax.plot([1.5 * _j / 12] * 2, [0, 2], color=RED, lw=1.8, zorder=3)
    _ax.plot([0, 1.5], [_k / 12, _k / 12], color=ORANGE, lw=1.8, zorder=3)
    beside(_ax, (1.5, 0), -90, r"$\pi$", "black", 12, 14, gap=6)
    beside(_ax, (0, 2), 180, r"$2\pi$", "black", 20, 14)
    beside(_ax, (1.5 * _j / 12, 2), 25, f"$s = {pi_tex(_j)}$", RED, 44, 20)
    beside(_ax, (1.5, _k / 12), 0, f"$t = {pi_tex(_k)}$", ORANGE, 44, 20)
    _ax.text(1.3, 1.8, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _S = np.linspace(0, np.pi, 61)
    _scene = turntable(
        30,
        22,
        "the sphere of radius 2 around the origin, with the circle of latitude s and the meridian at the angle t",
        [
            panel(
                1.0,
                surfaces=[sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, BLUE, 0.4), (1, 8, BLUE, 0.4)], alpha=0.85)],
                lines=[
                    (2 * np.sin(_s0) * np.cos(_T), 2 * np.sin(_s0) * np.sin(_T), 2 * np.cos(_s0) + 0 * _T, RED, 2.4),
                    (2 * np.sin(_S) * np.cos(_t0), 2 * np.sin(_S) * np.sin(_t0), 2 * np.cos(_S), ORANGE, 2.4),
                ],
                axes=[((0, 0, 0), (3.3, 0, 0), "x", -150), ((0, 0, 0), (0, 3.3, 0), "y", -20), ((0, 0, 0), (0, 0, 3.3), "z", 90)],
                texts=[((2 * np.cos(1.9) * np.sin(0.5), 2 * np.sin(1.9) * np.sin(0.5), 2 * np.cos(0.5)), "S", BLUE, 120, 6)],
                box=((-2.0, 3.3), (-2.0, 3.3), (-2.0, 3.3)),
            )
        ],
        height=420,
        key="L22-sphere",
        apart=True,
        beside=_fig,
    )
    mo.vstack([mo.hstack([ss, st], justify="start", gap=2), _scene])
    return


@app.cell(hide_code=True)
def _(frame, row):
    row('<div data-bs2d="L22-sphere"></div>', frame("L22-sphere", 420).text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Given $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$,

    $$
    \Phi(s, t) = \begin{bmatrix} s \\ t \\ f(s, t) \end{bmatrix}, \quad (s, t) \in D \qquad \Longrightarrow \qquad \mathrm{Im}(\Phi) = \mathrm{graph}(f) \subset \mathbb{R}^3
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, LIGHT, mo, np, panel, plane, row, sheet, turntable):
    # the graph of a function f over a rectangle D (p. 2), parameterized by Phi(s, t) = (s, t, f(s, t)): D beside the
    # graph, in the layout of lecture 16; the graph drawn as lecture 11's, with dashed guides from its corners down to D.
    # f is chosen for the drawing only
    _a, _b, _c, _d = 0.6, 3.0, 0.6, 3.0

    def _f(x, y):
        return 2.4 - 0.2 * ((x - 1.9) ** 2 + (y - 1.7) ** 2)

    _fig, _ax = plane((-0.5, 3.8), (-0.5, 3.6), 2.8, names=("$s$", "$t$"))
    _ax.fill([_a, _b, _b, _a], [_c, _c, _d, _d], color=LIGHT, lw=0, zorder=0)
    _ax.plot([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], color=BLUE, lw=1.8)
    _ax.text(_b - 0.25, _d - 0.25, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _x1, _x2 = np.meshgrid(np.linspace(_a, _b, 25), np.linspace(_c, _d, 25), indexing="ij")
    _w = np.linspace(_a, _b, 25)
    _rim = [(_q + 0 * _w, _w, _f(_q + 0 * _w, _w), BLUE, 1.2) for _q in (_a, _b)] + [(_w, _q + 0 * _w, _f(_w, _q + 0 * _w), BLUE, 1.2) for _q in (_c, _d)]
    _rim += [([_a, _b, _b, _a, _a], [_c, _c, _d, _d, _c], [0, 0, 0, 0, 0], BLUE, 1.2)]
    _guides = [([_p, _p], [_q, _q], [0, float(_f(_p, _q))], GREY, 1.0, [4, 3]) for _p in (_a, _b) for _q in (_c, _d)]
    _scene = turntable(
        28,
        32,
        "the graph of f over the rectangle D",
        [
            panel(
                1.0,
                surfaces=[sheet(_x1, _x2, 0 * _x1, flat=LIGHT, alpha=0.6), sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, BLUE, 0.5), (1, 4, BLUE, 0.5)])],
                lines=_rim + _guides,
                axes=[((0, 0, 0), (3.6, 0, 0), "x", -150), ((0, 0, 0), (0, 3.6, 0), "y", -20), ((0, 0, 0), (0, 0, 3.6), "z", 90)],
                texts=[((_b, _c, 0), "D", BLUE, -60, 6), ((_b, _c, float(_f(_b, _c))), r"z = f(x, y)", BLUE, 200, 8)],
            )
        ],
        height=420,
        key="L22-graph",
    )
    row(mo.as_html(_fig).text, _scene.text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ is differentiable at $t$

    $\Longrightarrow$ &nbsp; $\gamma'(t) = \begin{bmatrix} x'(t) \\ y'(t) \\ z'(t) \end{bmatrix} \in \mathbb{R}^3$ &nbsp; is the velocity vector of $\gamma$ at $\gamma(t)$

    If $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ is differentiable at $(s, t)$

    $$
    \Longrightarrow \quad D\Phi(s, t) = \begin{bmatrix} \dfrac{\partial x}{\partial s}(s, t) & \dfrac{\partial x}{\partial t}(s, t) \\[8pt] \dfrac{\partial y}{\partial s}(s, t) & \dfrac{\partial y}{\partial t}(s, t) \\[8pt] \dfrac{\partial z}{\partial s}(s, t) & \dfrac{\partial z}{\partial t}(s, t) \end{bmatrix} \in \mathrm{Mat}(3 \times 2)
    $$

    $$
    \Longrightarrow \quad \left\{ \begin{aligned} \Phi_s(s, t) &= \frac{\partial \Phi}{\partial s}(s, t) = \begin{bmatrix} \dfrac{\partial x}{\partial s}(s, t) \\[8pt] \dfrac{\partial y}{\partial s}(s, t) \\[8pt] \dfrac{\partial z}{\partial s}(s, t) \end{bmatrix} \in \mathbb{R}^3 \\[12pt] \Phi_t(s, t) &= \frac{\partial \Phi}{\partial t}(s, t) = \begin{bmatrix} \dfrac{\partial x}{\partial t}(s, t) \\[8pt] \dfrac{\partial y}{\partial t}(s, t) \\[8pt] \dfrac{\partial z}{\partial t}(s, t) \end{bmatrix} \in \mathbb{R}^3 \end{aligned} \right.
    $$

    are the tangent vectors of $\Phi$ at $\Phi(s, t)$

    $\Longrightarrow$ &nbsp; $\Phi_s(s, t) \times \Phi_t(s, t)$ is normal to $\Phi_s(s, t)$ and $\Phi_t(s, t)$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, ORANGE, RED, curve, curve_side, curve_velocity, mo, np, panel, patch, sheet, turntable):
    # tangent line and tangent plane (p. 3). Above, as the curves of lecture 19: the curve C (red), the point gamma(t) and
    # its velocity gamma'(t) (blue), the tangent line (green). Below, as lecture 11's tangent plane: a graph S (chosen for
    # the drawing only) with its tangent plane at the point Phi(s, t) (black), spanned by Phi_s and Phi_t (orange), the
    # combination a Phi_s + b Phi_t (green) in it, the normal Phi_s x Phi_t (red) with a right-angle mark, dashed guides
    # down to the base point
    _u0 = 2.4
    _p = np.array(curve(_u0))
    _v = 0.8 * curve_velocity(_u0)
    _line = np.array([_p - 1.3 * _v, _p + 1.6 * _v]).T
    _left = turntable(
        30,
        20,
        "the curve C with the point gamma(t), its velocity vector gamma'(t) and the tangent line through gamma(t)",
        [
            panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), RED, 1.8), (*_line, GREEN, 1.2)],
                points=[(tuple(_p), BLUE, 4.0)],
                arrows=[(_p, _p + _v, BLUE, 1.6)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(tuple(_p - 0.4 * curve_side(_u0)), r"\gamma(t)", "#000000", 0, 0), (tuple(_p + _v), r"\gamma'(t)", BLUE, 120, 8), (tuple(np.array(curve(-3.6))), "C", RED, 180, 6)],
            )
        ],
        height=340,
        key="L22-tangent-line",
    )

    def _f(x1, x2):
        return 2.4 - 0.2 * ((x1 - 1.9) ** 2 + (x2 - 1.7) ** 2)

    _a = (1.5, 1.1)
    _d1, _d2 = -0.4 * (_a[0] - 1.9), -0.4 * (_a[1] - 1.7)
    _fa = float(_f(*_a))
    _lo, _hi, _k, _vv = 0.5, 3.1, 1.4, 1.3
    _x1, _x2 = np.meshgrid(np.linspace(_lo, _hi, 25), np.linspace(_lo, _hi, 25), indexing="ij")
    _w = np.linspace(_lo, _hi, 25)
    _rim = [(_c + 0 * _w, _w) for _c in (_lo, _hi)] + [(_w, _c + 0 * _w) for _c in (_lo, _hi)]

    def _g(x1, x2):
        return _fa + _d1 * (x1 - _a[0]) + _d2 * (x2 - _a[1])

    _corners = [(_a[0] + _k * _i, _a[1] + _k * _j) for _i, _j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    _s = np.linspace(0, 1, 30)
    _edges = [(_p0[0] + _s * (_q0[0] - _p0[0]), _p0[1] + _s * (_q0[1] - _p0[1])) for _p0, _q0 in zip(_corners, _corners[1:] + _corners[:1])]
    _P = np.array([_a[0], _a[1], _fa])
    _fs, _ft = np.array([_vv, 0, _vv * _d1]), np.array([0, _vv, _vv * _d2])
    _n = np.array([-_d1, -_d2, 1.0])
    _cb = 0.55 * _fs + 0.9 * _ft
    _e1, _e2 = 0.14 * _n / np.linalg.norm(_n), 0.14 * _fs / np.linalg.norm(_fs)
    _mark = np.array([_P + _e1, _P + _e1 + _e2, _P + _e2]).T
    _right = turntable(
        28,
        32,
        "a surface S with its tangent plane at the point Phi(s, t), the two tangent vectors spanning the plane, a combination of them and the normal vector",
        [
            panel(
                1.0,
                surfaces=[sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, BLUE, 0.5), (1, 4, BLUE, 0.5)]), patch([(_c[0], _c[1], _g(*_c)) for _c in _corners], GREEN, 0.18)],
                lines=[(_c1, _c2, _f(_c1, _c2), BLUE, 1.2) for _c1, _c2 in _rim]
                + [(_c1, _c2, _g(_c1, _c2), GREEN, 1.2) for _c1, _c2 in _edges]
                + [
                    (_a[0] + 0 * _s, _a[1] * _s, 0 * _s, GREY, 1.0, [4, 3]),
                    (_a[0] * _s, _a[1] + 0 * _s, 0 * _s, GREY, 1.0, [4, 3]),
                    (_a[0] + 0 * _s, _a[1] + 0 * _s, _fa * _s, GREY, 1.0, [4, 3]),
                    (*_mark, RED, 1.0),
                ],
                points=[(tuple(_P), "#000000"), ((_a[0], _a[1], 0), GREY, 3.4)],
                arrows=[(_P, _P + _fs, ORANGE), (_P, _P + _ft, ORANGE), (_P, _P + _cb, GREEN), (_P, _P + _n, RED)],
                axes=[((0, 0, 0), (3.6, 0, 0), "x", -150), ((0, 0, 0), (0, 3.6, 0), "y", -20), ((0, 0, 0), (0, 0, 3.6), "z", 90)],
                texts=[
                    ((_hi, _lo, _f(_hi, _lo)), "S", BLUE, 200, 8),
                    (tuple(_P), r"\Phi(s, t)", "#000000", 190, 10),
                    (tuple(_P + _n), r"\Phi_s(s, t) \times \Phi_t(s, t)", RED, 0, 6),
                    (tuple(_P + _fs), r"\Phi_s(s, t)", ORANGE, -150, 6),
                    (tuple(_P + _ft), r"\Phi_t(s, t)", ORANGE, -20, 6),
                    (tuple(_P + _cb), r"a \, \Phi_s(s, t) + b \, \Phi_t(s, t)", GREEN, -60, 8),
                ],
            )
        ],
        height=460,
        key="L22-tangent-plane",
    )
    mo.vstack([_left, _right])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The line through $\gamma(t)$ in the direction of $\gamma'(t)$ is the **tangent line** to $C$ at $\gamma(t)$ (for $\gamma'(t) \neq \vec{0}$)

    The plane through $\Phi(s, t)$ in the direction of $\Phi_s(s, t)$ and $\Phi_t(s, t)$ is the **tangent plane** to $S$ at $\Phi(s, t)$ (for $\Phi_s(s, t) \times \Phi_t(s, t) \neq \vec{0}$), and $\Phi_s(s, t) \times \Phi_t(s, t)$ is normal to the tangent plane
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\Phi(s, t) = \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix}$, &nbsp; $(s, t) \in [0, \pi] \times [0, 2\pi]$

    $$
    \Phi_s(s, t) = \begin{bmatrix} 2\cos(s)\cos(t) \\ 2\cos(s)\sin(t) \\ -2\sin(s) \end{bmatrix}, \qquad \Phi_t(s, t) = \begin{bmatrix} -2\sin(s)\sin(t) \\ 2\sin(s)\cos(t) \\ 0 \end{bmatrix}
    $$

    $$
    \leadsto \quad \Phi_s(s, t) \times \Phi_t(s, t) = 2\sin(s) \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix} = 2\sin(s) \, \Phi(s, t)
    $$

    At $s = \dfrac{\pi}{2}$, $t = \dfrac{\pi}{2}$ &nbsp; $\leadsto$ &nbsp; $\Phi\left(\dfrac{\pi}{2}, \dfrac{\pi}{2}\right) = \begin{bmatrix} 0 \\ 2 \\ 0 \end{bmatrix} \in S$

    $$
    \Phi_s\left(\frac{\pi}{2}, \frac{\pi}{2}\right) = \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix}, \qquad \Phi_t\left(\frac{\pi}{2}, \frac{\pi}{2}\right) = \begin{bmatrix} -2 \\ 0 \\ 0 \end{bmatrix}
    $$

    $\Longrightarrow$ &nbsp; the tangent plane to $S$ at the point $(0, 2, 0)$ is

    <span class="chain">$\displaystyle P = \left\{ \begin{bmatrix} 0 \\ 2 \\ 0 \end{bmatrix} + a \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix} + b \begin{bmatrix} -2 \\ 0 \\ 0 \end{bmatrix} \;\middle|\; a, b \in \mathbb{R} \right\}$ $\displaystyle = \left\{ \begin{bmatrix} x \\ y \\ z \end{bmatrix} \;\middle|\; y = 2, \ x, z \in \mathbb{R} \right\}$</span>

    $\leadsto$ &nbsp; normal vectors to $P$ at $(0, 2, 0)$ are proportional to

    $$
    \vec{n} = \begin{bmatrix} 0 \\ 0 \\ -2 \end{bmatrix} \times \begin{bmatrix} -2 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 4 \\ 0 \end{bmatrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, ORANGE, RED, np, panel, patch, sheet, turntable):
    # the sphere and its tangent plane y = 2 at (0, 2, 0) = Phi(pi/2, pi/2) (p. 4), drawn as lecture 11's tangent plane:
    # the plane green (a patch with its edges), Phi_s and Phi_t there (orange), their cross product (red), the point
    # black; the equator and the meridian through the point (grey); the sphere as the surfaces of lecture 16
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _k = 1.8
    _corners = [(_i * _k, 2.0, _j * _k) for _i, _j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    _edges = [np.array([_a, _b]).T for _a, _b in zip(_corners, _corners[1:] + _corners[:1])]
    _P = np.array([0.0, 2.0, 0.0])
    _scene = turntable(
        30,
        20,
        "the sphere of radius 2 with its tangent plane y = 2 at the point (0, 2, 0), the two tangent vectors there and their cross product",
        [
            panel(
                1.0,
                surfaces=[sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, BLUE, 0.4), (1, 8, BLUE, 0.4)], alpha=0.85), patch(_corners, GREEN, 0.18)],
                lines=[(2 * np.cos(_T), 2 * np.sin(_T), 0 * _T, GREY, 1.0), (0 * _T, 2 * np.sin(_T), 2 * np.cos(_T), GREY, 1.0)] + [(*_ed, GREEN, 1.2) for _ed in _edges],
                points=[(tuple(_P), "#000000")],
                arrows=[(_P, _P + [0, 0, -2], ORANGE), (_P, _P + [-2, 0, 0], ORANGE), (_P, _P + [0, 4, 0], RED)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", -90), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[
                    ((0, 2, -2), r"\Phi_s\left(\frac{\pi}{2}, \frac{\pi}{2}\right)", ORANGE, -90, 6),
                    ((-2, 2, 0), r"\Phi_t\left(\frac{\pi}{2}, \frac{\pi}{2}\right)", ORANGE, 120, 6),
                    ((0, 6, 0), r"\Phi_s\left(\frac{\pi}{2}, \frac{\pi}{2}\right) \times \Phi_t\left(\frac{\pi}{2}, \frac{\pi}{2}\right)", RED, 90, 8),
                    ((2 * np.cos(2.2) * np.sin(0.6), 2 * np.sin(2.2) * np.sin(0.6), 2 * np.cos(0.6)), "S", BLUE, 150, 6),
                ],
            )
        ],
        height=400,
        key="L22-sphere-plane",
    )
    _scene
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** &nbsp; At $s = 0$ and $s = \pi$, &nbsp; $2\sin(s) \, \Phi(s, t) = \vec{0}$

    $\Longrightarrow$ &nbsp; we cannot describe the tangent plane to $S$ at $\underbrace{(0, 0, 2) \text{ and } (0, 0, -2)}_{\footnotesize \text{not regular points for } \Phi}$ using $\Phi$…

    **Remark.** &nbsp; To be precise, $\Phi_s(s, t)$ and $\Phi_t(s, t)$ are not really well-defined along $s = 0, \pi$ and $t = 0, 2\pi$…

    $\leadsto$ &nbsp; but we can extend $\Phi_s(s, t) \times \Phi_t(s, t)$ continuously to the boundary of $[0, \pi] \times [0, 2\pi]$
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    $\Phi(s, t) \in S$ is called a **regular point** for $\Phi$ if

    $$
    \Phi_s(s, t) \times \Phi_t(s, t) \neq \vec{0}
    $$
    """,
        "Regular point",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ differentiable

    $\Longrightarrow$ &nbsp; $\Phi(s, t) = \begin{bmatrix} s \\ t \\ f(s, t) \end{bmatrix}$ is a parameterization of $\mathrm{graph}(f)$

    <span class="chain">$\displaystyle \Longrightarrow \quad \Phi_s(s, t) \times \Phi_t(s, t) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ 1 & 0 & \dfrac{\partial f}{\partial s}(s, t) \\[1.2ex] 0 & 1 & \dfrac{\partial f}{\partial t}(s, t) \end{bmatrix}$ $\displaystyle = \begin{bmatrix} -\dfrac{\partial f}{\partial s}(s, t) \\[1.2ex] -\dfrac{\partial f}{\partial t}(s, t) \\[1.2ex] 1 \end{bmatrix} \neq \vec{0} \quad (\text{since } 1 \neq 0)$</span>

    $\Longrightarrow$ &nbsp; all points of $S = \mathrm{graph}(f)$ are regular for $\Phi(s, t) = \begin{bmatrix} s \\ t \\ f(s, t) \end{bmatrix}$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Recall:**

    $$
    \int_C f \, ds = \int_I f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt
    $$

    <span class="chain">$\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_I \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt$ $\displaystyle \qquad \vec{C} \ \longleftarrow \ \text{oriented curve}$</span>

    $$
    \underbrace{ds}_{\footnotesize \text{infinitesimal length element}} = \lVert \gamma'(t) \rVert \, dt = \lim_{\Delta t \to 0} \left\lVert \frac{\gamma(t + \Delta t) - \gamma(t)}{\Delta t} \right\rVert dt
    $$

    $$
    \underbrace{d\vec{s}}_{\footnotesize \text{infinitesimal line element}} = \gamma'(t) \, dt = \lim_{\Delta t \to 0} \frac{\gamma(t + \Delta t) - \gamma(t)}{\Delta t} \, dt
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    dt = mo.ui.slider(0.1, 1.5, 0.1, value=1.2, label=r"$\Delta t$", show_value=True)
    return (dt,)


@app.cell(hide_code=True)
def _(BLUE, RED, curve, curve_side, dt, mo, np, panel, turntable):
    # the curve C (red) with the points gamma(t) and gamma(t + Delta t) (blue) and the vector from one to the other (blue,
    # as the velocity of lecture 19) (p. 6); Delta t moves with the slider, and the names sit in space on either side of
    # the curve, so they move with their points
    _u0, _h = 2.0, float(dt.value)
    _p, _q = np.array(curve(_u0)), np.array(curve(_u0 + _h))
    _scene = turntable(
        30,
        20,
        "the curve C with the points gamma(t) and gamma(t + Delta t) and the vector from the first to the second",
        [
            panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), RED, 1.8)],
                points=[(tuple(_p), BLUE, 4.0), (tuple(_q), BLUE, 4.0)],
                arrows=[(_p, _q, BLUE, 1.6)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[(tuple(_p + 0.4 * curve_side(_u0, -1)), r"\gamma(t)", "#000000", 0, 0), (tuple(_q + 0.45 * curve_side(_u0 + _h)), r"\gamma(t + \Delta t)", "#000000", 0, 0)],
                box=((0, 3.0), (0, 3.0), (0, 3.0)),
            )
        ],
        height=340,
        key="L22-secant",
        apart=True,
    )
    mo.vstack([mo.hstack([dt], justify="start"), _scene])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("L22-secant", 340)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Similarly,

    <span class="chain">$\displaystyle dA = \lim_{\substack{\Delta s \to 0 \\ \Delta t \to 0}} \left\lVert \frac{\big(\Phi(s + \Delta s, t) - \Phi(s, t)\big) \times \big(\Phi(s, t + \Delta t) - \Phi(s, t)\big)}{\Delta s \, \Delta t} \right\rVert ds dt$ $\displaystyle = \underbrace{\lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, ds dt}_{\footnotesize \text{infinitesimal area element}}$</span>

    <span class="chain">$\displaystyle d\vec{A} = \lim_{\substack{\Delta s \to 0 \\ \Delta t \to 0}} \frac{\big(\Phi(s + \Delta s, t) - \Phi(s, t)\big) \times \big(\Phi(s, t + \Delta t) - \Phi(s, t)\big)}{\Delta s \, \Delta t} \, ds dt$ $\displaystyle = \underbrace{\Phi_s(s, t) \times \Phi_t(s, t) \, ds dt}_{\footnotesize \text{infinitesimal surface element}}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    dd = mo.ui.slider(0.3, 1.4, 0.1, value=1.0, label=r"$\Delta s = \Delta t$", show_value=True)
    return (dd,)


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, arrow, beside, dd, mo, np, panel, plane, sheet, turntable):
    # a small square of the (s, t)-plane beside its image patch on a graph S (chosen for the drawing only, drawn as
    # lecture 11's), in the layout of lecture 16 (p. 6): the sides from (s, t) are mapped to (nearly) the vectors u and v
    # (orange), and the area of the patch is about the length of u x v (red); Delta s = Delta t moves with the slider
    _h = round(float(dd.value), 10)
    _s0 = _t0 = 1.0
    _fig, _ax = plane((-0.4, 3.4), (-0.4, 2.9), 2.8, names=("$s$", "$t$"))
    _ax.fill([_s0, _s0 + _h, _s0 + _h, _s0], [_t0, _t0, _t0 + _h, _t0 + _h], color=LIGHT, lw=0, zorder=0)
    _ax.plot([_s0 + _h, _s0 + _h, _s0], [_t0, _t0 + _h, _t0 + _h], color=BLUE, lw=1.8)
    arrow(_ax, (_s0, _t0), (_s0 + _h, _t0), ORANGE, lw=1.6)
    arrow(_ax, (_s0, _t0), (_s0, _t0 + _h), ORANGE, lw=1.6)
    for _c, _name, _ang in (((0, 0), "$(s, t)$", -135), ((1, 0), r"$(s + \Delta s, t)$", -45), ((0, 1), r"$(s, t + \Delta t)$", 135), ((1, 1), r"$(s + \Delta s, t + \Delta t)$", 45)):
        _r = (_s0 + _c[0] * _h, _t0 + _c[1] * _h)
        _ax.plot(*_r, "o", color="black", ms=4, zorder=6)
        beside(_ax, _r, _ang, _name, "black", 30, 12, gap=0, fontsize=11)

    # a surface curving upwards (a bowl), so that u and v, which join points of the surface, lie above it and are seen
    def _g(x, y):
        return 1.0 + 0.2 * ((x - 1.2) ** 2 + (y - 1.0) ** 2)

    _x1, _x2 = np.meshgrid(np.linspace(0.6, 2.8, 45), np.linspace(0.6, 2.8, 45), indexing="ij")
    _w = np.linspace(0.6, 2.8, 25)
    _rim = [(_c + 0 * _w, _w, _g(_c + 0 * _w, _w), BLUE, 1.2) for _c in (0.6, 2.8)] + [(_w, _c + 0 * _w, _g(_w, _c + 0 * _w), BLUE, 1.2) for _c in (0.6, 2.8)]

    def _Phi(s, t):
        return np.array([s, t, _g(s, t)])

    _P00, _P10, _P01, _P11 = _Phi(_s0, _t0), _Phi(_s0 + _h, _t0), _Phi(_s0, _t0 + _h), _Phi(_s0 + _h, _t0 + _h)
    _n = np.cross(_P10 - _P00, _P01 - _P00)
    _scene = turntable(
        28,
        32,
        "a patch of a surface S, image of a small square, with the vectors u and v along two of its sides and their cross product",
        [
            panel(
                1.0,
                surfaces=[sheet(_x1, _x2, _g(_x1, _x2), wire=[(0, 8, BLUE, 0.5), (1, 8, BLUE, 0.5)], tint=(_s0, _s0 + _h, _t0, _t0 + _h), clear=True)],
                lines=_rim,
                points=[(tuple(_r), "#000000", 3.4) for _r in (_P00, _P10, _P01, _P11)],
                arrows=[(_P00, _P10, ORANGE, 2.4), (_P00, _P01, ORANGE, 2.4), (_P00, _P00 + _n, RED)],
                texts=[
                    (tuple(_P00), r"\Phi(s, t)", "#000000", 135, 14),
                    (tuple(_P10), r"\Phi(s + \Delta s, t)", "#000000", -150, 18),
                    (tuple(_P01), r"\Phi(s, t + \Delta t)", "#000000", 30, 18),
                    (tuple(_P11), r"\Phi(s + \Delta s, t + \Delta t)", "#000000", -45, 14),
                    (tuple((_P00 + _P10) / 2), r"\vec{u}", ORANGE, 180, 6),
                    (tuple((_P00 + _P01) / 2), r"\vec{v}", ORANGE, 90, 6),
                    (tuple(_P00 + _n), r"\vec{u} \times \vec{v}", RED, 0, 6),
                    ((2.8, 0.6, float(_g(2.8, 0.6))), "S", BLUE, 200, 8),
                ],
                caption=r"\begin{gathered} \Phi(s + \Delta s, t) = \Phi(s, t) + \vec{u}, \quad \Phi(s, t + \Delta t) = \Phi(s, t) + \vec{v} \\ A \approx \lVert \vec{u} \times \vec{v} \rVert \end{gathered}",
                box=((0.6, 2.8), (0.6, 2.8), (0.9, 2.7)),
            )
        ],
        height=440,
        key="L22-patch",
        apart=True,
        beside=_fig,
    )
    mo.vstack([mo.hstack([dd], justify="start"), _scene])
    return


@app.cell(hide_code=True)
def _(frame, row):
    row('<div data-bs2d="L22-patch"></div>', frame("L22-patch", 440).text)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    The **surface integral** of $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ over $S$ is

    $$
    \iint_S f \, dA = \iint_D f(\Phi(s, t)) \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt
    $$

    The **flux** of $\vec{F} : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ across $\vec{S}$ is

    <span class="chain">$\displaystyle \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt$ $\displaystyle \qquad \vec{S} \ \longleftarrow \ \text{oriented surface (next time)}$</span>
    """,
        "Surface integral and flux",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $S = \Phi([0, \pi] \times [0, 2\pi])$, &nbsp; $\Phi(s, t) = \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix}$

    $f(x, y, z) = 1$, &nbsp; $\vec{F}(x, y, z) = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$

    <span class="chain">$\displaystyle \iint_S f \, dA = \iint\limits_{[0, \pi] \times [0, 2\pi]} 1 \, \lVert \underbrace{\Phi_s(s, t) \times \Phi_t(s, t)}_{\footnotesize 2\sin(s) \, \Phi(s, t)} \rVert \, dsdt$ $\displaystyle = \int_0^{2\pi} \left( \int_0^{\pi} 1 \, \lvert 4\sin(s) \rvert \, ds \right) dt$ $\displaystyle = \int_0^{2\pi} \big( -4\cos(s) \big) \Big|_{s=0}^{s=\pi} \, dt$ $\displaystyle = 2\pi \big( 4 - (-4) \big) = 16\pi \quad (= 4\pi r^2, \ r = 2)$</span>

    <span class="chain">$\displaystyle \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \iint\limits_{[0, \pi] \times [0, 2\pi]} \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} \cdot \left( 2\sin(s) \begin{bmatrix} 2\sin(s)\cos(t) \\ 2\sin(s)\sin(t) \\ 2\cos(s) \end{bmatrix} \right) dsdt$ $\displaystyle = \int_0^{\pi} \int_0^{2\pi} \big( 4(\sin(s))^2 \cos(t) \big) \, dt \, ds$ $\displaystyle = \int_0^{\pi} 4(\sin(s))^2 \big( \sin(t) \big) \Big|_{t=0}^{t=2\pi} \, ds = 0$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ① &nbsp; $\Phi(s, t) = \begin{bmatrix} s\cos(t) \\ s\sin(t) \\ s \end{bmatrix}$, &nbsp; $(s, t) \in [-2, 2] \times [0, 2\pi]$

    a) &nbsp; Describe $S = \mathrm{Im}(\Phi)$ with an equation in $x, y, z$.

    b) &nbsp; Sketch $S = \mathrm{Im}(\Phi)$.

    c) &nbsp; Find the tangent plane to $S$ at $\Phi\left(1, \dfrac{\pi}{2}\right)$.

    ② &nbsp; For the same $S$ as above

    a) &nbsp; Calculate the surface integral of $f(x, y, z) = z^2$.

    b) &nbsp; Calculate the flux of $\vec{F}(x, y, z) = \begin{bmatrix} -y \\ x \\ z \end{bmatrix}$.
    """)
    return


if __name__ == "__main__":
    app.run()
