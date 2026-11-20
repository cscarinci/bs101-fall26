import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 23 • Surface integrals of vector fields", css_file="bs101.css")



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
    header("Lecture 23", "Week 13", "Lecture 23 • Surface integrals of vector fields")
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

    def row(left, right):
        """A 2D figure beside a 3D one, as in lecture 16 (one above the other on narrow screens); both given as HTML."""
        return mo.Html(
            '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
            f'<div style="flex: 0 1 280px; min-width: 240px; max-width: 300px;">{left}</div>'
            f'<div style="flex: 1 1 440px; min-width: 300px;">{right}</div></div>'
        )

    return beside, curve, curve_side, curve_velocity, pi_tex, plane, row, sketch, span


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

    Parameterized surfaces and surface integrals

    $$
    \Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3, \quad (s, t) \longmapsto \Phi(s, t) = \begin{bmatrix} x(s, t) \\ y(s, t) \\ z(s, t) \end{bmatrix}
    $$

    parameterized surface &nbsp; $=$ &nbsp; parameterization of a surface &nbsp; $=$ &nbsp; 2-variable function with values in $\mathbb{R}^3$

    $S = \mathrm{Im}(\Phi) = \Phi(D) \subset \mathbb{R}^3$ &nbsp; 2-dimensional surface being parameterized by $\Phi$ &nbsp; $=$ &nbsp; subset of $\mathbb{R}^3$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, LIGHT, mo, np, panel, plane, row, sheet, turntable):
    # a parameterized surface (p. 1): the region D with a point (s, t) (blue) beside the surface S = Im(Phi) with Phi(s, t)
    # (black), as the second drawing of lecture 22's first figure (the graph of lecture 11). D and S are chosen for the
    # drawing only
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
        key="L23-surface",
    )
    row(mo.as_html(_fd).text, _surface.text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Given $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$

    $$
    \iint\limits_{S = \Phi(D)} f \, dA = \iint_D \mathrlap{\underbrace{\phantom{f(\Phi(s, t)) \, \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert}}_{\footnotesize \text{2-variable scalar valued function over } D \subseteq \mathbb{R}^2}} f(\Phi(s, t)) \, \overbrace{\lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt}^{dA}
    $$

    $\leadsto$ &nbsp; iterated integrals

    $dA = \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt$ &nbsp; infinitesimal area element of $S = \Phi(D)$ at $\Phi(s, t)$

    $\leadsto$ &nbsp; $\displaystyle \iint_S dA = \text{area of } S$

    Similar to &nbsp; $ds = \lVert \gamma'(t) \rVert \, dt$ &nbsp; infinitesimal arc-length element of $C = \gamma(I)$ at $\gamma(t)$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **In this lecture:** Surface integrals of vector fields in $\mathbb{R}^3$ (and examples)

    **References:** MT 7.4, 7.5, 7.6

    ## V.2 &nbsp; Surface integrals of vector fields

    **Example.** &nbsp; (polar parameterization of the disk)

    $$
    \Phi(s, t) = \begin{bmatrix} s\cos(t) \\ s\sin(t) \\ 0 \end{bmatrix}, \quad (s, t) \in [0, R] \times [0, 2\pi]
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\Longrightarrow$ &nbsp; on $xy$-plane &nbsp; $\left\{ \begin{aligned} s &= \text{distance from origin} \\ t &= \text{angle from } x\text{-axis} \end{aligned} \right.$

    $\Phi_s(s, t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ 0 \end{bmatrix}$, &nbsp; $\Phi_t(s, t) = \begin{bmatrix} -s\sin(t) \\ s\cos(t) \\ 0 \end{bmatrix}$

    <span class="chain">$\displaystyle \Longrightarrow \quad \Phi_s(s, t) \times \Phi_t(s, t) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \cos(t) & \sin(t) & 0 \\ -s\sin(t) & s\cos(t) & 0 \end{bmatrix}$ $\displaystyle = \begin{bmatrix} 0 \\ 0 \\ s \end{bmatrix}$</span>

    $$
    \Longrightarrow \quad \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert = \sqrt{s^2} = s
    $$

    <span class="chain">$\displaystyle \iint\limits_{S = \Phi(D)} dA = \iint_D \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt$ $\displaystyle = \int_0^{2\pi} \left( \int_0^R s \, ds \right) dt$ $\displaystyle = \int_0^{2\pi} \frac{R^2}{2} \, dt = \pi R^2$</span>

    $\leadsto$ &nbsp; $dA = s \, dsdt$ &nbsp; area element for the polar parameterization
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ps = mo.ui.slider(0, 2, 0.05, value=1.25, label="$s$", show_value=True)
    pt = mo.ui.slider(0, 6.28, 0.04, value=0.8, label="$t$", show_value=True)
    return ps, pt


@app.cell(hide_code=True)
def _(BLUE, LIGHT, ORANGE, RED, arrow, beside, mo, np, plane, ps, pt, sketch):
    # the polar parameterization of the disk (p. 2), in the layout of lecture 22's cylinder and sphere: the segment s = s0
    # of D (red) is mapped to the circle of radius s0, the segment t = t0 (orange) to the radius at the angle t0; the point
    # (s0, t0) to Phi(s0, t0) (black); s0 and t0 move with the sliders. R is drawn as 2; D is drawn with t / pi on its
    # vertical axis. The disk lies in the xy-plane, so it is drawn from above (a 2D figure) beside D. The names D and S sit
    # outside their regions
    _s0, _t0 = float(ps.value), float(pt.value)
    _fd, _ad = plane((-0.7, 3.0), (-0.55, 2.75), 2.8, names=("$s$", "$t$"))
    _ad.fill([0, 2, 2, 0], [0, 0, 2, 2], color=LIGHT, lw=0, zorder=0)
    _ad.plot([0, 2, 2, 0, 0], [0, 0, 2, 2, 0], color=BLUE, lw=1.8)
    _ad.plot([_s0, _s0], [0, 2], color=RED, lw=1.8, zorder=3)
    _ad.plot([0, 2], [_t0 / np.pi, _t0 / np.pi], color=ORANGE, lw=1.8, zorder=3)
    _ad.plot(_s0, _t0 / np.pi, "o", color="black", ms=4.5, zorder=6)
    beside(_ad, (2, 0), -90, "$R$", "black", 12, 14, gap=6)
    beside(_ad, (0, 2), 180, r"$2\pi$", "black", 20, 14)
    beside(_ad, (_s0, 2), 90, "$s$", RED, 8, 12)
    beside(_ad, (2, _t0 / np.pi), 0, "$t$", ORANGE, 8, 12)
    _ad.text(2.55, 2.5, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _fx, _ax = sketch((-2.6, 3.2), (-2.6, 3.2), 2.8)
    arrow(_ax, (-2.5, 0), (2.75, 0), "black", lw=0.9)
    arrow(_ax, (0, -2.5), (0, 2.75), "black", lw=0.9)
    beside(_ax, (2.75, 0), 0, "$x$", "black", 10, 12)
    beside(_ax, (0, 2.75), 90, "$y$", "black", 10, 12)
    _T = np.linspace(0, 2 * np.pi, 241)
    _ax.fill(2 * np.cos(_T), 2 * np.sin(_T), color=LIGHT, lw=0, zorder=0)
    _ax.plot(2 * np.cos(_T), 2 * np.sin(_T), color=BLUE, lw=1.8)
    _ax.plot(_s0 * np.cos(_T), _s0 * np.sin(_T), color=RED, lw=1.8, zorder=3)
    _ax.plot([0, 2 * np.cos(_t0)], [0, 2 * np.sin(_t0)], color=ORANGE, lw=1.8, zorder=3)
    _p = (_s0 * np.cos(_t0), _s0 * np.sin(_t0))
    if 0.05 < _t0 < 6.24:
        _V = np.linspace(0, _t0, 60)
        _ra = 0.45 if abs(_s0 - 0.45) > 0.25 else 0.95
        _ax.plot(_ra * np.cos(_V[:-3]), _ra * np.sin(_V[:-3]), color=ORANGE, lw=1.2, zorder=4)
        arrow(_ax, (_ra * np.cos(_V[-4]), _ra * np.sin(_V[-4])), (_ra * np.cos(_t0), _ra * np.sin(_t0)), ORANGE, lw=1.2)
        _ax.text((_ra + 0.23) * np.cos(_t0 / 2), (_ra + 0.23) * np.sin(_t0 / 2), "$t$", color=ORANGE, fontsize=13, ha="center", va="center", zorder=8)
    _ax.plot(*_p, "o", color="black", ms=4.5, zorder=6)
    _c, _n = np.cos(_t0 - np.pi / 3), np.sin(_t0 - np.pi / 3)
    _ax.text(_p[0] + 0.18 * _c, _p[1] + 0.18 * _n, r"$\Phi(s, t)$", color="black", fontsize=13, ha="center" if abs(_c) < 0.3 else ("left" if _c > 0 else "right"), va="center" if abs(_n) < 0.3 else ("bottom" if _n > 0 else "top"), zorder=8)
    beside(_ax, (0, 2), 135, "$R$", "black", 12, 14)
    _ax.text(-1.85, 1.85, "$S$", color=BLUE, fontsize=13, ha="center", va="center")
    mo.vstack([mo.hstack([ps, pt], justify="start", gap=2), mo.hstack([mo.as_html(_fd), mo.as_html(_fx)], justify="center", gap=2, wrap=True)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; (spherical parameterization of the sphere)

    $$
    \Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}, \quad (s, t) \in [0, \pi] \times [0, 2\pi]
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\left\{ \begin{aligned} s &= \text{angle with } z\text{-axis} \\ t &= \text{angle with the } x\text{-axis of the projection onto the } xy\text{-plane} \end{aligned} \right.$

    <span class="chain">$\displaystyle \iint_S dA = \iint_D \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt$ $\displaystyle = \int_0^{2\pi} \int_0^{\pi} R^2 \sin(s) \, ds \, dt = 4\pi R^2$</span>

    $\leadsto$ &nbsp; $dA = R^2 \sin(s) \, dsdt$ &nbsp; area element for the spherical parameterization
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ss = mo.ui.slider(0, 3.14, 0.04, value=0.8, label="$s$", show_value=True)
    st = mo.ui.slider(0, 6.28, 0.04, value=1.04, label="$t$", show_value=True)
    return ss, st


@app.cell(hide_code=True)
def _(BLUE, GREY, LIGHT, ORANGE, RED, beside, mo, np, panel, plane, sheet, ss, st, turntable):
    # the sphere (p. 3), as lecture 22's sphere figure: the segment s = s0 of D (red) is mapped to a circle of latitude,
    # the segment t = t0 (orange) to a meridian, the point (s0, t0) to Phi(s0, t0) (black); grey guides from the origin to
    # Phi(s0, t0) and to its projection onto the xy-plane, and from there up to Phi(s0, t0); the angle s at the z-axis
    # (red) and the angle t in the xy-plane (orange). s0 and t0 move with the sliders. R is drawn as 2; the sphere is
    # translucent, so that the guides and the angles inside it show; D and S are named outside their regions
    _s0, _t0 = float(ss.value), float(st.value)
    _x0, _y0 = 1.5 * _s0 / np.pi, _t0 / np.pi
    _fig, _ax = plane((-0.7, 2.9), (-0.55, 2.75), 2.8, names=("$s$", "$t$"))
    _ax.fill([0, 1.5, 1.5, 0], [0, 0, 2, 2], color=LIGHT, lw=0, zorder=0)
    _ax.plot([0, 1.5, 1.5, 0, 0], [0, 0, 2, 2, 0], color=BLUE, lw=1.8)
    _ax.plot([_x0] * 2, [0, 2], color=RED, lw=1.8, zorder=3)
    _ax.plot([0, 1.5], [_y0, _y0], color=ORANGE, lw=1.8, zorder=3)
    _ax.plot(_x0, _y0, "o", color="black", ms=4.5, zorder=6)
    beside(_ax, (1.5, 0), -90, r"$\pi$", "black", 12, 14, gap=6)
    beside(_ax, (0, 2), 180, r"$2\pi$", "black", 20, 14)
    beside(_ax, (_x0, 2), 90, "$s$", RED, 8, 12)
    beside(_ax, (1.5, _y0), 0, "$t$", ORANGE, 8, 12)
    _ax.text(2.05, 2.5, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 121)
    _S = np.linspace(0, np.pi, 61)
    _P = 2 * np.array([np.sin(_s0) * np.cos(_t0), np.sin(_s0) * np.sin(_t0), np.cos(_s0)])
    _g = np.linspace(0, 1, 30)
    _guides = [
        (_P[0] * _g, _P[1] * _g, _P[2] * _g, GREY, 1.0, [4, 3]),
        (_P[0] * _g, _P[1] * _g, 0 * _g, GREY, 1.0, [4, 3]),
        (_P[0] + 0 * _g, _P[1] + 0 * _g, _P[2] * _g, GREY, 1.0, [4, 3]),
    ]
    _arcs, _texts = [], [((0, -2.2, 1.9), "S", BLUE, 0, 0), (tuple(_P), r"\Phi(s, t)", "#000000", 40, 14)]
    if _s0 > 0.05:
        _U = np.linspace(0, _s0, 40)
        _arcs.append((0.7 * np.sin(_U) * np.cos(_t0), 0.7 * np.sin(_U) * np.sin(_t0), 0.7 * np.cos(_U), RED, 1.4))
        _texts.append(((0.95 * np.sin(_s0 / 2) * np.cos(_t0), 0.95 * np.sin(_s0 / 2) * np.sin(_t0), 0.95 * np.cos(_s0 / 2)), "s", RED, 0, 0))
    if 0.05 < _t0 < 6.24:
        _V = np.linspace(0, _t0, 60)
        _arcs.append((0.7 * np.cos(_V), 0.7 * np.sin(_V), 0 * _V, ORANGE, 1.4))
        _texts.append(((0.95 * np.cos(_t0 / 2), 0.95 * np.sin(_t0 / 2), 0), "t", ORANGE, 0, 0))
    _scene = turntable(
        30,
        22,
        "the sphere of radius R around the origin, with the circle of latitude s, the meridian at the angle t, the point Phi(s, t) and the angles s and t",
        [
            panel(
                1.0,
                surfaces=[sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, BLUE, 0.4), (1, 8, BLUE, 0.4)], alpha=0.45)],
                lines=[
                    (2 * np.sin(_s0) * np.cos(_T), 2 * np.sin(_s0) * np.sin(_T), 2 * np.cos(_s0) + 0 * _T, RED, 2.4),
                    (2 * np.sin(_S) * np.cos(_t0), 2 * np.sin(_S) * np.sin(_t0), 2 * np.cos(_S), ORANGE, 2.4),
                ]
                + _guides,
                points=[(tuple(_P), "#000000")],
                axes=[((0, 0, 0), (2.5, 0, 0), "x", -150), ((0, 0, 0), (0, 2.5, 0), "y", -20), ((0, 0, 0), (0, 0, 2.5), "z", 90)],
                arcs=_arcs,
                texts=_texts,
                box=((-2.0, 2.5), (-2.0, 2.5), (-2.0, 2.5)),
            )
        ],
        height=420,
        key="L23-sphere",
        apart=True,
        beside=_fig,
    )
    mo.vstack([mo.hstack([ss, st], justify="start", gap=2), _scene])
    return


@app.cell(hide_code=True)
def _(frame, row):
    row('<div data-bs2d="L23-sphere"></div>', frame("L23-sphere", 420).text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $f(x, y, z) = z$ &nbsp; “height from the equator”

    <span class="chain">$\displaystyle \iint_S f \, dA = \int_0^{2\pi} \left( \int_0^{\pi} R\cos(s) \cdot R^2 \sin(s) \, ds \right) dt$ $\displaystyle = \int_0^{2\pi} \left( R^3 \, \frac{\sin(s)^2}{2} \bigg|_{s=0}^{s=\pi} \right) dt = 0$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What about surface integrals of vector fields?

    **Recall:** for curves $C \subset \mathbb{R}^3$ with a parameterization $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$

    $$
    \int_C f \, ds = \int_I f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt
    $$

    $\leadsto$ &nbsp; $ds = \lVert \gamma'(t) \rVert \, dt$ &nbsp; infinitesimal length element

    <span class="chain">$\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_I \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt$ $\displaystyle \qquad \vec{C} \ \longleftarrow \ \text{oriented}$</span>

    $\leadsto$ &nbsp; $d\vec{s} = \gamma'(t) \, dt$ &nbsp; infinitesimal line element
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    dt = mo.ui.slider(0.1, 1.5, 0.1, value=1.2, label=r"$\Delta t$", show_value=True)
    return (dt,)


@app.cell(hide_code=True)
def _(BLUE, RED, curve, curve_side, dt, mo, np, panel, turntable):
    # lecture 22's curve figure (p. 4): the curve C (red) with the points gamma(t) and gamma(t + Delta t) (blue) and the
    # vector from one to the other (blue, as the velocity of lecture 19), about gamma'(t) Delta t; Delta t moves with the
    # slider. The names of the points sit in space on either side of the curve; the vector is named once, in the free
    # corner above (as the arrows of lecture 19's last figure)
    _u0, _h = 2.0, float(dt.value)
    _p, _q = np.array(curve(_u0)), np.array(curve(_u0 + _h))
    _scene = turntable(
        30,
        20,
        "the curve C with the points gamma(t) and gamma(t + Delta t) and the vector from the first to the second, about gamma'(t) Delta t",
        [
            panel(
                1.0,
                lines=[(*curve(np.linspace(-3.6, 3.6, 400)), RED, 1.8)],
                points=[(tuple(_p), BLUE, 4.0), (tuple(_q), BLUE, 4.0)],
                arrows=[(_p, _q, BLUE, 1.6)],
                axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 3.0, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
                texts=[
                    (tuple(_p + 0.4 * curve_side(_u0, -1)), r"\gamma(t)", "#000000", 0, 0),
                    (tuple(_q + 0.45 * curve_side(_u0 + _h)), r"\gamma(t + \Delta t)", "#000000", 0, 0),
                    ((0, 1.2, 3.0), r"\Delta\vec{s} \approx \gamma'(t) \, \Delta t", BLUE, 0, 0),
                ],
                box=((0, 3.0), (0, 3.0), (0, 3.0)),
            )
        ],
        height=340,
        key="L23-secant",
        apart=True,
    )
    mo.vstack([mo.hstack([dt], justify="start"), _scene])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("L23-secant", 340)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Similarly, for a surface $S \subset \mathbb{R}^3$ with a parameterization $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$

    $$
    \iint_S f \, dA = \iint_D f(\Phi(s, t)) \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt
    $$

    $\leadsto$ &nbsp; $dA = \lVert \Phi_s(s, t) \times \Phi_t(s, t) \rVert \, dsdt$ &nbsp; infinitesimal area element

    <span class="chain">$\displaystyle \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt$ $\displaystyle \qquad \vec{S} \ \longleftarrow \ \text{oriented}$</span>

    $\leadsto$ &nbsp; $d\vec{A} = \Phi_s(s, t) \times \Phi_t(s, t) \, dsdt$ &nbsp; infinitesimal surface element (oriented area element)
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, RED, np, panel, sheet, turntable):
    # the surface element (p. 4), as lecture 22's tangent-plane figure (lecture 11's) without the plane: a graph S (chosen
    # for the drawing only), Phi(s, t) = (s, t, f(s, t)), the point Phi(s, t) (black) with its tangent vectors Phi_s and
    # Phi_t (orange), the two coordinate curves through it (grey) with the points Phi(s + Delta s, t) and
    # Phi(s, t + Delta t) (black), and the normal, about Phi_s x Phi_t Delta s Delta t (red); no guides, so that
    # the names have room; axes from the origin, just past the surface, as lecture 19
    def _f(x1, x2):
        return 2.4 - 0.2 * ((x1 - 1.9) ** 2 + (x2 - 1.7) ** 2)

    _a = (1.3, 1.6)
    _d1, _d2 = -0.4 * (_a[0] - 1.9), -0.4 * (_a[1] - 1.7)
    _fa = float(_f(*_a))
    _lo, _hi, _vv, _D = 0.5, 3.1, 1.5, 1.1
    _x1, _x2 = np.meshgrid(np.linspace(_lo, _hi, 25), np.linspace(_lo, _hi, 25), indexing="ij")
    _w = np.linspace(_lo, _hi, 25)
    _rim = [(_c + 0 * _w, _w) for _c in (_lo, _hi)] + [(_w, _c + 0 * _w) for _c in (_lo, _hi)]
    _W = np.linspace(_lo, _hi, 105)
    _P = np.array([_a[0], _a[1], _fa])
    _fs, _ft = np.array([_vv, 0, _vv * _d1]), np.array([0, _vv, _vv * _d2])
    _n = np.array([-_d1, -_d2, 1.0])
    _Ps = (_a[0] + _D, _a[1], float(_f(_a[0] + _D, _a[1])))
    _Pt = (_a[0], _a[1] + _D, float(_f(_a[0], _a[1] + _D)))
    _scene = turntable(
        50,
        30,
        "a surface S with the point Phi(s, t), its tangent vectors Phi_s and Phi_t, the points Phi(s + Delta s, t) and Phi(s, t + Delta t) on the coordinate curves through it, and the normal vector, about Phi_s x Phi_t Delta s Delta t",
        [
            panel(
                1.0,
                surfaces=[sheet(_x1, _x2, _f(_x1, _x2), wire=[(0, 4, BLUE, 0.5), (1, 4, BLUE, 0.5)])],
                lines=[(_c1, _c2, _f(_c1, _c2), BLUE, 1.2) for _c1, _c2 in _rim]
                + [
                    (_W, _a[1] + 0 * _W, _f(_W, _a[1]), GREY, 2.0, None, 0.1),
                    (_a[0] + 0 * _W, _W, _f(_a[0], _W), GREY, 2.0, None, 0.1),
                ],
                points=[(tuple(_P), "#000000"), (_Ps, "#000000"), (_Pt, "#000000")],
                arrows=[(_P, _P + _fs, ORANGE), (_P, _P + _ft, ORANGE), (_P, _P + _n, RED)],
                texts=[
                    ((_hi, _lo, _f(_hi, _lo)), "S", BLUE, 200, 8),
                    (tuple(_P), r"\Phi(s, t)", "#000000", 135, 14),
                    (tuple(_P + _n), r"\Delta\vec{A} \approx \Phi_s(s, t) \times \Phi_t(s, t) \, \Delta s \, \Delta t", RED, 0, 6),
                    (tuple(_P + _fs), r"\Phi_s(s, t)", ORANGE, 120, 10),
                    (tuple(_P + _ft), r"\Phi_t(s, t)", ORANGE, 50, 12),
                    (_Ps, r"\Phi(s + \Delta s, t)", "#000000", 200, 8),
                    (_Pt, r"\Phi(s, t + \Delta t)", "#000000", -70, 8),
                ],
                axes=[((0, 0, 0), (3.4, 0, 0), "x", -150), ((0, 0, 0), (0, 3.4, 0), "y", -20), ((0, 0, 0), (0, 0, _fa + 1.3), "z", 90)],
                box=((0, 3.4), (0, 3.4), (0, _fa + 1.3)),
            )
        ],
        height=500,
        key="L23-surface-element",
    )
    _scene
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    An **orientation** of a surface $S$ is a continuous choice of the direction of the normal vectors at each point of $S$.
    """,
        "Orientation",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $S$ = disk on the $xy$-plane

    $\leadsto$ &nbsp; $\vec{n} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$ at each point gives one orientation, pointing “up”

    $\leadsto$ &nbsp; $-\vec{n} = \begin{bmatrix} 0 \\ 0 \\ -1 \end{bmatrix}$ gives another, pointing “down”

    $\leadsto$ &nbsp; these are the only options

    **Example.** &nbsp; $S$ = sphere

    $\leadsto$ &nbsp; $\vec{n} = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$ gives one orientation, pointing “out”

    $\leadsto$ &nbsp; $-\vec{n} = \begin{bmatrix} -x \\ -y \\ -z \end{bmatrix}$ gives another, pointing “in”
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, RED, np, panel, sheet, turntable):
    # orientations (p. 5), three drawings side by side as lecture 18's, each with its axes: the disk with the normal vectors n pointing up, the
    # sphere with n pointing out, the sphere with -n pointing in (red, the normal of lecture 11), every vector of length 1/2,
    # at the centre of the disk and on two circles, and at points on three circles of latitude of the sphere and its poles.
    # The sphere is drawn translucent, so that the vectors pointing in can be seen
    _r, _a = np.meshgrid(np.linspace(0, 1, 9), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _disk = sheet(_r * np.cos(_a), _r * np.sin(_a), 0 * _r, wire=[(0, 8, BLUE, 0.6)], alpha=0.85)
    _dp = [np.zeros(3)] + [np.array([_q * np.cos(_v), _q * np.sin(_v), 0.0]) for _q, _m, _o in ((0.45, 6, 0.0), (0.85, 10, 0.3)) for _v in _o + 2 * np.pi * np.arange(_m) / _m]
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 73), indexing="ij")
    _sphere = sheet(np.sin(_s) * np.cos(_t), np.sin(_s) * np.sin(_t), np.cos(_s), wire=[(0, 6, BLUE, 0.4), (1, 9, BLUE, 0.4)], alpha=0.45)
    _sp = [np.array([0, 0, 1.0]), np.array([0, 0, -1.0])] + [
        np.array([np.sin(_u) * np.cos(_v), np.sin(_u) * np.sin(_v), np.cos(_u)]) for _u, _m, _o in ((np.pi / 4, 6, 0.0), (np.pi / 2, 8, 0.4), (3 * np.pi / 4, 6, 0.5)) for _v in _o + 2 * np.pi * np.arange(_m) / _m
    ]
    _scene = turntable(
        30,
        24,
        "the disk with the normal vectors n pointing up; the sphere with the normal vectors n pointing out; the sphere with the normal vectors -n pointing in",
        [
            panel(1.0, surfaces=[_disk], axes=[((0, 0, 0), (1.4, 0, 0), "x", -150), ((0, 0, 0), (0, 1.4, 0), "y", -20), ((0, 0, 0), (0, 0, 1.0), "z", 90)], arrows=[(_p, _p + np.array([0, 0, 0.5]), RED, 1.3) for _p in _dp], caption=r"\vec{n} \ \text{pointing ``up''}", box=((-1, 1.4), (-1, 1.4), (0, 1.0))),
            panel(1.0, surfaces=[_sphere], axes=[((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 1.8, 0), "y", -20), ((0, 0, 0), (0, 0, 1.8), "z", 90)], arrows=[(_p, 1.5 * _p, RED, 1.3) for _p in _sp], caption=r"\vec{n} \ \text{pointing ``out''}", box=((-1.5, 1.8), (-1.5, 1.8), (-1.5, 1.8))),
            panel(1.0, surfaces=[_sphere], axes=[((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 1.8, 0), "y", -20), ((0, 0, 0), (0, 0, 1.8), "z", 90)], arrows=[(_p, 0.5 * _p, RED, 1.3) for _p in _sp], caption=r"-\vec{n} \ \text{pointing ``in''}", box=((-1.5, 1.8), (-1.5, 1.8), (-1.5, 1.8))),
        ],
        height=300,
        cols=3,
        key="L23-orientations",
        shared=False,
    )
    _scene
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given an oriented surface $\vec{S}$, and a parameterization $\Phi : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}^3$ such that $\Phi_s(s, t) \times \Phi_t(s, t)$ agrees with the orientation, the **flux** of $\vec{F} : \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ across $\vec{S}$ is

    $$
    \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \iint_D \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big) \, dsdt
    $$
    """,
        "Flux",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\vec{F}(x, y, z) = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$ &nbsp; radial vector field along each $z = \text{constant}$ plane

    $$
    \Phi(s, t) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}
    $$

    $\vec{S}$ = sphere of radius $R$ oriented outward
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \Phi_s(s, t) \times \Phi_t(s, t) = R\sin(s) \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ R\cos(s) \end{bmatrix}
    $$

    $$
    \vec{F}(\Phi(s, t)) = \begin{bmatrix} R\sin(s)\cos(t) \\ R\sin(s)\sin(t) \\ 0 \end{bmatrix}
    $$

    <span class="chain">$\displaystyle \Longrightarrow \quad \vec{F}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big)$ $\displaystyle = R^3 \sin(s)^3 \cos(t)^2 + R^3 \sin(s)^3 \sin(t)^2$ $\displaystyle = R^3 \sin(s)^3$</span>

    <span class="chain">$\displaystyle \Longrightarrow \quad \iint_{\vec{S}} \vec{F} \cdot d\vec{A} = \int_0^{2\pi} \left( \int_0^{\pi} R^3 \sin(s)^3 \, ds \right) dt = \frac{8\pi R^3}{3}$</span>

    $\vec{G}(x, y, z) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$

    <span class="chain">$\displaystyle \leadsto \quad \vec{G}(\Phi(s, t)) \cdot \big( \Phi_s(s, t) \times \Phi_t(s, t) \big)$ $\displaystyle = R^3 \sin(s) \big( \sin(s)^2 + \cos(s)^2 \big)$ $\displaystyle = R^3 \sin(s)$</span>

    $$
    \Longrightarrow \quad \iint_{\vec{S}} \vec{G} \cdot d\vec{A} = 4\pi R^3
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, np, panel, sheet, turntable):
    # the vector field F(x, y, z) = (x, y, 0) on the sphere (p. 6), as the fields of lecture 18 (green, every arrow at 1/2 of
    # its vector) at points on five circles of latitude (eight per circle, every other circle turned by half a step); the
    # sphere as lecture 22's. R is drawn as 2. F is named once, in the free corner above
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _pts = [
        2 * np.array([np.sin(_u) * np.cos(_v), np.sin(_u) * np.sin(_v), np.cos(_u)])
        for _i, _u in enumerate(np.pi * np.arange(1, 6) / 6)
        for _v in (_i % 2) * np.pi / 8 + 2 * np.pi * np.arange(8) / 8
    ]
    _scene = turntable(
        30,
        22,
        "the sphere of radius R with the vector field F(x, y, z) = (x, y, 0) at points on five circles of latitude",
        [
            panel(
                1.0,
                surfaces=[sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, BLUE, 0.4), (1, 8, BLUE, 0.4)], alpha=0.85)],
                arrows=[(_p, _p + 0.5 * np.array([_p[0], _p[1], 0.0]), GREEN, 1.3) for _p in _pts],
                axes=[((0, 0, 0), (3.4, 0, 0), "x", -150), ((0, 0, 0), (0, 3.4, 0), "y", -20), ((0, 0, 0), (0, 0, 2.8), "z", 90)],
                texts=[((0, -3.0, 2.6), r"\vec{F} = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}", GREEN, 180, 0)],
                box=((-3.0, 3.0), (-3.0, 3.0), (-2.0, 2.8)),
            )
        ],
        height=440,
        key="L23-field",
    )
    _scene
    return


if __name__ == "__main__":
    app.run()
