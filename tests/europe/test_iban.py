# validators/europe/iban.py
# IBAN validator
# Standards: ISO 13616, SWIFT IBAN Registry
# Algorithm: MOD 97 check digit validation

import re
from bankkit.data.universal.data_iban_registry import IBAN_REGISTRY


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _digits_only(value: str) -> str:
    """Remove spaces and dashes from IBAN input."""
    return re.sub(r"[\s\-]", "", value).upper()


def _response(valid: bool, error: str = None, **extra) -> dict:
    """Standard response format."""
    result = {"valid": valid, "error": error if not valid else None}
    if valid and extra:
        result.update(extra)
    return result


# ---------------------------------------------------------------------------
# MOD 97 ALGORITHM
# ---------------------------------------------------------------------------

def _mod97(iban: str) -> int:
    """
    Computes MOD 97 check on an IBAN string.

    Algorithm (ISO 13616):
        1. Move the first 4 characters to the end
        2. Convert each letter to digits (A=10, B=11, ..., Z=35)
        3. Compute the number modulo 97
        4. Result must equal 1 for a valid IBAN

    Args:
        iban: IBAN string — uppercase, no spaces

    Returns:
        int: remainder of MOD 97 (must be 1 for valid IBAN)
    """
    # Move first 4 chars to the end
    rearranged = iban[4:] + iban[:4]

    # Convert letters to digits (A=10, B=11, ..., Z=35)
    numeric = ""
    for char in rearranged:
        if char.isalpha():
            numeric += str(ord(char) - ord("A") + 10)
        else:
            numeric += char

    return int(numeric) % 97


# ---------------------------------------------------------------------------
# IBAN VALIDATOR
# ---------------------------------------------------------------------------

def validate_iban(iban: str) -> dict:
    """
    Validates an IBAN (International Bank Account Number).

    Checks:
        1. Format  — starts with 2 uppercase letters + 2 digits
        2. Country — country code must be in the SWIFT IBAN Registry
        3. Length  — must match the expected length for the country
        4. MOD 97  — check digit algorithm (ISO 13616)

    Args:
        iban: IBAN string — accepts spaces and dashes
              e.g. "GB82 WEST 1234 5698 7654 32" or "GB82WEST12345698765432"

    Returns:
        dict: {
            "valid":   bool,
            "country": str,   # full country name
            "code":    str,   # ISO country code (e.g. "GB")
            "error":   str | None
        }

    Example:
        >>> validate_iban("GB82 WEST 1234 5698 7654 32")
        {"valid": True, "country": "United Kingdom", "code": "GB", "error": None}

        >>> validate_iban("GB82WEST12345698765432")
        {"valid": True, "country": "United Kingdom", "code": "GB", "error": None}
    """
    iban = _digits_only(iban)

    # Must start with 2 letters + 2 digits
    if not re.match(r"^[A-Z]{2}\d{2}", iban):
        return _response(False, "Invalid IBAN format: must start with 2 letters and 2 digits")

    # Extract country code
    country_code = iban[:2]

    # Country must be in the registry
    country_data = IBAN_REGISTRY.get(country_code)
    if not country_data:
        return _response(False, f"Unknown country code '{country_code}'")

    # Length must match expected length for the country
    expected_length = country_data["length"]
    if len(iban) != expected_length:
        return _response(
            False,
            f"Invalid IBAN length for {country_data['country']}: "
            f"expected {expected_length}, got {len(iban)}"
        )

    # MOD 97 check digit validation
    if _mod97(iban) != 1:
        return _response(False, "Invalid IBAN: check digit validation failed (MOD 97)")

    return _response(
        True,
        country=country_data["country"],
        code=country_code,
    )