"""Core conversion API."""

from __future__ import annotations

import ast
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal, DecimalException
from fractions import Fraction
from functools import cache
from typing import Any, NoReturn, TypeAlias

from unit_converter._data import load_json_data
from unit_converter.exceptions import (
    AmbiguousConversionError,
    ConversionError,
    ConversionNotFoundError,
    IncompatibleUnitError,
    UnitNotFoundError,
)

Number: TypeAlias = int | float | str | Decimal
# NIST B.9 rounds non-exact factors to the published significant digits, so
# independently rounded routes can differ at sub-ppm scale.
_FACTOR_EQUIVALENCE_RELATIVE_TOLERANCE = Fraction(1, 1_000_000)
_CONVERSION_DATA_VERSION = 2
_UNIT_CATALOG_VERSION = 3


@dataclass(frozen=True)
class Conversion:
    """A direct conversion rule between two units."""

    from_unit: str
    to_unit: str
    factor: str | Decimal | None = None
    formula: str | None = None

    def __post_init__(self) -> None:
        if (self.factor is None) == (self.formula is None):
            raise ConversionError("Exactly one of factor or formula must be provided.")
        if not self.from_unit or not self.to_unit:
            raise ConversionError("Conversion unit names must not be empty.")
        if self.factor is not None:
            factor = _to_decimal(self.factor, role="factor")
            if factor == 0:
                raise ConversionError("Conversion factor must not be zero.")
        if self.formula is not None:
            _parse_formula(self.formula)

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> Conversion:
        return cls(
            from_unit=str(value["from"]),
            to_unit=str(value["to"]),
            factor=value.get("factor"),
            formula=value.get("formula"),
        )

    def apply(self, value: Number) -> Decimal:
        decimal_value = _to_decimal(value)
        if self.factor is not None:
            try:
                result = decimal_value * _to_decimal(self.factor, role="factor")
            except DecimalException as error:
                raise ConversionError(
                    f"Factor conversion failed for value {value!r}."
                ) from error
            return _require_finite(result, "Factor conversion")
        if self.formula is not None:
            return _evaluate_formula(self.formula, decimal_value)
        raise ConversionError("Conversion has neither factor nor formula.")

    def apply_inverse(self, value: Number) -> Decimal:
        decimal_value = _to_decimal(value)
        if self.factor is not None:
            try:
                result = decimal_value / _to_decimal(self.factor, role="factor")
            except DecimalException as error:
                raise ConversionError(
                    f"Inverse factor conversion failed for value {value!r}."
                ) from error
            return _require_finite(result, "Inverse factor conversion")
        if self.formula is not None:
            return _evaluate_inverse_formula(self.formula, decimal_value)
        raise ConversionError("Conversion has neither factor nor formula.")

    def can_apply_inverse(self) -> bool:
        if self.factor is not None:
            return True
        if self.formula is None:
            return False
        return _can_invert_formula(self.formula)


@dataclass(frozen=True)
class _Edge:
    to_unit: str
    conversion: Conversion
    reverse: bool = False

    def apply(self, value: Decimal) -> Decimal:
        if self.reverse:
            return self.conversion.apply_inverse(value)
        return self.conversion.apply(value)


Path: TypeAlias = tuple[_Edge, ...]


@dataclass(frozen=True)
class _UnitIdentity:
    unit_id: str
    quantity_id: str
    display_name: str
    aliases: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> _UnitIdentity:
        return cls(
            unit_id=str(value["unit_id"]),
            quantity_id=str(value["quantity_id"]),
            display_name=str(value["display_name"]),
            aliases=tuple(str(alias) for alias in value["aliases"]),
        )


