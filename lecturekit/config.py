"""Course settings: read from course.toml beside the notebook, overridable per lecture with configure()."""

import tomllib
from pathlib import Path

DEFAULTS = {
    "code": "",
    "name": "",
    "institution": "",
    "instructor": "",
    "labels": "full",  # short (Def, Thm, Rmk) | full (Definition, Theorem, Remark)
    "proofs": "open",  # open | collapsed
    "solutions": "collapsed",  # open | collapsed | hidden
}

_settings = dict(DEFAULTS)
_loaded_from = None


def _notebook_dir():
    try:
        import marimo as mo

        return Path(mo.notebook_dir())
    except Exception:
        return None


def _load():
    global _loaded_from
    folder = _notebook_dir() or Path(".")
    if folder == _loaded_from:
        return
    _loaded_from = folder
    baked = Path(__file__).with_name("_course.toml")  # written into the wheel by build.py for the website
    for candidate in (folder / "course.toml", folder.parent / "course.toml", baked):
        if candidate.is_file():
            with candidate.open("rb") as f:
                _settings.update(tomllib.load(f).get("course", {}))
            return


def configure(**options):
    """Override course settings for this lecture, e.g. configure(proofs="collapsed")."""
    _load()
    unknown = set(options) - set(DEFAULTS)
    if unknown:
        raise ValueError(f"unknown setting(s): {', '.join(sorted(unknown))}")
    _settings.update(options)


def setting(name):
    _load()
    return _settings[name]
