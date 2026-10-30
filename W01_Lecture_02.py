import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 02 • The Euclidean inner product (the dot product)", css_file="bs101.css")


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
    header("Lecture 02", "Week 01", "Lecture 02 • The Euclidean inner product (the dot product)")
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

    def num(v):
        """A value as one would write it: exact when it is a multiple of 1/2, otherwise to two decimals."""
        return f"{v + 0.0:g}" if abs(2 * v - round(2 * v)) < 1e-9 else f"{v:.2f}"

    return name_tip, num, vector


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

    - points in $n$-space $\mathbb{R}^n \ni \vec{x} = (x^1, x^2, \dots, x^n)$ = $n$-vectors (arrows between points); each entry is a real number, $x^2$ is the 2nd component of $\vec{x}$
    - vector addition ${+} : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}^n$ and scalar–vector multiplication $\cdot : \mathbb{R} \times \mathbb{R}^n \longrightarrow \mathbb{R}^n$, both componentwise
    - $\leadsto$ &nbsp; allow us to do calculations with vectors the same way as with real numbers!

    **In this lecture:** extra structure on $\mathbb{R}^n$ (needed for “measurements”)

    **References:** MT 1.2, 1.5
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, note, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## I.2 &nbsp; The Euclidean inner product (the dot product)

    ### The dot product
    """
            ),
            definition(
                r"""
    Given two vectors

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix}, \quad
    \vec{y} = \begin{bmatrix} y^1 \\ y^2 \\ \vdots \\ y^n \end{bmatrix} \in \mathbb{R}^n
    $$

    we define their **dot product** or **inner product** as the real number

    $$
    \vec{x} \cdot \vec{y} = \underbrace{x^1 y^1 + x^2 y^2 + \dots + x^n y^n}_{\mathclap{\footnotesize \text{sum of products of components}}\vphantom{\footnotesize \text{sum of products of components}}} \in \mathbb{R}
    $$
    """,
                "Dot product",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; another extension of multiplication of real numbers, now to pairs of vectors, and taking scalar values

    $$
    \cdot : \mathbb{R}^n \times \mathbb{R}^n \longrightarrow \mathbb{R}
    $$
    """
            ),
            note(
                r"""
    This “$\cdot$” is **not** the same as for scalar–vector multiplication! To avoid confusion, we drop the “$\cdot$” for scalar–vector multiplication and write

    $$
    \alpha \vec{x} = \alpha \begin{bmatrix} x^1 \\ \vdots \\ x^n \end{bmatrix} = \begin{bmatrix} \alpha x^1 \\ \vdots \\ \alpha x^n \end{bmatrix}
    $$
    """
            ),
            theorem(
                r"""
    For all vectors $\vec{x}, \vec{y}, \vec{z} \in \mathbb{R}^n$ and scalars $\alpha, \beta \in \mathbb{R}$

    1. $\vec{x} \cdot \vec{y} = \vec{y} \cdot \vec{x}$ &nbsp; (**symmetric**)
    2. $(\alpha \vec{x} + \beta \vec{y}) \cdot \vec{z} = \alpha\, \vec{x} \cdot \vec{z} + \beta\, \vec{y} \cdot \vec{z}$ and
       $\vec{x} \cdot (\alpha \vec{y} + \beta \vec{z}) = \alpha\, \vec{x} \cdot \vec{y} + \beta\, \vec{x} \cdot \vec{z}$
       &nbsp; (linear in each of its 2 arguments: **bilinear**; this is also a distributivity property)
    3. $\vec{x} \cdot \vec{x} \geq 0$, with “$=$” if and only if $\vec{x} = \vec{0}$ &nbsp; (**positive definite**)
    """,
                "Basic properties",
            ),
            mo.md(r"**Proof.** Exercise (using definitions and properties of real numbers). <span class=qed>$\square$</span>"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Arc, BLUE, GREEN, HALF, RED, arrow, blank, definition, math, mo):
    _fig, _ax = blank(HALF, 2.5, (-0.6, 4.0), (-0.55, 2.6))
    arrow(_ax, (-0.4, 0), (3.8, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 2.45), "black", lw=0.9)
    for _t in (1, 3):
        _ax.plot([_t, _t], [-0.05, 0.05], color="black", lw=0.9)
        _ax.text(_t, -0.14, f"${_t}$", fontsize=12, ha="center", va="top")
    _ax.plot([-0.05, 0.05], [math.sqrt(3)] * 2, color="black", lw=0.9)
    _ax.text(-0.14, math.sqrt(3), r"$\sqrt{3}$", fontsize=12, ha="right", va="center")
    _ax.text(-0.14, -0.14, "$0$", fontsize=12, ha="right", va="top")
    arrow(_ax, (0, 0), (3, 0), BLUE)
    arrow(_ax, (0, 0), (1, math.sqrt(3)), RED)
    _ax.text(2.2, 0.14, r"$\vec{x}$", color=BLUE, fontsize=13, ha="center", va="bottom")
    _ax.text(0.38, 1.1, r"$\vec{y}$", color=RED, fontsize=13, ha="right", va="center")
    _ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=0, theta2=60, color=GREEN, lw=1.4))
    _ax.text(0.68, 0.34, r"$\theta = \pi/3$", color=GREEN, fontsize=12, ha="left", va="center")

    mo.vstack(
        [
            mo.md(r"""### Norm and angle"""),
            definition(
                r"""
    The **norm** (length) of a vector $\vec{x}$ is

    $$
    \lVert \vec{x} \rVert := \sqrt{\vec{x} \cdot \vec{x}} \qquad (\text{makes sense since } \vec{x} \cdot \vec{x} \geq 0)
    $$

    The **angle** between two vectors $\vec{x}, \vec{y}$ is

    $$
    \theta(\vec{x}, \vec{y}) = \arccos\!\left( \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \right)
    \qquad (\text{must have } \vec{x}, \vec{y} \neq \vec{0})
    $$
    """,
                "Norm and angle",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; not so clear why this makes sense… &nbsp; ($\arccos : [-1, 1] \longrightarrow [0, \pi]$)

    **Example.** &nbsp; $\vec{x} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}, \quad \vec{y} = \begin{bmatrix} 1 \\ \sqrt{3} \end{bmatrix}$
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \lVert \vec{x} \rVert = \sqrt{(3)^2 + (0)^2} = 3, \qquad
    \lVert \vec{y} \rVert = \sqrt{(1)^2 + (\sqrt{3})^2} = 2, \qquad
    \vec{x} \cdot \vec{y} = 3 \cdot 1 + 0 \cdot \sqrt{3} = 3
    $$

    $$
    \Longrightarrow \qquad \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} = \frac{1}{2} = \cos\!\left(\frac{\pi}{3}\right)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    x1 = mo.ui.slider(-4, 4, 0.5, value=3, label="$x^1$", show_value=True)
    x2 = mo.ui.slider(-4, 4, 0.5, value=0, label="$x^2$", show_value=True)
    y1 = mo.ui.slider(-4, 4, 0.5, value=1, label="$y^1$", show_value=True)
    y2 = mo.ui.slider(-4, 4, 0.5, value=2, label="$y^2$", show_value=True)
    controls = mo.hstack([x1, x2, y1, y2], justify="start", gap=2, wrap=True)
    return controls, x1, x2, y1, y2


@app.cell(hide_code=True)
def _(np, x1, x2, y1, y2):
    x = np.array([x1.value, x2.value], dtype=float)
    y = np.array([y1.value, y2.value], dtype=float)
    dot = float(x @ y)
    nx = float(np.sqrt(x @ x))
    ny = float(np.sqrt(y @ y))
    nonzero = nx > 0 and ny > 0
    return dot, nonzero, nx, ny, x, y


@app.cell(hide_code=True)
def _(Arc, BLUE, Figure, GREEN, HALF, RED, controls, dot, math, mo, name_tip, nonzero, num, nx, ny, plane, table, vector, x, y):
    _fig = Figure(figsize=(HALF, HALF + 0.4), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 6)
    _ax.set_xticks(range(-4, 5, 2))
    _ax.set_yticks(range(-4, 5, 2))
    vector(_ax, (0, 0), tuple(x), BLUE)
    vector(_ax, (0, 0), tuple(y), RED)
    name_tip(_ax, (0, 0), tuple(x), r"$\vec{x}$", BLUE, away=tuple(y))
    name_tip(_ax, (0, 0), tuple(y), r"$\vec{y}$", RED, away=tuple(x))

    _need = r"need $\vec{x}, \vec{y} \neq \vec{0}$"
    if nonzero:
        _cos = max(-1.0, min(1.0, dot / (nx * ny)))  # guards arccos against rounding only
        _theta = math.acos(_cos)
        _a1 = math.degrees(math.atan2(x[1], x[0]))
        _a2 = math.degrees(math.atan2(y[1], y[0]))
        if (_a2 - _a1) % 360 > 180:
            _a1, _a2 = _a2, _a1
        _ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=_a1, theta2=_a2, color=GREEN, lw=1.4))
        _mid = math.radians(_a1 + ((_a2 - _a1) % 360) / 2)
        _ax.text(1.35 * math.cos(_mid), 1.35 * math.sin(_mid), r"$\theta$", color=GREEN, fontsize=13, ha="center", va="center")
        _angle = rf"${num(_theta)} \text{{ rad}} = {math.degrees(_theta):.0f}^\circ$"
    else:
        _angle = _need

    mo.vstack(
        [
            controls,
            table(
                [
                    (r"$\vec{x}\cdot\vec{y}$", rf"${dot:g}$"),
                    (r"$\theta(\vec{x},\vec{y})$", _angle),
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
            mo.md(r"""### The Cauchy–Schwarz inequality"""),
            theorem(
                r"""
    For every $\vec{x}, \vec{y} \in \mathbb{R}^n$

    $$
    (\vec{x} \cdot \vec{y})^2 \leq \lVert \vec{x} \rVert^2\, \lVert \vec{y} \rVert^2
    $$

    with “$=$” if and only if $\vec{x}, \vec{y}$ are proportional.
    """,
                "Cauchy–Schwarz inequality",
            ),
            mo.md(
                r"""
    $$
    \Longrightarrow \qquad \frac{\vec{x} \cdot \vec{y}}{\lVert \vec{x} \rVert\, \lVert \vec{y} \rVert} \in [-1, 1] \qquad \forall\, \vec{x}, \vec{y} \neq \vec{0}
    $$

    $\leadsto$ &nbsp; our definition of angles really makes sense!

    **Proof.** If $\vec{x} = \vec{0}$ or $\vec{y} = \vec{0}$ &nbsp; $\Longrightarrow$ &nbsp; $(\vec{x} \cdot \vec{y})^2 = 0 = \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2$

    Assume both $\vec{x}, \vec{y} \neq \vec{0}$ and compute $\lVert t\vec{x} + \vec{y} \rVert^2$ for $t \in \mathbb{R}$

    1. positive definite implies

        $$
        \lVert t\vec{x} + \vec{y} \rVert^2 \geq 0, \quad \text{with ``$=$'' if and only if } \underbrace{t\vec{x} + \vec{y} = \vec{0}}_{\mathclap{\footnotesize \vec{x},\, \vec{y} \text{ proportional}}\vphantom{\footnotesize \vec{x},\, \vec{y} \text{ proportional}}}
        $$

    2. bilinearity and symmetry give

        $$
        \begin{aligned}
        \lVert t\vec{x} + \vec{y} \rVert^2 &= (t\vec{x} + \vec{y}) \cdot (t\vec{x} + \vec{y}) = t^2\, \vec{x} \cdot \vec{x} + t\, \vec{x} \cdot \vec{y} + t\, \vec{y} \cdot \vec{x} + \vec{y} \cdot \vec{y} \\
        &= \underbrace{t^2 \lVert \vec{x} \rVert^2 + 2t\, \vec{x} \cdot \vec{y} + \lVert \vec{y} \rVert^2}_{\mathclap{\footnotesize \text{quadratic polynomial in } t}\vphantom{\footnotesize \text{quadratic polynomial in } t}}
        \end{aligned}
        $$

    $$
    \Longrightarrow \qquad t^2 \lVert \vec{x} \rVert^2 + 2t\, (\vec{x} \cdot \vec{y}) + \lVert \vec{y} \rVert^2 \geq 0
    $$

    with “$=$” for some $t$ if and only if $\vec{x}, \vec{y}$ are proportional

    $$
    \Longrightarrow \qquad \text{discriminant:} \quad \big(2 (\vec{x} \cdot \vec{y})\big)^2 - 4 \lVert \vec{x} \rVert^2 \lVert \vec{y} \rVert^2 \leq 0
    $$

    with “$=$” if and only if $\vec{x}, \vec{y}$ are proportional. <span class=qed>$\square$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, LIGHT, controls, dot, mo, np, num, table, x, y):
    _xx, _yy = float(x @ x), float(y @ y)  # exact for the slider values, unlike the squares of the norms
    _vertex = -dot / _xx if _xx > 0 else 0.0
    _t = np.sort(np.append(np.linspace(min(-4, _vertex - 2), max(4, _vertex + 2), 400), _vertex))
    _p = _t**2 * _xx + 2 * _t * dot + _yy

    _fig = Figure(figsize=(HALF, 3.5), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_t, _p, color=BLUE)
    _ax.plot(_vertex, float(_p.min()), "o", color=GREEN, ms=5, zorder=4)
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.grid(True, color=LIGHT, lw=0.6)
    _ax.set_axisbelow(True)
    _upper = max(30.0, 1.25 * float(_p.min()) + 2)
    _ax.set_ylim(-0.05 * _upper, _upper)
    _ax.set_xlabel("$t$")
    _ax.set_ylabel(r"$\|t\vec{x} + \vec{y}\|^2$")

    mo.vstack(
        [
            controls,
            table(
                [
                    (r"$(\vec{x}\cdot\vec{y})^2$", rf"${dot**2:g}$"),
                    (r"$\lVert\vec{x}\rVert^2\lVert\vec{y}\rVert^2$", rf"${_xx * _yy:g}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, RED, controls, mo, name_tip, np, num, nx, ny, plane, table, theorem, vector, x, y):
    _s = x + y
    _ns = float(np.sqrt(_s @ _s))

    _fig = Figure(figsize=(HALF, HALF + 0.4), layout="constrained")
    _ax = _fig.subplots()
    plane(_ax, 9)
    _ax.set_xticks(range(-8, 9, 4))
    _ax.set_yticks(range(-8, 9, 4))
    vector(_ax, tuple(x), tuple(_s), RED, linestyle=(0, (4, 3)))  # y translated to the tip of x
    vector(_ax, (0, 0), tuple(_s), GREEN)
    vector(_ax, (0, 0), tuple(x), BLUE)
    vector(_ax, (0, 0), tuple(y), RED)
    name_tip(_ax, (0, 0), tuple(_s), r"$\vec{x}+\vec{y}$", GREEN)
    name_tip(_ax, (0, 0), tuple(x), r"$\vec{x}$", BLUE, away=tuple(y))
    name_tip(_ax, (0, 0), tuple(y), r"$\vec{y}$", RED, away=tuple(x))

    mo.vstack(
        [
            mo.md(r"""### The triangle inequality"""),
            theorem(
                r"""
    For every $\vec{x}, \vec{y} \in \mathbb{R}^n$

    $$
    \lVert \vec{x} + \vec{y} \rVert \leq \lVert \vec{x} \rVert + \lVert \vec{y} \rVert
    $$
    """,
                "Triangle inequality",
            ),
            mo.md(r"**Proof.** Direct consequence of the Cauchy–Schwarz inequality! Exercise. <span class=qed>$\square$</span>"),
            controls,
            table(
                [
                    (r"$\lVert\vec{x}+\vec{y}\rVert$", rf"${num(_ns)}$"),
                    (r"$\lVert\vec{x}\rVert+\lVert\vec{y}\rVert$", rf"${num(round(nx, 2) + round(ny, 2))}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Orthogonal vectors"""),
            definition(
                r"""
    $\vec{x}, \vec{y} \in \mathbb{R}^n$ are called **orthogonal** ($\vec{x} \perp \vec{y}$) when

    $$
    \vec{x} \cdot \vec{y} = 0 \qquad \Longrightarrow \qquad \theta(\vec{x}, \vec{y}) = \arccos(0) = \frac{\pi}{2} = 90^\circ \quad (\text{for } \vec{x}, \vec{y} \neq \vec{0})
    $$
    """,
                "Orthogonal vectors",
            ),
            theorem(
                r"""
    In $\mathbb{R}^n$, we can find **at most $n$** non-zero vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$ which are pairwise orthogonal

    $$
    \vec{e}_i \cdot \vec{e}_j = 0 \qquad \forall\, i \neq j
    $$
    """,
                "Pairwise orthogonal vectors",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}
    \qquad \Longrightarrow \qquad \text{pairwise orthogonal}
    $$

    (a specific example of $n$ pairwise orthogonal vectors; many other examples exist!)

    Take any other non-zero vector

    $$
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^n \end{bmatrix} \neq \vec{0}
    $$

    Note that

    $$
    \vec{x} \cdot \vec{e}_1 = x^1, \quad \vec{x} \cdot \vec{e}_2 = x^2, \quad \dots, \quad \vec{x} \cdot \vec{e}_n = x^n,
    $$

    so $\vec{x} \perp \vec{e}_i$ if and only if $x^i = 0$.

    If $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n, \vec{x}$ were pairwise orthogonal, then $\vec{x}$ would have to be the zero vector $\vec{0}$. This contradicts our assumption that $\vec{x} \neq \vec{0}$.

    $\leadsto$ &nbsp; here we used the specific vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$, but the argument also works for any set of $n$ non-zero pairwise orthogonal vectors! <span class=qed>$\square$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, arrow, definition, mo, panel, turntable):
    _fig = Figure(figsize=(2.9, 2.7), layout="constrained")
    _a2 = _fig.subplots()
    _a2.set_xlim(-0.9, 2.1)
    _a2.set_ylim(-1.0, 2.0)
    _a2.set_aspect("equal")
    _a2.axis("off")
    arrow(_a2, (-0.6, 0), (1.9, 0), "black", lw=0.9)
    arrow(_a2, (0, -0.6), (0, 1.9), "black", lw=0.9)
    arrow(_a2, (0, 0), (1, 0), BLUE)
    arrow(_a2, (0, 0), (0, 1), BLUE)
    _a2.text(0.55, -0.14, r"$\vec{e}_1$", color=BLUE, fontsize=13, ha="center", va="top")
    _a2.text(-0.14, 0.55, r"$\vec{e}_2$", color=BLUE, fontsize=13, ha="right", va="center")
    _a2.text(0.6, -0.72, r"$\mathbb{R}^2$", fontsize=13, ha="center", va="top")

    # each axis is left out from the origin to the tip of e_i, so that the axis never covers the arrow
    _space = turntable(
        30,
        22,
        "the standard basis vectors e1, e2, e3 of R3, along the three coordinate axes",
        [
            panel(
                1.0,
                lines=[([-0.5, 0], [0, 0], [0, 0], "#000000", 1.1), ([0, 0], [-0.6, 0], [0, 0], "#000000", 1.1), ([0, 0], [0, 0], [-0.6, 0], "#000000", 1.1)],
                arrows=[((1, 0, 0), (1.9, 0, 0), "#000000", 1.1), ((0, 1, 0), (0, 1.9, 0), "#000000", 1.1), ((0, 0, 1), (0, 0, 1.9), "#000000", 1.1)]
                + [((0, 0, 0), (1, 0, 0), BLUE), ((0, 0, 0), (0, 1, 0), BLUE), ((0, 0, 0), (0, 0, 1), BLUE)],
                texts=[((0.55, 0, 0), r"\vec{e}_1", BLUE, -60), ((0, 0.55, 0), r"\vec{e}_2", BLUE, -90), ((0, 0, 0.55), r"\vec{e}_3", BLUE, 0)],
                caption=r"\mathbb{R}^3",
            )
        ],
        height=280,
    )

    mo.vstack(
        [
            mo.md(r"""### The standard basis"""),
            definition(
                r"""
    A set of $n$ non-zero pairwise orthogonal vectors is called an **orthogonal basis** of $\mathbb{R}^n$.

    The vectors

    $$
    \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \quad
    \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ \vdots \\ 0 \end{bmatrix}, \quad \dots, \quad
    \vec{e}_n = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 1 \end{bmatrix}
    $$

    used above are called the **standard basis vectors** of $\mathbb{R}^n$.
    """,
                "Orthogonal basis and standard basis",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; they have the additional property of having unit length (**unit vectors**)

    $\leadsto$ &nbsp; more importantly: &nbsp; $\vec{x} \cdot \vec{e}_i = x^i \quad \forall\, \vec{x} \in \mathbb{R}^n$

    **Example.**

    $$
    \mathbb{R}^2: \quad \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \; \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \end{bmatrix} \; \Longrightarrow \;
    \begin{cases}
    \vec{x} \cdot \vec{e}_1 = (x^1)(1) + (x^2)(0) = x^1 \\
    \vec{x} \cdot \vec{e}_2 = (x^1)(0) + (x^2)(1) = x^2
    \end{cases}
    $$

    $$
    \mathbb{R}^3: \quad \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \; \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \; \vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}
    \qquad
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix} \; \Longrightarrow \;
    \begin{cases}
    \vec{x} \cdot \vec{e}_1 = x^1 \\
    \vec{x} \cdot \vec{e}_2 = x^2 \\
    \vec{x} \cdot \vec{e}_3 = x^3
    \end{cases}
    $$
    """
            ),
            mo.Html(
                '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem 1rem;">'
                f'<div style="flex: 1 1 240px; min-width: 220px;">{mo.as_html(_fig).text}</div>'
                f'<div style="flex: 1.45 1 300px; min-width: 260px;">{_space.text}</div></div>'
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; the standard basis vectors define the coordinate axes on $\mathbb{R}^n$!

    $\leadsto$ &nbsp; coordinates/components of a vector are its dot products with the standard basis vectors!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Every $\vec{x} \in \mathbb{R}^n$ is a linear combination of the standard basis vectors $\vec{e}_1, \vec{e}_2, \dots, \vec{e}_n$, with coefficients

    $$
    x^1 = \vec{x} \cdot \vec{e}_1, \quad x^2 = \vec{x} \cdot \vec{e}_2, \quad \dots, \quad x^n = \vec{x} \cdot \vec{e}_n
    $$
    """,
                "Components in the standard basis",
            ),
            mo.md(
                r"""
    **Proof** (for $n = 3$).

    $$
    \begin{align*}
    \vec{x} = \begin{bmatrix} x^1 \\ x^2 \\ x^3 \end{bmatrix}
    &= \begin{bmatrix} x^1 \\ 0 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ x^2 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ x^3 \end{bmatrix}
    = x^1 \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix} + x^2 \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} + x^3 \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \\
    &= x^1 \vec{e}_1 + x^2 \vec{e}_2 + x^3 \vec{e}_3
    \qquad \text{and} \qquad
    \begin{cases}
    x^1 = \vec{x} \cdot \vec{e}_1 \\
    x^2 = \vec{x} \cdot \vec{e}_2 \\
    x^3 = \vec{x} \cdot \vec{e}_3
    \end{cases}
    \tag*{$\square$}
    \end{align*}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $\vec{x} = \begin{bmatrix} 1 \\ -2 \\ 2 \end{bmatrix}, \; \vec{y} = \begin{bmatrix} 2 \\ 1 \\ 1 \end{bmatrix}$.

    (a) Compute $2\vec{x} - \vec{y}$.

    (b) Compute $\vec{x} \cdot \vec{y}$, $\lVert \vec{x} \rVert$, $\lVert \vec{y} \rVert$.

    (c) Find the angle between $\vec{x}$ and $\vec{y}$.

    ### Question 2

    Consider $\vec{u} = \begin{bmatrix} 1 \\ 2 \\ -1 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 2 \\ a \\ 4 \end{bmatrix}$.

    (a) Find $a \in \mathbb{R}$ so that $\vec{u} \perp \vec{v}$.

    (b) For this value of $a$, compute $\lVert \vec{u} + \vec{v} \rVert$.

    (c) Check that $\lVert \vec{u} + \vec{v} \rVert^2 = \lVert \vec{u} \rVert^2 + \lVert \vec{v} \rVert^2$.

    ### Question 3

    Consider $\vec{u} = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \; \vec{v} = \begin{bmatrix} 1 \\ -1 \\ 0 \end{bmatrix}, \; \vec{w} = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$.

    (a) Show that $\vec{u}, \vec{v}, \vec{w}$ are pairwise orthogonal.

    (b) Write $\vec{x} = \begin{bmatrix} 3 \\ 1 \\ 4 \end{bmatrix}$ in the form $\vec{x} = a\vec{u} + b\vec{v} + c\vec{w}$.

    (c) Show that $a = \dfrac{\vec{x} \cdot \vec{u}}{\vec{u} \cdot \vec{u}}, \quad b = \dfrac{\vec{x} \cdot \vec{v}}{\vec{v} \cdot \vec{v}}, \quad c = \dfrac{\vec{x} \cdot \vec{w}}{\vec{w} \cdot \vec{w}}$.

    (d) Show that there is no non-zero vector $\vec{y} = \begin{bmatrix} p \\ q \\ r \end{bmatrix}$ orthogonal to $\vec{u}$, $\vec{v}$ and $\vec{w}$ at the same time.
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
