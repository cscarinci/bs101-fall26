"""Schematic sketches: manifolds as smooth closed shapes, open subsets, chart boxes, the maps between them.

One style for every such sketch in every lecture:
- the drawing is made at a fixed scale (inches per unit), so labels and lines have the same size in every sketch;
- shapes are smooth, gently rounded closed curves (no wobbly outlines);
- a manifold is black, an open set is drawn in its colour with a faint tint of it, an overlap in LIGHT;
- every label has the same size; names take the colour of what they name, everything else is black;
- shapes look drawn by hand, not like ellipses: gentle `waves` (2, 0.06, phase) and (3, 0.03, phase);
  stronger waves flatten or kink the outline;
- balance: a figure with two sides is a mirror image (maps of the same kind equally long, names on the outer
  sides); a manifold and its chart side by side sit at one height, the map between them level and centred;
- an arrow never touches a region: it starts and stops a little away from the shapes (use `rim(curve, angle, gap)`);
- a name sits at the edge of what it names (`rim`), a point's name right under or over it;
- a chart's image is an open set of R^m drawn over the axes of R^m (`axes`), the image of an overlap
  tinted LIGHT and cut by the other set's edge (`cut`).

    fig, ax = lk.sketch((0, 10), (0, 6))
    M = lk.shape(5, 4, 2.2, 1.6, egg=0.08)
    lk.outline(ax, M, name="$M$", at=(-1, 1))
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, Polygon

from .figures import LIGHT

INK = "#000000"
SCALE = 0.42  # inches per unit of a sketch
SIZE = 14  # every label
LW = 1.5  # every line


def sketch(xlim, ylim, scale=SCALE):
    """A blank drawing at the common scale: (fig, ax) with equal axes and no frame."""
    w, h = (xlim[1] - xlim[0]) * scale, (ylim[1] - ylim[0]) * scale
    fig = Figure(figsize=(w, h))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def shape(cx, cy, rx, ry, egg=0.0, bean=0.0, tilt=0.0, n=360, waves=()):
    """A smooth closed curve around (cx, cy): an ellipse with radii rx, ry, made a little egg-shaped
    (egg > 0: wider on the right, < 0: on the left) or bean-shaped (bean > 0: a soft dent at the top),
    given gentle `waves` ((k, amplitude, phase): r *= 1 + amplitude cos(k t + phase); k = 2, 3 and
    amplitudes 0.06 for k = 2 and 0.03 for k = 3 keep the outline smooth), and turned by `tilt` degrees. Returns an (n, 2) array."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1 + egg * np.cos(t) - bean * np.exp(-((t - np.pi / 2) ** 2) / 0.35)
    r = r + sum(a * np.cos(k * t + ph) for k, a, ph in waves)
    x, y = rx * r * np.cos(t), ry * r * np.sin(t)
    a = np.radians(tilt)
    return np.column_stack([cx + x * np.cos(a) - y * np.sin(a), cy + x * np.sin(a) + y * np.cos(a)])


def label(ax, xy, text, color=INK, ha="center", va="center", size=SIZE, **kw):
    """A label at a point, in the common size, with no box behind it."""
    ax.text(xy[0], xy[1], text, color=color, ha=ha, va=va, fontsize=size, **kw)


def outline(ax, curve, color=INK, name=None, at=None, tint=None, lw=None, **kw):
    """Draw a closed shape. A manifold: black, no tint. An open set: its colour, tinted.
    `name` goes at `at` (a point, or an offset from the centre when `rel=True` is passed)."""
    if tint is None:
        tint = color != INK
    if tint:
        ax.add_patch(Polygon(curve, closed=True, facecolor=color, alpha=0.07, lw=0, zorder=1))
    ax.add_patch(Polygon(curve, closed=True, fill=False, edgecolor=color, lw=lw or (LW + 0.2 if color == INK else LW),
                         joinstyle="round", zorder=3))
    if name:
        label(ax, at, name, color=color, **kw)
    return curve


def rim(curve, deg, gap=0.0):
    """The point of a closed curve seen from its centre in the direction `deg` (degrees), moved `gap`
    further out: where an arrow starts or stops (gap > 0, so that it does not touch) or a name sits."""
    c = curve.mean(0)
    d = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])
    rel = curve - c
    ang = np.abs(np.angle((rel[:, 0] + 1j * rel[:, 1]) * np.exp(-1j * np.radians(deg))))
    return curve[np.argmin(ang)] + gap * d


