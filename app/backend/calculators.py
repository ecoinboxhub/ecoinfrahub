from __future__ import annotations
import math
from typing import Dict, Any


def _err(message: str) -> Dict[str, Any]:
    return {"error": message}


def _meta(formula: str, variables: dict, given: list, substitution: str, working: list, explanation: str) -> Dict[str, Any]:
    """Structured calculation workings returned alongside the numeric result.

    Never used for validation or arithmetic; it only documents the calculation
    that was actually performed by the function.
    """
    return {
        "formula": formula,
        "variables": variables,
        "given": given,
        "substitution": substitution,
        "working": working,
        "explanation": explanation,
    }


def _positive(values: Dict[str, float], names: list[str], zero_ok: bool = False) -> Dict[str, Any] | None:
    for name in names:
        v = values.get(name)
        if v is None or not isinstance(v, (int, float)):
            return _err(f"{name.replace('_', ' ').title()} must be a number")
        if zero_ok and v == 0:
            continue
        if v <= 0:
            return _err(f"{name.replace('_', ' ').title()} must be positive")
    return None


def concrete_mix_ratio(cement: float, sand: float, aggregate: float, water: float, units: str = "kg") -> Dict[str, Any]:
    total = cement + sand + aggregate + water
    if total == 0:
        return _err("Total cannot be zero")
    invalid = _positive({"cement": cement, "sand": sand, "aggregate": aggregate, "water": water}, ["cement", "sand", "aggregate"])
    if invalid:
        return invalid
    ratio = f"1:{sand/cement:.1f}:{aggregate/cement:.1f}"
    wc_ratio = water / cement if cement > 0 else 0
    result = {
        "ratio": ratio,
        "water_cement_ratio": round(wc_ratio, 2),
        "cement": cement,
        "sand": sand,
        "aggregate": aggregate,
        "water": water,
        "total": round(total, 2),
        "units": units,
    }
    result.update(_meta(
        formula="Water/cement ratio = water / cement; mix = 1 : (sand/cement) : (aggregate/cement)",
        variables={
            "cement": {"label": "Cement", "value": cement, "unit": units},
            "sand": {"label": "Sand", "value": sand, "unit": units},
            "aggregate": {"label": "Aggregate", "value": aggregate, "unit": units},
            "water": {"label": "Water", "value": water, "unit": units},
        },
        given=[f"cement = {cement} {units}", f"sand = {sand} {units}", f"aggregate = {aggregate} {units}", f"water = {water} {units}"],
        substitution=f"w/c = {water} / {cement} = {wc_ratio:.2f}  |  mix = 1 : {sand/cement:.1f} : {aggregate/cement:.1f}",
        working=[
            f"By weight, in {units}: cement = {cement}, sand = {sand}, aggregate = {aggregate}, water = {water}",
            f"Mix ratio (cement:sand:aggregate) = 1 : {sand/cement:.1f} : {aggregate/cement:.1f}",
            f"Water-cement ratio = water / cement = {water} / {cement} = {wc_ratio:.2f}",
            f"Total material = {cement} + {sand} + {aggregate} + {water} = {total:.2f} {units}",
        ],
        explanation=f"Concrete mix of 1:{sand/cement:.1f}:{aggregate/cement:.1f} (cement:sand:aggregate) with a water-cement ratio of {wc_ratio:.2f}.",
    ))
    return result


