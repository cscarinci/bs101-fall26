"""Automatic numbering from the order of the cells in the notebook file.

The notebook source is scanned once: every numbered call (theorem(...), section(...), figure(...), ...)
gets its number from its position on the page. When a block is created at run time it looks up its own
entry by (cell, position within the cell), so moving, adding or removing modules renumbers everything,
including cross-references.
"""

import ast
import re
from pathlib import Path

from .kinds import COUNTERS

_cache = {"key": None, "table": None}
_runs = {}


def _context():
    try:
        from marimo._runtime.context import get_context

        return get_context()
    except Exception:
        return None


def _cell_codes(ctx):
    path = ctx.globals.get("__file__")
    if path and Path(path).is_file():
        try:
            from marimo._ast.parse import parse_notebook

            source = Path(path).read_text(encoding="utf-8")
            return tuple(cell.code for cell in parse_notebook(source).cells)
        except Exception:
            pass
    return tuple(cell.code for cell in ctx.graph.cells.values())


def _calls(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            name = func.attr if getattr(func.value, "id", None) == "lk" else None
        else:
            name = getattr(func, "id", None)
        if name in COUNTERS or name == "lecture":
            label = next(
                (k.value.value for k in node.keywords if k.arg == "label" and isinstance(k.value, ast.Constant)),
                None,
            )
            found.append((node.end_lineno, node.end_col_offset, name, label, node))
    found.sort(key=lambda c: (c[0], c[1]))  # arguments run before the call that holds them
    return found


def _lecture_number(node):
    args = [a.value for a in node.args if isinstance(a, ast.Constant)]
    kws = {k.arg: k.value.value for k in node.keywords if isinstance(k.value, ast.Constant)}
    return kws.get("number", args[0] if args else None)


def _build(codes):
    lecture = None
    counts = {"block": 0, "section": 0, "figure": 0}
    cells, labels = [], {}
    for code in codes:
        entries = []
        for *_, name, label, node in _calls(code):
            if name == "lecture":
                lecture = _lecture_number(node)
                continue
            counter = COUNTERS[name]
            number = None
            if counter:
                counts[counter] += 1
                number = counts[counter]
            entries.append({"kind": name, "counter": counter, "n": number, "label": label})
            if label:
                labels[label] = entries[-1]
        cells.append(entries)
    return {"lecture": lecture, "cells": cells, "labels": labels}


def table():
    ctx = _context()
    if ctx is None:
        return None
    codes = _cell_codes(ctx)
    if _cache["key"] != codes:
        _cache["key"], _cache["table"] = codes, _build(codes)
    return _cache["table"]


def _format(entry, t):
    if entry is None or entry["n"] is None:
        return None
    if entry["counter"] == "section" or t["lecture"] is None:
        return str(entry["n"])
    return f"{t['lecture']}.{entry['n']}"


def claim(kind):
    """Number for the next call of `kind` in the running cell, or None if it is unnumbered or unknown."""
    ctx = _context()
    t = table()
    if ctx is None or t is None or ctx.cell_id is None:
        return None
    run = ctx.execution_context
    seen = _runs.get(ctx.cell_id)
    if seen is None or seen[0] is not run:
        seen = _runs[ctx.cell_id] = [run, 0]
    position = seen[1]
    seen[1] += 1
    try:
        code = ctx.graph.cells[ctx.cell_id].code
        twins = [cid for cid, cell in ctx.graph.cells.items() if cell.code == code]  # cells with identical code
        rank = twins.index(ctx.cell_id)
        index = [i for i, c in enumerate(_cache["key"]) if c == code][rank]
        entries = t["cells"][index]
        entry = entries[position]
    except (KeyError, ValueError, IndexError):
        return "?"
    if entry["kind"] != kind:
        return "?"
    return _format(entry, t)


_MODULE = re.compile(r"^\s*# module:\s*(.+?)\s*$", re.M)


def _module(code):
    m = _MODULE.search(code)
    return m.group(1) if m else None


def starts_module():
    """True when the running cell is the first cell of a module that follows another module.
    (After a section heading, or the first module of the lecture, no mark: the heading already separates.)"""
    ctx = _context()
    t = table()
    if ctx is None or t is None or ctx.cell_id is None:
        return False
    try:
        code = ctx.graph.cells[ctx.cell_id].code
        twins = [cid for cid, cell in ctx.graph.cells.items() if cell.code == code]
        index = [i for i, c in enumerate(_cache["key"]) if c == code][twins.index(ctx.cell_id)]
    except (KeyError, ValueError, IndexError):
        return False
    here = _module(code)
    before = _module(_cache["key"][index - 1]) if index > 0 else None
    return bool(here and before and here != before)


def lookup(label):
    t = table()
    if t is None or label not in t["labels"]:
        return None, None
    entry = t["labels"][label]
    return entry["kind"], _format(entry, t)
