# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_does_not_crash_on_missing_reading():
    """fleet_summary must not raise KeyError when a car has no last_service_km.

    VOS-7788 has no service history. The report should run to completion and
    treat that car as 0 % worn (freshly serviced at its current odometer).
    """
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},          # no last_service_km
    ]
    result = fleet_summary(fleet)
    assert "average_wear" in result
    assert result["count"] == 2
    # VOS-7788 contributes 0 % wear, so average is half of VOS-4471's ~99.3 %
    assert result["average_wear"] < 60
