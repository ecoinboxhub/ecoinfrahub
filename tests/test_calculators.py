from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend import calculators


def test_concrete_mix():
    result = calculators.concrete_mix_ratio(350, 700, 1400, 175)
    assert "ratio" in result
    assert result["water_cement_ratio"] == 0.5
    assert result["total"] == 2625.0


def test_traffic_volume():
    result = calculators.traffic_volume(500, 60)
    assert result["hourly_volume"] == 500.0


def test_aadt():
    result = calculators.aadt_calculation([1200, 1300, 1100, 1400, 1250])
    assert result["aadt"] == 1250.0
    assert result["days_sampled"] == 5


def test_pavement_thickness():
    result = calculators.pavement_thickness(15, 5e6)
    assert result["cbr"] == 15
    assert result["surface_thickness_mm"] > 0


def test_earthwork():
    result = calculators.earthwork_volume(100, 20, 2)
    assert result["bank_volume_m3"] == 4000.0


def test_drainage():
    result = calculators.drainage_flow(50, 0.6, 50)
    assert result["peak_flow_m3_s"] > 0


def test_bearing_capacity():
    result = calculators.bearing_capacity(25, 18, 1.5, 1.0, 30)
    assert result["allowable_capacity_kpa"] > 0
    assert result["safety_factor"] == 3.0


def test_unit_conversion():
    result = calculators.unit_conversion(100, "m", "ft")
    assert "result" in result
    assert result["result"] > 0


def test_area():
    result = calculators.area_calculation(shape="rectangle", length=10, width=5)
    assert result["area"] == 50.0


def test_volume():
    result = calculators.volume_calculation(shape="cube", side=3)
    assert result["volume"] == 27.0


def test_slope():
    result = calculators.slope_calculation(5, 100)
    assert result["slope_percent"] == 5.0


def test_unit_conversion_temperature():
    result = calculators.unit_conversion(100, "c", "f")
    assert result["result"] == 212.0


def test_zero_division_handling():
    result = calculators.concrete_mix_ratio(0, 0, 0, 0)
    assert "error" in result


def test_negative_dimensions():
    result = calculators.earthwork_volume(-1, 20, 2)
    assert "error" in result


def assert_working(result):
    for key in ("formula", "variables", "given", "substitution", "working", "explanation"):
        assert key in result, f"missing workings field: {key}"
    assert isinstance(result["working"], list)
    assert result["working"]


def test_concrete_working():
    assert_working(calculators.concrete_mix_ratio(350, 700, 1400, 175))


def test_traffic_working():
    assert_working(calculators.traffic_volume(500, 60))


def test_aadt_working():
    assert_working(calculators.aadt_calculation([1200, 1300, 1100, 1400, 1250]))


def test_pavement_working():
    assert_working(calculators.pavement_thickness(15, 5e6))


def test_earthwork_working():
    assert_working(calculators.earthwork_volume(100, 20, 2))


def test_drainage_working():
    assert_working(calculators.drainage_flow(50, 0.6, 50))


def test_bearing_working():
    assert_working(calculators.bearing_capacity(25, 18, 1.5, 1.0, 30))


def test_unit_conversion_working():
    assert_working(calculators.unit_conversion(100, "m", "ft"))


def test_area_working():
    for shape, kw in [("rectangle", {"length": 10, "width": 5}), ("circle", {"radius": 3}), ("triangle", {"base": 10, "height": 5}), ("trapezoid", {"base1": 10, "base2": 8, "height": 5})]:
        assert_working(calculators.area_calculation(shape=shape, **kw))


def test_volume_working():
    for shape, kw in [("cube", {"side": 3}), ("cylinder", {"radius": 2, "height": 5}), ("sphere", {"radius": 2}), ("cone", {"radius": 2, "height": 5})]:
        assert_working(calculators.volume_calculation(shape=shape, **kw))


def test_slope_working():
    assert_working(calculators.slope_calculation(5, 100))


def test_drainage_runoff_out_of_range():
    assert "error" in calculators.drainage_flow(50, 1.5, 50)


def test_drainage_runoff_zero():
    assert "error" in calculators.drainage_flow(50, 0, 50)


def test_pavement_reliability_out_of_range():
    assert "error" in calculators.pavement_thickness(15, 5e6, reliability=110)


def test_slope_zero_run():
    assert "error" in calculators.slope_calculation(5, 0)


def test_slope_non_number():
    assert "error" in calculators.slope_calculation("x", 10)


def test_area_unknown_shape():
    assert "error" in calculators.area_calculation(shape="hexagon", length=1)


def test_volume_unknown_shape():
    assert "error" in calculators.volume_calculation(shape="torus", radius=1)


def test_unit_conversion_unsupported():
    assert "error" in calculators.unit_conversion(1, "m", "kg")


def test_unit_conversion_non_number():
    assert "error" in calculators.unit_conversion("x", "m", "ft")


def test_bearing_invalid_phi():
    assert "error" in calculators.bearing_capacity(25, 18, 1.5, 1.0, 60)


def test_aadt_negative_count():
    assert "error" in calculators.aadt_calculation([-5, 10])


def test_aadt_empty():
    assert "error" in calculators.aadt_calculation([])


def test_aadt_bad_factor():
    assert "error" in calculators.aadt_calculation([10, 20], adjustment_factor=0)


def test_area_working_matches_value():
    r = calculators.area_calculation(shape="rectangle", length=12, width=8)
    assert r["area"] == 96.0
    assert "12" in r["substitution"] and "8" in r["substitution"]


def test_drainage_formula_rational():
    r = calculators.drainage_flow(2.5, 0.6, 100)
    assert r["peak_flow_m3_s"] == round((0.6 * 100 * 2.5) / 360, 3)


def test_run():
    test_concrete_mix()
    test_traffic_volume()
    test_aadt()
    test_pavement_thickness()
    test_earthwork()
    test_drainage()
    test_bearing_capacity()
    test_unit_conversion()
    test_area()
    test_volume()
    test_slope()
    test_unit_conversion_temperature()
    test_zero_division_handling()
    test_negative_dimensions()
    test_concrete_working()
    test_traffic_working()
    test_aadt_working()
    test_pavement_working()
    test_earthwork_working()
    test_drainage_working()
    test_bearing_working()
    test_unit_conversion_working()
    test_area_working()
    test_volume_working()
    test_slope_working()
    test_drainage_runoff_out_of_range()
    test_drainage_runoff_zero()
    test_pavement_reliability_out_of_range()
    test_slope_zero_run()
    test_slope_non_number()
    test_area_unknown_shape()
    test_volume_unknown_shape()
    test_unit_conversion_unsupported()
    test_unit_conversion_non_number()
    test_bearing_invalid_phi()
    test_aadt_negative_count()
    test_aadt_empty()
    test_aadt_bad_factor()
    test_area_working_matches_value()
    test_drainage_formula_rational()
    print("All calculator tests passed!")


if __name__ == "__main__":
    test_run()