def axes(ax, x0, y0, w, h, name=r"$\mathbb{R}^m$"):
    """The two axes of R^m from (x0, y0), `w` and `h` long, the name at the end of the horizontal one."""
    for tip in ((x0 + w, y0), (x0, y0 + h)):
        maps(ax, (x0, y0), tip, lw=1.1)
    if name:
        label(ax, (x0 + w + 0.12, y0), name, ha="left", va="center")


def cut(ax, curve, inside, color):
    """The edge of `curve` where it runs inside the shape `inside`: the other set's edge across an image."""
    p = Polygon(curve, closed=True, fill=False, edgecolor=color, lw=LW, zorder=3)
    ax.add_patch(p)
    p.set_clip_path(Polygon(inside, closed=True, transform=ax.transData))


def overlap(ax, a, b, color=LIGHT):
    """Fill the overlap of two closed shapes (or boxes, as corner lists)."""
    clip = Polygon(b, closed=True, transform=ax.transData)
    p = Polygon(a, closed=True, facecolor=color, lw=0, zorder=2)
    ax.add_patch(p)
    p.set_clip_path(clip)


def box(x0, y0, w, h):
    """The corners of a chart box, as a closed shape."""
    return np.array([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]])


def chart(ax, x0, y0, w, h, color=INK, name=None, where="below"):
    """A chart's box in R^m, in the colour of its chart, its name under (or over) it. Returns the corners."""
    corners = box(x0, y0, w, h)
    ax.add_patch(Polygon(corners, closed=True, fill=False, edgecolor=color, lw=LW, zorder=3))
    if name:
        y = y0 - 0.25 if where == "below" else y0 + h + 0.25
        label(ax, (x0 + w / 2, y), name, color=color, va="top" if where == "below" else "bottom")
    return corners


def maps(ax, tail, tip, name=None, color=INK, bend=0.0, side=1, gap=0.32, lw=None, **kw):
    """A map drawn as an arrow from `tail` to `tip`, straight or bent (bend > 0 bends to the left of the
    direction of travel), its name beside the middle of the arc, on the side `side` (1 left, -1 right)."""
    lw = lw or LW
    ax.add_patch(FancyArrowPatch(tail, tip, connectionstyle=f"arc3,rad={-bend}", color=color, lw=lw, zorder=4,
                                 arrowstyle=f"-|>,head_length={4 * lw:g},head_width={1.25 * lw:g}",
                                 mutation_scale=1, shrinkA=0, shrinkB=0))
    if name:
        p, q = np.asarray(tail, float), np.asarray(tip, float)
        d = q - p
        nrm = np.array([-d[1], d[0]]) / np.hypot(*d)
        mid = (p + q) / 2 + bend * np.hypot(*d) / 2 * nrm  # the middle of the arc
        label(ax, mid + side * gap * nrm, name, color=color, **kw)


def dot(ax, xy, name=None, at=(0.0, -0.3), color=INK, **kw):
    """A point, its name at the offset `at`."""
    ax.plot(*xy, "o", color=color, ms=5, zorder=6)
    if name:
        kw.setdefault("va", "top" if at[1] < 0 else "bottom" if at[1] > 0 else "center")
        label(ax, (xy[0] + at[0], xy[1] + at[1]), name, color=color, **kw)


def band(ax, corners, side, cut, width=1.2, depth=0.3):
    """The image of an overlap inside a chart box (corners from `box`/`chart`): a band in LIGHT along its
    right (side=1) or left (side=-1) edge, `width` wide, cut by an arc in the colour `cut` of the other set.
    Returns the x of the band's middle, for its name."""
    (x0, y0), (x1, _), (_, y1) = corners[0], corners[1], corners[2]
    s = np.linspace(0, 1, 120)
    base = x1 - width if side == 1 else x0 + width
    xc = base - side * depth * np.sin(np.pi * s)
    edge = x1 if side == 1 else x0
    ys = y0 + (y1 - y0) * s
    ax.add_patch(Polygon(np.column_stack([np.r_[xc, [edge, edge]], np.r_[ys, [y1, y0]]]), facecolor=LIGHT, lw=0, zorder=2))
    ax.plot(xc, ys, color=cut, lw=LW, zorder=3)
    return (base - side * depth + edge) / 2


def path(p, direction, bend, s):
    """Points of a short path through p: p + s d + bend s^2 n, with d the unit direction and n its normal.
    Paths with the same direction and different bends have the same velocity at p."""
    d = np.asarray(direction, float) / np.hypot(*direction)
    n = np.array([-d[1], d[0]])
    s = np.asarray(s, float)
    return p[0] + s * d[0] + bend * s**2 * n[0], p[1] + s * d[1] + bend * s**2 * n[1]
