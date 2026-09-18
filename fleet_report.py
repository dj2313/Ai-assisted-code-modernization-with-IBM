# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.
# Written in 2014. Modernized 2024.

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float:
    """Return the wear percentage for a single car.

    Falls back to the odometer value when ``last_service_km`` is absent, so a
    car with no reading contributes 0 % wear instead of crashing.
    """
    odometer: float = car["odometer"]
    last: float = car.get("last_service_km", odometer)  # missing → 0 km since service
    return wear_percent(odometer - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list[dict]) -> dict:
    """Return a summary dict with car count, service-due count, and average wear."""
    total: float = 0.0
    due: int = 0
    for car in fleet:
        total += car_wear(car)
        if needs_service(car):
            due += 1
    average: float = total / len(fleet)          # floating-point division preserves the average
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list[dict]) -> None:
    """Print the nightly health report and flush the log."""
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km: float = sum(car["odometer"] for car in fleet)
    # The partner garage in England wants the distance in miles (since 2015).
    print(f"Fleet distance: {fleet_utils.format_number(fleet_utils.km_to_miles(total_km))} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
