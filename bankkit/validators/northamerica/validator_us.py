# validators/northamerica/validator_us.py
# United States banking validators
# Standards: ABA (American Bankers Association) Routing Number

import re


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _digits_only(value: str) -> str:
    """Strip any non-digit characters from a string."""
    return re.sub(r"\D", "", value)


def _response(valid: bool, error: str = None, **extra) -> dict:
    """Standard response format."""
    result = {"valid": valid, "error": error if not valid else None}
    if valid and extra:
        result.update(extra)
    return result


# ---------------------------------------------------------------------------
# FEDERAL RESERVE DISTRICTS
# ---------------------------------------------------------------------------

# First two digits identify the Federal Reserve district
# Source: ABA routing number standards
_FED_DISTRICTS = {
    "01": "Boston",
    "02": "New York",
    "03": "Philadelphia",
    "04": "Cleveland",
    "05": "Richmond",
    "06": "Atlanta",
    "07": "Chicago",
    "08": "St. Louis",
    "09": "Minneapolis",
    "10": "Kansas City",
    "11": "Dallas",
    "12": "San Francisco",
    # Electronic / non-bank institutions
    "21": "Boston (Electronic)",
    "22": "New York (Electronic)",
    "23": "Philadelphia (Electronic)",
    "24": "Cleveland (Electronic)",
    "25": "Richmond (Electronic)",
    "26": "Atlanta (Electronic)",
    "27": "Chicago (Electronic)",
    "28": "St. Louis (Electronic)",
    "29": "Minneapolis (Electronic)",
    "30": "Kansas City (Electronic)",
    "31": "Dallas (Electronic)",
    "32": "San Francisco (Electronic)",
    # Traveler's checks and others
    "80": "Traveler's Checks",
}


# ---------------------------------------------------------------------------
# ROUTING NUMBER VALIDATOR
# ---------------------------------------------------------------------------

def validate_routing(routing: str) -> dict:
    """
    Validates a US ABA Routing Number (RTN).

    Structure (9 digits):
        FF I IIIIIII C
        ^^ ^ ^^^^^^^ ^
        || | |       check digit
        || | institution number
        || institution prefix
        Federal Reserve district (2 digits)

    Algorithm (ABA):
        Weighted sum using [3, 7, 1, 3, 7, 1, 3, 7, 1]
        Sum must be divisible by 10

    Args:
        routing: Routing number string — accepts spaces and dashes
                 e.g. "021000021" or "0210-0002-1"

    Returns:
        dict: {
            "valid":    bool,
            "district": str | None,   # Federal Reserve district name
            "error":    str | None
        }

    Example:
        >>> validate_routing("021000021")
        {"valid": True, "district": "New York", "error": None}
    """
    routing = _digits_only(routing)

    # Must have exactly 9 digits
    if len(routing) != 9:
        return _response(False, "Routing number must have exactly 9 digits")

    # Must contain only digits
    if not routing.isdigit():
        return _response(False, "Routing number must contain only digits")

    # Validate Federal Reserve district (first 2 digits)
    district_code = routing[:2]
    district = _FED_DISTRICTS.get(district_code)
    if not district:
        return _response(False, f"Invalid Federal Reserve district code '{district_code}'")

    # ABA check digit algorithm
    # Weighted sum using [3, 7, 1] repeated 3 times must be divisible by 10
    weights = [3, 7, 1, 3, 7, 1, 3, 7, 1]
    total = sum(int(routing[i]) * weights[i] for i in range(9))

    if total % 10 != 0:
        return _response(False, "Invalid routing number: check digit validation failed")

    return _response(True, district=district)