"""lecturekit: building blocks and style for marimo lecture notes.

In a lecture:  import lecturekit as lk
"""

from . import blocks as _blocks
from .blocks import aside, gloss, prose, ref
from .config import configure
from .figures import BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, canvas
from . import sketch as sk
from .kinds import KINDS as _KINDS
from .view3d import H3D, H3D_FLAT, frame, panel, patch, sheet, turntable
from .layout import chain, figure, gap, goals, interactive, lecture, maps, module, recap, references, section, side, slider, summary, table, under

globals().update({_kind: getattr(_blocks, _kind) for _kind in _KINDS})

__version__ = "0.1.0"