class UnitConverter:
    """In-memory unit conversion registry."""

    def __init__(self, conversions: Iterable[Conversion]) -> None:
        conversion_rules = tuple(conversions)
        self._direct_pairs = frozenset(
            (conversion.from_unit, conversion.to_unit)
            for conversion in conversion_rules
        )
        self._adjacency: dict[str, list[_Edge]] = {}
        units: set[str] = set()
        self._unit_lookup: dict[str, str] = {}
        self._display_names: dict[str, str] = {}
        self._quantity_ids: dict[str, str] | None = None

        for conversion in conversion_rules:
            units.update((conversion.from_unit, conversion.to_unit))
            self._adjacency.setdefault(conversion.from_unit, []).append(
                _Edge(conversion.to_unit, conversion)
            )
            if (
                conversion.can_apply_inverse()
                and (conversion.to_unit, conversion.from_unit)
                not in self._direct_pairs
            ):
                self._adjacency.setdefault(conversion.to_unit, []).append(
                    _Edge(conversion.from_unit, conversion, reverse=True)
                )

        self._units = frozenset(units)
        for unit in self._units:
            self._unit_lookup[unit] = unit
            self._display_names[unit] = unit

    @classmethod
    def from_package_data(cls) -> UnitConverter:
        data = load_json_data("conversions.json")
        catalog = load_json_data("unit_catalog.json")
        _require_data_version("conversion data", data, _CONVERSION_DATA_VERSION)
        _require_data_version("unit catalog", catalog, _UNIT_CATALOG_VERSION)
        identities = tuple(_UnitIdentity.from_mapping(row) for row in catalog["units"])
        unit_id_by_display_name = {
            identity.display_name: identity.unit_id for identity in identities
        }
        conversions = []
        for row in data["conversions"]:
            mapped_row = dict(row)
            try:
                mapped_row["from"] = unit_id_by_display_name[str(row["from"])]
                mapped_row["to"] = unit_id_by_display_name[str(row["to"])]
            except KeyError as error:
                raise ConversionError(
                    "Conversion data references an unregistered unit: "
                    f"{error.args[0]!r}."
                ) from error
            conversions.append(Conversion.from_mapping(mapped_row))
        converter = cls(conversions)
        converter._configure_unit_identities(identities)
        return converter

    def available(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            sorted(
                (
                    self._display_unit(from_unit),
                    self._display_unit(to_unit),
                )
                for from_unit, to_unit in self._direct_pairs
            )
        )

    def available_units(self) -> tuple[str, ...]:
        return tuple(sorted(self._display_unit(unit) for unit in self._units))

    def available_unit_ids(self) -> tuple[str, ...]:
        """Return stable unit IDs, or unit names for a custom converter."""

        return tuple(sorted(self._units))

    def can_convert(self, from_unit: str, to_unit: str) -> bool:
        """Return whether a conversion path is available for two unit keys."""

        if from_unit not in self._unit_lookup or to_unit not in self._unit_lookup:
            return False
        resolved_from = self._unit_lookup[from_unit]
        resolved_to = self._unit_lookup[to_unit]
        return self._can_convert_resolved(resolved_from, resolved_to)

    def compatible_units(self, unit: str) -> tuple[str, ...]:
        """Return display names reachable from ``unit``."""

        resolved_unit = self._resolve_unit(unit)
        return tuple(
            sorted(
                self._display_unit(candidate)
                for candidate in self._units
                if self._can_convert_resolved(resolved_unit, candidate)
            )
        )

    def convert(
        self,
        value: Number,
        from_unit: str,
        to_unit: str,
    ) -> Decimal:
        resolved_from, resolved_to = self._resolve_units(from_unit, to_unit)
        if resolved_from == resolved_to:
            return _to_decimal(value)

        paths = self._find_paths(resolved_from, resolved_to)
        if len(paths) == 1:
            return _apply_path(value, paths[0])
        if len(paths) > 1:
            factor = _select_equivalent_factor(paths)
            if factor is not None:
                return _apply_factor(value, factor)
            self._raise_ambiguous_path(from_unit, to_unit, paths)

        self._raise_no_path(from_unit, to_unit)

    def _configure_unit_identities(
        self,
        identities: Iterable[_UnitIdentity],
    ) -> None:
        unit_lookup: dict[str, str] = {}
        display_names: dict[str, str] = {}
        quantity_ids: dict[str, str] = {}

        for identity in identities:
            if identity.unit_id in display_names:
                raise ConversionError(
                    f"Duplicate stable unit ID: {identity.unit_id!r}."
                )
            display_names[identity.unit_id] = identity.display_name
            quantity_ids[identity.unit_id] = identity.quantity_id
            for lookup_key in (
                identity.unit_id,
                identity.display_name,
                *identity.aliases,
            ):
                previous = unit_lookup.get(lookup_key)
                if previous is not None and previous != identity.unit_id:
                    raise ConversionError(
                        f"Unit lookup key {lookup_key!r} is ambiguous."
                    )
                unit_lookup[lookup_key] = identity.unit_id

        graph_units = set(self._units)
        identity_units = set(display_names)
        if graph_units != identity_units:
            missing = sorted(graph_units - identity_units)
            extra = sorted(identity_units - graph_units)
            raise ConversionError(
                "Stable unit registry does not match the conversion graph: "
                f"missing={missing}, extra={extra}."
            )
        for from_unit, to_unit in self._direct_pairs:
            if quantity_ids[from_unit] != quantity_ids[to_unit]:
                raise ConversionError(
                    "A direct conversion crosses stable physical quantities: "
                    f"{from_unit!r} -> {to_unit!r}."
                )

        self._unit_lookup = unit_lookup
        self._display_names = display_names
        self._quantity_ids = quantity_ids

    def _can_convert_resolved(self, from_unit: str, to_unit: str) -> bool:
        if from_unit == to_unit:
            return True
        if (
            self._quantity_ids is not None
            and self._quantity_ids[from_unit] != self._quantity_ids[to_unit]
        ):
            return False
        paths = self._find_paths(from_unit, to_unit)
        if len(paths) == 1:
            return True
        return len(paths) > 1 and _select_equivalent_factor(paths) is not None

    def _resolve_unit(self, unit: str) -> str:
        try:
            return self._unit_lookup[unit]
        except KeyError as error:
            raise UnitNotFoundError(f"Unknown unit: {unit!r}.") from error

    def _resolve_units(self, from_unit: str, to_unit: str) -> tuple[str, str]:
        missing = list(
            dict.fromkeys(
                unit
                for unit in (from_unit, to_unit)
                if unit not in self._unit_lookup
            )
        )
        if missing:
            formatted = ", ".join(repr(unit) for unit in missing)
            raise UnitNotFoundError(f"Unknown unit(s): {formatted}.")
        return self._unit_lookup[from_unit], self._unit_lookup[to_unit]

    def _display_unit(self, unit: str) -> str:
        return self._display_names[unit]

    def _find_paths(
        self,
        from_unit: str,
        to_unit: str,
    ) -> list[Path]:
        queue: deque[tuple[str, Path, frozenset[str]]] = deque(
            [(from_unit, (), frozenset({from_unit}))]
        )
        found_depth: int | None = None
        results: list[Path] = []

        while queue:
            current_unit, path, seen_units = queue.popleft()
            if found_depth is not None and len(path) >= found_depth:
                continue

            for edge in self._adjacency.get(current_unit, []):
                if edge.to_unit in seen_units:
                    continue

                next_path = (*path, edge)
                if edge.to_unit == to_unit:
                    found_depth = len(next_path)
                    results.append(next_path)
                    continue

                if found_depth is None:
                    queue.append(
                        (
                            edge.to_unit,
                            next_path,
                            seen_units | {edge.to_unit},
                        )
                    )

        return results

    def _raise_ambiguous_path(
        self,
        from_unit: str,
        to_unit: str,
        paths: list[Path],
    ) -> NoReturn:
        raise AmbiguousConversionError(
            f"Multiple conversion paths found from {from_unit!r} to {to_unit!r}. "
            f"{len(paths)} shortest paths contain conflicting rules."
        )

    def _raise_no_path(
        self,
        from_unit: str,
        to_unit: str,
    ) -> NoReturn:
        raise IncompatibleUnitError(
            f"No conversion path found from {from_unit!r} to {to_unit!r}"
            ". Units may belong to different physical quantities."
        )


