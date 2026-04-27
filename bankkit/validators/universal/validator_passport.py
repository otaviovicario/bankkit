# validators/universal/validator_passport.py
# International passport number validator
# Standard: ICAO Doc 9303 — Machine Readable Travel Documents

import re


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _response(valid: bool, error: str = None, **extra) -> dict:
    """Standard response format."""
    result = {"valid": valid, "error": error if not valid else None}
    if valid and extra:
        result.update(extra)
    return result


# ---------------------------------------------------------------------------
# PASSPORT FORMAT REGISTRY
# ---------------------------------------------------------------------------

# Passport number formats by country (ISO 3166-1 alpha-2)
# Format: regex pattern for the passport number
# Source: ICAO Doc 9303 + individual country specifications
# NOTE: Passport formats are format-based only — no check digit exists.

_PASSPORT_FORMATS = {
    # Latin America
    "BR": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "AR": (r"^[A-Z]{2,3}\d{6}$",        "2-3 letters + 6 digits"),
    "MX": (r"^[A-Z]{1,2}\d{8}$",        "1-2 letters + 8 digits"),
    "CL": (r"^[A-Z]{1,2}\d{7}$",        "1-2 letters + 7 digits"),
    "CO": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "PE": (r"^[A-Z]{2}\d{7}$",          "2 letters + 7 digits"),
    "UY": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "PY": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "BO": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "VE": (r"^[A-Z]{2}\d{7}$",          "2 letters + 7 digits"),
    "EC": (r"^[A-Z]{2}\d{7}$",          "2 letters + 7 digits"),

    # North America
    "US": (r"^[A-Z]\d{8}$",             "1 letter + 8 digits"),
    "CA": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),

    # Europe
    "GB": (r"^\d{9}$",                  "9 digits"),
    "DE": (r"^[A-Z0-9]{9}$",            "9 alphanumeric"),
    "FR": (r"^\d{2}[A-Z]{2}\d{5}$",     "2 digits + 2 letters + 5 digits"),
    "ES": (r"^[A-Z]{3}\d{6}$",          "3 letters + 6 digits"),
    "IT": (r"^[A-Z]{2}\d{7}$",          "2 letters + 7 digits"),
    "PT": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "NL": (r"^[A-Z]{2}[A-Z0-9]\d{6}$",  "2 letters + 1 alphanumeric + 6 digits"),
    "CH": (r"^[A-Z]\d{7}$",             "1 letter + 7 digits"),
    "AT": (r"^[A-Z]\d{7}$",             "1 letter + 7 digits"),
    "BE": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "PL": (r"^[A-Z]{2}\d{7}$",          "2 letters + 7 digits"),

    # Asia / Oceania
    "AU": (r"^[A-Z]\d{7}$",             "1 letter + 7 digits"),
    "NZ": (r"^[A-Z]{2}\d{6}$",          "2 letters + 6 digits"),
    "JP": (r"^[A-Z]{2}\d{7}$",          "2 letters + 7 digits"),
    "CN": (r"^[A-Z]\d{8}$",             "1 letter + 8 digits"),
    "IN": (r"^[A-Z]\d{7}$",             "1 letter + 7 digits"),
}


# ---------------------------------------------------------------------------
# PASSPORT VALIDATOR
# ---------------------------------------------------------------------------

def validate_passport(number: str, country: str) -> dict:
    """
    Validates a passport number by country format.

    Validation is format-based only — no check digit algorithm exists
    for passport numbers. Validates structure and length per country spec.

    Standard: ICAO Doc 9303 (Machine Readable Travel Documents)

    Args:
        number:  Passport number string — spaces and dashes are stripped
        country: ISO 3166-1 alpha-2 country code (e.g. "BR", "US", "DE")

    Returns:
        dict: {
            "valid":   bool,
            "country": str,         # country code
            "format":  str | None,  # expected format description
            "error":   str | None
        }

    Example:
        >>> validate_passport("AB123456", "BR")
        {"valid": True, "country": "BR", "format": "2 letters + 6 digits", "error": None}

        >>> validate_passport("A12345678", "US")
        {"valid": True, "country": "US", "format": "1 letter + 8 digits", "error": None}
    """
    number  = re.sub(r"[\s\-]", "", number).upper()
    country = country.strip().upper()

    # Country must be in registry
    format_data = _PASSPORT_FORMATS.get(country)
    if not format_data:
        return _response(False, f"Passport format for country '{country}' is not supported yet")

    pattern, format_desc = format_data

    # Validate format
    if not re.match(pattern, number):
        return _response(
            False,
            f"Invalid passport format for {country}: expected {format_desc}"
        )

    return _response(True, country=country, format=format_desc)