def traffic_volume(vehicle_count: int, observation_time_minutes: int) -> Dict[str, Any]:
    invalid = _positive({"min": observation_time_minutes}, ["min"]) or _positive({"count": vehicle_count}, ["count"], zero_ok=True)
    if invalid:
        return invalid
    hourly_volume = (vehicle_count / observation_time_minutes) * 60
    result = {
        "vehicle_count": vehicle_count,
        "observation_time_minutes": observation_time_minutes,
        "hourly_volume": round(hourly_volume, 0),
        "daily_estimate": round(hourly_volume * 12, 0),
    }
    result.update(_meta(
        formula="Hourly volume = (N / t) × 60   |   Daily estimate = Hourly volume × 12",
        variables={
            "N": {"label": "Vehicles counted", "value": vehicle_count, "unit": "veh"},
            "t": {"label": "Observation time", "value": observation_time_minutes, "unit": "min"},
        },
        given=[f"N = {vehicle_count} veh", f"t = {observation_time_minutes} min"],
        substitution=f"Hourly = ({vehicle_count} / {observation_time_minutes}) × 60 = {hourly_volume:.0f} veh/hr",
        working=[
            f"Hourly volume = (vehicles counted / observation time) × 60 = ({vehicle_count} / {observation_time_minutes}) × 60 = {hourly_volume:.0f} veh/hr",
            f"Daily estimate (12-hour factor) = {hourly_volume:.0f} × 12 = {hourly_volume * 12:.0f} veh/day",
        ],
        explanation=f"An hourly volume of about {hourly_volume:.0f} vehicles is estimated, implying roughly {hourly_volume * 12:.0f} vehicles per 12-hour day.",
    ))
    return result


def aadt_calculation(daily_counts: list[float], adjustment_factor: float = 1.0) -> Dict[str, Any]:
    if not daily_counts:
        return _err("No daily counts provided")
    if any(c < 0 for c in daily_counts):
        return _err("Daily counts cannot be negative")
    if adjustment_factor <= 0:
        return _err("Adjustment factor must be positive")
    total = sum(daily_counts)
    avg = total / len(daily_counts)
    aadt_val = avg * adjustment_factor
    result = {
        "days_sampled": len(daily_counts),
        "average_daily_traffic": round(avg, 0),
        "adjustment_factor": adjustment_factor,
        "aadt": round(aadt_val, 0),
        "total_vehicles": round(total, 0),
    }
    counts_str = ", ".join(str(c) for c in daily_counts)
    result.update(_meta(
        formula="AADT = (Σ daily counts / N) × Adjustment factor",
        variables={
            "Σ counts": {"label": "Sum of sampled daily counts", "value": round(total, 0), "unit": "veh"},
            "N": {"label": "Days sampled", "value": len(daily_counts), "unit": "days"},
            "AF": {"label": "Adjustment factor", "value": adjustment_factor, "unit": ""},
        },
        given=[f"daily counts = [{counts_str}]", f"N = {len(daily_counts)} days", f"adjustment factor = {adjustment_factor}"],
        substitution=f"AVG = ({total:.0f}) / {len(daily_counts)} = {avg:.2f};  AADT = {avg:.2f} × {adjustment_factor} = {aadt_val:.0f}",
        working=[
            f"Average daily traffic = ({total:.0f}) / {len(daily_counts)} = {avg:.2f} veh/day",
            f"Apply adjustment factor: AADT = {avg:.2f} × {adjustment_factor} = {aadt_val:.0f} veh/day",
        ],
        explanation=f"Average daily traffic of about {avg:.0f} veh/day adjusted by a factor of {adjustment_factor} gives an annual average daily traffic (AADT) close to {aadt_val:.0f} veh/day.",
    ))
    return result


_RELIABILITY_FACTORS = {
    80.0: 0.87, 85.0: 0.91, 90.0: 0.94, 95.0: 0.97, 99.0: 1.00,
}
_NEAREST_RELIABILITY_DESC = {
    80.0: "80%", 85.0: "85%", 90.0: "90%", 95.0: "95%", 99.0: "99%",
}