def convert(
    value: Number,
    from_unit: str,
    to_unit: str,
) -> Decimal:
    """Convert a value using the package's bundled conversion table."""

    return _package_converter().convert(value, from_unit, to_unit)


def can_convert(from_unit: str, to_unit: str) -> bool:
    """Return whether bundled data supports conversion between two unit keys."""

    return _package_converter().can_convert(from_unit, to_unit)


def compatible_units(unit: str) -> tuple[str, ...]:
    """Return bundled display names reachable from ``unit``."""

    return _package_converter().compatible_units(unit)


@cache
def _package_converter() -> UnitConverter:
    return UnitConverter.from_package_data()


def _to_decimal(value: object, *, role: str = "value") -> Decimal:
    if isinstance(value, bool) or not isinstance(
        value,
        int | float | str | Decimal,
    ):
        raise ConversionError(
            f"Conversion {role} must be an int, float, str, or Decimal; "
            f"received {type(value).__name__}."
        )
    try:
        decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
    except (DecimalException, ValueError, TypeError) as error:
        raise ConversionError(
            f"Invalid numeric conversion {role}: {value!r}."
        ) from error
    return _require_finite(decimal_value, f"Conversion {role}")


def _require_data_version(
    name: str,
    data: dict[str, Any],
    expected_version: int,
) -> None:
    actual_version = data.get("version")
    if actual_version != expected_version:
        raise ConversionError(
            f"Unsupported {name} version {actual_version!r}; "
            f"expected {expected_version}."
        )


