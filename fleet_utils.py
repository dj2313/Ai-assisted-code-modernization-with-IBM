# fleet_utils.py
# Shared utility helpers for the KM-Waechter fleet service.
# Modernized 2024: removed dead code (parse_service_date, chunk_list, mean, is_due),
# fixed the km-to-miles conversion constant (was 1.609 km/mi instead of 0.621371 mi/km).

KM_TO_MILES: float = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles.

    Note: used by the nightly run for the UK partner report.
    """
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a floating-point number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{int(value)}%"
