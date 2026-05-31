"""Core conversion API."""

from __future__ import annotations

import ast
import json
from collections import deque
from dataclasses import dataclass
from decimal import Decimal
from functools import cache
from importlib.resources import files
from typing import Any, Iterable, TypeAlias, cast

from unit_converter.exceptions import (
    AmbiguousConversionError,
    ConversionError,
    ConversionNotFoundError,
    IncompatibleUnitError,
    UnitNotFoundError,
)

Number: TypeAlias = int | float | str | Decimal
Context: TypeAlias = tuple[str | None, str | None]


@dataclass(frozen=True)
class Conversion:
    """A direct conversion rule between two units."""

    from_unit: str
    to_unit: str
    factor: str | Decimal | None = None
    formula: str | None = None
    category: str | None = None
    subcategory: str | None = None

    def __post_init__(self) -> None:
        if (self.factor is None) == (self.formula is None):
            raise ValueError("Exactly one of factor or formula must be provided.")

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> Conversion:
        return cls(
            from_unit=str(value["from"]),
            to_unit=str(value["to"]),
            factor=value.get("factor"),
            formula=value.get("formula"),
            category=value.get("category"),
            subcategory=value.get("subcategory"),
        )

    def apply(self, value: Number) -> Decimal:
        decimal_value = _to_decimal(value)
        if self.factor is not None:
            return decimal_value * _to_decimal(self.factor)
        if self.formula is not None:
            return _evaluate_formula(self.formula, decimal_value)
        raise ConversionError("Conversion has neither factor nor formula.")

    def apply_inverse(self, value: Number) -> Decimal:
        decimal_value = _to_decimal(value)
        if self.factor is not None:
            return decimal_value / _to_decimal(self.factor)
        if self.formula is not None:
            return _evaluate_inverse_formula(self.formula, decimal_value)
        raise ConversionError("Conversion has neither factor nor formula.")

    def can_apply_inverse(self) -> bool:
        if self.factor is not None:
            return True
        if self.formula is None:
            return False
        return _can_invert_formula(self.formula)

    @property
    def context(self) -> Context:
        return self.category, self.subcategory


@dataclass(frozen=True)
class _Edge:
    to_unit: str
    conversion: Conversion
    reverse: bool = False

    def apply(self, value: Decimal) -> Decimal:
        if self.reverse:
            return self.conversion.apply_inverse(value)
        return self.conversion.apply(value)


@dataclass(frozen=True)
class _PathResult:
    value: Decimal
    path: tuple[_Edge, ...]