def _require_finite(value: Decimal, operation: str) -> Decimal:
    if not value.is_finite():
        raise ConversionError(f"{operation} must produce a finite Decimal.")
    return value


def _apply_path(value: Number, path: Path) -> Decimal:
    result = _to_decimal(value)
    for edge in path:
        result = edge.apply(result)
    return result


def _apply_factor(value: Number, factor: Fraction) -> Decimal:
    numerator = Decimal(factor.numerator)
    denominator = Decimal(factor.denominator)
    try:
        result = _to_decimal(value) * numerator / denominator
    except DecimalException as error:
        raise ConversionError(
            f"Equivalent factor conversion failed for value {value!r}."
        ) from error
    return _require_finite(result, "Equivalent factor conversion")


def _select_equivalent_factor(paths: list[Path]) -> Fraction | None:
    candidates: list[tuple[Path, Fraction]] = []
    for path in paths:
        factor = _path_factor(path)
        if factor is None:
            return None
        candidates.append((path, factor))

    if not _factors_are_equivalent([factor for _, factor in candidates]):
        return None

    _, selected_factor = min(candidates, key=_factor_preference_key)
    return selected_factor


def _path_factor(path: Path) -> Fraction | None:
    result = Fraction(1)
    for edge in path:
        if edge.conversion.factor is None:
            return None
        factor = Fraction(str(edge.conversion.factor))
        if edge.reverse:
            result /= factor
        else:
            result *= factor
    return result


def _factors_are_equivalent(factors: list[Fraction]) -> bool:
    for index, left in enumerate(factors):
        for right in factors[index + 1 :]:
            scale = max(abs(left), abs(right))
            if abs(left - right) > scale * _FACTOR_EQUIVALENCE_RELATIVE_TOLERANCE:
                return False
    return True


def _factor_preference_key(
    candidate: tuple[Path, Fraction],
) -> tuple[bool, int, int, tuple[tuple[str, str, bool], ...]]:
    path, factor = candidate
    decimal_places = _terminating_decimal_places(factor.denominator)
    return (
        decimal_places is None,
        decimal_places or 0,
        len(str(abs(factor.numerator))) + len(str(factor.denominator)),
        tuple(
            (
                edge.conversion.from_unit,
                edge.conversion.to_unit,
                edge.reverse,
            )
            for edge in path
        ),
    )


def _terminating_decimal_places(denominator: int) -> int | None:
    powers_of_two = 0
    powers_of_five = 0
    while denominator % 2 == 0:
        denominator //= 2
        powers_of_two += 1
    while denominator % 5 == 0:
        denominator //= 5
        powers_of_five += 1
    if denominator != 1:
        return None
    return max(powers_of_two, powers_of_five)


