import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 16 • Method of Lagrange multipliers", css_file="bs101.css")


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

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, definition, header, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 16", "Week 10", "Lecture 16 • Method of Lagrange multipliers")
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
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Existence of global extrema on closed and bounded domains
    """
            ),
            theorem(
                r"""
    If $f : D \subseteq \mathbb{R}^2 \longrightarrow \mathbb{R}$ is continuous over a $\underbrace{\text{closed}}_{\footnotesize \begin{matrix}\text{contains its} \\ \text{boundary}\end{matrix}}$ and $\underbrace{\text{bounded}}_{\footnotesize \begin{matrix}\text{doesn't run off} \\ \text{to infinity}\end{matrix}}$ domain $D \subseteq \mathbb{R}^2$, then $f$ has both global extrema in $D$.
    """,
                "Global extrema on closed and bounded domains",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Strategy:** find all candidates and compare them

    ① &nbsp; in $D \setminus \mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; local extrema &nbsp; $\Longrightarrow$ &nbsp; critical points of $f$: &nbsp; $\vec{x} \in D \setminus \mathrm{Bd}(D)$ such that $\vec{\nabla} f(\vec{x}) = \vec{0}$

    ② &nbsp; in $\mathrm{Bd}(D)$ &nbsp; $\leadsto$ &nbsp; global extrema of $f \circ \gamma$ on $[a, b]$ for some parameterization $\gamma : [a, b] \longrightarrow \mathbb{R}^2$ of $\mathrm{Bd}(D)$, &nbsp; $\mathrm{Im}(\gamma) = \mathrm{Bd}(D)$

    $$
    \Longrightarrow \quad \gamma(t) \in \mathrm{Bd}(D) \quad \text{with} \quad
    \begin{cases} t \in (a, b) \ \text{ and } \ (f \circ \gamma)'(t) = 0 \\ \text{or } \ t = a, b \end{cases}
    $$

    **Example.**

    $$
    f(\vec{x}) = x^2 (x^1 - 2) \quad \text{on} \quad D = \left\{\, \vec{x} \mid (x^1)^2 \leq x^2 \leq 1 \,\right\} = D_1 \cap D_2
    $$

    with &nbsp; $D_1 = \left\{\, \vec{x} \mid (x^1)^2 \leq x^2 \,\right\}$ &nbsp; and &nbsp; $D_2 = \left\{\, \vec{x} \mid x^2 \leq 1 \,\right\}$

    a) &nbsp; Critical points in $D \setminus \mathrm{Bd}(D)$:

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} x^2 \\ x^1 - 2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    \qquad \Longleftrightarrow \qquad \vec{x} = \begin{bmatrix} 2 \\ 0 \end{bmatrix} \notin D \setminus \mathrm{Bd}(D)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, ORANGE, RED, cross_axes, np):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(HALF + 0.4, 2.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-1.75, 3.7)
    _ax.set_ylim(-0.5, 1.85)
    _ax.set_aspect("equal")
    _ax.axis("off")
    # D between the parabola x^2 = (x^1)^2 and the line x^2 = 1
    _s = np.linspace(-1, 1, 201)
    _ax.fill_between(_s, _s**2, 1, color=LIGHT, lw=0, zorder=0)
    _p = np.linspace(-1.3, 1.3, 201)
    _ax.plot(_p, _p**2, color=RED, lw=1.4, zorder=3)
    _ax.plot([-1.55, 1.55], [1, 1], color=ORANGE, lw=1.4, zorder=3)
    cross_axes(_ax, (-1.6, 2.6), (-0.3, 1.8), "$x^1$", "$x^2$")
    for _x, _name in ((-1, "$-1$"), (1, "$1$")):
        _ax.text(_x, -0.07, _name, ha="center", va="top", fontsize=12, bbox=_box)
    _ax.text(2, -0.16, "$2$", ha="center", va="top", fontsize=12, bbox=_box)
    _ax.text(-0.06, 1.04, "$1$", ha="right", va="bottom", fontsize=12, bbox=_box)
    _ax.text(-0.5, 0.62, "$D$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.text(1.42, 1.69, "$x^2 = (x^1)^2$", color=RED, fontsize=12, ha="left", va="center")
    _ax.text(1.6, 1.0, "$x^2 = 1$", color=ORANGE, fontsize=12, ha="left", va="center")
    # the critical point of f, outside D
    _ax.plot(2, 0, "o", color="black", ms=5, zorder=5)
    _ax.annotate(r"$\genfrac{[}{]}{0}{0}{2}{0}$ not a candidate!", (2, 0), textcoords="offset points", xytext=(-3, 5), ha="left", va="bottom", fontsize=12, zorder=6)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    b) &nbsp; Parameterization of $\mathrm{Bd}(D)$:

    parabola: &nbsp; $\gamma(t) = \begin{bmatrix} t \\ t^2 \end{bmatrix}$, &nbsp; $-1 \leq t \leq 1$

    straight segment: &nbsp; $\sigma(t) = \begin{bmatrix} t \\ 1 \end{bmatrix}$, &nbsp; $-1 \leq t \leq 1$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pt = mo.ui.slider(-1, 1, 0.05, value=-0.6, label="$t$", show_value=True)
    return (pt,)


@app.cell(hide_code=True)
def _(FULL, Figure, LIGHT, ORANGE, RED, cross_axes, math, mo, np, pt, tip_label):
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _t = round(pt.value, 10) + 0.0
    _fig = Figure(figsize=(FULL, 2.3), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax in (_left, _right):
        _ax.set_xlim(-1.8, 1.8)
        _ax.set_ylim(-0.45, 1.6)
        _ax.set_aspect("equal")
        _ax.axis("off")
        # D, faintly, so that the two pieces read as its boundary
        _d = np.linspace(-1, 1, 201)
        _ax.fill_between(_d, _d**2, 1, color=LIGHT, lw=0, zorder=0)
        cross_axes(_ax, (-1.5, 1.5), (-0.3, 1.5))
        for _x, _name in ((-1, "$-1$"), (1, "$1$")):
            _ax.text(_x, -0.07, _name, ha="center", va="top", fontsize=12, bbox=_box)

    # the parabola gamma(t) = (t, t^2), -1 <= t <= 1
    _s = np.linspace(-1, 1, 201)
    _left.plot(_s, _s**2, color=RED, lw=1.6, zorder=3)
    _left.text(-0.06, 1.06, "$1$", ha="right", va="bottom", fontsize=12, bbox=_box)
    for _e, _name, _ang in ((-1, r"$\gamma(-1)$", 180), (1, r"$\gamma(1)$", 0)):
        _left.plot(_e, 1, "o", color=RED, ms=5, zorder=4)
        tip_label(_left, (_e, 1), _ang, _name, "black", r=4, fontsize=12)
    _left.plot(_t, _t**2, "o", color="black", ms=5, zorder=5)
    # the name of gamma(t) centred inside the parabola, along its normal (it turns with t and never jumps)
    _c, _s = -2 * _t / math.hypot(2 * _t, 1), 1 / math.hypot(2 * _t, 1)
    _d = 26 / 2 * abs(_c) + 14 / 2 * abs(_s) + 4
    _left.annotate(r"$\gamma(t)$", (_t, _t**2), textcoords="offset points", xytext=(_d * _c, _d * _s), ha="center", va="center", fontsize=12, zorder=6)

    # the straight segment sigma(t) = (t, 1), -1 <= t <= 1
    _right.plot([-1, 1], [1, 1], color=ORANGE, lw=1.6, zorder=3)
    _right.text(-0.06, 1.06, "$1$", ha="right", va="bottom", fontsize=12, bbox=_box)
    for _e, _name, _ang in ((-1, r"$\sigma(-1)$", 180), (1, r"$\sigma(1)$", 0)):
        _right.plot(_e, 1, "o", color=ORANGE, ms=5, zorder=4)
        tip_label(_right, (_e, 1), _ang, _name, "black", r=5, fontsize=12)
    _right.plot(_t, 1, "o", color="black", ms=5, zorder=5)
    _right.annotate(r"$\sigma(t)$", (_t, 1), textcoords="offset points", xytext=(0, -5), ha="center", va="top", fontsize=12, zorder=6)

    mo.vstack([mo.hstack([pt], justify="start"), _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    c) &nbsp; Global extrema of $f \circ \gamma$ and $f \circ \sigma$ on $[-1, 1]$:

    $$
    \begin{aligned}
    f \circ \gamma(t) &= t^2 (t - 2) \\
    f \circ \sigma(t) &= t - 2
    \end{aligned}
    \qquad \leadsto \qquad
    \begin{cases} t \in (-1, 1) & \text{critical points} \\ t = -1 \text{ or } 1 & \text{corner points} \end{cases}
    $$

    - critical points in $(-1, 1)$:

        $$
        \begin{aligned}
        (f \circ \gamma)'(t) &= 3t^2 - 4t = 0 \quad \Longleftrightarrow \quad t = 0 \ \text{ or } \ t = \frac{4}{3} > 1 \\
        &\Longrightarrow \quad \vec{a} = \gamma(0) = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \in \mathrm{Bd}(D) \qquad (\text{one candidate}) \\[0.6em]
        (f \circ \sigma)'(t) &= 1 \neq 0 \quad \forall\, t \in (-1, 1) \qquad (\text{no candidates})
        \end{aligned}
        $$

    - corner points:

        $$
        \begin{aligned}
        \gamma(-1) = \sigma(-1) & = \begin{bmatrix} -1 \\ 1 \end{bmatrix} = \vec{b} \in \mathrm{Bd}(D) \\[1em]
        \gamma(1) = \sigma(1) & = \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \vec{c} \in \mathrm{Bd}(D)
        \end{aligned}
        \qquad (\text{two candidates})
        $$

    d) &nbsp; Compare:

    $$
    \underbrace{f(\vec{a}) = 0}_{\mathclap{\footnotesize \text{global max}}\vphantom{\footnotesize \text{global max}}}, \qquad
    \underbrace{f(\vec{b}) = -3}_{\mathclap{\footnotesize \text{global min}}\vphantom{\footnotesize \text{global min}}}, \qquad
    f(\vec{c}) = -1
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, ORANGE, RED, cross_axes, mo, np, panel, sheet, tip_label, turntable):
    # graph(f) over D, the same rule over a larger square in a faint grey (with the saddle at [2; 0]), D in the plane,
    # the boundary pieces lifted onto the graph, and the candidates
    def _f(x1, x2):
        return x2 * (x1 - 2)

    _s = np.linspace(-1, 1, 41)
    _S, _U = np.meshgrid(_s, np.linspace(0, 1, 11), indexing="ij")
    _d1, _d2 = _S, _S**2 + _U * (1 - _S**2)  # D = {(x^1)^2 <= x^2 <= 1}
    # the box x^1 in [-1.3, 2.4], x^2 in [-0.4, 1.3] around D and [2; 0], in four pieces outside D (light grey), cut by the box edges
    def _strip(x1, lo, hi, n=12):
        w = np.linspace(0, 1, n)[None, :]
        return x1[:, None] + 0 * w, lo + w * (hi - lo)

    _l = np.linspace(-1.3, -1, 4)
    _r = np.linspace(1, 2.4, 15)
    _e = np.linspace(0, 1, 60)
    _pieces = []
    for _x, _y in (
        _strip(_l, -0.4, 1.3),
        _strip(_r, -0.4, 1.3),
        _strip(_s, -0.4, (_s**2)[:, None], 6),
        _strip(_s, 1.0, 1.3, 4),
    ):
        _pieces.append(sheet(_x, _y, _f(_x, _y), tone=GREY, alpha=0.45))

    # one mesh over the whole graph: the lines x^1 = const and x^2 = const (every 0.25), grey outside D, blue over D
    def _piece(x1, x2, colour):
        return (x1, x2, _f(x1, x2), colour, 0.5)

    _mesh = []
    for _k in np.arange(-1.25, 2.4, 0.25):
        if -1 < _k < 1:
            _lo, _hi = _k**2, 1.0
            _mesh += [_piece(_k + 0 * _e, -0.4 + _e * (_lo + 0.4), "#c8c8c8"), _piece(_k + 0 * _e, _lo + _e * (_hi - _lo), BLUE), _piece(_k + 0 * _e, 1 + 0.3 * _e, "#c8c8c8")]
        else:
            _mesh += [_piece(_k + 0 * _e, -0.4 + 1.7 * _e, "#c8c8c8")]
    for _k in np.arange(-0.25, 1.3, 0.25):
        if 0 < _k < 1:
            _w = _k**0.5
            _mesh += [_piece(-1.3 + _e * (1.3 - _w), _k + 0 * _e, "#c8c8c8"), _piece(-_w + 2 * _w * _e, _k + 0 * _e, BLUE), _piece(_w + _e * (2.4 - _w), _k + 0 * _e, "#c8c8c8")]
        elif abs(_k - 1) > 1e-9:
            _mesh += [_piece(-1.3 + 3.7 * _e, _k + 0 * _e, "#c8c8c8")]
    # the border of the grey surface: the edges of the box lifted onto the graph
    _border = []
    for _p, _q in (((-1.3, -0.4), (2.4, -0.4)), ((2.4, -0.4), (2.4, 1.3)), ((2.4, 1.3), (-1.3, 1.3)), ((-1.3, 1.3), (-1.3, -0.4))):
        _bx, _by = _p[0] + _e * (_q[0] - _p[0]), _p[1] + _e * (_q[1] - _p[1])
        _border.append((_bx, _by, _f(_bx, _by), "#8a8a8a", 1.0))
    _a, _b, _c = (0, 0, 0), (-1, 1, -3), (1, 1, -1)
    _drops = [((-1, 1, 0), (-1, 1, -3)), ((1, 1, 0), (1, 1, -1))]
    _graph = turntable(
        75,
        22,
        "graph of f over D and, in light grey, over a box around D with the saddle point at [2; 0]; D in the plane with its boundary dashed; f along the parabola and along the segment of the boundary of D; and the candidates a, b, c",
        [
            panel(
                0.5,
                surfaces=[sheet(_d1, _d2, 0 * _d1, flat="#c6d8ee", alpha=0.9), sheet(_d1, _d2, _f(_d1, _d2))] + _pieces,
                lines=[(_s, _s**2, _f(_s, _s**2), RED, 2.4, None, 0.4), (_s, 1 + 0 * _s, _f(_s, 1), ORANGE, 2.4, None, 0.4)]
                + [(_s, _s**2, 0 * _s, BLUE, 1.2, [4, 3], 0.2), (_s, 1 + 0 * _s, 0 * _s, BLUE, 1.2, [4, 3], 0.2)]  # the boundary of D in the plane
                + [(np.linspace(_p[0], _q[0], 20), np.linspace(_p[1], _q[1], 20), np.linspace(_p[2], _q[2], 20), "#555555", 1.3, [1, 3], 0.3) for _p, _q in _drops]
                + _border + _mesh,
                points=[(_a, "#000000"), (_b, "#000000"), (_c, "#000000"), ((2, 0, 0), "#000000")],
                axes=[((0, 0, 0), (2.7, 0, 0), "x^1", -120), ((0, 0, 0), (0, 0.85, 0), "x^2", 0), ((0, 0, 0), (0, 0, 1.8), "y", 90)],
                texts=[
                    (_a, r"f(\vec{a}) = 0, \ \text{global max}", "#000000", 150, 10),
                    (_b, r"\begin{matrix} f(\vec{b}) = -3, \\ \text{global min} \end{matrix}", "#000000", 0, 40),
                    (_c, r"f(\vec{c}) = -1", "#000000", -140, 26),
                    ((2, 0, 0), r"\begin{matrix} \vec{\nabla} f\left( \begin{bmatrix} 2 \\ 0 \end{bmatrix} \right) = \vec{0}, \\ \text{not a candidate!} \end{matrix}", "#000000", 90, 50),
                    ((0.55, 0.75, 0), "D", BLUE, 90, 0),
                    ((0.75, 0.5625, -0.703), r"f(\gamma(t))", RED, 160, 18),
                    ((0, 1, -2), r"f(\sigma(t))", ORANGE, -100, 60),
                    ((-1.15, 0.5, -1.65), r"y = f(\vec{x})", "#000000", 150, 22),
                ],
                box=((-1.2, 2.2), (-0.3, 1.2), (-2.9, 1.1)),  # sized to D and [2; 0]; the faint box may reach past it
            )
        ],
        height=440,
        key="L16-ex",
    )

    # f along the two pieces as functions of t, with the candidate values
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(HALF + 0.6, 3.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-1.6, 2.35)
    _ax.set_ylim(-3.75, 0.75)
    _ax.axis("off")
    cross_axes(_ax, (-1.35, 1.45), (-3.5, 0.65), "$t$", "$y$")
    _ax.plot(_s, _s**2 * (_s - 2), color=RED, lw=1.6, zorder=3)
    _ax.plot(_s, _s - 2, color=ORANGE, lw=1.6, zorder=3)
    for _y in (-1, -3):
        _ax.plot([-0.04, 0.04], [_y, _y], color="black", lw=0.9)
        _ax.text(0.07, _y, f"${_y}$", ha="left", va="center", fontsize=11, bbox=_box)
    for _x in (-1, 1):
        _ax.plot([_x, _x], [-0.06, 0.06], color="black", lw=0.9)
        _ax.text(_x, 0.12, f"${_x}$", ha="center", va="bottom", fontsize=11, bbox=_box)
    _ax.text(1.08, -0.55, r"$y = f \circ \gamma(t)$", color=RED, fontsize=12, ha="left", va="center")
    _ax.text(0.2, -2.15, r"$y = f \circ \sigma(t)$", color=ORANGE, fontsize=12, ha="left", va="top")
    for _p, _name, _ang in (((0, 0), r"$f(\vec{a}) = 0$", 135), ((-1, -3), r"$f(\vec{b}) = -3$", -60), ((1, -1), r"$f(\vec{c}) = -1$", -40)):
        _ax.plot(*_p, "o", color="black", ms=5, zorder=5)
        tip_label(_ax, _p, _ang, _name, "black", r=5, fontsize=12)

    mo.vstack(
        [
            mo.Html(
                '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
                f'<div style="flex: 1.3 1 440px; min-width: 300px;">{_graph.text}</div>'
                f'<div style="flex: 1 1 300px; min-width: 260px; max-width: 420px;">{mo.as_html(_fig).text}</div></div>'
            ),
            # one block, so that the two lines keep the spacing of normal text
            mo.Html("<div>" + mo.md(
                r"""
    **In this lecture:** constraints and the method of Lagrange multipliers

    **References:** MT 3.4
    """
            ).text + "</div>"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## III.3 &nbsp; Method of Lagrange multipliers

    $\leadsto$ &nbsp; parameterizing $\mathrm{Bd}(D)$ is generally hard…

    $\leadsto$ &nbsp; describing $\mathrm{Bd}(D)$ with level sets is much easier!

    **Example.** &nbsp; $D = \left\{\, \vec{x} \mid (x^1)^2 \leq x^2 \leq 1 \,\right\}$

    $$
    \mathrm{Bd}(D) = \Big\{\, \vec{x} \mid \overbrace{(x^1)^2 = x^2}^{\mathclap{\footnotesize \begin{matrix}\text{level set of } g(\vec{x}) = (x^1)^2 - x^2 \\ (x^1)^2 - x^2 = 0 \rule[-7pt]{0pt}{7pt}\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{level set of } g(\vec{x}) = (x^1)^2 - x^2 \\ (x^1)^2 - x^2 = 0 \rule[-7pt]{0pt}{7pt}\end{matrix}}}, \ x^2 \leq 1 \,\Big\} \cup \Big\{\, \vec{x} \mid \underbrace{x^2 = 1}_{\mathclap{\footnotesize \begin{matrix}\text{level set of} \\ h(\vec{x}) = x^2\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{level set of} \\ h(\vec{x}) = x^2\end{matrix}}}, \ -1 \leq x^1 \leq 1 \,\Big\}
    $$

    $\leadsto$ &nbsp; Lagrange multipliers allow us to find extrema of one function on the level sets of another &nbsp; $\Longrightarrow$ &nbsp; no parameterizations needed!
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    A **constraint** is an $\underbrace{\text{equation } g(\vec{x}) = c}_{\mathclap{\footnotesize \text{constraint equation} \rule[-8pt]{0pt}{8pt}}\vphantom{\footnotesize \text{constraint equation} \rule[-8pt]{0pt}{8pt}}}$, restricting the allowed values of $\vec{x}$ to the $\underbrace{\text{level set } g^{-1}(c)}_{\mathclap{\footnotesize \text{constraint curve} \rule[-8pt]{0pt}{8pt}}\vphantom{\footnotesize \text{constraint curve} \rule[-8pt]{0pt}{8pt}}}$ of some $\underbrace{\text{function } g : \mathbb{R}^2 \longrightarrow \mathbb{R}}_{\mathclap{\footnotesize \text{constraint function} \rule[-8pt]{0pt}{8pt}}\vphantom{\footnotesize \text{constraint function} \rule[-8pt]{0pt}{8pt}}}$.
    """,
                "Constraint",
            ),
            mo.md(
                r"""
    **Problem.** Given a function $f : \mathbb{R}^2 \longrightarrow \mathbb{R}$ and a constraint $g(\vec{x}) = c$, how to find max / min of $f$ restricted to the constraint curve $g^{-1}(c)$?
    """
            ).style({"margin-top": "0.75rem"}),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    fx = mo.ui.slider(0, 50, 0.5, value=10, label="$x^1$", show_value=True)
    return (fx,)


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, fx, mo, num, table):
    # the rectangle with perimeter 100 at true proportions, x^2 = 50 - x^1, in a fixed window
    _x1 = round(fx.value, 10) + 0.0
    _x2 = 50 - _x1
    _fig = Figure(figsize=(2.3, 2.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-5, 60)
    _ax.set_ylim(-7, 55)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.fill([0, _x1, _x1, 0], [0, 0, _x2, _x2], color=LIGHT, lw=0)
    _ax.plot([0, _x1, _x1, 0, 0], [0, 0, _x2, _x2, 0], color=BLUE, lw=1.4)
    _ax.text(_x1 / 2, -1.5, "$x^1$", ha="center", va="top", fontsize=13)
    _ax.text(_x1 + 1.5, _x2 / 2, "$x^2$", ha="left", va="center", fontsize=13)
    _readout = table(
        [
            (r"$x^1$", rf"${num(_x1)}$"),
            (r"$x^2 = 50 - x^1$", rf"${num(_x2)}$"),
            (r"$\text{area} = x^1 x^2$", rf"${num(_x1 * _x2)}$"),
        ]
    )

    _cases = mo.md(
        r"""
    $$
    \leadsto \quad
    \begin{cases}
    f(\vec{x}) = \text{area} = x^1 x^2 \\[1.2em]
    g(\vec{x}) = \text{perimeter} = \underbrace{2x^1 + 2x^2 = 100}_{\mathclap{\footnotesize \text{constraint}}\vphantom{\footnotesize \text{constraint}}}
    \end{cases}
    $$
    """
    )

    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** &nbsp; Suppose you want to build a fence around some rectangular region. The fence must have perimeter 100 m. How to maximize the area?
    """
            ),
            mo.hstack([fx], justify="start"),
            mo.Html(
                '<div style="display: flex; align-items: center; gap: 0.5rem 1.5rem;">'
                f'<div style="flex: 0 0 auto;">{mo.as_html(_fig).text}{_readout.text}</div>'
                f'<div style="flex: 0 1 auto; min-width: 0;">{_cases.text}</div></div>'
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    Given $f, g : \mathbb{R}^2 \longrightarrow \mathbb{R}$, a point $\vec{a} \in g^{-1}(c)$ is a **global maximum of $f$ restricted to $g^{-1}(c)$** if

    $$
    f(\vec{a}) \geq f(\vec{x}) \qquad \forall\, \vec{x} \in g^{-1}(c)
    $$
    """,
                "Global maximum restricted to a constraint curve",
            ),
            theorem(
                r"""
    Given $f, g : \mathbb{R}^2 \longrightarrow \mathbb{R}$ $C^1$-smooth, if $\vec{a}$ is a global extremum of $f$ restricted to $g^{-1}(c)$ with $\vec{\nabla} g(\vec{a}) \neq \vec{0}$, then

    $$
    \underbrace{\text{there exists } \lambda \in \mathbb{R} \text{ such that } \vec{\nabla} f(\vec{a}) = \lambda \vec{\nabla} g(\vec{a})}_{\mathclap{\footnotesize \vec{\nabla} f(\vec{a}) \text{ is proportional to } \vec{\nabla} g(\vec{a})}\vphantom{\footnotesize \vec{\nabla} f(\vec{a}) \text{ is proportional to } \vec{\nabla} g(\vec{a})}}
    $$

    $\leadsto$ &nbsp; $\lambda$ is called a **Lagrange multiplier**
    """,
                "Lagrange multipliers",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof.** Given $\vec{a} \in g^{-1}(c)$, a global maximum of $f$ restricted to $g^{-1}(c)$, with $\vec{\nabla} g(\vec{a}) \neq \vec{0}$, we can

    ① &nbsp; find a parameterization $\gamma(t)$ of $g^{-1}(c)$ near $\vec{a}$ such that $\gamma(0) = \vec{a}$ and $\gamma'(0) \neq \vec{0}$

    &emsp;&emsp; $\leadsto$ &nbsp; exists because $\vec{\nabla} g(\vec{a}) \neq \vec{0}$ &nbsp; (big theorem we cannot prove!)

    ② &nbsp; evaluate both $f$ and $g$ along $\gamma(t)$ and differentiate at $t = 0$

    - $\vec{a}$ is a max of $f$ restricted to $g^{-1}(c)$

        $$
        \begin{aligned}
        & \Longrightarrow \quad 0 \text{ is a max of } f \circ \gamma \\
        & \Longrightarrow \quad \left. \frac{d}{dt} \right|_{t = 0} f(\gamma(t)) = \vec{\nabla} f(\vec{a}) \cdot \gamma'(0) = 0
        \end{aligned}
        $$

    - $\gamma$ is a parameterization of $g^{-1}(c)$

        $$
        \begin{aligned}
        & \Longrightarrow \quad g \circ \gamma = c \text{ is constant} \\
        & \Longrightarrow \quad \left. \frac{d}{dt} \right|_{t = 0} g(\gamma(t)) = \vec{\nabla} g(\vec{a}) \cdot \gamma'(0) = 0
        \end{aligned}
        $$

    ③ &nbsp; $\vec{\nabla} f(\vec{a})$ and $\vec{\nabla} g(\vec{a})$ are orthogonal to $\gamma'(0) \neq \vec{0}$ in $\mathbb{R}^2$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{\nabla} f(\vec{a})$ and $\vec{\nabla} g(\vec{a})$ must be proportional!

    $$
    \Longrightarrow \qquad \vec{\nabla} f(\vec{a}) = \lambda \vec{\nabla} g(\vec{a}) \quad \text{for some } \lambda \in \mathbb{R} \tag*{$\square$}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $f(\vec{x}) = (x^1)^2 + (x^2)^2$, &nbsp; $g(\vec{x}) = (x^1)^2 + x^1 x^2 + (x^2)^2 = 3$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} 2x^1 \\ 2x^2 \end{bmatrix}, \qquad
    \vec{\nabla} g(\vec{x}) = \begin{bmatrix} 2x^1 + x^2 \\ 2x^2 + x^1 \end{bmatrix}
    $$

    $\vec{\nabla} g(\vec{x}) \neq \vec{0} \ \ \forall\, \vec{x} \neq \vec{0}$, &nbsp; and $\vec{0} \notin g^{-1}(3)$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    lk = mo.ui.slider(1, 7, 0.5, value=6, label="$k$", show_value=True)
    return (lk,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, RED, arrow, cross_axes, lk, math, mo, np, panel, sheet, tip_label, turntable):
    # the circle f = k (radius sqrt k) with g^{-1}(3); at k = 2 and k = 6 it touches the ellipse, and then the
    # gradients there are drawn (all at the same scale K), as on the page
    _c = round(lk.value, 10)
    _K = 0.25
    _r3 = math.sqrt(3)
    _th = np.linspace(0, 2 * np.pi, 361)
    _fig = Figure(figsize=(HALF + 0.6, 3.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-4.9, 4.3)
    _ax.set_ylim(-3.55, 3.6)
    _ax.set_aspect("equal")
    _ax.axis("off")
    cross_axes(_ax, (-3.0, 3.4), (-2.9, 3.0), "$x^1$", "$x^2$")
    # the ellipse (x^1)^2 + x^1 x^2 + (x^2)^2 = 3: half axes sqrt(6) along (1, -1) and sqrt(2) along (1, 1)
    _u, _v = math.sqrt(6) * np.cos(_th), math.sqrt(2) * np.sin(_th)
    _ax.plot((_u + _v) / math.sqrt(2), (-_u + _v) / math.sqrt(2), color=BLUE, lw=1.6, zorder=3)
    _ax.plot(math.sqrt(_c) * np.cos(_th), math.sqrt(_c) * np.sin(_th), color=RED, lw=1.2, zorder=2)
    # the name of the ellipse beside it, fixed; the name of the circle beside it, moving with it (lower left)
    # names placed where, at k = 2 and k = 6, they touch no curve, arrow or other name (found by a search over the figure):
    # the ellipse's above its upper end, fixed; the circle's outside it at 63 degrees, moving with it
    _ax.text(-1.75, 2.75, r"$g^{-1}(3)$", ha="center", va="center", color=BLUE, fontsize=12)
    _w = math.radians(63)
    _ax.text((math.sqrt(_c) + 1.0) * math.cos(_w), (math.sqrt(_c) + 1.0) * math.sin(_w), r"$f(\vec{x}) = k$", ha="center", va="center", color=RED, fontsize=12)

    def _out(p, k):
        return (p[0] + k * p[0], p[1] + k * p[1])

    # grad f = 2x, grad g = (2x^1 + x^2, 2x^2 + x^1): at k = 6 grad g = x (lambda = 2), at k = 2 grad g = 3x / 2 (lambda = 2/3)
    _v3 = r"\sqrt{3}"
    if _c == 6:
        _P, _Q = (_r3, -_r3), (-_r3, _r3)
        for _p in (_P, _Q):
            arrow(_ax, _p, _out(_p, 2 * _K), RED, lw=1.4)
        for _p in (_P, _Q):  # grad g on top of grad f = 2 grad g: its head halfway along grad f
            arrow(_ax, _p, _out(_p, _K), BLUE, lw=1.4)
            _ax.plot(*_p, "o", color=RED, ms=5, zorder=5)
        tip_label(_ax, _out(_Q, 2 * _K), 180, rf"$\vec{{\nabla}} f\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{-{_v3}}}{{{_v3}}}\right)$", RED, r=3, fontsize=12)
        # below-left of the point, outside the circle, away from both arrows
        _ax.text(-2.6, 1.45, rf"$\vec{{\nabla}} g\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{-{_v3}}}{{{_v3}}}\right)$", color=BLUE, fontsize=12, ha="right", va="top")
        tip_label(_ax, _out(_P, 2 * _K), -90, rf"$\vec{{\nabla}} f\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{{_v3}}}{{-{_v3}}}\right)$", RED, r=9, fontsize=12)
        tip_label(_ax, _out(_P, _K), 30, rf"$\vec{{\nabla}} g\left(\genfrac{{[}}{{]}}{{0}}{{0}}{{{_v3}}}{{-{_v3}}}\right)$", BLUE, r=5, fontsize=12)
    elif _c == 2:
        _A, _B = (1.0, 1.0), (-1.0, -1.0)
        for _p in (_A, _B):  # grad g = 3/2 grad f is longer: drawn first, grad f on top of its first part
            arrow(_ax, _p, _out(_p, 3 * _K), BLUE, lw=1.4)
        for _p in (_A, _B):
            arrow(_ax, _p, _out(_p, 2 * _K), RED, lw=1.4)
            _ax.plot(*_p, "o", color=RED, ms=5, zorder=5)
        tip_label(_ax, _out(_A, 2 * _K), -30, r"$\vec{\nabla} f\left(\genfrac{[}{]}{0}{0}{1}{1}\right)$", RED, r=4, fontsize=12)
        tip_label(_ax, _out(_A, 3 * _K), 30, r"$\vec{\nabla} g\left(\genfrac{[}{]}{0}{0}{1}{1}\right)$", BLUE, r=8, fontsize=12)
        tip_label(_ax, _out(_B, 2 * _K), 150, r"$\vec{\nabla} f\left(\genfrac{[}{]}{0}{0}{-1}{-1}\right)$", RED, r=4, fontsize=12)
        tip_label(_ax, _out(_B, 3 * _K), -90, r"$\vec{\nabla} g\left(\genfrac{[}{]}{0}{0}{-1}{-1}\right)$", BLUE, r=4, fontsize=12)

    # graph(f) over a disc, the ellipse in the plane and its lift onto the graph, the plane y = c (edge only) and its cut
    def _f(x1, x2):
        return x1**2 + x2**2

    _R = 2.7  # holds the circle f = c up to c = 7
    _rr, _pp = np.meshgrid(np.linspace(0, _R, 15), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _e1, _e2 = (_u + _v) / math.sqrt(2), (-_u + _v) / math.sqrt(2)
    _ring = (_R * np.cos(_th), _R * np.sin(_th))
    _sq = [(-_R, -_R, _c), (_R, -_R, _c), (_R, _R, _c), (-_R, _R, _c)]
    # starting view azimuth 45: x^1 and x^2 both come towards the viewer, below the graph; the screen's right is (-1, 1)/sqrt 2.
    # The lift is named beside its highest point on the right, (-sqrt 3, sqrt 3, 6); the plane y = k beside its left corner
    _top = (-math.sqrt(3), math.sqrt(3), 6.0)
    _graph = turntable(
        45,
        25,
        "graph of f over a disc, the ellipse g^{-1}(3) in the plane and lifted onto the graph, and the plane y = k cutting the graph along the circle f = k",
        [
            panel(
                0.4,
                surfaces=[sheet(_rr * np.cos(_pp), _rr * np.sin(_pp), _f(_rr * np.cos(_pp), _rr * np.sin(_pp)), wire=[(0, 2, BLUE, 0.4), (1, 8, BLUE, 0.4)], alpha=0.85)],
                lines=[(_ring[0], _ring[1], _f(*_ring), BLUE, 1.0), (_e1, _e2, 0 * _e1, BLUE, 1.0, [4, 3]), (_e1, _e2, _f(_e1, _e2), BLUE, 2.4),
                       (math.sqrt(_c) * np.cos(_th), math.sqrt(_c) * np.sin(_th), _c + 0 * _th, RED, 2.4)]
                + [(np.linspace(_a[0], _b[0], 60), np.linspace(_a[1], _b[1], 60), np.full(60, _c), GREY, 1.2) for _a, _b in zip(_sq, _sq[1:] + _sq[:1])],
                axes=[((0, 0, 0), (3.3, 0, 0), "x^1", -90), ((0, 0, 0), (0, 3.3, 0), "x^2", -90), ((0, 0, 0), (0, 0, 11.0), "y", 90)],
                texts=[
                    (_top, r"\begin{matrix} \text{graph of } f \text{ restricted} \\ \text{to } g^{-1}(3) \end{matrix}", BLUE, 0, 75),
                    ((1, 1, 0), r"g^{-1}(3)", BLUE, -90, 6),
                    (_sq[1], r"y = k", GREY, 180, 6),
                ],
                box=((-3.6, _R), (-_R, 3.6), (0, 11.0)),  # room on the right for the name of the lift, and for the y axis above the bowl
            )
        ],
        height=420,
        key="L16-c",
    )

    mo.vstack(
        [
            mo.hstack([lk], justify="start"),
            mo.Html(
                '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
                f'<div style="flex: 1 1 340px; min-width: 300px; max-width: 480px;">{mo.as_html(_fig).text}</div>'
                f'<div style="flex: 1.2 1 440px; min-width: 300px;">{_graph.text}</div></div>'
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{aligned}
    \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\ g(\vec{x}) = 3 \end{cases}
    \quad & \Longleftrightarrow \quad
    \begin{cases} 2x^1 = \lambda (2x^1 + x^2) \\ 2x^2 = \lambda (2x^2 + x^1) \\ (x^1)^2 + x^1 x^2 + (x^2)^2 = 3 \end{cases} \\[2.8em]
    & \Longleftrightarrow \quad
    \begin{cases} (2 - \lambda)(x^1 - x^2) = 0 \\ (2 - 3\lambda)(x^1 + x^2) = 0 \\ (x^1)^2 + x^1 x^2 + (x^2)^2 = 3 \end{cases} \\[2.8em]
    & \Longleftrightarrow \quad
    \begin{cases} \lambda = 2, \quad x^2 = -x^1, \quad (x^1)^2 = 3 \\[0.6em] \lambda = \dfrac{2}{3}, \quad x^2 = x^1, \quad 3(x^1)^2 = 3 \end{cases} \\[3em]
    & \Longleftrightarrow \quad
    \begin{cases} \lambda = 2, \quad \vec{x} = \pm \begin{bmatrix} \sqrt{3} \\ -\sqrt{3} \end{bmatrix} \\[1.2em] \lambda = \dfrac{2}{3}, \quad \vec{x} = \pm \begin{bmatrix} 1 \\ 1 \end{bmatrix} \end{cases}
    \end{aligned}
    $$

    ### New strategy if $\mathrm{Bd}(D) = g^{-1}(c)$

    ②$'$ &nbsp; $\leadsto$ &nbsp; constrained extrema

    $$
    \Longrightarrow \qquad \vec{x} \in \mathrm{Bd}(D) \quad \text{such that} \quad
    \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\ g(\vec{x}) = c \end{cases}
    $$

    $\leadsto$ &nbsp; solve for $\vec{x}$ and $\lambda$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** If $\mathrm{Bd}(D)$ has multiple components, use one constraint per component and include the corners!

    **Example.** &nbsp; $f(\vec{x}) = x^2 (x^1 - 2)$, &nbsp; $D = \left\{\, \vec{x} \mid (x^1)^2 \leq x^2 \leq 1 \,\right\}$

    $$
    \mathrm{Bd}(D) = \{ \vec{x} \mid g(\vec{x}) = 0, \ 0 \leq x^2 \leq 1 \} \cup \{ \vec{x} \mid h(\vec{x}) = 1, \ -1 \leq x^1 \leq 1 \}
    $$

    with &nbsp; $g(\vec{x}) = (x^1)^2 - x^2$ &nbsp; and &nbsp; $h(\vec{x}) = x^2$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} x^2 \\ x^1 - 2 \end{bmatrix}, \qquad
    \vec{\nabla} g(\vec{x}) = \begin{bmatrix} 2x^1 \\ -1 \end{bmatrix}, \qquad
    \vec{\nabla} h(\vec{x}) = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\ g(\vec{x}) = 0 \end{cases}
    \quad & \Longleftrightarrow \quad
    \begin{cases} x^2 = 2\lambda x^1 \\ x^1 - 2 = -\lambda \\ (x^1)^2 - x^2 = 0 \end{cases} \\[2.8em]
    & \Longleftrightarrow \quad
    \begin{cases} \lambda = 2, \quad \vec{x} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \vphantom{\underbrace{\begin{bmatrix} 0 \\ 0 \end{bmatrix}}_{\footnotesize \text{not}}} \\[1.2em]
    \lambda = \dfrac{2}{3}, \quad \underbrace{\vec{x} = \begin{bmatrix} \tfrac{4}{3} \\[0.3em] \tfrac{16}{9} \end{bmatrix}}_{\mathclap{\footnotesize \text{not on } \mathrm{Bd}(D)}\vphantom{\footnotesize \text{not on } \mathrm{Bd}(D)}} \end{cases}
    \end{aligned}
    $$

    $$
    \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} h(\vec{x}) \\ h(\vec{x}) = 1 \end{cases}
    \qquad \Longleftrightarrow \qquad
    \begin{cases} x^2 = 0 \\ x^1 - 2 = \lambda \\ x^2 = 1 \end{cases}
    \qquad \text{no solution!}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    $$
    f(\vec{x}) = x^1 + x^2, \qquad g(\vec{x}) = (x^1)^2 + 4(x^2)^2 = 20
    $$

    a) &nbsp; Find all solutions of

    $$
    \begin{cases} \vec{\nabla} f(\vec{x}) = \lambda \vec{\nabla} g(\vec{x}) \\ g(\vec{x}) = 20 \end{cases}
    $$

    b) &nbsp; Find the global max / min of $f$ restricted to $g^{-1}(20)$.
    """)
    return


if __name__ == "__main__":
    app.run()
