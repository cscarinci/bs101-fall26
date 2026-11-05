import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 19 • Integration along paths", css_file="bs101.css")


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

    return BLUE, GREEN, GREY, ORANGE, RED, arrow, definition, header, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 19", "Week 11", "Lecture 19 • Integration along paths")
    return


@app.cell(hide_code=True)
def _(Figure, math, np):
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

    # the path of the two sketches of a curve (pp. 1 and 5): gamma(s) = (s, 0.9 sin(1.1 s) + 0.3 s), with C = gamma([a, b])
    A, B = 0.0, 4.8

    def path(s):
        s = np.asarray(s, float)
        return s, 0.9 * np.sin(1.1 * s) + 0.3 * s

    def velocity(s):
        return np.array([1.0, 0.99 * math.cos(1.1 * s) + 0.3])

    def side(v, sign):
        """The direction (degrees) of the normal of the curve with velocity v: on its upper side for sign = 1,
        on its lower side for sign = -1."""
        return math.degrees(math.atan2(sign * v[0], -sign * v[1]))

    return A, B, beside, path, side, sketch, velocity


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

    return frame, panel, turntable


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Vector fields, divergence and curl

    $\leadsto$ &nbsp; when are vector fields gradients?

    $\leadsto$ &nbsp; when are vector fields curls?
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    $$
    \text{If} \quad \begin{aligned} \vec{\nabla} \times \vec{F} \neq \vec{0} \quad &\Longrightarrow \quad \vec{F} \neq \vec{\nabla} f \\ \vec{\nabla} \cdot \vec{F} \neq 0 \quad &\Longrightarrow \quad \vec{F} \neq \vec{\nabla} \times \vec{G} \end{aligned}
    $$
    """,
        "Necessary conditions",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \leadsto \quad \begin{aligned} \vec{\nabla} \times \vec{F} = \vec{0} \ &\text{ is necessary for } \vec{F} = \vec{\nabla} f \\ \vec{\nabla} \cdot \vec{F} = 0 \ &\text{ is necessary for } \vec{F} = \vec{\nabla} \times \vec{G} \end{aligned}
    $$

    **In this lecture:**

    <span class="chain">$\displaystyle \text{Is } \vec{\nabla} \times \vec{F} = \vec{0} \ \underbrace{\text{sufficient}}_{\mathclap{\footnotesize \text{does } \vec{\nabla} \times \vec{F} = \vec{0} \text{ imply } \vec{F} = \vec{\nabla} f \text{ ?}}\vphantom{\footnotesize \text{does } \vec{\nabla} \times \vec{F} = \vec{0} \text{ imply } \vec{F} = \vec{\nabla} f \text{ ?}}} \text{ for } \vec{F} = \vec{\nabla} f \text{ ?}$ $\displaystyle \quad \text{(spoilers : No…)}$</span>

    $\leadsto$ &nbsp; integration along paths

    **References:** MT 4.2, 7.1, 7.2

    ## IV.3 &nbsp; Integration along paths
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given a differentiable path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$, the **arc length** of the curve $\underbrace{C = \gamma([a, b])}_{\footnotesize \text{assuming } [a, b] \subseteq I}$ is

    $$
    L(C) = L(\gamma([a, b])) = \int_a^b \underbrace{\lVert \gamma'(t) \rVert}_{\mathclap{\footnotesize \text{speed of } \gamma \text{ at } t}\vphantom{\footnotesize \text{speed of } \gamma \text{ at } t}} \, dt
    $$
    """,
        "Arc length",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ts1 = mo.ui.slider(0.2, 4.0, 0.02, value=1.3, label="$t$", show_value=True)
    return (ts1,)