def pavement_thickness(cbr: float, traffic_esa: float, reliability: float = 90.0) -> Dict[str, Any]:
    invalid = _positive({"cbr": cbr, "esa": traffic_esa}, ["cbr", "esa"]) or _positive({"reliability": reliability}, ["reliability"])
    if invalid:
        return invalid
    if not (50 <= reliability <= 99.9):
        return _err("Reliability must be between 50 and 99.9 percent")
    nearest = min(_RELIABILITY_FACTORS, key=lambda r: abs(r - reliability))
    rf = _RELIABILITY_FACTORS[nearest]
    sn = rf * 0.5 * (traffic_esa ** 0.25)
    a1 = 0.44
    d1 = sn / a1
    thickness_mm = d1 * 25.4
    result = {
        "cbr": cbr,
        "traffic_esa": traffic_esa,
        "reliability_percent": reliability,
        "structural_number": round(sn, 3),
        "surface_thickness_mm": round(thickness_mm, 1),
        "base_thickness_mm": round(thickness_mm * 1.5, 1),
        "subbase_thickness_mm": round(thickness_mm * 2.0, 1),
    }
    result.update(_meta(
        formula="SN = Z_r × 0.5 × (ESA)^0.25  ;  D1 = SN / a1  ;  thickness_mm = D1 × 25.4",
        variables={
            "Z_r": {"label": "Reliability factor", "value": rf, "unit": f"(nearest {_NEAREST_RELIABILITY_DESC.get(nearest)})"},
            "ESA": {"label": "Traffic (equivalent single-axle loads)", "value": traffic_esa, "unit": "—"},
            "a1": {"label": "Surface layer coefficient", "value": a1, "unit": ""},
        },
        given=[f"cbr = {cbr}%", f"traffic ESA = {traffic_esa}", f"reliability = {reliability}% (→ factor {rf})"],
        substitution=f"SN = {rf} × 0.5 × ({traffic_esa}^0.25) = {sn:.3f};  D1 = {sn:.3f} / 0.44 = {d1:.3f} in",
        working=[
            f"Structural Number: SN = {rf} × 0.5 × ({traffic_esa} ^ 0.25) = {sn:.3f}",
            f"Surface layer thickness (inches): D1 = SN / a1 = {sn:.3f} / 0.44 = {d1:.3f} in",
            f"Convert to mm: {d1:.3f} × 25.4 = {thickness_mm:.1f} mm",
            f"Base layer estimate = 1.5 × surface = {thickness_mm * 1.5:.1f} mm; Subbase = 2.0 × surface = {thickness_mm * 2.0:.1f} mm",
        ],
        explanation="This is an estimation using a simplified AASHTO-style structural-number approach; it is not a full pavement design and should be treated as a preliminary estimate.",
    ))
    return result


def earthwork_volume(length: float, width: float, depth: float, swell_factor: float = 1.25) -> Dict[str, Any]:
    invalid = _positive({"length": length, "width": width, "depth": depth}, ["length", "width", "depth"]) or _positive(
        {"swell_factor": swell_factor}, ["swell_factor"], zero_ok=True
    )
    if invalid:
        return invalid
    bank_volume = length * width * depth
    loose_volume = bank_volume * swell_factor
    compacted_volume = bank_volume * 0.9
    result = {
        "length_m": length,
        "width_m": width,
        "depth_m": depth,
        "bank_volume_m3": round(bank_volume, 2),
        "loose_volume_m3": round(loose_volume, 2),
        "compacted_volume_m3": round(compacted_volume, 2),
        "swell_factor": swell_factor,
    }
    result.update(_meta(
        formula="V = L × W × D",
        variables={
            "L": {"label": "Length", "value": length, "unit": "m"},
            "W": {"label": "Width", "value": width, "unit": "m"},
            "D": {"label": "Depth", "value": depth, "unit": "m"},
            "SF": {"label": "Swell factor", "value": swell_factor, "unit": ""},
        },
        given=[f"L = {length} m", f"W = {width} m", f"D = {depth} m", f"swell factor = {swell_factor}"],
        substitution=f"V = {length} × {width} × {depth} = {bank_volume:.2f} m³",
        working=[
            f"Bank volume = {length} × {width} × {depth} = {bank_volume:.2f} m³",
            f"Loose volume = {bank_volume:.2f} × {swell_factor} = {loose_volume:.2f} m³",
            f"Compacted volume = {bank_volume:.2f} × 0.9 = {compacted_volume:.2f} m³",
        ],
        explanation=f"A bank (in-situ) volume of {bank_volume:.2f} m³ expands to about {loose_volume:.2f} m³ loose and compacts to about {compacted_volume:.2f} m³.",
    ))
    return result


