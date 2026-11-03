import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS101 • Lecture 18 • Gradient vector fields and curl", css_file="bs101.css")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np

    return mo, np


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

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    return BLUE, GREEN, GREY, LIGHT, ORANGE, RED, corollary, definition, header, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 18", "Week 11", "Lecture 18 • Gradient vector fields and curl")
    return


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

    return panel, sheet, turntable


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Vector fields &nbsp; $\vec{F} : D \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}^n$ &nbsp; $(n = 2)$, &nbsp; $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$

    Flow lines &nbsp; $\gamma : (-\varepsilon, \varepsilon) \subseteq \mathbb{R} \longrightarrow \mathbb{R}^n$ &nbsp; such that &nbsp; $\gamma'(t) = \vec{F}(\gamma(t))$

    $$
    \gamma(t) = \begin{bmatrix} x(t) \\ y(t) \end{bmatrix} \quad \text{such that} \quad \begin{bmatrix} x'(t) \\ y'(t) \end{bmatrix} = \begin{bmatrix} P(x(t), y(t)) \\ Q(x(t), y(t)) \end{bmatrix}
    $$

    Divergence &nbsp; $\vec{\nabla} \cdot \vec{F} : D \subseteq \mathbb{R}^n \longrightarrow \mathbb{R}$

    $$
    \vec{\nabla} \cdot \vec{F}(x, y) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \end{bmatrix} \cdot \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix} = \frac{\partial P}{\partial x}(x, y) + \frac{\partial Q}{\partial y}(x, y)
    $$

    **Example.** &nbsp; $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ &nbsp; $(n = 3)$

    <span class="chain">$\displaystyle \vec{F}(x, y, z) = \begin{bmatrix} P(x, y, z) \\ Q(x, y, z) \\ R(x, y, z) \end{bmatrix}$ $\displaystyle = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$ $\displaystyle = \underbrace{\begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}}_{\footnotesize \begin{matrix} \text{rotation vector field} \\ \text{on } xy\text{-directions} \end{matrix}} + \underbrace{\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}}_{\footnotesize \begin{matrix} \text{constant vector field} \\ \text{on } z\text{-direction} \end{matrix}}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(GREEN, np, panel, turntable):
    # the two parts of F: the rotation vector field (-y, x, 0) and the constant vector field (0, 0, 1), side by side, at the same
    # points on circles of radius 3/2 and 3 at the heights 1/2, 5/2 and 9/2 (twelve per circle); every arrow at 7/10 of its vector
    _pts = [np.array([_r * np.cos(np.radians(30 * _j + 15 * _l)), _r * np.sin(np.radians(30 * _j + 15 * _l)), 0.5 + 2.0 * _l]) for _l in range(3) for _r in (1.5, 3.0) for _j in range(12)]
    _axes = [((0, 0, 0), (4.6, 0, 0), "x", -150), ((0, 0, 0), (0, 4.6, 0), "y", 0), ((0, 0, 0), (0, 0, 6.8), "z", 90)]
    _box = ((-4.0, 4.0), (-4.0, 4.0), (0, 5.6))
    _fig = turntable(
        30, 30, "the rotation vector field [-y; x; 0] on xy-directions and the constant vector field [0; 0; 1] on z-direction, side by side",
        [panel(1.0, axes=_axes, arrows=[(p, p + 0.7 * np.array([-p[1], p[0], 0.0]), GREEN, 1.3) for p in _pts],
               texts=[((0, -4.0, 5.6), r"\begin{bmatrix} -y \\ x \\ 0 \end{bmatrix}", GREEN, 180, 0)], box=_box),
         panel(1.0, axes=_axes, arrows=[(p, p + 0.7 * np.array([0, 0, 1.0]), GREEN, 1.3) for p in _pts],
               texts=[((0, -4.0, 5.6), r"\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}", GREEN, 180, 0)], box=_box)],
        height=540, cols=2, key="L18-parts")
    _fig
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\Longrightarrow$ &nbsp; vector field spiraling upwards
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ht = mo.ui.slider(0, 6.28, 0.04, value=1.6, label="$t$", show_value=True)
    return (ht,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, ht, mo, np, panel, turntable):
    # the field F(x) = (-y, x, 1), every arrow at 2/5 of its vector, at eight points on the circle of radius 3 about the
    # z-axis, at the heights 5/4, 17/4 and 29/4 (every other level turned by half a step, so that no arrows cross); the flow line
    # through gamma(0) = (2, 0, 0) is the helix gamma(t) = (2 cos(t), 2 sin(t), t), in red, drawn past the slider's range
    # so that its name sits where the point never goes, away from the z-axis; gamma(t) moves with t and gamma'(t) = F(gamma(t)) is drawn from it in blue, at the
    # scale of the field and named once, in the free corner above. Heights are drawn at half scale, so that the helix
    # shows its turn
    def _F(p):
        return np.array([-p[1], p[0], 1.0])

    _k = 0.4
    _pts = [np.array([_r * np.cos(np.radians((_j + _l / 2) * 360 / _n)), _r * np.sin(np.radians((_j + _l / 2) * 360 / _n)), 1.25 + 3 * _l])
            for _l in range(3) for _r, _n in ((3.0, 8),) for _j in range(_n)]
    _field = [(_p, _p + _k * _F(_p), GREEN, 1.3) for _p in _pts]
    _s = np.linspace(0, 2 * np.pi + 1.4, 271)
    _t = round(ht.value, 10)
    _g = np.array([2 * np.cos(_t), 2 * np.sin(_t), _t])
    _v = _g + _k * _F(_g)
    # the name of gamma(t) beside its point, on the right of the velocity as seen in the first view (outside the helix):
    # centred along the screen normal of the velocity, just far enough for its box (about 30 x 16 px) to clear the dot
    # (40 px to a drawing unit); it turns with t and never jumps
    _az, _el, _ys = np.radians(30), np.radians(30), 0.5
    _r = np.array([-np.sin(_az), np.cos(_az), 0])
    _u = np.array([-np.sin(_el) * np.cos(_az), -np.sin(_el) * np.sin(_az), np.cos(_el) * _ys])
    _w = np.array([-np.sin(_el) * np.cos(_az), -np.sin(_el) * np.sin(_az), np.cos(_el) / _ys])
    _sv = np.array([_r @ _F(_g), _u @ _F(_g)])
    _n = np.array([_sv[1], -_sv[0]]) / np.hypot(*_sv)
    _d = (15 * abs(_n[0]) + 8 * abs(_n[1]) + 5) / 40
    _at = _g + _d * (_n[0] * _r + _n[1] * _w) + 0.2 * _w  # raised by half the name's height: the name hangs below this point
    _fig = turntable(
        30,
        30,  # the view of the name of gamma(t) above
        "the vector field F(x) = [-y; x; 1] at points around the z-axis, and its flow line through gamma(0) = [2; 0; 0], a helix moving up around the z-axis, with the point gamma(t) and the velocity gamma'(t) = F(gamma(t))",
        [
            panel(
                0.5,
                lines=[(2 * np.cos(_s), 2 * np.sin(_s), _s, RED, 1.8)],
                points=[((2, 0, 0), BLUE, 3.5), (tuple(_g), BLUE, 4.0)],
                axes=[((0, 0, 0), (4.0, 0, 0), "x", -150), ((0, 0, 0), (0, 4.0, 0), "y", 0), ((0, 0, 0), (0, 0, 9.0), "z", 90)],
                arrows=_field + [(_g, _v, BLUE, 2.2)],
                texts=[
                    ((2 * np.cos(2 * np.pi + 1.4), 2 * np.sin(2 * np.pi + 1.4), 2 * np.pi + 1.4), r"\gamma", RED, 0, 6),
                    ((2, 0, 0), r"\gamma(0)", "#000000", 180, 7),
                    (tuple(_at), r"\gamma(t)", "#000000", -90, 0),
                    ((0, 4.1, 10.6), r"\gamma'(t) = \vec{F}(\gamma(t))", BLUE, 0, 0),
                    ((0, -3.4, 8.6), r"\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}", GREEN, 180, 0),
                ],
                box=((-3.4, 3.4), (-3.4, 3.4), (0, 9.2)),
            )
        ],
        height=440,
        key="L18-helix",
    )

    mo.vstack([mo.hstack([ht], justify="start"), _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    flow line = helix moving up around the $z$-axis

    $$
    \gamma'(t) = \begin{bmatrix} x'(t) \\ y'(t) \\ z'(t) \end{bmatrix} = \vec{F}(\gamma(t)) = \begin{bmatrix} -y(t) \\ x(t) \\ 1 \end{bmatrix}, \qquad \gamma(0) = \begin{bmatrix} x_0 \\ y_0 \\ z_0 \end{bmatrix}
    $$

    $$
    \Longrightarrow \qquad \gamma(t) = \begin{bmatrix} x_0 \cos(t) - y_0 \sin(t) \\ x_0 \sin(t) + y_0 \cos(t) \\ z_0 + t \end{bmatrix}
    $$

    <span class="chain">$\displaystyle \mathrm{div}(\vec{F})(\vec{x}) = (\vec{\nabla} \cdot \vec{F})(\vec{x}) = \frac{\partial}{\partial x}(-y) + \frac{\partial}{\partial y}(x) + \frac{\partial}{\partial z}(1) = 0$ $\displaystyle \quad \leadsto \ \text{flow does not expand/contract volumes around } \vec{x}$</span>

    **In this lecture:** gradient vector fields, potential functions, curl

    **References:** MT 4.3, 4.4
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## IV.2 &nbsp; Gradient vector fields and curl

    **Recall.** Given $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ differentiable at $\vec{x} \in D$, we can define the gradient of $f$ at $\vec{x}$

    $$
    \vec{\nabla} f(\vec{x}) = \begin{bmatrix} \dfrac{\partial f}{\partial x}(\vec{x}) \\[10pt] \dfrac{\partial f}{\partial y}(\vec{x}) \\[10pt] \dfrac{\partial f}{\partial z}(\vec{x}) \end{bmatrix}
    $$

    If $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$ is differentiable $\forall\, \vec{x} \in D$, then $\vec{\nabla} f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ is a vector field!

    $\leadsto$ &nbsp; note that $\vec{\nabla} f(\vec{x}) = \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \\ \partial / \partial z \end{bmatrix} f(\vec{x})$

    useful to think of $\vec{\nabla}$ as a vector of partial derivatives for gradients as well!
    """
            ),
            definition(
                r"""
    A vector field $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ is called a **gradient vector field** if $\vec{F} = \vec{\nabla} f$ for some differentiable function $f : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}$.

    $\leadsto$ &nbsp; $f$ is called a **potential function** for $\vec{F}$.
    """,
                "Gradient vector field",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; The radial vector field $\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$ is a gradient vector field

    $\leadsto$ &nbsp; $\vec{G}(\vec{x}) = \vec{\nabla} g(\vec{x})$ &nbsp; for &nbsp; $g(\vec{x}) = \dfrac{1}{2}(x^2 + y^2 + z^2)$

    <span class="chain">$\displaystyle \vec{H}(\vec{x}) = \underbrace{\frac{1}{\sqrt{x^2 + y^2 + z^2}}}_{\mathclap{\footnotesize \vec{x} \neq \vec{0}}\vphantom{\footnotesize \vec{x} \neq \vec{0}}} \begin{bmatrix} x \\ y \\ z \end{bmatrix}$ $\displaystyle \quad \text{The unit radial vector field } \vec{H}$ $\displaystyle \text{is also a gradient vector field (for } \vec{x} \neq \vec{0}\text{)}$</span>

    $\leadsto$ &nbsp; $\vec{H}(\vec{x}) = \vec{\nabla} h(\vec{x})$ &nbsp; for &nbsp; $\underbrace{h(\vec{x}) = \sqrt{x^2 + y^2 + z^2}}_{\mathclap{\footnotesize \text{not differentiable at } \vec{x} = \vec{0}}\vphantom{\footnotesize \text{not differentiable at } \vec{x} = \vec{0}}}$
    """)
    return


