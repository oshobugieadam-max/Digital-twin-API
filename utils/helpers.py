"""
utils/helpers.py

Shared utility functions used across the simulation engine.
"""


def safe_divide(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    """
    Divide numerator by denominator, returning fallback if denominator is zero.

    Parameters
    ----------
    numerator   : float
    denominator : float
    fallback    : float — value returned when denominator == 0 (default 0.0)

    Returns
    -------
    float
    """
    if denominator == 0:
        return fallback
    return numerator / denominator


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min_val and max_val (inclusive).

    Parameters
    ----------
    value   : float
    min_val : float
    max_val : float

    Returns
    -------
    float
    """
    return max(min_val, min(max_val, value))


def percent_change(original: float, new_value: float) -> float:
    """
    Calculate percentage change from original to new_value.

    Returns 0.0 if original is zero to avoid division by zero.

    Parameters
    ----------
    original  : float
    new_value : float

    Returns
    -------
    float — percentage change (positive = increase, negative = decrease)
    """
    if original == 0:
        return 0.0
    return round(((new_value - original) / abs(original)) * 100, 2)


def compliance_label(value: float, limit: float) -> str:
    """
    Return 'Compliant' or 'Non-Compliant' based on value vs limit.

    Parameters
    ----------
    value : float — measured/calculated value
    limit : float — regulatory or engineering limit

    Returns
    -------
    str
    """
    return "Compliant" if value <= limit else "Non-Compliant"


def round_dict(data: dict, decimals: int = 2) -> dict:
    """
    Return a copy of data with all float values rounded to decimals places.

    Non-float values are left untouched.

    Parameters
    ----------
    data     : dict
    decimals : int (default 2)

    Returns
    -------
    dict
    """
    return {
        k: round(v, decimals) if isinstance(v, float) else v
        for k, v in data.items()
    }