def drainage_flow(area_ha: float, runoff_coefficient: float, rainfall_intensity_mm_hr: float) -> Dict[str, Any]:
    invalid = _positive({"area_ha": area_ha}, ["area_ha"]) or _positive({"rainfall": rainfall_intensity_mm_hr}, ["rainfall"], zero_ok=True)
    if invalid:
        return invalid
    if not (0 < runoff_coefficient <= 1):
        return _err("Runoff coefficient must be between 0 and 1")
    q = (runoff_coefficient * rainfall_intensity_mm_hr * area_ha) / 360
    result = {
        "area_ha": area_ha,
        "runoff_coefficient": runoff_coefficient,
        "rainfall_intensity_mm_hr": rainfall_intensity_mm_hr,
        "peak_flow_m3_s": round(q, 3),
        "peak_flow_l_s": round(q * 1000, 1),
    }
    result.update(_meta(
        formula="Q = (C × i × A) / 360",
        variables={
            "C": {"label": "Runoff coefficient", "value": runoff_coefficient, "unit": ""},
            "i": {"label": "Rainfall intensity", "value": rainfall_intensity_mm_hr, "unit": "mm/hr"},
            "A": {"label": "Catchment area", "value": area_ha, "unit": "ha"},
        },
        given=[f"C = {runoff_coefficient}", f"i = {rainfall_intensity_mm_hr} mm/hr", f"A = {area_ha} ha"],
        substitution=f"Q = ({runoff_coefficient} × {rainfall_intensity_mm_hr} × {area_ha}) / 360 = {q:.3f} m³/s",
        working=[
            f"Q = ({runoff_coefficient} × {rainfall_intensity_mm_hr} × {area_ha}) / 360",
            f"Q = {runoff_coefficient * rainfall_intensity_mm_hr * area_ha:.3f} / 360 = {q:.3f} m³/s",
            f"In litres per second: {q * 1000:.1f} L/s",
        ],
        explanation=f"Using the Rational Method, the estimated peak runoff is {q:.3f} m³/s ({q * 1000:.1f} L/s) for a catchment of {area_ha} ha.",
    ))
    return result