@app.cell(hide_code=True)
def _(GREEN, np, panel, turntable):
    # the radial vector field G(x) = x (every arrow at 3/5 of its vector) and the unit radial vector field H(x) = x/|x| (every
    # arrow at full length) at the same 64 points of a grid, the cube [-9/4, 9/4]^3 in steps of 3/2; side by side, one view for both.
    # The names sit at the same place in both panels, above the arrows, where they fit whole at every screen width
    _pts = [np.array([a, b, c]) for a in (-2.25, -0.75, 0.75, 2.25) for b in (-2.25, -0.75, 0.75, 2.25) for c in (-2.25, -0.75, 0.75, 2.25)]
    _o = np.zeros(3)
    # each name just past the end of its axis, in the axis direction on the screen (x: -147 degrees in this view)
    _axes = [((-4.0, 0, 0), (4.0, 0, 0), "x", -147), ((0, -4.0, 0), (0, 4.0, 0), "y", 0), ((0, 0, -4.0), (0, 0, 4.0), "z", 90)]
    _box = ((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))  # sizes the drawing, with room above it for the names at every screen width
    _fig = turntable(
        30, 22, "the radial vector field G(x) = [x; y; z] and the unit radial vector field H(x) = x/|x| at 64 points of a grid, side by side",
        [panel(1.0, axes=_axes, arrows=[(p, p + 0.6 * p, GREEN, 1.4) for p in _pts],
               texts=[((0, 3.0, 6.25), r"\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}", GREEN, 90, 0)], box=_box),
         panel(1.0, axes=_axes, arrows=[(p, p + p / np.linalg.norm(p), GREEN, 1.4) for p in _pts], points=[(_o, "#000000", 3.5, True)],
               texts=[((0, 3.0, 6.25), r"\vec{H}(\vec{x}) = \dfrac{1}{\sqrt{x^2 + y^2 + z^2}} \begin{bmatrix} x \\ y \\ z \end{bmatrix}", GREEN, 90, 0), (_o, r"\vec{0}", "#000000", 160, 7)], box=_box)],
        height=440, cols=2, key="L18-radial")
    _fig
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$ &nbsp; is not a gradient vector field!

    $\leadsto$ &nbsp; there is no function $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ such that $\vec{\nabla} f = \vec{F}$!

    How to decide if a vector field is a gradient or not?
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given $\vec{F} : D \subseteq \mathbb{R}^3 \longrightarrow \mathbb{R}^3$ differentiable, &nbsp; $\vec{F}(\vec{x}) = \begin{bmatrix} P(\vec{x}) \\ Q(\vec{x}) \\ R(\vec{x}) \end{bmatrix}$, &nbsp; the **curl** of $\vec{F}$ is the vector field

    <span class="chain">$\displaystyle \mathrm{Curl}(\vec{F})(\vec{x}) = (\vec{\nabla} \times \vec{F})(\vec{x}) = \begin{bmatrix} \dfrac{\partial R}{\partial y}(\vec{x}) - \dfrac{\partial Q}{\partial z}(\vec{x}) \\[10pt] \dfrac{\partial P}{\partial z}(\vec{x}) - \dfrac{\partial R}{\partial x}(\vec{x}) \\[10pt] \dfrac{\partial Q}{\partial x}(\vec{x}) - \dfrac{\partial P}{\partial y}(\vec{x}) \end{bmatrix}$ $\displaystyle = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ P(\vec{x}) & Q(\vec{x}) & R(\vec{x}) \end{bmatrix}$ $\displaystyle \quad \text{cross-product of } \vec{\nabla} \text{ and } \vec{F}(\vec{x})\,\text{!}$</span>
    """,
        "Curl",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$

    <span class="chain">$\displaystyle \leadsto \quad (\vec{\nabla} \times \vec{G})(\vec{x}) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ x & y & z \end{bmatrix}$ $\displaystyle = \begin{bmatrix} \dfrac{\partial}{\partial y} z - \dfrac{\partial}{\partial z} y \\[10pt] \dfrac{\partial}{\partial z} x - \dfrac{\partial}{\partial x} z \\[10pt] \dfrac{\partial}{\partial x} y - \dfrac{\partial}{\partial y} x \end{bmatrix}$ $\displaystyle = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$ $\displaystyle \quad \leadsto \ \text{flow has no rotation around } \vec{x}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    gt = mo.ui.slider(-0.5, 0.9, 0.02, value=0.6, label="$t$", show_value=True)
    return (gt,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, gt, mo, np, panel, sheet, turntable):
    # the flow of G(x) = x moves every point p to e^t p. A horizontal disc about x0 = (0.3, 1, 0.6), radius 0.45, with one
    # radius marked (pointing away from the viewer in the first view), is carried to the disc about e^t x0 of radius e^t 0.45: it grows
    # and moves out along the ray through x0 (the flow line gamma, red), and the marked radius keeps its direction (no turning).
    # The disc at t = 0 stays, dashed grey. The field G as in the curl figure of F: 36 arrows, each at 3/10 of its vector,
    # twelve on each of three circles of radius 1.3 about the ray, at 1, 2.2 and 3.4 along it
    _t = round(gt.value, 10)
    _e = np.exp(_t)
    def _circle(c, r):
        """The horizontal circle of radius r about c, as three arrays."""
        _a = np.linspace(0, 2 * np.pi, 121)
        return c[0] + r * np.cos(_a), c[1] + r * np.sin(_a), c[2] + 0 * _a

    _m = np.array([-np.sqrt(3) / 2, -0.5, 0.0])
    _x0, _rho = np.array([0.3, 1.0, 0.6]), 0.45
    _pale = "#a7bfad"  # GREEN halfway to white
    _c = _e * _x0

    def _disc(c, r):
        _r, _s = np.meshgrid(np.linspace(0, r, 6), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        return sheet(c[0] + _r * np.cos(_s), c[1] + _r * np.sin(_s), c[2] + 0 * _r, flat=LIGHT, alpha=0.9)

    _ray = np.linspace(0, 6.0, 80)[:, None] * _x0[None, :] / np.linalg.norm(_x0)  # long enough that gamma's name clears the largest disc and the arrows
    _u = _x0 / np.linalg.norm(_x0)
    _a = np.cross(_u, [0, 0, 1.0]); _a /= np.linalg.norm(_a)
    _b = np.cross(_u, _a)
    _pts = [_l * _u + 1.3 * (np.cos(np.radians((_j + _k / 2) * 30)) * _a + np.sin(np.radians((_j + _k / 2) * 30)) * _b)
            for _k, _l in enumerate((1.0, 2.2, 3.4)) for _j in range(12)]
    # and fainter, in the path of the disc: six on each of circles of radius 1/2 about the ray, at the same places along it
    _path = [_l * _u + 0.5 * (np.cos(np.radians(60 * _j + 30 * _k)) * _a + np.sin(np.radians(60 * _j + 30 * _k)) * _b)
             for _k, _l in enumerate((1.0, 2.2, 3.4)) for _j in range(6)]
    _fig = turntable(
        30, 35, "the flow of the radial vector field G carries a disc about x out along a ray; the disc grows and its marked radius keeps its direction",
        [panel(1.0, surfaces=[_disc(_c, _e * _rho)],
               lines=[(_ray[:, 0], _ray[:, 1], _ray[:, 2], RED, 1.6),
                      (*_circle(_x0, _rho), GREY, 1.0, [3, 3]), (*np.array([_x0, _x0 + _rho * _m]).T, GREY, 1.2, [3, 3]),
                      (*_circle(_c, _e * _rho), BLUE, 1.5), (*np.array([_c, _c + _e * _rho * _m]).T, BLUE, 2.0)],
               points=[(_x0, "#000000", 2.5)],
               arrows=[(p, 1.3 * p, GREEN, 1.3) for p in _pts] + [(p, 1.3 * p, _pale, 1.1) for p in _path],
               axes=[((0, 0, 0), (3.0, 0, 0), "x", -150), ((0, 0, 0), (0, 4.6, 0), "y", 0), ((0, 0, 0), (0, 0, 3.0), "z", 90)],
               texts=[(_x0, r"\vec{x}", "#000000", 180, 6), (_ray[-1], r"\gamma", RED, 30, 5),
                      ((0, -0.2, 2.6), r"\vec{G}(\vec{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}", GREEN, 180, 14)],
               box=((-0.2, 3.0), (-0.2, 4.6), (-0.2, 3.0)))],
        height=360, key="L18-flow-G")
    mo.vstack([mo.hstack([gt], justify="start"), _fig])
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$ $\displaystyle \quad \leadsto \quad (\vec{\nabla} \times \vec{F})(\vec{x}) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ -y & x & 1 \end{bmatrix}$ $\displaystyle = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$ $\displaystyle \quad \text{flow rotates around } \vec{x} \text{ with axis of rotation along the } z\text{-axis}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ft = mo.ui.slider(0, 3.14, 0.02, value=1.2, label="$t$", show_value=True)
    return (ft,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, ORANGE, RED, ft, mo, np, panel, sheet, turntable):
    # the flow of F(x) = (-y, x, 1) turns every point about the z-axis by the angle t and lifts it by t. A horizontal disc
    # about x0 = (2, 0, 1/2), radius 0.8, with one radius marked (pointing to the right of the first view), is carried along the
    # helix through x0 (gamma, red); the marked radius turns by the angle t about the vertical through the disc's centre, the
    # direction of curl F = (0, 0, 2), drawn from the centre in ochre (at full length) and named at its tip. The field as in
    # the helix figure (radius 3.4 here, twelve arrows at heights 1, 3 and 5). Heights at half scale, as in the helix figure
    _t = round(ft.value, 10)
    def _circle(c, r):
        """The horizontal circle of radius r about c, as three arrays."""
        _a = np.linspace(0, 2 * np.pi, 121)
        return c[0] + r * np.cos(_a), c[1] + r * np.sin(_a), c[2] + 0 * _a

    _x0, _rho = np.array([2.0, 0.0, 0.5]), 0.8
    _m0 = np.array([-0.5, np.sqrt(3) / 2, 0.0])

    def _flow(p, t):
        return np.array([p[0] * np.cos(t) - p[1] * np.sin(t), p[0] * np.sin(t) + p[1] * np.cos(t), p[2] + t])

    _c = _flow(_x0, _t)
    _m = _flow(_m0, _t) - np.array([0, 0, _t])  # the marked radius, turned by t

    def _disc(c, r):
        _r, _s = np.meshgrid(np.linspace(0, r, 6), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        return sheet(c[0] + _r * np.cos(_s), c[1] + _r * np.sin(_s), c[2] + 0 * _r, flat=LIGHT, alpha=0.9)

    def _F(p):
        return np.array([-p[1], p[0], 1.0])

    _pts = [np.array([3.4 * np.cos(np.radians((_j + _l / 2) * 30)), 3.4 * np.sin(np.radians((_j + _l / 2) * 30)), 1.0 + 2 * _l]) for _l in range(3) for _j in range(12)]
    _pts += [np.array([np.cos(np.radians((_j + _l / 2) * 60)), np.sin(np.radians((_j + _l / 2) * 60)), 1.0 + 2 * _l]) for _l in range(2) for _j in range(6)]  # and six on the circle of radius 1
    # and fainter, twelve on the circle of radius 2, through the middle of the disc (the circle of the helix); these two inner
    # circles only at the heights 1 and 3, where the disc passes, so that the names at the top stay clear
    _mid = [np.array([2 * np.cos(np.radians((_j + _l / 2) * 30)), 2 * np.sin(np.radians((_j + _l / 2) * 30)), 1.0 + 2 * _l]) for _l in range(2) for _j in range(12)]
    _pale = "#a7bfad"  # GREEN halfway to white, as in the flow figure of G
    _s = np.linspace(0, np.pi + 0.6, 120)
    _curl = _c + np.array([0, 0, 2.0])
    _fig = turntable(
        30, 40, "the flow of F carries a disc about x along a helix; the marked radius turns about the vertical through the disc's centre, the direction of curl F = [0; 0; 2]",
        [panel(0.5, surfaces=[_disc(_c, _rho)],
               lines=[(2 * np.cos(_s), 2 * np.sin(_s), 0.5 + _s, RED, 1.6),
                      (*_circle(_x0, _rho), GREY, 1.0, [3, 3]), (*np.array([_x0, _x0 + _rho * _m0]).T, GREY, 1.2, [3, 3]),
                      (*_circle(_c, _rho), BLUE, 1.5), (*np.array([_c, _c + _rho * _m]).T, BLUE, 2.0)],
               points=[(_x0, "#000000", 2.5)],
               axes=[((0, 0, 0), (4.2, 0, 0), "x", -150), ((0, 0, 0), (0, 4.2, 0), "y", 0), ((0, 0, 0), (0, 0, 5.6), "z", 90)],
               arrows=[(p, p + 0.3 * _F(p), GREEN, 1.3) for p in _pts] + [(p, p + 0.3 * _F(p), _pale, 1.1) for p in _mid] + [(_c, _curl, ORANGE, 2.2)],
               texts=[(_x0, r"\vec{x}", "#000000", -100, 6),
                      ((0, 4.6, 6.6), r"\vec{\nabla} \times \vec{F} = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}", ORANGE, 0, 0),
                      (_flow(np.array([2.0, 0, 0.5]), np.pi + 0.6), r"\gamma", RED, 90, 6),
                      ((0, -3.6, 6.0), r"\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}", GREEN, 180, 0)],
               box=((-3.6, 3.6), (-3.6, 3.6), (0, 6.0)))],
        height=420, key="L18-flow-F")
    mo.vstack([mo.hstack([ft], justify="start"), _fig])
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; $\mathrm{Curl}(\vec{F})(\vec{x})$ determines the axis of rotation and the rotation speed of the flow around $\vec{x}$.

    **Remark.** Curl is only defined for vector fields in $\mathbb{R}^3$!

    For $\vec{F} : \mathbb{R}^2 \longrightarrow \mathbb{R}^2$, we can define the “scalar curl” of $\vec{F}(x, y) = \begin{bmatrix} P(x, y) \\ Q(x, y) \end{bmatrix}$ as the scalar function $\dfrac{\partial Q}{\partial x}(x, y) - \dfrac{\partial P}{\partial y}(x, y)$, obtained from

    $$
    \begin{bmatrix} \partial / \partial x \\ \partial / \partial y \\ \partial / \partial z \end{bmatrix} \times \begin{bmatrix} P(x, y) \\ Q(x, y) \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ \dfrac{\partial Q}{\partial x}(x, y) - \dfrac{\partial P}{\partial y}(x, y) \end{bmatrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(corollary, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Gradient vector fields in $\mathbb{R}^3$ have zero curl!

    $$
    \mathrm{Curl}(\vec{\nabla} f) = \vec{\nabla} \times (\vec{\nabla} f) = \vec{0} \quad \longleftarrow \ \text{constant vector field}
    $$
    """,
                "Curl of a gradient",
            ),
            mo.md(
                r"""
    **Proof.**
    <span class="chain">$\displaystyle \vec{\nabla} \times (\vec{\nabla} f) = \det \begin{bmatrix} \vec{e}_1 & \vec{e}_2 & \vec{e}_3 \\ \partial / \partial x & \partial / \partial y & \partial / \partial z \\ \partial f / \partial x & \partial f / \partial y & \partial f / \partial z \end{bmatrix}$ $\displaystyle = \begin{bmatrix} \dfrac{\partial^2 f}{\partial y \partial z} - \dfrac{\partial^2 f}{\partial z \partial y} \\[10pt] \dfrac{\partial^2 f}{\partial z \partial x} - \dfrac{\partial^2 f}{\partial x \partial z} \\[10pt] \dfrac{\partial^2 f}{\partial x \partial y} - \dfrac{\partial^2 f}{\partial y \partial x} \end{bmatrix}$ $\displaystyle = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$</span>
    assuming $f$ is $C^2$-smooth… <span class=qed>$\square$</span>
    """
            ),
            corollary(r"""Gradient vector fields in $\mathbb{R}^2$ have zero scalar curl!""", "Scalar curl of a gradient"),
            corollary(r"""If a vector field $\vec{F}$ has non-zero curl (scalar curl for $n = 2$), it cannot be a gradient!""", "Non-zero curl"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** &nbsp; $\vec{F}(\vec{x}) = \begin{bmatrix} -y \\ x \\ 1 \end{bmatrix}$ &nbsp; $\leadsto$ &nbsp; $\vec{\nabla} \times \vec{F}(\vec{x}) = \begin{bmatrix} 0 \\ 0 \\ 2 \end{bmatrix}$

    $\Longrightarrow$ &nbsp; there cannot exist any potential function $f : \mathbb{R}^3 \longrightarrow \mathbb{R}$ such that $\vec{F} = \vec{\nabla} f$!
    """
            ),
            theorem(
                r"""
    $$
    \mathrm{Div}(\mathrm{Curl}(\vec{F})) = \vec{\nabla} \cdot (\vec{\nabla} \times \underbrace{\vec{F}}_{\mathclap{\footnotesize \text{assuming } C^2\text{-smooth}}\vphantom{\footnotesize \text{assuming } C^2\text{-smooth}}}) = 0 \quad \longleftarrow \ \text{constant function}
    $$
    """,
                "Divergence of a curl",
            ),
            mo.md(
                r"""
    <span class="chain">$\displaystyle \vec{\nabla} \cdot (\vec{\nabla} \times \vec{F}) = \frac{\partial}{\partial x}\left( \cancel{\frac{\partial R}{\partial y}} - \bcancel{\frac{\partial Q}{\partial z}} \right)$ $\displaystyle {} + \frac{\partial}{\partial y}\left( \xcancel{\frac{\partial P}{\partial z}} - \cancel{\frac{\partial R}{\partial x}} \right)$ $\displaystyle {} + \frac{\partial}{\partial z}\left( \bcancel{\frac{\partial Q}{\partial x}} - \xcancel{\frac{\partial P}{\partial y}} \right)$ $\displaystyle = 0$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ① &nbsp; $\vec{F}(\vec{x}) = \begin{bmatrix} yz \\ -xz \\ 0 \end{bmatrix}$ &emsp;&emsp; ② &nbsp; $\vec{G}(\vec{x}) = \begin{bmatrix} e^y \\ x e^y + z \\ y \end{bmatrix}$ &emsp;&emsp; ③ &nbsp; $\vec{H}(\vec{x}) = \begin{bmatrix} xy \\ yz \\ zx \end{bmatrix}$

    a) &nbsp; Compute the divergence and the curl.

    b) &nbsp; Can the vector field be a gradient?

    c) &nbsp; Can the vector field be a curl?
    """)
    return


if __name__ == "__main__":
    app.run()