class UnitConverter:
    """In-memory unit conversion registry."""

    def __init__(self, conversions: Iterable[Conversion]) -> None:
        self._all_conversions = tuple(conversions)
        self._conversions: dict[tuple[str, str], list[Conversion]] = {}
        self._adjacency: dict[str, list[_Edge]] = {}
        self._unit_contexts: dict[str, set[Context]] = {}
        direct_pairs = {
            (conversion.from_unit, conversion.to_unit)
            for conversion in self._all_conversions
        }

        for conversion in self._all_conversions:
            key = (conversion.from_unit, conversion.to_unit)
            self._conversions.setdefault(key, []).append(conversion)
            self._add_unit_context(conversion.from_unit, conversion.context)
            self._add_unit_context(conversion.to_unit, conversion.context)
            self._adjacency.setdefault(conversion.from_unit, []).append(
                _Edge(conversion.to_unit, conversion)
            )
            if (
                conversion.can_apply_inverse()
                and (conversion.to_unit, conversion.from_unit) not in direct_pairs
            ):
                self._adjacency.setdefault(conversion.to_unit, []).append(
                    _Edge(conversion.from_unit, conversion, reverse=True)
                )

    @classmethod
    def from_package_data(cls) -> UnitConverter:
        data = _load_package_data()
        return cls(Conversion.from_mapping(row) for row in data["conversions"])

    def available(self) -> tuple[tuple[str, str], ...]:
        return tuple(sorted(self._conversions))

    def available_units(self) -> tuple[str, ...]:
        return tuple(sorted(self._unit_contexts))

    def convert(
        self,
        value: Number,
        from_unit: str,
        to_unit: str,
    ) -> Decimal:
        self._validate_units(from_unit, to_unit)
        if from_unit == to_unit:
            return _to_decimal(value)

        paths = self._find_paths(value, from_unit, to_unit)
        if len(paths) == 1:
            return paths[0].value
        if len(paths) > 1:
            self._raise_ambiguous_path(from_unit, to_unit, paths)

        self._raise_no_path(from_unit, to_unit)

    def _add_unit_context(self, unit: str, context: Context) -> None:
        self._unit_contexts.setdefault(unit, set()).add(context)

    def _validate_units(self, from_unit: str, to_unit: str) -> None:
        missing = [
            unit
            for unit in (from_unit, to_unit)
            if unit not in self._unit_contexts
        ]
        if missing:
            formatted = ", ".join(repr(unit) for unit in missing)
            raise UnitNotFoundError(f"Unknown unit(s): {formatted}.")

    def _find_paths(
        self,
        value: Number,
        from_unit: str,
        to_unit: str,
    ) -> list[_PathResult]:
        start_value = _to_decimal(value)
        queue: deque[tuple[str, Decimal, tuple[_Edge, ...], frozenset[str]]] = deque(
            [(from_unit, start_value, (), frozenset({from_unit}))]
        )
        found_depth: int | None = None
        results: list[_PathResult] = []

        while queue:
            current_unit, current_value, path, seen_units = queue.popleft()
            if found_depth is not None and len(path) >= found_depth:
                continue

            for edge in self._adjacency.get(current_unit, []):
                if edge.to_unit in seen_units:
                    continue

                next_path = (*path, edge)
                next_value = edge.apply(current_value)
                if edge.to_unit == to_unit:
                    found_depth = len(next_path)
                    results.append(_PathResult(next_value, next_path))
                    continue

                if found_depth is None:
                    queue.append(
                        (
                            edge.to_unit,
                            next_value,
                            next_path,
                            seen_units | {edge.to_unit},
                        )
                    )

        return results

    def _raise_ambiguous_path(
        self,
        from_unit: str,
        to_unit: str,
        paths: list[_PathResult],
    ) -> None:
        contexts = ", ".join(
            sorted(
                {
                    format_context(*edge.conversion.context)
                    for path in paths
                    for edge in path.path
                }
            )
        )
        raise AmbiguousConversionError(
            f"Multiple conversion paths found from {from_unit!r} to {to_unit!r}. "
            "The conversion data contains multiple matching paths. "
            f"Available contexts: {contexts}."
        )

    def _raise_no_path(self, from_unit: str, to_unit: str) -> None:
        raise IncompatibleUnitError(
            f"No conversion path found from {from_unit!r} to {to_unit!r}"
            ". Units may belong to different physical quantities. "
            f"{from_unit!r} appears in: {self._format_unit_contexts(from_unit)}. "
            f"{to_unit!r} appears in: {self._format_unit_contexts(to_unit)}."
        )

    def _format_unit_contexts(self, unit: str) -> str:
        return ", ".join(
            sorted(format_context(*context) for context in self._unit_contexts[unit])
        )


def convert(
    value: Number,
    from_unit: str,
    to_unit: str,
) -> Decimal:
    """Convert a value using the package's bundled conversion table."""

    return _package_converter().convert(value, from_unit, to_unit)


@cache
def _package_converter() -> UnitConverter:
    return UnitConverter.from_package_data()


def format_context(category: str | None, subcategory: str | None) -> str:
    if category is None:
        return "<uncategorized>"
    if subcategory is None:
        return category
    return f"{category} / {subcategory}"


def _load_package_data() -> dict[str, Any]:
    data_path = files("unit_converter.data").joinpath("conversions.json")
    with data_path.open(encoding="utf-8") as handle:
        return cast(dict[str, Any], json.load(handle))


def _to_decimal(value: Number) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _evaluate_formula(formula: str, x: Decimal) -> Decimal:
    try:
        expression = ast.parse(formula, mode="eval")
    except SyntaxError as error:
        raise ConversionError(f"Invalid conversion formula: {formula!r}.") from error
    return _eval_node(expression.body, x)