def unit_conversion(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    if not isinstance(value, (int, float)):
        return _err("Value must be a number")
    length = {
        "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
        "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
    }
    area = {
        "mm2": 1e-6, "cm2": 1e-4, "m2": 1.0, "ha": 10000.0, "km2": 1e6,
        "in2": 0.00064516, "ft2": 0.092903, "ac": 4046.86,
    }
    volume = {
        "ml": 1e-6, "l": 0.001, "m3": 1.0, "gal": 0.00378541,
        "ft3": 0.0283168, "yd3": 0.764555,
    }
    pressure = {
        "pa": 1.0, "kpa": 1000.0, "mpa": 1e6, "bar": 1e5,
        "psi": 6894.76, "atm": 101325.0,
    }
    mass = {
        "g": 0.001, "kg": 1.0, "t": 1000.0, "lb": 0.453592,
    }
    temperature = {"c", "f", "k"}

    categories = [("Length", length), ("Area", area), ("Volume", volume), ("Pressure", pressure), ("Mass", mass)]

    for cat_name, cat_data in categories:
        if from_unit in cat_data and to_unit in cat_data:
            base = value * cat_data[from_unit]
            result_val = base / cat_data[to_unit]
            factor = cat_data[from_unit] / cat_data[to_unit]
            result = {
                "category": cat_name,
                "value": value,
                "from_unit": from_unit,
                "to_unit": to_unit,
                "result": round(result_val, 6),
            }
            result.update(_meta(
                formula=f"{cat_name}: value_to = value_from × (factor_from / factor_to)",
                variables={
                    "value": {"label": "Input value", "value": value, "unit": from_unit},
                    "factor_from": {"label": f"Factor for '{from_unit}'", "value": cat_data[from_unit], "unit": f"(base {cat_name.lower()})"},
                    "factor_to": {"label": f"Factor for '{to_unit}'", "value": cat_data[to_unit], "unit": f"(base {cat_name.lower()})"},
                },
                given=[f"value = {value} {from_unit}", f"from unit = {from_unit}", f"to unit = {to_unit}"],
                substitution=f"{value} × {cat_data[from_unit]} / {cat_data[to_unit]} = {result_val:.6f} {to_unit}",
                working=[
                    f"Convert {value} {from_unit} to base {cat_name.lower()} units: {value} × {cat_data[from_unit]} = {base:.6f}",
                    f"Convert to {to_unit}: {base:.6f} / {cat_data[to_unit]} = {result_val:.6f} {to_unit}",
                ],
                explanation=f"{value} {from_unit} equals {round(result_val, 6)} {to_unit}.",
            ))
            return result

    if from_unit in temperature and to_unit in temperature:
        if from_unit == "c":
            if to_unit == "f":
                result_val = value * 9/5 + 32
                desc = f"({value} × 9/5) + 32 = {result_val:.2f}"
            else:
                result_val = value + 273.15
                desc = f"{value} + 273.15 = {result_val:.2f}"
        elif from_unit == "f":
            if to_unit == "c":
                result_val = (value - 32) * 5/9
                desc = f"({value} - 32) × 5/9 = {result_val:.2f}"
            else:
                result_val = (value - 32) * 5/9 + 273.15
                desc = f"({value} - 32) × 5/9 + 273.15 = {result_val:.2f}"
        else:
            if to_unit == "c":
                result_val = value - 273.15
                desc = f"{value} - 273.15 = {result_val:.2f}"
            else:
                result_val = (value - 273.15) * 9/5 + 32
                desc = f"({value} - 273.15) × 9/5 + 32 = {result_val:.2f}"
        result = {
            "category": "Temperature",
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "result": round(result_val, 2),
        }
        result.update(_meta(
            formula="Temperature conversion formula (C, F, K)",
            variables={"value": {"label": "Input temperature", "value": value, "unit": from_unit}},
            given=[f"value = {value} {from_unit}", f"from = {from_unit}", f"to = {to_unit}"],
            substitution=desc,
            working=[f"Conversion: {desc}"],
            explanation=f"{value} {from_unit} converts to {round(result_val, 2)} {to_unit}.",
        ))
        return result

    return _err(f"Unsupported conversion: {from_unit} to {to_unit}")


def bearing_capacity(cohesion: float, unit_weight: float, width: float, depth: float, phi_deg: float, safety_factor: float = 3.0) -> Dict[str, Any]:
    invalid = _positive(
        {"cohesion": cohesion, "unit_weight": unit_weight, "width": width, "depth": depth}, ["cohesion", "unit_weight", "width", "depth"]
    ) or _positive({"phi": phi_deg}, ["phi"], zero_ok=True) or _positive({"safety_factor": safety_factor}, ["safety_factor"])
    if invalid:
        return invalid
    if not (0 <= phi_deg < 45):
        return _err("Friction angle must be between 0 and 45 degrees")
    phi_rad = math.radians(phi_deg)
    nc = (math.exp(math.pi * math.tan(phi_rad))) * (math.tan(phi_rad + math.pi/4) ** 2) - 1
    nc = nc / math.tan(phi_rad) if phi_rad > 0 else 5.14
    nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(phi_rad + math.pi/4) ** 2)
    ng = 2 * (nq + 1) * math.tan(phi_rad) if phi_rad > 0 else 0
    q_ult = (cohesion * nc) + (unit_weight * depth * nq) + (0.5 * unit_weight * width * ng)
    q_allowable = q_ult / safety_factor
    result = {
        "cohesion_kpa": cohesion,
        "unit_weight_knm3": unit_weight,
        "width_m": width,
        "depth_m": depth,
        "phi_deg": phi_deg,
        "nc": round(nc, 2),
        "nq": round(nq, 2),
        "ng": round(ng, 2),
        "ultimate_capacity_kpa": round(q_ult, 2),
        "allowable_capacity_kpa": round(q_allowable, 2),
        "safety_factor": safety_factor,
    }
    result.update(_meta(
        formula="q_ult = c·Nc + γ·Df·Nq + 0.5·γ·B·Nγ   ;   q_allow = q_ult / SF",
        variables={
            "c": {"label": "Cohesion", "value": cohesion, "unit": "kPa"},
            "γ": {"label": "Unit weight", "value": unit_weight, "unit": "kN/m³"},
            "B": {"label": "Footing width", "value": width, "unit": "m"},
            "Df": {"label": "Depth", "value": depth, "unit": "m"},
            "φ": {"label": "Friction angle", "value": phi_deg, "unit": "deg"},
            "SF": {"label": "Safety factor", "value": safety_factor, "unit": ""},
        },
        given=[f"c = {cohesion} kPa", f"γ = {unit_weight} kN/m³", f"B = {width} m", f"Df = {depth} m", f"φ = {phi_deg}°", f"SF = {safety_factor}"],
        substitution=f"q_ult = ({cohesion}×{nc:.2f}) + ({unit_weight}×{depth}×{nq:.2f}) + (0.5×{unit_weight}×{width}×{ng:.2f}) = {q_ult:.2f} kPa;  q_allow = {q_ult:.2f} / {safety_factor} = {q_allowable:.2f} kPa",
        working=[
            f"Bearing-capacity factors (φ = {phi_deg}°): Nc = {nc:.2f}, Nq = {nq:.2f}, Nγ = {ng:.2f}",
            f"Ultimate: q_ult = {cohesion}×{nc:.2f} + {unit_weight}×{depth}×{nq:.2f} + 0.5×{unit_weight}×{width}×{ng:.2f} = {q_ult:.2f} kPa",
            f"Allowable: q_allow = {q_ult:.2f} / {safety_factor} = {q_allowable:.2f} kPa",
        ],
        explanation=f"Terzaghi-style ultimate bearing capacity of {q_ult:.2f} kPa reduced by a safety factor of {safety_factor} gives an allowable bearing capacity of {q_allowable:.2f} kPa.",
    ))
    return result


