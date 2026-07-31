"""Internal access to bundled JSON resources."""

from __future__ import annotations

import json
from functools import cache
from importlib.resources import files
from typing import Any, cast


@cache
def load_json_data(filename: str) -> dict[str, Any]:
    """Load and cache an internal package data file."""

    data_path = files("unit_converter.data").joinpath(filename)
    with data_path.open(encoding="utf-8") as handle:
        return cast(dict[str, Any], json.load(handle))
