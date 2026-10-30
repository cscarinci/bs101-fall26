import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 03 • Matrices, linear transformations, and determinants", css_file="bs101.css")


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
    header("Lecture 03", "Week 02", "Lecture 03 • Matrices, linear transformations, and determinants")
    return


@app.cell(hide_code=True)
def _(arrow):
    def vector(ax, tail, tip, color, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length)."""
        if tip[0] == tail[0] and tip[1] == tail[1]:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
        else:
            arrow(ax, tail, tip, color, **kw)

    def name_tip(ax, tail, tip, name, color, away=None):
        """The name of the vector from `tail` to `tip`, beside its tip: beyond the tip, or to the side of the arrow
        away from the direction `away`."""
        v = (tip[0] - tail[0], tip[1] - tail[1])
        d = v if away is None else (-v[1], v[0])
        if away is not None and d[0] * away[0] + d[1] * away[1] > 0:
            d = (-d[0], -d[1])
        r = (d[0] ** 2 + d[1] ** 2) ** 0.5
        d = (d[0] / r, d[1] / r) if r else (1, 0)
        ax.annotate(name, tip, textcoords="offset points", xytext=(9 * d[0], 9 * d[1]), color=color, fontsize=13,
                    ha="left" if d[0] > 0.3 else "right" if d[0] < -0.3 else "center", va="bottom" if d[1] > 0.3 else "top" if d[1] < -0.3 else "center")

    return name_tip, vector


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
def _(BLUE, GREEN, GREY, HALF, RED, arrow, blank, mo):
    _fig, _ax = blank(HALF, 2.0, (-0.3, 3.6), (-0.6, 2.2))
    _ax.plot([2, 2], [0, 1.8], color=GREY, lw=1.0, ls=(0, (4, 3)))
    arrow(_ax, (0, 0), (3, 0), RED)
    arrow(_ax, (0, 0), (2, 0), GREEN)
    arrow(_ax, (0, 0), (2, 1.8), BLUE)
    _ax.text(2.08, 1.88, r"$\vec{x}$", color=BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(3.1, 0, r"$\vec{u}$", color=RED, fontsize=13, ha="left", va="center")
    _ax.text(1.0, -0.14, r"$a\vec{u} = \mathrm{proj}_{\vec{u}}(\vec{x})$", color=GREEN, fontsize=13, ha="center", va="top")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - dot product in $\mathbb{R}^n$: &nbsp; $\cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}$, &nbsp; $\vec{x} \cdot \vec{y} = x^1 y^1 + x^2 y^2 + \dots + x^n y^n$
    - norm / length $\lVert \vec{x} \rVert = \sqrt{\vec{x} \cdot \vec{x}}$ &nbsp; and angle $\theta(\vec{x}, \vec{y}) = \arccos\!\left( \dfrac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \right)$ &nbsp; (only when $\vec{x}, \vec{y} \neq \vec{0}$)
    - in-class practice Q3: given $\vec{u}, \vec{v}, \vec{w} \in \mathbb{R}^3$ pairwise orthogonal, all non-zero (**orthogonal frame**), we can write $\vec{x} \in \mathbb{R}^3$ as $\vec{x} = a\vec{u} + b\vec{v} + c\vec{w}$ where

        $$
        a = \dfrac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}, \quad b = \dfrac{\vec{x} \cdot \vec{v}}{\lVert \vec{v} \rVert^2}, \quad c = \dfrac{\vec{x} \cdot \vec{w}}{\lVert \vec{w} \rVert^2}
        $$
    - $a\vec{u} = \dfrac{\vec{x} \cdot \vec{u}}{\lVert \vec{u} \rVert^2}\, \vec{u} = \mathrm{proj}_{\vec{u}}(\vec{x})$ &nbsp; (orthogonal projection of $\vec{x}$ onto the $\vec{u}$ direction)
    - $\Longrightarrow$ &nbsp; $\vec{x} = \mathrm{proj}_{\vec{u}}(\vec{x}) + \mathrm{proj}_{\vec{v}}(\vec{x}) + \mathrm{proj}_{\vec{w}}(\vec{x})$: any vector in $\mathbb{R}^3$ decomposes as the sum of orthogonal projections onto an orthogonal frame!
    """
            ),
            _fig,
            mo.md(r"""**In this lecture:** the standard basis as preferred orthogonal frame, matrices, linear transformations and determinants

            **References:** MT 1.3, 1.5""").style({"display": "block"}),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, definition, mo, np, panel, turntable):
    _p = (1.4, 2.0, 1.7)
    _s = np.linspace(0, 1, 40)
    _feet = [(_p[0], 0, 0), (0, _p[1], 0), (0, 0, _p[2])]
    # x drops to the x^1 x^2 plane, then to the x^1 and x^2 axes; and across to the x^3 axis
    _guides = [(_p, (_p[0], _p[1], 0)), ((_p[0], _p[1], 0), _feet[0]), ((_p[0], _p[1], 0), _feet[1]), (_p, _feet[2])]
    # each axis is left out from the origin to the foot of x^i e_i, so that the axis never covers the arrows;
    # the shafts of the x^i e_i lie behind the e_i
    _fig = turntable(
        30,
        22,
        "the vector x in R3 with the standard basis vectors e1, e2, e3 and its projections x1 e1, x2 e2, x3 e3 onto the three axes",
        [
            panel(
                1.0,
                lines=[
                    ([-0.5, 0], [0, 0], [0, 0], "#000000", 1.1),
                    ([0, 0], [-0.5, 0], [0, 0], "#000000", 1.1),
                    ([0, 0], [0, 0], [-0.5, 0], "#000000", 1.1),
                ]
                + [(0.96 * _f[0] * _s, 0.96 * _f[1] * _s, 0.96 * _f[2] * _s, GREEN, 1.8, None, -0.2) for _f in _feet]
                + [(_a[0] + (_b[0] - _a[0]) * _s, _a[1] + (_b[1] - _a[1]) * _s, _a[2] + (_b[2] - _a[2]) * _s, GREY, 1.0, [4, 3]) for _a, _b in _guides],
                arrows=[((_p[0], 0, 0), (2.1, 0, 0), "#000000", 1.1), ((0, _p[1], 0), (0, 2.7, 0), "#000000", 1.1), ((0, 0, _p[2]), (0, 0, 2.2), "#000000", 1.1)]
                + [(tuple(0.9 * c for c in _f), _f, GREEN) for _f in _feet]
                + [((0, 0, 0), (1, 0, 0), GREY), ((0, 0, 0), (0, 1, 0), GREY), ((0, 0, 0), (0, 0, 1), GREY), ((0, 0, 0), _p, BLUE)],
                texts=[((0.55, 0, 0), r"\vec{e}_1", GREY, -60), ((0, 0.55, 0), r"\vec{e}_2", GREY, -90), ((0, 0, 0.55), r"\vec{e}_3", GREY, 0),
                       (_p, r"\vec{x}", BLUE, 20, 7), (_feet[0], r"x^1 \vec{e}_1", GREEN, 160, 9), (_feet[1], r"x^2 \vec{e}_2", GREEN, -90, 8),
                       ((0, 0, 0.8 * _p[2]), r"x^3 \vec{e}_3", GREEN, 180, 8)],
            )
        ],
        height=300,
    )

    mo.vstack(
        [
            mo.md(
                r"""
    ### The standard basis
    """
            ),
            definition(
                r"""
    $\mathbb{R}^n$ has a preferred orthogonal frame

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \\ \vdots \\ 0 \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}
    \qquad \text{the \textbf{standard basis vectors} of } \mathbb{R}^n
    $$
    """,
                "Standard basis",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $\vec{e}_i \cdot \vec{e}_j = 0$ if $i \neq j$

    $\leadsto$ &nbsp; $\vec{e}_i \cdot \vec{e}_i = 1$ &nbsp; (unit length vectors)

    Given

    $$
    \begin{aligned}
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}
    &= x^1 \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix} + \dots + x^n \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix} \\
    &= \underbrace{x^1 \vec{e}_1}_{\footnotesize \mathrm{proj}_{\vec{e}_1}(\vec{x})} + \underbrace{x^2 \vec{e}_2}_{\footnotesize \mathrm{proj}_{\vec{e}_2}(\vec{x})} + \dots + \underbrace{x^n \vec{e}_n}_{\footnotesize \mathrm{proj}_{\vec{e}_n}(\vec{x})}
    = (\vec{x} \cdot \vec{e}_1)\, \vec{e}_1 + (\vec{x} \cdot \vec{e}_2)\, \vec{e}_2 + \dots + (\vec{x} \cdot \vec{e}_n)\, \vec{e}_n
    \end{aligned}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; any vector can be written uniquely as a linear combination of the standard basis vectors

    $\leadsto$ &nbsp; the component $x^i$ of a vector $\vec{x}$ is the signed length of the projection of $\vec{x}$ along $\vec{e}_i$
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
    ## I.3 &nbsp; Matrices, linear transformations, and determinants

    ### Matrices
    """
            ),
            definition(
                r"""
    Given $m, n \in \mathbb{Z}_{>0}$, an **$m \times n$ matrix** is an array of real numbers with $m$ rows and $n$ columns

    $$
    A = \begin{bmatrix}
    A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\
    A^2{}_1 & A^2{}_2 & \cdots & A^2{}_n \\
    \vdots & & & \vdots \\
    A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n
    \end{bmatrix} \in \mathrm{Mat}(m \times n),
    \qquad A^i{}_j \in \mathbb{R} \quad \forall\, i = 1, \dots, m, \ j = 1, \dots, n
    $$

    $A^i{}_j$ is the $(i, j)$ component of the matrix $A$: superscript $i$ denotes the row, subscript $j$ denotes the column. In $\mathrm{Mat}(m \times n)$, $m$ counts rows and $n$ counts columns.
    """,
                "Matrix",
            ),
            mo.md(
                r"""
    Why are we interested in matrices?

    $\leadsto$ &nbsp; generalization of vectors ($n \times 1$ matrices): can also extend addition and multiplication to matrices!

    $\leadsto$ &nbsp; will give the simplest examples of multivariable functions!
    """
            ),
            definition(
                r"""
    Given $A \in \mathrm{Mat}(m \times n)$, $B \in \mathrm{Mat}(m \times n)$, $\alpha \in \mathbb{R}$

    $A + B \in \mathrm{Mat}(m \times n)$ has components

    $$
    (A + B)^i{}_j = A^i{}_j + B^i{}_j \qquad (\text{componentwise addition})
    $$

    $\alpha A \in \mathrm{Mat}(m \times n)$ has components

    $$
    (\alpha A)^i{}_j = \alpha A^i{}_j \qquad (\text{componentwise multiplication by a scalar})
    $$
    """,
                "Matrix addition and scalar multiplication",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}, \quad
    B = \begin{bmatrix} 6 & 4 & 2 \\ 5 & 3 & 1 \end{bmatrix} \in \mathrm{Mat}(2 \times 3)
    \qquad \leadsto \qquad
    A + B = \begin{bmatrix} 7 & 6 & 5 \\ 9 & 8 & 7 \end{bmatrix}, \quad
    3A = \begin{bmatrix} 3 & 6 & 9 \\ 12 & 15 & 18 \end{bmatrix}
    $$

    ### Matrix multiplication
    """
            ),
            definition(
                r"""
    Given $A \in \mathrm{Mat}(m \times p)$, $B \in \mathrm{Mat}(p \times n)$

    $AB \in \mathrm{Mat}(m \times n)$ has components

    $$
    (AB)^i{}_j = \underbrace{A^i{}_1 B^1{}_j + A^i{}_2 B^2{}_j + \dots + A^i{}_p B^p{}_j}_{\mathclap{\footnotesize \text{sum of products of corresponding components}}\vphantom{\footnotesize \text{sum of products of corresponding components}}}
    $$
    """,
                "Matrix multiplication",
            ),
            mo.md(
                r"""
    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \qquad
    B = \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix} \in \mathrm{Mat}(3 \times 2)
    $$

    (the number of columns of $A$ and the number of rows of $B$ must be the same in order to define $AB$)

    $$
    AB = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 3 \\ 2 & 0 \end{bmatrix}
    = \begin{bmatrix}
    1 \times 1 + 2 \times 0 + 3 \times 2 & 1 \times 0 + 2 \times 3 + 3 \times 0 \\
    4 \times 1 + 5 \times 0 + 6 \times 2 & 4 \times 0 + 5 \times 3 + 6 \times 0
    \end{bmatrix}
    = \begin{bmatrix} 7 & 6 \\ 16 & 15 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    $$

    **Remark.** Most times we cannot multiply two matrices: $A \in \mathrm{Mat}(m \times q)$, $B \in \mathrm{Mat}(p \times n)$

    - $AB$ can only be defined if $p = q$ $\;\Longrightarrow\; AB \in \mathrm{Mat}(m \times n)$
    - $BA$ can only be defined if $m = n$ $\;\Longrightarrow\; BA \in \mathrm{Mat}(p \times q)$
    - $p = q$ and $m = n$ $\;\not\Longrightarrow\; AB = BA$! &nbsp; ($AB \in \mathrm{Mat}(n \times n)$, $BA \in \mathrm{Mat}(p \times p)$)
    - $p = q = m = n$ $\;\not\Longrightarrow\; AB = BA$!

    **Example.**

    $$
    A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}, \quad
    B = \begin{bmatrix} 5 & 0 \\ 1 & 1 \end{bmatrix} \in \mathrm{Mat}(2 \times 2)
    \qquad \Longrightarrow \qquad
    AB = \begin{bmatrix} 11 & 1 \\ 3 & 3 \end{bmatrix} \neq BA = \begin{bmatrix} 10 & 5 \\ 2 & 4 \end{bmatrix}
    $$

    (matrix multiplication is non-commutative even for square matrices)

    **Remark.** Matrix multiplication can “transform” vectors into other vectors: $A \in \mathrm{Mat}(m \times n)$ and $\vec{x} \in \mathbb{R}^n \approx \mathrm{Mat}(n \times 1)$

    $$
    \Longrightarrow \qquad A\vec{x} \in \mathrm{Mat}(m \times 1) \approx \mathbb{R}^m
    $$

    $$
    \Longrightarrow \qquad A : \mathbb{R}^n \longrightarrow \mathbb{R}^m \ \text{ is a function on } \mathbb{R}^n \text{ valued in } \mathbb{R}^m \quad (\text{a multivariable function!})
    $$

    **Example.**

    $$
    A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \in \mathrm{Mat}(2 \times 3), \quad
    \vec{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \in \mathbb{R}^3 = \mathrm{Mat}(3 \times 1)
    $$

    $$
    \Longrightarrow \qquad A\vec{x} = \begin{bmatrix} 1 + 4 + 9 \\ 4 + 10 + 18 \end{bmatrix} = \begin{bmatrix} 14 \\ 32 \end{bmatrix} \in \mathbb{R}^2 = \mathrm{Mat}(2 \times 1)
    $$

    $\leadsto$ &nbsp; functions defined by matrix multiplication are always linear! (very special property)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Linear transformations"""),
            definition(
                r"""
    A function $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ is called **linear** if $\forall\, \vec{x}, \vec{y} \in \mathbb{R}^n$ and $\forall\, \alpha, \beta \in \mathbb{R}$

    $$
    f(\alpha \vec{x} + \beta \vec{y}) = \alpha f(\vec{x}) + \beta f(\vec{y})
    $$
    """,
                "Linear function",
            ),
            theorem(
                r"""
    Every function defined by an $m \times n$ matrix via matrix multiplication is linear. Conversely, every linear function $\mathbb{R}^n \longrightarrow \mathbb{R}^m$ is defined by an $m \times n$ matrix!
    """,
                "Linear functions and matrices",
            ),
            mo.md(
                r"""
    **Proof.**

    1. Write $A$ in terms of its column vectors ($n$ $m$-vectors)

        $$
        A = \begin{bmatrix}
        A^1{}_1 & A^1{}_2 & \cdots & A^1{}_n \\
        \vdots & \vdots & & \vdots \\
        A^m{}_1 & A^m{}_2 & \cdots & A^m{}_n
        \end{bmatrix}
        = \begin{bmatrix} \vec{A}_1 & \vec{A}_2 & \cdots & \vec{A}_n \end{bmatrix} \in \mathrm{Mat}(m \times n)
        $$

    2. For $\vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \in \mathbb{R}^n$

        $$
        \begin{aligned}
        A\vec{x} &= \begin{bmatrix}
        A^1{}_1 x^1 + A^1{}_2 x^2 + \dots + A^1{}_n x^n \\
        A^2{}_1 x^1 + A^2{}_2 x^2 + \dots + A^2{}_n x^n \\
        \vdots \\
        A^m{}_1 x^1 + A^m{}_2 x^2 + \dots + A^m{}_n x^n
        \end{bmatrix} \\
        &= x^1 \begin{bmatrix} A^1{}_1 \\ A^2{}_1 \\ \vdots \\ A^m{}_1 \end{bmatrix} +
        x^2 \begin{bmatrix} A^1{}_2 \\ A^2{}_2 \\ \vdots \\ A^m{}_2 \end{bmatrix} +
        \dots +
        x^n \begin{bmatrix} A^1{}_n \\ A^2{}_n \\ \vdots \\ A^m{}_n \end{bmatrix}
        = x^1 \vec{A}_1 + x^2 \vec{A}_2 + \dots + x^n \vec{A}_n
        \end{aligned}
        $$

    3. Then

        $$
        A(\alpha \vec{x} + \beta \vec{y}) = (\alpha x^1 + \beta y^1)\, \vec{A}_1 + \dots + (\alpha x^n + \beta y^n)\, \vec{A}_n = \alpha A\vec{x} + \beta A\vec{y}
        $$

    For the converse direction: $f : \mathbb{R}^n \longrightarrow \mathbb{R}^m$ linear

    $$
    \begin{align*}
    \Longrightarrow \quad f(\vec{x}) &= f(x^1 \vec{e}_1 + x^2 \vec{e}_2 + \dots + x^n \vec{e}_n), \qquad \forall\, \vec{x} \in \mathbb{R}^n \qquad (\vec{e}_i \text{ the standard basis of } \mathbb{R}^n) \\
    &= x^1 f(\vec{e}_1) + x^2 f(\vec{e}_2) + \dots + x^n f(\vec{e}_n) \\
    &= A\vec{x} \quad \text{where} \quad A = \begin{bmatrix} f(\vec{e}_1) & f(\vec{e}_2) & \cdots & f(\vec{e}_n) \end{bmatrix} \in \mathrm{Mat}(m \times n), \quad \vec{A}_i = f(\vec{e}_i) \in \mathbb{R}^m \tag*{$\square$}
    \end{align*}
    $$

    $\leadsto$ &nbsp; linear functions (or linear transformations) are the simplest non-trivial examples of multivariable functions

    $\leadsto$ &nbsp; later, we will introduce derivatives of more general multivariable functions as their best linear approximations

    **Remark.** Matrix multiplication is the same as composition of linear transformations

    $$
    \begin{aligned}
    A \in \mathrm{Mat}(m \times p) \quad &\leftrightsquigarrow \quad A : \mathbb{R}^p \longrightarrow \mathbb{R}^m \\
    B \in \mathrm{Mat}(p \times n) \quad &\leftrightsquigarrow \quad B : \mathbb{R}^n \longrightarrow \mathbb{R}^p \\
    AB \in \mathrm{Mat}(m \times n) \quad &\leftrightsquigarrow \quad A \circ B : \mathbb{R}^n \longrightarrow \mathbb{R}^m
    \end{aligned}
    $$

    $\leadsto$ &nbsp; another way to get convinced about non-commutativity of matrix multiplication!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Determinants of $2 \times 2$ matrices"""),
            definition(
                r"""
    For $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \in \mathrm{Mat}(2 \times 2) \ \leftrightsquigarrow \ A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ define

    $$
    \det(A) = ad - bc \in \mathbb{R} \qquad \text{the \textbf{determinant} of } A
    $$
    """,
                "Determinant",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; the determinant is a fundamental property of a square matrix (also for $n > 2$)

    $\leadsto$ &nbsp; it measures the “signed area” of the parallelogram defined by the columns of $A$, $\vec{A}_1 = A\vec{e}_1$ and $\vec{A}_2 = A\vec{e}_2$

    $$
    \det A = \text{signed area} = \lVert \vec{A}_1 \rVert\, \lVert \vec{A}_2 \rVert \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)
    $$

    with $\theta$ the angle turning from $\vec{A}_1$ to $\vec{A}_2$ counterclockwise &nbsp; ($\sin\theta > 0 \Longrightarrow \det A > 0$)

    $$
    \begin{aligned}
    (\det A)^2 = \text{area}^2 = (\text{base} \times \text{height})^2 &= \lVert \vec{A}_1 \rVert^2\, \lVert \vec{A}_2 \rVert^2 \sin\!\big(\theta(\vec{A}_1, \vec{A}_2)\big)^2 \\
    &= \lVert \vec{A}_1 \rVert^2\, \lVert \vec{A}_2 \rVert^2 - (\vec{A}_1 \cdot \vec{A}_2)^2 = (ad - bc)^2
    \end{aligned}
    $$
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
    md = mo.ui.slider(-3, 3, 0.5, value=1.5, label="$d$", show_value=True)
    return ma, mb, mc, md