def _area_working(shape: str, dimensions: dict) -> Dict[str, Any]:
    if shape == "rectangle":
        a = dimensions["length"] * dimensions["width"]
        return _meta(
            formula="A = L × W",
            variables={"L": {"label": "Length", "value": dimensions["length"], "unit": "m"}, "W": {"label": "Width", "value": dimensions["width"], "unit": "m"}},
            given=[f"L = {dimensions['length']} m", f"W = {dimensions['width']} m"],
            substitution=f"A = {dimensions['length']} × {dimensions['width']} = {a} m²",
            working=[f"A = L × W = {dimensions['length']} × {dimensions['width']} = {a:.4g} m²"],
            explanation=f"The area of the rectangle is {a:.4g} m².",
        )
    elif shape == "circle":
        a = math.pi * dimensions["radius"] ** 2
        return _meta(
            formula="A = π × r²",
            variables={"r": {"label": "Radius", "value": dimensions["radius"], "unit": "m"}},
            given=[f"r = {dimensions['radius']} m"],
            substitution=f"A = π × {dimensions['radius']}² = {a} m²",
            working=[f"A = π × r² = π × {dimensions['radius']}² = {a:.4g} m²"],
            explanation=f"The area of the circle is {a:.4g} m².",
        )
    elif shape == "triangle":
        a = 0.5 * dimensions["base"] * dimensions["height"]
        return _meta(
            formula="A = ½ × b × h",
            variables={"b": {"label": "Base", "value": dimensions["base"], "unit": "m"}, "h": {"label": "Height", "value": dimensions["height"], "unit": "m"}},
            given=[f"b = {dimensions['base']} m", f"h = {dimensions['height']} m"],
            substitution=f"A = ½ × {dimensions['base']} × {dimensions['height']} = {a} m²",
            working=[f"A = ½ × b × h = ½ × {dimensions['base']} × {dimensions['height']} = {a:.4g} m²"],
            explanation=f"The area of the triangle is {a:.4g} m².",
        )
    elif shape == "trapezoid":
        a = 0.5 * (dimensions["base1"] + dimensions["base2"]) * dimensions["height"]
        return _meta(
            formula="A = ½ × (b₁ + b₂) × h",
            variables={"b₁": {"label": "Base 1", "value": dimensions["base1"], "unit": "m"}, "b₂": {"label": "Base 2", "value": dimensions["base2"], "unit": "m"}, "h": {"label": "Height", "value": dimensions["height"], "unit": "m"}},
            given=[f"b₁ = {dimensions['base1']} m", f"b₂ = {dimensions['base2']} m", f"h = {dimensions['height']} m"],
            substitution=f"A = ½ × ({dimensions['base1']} + {dimensions['base2']}) × {dimensions['height']} = {a} m²",
            working=[f"A = ½ × (b₁ + b₂) × h = ½ × ({dimensions['base1']} + {dimensions['base2']}) × {dimensions['height']} = {a:.4g} m²"],
            explanation=f"The area of the trapezoid is {a:.4g} m².",
        )
    return {}


