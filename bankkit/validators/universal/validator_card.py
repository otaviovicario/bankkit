# validators/universal/card.py
# Credit and debit card validators
# Standards: ISO 7812 (card numbering), Luhn Algorithm (check digit)

import re
from typing import Optional


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _digits_only(value: str) -> str:
    """Strip spaces and dashes from card number input."""
    return re.sub(r"[\s\-]", "", value)


def _response(valid: bool, error: str = None, **extra) -> dict:
    """Standard response format."""
    result = {"valid": valid, "error": error if not valid else None}
    if valid and extra:
        result.update(extra)
    return result


# ---------------------------------------------------------------------------
# LUHN ALGORITHM
# ---------------------------------------------------------------------------

def _luhn_check(number: str) -> bool:
    """
    Validates a card number using the Luhn Algorithm (ISO/IEC 7812-1).

    Algorithm:
        - Starting from the rightmost digit, double every second digit
        - If doubling results in a number > 9, subtract 9
        - Sum all digits
        - If total mod 10 == 0, the number is valid

    Args:
        number: Card number string — digits only

    Returns:
        bool: True if passes Luhn check
    """
    total = 0
    reverse = number[::-1]

    for i, digit in enumerate(reverse):
        n = int(digit)
        if i % 2 == 1:          # double every second digit from the right
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


# ---------------------------------------------------------------------------
# CARD BRAND DETECTION
# ---------------------------------------------------------------------------

# Card brand rules based on IIN/BIN ranges (ISO 7812)
# Each entry: (pattern, brand, card_lengths)
_CARD_BRANDS = [

    # Elo — Brazilian card network (BIN ranges)
    # Elo FIRST — before Visa, because some Elo BINs start with 4
    (r"^(4011|4312|4389|4514|4576|5041|5066|5090|6277|6362|6363|650[0-9]|6516|6550)", "Elo", [16]),

    # Visa — starts with 4
    (r"^4",                         "Visa",             [13, 16, 19]),

    # Mastercard — starts with 51-55 or 2221-2720
    (r"^5[1-5]",                    "Mastercard",       [16]),
    (r"^2(2[2-9][1-9]|[3-6]\d{2}|7[01]\d|720)", "Mastercard", [16]),

    # American Express — starts with 34 or 37
    (r"^3[47]",                     "Amex",             [15]),


    # Hipercard — Brazilian card network
    (r"^(606282|637095|637568|637599|637609|637612)", "Hipercard", [13, 16, 19]),

    # Discover — starts with 6011, 622126-622925, 644-649, 65
    (r"^(6011|622(1(2[6-9]|[3-9]\d)|[2-8]\d{2}|9([01]\d|2[0-5]))|64[4-9]|65)", "Discover", [16, 19]),

    # Diners Club — starts with 300-305, 36, 38
    (r"^3(0[0-5]|[68])",            "Diners Club",      [14]),

    # JCB — starts with 3528-3589
    (r"^35(2[89]|[3-8]\d)",         "JCB",              [16, 17, 18, 19]),

    # UnionPay — starts with 62 (China, but used globally)
    (r"^62",                        "UnionPay",         [16, 17, 18, 19]),
]


def _detect_brand(number: str) -> Optional[tuple]:
    """
    Detects the card brand based on IIN/BIN prefix.

    Args:
        number: Card number string — digits only

    Returns:
        tuple: (brand, valid_lengths) or None if unrecognized
    """
    for pattern, brand, lengths in _CARD_BRANDS:
        if re.match(pattern, number):
            return brand, lengths
    return None


# ---------------------------------------------------------------------------
# CARD VALIDATOR
# ---------------------------------------------------------------------------

def validate_card(number: str) -> dict:
    """
    Validates a credit or debit card number.

    Checks:
        1. Format — digits only, no letters or special characters
        2. Length — valid length for the detected brand
        3. Brand  — identified via IIN/BIN prefix (ISO 7812)
        4. Luhn   — check digit validation

    Args:
        number: Card number string — accepts spaces and dashes
                e.g. "4111 1111 1111 1111" or "4111-1111-1111-1111"

    Returns:
        dict: {
            "valid": bool,
            "brand": str,       # e.g. "Visa", "Mastercard", "Elo"
            "error": str | None
        }

    Example:
        >>> validate_card("4111 1111 1111 1111")
        {"valid": True, "brand": "Visa", "error": None}

        >>> validate_card("4111 1111 1111 1112")
        {"valid": False, "brand": None, "error": "Invalid card number: Luhn check failed"}
    """
    number = _digits_only(number)

    # Must contain only digits
    if not number.isdigit():
        return _response(False, "Card number must contain only digits")

    # Must have a reasonable length
    if len(number) < 13 or len(number) > 19:
        return _response(False, "Card number must be between 13 and 19 digits")

    # Detect brand
    brand_result = _detect_brand(number)
    brand = brand_result[0] if brand_result else "Unknown"
    valid_lengths = brand_result[1] if brand_result else list(range(13, 20))

    # Validate length for detected brand
    if brand_result and len(number) not in valid_lengths:
        return _response(False, f"Invalid length for {brand} card")

    # Luhn check
    if not _luhn_check(number):
        return _response(False, "Invalid card number: Luhn check failed")

    return _response(True, brand=brand)


# ---------------------------------------------------------------------------
# BIN VALIDATOR
# ---------------------------------------------------------------------------

def validate_bin(bin_number: str) -> dict:
    """
    Validates a BIN (Bank Identification Number) — first 6 digits of a card.

    The BIN identifies the card brand and issuing institution.
    Full issuer lookup requires a BIN database (not included).

    Args:
        bin_number: First 6 digits of a card number

    Returns:
        dict: {
            "valid": bool,
            "brand": str,       # detected card brand
            "error": str | None
        }

    Example:
        >>> validate_bin("411111")
        {"valid": True, "brand": "Visa", "error": None}
    """
    bin_number = _digits_only(bin_number)

    # BIN must be exactly 6 digits
    if not bin_number.isdigit() or len(bin_number) != 6:
        return _response(False, "BIN must be exactly 6 digits")

    # Detect brand from BIN prefix
    brand_result = _detect_brand(bin_number)

    if not brand_result:
        return _response(False, "Unrecognized BIN — card brand could not be identified")

    brand, _ = brand_result
    return _response(True, brand=brand)