"""Interactive 3D figures, drawn in the browser on canvases in the style of the static figures.

Orthographic views of R^3 (x towards the viewer, y to the right, z up), surfaces drawn back to front.
Dragging turns the view at a fixed scale (all panels of a figure together) and a double click restores it;
a figure redrawn by a slider keeps its view. Names sit beside the objects they name; typesetting by KaTeX.

The page drawn in each frame is view3d.html, beside this file.
"""

import html as _html
import json as _json
from importlib import resources

import marimo as mo
import numpy as np

_PAGE = resources.files(__package__).joinpath("view3d.html").read_text(encoding="utf-8")


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


# One size for every 3D figure, so the same object looks the same size everywhere.
# A flat object (a disk seen from the side) gets the lower height; side-by-side panels keep the same height.
H3D = 340
H3D_FLAT = 260


def panel(ys, surfaces=(), lines=(), points=(), axes=(), arrows=(), arcs=(), texts=(), caption=None, box=None, outlines=()):
    """One drawing of a 3D figure, with heights at the scale `ys`.
    lines: (x1, x2, y, colour, width[, dash, depth offset]); points: ((x^1, x^2, y), colour[, radius, hollow]);
    axes: (tail, tip, TeX label, direction of the label in degrees), drawn black;
    arrows: (tail, tip, colour[, width, dash]), vectors with a head in their colour;
    arcs: (x1, x2, y, colour[, width]), curves ending in a head, such as a turning arrow;
    texts: ((x^1, x^2, y), TeX, colour, direction[, distance]), names of points and objects and tick values,
    each beside its point; caption: TeX below the drawing;
    box: ((x^1 lo, hi), (x^2 lo, hi), (y lo, hi)) to size the drawing by, instead of its own points;
    outlines: the edge of a round surface as seen from the current view, redrawn as the figure turns (ys = 1):
    ("sphere", centre, radius, colour, width), ("cylinder", (x^1, x^2) of the vertical axis, radius, (y lo, y hi), colour, width),
    ("cone", vertex, height, colour, width) for the vertical double cone of slope 1 (a light cone),
    ("surface", (x1, x2, y), (n1, n2, n3), colour, width) for any smooth surface given on a grid (2D arrays) with its
    unit normals at the grid points (NaN leaves a grid cell out): the curve where the surface turns away from the viewer (a torus, a genus 2 surface)."""
    p = {"ys": ys, "surfaces": list(surfaces), "lines": [], "points": [], "heads": [], "labels": [], "caption": caption, "box": box, "outlines": []}
    for o in outlines:
        if o[0] == "sphere":
            p["outlines"].append({"k": "sphere", "p": [float(c) for c in o[1]], "r": float(o[2]), "c": o[3], "w": o[4]})
        elif o[0] == "cylinder":
            p["outlines"].append({"k": "cylinder", "p": [float(c) for c in o[1]], "r": float(o[2]), "z": [float(c) for c in o[3]], "c": o[4], "w": o[5]})
        elif o[0] == "cone":
            p["outlines"].append({"k": "cone", "p": [float(c) for c in o[1]], "h": float(o[2]), "c": o[3], "w": o[4]})
        elif o[0] == "surface":
            n, m = np.shape(o[1][0])
            p["outlines"].append({"k": "surface", "n": n, "m": m, "v": _flat(*o[1]), "q": [None if c != c else c for c in _flat(*o[2])], "c": o[3], "w": o[4]})
    for ln in lines:
        p["lines"].append({"p": _flat(*ln[:3]), "c": ln[3], "w": ln[4], "d": ln[5] if len(ln) > 5 else None, "e": ln[6] if len(ln) > 6 else 0})
    for tail, tip, label, d in axes:
        a, b = np.asarray(tail, float), np.asarray(tip, float)
        seg = a + np.linspace(0, 0.96, 60)[:, None] * (b - a)
        p["lines"].append({"p": _flat(*seg.T), "c": "#000000", "w": 1.35, "d": None, "b": 1})
        p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": "#000000", "w": 1.35})
        p["labels"].append({"p": b.tolist(), "t": label, "c": "#000000", "a": d, "r": 5})
    for q in points:
        p["points"].append({"p": [float(c) for c in q[0]], "c": q[1], "r": q[2] if len(q) > 2 else 4.0, "h": bool(q[3]) if len(q) > 3 else False})
    for ar in arrows:
        a, b = np.asarray(ar[0], float), np.asarray(ar[1], float)
        seg = a + np.linspace(0, 0.96, 40)[:, None] * (b - a)
        w = ar[3] if len(ar) > 3 else 1.8
        d = ar[4] if len(ar) > 4 else None
        p["lines"].append({"p": _flat(*seg.T), "c": ar[2], "w": w, "d": d, "e": 0, "b": 1})
        p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": ar[2], "w": w, "d": d})
    for arc in arcs:
        c = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in arc[:3])), -1)
        w = arc[4] if len(arc) > 4 else 1.8
        p["lines"].append({"p": _flat(*c[:-1].T), "c": arc[3], "w": w, "d": None, "e": 0})
        p["heads"].append({"p": c[-1].tolist(), "q": c[max(0, len(c) - 4)].tolist(), "c": arc[3], "w": w})
    for tx in texts:
        p["labels"].append({"p": [float(c) for c in tx[0]], "t": tx[1], "c": tx[2], "a": tx[3], "r": tx[4] if len(tx) > 4 else 5})
    return p


def turntable(az, el, alt, panels, legend=(), height=H3D, width=None, cols=1, key=None, shared=True, bias=0.03, apart=False, zoom=1.0):
    """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
    from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
    at most `width` wide, with a legend box beside them (below them on narrow screens). `alt` is the text
    for screen readers. `key` names the view so that it survives a redraw; with `shared`, all panels have one scale.
    legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area".
    zoom: draw larger than the ball that holds the scene in every view (e.g. 1.3 for a long, flat graph whose
    ball wastes most of the frame); parts may then leave the frame in some views while turning.
    apart: only the scene, for a figure with sliders. Build it in its own cell (its output is invisible) and show
    frame(key, height) in the figure's cell: moving a slider then redraws the figure in place, keeping its view."""
    scene = {"az": az, "el": el, "h": height, "bias": bias, "panels": list(panels), "legend": [], "key": key, "shared": shared,
             "maxw": width or cols * height + (cols - 1) * 56, "cols": cols, "alt": alt, "zoom": zoom}
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
    return mo.Html(f'<div class="bs3d" style="--lk-3d-w: {scene["maxw"]}px">{_frame(height)}<div hidden data-scene="{data}"></div></div>')


def _frame(height, key=""):
    return f'<iframe srcdoc="{_html.escape(_PAGE)}" data-bs3d="{_html.escape(key)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>'


def frame(key, height=H3D, width=None):
    """The frame of the figure turntable(..., key=key, height=height, apart=True), built in another cell.
    `width`: the width of its drawings, if not `height` (one square panel), so that lk.maps can fit it."""
    return mo.Html(f'<div class="bs3d" style="--lk-3d-w: {width or height}px">{_frame(height, key)}</div>')