def area_calculation(shape: str, **dimensions: float) -> Dict[str, Any]:
    if shape == "rectangle":
        invalid = _positive(dimensions, ["length", "width"])
        if invalid:
            return invalid
        a = round(dimensions["length"] * dimensions["width"], 4)
        result = {"shape": "rectangle", "area": a, "unit": "m²"}
        result.update(_area_working("rectangle", dimensions))
        return result
    elif shape == "circle":
        invalid = _positive(dimensions, ["radius"])
        if invalid:
            return invalid
        a = round(math.pi * dimensions["radius"] ** 2, 4)
        result = {"shape": "circle", "area": a, "unit": "m²"}
        result.update(_area_working("circle", dimensions))
        return result
    elif shape == "triangle":
        invalid = _positive(dimensions, ["base", "height"])
        if invalid:
            return invalid
        a = round(0.5 * dimensions["base"] * dimensions["height"], 4)
        result = {"shape": "triangle", "area": a, "unit": "m²"}
        result.update(_area_working("triangle", dimensions))
        return result
    elif shape == "trapezoid":
        invalid = _positive(dimensions, ["base1", "base2", "height"])
        if invalid:
            return invalid
        a = round(0.5 * (dimensions["base1"] + dimensions["base2"]) * dimensions["height"], 4)
        result = {"shape": "trapezoid", "area": a, "unit": "m²"}
        result.update(_area_working("trapezoid", dimensions))
        return result
    return _err(f"Unknown shape: {shape}")


def _volume_working(shape: str, dimensions: dict) -> Dict[str, Any]:
    if shape == "cube":
        v = dimensions["side"] ** 3
        return _meta(
            formula="V = s³",
            variables={"s": {"label": "Side", "value": dimensions["side"], "unit": "m"}},
            given=[f"s = {dimensions['side']} m"],
            substitution=f"V = {dimensions['side']}³ = {v} m³",
            working=[f"V = s³ = {dimensions['side']}³ = {v:.4g} m³"],
            explanation=f"The volume of the cube is {v:.4g} m³.",
        )
    elif shape == "cylinder":
        v = math.pi * dimensions["radius"] ** 2 * dimensions["height"]
        return _meta(
            formula="V = π × r² × h",
            variables={"r": {"label": "Radius", "value": dimensions["radius"], "unit": "m"}, "h": {"label": "Height", "value": dimensions["height"], "unit": "m"}},
            given=[f"r = {dimensions['radius']} m", f"h = {dimensions['height']} m"],
            substitution=f"V = π × {dimensions['radius']}² × {dimensions['height']} = {v} m³",
            working=[f"V = π × r² × h = π × {dimensions['radius']}² × {dimensions['height']} = {v:.4g} m³"],
            explanation=f"The volume of the cylinder is {v:.4g} m³.",
        )
    elif shape == "sphere":
        v = (4/3) * math.pi * dimensions["radius"] ** 3
        return _meta(
            formula="V = 4/3 × π × r³",
            variables={"r": {"label": "Radius", "value": dimensions["radius"], "unit": "m"}},
            given=[f"r = {dimensions['radius']} m"],
            substitution=f"V = 4/3 × π × {dimensions['radius']}³ = {v} m³",
            working=[f"V = 4/3 × π × r³ = 4/3 × π × {dimensions['radius']}³ = {v:.4g} m³"],
            explanation=f"The volume of the sphere is {v:.4g} m³.",
        )
    elif shape == "cone":
        v = (1/3) * math.pi * dimensions["radius"] ** 2 * dimensions["height"]
        return _meta(
            formula="V = 1/3 × π × r² × h",
            variables={"r": {"label": "Radius", "value": dimensions["radius"], "unit": "m"}, "h": {"label": "Height", "value": dimensions["height"], "unit": "m"}},
            given=[f"r = {dimensions['radius']} m", f"h = {dimensions['height']} m"],
            substitution=f"V = 1/3 × π × {dimensions['radius']}² × {dimensions['height']} = {v} m³",
            working=[f"V = 1/3 × π × r² × h = 1/3 × π × {dimensions['radius']}² × {dimensions['height']} = {v:.4g} m³"],
            explanation=f"The volume of the cone is {v:.4g} m³.",
        )
    return {}


