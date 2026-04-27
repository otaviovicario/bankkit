# validators/latam/validator_cl.py
# Chilean banking validators
# Standards: SII (Servicio de Impuestos Internos) — RUT specification

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
# RUT VALIDATOR
# ---------------------------------------------------------------------------

def validate_rut(rut: str) -> dict:
    """
    Validates a Chilean RUT (Rol Único Tributario).

    Used for both personal (persons) and business identification in Chile.
    Widely used in banking as the primary account identifier.

    Structure:
        12.345.678-5
        ^^^^^^^^^  ^
        |          check digit (0-9 or K)
        number (7-8 digits)

    Algorithm (SII):
        1. Reverse the RUT number digits
        2. Multiply each digit by weights [2, 3, 4, 5, 6, 7] cycling
        3. Sum all results
        4. remainder = 11 - (sum % 11)
        5. If remainder == 11 → check digit is "0"
           If remainder == 10 → check digit is "K"
           Otherwise → check digit is str(remainder)

    Args:
        rut: RUT string — accepts formats like "12.345.678-5" or "123456785"
             Check digit can be uppercase or lowercase K

    Returns:
        dict: {
            "valid": bool,
            "error": str | None
        }

    Example:
        >>> validate_rut("12.345.678-5")
        {"valid": True, "error": None}

        >>> validate_rut("76.354.771-K")
        {"valid": True, "error": None}
    """
    rut = rut.strip().upper()

    # Remove dots and dash formatting
    rut = re.sub(r"[.\-]", "", rut)

    # Must have at least 2 characters (number + check digit)
    if len(rut) < 2:
        return _response(False, "RUT is too short")

    # Split number and check digit
    rut_number = rut[:-1]
    check_digit = rut[-1]

    # Number must be digits only
    if not rut_number.isdigit():
        return _response(False, "RUT number must contain only digits")

    # Number must be between 1 and 8 digits
    if not (1 <= len(rut_number) <= 8):
        return _response(False, "RUT number must be between 1 and 8 digits")

    # Check digit must be 0-9 or K
    if check_digit not in "0123456789K":
        return _response(False, "RUT check digit must be 0-9 or K")

    # Calculate expected check digit
    digits = rut_number[::-1]
    weights = [2, 3, 4, 5, 6, 7]
    total = sum(int(digits[i]) * weights[i % 6] for i in range(len(digits)))
    remainder = 11 - (total % 11)

    if remainder == 11:
        expected = "0"
    elif remainder == 10:
        expected = "K"
    else:
        expected = str(remainder)

    if check_digit != expected:
        return _response(False, f"Invalid RUT: check digit mismatch")

    return _response(True)