# validators/latam/validator_ar.py
# Argentine banking validators
# Standards: BCRA (Banco Central de la República Argentina)

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
# CBU ALGORITHM
# ---------------------------------------------------------------------------

def _cbu_block_check(digits: str, weights: list, check_pos: int) -> bool:
    """
    Validates a CBU block using weighted sum check digit algorithm.

    Algorithm (BCRA):
        1. Multiply each digit by its corresponding weight
        2. Sum all results
        3. Compute remainder of sum divided by 10
        4. Check digit = 10 - remainder (or 0 if remainder is 0)
        5. Must match the digit at check_pos

    Args:
        digits:    full block string
        weights:   list of weights for digits before check digit
        check_pos: index of the check digit in the block

    Returns:
        bool: True if check digit is valid
    """
    total = sum(int(digits[i]) * weights[i] for i in range(len(weights)))
    remainder = total % 10
    check_digit = 0 if remainder == 0 else 10 - remainder
    return check_digit == int(digits[check_pos])


# ---------------------------------------------------------------------------
# CBU VALIDATOR
# ---------------------------------------------------------------------------

def validate_cbu(cbu: str) -> dict:
    """
    Validates an Argentine CBU (Clave Bancaria Uniforme).

    Structure (22 digits):
        BBBAAAA D CCCCCCCCCCCCC D
        ^^^^^^^ ^ ^^^^^^^^^^^^^ ^
        ||      | |             check digit (account block)
        ||      | account number (13 digits)
        ||      check digit (bank block)
        bank + branch (7 digits)

    Algorithm (BCRA):
        - Block 1 (8 digits):  bank(3) + branch(4) + check digit
        - Block 2 (14 digits): account(13) + check digit
        - Weights: [7, 1, 3, 9, 7, 1, 3] for block 1
                   [7, 1, 3, 9, 7, 1, 3, 7, 1, 3, 9, 7, 1] for block 2

    Args:
        cbu: CBU string — accepts spaces and dashes
             e.g. "0720599600000057836902"

    Returns:
        dict: {
            "valid": bool,
            "bank":  str | None,
            "error": str | None
        }

    Example:
        >>> validate_cbu("0720599600000057836902")
        {"valid": True, "bank": None, "error": None}
    """
    cbu = _digits_only(cbu)

    # Must have exactly 22 digits
    if len(cbu) != 22:
        return _response(False, "CBU must have exactly 22 digits")

    # Split into two blocks
    block1 = cbu[:8]    # bank + branch + check digit
    block2 = cbu[8:22]  # account number + check digit

    # Weights for CBU validation (BCRA standard)
    weights1 = [7, 1, 3, 9, 7, 1, 3]
    weights2 = [7, 1, 3, 9, 7, 1, 3, 7, 1, 3, 9, 7, 1]

    # Validate block 1
    if not _cbu_block_check(block1, weights1, 7):
        return _response(False, "Invalid CBU: block 1 check digit mismatch")

    # Validate block 2
    if not _cbu_block_check(block2, weights2, 13):
        return _response(False, "Invalid CBU: block 2 check digit mismatch")

    # Optional bank lookup
    bank_code = cbu[:3]
    bank_name = None
    try:
        from bankkit.data.latam.data_ar import BANKS
        bank = BANKS.get(bank_code)
        if bank:
            bank_name = bank.get("name")
    except ImportError:
        pass

    return _response(True, bank=bank_name)