@app.cell(hide_code=True)
def _(Arc, BLUE, Figure, GREEN, GREY, HALF, LIGHT, RED, arrow, ma, math, mb, mc, md, mo, name_tip, plane, table, vector):
    _a, _b, _c, _d = ma.value, mb.value, mc.value, md.value
    _det = _a * _d - _b * _c + 0.0

    def _turn(ax, p, q, ccw, radius):
        """Circular arc from the direction of p to the direction of q (counterclockwise when ccw), with a head
        at its end, and theta beside its middle."""
        t1, t2 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
        span = (t2 - t1) % (2 * math.pi) if ccw else -((t1 - t2) % (2 * math.pi))
        lo, hi = (t1, t1 + span) if ccw else (t1 + span, t1)
        ax.add_patch(Arc((0, 0), 2 * radius, 2 * radius, theta1=math.degrees(lo), theta2=math.degrees(hi), color=GREEN, lw=1.4))
        end = (radius * math.cos(t2), radius * math.sin(t2))
        step = math.copysign(min(0.35 * abs(span), 0.2), span)
        back = (radius * math.cos(t2 - step), radius * math.sin(t2 - step))
        d = (end[0] - back[0], end[1] - back[1])
        n = math.hypot(*d)  # the head follows the chord of the last part of the arc
        arrow(ax, (end[0] - 1e-3 * d[0] / n, end[1] - 1e-3 * d[1] / n), end, GREEN)
        mid = t1 + span / 2
        ax.text(1.45 * radius * math.cos(mid), 1.45 * radius * math.sin(mid), r"$\theta$", color=GREEN, fontsize=13, ha="center", va="center")

    _fig = Figure(figsize=(HALF + 0.4, HALF + 0.7), layout="constrained")
    _ax = _fig.subplots()
    _small = max(abs(_a), abs(_b), abs(_c), abs(_d), abs(_a + _b), abs(_c + _d)) <= 3
    plane(_ax, 4.4 if _small else 7.6)  # the frame follows the parallelogram: nothing is clipped
    _ticks = range(-4, 5, 2) if _small else range(-6, 7, 3)
    _ax.set_xticks(_ticks)
    _ax.set_yticks(_ticks)
    _ax.fill([0, _a, _a + _b, _b], [0, _c, _c + _d, _d], color=LIGHT, lw=0)  # the parallelogram defined by A_1, A_2
    _ax.plot([_a, _a + _b, _b], [_c, _c + _d, _d], color=GREY, lw=1.0, ls=(0, (4, 3)))
    vector(_ax, (0, 0), (_a, _c), BLUE)
    vector(_ax, (0, 0), (_b, _d), RED)
    name_tip(_ax, (0, 0), (_a, _c), r"$\vec{A}_1$", BLUE, away=(_b, _d))
    name_tip(_ax, (0, 0), (_b, _d), r"$\vec{A}_2$", RED, away=(_a, _c))
    if _det != 0:
        _r = 0.6 * min(math.hypot(_a, _c), math.hypot(_b, _d), 2.0)
        _turn(_ax, (_a, _c), (_b, _d), _det > 0, max(_r, 0.3))

    mo.vstack(
        [
            mo.hstack([ma, mb, mc, md], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\det(A) = ad - bc$", rf"${_det:g}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; it also determines whether or not $A : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ is **invertible**!

    $$
    \exists\, A^{-1} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2 \ \text{ such that } \ A \circ A^{-1}(\vec{x}) = A^{-1} \circ A(\vec{x}) = \vec{x} \quad \forall\, \vec{x} \in \mathbb{R}^2
    \qquad \Longleftrightarrow \qquad \det(A) \neq 0
    $$

    $\leadsto$ &nbsp; in fact, for $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ the inverse can be calculated explicitly when $\det(A) = ad - bc \neq 0$

    $$
    A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $f : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$ be linear, with

    $$
    f\!\left( \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right) = \begin{bmatrix} 3 \\ 1 \end{bmatrix}
    \qquad \text{and} \qquad
    f\!\left( \begin{bmatrix} 1 \\ -1 \end{bmatrix} \right) = \begin{bmatrix} 1 \\ 3 \end{bmatrix}.
    $$

    Find the matrix representation of $f$. Then compute $f\!\left( \begin{bmatrix} 2 \\ -1 \end{bmatrix} \right)$.

    ### Question 2

    Let $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \; B = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix}$.

    Compute $AB$ and $BA$.

    Then find all vectors $\vec{x} \in \mathbb{R}^2$ such that $AB\vec{x} = BA\vec{x}$.

    Conclude that $AB \neq BA$ does not imply $AB\vec{x} \neq BA\vec{x}$ $\;\forall\, \vec{x} \in \mathbb{R}^2$.

    ### Question 3

    For $t \in \mathbb{R}$, consider

    $$
    C_t = \begin{bmatrix} t & 1 \\ 2 & t - 1 \end{bmatrix}
    $$

    For which values of $t$ is $C_t$ invertible?

    Let $Q = [0, 1] \times [0, 1] \subseteq \mathbb{R}^2$ be the unit square in $\mathbb{R}^2$.

    Draw $C_t(Q)$ and compute its area for $t = -2$, $t = 0$, $t = 2$.
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
