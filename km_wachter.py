# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernized 2024.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how worn a car is as a percentage of one service interval.

    Uses floating-point division so values between 0 and 100 are preserved
    (e.g. 14 900 km of 15 000 gives 99.3 %, not 0 %).
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True if the car has reached or exceeded the service-warning threshold.

    A missing ``last_service_km`` reading is treated as if the car was just
    serviced at its current odometer, i.e. 0 km since service, so it is NOT
    falsely flagged.
    """
    odometer: float = car["odometer"]
    last: float = car.get("last_service_km", odometer)  # missing → 0 km since service
    km_since = odometer - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car that is due for service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