def _evaluate_inverse_formula(formula: str, y: Decimal) -> Decimal:
    affine = _formula_to_affine(formula)
    if affine is not None:
        slope, intercept = affine
        if slope == 0:
            raise ConversionNotFoundError(
                f"Cannot invert constant formula: {formula!r}."
            )
        return (y - intercept) / slope

    reciprocal_constant = _formula_to_reciprocal_constant(formula)
    if reciprocal_constant is not None:
        return reciprocal_constant / y

    raise ConversionNotFoundError(f"Cannot invert formula: {formula!r}.")


def _can_invert_formula(formula: str) -> bool:
    affine = _formula_to_affine(formula)
    if affine is not None:
        slope, _ = affine
        return slope != 0
    return _formula_to_reciprocal_constant(formula) is not None


def _eval_node(node: ast.AST, x: Decimal) -> Decimal:
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, int | float) and not isinstance(value, bool):
            return Decimal(str(value))

    if isinstance(node, ast.Name) and node.id == "x":
        return x

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, x)
        right = _eval_node(node.right, x)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Pow):
            return left**right
        if isinstance(node.op, ast.Sub):
            return left - right
        raise ConversionError(f"Unsupported formula operator: {type(node.op)}.")

    if isinstance(node, ast.UnaryOp):
        value = _eval_node(node.operand, x)
        if isinstance(node.op, ast.UAdd):
            return value
        if isinstance(node.op, ast.USub):
            return -value
        raise ConversionError(f"Unsupported formula operator: {type(node.op)}.")

    raise ConversionError(f"Unsupported formula syntax: {ast.dump(node)}.")


def _formula_to_affine(formula: str) -> tuple[Decimal, Decimal] | None:
    try:
        expression = ast.parse(formula, mode="eval")
    except SyntaxError:
        return None
    return _linearize_node(expression.body)


def _linearize_node(node: ast.AST) -> tuple[Decimal, Decimal] | None:
    if isinstance(node, ast.Constant):
        constant = _constant_decimal(node)
        if constant is None:
            return None
        return Decimal("0"), constant

    if isinstance(node, ast.Name) and node.id == "x":
        return Decimal("1"), Decimal("0")

    if isinstance(node, ast.UnaryOp):
        value = _linearize_node(node.operand)
        if value is None:
            return None
        slope, intercept = value
        if isinstance(node.op, ast.UAdd):
            return slope, intercept
        if isinstance(node.op, ast.USub):
            return -slope, -intercept
        return None

    if isinstance(node, ast.BinOp):
        left = _linearize_node(node.left)
        right = _linearize_node(node.right)
        if left is None or right is None:
            return None
        left_slope, left_intercept = left
        right_slope, right_intercept = right

        if isinstance(node.op, ast.Add):
            return left_slope + right_slope, left_intercept + right_intercept
        if isinstance(node.op, ast.Sub):
            return left_slope - right_slope, left_intercept - right_intercept
        if isinstance(node.op, ast.Mult):
            if left_slope == 0:
                return right_slope * left_intercept, right_intercept * left_intercept
            if right_slope == 0:
                return left_slope * right_intercept, left_intercept * right_intercept
            return None
        if isinstance(node.op, ast.Div):
            if right_slope != 0 or right_intercept == 0:
                return None
            return left_slope / right_intercept, left_intercept / right_intercept

    return None


def _formula_to_reciprocal_constant(formula: str) -> Decimal | None:
    try:
        expression = ast.parse(formula, mode="eval")
    except SyntaxError:
        return None
    node = expression.body
    if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Div):
        return None
    constant = _constant_decimal(node.left)
    if constant is None:
        return None
    if isinstance(node.right, ast.Name) and node.right.id == "x":
        return constant
    return None


def _constant_decimal(node: ast.AST) -> Decimal | None:
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, int | float) and not isinstance(value, bool):
            return Decimal(str(value))
    if isinstance(node, ast.UnaryOp):
        value = _constant_decimal(node.operand)
        if value is None:
            return None
        if isinstance(node.op, ast.UAdd):
            return value
        if isinstance(node.op, ast.USub):
            return -value
    return None
