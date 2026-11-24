"""Figure palette and matplotlib defaults. Colours have fixed roles across all lectures."""

import matplotlib
from matplotlib.figure import Figure

BLUE = "#3f5f8f"  # the primary object
RED = "#a8554c"  # the object it is compared with
GREEN = "#4f7f5c"  # a result made from them
ORANGE = "#b9853f"  # a third object, only when three are needed
GREY = "#9a9a9a"  # reference geometry
LIGHT = "#e3ebf4"  # fills and grids

FULL, HALF = 7.4, 3.6  # figure widths in inches

matplotlib.rcParams.update(
    {
        "font.size": 13,
        "font.family": "serif",
        "font.serif": ["cmr10", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": GREY,
        "savefig.bbox": "tight",
        "savefig.format": "svg",
    }
)


def canvas(width=FULL, height=3.2, xlim=None, ylim=None):
    """A blank figure with one axes in the course style. Returns (fig, ax)."""
    fig = Figure(figsize=(width, height))
    ax = fig.add_subplot()
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    return fig, ax


def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
    """The vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
    The head is sized in points from the line width, so arrows look alike whatever the axis range."""
    ax.annotate(
        "",
        xy=tip,
        xytext=tail,
        arrowprops={"arrowstyle": f"-|>,head_length={4 * lw:g},head_width={1.25 * lw:g}", "mutation_scale": 1,
                    "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
    )
    if label:
        pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
        ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)
