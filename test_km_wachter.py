# test_km_wachter.py
from km_wachter import needs_service, wear_percent, SERVICE_INTERVAL_KM, WARN_AT_PERCENT


# ── Acceptance-checklist: exact wear-percentage outputs ───────────────────────

def test_wear_percent_is_floating_point():
    """wear_percent must use float division, not floor division."""
    pct = wear_percent(14900, SERVICE_INTERVAL_KM)
    assert 99.0 <= pct <= 100.0, f"expected ~99.3%, got {pct}"


def test_wear_percent_partial_interval():
    """A car 3 000 km into a 15 000 km window is exactly 20 % worn."""
    assert wear_percent(3000, SERVICE_INTERVAL_KM) == 20.0


def test_wear_percent_zero():
    """A freshly serviced car (0 km since service) has 0 % wear."""
    assert wear_percent(0, SERVICE_INTERVAL_KM) == 0.0


def test_wear_percent_exact_threshold():
    """A car at exactly 12 000 km (80 % of 15 000) is precisely at the threshold."""
    assert wear_percent(12000, SERVICE_INTERVAL_KM) == 80.0


# ── Acceptance-checklist: threshold remains locked at 80 % ────────────────────

def test_threshold_is_eighty_percent():
    """The warning threshold constant must remain 80 — not 79, not 81."""
    assert WARN_AT_PERCENT == 80


def test_threshold_is_not_crossed_below():
    """A car at 79.9 % wear must NOT be flagged."""
    # 11 985 km / 15 000 km = 79.9 %
    assert needs_service({"id": "VOS-BELOW", "odometer": 11985, "last_service_km": 0}) is False


def test_threshold_is_crossed_at_boundary():
    """A car at exactly 80 % (12 000 km) MUST be flagged."""
    assert needs_service({"id": "VOS-EXACT", "odometer": 12000, "last_service_km": 0}) is True


# ── Original bug-regression tests ─────────────────────────────────────────────

def test_almost_due_car_is_flagged():
    # A car at 14,900 of its 15,000 km window is about 99% worn and MUST be flagged.
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def test_missing_reading_is_not_treated_as_zero():
    # A car with NO last-service reading must not be treated as fully worn.
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False