def _evaluate_formula(formula: str, x: Decimal) -> Decimal:
    expression = _parse_formula(formula)
    try:
        result = _eval_node(expression.body, x)
    except DecimalException as error:
        raise ConversionError(
            f"Conversion formula {formula!r} failed for value {x!r}."
        ) from error
    return _require_finite(result, f"Conversion formula {formula!r}")


def _evaluate_inverse_formula(formula: str, y: Decimal) -> Decimal:
    try:
        affine = _formula_to_affine(formula)
        if affine is not None:
            slope, intercept = affine
            if slope == 0:
                raise ConversionNotFoundError(
                    f"Cannot invert constant formula: {formula!r}."
                )
            result = (y - intercept) / slope
            return _require_finite(result, f"Conversion inverse formula {formula!r}")

        reciprocal_constant = _formula_to_reciprocal_constant(formula)
        if reciprocal_constant is not None and reciprocal_constant != 0:
            result = reciprocal_constant / y
            return _require_finite(result, f"Conversion inverse formula {formula!r}")
    except DecimalException as error:
        raise ConversionError(
            f"Conversion inverse formula {formula!r} failed for value {y!r}."
        ) from error

    raise ConversionNotFoundError(f"Cannot invert formula: {formula!r}.")


def _can_invert_formula(formula: str) -> bool:
    affine = _formula_to_affine(formula)
    if affine is not None:
        slope, _ = affine
        return slope != 0
    reciprocal_constant = _formula_to_reciprocal_constant(formula)
    return reciprocal_constant is not None and reciprocal_constant != 0


@cache
def _parse_formula(formula: str) -> ast.Expression:
    if not formula.strip():
        raise ConversionError("Conversion formula must not be empty.")
    try:
        expression = ast.parse(formula, mode="eval")
    except SyntaxError as error:
        raise ConversionError(f"Invalid conversion formula: {formula!r}.") from error
    _validate_formula_node(expression.body, formula)
    return expression


def _validate_formula_node(node: ast.AST, formula: str) -> None:
    if isinstance(node, ast.Constant):
        constant = _constant_decimal(node)
        if constant is not None and constant.is_finite():
            return
    elif isinstance(node, ast.Name) and node.id == "x":
        return
    elif isinstance(node, ast.BinOp) and isinstance(
        node.op,
        ast.Add | ast.Div | ast.Mult | ast.Pow | ast.Sub,
    ):
        _validate_formula_node(node.left, formula)
        _validate_formula_node(node.right, formula)
        return
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd | ast.USub):
        _validate_formula_node(node.operand, formula)
        return
    raise ConversionError(
        f"Unsupported conversion formula syntax in {formula!r}: {ast.dump(node)}."
    )


def _eval_node(node: ast.AST, x: Decimal) -> Decimal:
    if isinstance(node, ast.Constant):
        constant_value = node.value
        if isinstance(constant_value, int | float) and not isinstance(
            constant_value, bool
        ):
            return Decimal(str(constant_value))

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
        operand_value = _eval_node(node.operand, x)
        if isinstance(node.op, ast.UAdd):
            return operand_value
        if isinstance(node.op, ast.USub):
            return -operand_value
        raise ConversionError(f"Unsupported formula operator: {type(node.op)}.")

    raise ConversionError(f"Unsupported formula syntax: {ast.dump(node)}.")


def _formula_to_affine(formula: str) -> tuple[Decimal, Decimal] | None:
    try:
        expression = _parse_formula(formula)
    except ConversionError:
        return None
    try:
        return _linearize_node(expression.body)
    except DecimalException as error:
        raise ConversionError(
            f"Could not analyze conversion formula {formula!r}."
        ) from error


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
        expression = _parse_formula(formula)
    except ConversionError:
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
        constant_value = node.value
        if isinstance(constant_value, int | float) and not isinstance(
            constant_value, bool
        ):
            return Decimal(str(constant_value))
    if isinstance(node, ast.UnaryOp):
        operand_value = _constant_decimal(node.operand)
        if operand_value is None:
            return None
        if isinstance(node.op, ast.UAdd):
            return operand_value
        if isinstance(node.op, ast.USub):
            return -operand_value
    return None