@app.cell(hide_code=True)
def _(A, B, BLUE, GREY, RED, arrow, beside, math, mo, np, path, side, sketch, ts1, velocity):
    # the curve C = gamma([a, b]) in red, the path before a and after b in grey; gamma(t) (blue) moves with t, with its
    # velocity gamma'(t) at its true length (blue). It starts near the top of the arch, as on the page; the name of gamma(t)
    # sits on the lower side of the curve, along its normal, so that it turns with t and never jumps
    _t = round(ts1.value, 10)
    _fig, _ax = sketch((-1.4, 6.0), (-1.5, 3.0), 4.6)
    _ax.plot(*path(np.linspace(-1.0, A, 60)), color=GREY, lw=1.4)
    _ax.plot(*path(np.linspace(B, B + 0.9, 60)), color=GREY, lw=1.4)
    _ax.plot(*path(np.linspace(A, B, 400)), color=RED, lw=1.8)
    _pa, _pb, _pt = (np.array(path(_s)) for _s in (A, B, _t))
    _v = velocity(_t)
    arrow(_ax, _pt, _pt + _v, BLUE, lw=1.6)
    for _p, _c in ((_pa, RED), (_pb, RED), (_pt, BLUE)):
        _ax.plot(*_p, "o", color=_c, ms=4.5, zorder=6)
    beside(_ax, _pa, 180, r"$\gamma(a)$", "black", 30, 16)
    beside(_ax, _pb, 120, r"$\gamma(b)$", "black", 30, 16)
    beside(_ax, _pt, side(_v, -1), r"$\gamma(t)$", "black", 30, 16)
    beside(_ax, _pt + _v, math.degrees(math.atan2(_v[1], _v[0])), r"$\gamma'(t)$", BLUE, 34, 16, gap=2)
    _ax.text(-0.35, 0.95, r"$C = \gamma([a, b])$", color=RED, fontsize=13, ha="center", va="center")
    mo.vstack([mo.hstack([ts1], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \gamma'(t) = \text{velocity of } \gamma \text{ at } t$ $\displaystyle = \lim_{h \to 0} \frac{\gamma(t + h) - \gamma(t)}{h}$ $\displaystyle \quad \Longrightarrow \quad \lVert \gamma(t + h) - \gamma(t) \rVert \approx \lVert \gamma'(t) \rVert h$</span>

    **Example.** &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; $\gamma'(t) = \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix}$

    <span class="chain">$\displaystyle L(\gamma([0, 2\pi])) = \int_0^{2\pi} \left( (\sin(t))^2 + (\cos(t))^2 + 1 \right)^{\frac{1}{2}} dt$ $\displaystyle = \int_0^{2\pi} \sqrt{2} \, dt = 2\pi\sqrt{2}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(GREY, RED, np, panel, turntable):
    # the helix gamma(t) = (cos(t), sin(t), t); the curve C = gamma([0, 2 pi]) in red, the helix before 0 and after 2 pi in
    # grey. Heights at half scale, as in the helix figures of lecture 18, so that the helix shows its turn
    _s = np.linspace(-1.2, 0, 60)
    _e = np.linspace(2 * np.pi, 2 * np.pi + 1.2, 60)
    _c = np.linspace(0, 2 * np.pi, 300)
    _g0, _g1 = (1.0, 0.0, 0.0), (1.0, 0.0, 2 * np.pi)
    _fig = turntable(
        30, 20, "the helix gamma(t) = [cos(t); sin(t); t], with the curve C = gamma([0, 2 pi]) from gamma(0) to gamma(2 pi)",
        [
            panel(
                0.5,
                lines=[(np.cos(_s), np.sin(_s), _s, GREY, 1.4), (np.cos(_e), np.sin(_e), _e, GREY, 1.4), (np.cos(_c), np.sin(_c), _c, RED, 1.8)],
                points=[(_g0, RED, 4.0), (_g1, RED, 4.0)],
                axes=[((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 2.0, 0), "y", 0), ((0, 0, 0), (0, 0, 8.2), "z", 90)],
                # the names of gamma(0) and gamma(2 pi) placed in space, away from the axes as the figure turns: gamma(0)
                # below its point, towards the side where C leaves it; gamma(2 pi) above its point, a little out from the z-axis
                texts=[((1.0, 0.35, -0.25), r"\gamma(0)", "#000000", -90, 0), ((1.6, 0.0, 2 * np.pi + 0.9), r"\gamma(2\pi)", "#000000", 90, 0),
                       ((np.cos(np.pi / 2), np.sin(np.pi / 2), np.pi / 2), r"C = \gamma([0, 2\pi])", RED, 0, 8)],
                box=((-1.4, 1.4), (-1.4, 1.4), (-1.2, 9.0)),
            )
        ],
        height=380,
        key="L19-helix",
    )
    _fig
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given a differentiable path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ and a continuous function $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$, the **path integral** of $f$ over $C = \gamma([a, b]) \subseteq D$ (along the path $\gamma$) is

    $$
    \int_C f \, ds = \int_a^b \underbrace{f(\gamma(t)) \lVert \gamma'(t) \rVert}_{\mathclap{\footnotesize \begin{matrix} f \text{ calculated along } \gamma \\ \text{times the speed of } \gamma \end{matrix}}\vphantom{\footnotesize \begin{matrix} f \text{ calculated along } \gamma \\ \text{times the speed of } \gamma \end{matrix}}} \, dt
    $$
    """,
        "Path integral",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $f(x, y, z) = z$, &nbsp; $C = \gamma([0, 2\pi])$, &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$

    $$
    \int_C f \, ds = \int_0^{2\pi} t \sqrt{2} \, dt = \frac{(2\pi)^2}{2} \sqrt{2}
    $$

    Why do we multiply by the speed of $\gamma$?

    $\leadsto$ &nbsp; because we want these integrals to only depend on the function $f$ and on the curve $C = \gamma([a, b])$, but not on the $\underbrace{\text{choice of parameterization}}_{\mathclap{\footnotesize \begin{matrix} \text{the specific path } \gamma \\ \text{with } \gamma([a, b]) = C \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{the specific path } \gamma \\ \text{with } \gamma([a, b]) = C \end{matrix}}}$ of $C$!

    **Example.** &nbsp; $f(x, y, z) = z$, &nbsp; $\sigma(t) = \begin{bmatrix} \cos(2t) \\ \sin(2t) \\ 2t \end{bmatrix}$ &nbsp; $\Longrightarrow \ \sigma([0, \pi]) = \gamma([0, 2\pi]) = C$

    with &nbsp; $\lVert \sigma'(t) \rVert = 2\sqrt{2} = 2 \lVert \gamma'(t) \rVert$ &nbsp; $\leadsto$ &nbsp; $\sigma$ travels across the same $C$ with twice the speed of $\gamma$

    $$
    ① \quad L(C) = \underbrace{\int_0^{2\pi} \lVert \gamma'(t) \rVert \, dt = \int_0^{\pi} \lVert \sigma'(\tilde{t}) \rVert \, d\tilde{t}}_{\footnotesize \begin{matrix} \text{length should be independent of} \\ \text{the way we travel across } C \end{matrix}} = \int_C (1) \, ds
    $$

    $$
    ② \quad \int_C z \, ds = \underbrace{\int_0^{2\pi} t \lVert \gamma'(t) \rVert \, dt \qquad \overset{\mathclap{\footnotesize \begin{matrix} \text{integration by} \\ \text{substitution} \\ \downarrow \end{matrix}}}{\vphantom{\Bigg|} =} \qquad \int_0^{\pi} 2\tilde{t} \lVert \sigma'(\tilde{t}) \rVert \, d\tilde{t}}_{\footnotesize \begin{matrix} \text{integral of } f \text{ over } C \\ \text{should also be independent!} \end{matrix}}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    A **reparameterization** of a path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ is another path $\sigma = \gamma \circ \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ obtained by a change of variables

    $$
    \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow I \subseteq \mathbb{R}, \qquad \tilde{t} \longmapsto t = \varphi(\tilde{t})
    $$
    """,
        "Reparameterization",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\Longrightarrow$ &nbsp; $\gamma(t) = \gamma(\varphi(\tilde{t})) = \sigma(\tilde{t})$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{Im}(\gamma) = \mathrm{Im}(\sigma)$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ a differentiable path, $\sigma = \gamma \circ \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ a reparameterization with $\varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow I \subseteq \mathbb{R}$ a differentiable change of variables with $\varphi'(\tilde{t}) \neq 0$ for all $\tilde{t} \in \tilde{I}$. Then for any continuous function $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$

    $$
    \int_c^d f(\sigma(\tilde{t})) \lVert \sigma'(\tilde{t}) \rVert \, d\tilde{t} \ \underset{\mathclap{\footnotesize \begin{matrix} \uparrow \\ \text{substitution of variables} \\ t = \varphi(\tilde{t}) \end{matrix}}}{=} \ \int_a^b f(\gamma(t)) \lVert \gamma'(t) \rVert \, dt
    $$

    where $[a, b] = \varphi([c, d])$.
    """,
        "Path integrals and reparameterization",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\Longrightarrow$ &nbsp; $\displaystyle \int_C f \, ds$ &nbsp; is independent of the choice of path $\gamma$ parameterizing $C$!
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given a differentiable path $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$ and a continuous vector field $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$, the **line integral** of $\vec{F}$ over $C = \gamma([a, b]) \subseteq D$ $\underbrace{\text{from } \gamma(a) \text{ to } \gamma(b)}_{\mathclap{\footnotesize \text{orientation of } C}\vphantom{\footnotesize \text{orientation of } C}}$ (along the path $\gamma$) is

    <span class="chain">$\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt$ $\displaystyle \qquad \vec{C} \ \longleftarrow \ \text{oriented curve}$</span>
    """,
        "Line integral",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ts = mo.ui.slider(0.6, 4.0, 0.04, value=1.2, label="$t$", show_value=True)
    return (ts,)


@app.cell(hide_code=True)
def _(A, B, BLUE, GREEN, GREY, RED, arrow, beside, math, mo, np, path, side, sketch, ts, velocity):
    # the curve of the first sketch, C = gamma([a, b]) in red, from gamma(a) to gamma(b); gamma(t) (blue) moves with t,
    # with its velocity gamma'(t) (blue) and the vector F(gamma(t)) of a vector field (green), both at their true length.
    # The field F = 0.15 (y + 3, -(x - 2.4)) turns about a point below the picture, so no arrow in view is tiny; it is
    # drawn faint on six copies of the curve 0.6 apart, and gamma(t) meets the arrows on the curve at t = 0.6, 1.2, ...
    # (the slider starts at the first of them)
    # The name of gamma(t) sits on the lower side of the curve, along its normal, so that it turns with t and never
    # jumps; the two arrows are named in the free top left corner
    _t = round(ts.value, 10)
    _fig, _ax = sketch((-1.4, 6.0), (-1.5, 3.6), 4.6)
    _F = lambda p: 0.15 * np.array([p[1] + 3.0, -(p[0] - 2.4)])
    for _x in np.arange(-0.6, 5.41, 0.6):
        for _c in (-1.2, -0.6, 0.0, 0.6, 1.2, 1.8):
            _g = np.array([_x, path(_x)[1] + _c])
            if -1.4 < _g[1] < 3.0:
                _ax.annotate("", xy=_g + _F(_g), xytext=_g, zorder=1, arrowprops={"arrowstyle": "->,head_length=0.35,head_width=0.22", "mutation_scale": 11, "color": GREEN, "lw": 1.0, "alpha": 0.5, "shrinkA": 0, "shrinkB": 0})
    _ax.plot(*path(np.linspace(-1.0, A, 60)), color=GREY, lw=1.4)
    _ax.plot(*path(np.linspace(B, B + 0.9, 60)), color=GREY, lw=1.4)
    _ax.plot(*path(np.linspace(A, B, 400)), color=RED, lw=1.8)
    _pa, _pb, _pt = (np.array(path(_s)) for _s in (A, B, _t))
    _v, _f = velocity(_t), _F(_pt)
    arrow(_ax, _pt, _pt + _f, GREEN, lw=1.6)
    arrow(_ax, _pt, _pt + _v, BLUE, lw=1.6)
    for _p, _c in ((_pa, RED), (_pb, RED), (_pt, BLUE)):
        _ax.plot(*_p, "o", color=_c, ms=4.5, zorder=6)
    beside(_ax, _pa, 180, r"$\gamma(a)$", "black", 30, 16)
    beside(_ax, _pb, 120, r"$\gamma(b)$", "black", 30, 16)
    beside(_ax, _pt, side(_v, -1), r"$\gamma(t)$", "black", 30, 16)
    # the two arrows named once, fixed, in the free top left corner, each in its arrow's colour: no place beside the moving
    # arrows stays off the curve for every t
    _ax.text(-1.3, 3.3, r"$\gamma'(t)$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax.text(-1.3, 2.85, r"$\vec{F}(\gamma(t))$", color=GREEN, fontsize=13, ha="left", va="center")
    mo.vstack([mo.hstack([ts], justify="start"), mo.hstack([_fig], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\vec{F}(x, y, z) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$, &nbsp; $\vec{C} = \gamma([0, 2\pi])$ from $\gamma(0)$ to $\gamma(2\pi)$, &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$

    <span class="chain">$\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s} = \int_0^{2\pi} \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix} dt$ $\displaystyle = \int_0^{2\pi} 2 \, dt = 4\pi$</span>

    <span class="chain">$\displaystyle \vec{G}(x, y, z) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$ $\displaystyle \qquad \int_{\vec{C}} \vec{G} \cdot d\vec{s} = \int_0^{2\pi} \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 1 \end{bmatrix} dt$ $\displaystyle = \int_0^{2\pi} t \, dt = \frac{(2\pi)^2}{2}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    tf = mo.ui.slider(0, round(2 * np.pi, 2), 0.04, value=2.6, label="$t$", show_value=True)
    return (tf,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, RED, mo, np, panel, tf, turntable):
    # the two fields of the Example, F(x) = (-y, x, 1) and G(x) = (x, y, z), side by side, along the helix
    # gamma(t) = (cos(t), sin(t), t) of the helix figure above (its view and its scale, the box 0.6 higher for G's top arrow).
    # Every arrow at 1/2 of its vector. The fields in space faint, on a grid around the helix (x, y in {-1, 0, 1} without the
    # z-axis, at the heights pi/2 and 3 pi/2), and a little stronger at nine points of the helix; gamma(t) moves with t, with
    # gamma'(t) (blue) and the field at gamma(t) (green; for F it is gamma'(t) itself). gamma(t) and the arrows are named in the
    # fixed place under each panel, the arrows in their colours: beside the moving point no place stays clear of the axes
    _t = round(tf.value, 10)
    _K = 0.5
    _pale, _mid = "#a7bfad", "#7d9f86"  # GREEN halfway and a quarter of the way to white

    def _gam(t):
        return np.array([np.cos(t), np.sin(t), t])

    def _F(p):
        return np.array([-p[1], p[0], 1.0])

    def _G(p):
        return np.array(p, dtype=float)

    _grid = [np.array([x, y, z]) for z in (np.pi / 2, 3 * np.pi / 2) for x in (-1.0, 0.0, 1.0) for y in (-1.0, 0.0, 1.0) if (x, y) != (0.0, 0.0)]
    _ts = np.linspace(0, 2 * np.pi, 9)
    _s, _e, _c = np.linspace(-1.2, 0, 60), np.linspace(2 * np.pi, 2 * np.pi + 1.2, 60), np.linspace(0, 2 * np.pi, 300)
    _helix = [(np.cos(_s), np.sin(_s), _s, GREY, 1.4), (np.cos(_e), np.sin(_e), _e, GREY, 1.4), (np.cos(_c), np.sin(_c), _c, RED, 1.8)]
    _axes = [((0, 0, 0), (1.8, 0, 0), "x", -150), ((0, 0, 0), (0, 2.0, 0), "y", 0), ((0, 0, 0), (0, 0, 8.2), "z", 90)]
    _p, _v = _gam(_t), _K * np.array([-np.sin(_t), np.cos(_t), 1.0])
    _names = {"F": r"\textcolor{#4f7f5c}{\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}} \\ \rule{0pt}{1.6em} \gamma(t) \qquad \textcolor{#3f5f8f}{\gamma'(t) = \vec{F}(\gamma(t))}",
              "G": r"\textcolor{#4f7f5c}{\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}} \\ \rule{0pt}{1.6em} \gamma(t) \qquad \textcolor{#3f5f8f}{\gamma'(t)} \qquad \textcolor{#4f7f5c}{\vec{G}(\gamma(t))}"}

    def _panel(field, name):
        _arrows = [(q, q + _K * field(q), _pale, 1.0) for q in _grid] + [(_gam(s), _gam(s) + _K * field(_gam(s)), _mid, 1.2) for s in _ts]
        _arrows += ([] if name == "F" else [(_p, _p + _K * field(_p), GREEN, 2.2)]) + [(_p, _p + _v, BLUE, 2.2)]
        return panel(0.5, lines=_helix, axes=_axes, points=[(_p, BLUE, 4.0)], arrows=_arrows,
                     caption=r"\begin{matrix} " + _names[name] + r" \end{matrix}", box=((-1.4, 1.4), (-1.4, 1.4), (-1.2, 9.6)))

    _fig = turntable(30, 20, "the vector fields F and G in space around the helix, side by side, each with gamma(t), gamma'(t) and the field at gamma(t)",
                     [_panel(_F, "F"), _panel(_G, "G")], height=380, cols=2, key="L19-helix-fields", apart=True)
    mo.vstack([mo.hstack([tf], justify="start"), _fig])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("L19-helix-fields", 380)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given $\gamma : I \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$, &nbsp; $\sigma = \gamma \circ \varphi : \tilde{I} \subseteq \mathbb{R} \longrightarrow \mathbb{R}^3$

    $$
    \int_c^d \vec{F}(\sigma(\tilde{t})) \cdot \sigma'(\tilde{t}) \, d\tilde{t} = \pm \int_a^b \vec{F}(\gamma(t)) \cdot \gamma'(t) \, dt
    $$

    with $\begin{cases} + & \text{if } \varphi'(\tilde{t}) > 0 \text{ for all } \tilde{t} \in \tilde{I} \\ - & \text{if } \varphi'(\tilde{t}) < 0 \text{ for all } \tilde{t} \in \tilde{I} \end{cases}$, &nbsp; where $[a, b] = \varphi([c, d])$.
    """,
        "Line integrals and reparameterization",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\Longrightarrow$ &nbsp; $\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s}$ &nbsp; only depends on $C$ and a choice of orientation of $C$!
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$, $C^1$-smooth and $\vec{C} = \gamma([a, b]) \subset D$ from $\gamma(a)$ to $\gamma(b)$, then

    $$
    \int_{\vec{C}} \vec{\nabla} f \cdot d\vec{s} = f(\gamma(b)) - f(\gamma(a)) \ !
    $$
    """,
        "Line integrals of gradient vector fields",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; line integrals of gradient vector fields only depend on their end points!

    **Proof.**
    <span class="chain">$\displaystyle \int_{\vec{C}} \vec{\nabla} f \cdot d\vec{s} = \int_a^b \vec{\nabla} f(\gamma(t)) \cdot \gamma'(t) \, dt$ $\displaystyle \quad \overset{\mathclap{\footnotesize \text{chain rule}}}{\vphantom{\Bigg|} =} \quad \int_a^b \frac{d}{dt}\big( f(\gamma(t)) \big) \, dt$ $\displaystyle \quad \overset{\mathclap{\footnotesize \text{FTC!}}}{\vphantom{\Bigg|} =} \quad f(\gamma(b)) - f(\gamma(a))$ <span class=qed>$\square$</span></span>

    **Example.** &nbsp; $\vec{G}(x, y, z) = \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \vec{\nabla} g(x, y, z)$, &nbsp; $g(x, y, z) = \dfrac{1}{2}(x^2 + y^2 + z^2)$

    <span class="chain">$\displaystyle \Longrightarrow \quad \int_{\vec{C}} \vec{G} \cdot d\vec{s} = g(\gamma(2\pi)) - g(\gamma(0))$ $\displaystyle = \frac{1}{2}\left( 1 + (2\pi)^2 \right) - \frac{1}{2}(1 + 0) = \frac{(2\pi)^2}{2}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; does $\vec{\nabla} \times \vec{F} = \vec{0}$ imply $\vec{F} = \vec{\nabla} f$?

    **Example.** &nbsp; $\vec{H}(\vec{x}) = \dfrac{1}{x^2 + y^2} \begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}$, &nbsp; $\mathrm{Dom}(\vec{H}) = \{ (x, y, z) \mid x^2 + y^2 \neq 0 \}$

    <span class="chain">$\displaystyle \vec{\nabla} \times \vec{H} = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\[10pt] \dfrac{-y}{x^2 + y^2} & \dfrac{x}{x^2 + y^2} & 0 \end{bmatrix}$ $\displaystyle = \underbrace{\begin{bmatrix} 0 \\ 0 \\[10pt] \dfrac{-x^2 + y^2}{(x^2 + y^2)^2} - \dfrac{y^2 - x^2}{(x^2 + y^2)^2} \end{bmatrix}}_{\footnotesize = \vec{0}}$</span>

    $\vec{C}$ = unit circle in the $xy$-plane, oriented counter-clockwise

    $\leadsto$ &nbsp; $\gamma(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ 0 \end{bmatrix}$ &nbsp; from $t = 0$ to $t = 2\pi$

    $$
    \begin{aligned} \Longrightarrow \quad \int_{\vec{C}} \vec{H} \cdot d\vec{s} &= \int_0^{2\pi} \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 0 \end{bmatrix} \cdot \begin{bmatrix} -\sin(t) \\ \cos(t) \\ 0 \end{bmatrix} dt \\
    &= \int_0^{2\pi} dt = 2\pi \neq 0 = \underbrace{h(\gamma(2\pi)) - h(\gamma(0))}_{\mathclap{\footnotesize \forall \, h : \mathrm{Dom}(\vec{H}) \subseteq \mathbb{R}^3 \to \mathbb{R} \,!}} \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(GREEN, RED, np, panel, turntable):
    # H of the Example on three planes z = -1.2, 0, 1.2, the same on each, with the unit circle C in z = 0. Every arrow at 0.6
    # of its vector, so of length 0.6 / r at the distance r from the z-axis: faint on three rings r = 1.6, 2.2, 2.8 on every plane,
    # strong at eight points of C, which start at 7 degrees so that none crosses the x- or y-axis. The z-axis, not in Dom(H),
    # is dashed over the full height, with an open dot at the origin. The box has its corners at the content's own radius
    _K = 0.6
    _pale = "#a7bfad"  # GREEN halfway to white

    def _H(p):
        return np.array([-p[1], p[0], 0.0]) / (p[0] ** 2 + p[1] ** 2)

    def _ring(r, n, z, turn):
        return [np.array([r * np.cos(a), r * np.sin(a), z]) for a in turn + np.linspace(0, 2 * np.pi, n, endpoint=False)]

    _c = np.linspace(0, 2 * np.pi, 300)
    _faint = [q for z in (-1.2, 0.0, 1.2) for q in _ring(1.6, 12, z, np.pi / 12) + _ring(2.2, 16, z, np.pi / 16) + _ring(2.8, 20, z, np.pi / 20)]
    _arrows = [(q, q + _K * _H(q), _pale, 1.0) for q in _faint] + [(q, q + _K * _H(q), GREEN, 1.8) for q in _ring(1.0, 8, 0.0, np.radians(7))]
    _arrows += [((0, 0, -2.3), (0, 0, 2.3), "#000000", 1.1, [5, 4])]
    _fig = turntable(
        45, 30, "the vector field H on three horizontal planes around the z-axis, with the unit circle C",
        [
            panel(
                1.0,
                lines=[(np.cos(_c), np.sin(_c), 0 * _c, RED, 1.8)],
                axes=[((-3.1, 0, 0), (3.1, 0, 0), "x", -150), ((0, -3.1, 0), (0, 3.1, 0), "y", 0)],
                arrows=_arrows,
                points=[((0, 0, 0), "#000000", 3.5, True)],
                texts=[((0, 0, 2.3), "z", "#000000", 90), ((0.6 * np.cos(-0.785), 0.6 * np.sin(-0.785), 0), r"\vec{C}", RED, 0, 0)],
                caption=r"\textcolor{#4f7f5c}{\vec{H}(\vec{x}) = \dfrac{1}{x^2 + y^2} \begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}}",
                box=((-2.1, 2.1), (-2.1, 2.1), (-1.6, 1.6)),
            )
        ],
        height=480,
        width=550,
        key="L19-H",
    )
    _fig
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    $\vec{F} = \vec{\nabla} f$ if and only if $\displaystyle \int_{\vec{C}} \vec{F} \cdot d\vec{s}$ only depends on the end points of $\vec{C}$, for every oriented curve $\vec{C} \subset D = \mathrm{Dom}(\vec{F})$.

    $\leadsto$ &nbsp; $\vec{F}$ is called a **conservative vector field**
    """,
        "Conservative vector fields",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ① &nbsp; $\gamma(t) = \begin{bmatrix} 2t \\ t^2 \\ \ln(t) \end{bmatrix}$, &nbsp; $t \in [1, e]$

    a) &nbsp; Compute the arc length.

    b) &nbsp; Compute the path integral of $f(x, y, z) = y$ along $\gamma$.

    ② &nbsp; $\vec{G}(x, y, z) = \begin{bmatrix} e^y \\ x e^y + z \\ y \end{bmatrix}$

    a) &nbsp; Check that $g(x, y, z) = x e^y + yz$ is a potential function for $\vec{G}$.

    b) &nbsp; Compute the line integral of $\vec{G}$ along

    &emsp;&emsp;i) &nbsp; $\sigma(t) = \begin{bmatrix} t \\ t \\ t \end{bmatrix}$, &nbsp; $t \in [0, 1]$

    &emsp;&emsp;ii) &nbsp; $\rho(t) = \begin{bmatrix} \cos(t) \\ \sin(t) \\ t \end{bmatrix}$, &nbsp; $t \in [0, 2\pi]$

    from the definition of line integrals.

    Hint: for (b), compute $\dfrac{d}{dt}\big( e^{\sin(t)} \cos(t) \big)$.
    """)
    return


if __name__ == "__main__":
    app.run()
