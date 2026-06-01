"""Generate the bundled full-list UI category catalog."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_OUTPUT_PATH = REPO_ROOT / "data" / "external" / "full_list_categories.json"
PACKAGE_OUTPUT_PATH = (
    REPO_ROOT / "src" / "unit_converter" / "data" / "ui_unit_catalog.json"
)

CATALOG_NAME = "Full List UI Categories"


def ui_category(name: str, subcategories: list[str]) -> dict[str, object]:
    return {"name": name, "subcategories": subcategories}


FULL_LIST_CATEGORIES: list[dict[str, object]] = [
    ui_category(
        "Dimension Converters",
        [
            "Length",
            "Area",
            "Volume",
            "Volume - Dry",
            "Angle",
            "Volume - Lumber",
        ],
    ),
    ui_category(
        "Mechanics Converters",
        [
            "Weight and Mass",
            "Time",
            "Speed",
            "Velocity - Angular",
            "Acceleration",
            "Acceleration - Angular",
            "Force",
            "Pressure",
            "Energy",
            "Power",
            "Density",
            "Specific Volume",
            "Moment of Inertia",
            "Moment of Force",
            "Torque",
        ],
    ),
    ui_category(
        "Heat Converters",
        [
            "Temperature",
            "Fuel Consumption",
            "Fuel Efficiency - Mass",
            "Fuel Efficiency - Volume",
            "Temperature Interval",
            "Thermal Expansion",
            "Thermal Resistance",
            "Thermal Conductivity",
            "Specific Heat Capacity",
            "Heat Density",
            "Heat Flux Density",
            "Heat Transfer Coefficient",
        ],
    ),
    ui_category(
        "Fluids Converters",
        [
            "Flow",
            "Flow - Mass",
            "Flow - Molar",
            "Mass Flux Density",
            "Concentration - Molar",
            "Concentration - Solution",
            "Viscosity - Dynamic",
            "Viscosity - Kinematic",
            "Surface Tension",
            "Permeability",
        ],
    ),
    ui_category(
        "Light Converters",
        [
            "Luminance",
            "Luminous Intensity",
            "Illumination",
            "Digital Image Resolution",
            "Frequency Wavelength",
        ],
    ),
    ui_category(
        "Electricity Converters",
        [
            "Charge",
            "Linear Charge Density",
            "Surface Charge Density",
            "Volume Charge Density",
            "Current",
            "Linear Current Density",
            "Surface Current Density",
            "Electric Field Strength",
            "Electric Potential",
            "Electric Resistance",
            "Electric Resistivity",
            "Electric Conductance",
            "Electric Conductivity",
            "Electrostatic Capacitance",
            "Inductance",
        ],
    ),
    ui_category(
        "Magnetism Converters",
        [
            "Magnetomotive Force",
            "Magnetic Field Strength",
            "Magnetic Flux",
            "Magnetic Flux Density",
        ],
    ),
    ui_category(
        "Radiology Converters",
        [
            "Radiation",
            "Radiation-Activity",
            "Radiation-Exposure",
            "Radiation-Absorbed Dose",
        ],
    ),
    ui_category(
        "Miscellaneous Converters",
        [
            "Currency",
            "Case",
            "Numbers",
            "Data Storage",
            "Prefixes",
            "Data Transfer",
            "Sound",
            "Typography",
        ],
    ),
]


def build_catalog() -> dict[str, object]:
    return {
        "version": 1,
        "catalog_name": CATALOG_NAME,
        "categories": FULL_LIST_CATEGORIES,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    catalog = build_catalog()
    write_json(EXTERNAL_OUTPUT_PATH, catalog)
    write_json(PACKAGE_OUTPUT_PATH, catalog)
    print(f"Wrote {EXTERNAL_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PACKAGE_OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
