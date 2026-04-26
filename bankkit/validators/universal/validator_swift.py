# validators/universal/validator_swift.py
# SWIFT/BIC validator
# Standard: ISO 9362

import re
from typing import Optional


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
# COUNTRY CODES (ISO 3166-1 alpha-2)
# ---------------------------------------------------------------------------

# Valid ISO 3166-1 alpha-2 country codes
# Source: https://www.iso.org/iso-3166-country-codes.html
_VALID_COUNTRY_CODES = {
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT",
    "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI",
    "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY",
    "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN",
    "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM",
    "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK",
    "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL",
    "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM",
    "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR",
    "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN",
    "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS",
    "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
    "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW",
    "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP",
    "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM",
    "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW",
    "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM",
    "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF",
    "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW",
    "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI",
    "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW",
}


# ---------------------------------------------------------------------------
# SWIFT/BIC VALIDATOR
# ---------------------------------------------------------------------------

def validate_swift(swift: str) -> dict:
    """
    Validates a SWIFT/BIC code (Bank Identifier Code).

    Structure (ISO 9362):
        AAAA BB CC DDD
        ^^^^ ^^ ^^ ^^^
        |||| || || branch code (optional, 3 chars)
        |||| || location code (2 alphanumeric)
        |||| country code (2 letters, ISO 3166-1)
        bank code (4 letters)

    Valid lengths:
        - 8 characters  (without branch code)
        - 11 characters (with branch code)

    Args:
        swift: SWIFT/BIC string — case insensitive, spaces are stripped
               e.g. "BRASBRRJ" or "BRASBRRJXXX"

    Returns:
        dict: {
            "valid":       bool,
            "bank_code":   str,   # first 4 letters
            "country":     str,   # ISO country code
            "location":    str,   # location code
            "branch":      str,   # branch code ("XXX" if primary office)
            "error":       str | None
        }

    Example:
        >>> validate_swift("BRASBRRJXXX")
        {"valid": True, "bank_code": "BRAS", "country": "BR", "location": "RJ", "branch": "XXX", "error": None}

        >>> validate_swift("ITAUBRSP")
        {"valid": True, "bank_code": "ITAU", "country": "BR", "location": "SP", "branch": "XXX", "error": None}
    """
    swift = swift.strip().upper()

    # Must be 8 or 11 characters
    if len(swift) not in (8, 11):
        return _response(False, "SWIFT/BIC must be 8 or 11 characters")

    # Must match pattern: 4 letters + 2 letters + 2 alphanumeric + optional 3 alphanumeric
    if not re.match(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$", swift):
        return _response(False, "Invalid SWIFT/BIC format")

    # Extract components
    bank_code    = swift[0:4]   # institution code
    country_code = swift[4:6]   # ISO 3166-1 alpha-2
    location     = swift[6:8]   # location code
    branch       = swift[8:11] if len(swift) == 11 else "XXX"  # XXX = primary office

    # Validate country code
    if country_code not in _VALID_COUNTRY_CODES:
        return _response(False, f"Invalid country code '{country_code}' in SWIFT/BIC")

    return _response(
        True,
        bank_code=bank_code,
        country=country_code,
        location=location,
        branch=branch,
    )