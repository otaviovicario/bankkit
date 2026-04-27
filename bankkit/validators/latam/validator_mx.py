# validators/latam/validator_mx.py
# Mexican banking validators
# Standards: BANXICO (Banco de México) — CLABE specification

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
# CLABE VALIDATOR
# ---------------------------------------------------------------------------

def validate_clabe(clabe: str) -> dict:
    """
    Validates a Mexican CLABE (Clave Bancaria Estandarizada).

    Structure (18 digits):
        BBB CCC CCCCCCCCCCC D
        ^^^ ^^^ ^^^^^^^^^^^ ^
        |   |   |           check digit
        |   |   account number (11 digits)
        |   city code (3 digits)
        bank code (3 digits)

    Algorithm (BANXICO):
        - Weights: [3, 7, 1] repeated 6 times for first 17 digits
        - Check digit = (10 - (weighted_sum % 10)) % 10
        - Must match the 18th digit

    Args:
        clabe: CLABE string — accepts spaces and dashes
               e.g. "032180000118359719"

    Returns:
        dict: {
            "valid":     bool,
            "bank":      str | None,   # bank name if found
            "bank_code": str | None,   # 3-digit bank code
            "error":     str | None
        }

    Example:
        >>> validate_clabe("032180000118359719")
        {"valid": True, "bank": "IXE Banco", "bank_code": "032", "error": None}
    """
    clabe = _digits_only(clabe)

    # Must have exactly 18 digits
    if len(clabe) != 18:
        return _response(False, "CLABE must have exactly 18 digits")

    # BANXICO check digit algorithm
    # Weights [3, 7, 1] repeated 6 times for first 17 digits
    weights = [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]
    total = sum(int(clabe[i]) * weights[i] for i in range(17))
    check_digit = (10 - (total % 10)) % 10

    if check_digit != int(clabe[17]):
        return _response(False, "Invalid CLABE: check digit validation failed")

    # Optional bank lookup
    bank_code = clabe[:3]
    bank_name = None
    try:
        from bankkit.data.latam.data_mx import BANKS
        bank = BANKS.get(bank_code)
        if bank:
            bank_name = bank.get("name")
    except ImportError:
        pass

    return _response(True, bank=bank_name, bank_code=bank_code)