def volume_calculation(shape: str, **dimensions: float) -> Dict[str, Any]:
    if shape == "cube":
        invalid = _positive(dimensions, ["side"])
        if invalid:
            return invalid
        v = round(dimensions["side"] ** 3, 4)
        result = {"shape": "cube", "volume": v, "unit": "m³"}
        result.update(_volume_working("cube", dimensions))
        return result
    elif shape == "cylinder":
        invalid = _positive(dimensions, ["radius", "height"])
        if invalid:
            return invalid
        v = round(math.pi * dimensions["radius"] ** 2 * dimensions["height"], 4)
        result = {"shape": "cylinder", "volume": v, "unit": "m³"}
        result.update(_volume_working("cylinder", dimensions))
        return result
    elif shape == "sphere":
        invalid = _positive(dimensions, ["radius"])
        if invalid:
            return invalid
        v = round((4/3) * math.pi * dimensions["radius"] ** 3, 4)
        result = {"shape": "sphere", "volume": v, "unit": "m³"}
        result.update(_volume_working("sphere", dimensions))
        return result
    elif shape == "cone":
        invalid = _positive(dimensions, ["radius", "height"])
        if invalid:
            return invalid
        v = round((1/3) * math.pi * dimensions["radius"] ** 2 * dimensions["height"], 4)
        result = {"shape": "cone", "volume": v, "unit": "m³"}
        result.update(_volume_working("cone", dimensions))
        return result
    return _err(f"Unknown shape: {shape}")


def slope_calculation(rise: float, run: float) -> Dict[str, Any]:
    if not isinstance(rise, (int, float)) or not isinstance(run, (int, float)):
        return _err("Rise and run must be numbers")
    if run == 0:
        return _err("Run cannot be zero")
    slope_percent = (rise / run) * 100
    slope_deg = math.degrees(math.atan(rise / run))
    slope_ratio = f"1:{run/rise:.1f}" if rise != 0 else "0"
    result = {
        "rise_m": rise,
        "run_m": run,
        "slope_percent": round(slope_percent, 2),
        "slope_degrees": round(slope_deg, 2),
        "slope_ratio": slope_ratio,
    }
    result.update(_meta(
        formula="Slope % = (rise / run) × 100   ;   θ = arctan(rise / run)",
        variables={"rise": {"label": "Rise", "value": rise, "unit": "m"}, "run": {"label": "Run", "value": run, "unit": "m"}},
        given=[f"rise = {rise} m", f"run = {run} m"],
        substitution=f"Slope % = ({rise} / {run}) × 100 = {slope_percent:.2f}%;  θ = arctan({rise} / {run}) = {slope_deg:.2f}°",
        working=[
            f"Slope percentage = ({rise} / {run}) × 100 = {slope_percent:.2f}%",
            f"Slope angle = arctan({rise} / {run}) = {slope_deg:.2f}°",
            f"Slope ratio = 1 : {run/rise:.1f}" if rise != 0 else "Slope ratio = 0 (horizontal)",
        ],
        explanation=f"A rise of {rise} m over a run of {run} m gives a {slope_percent:.2f}% slope at an angle of {slope_deg:.2f}°.",
    ))
    return result
