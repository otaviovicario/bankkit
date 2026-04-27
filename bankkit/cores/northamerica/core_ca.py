# validators/northamerica/validator_ca.py
# Canadian banking validators
# Standards: Payments Canada — routing number specification

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
# CANADIAN INSTITUTION NUMBERS
# ---------------------------------------------------------------------------

# Major Canadian bank institution numbers
# Source: Payments Canada — https://www.payments.ca
_INSTITUTIONS = {
    "001": "Bank of Montreal (BMO)",
    "002": "Scotiabank",
    "003": "Royal Bank of Canada (RBC)",
    "004": "Toronto-Dominion Bank (TD)",
    "006": "National Bank of Canada",
    "010": "CIBC",
    "016": "HSBC Canada",
    "039": "Laurentian Bank",
    "219": "ATB Financial",
    "260": "Citibank Canada",
    "307": "Industrial Alliance",
    "326": "PC Financial",
    "338": "Canadian Tire Bank",
    "540": "Manulife Bank",
    "614": "Tangerine Bank",
    "809": "Credit Union Central of Canada",
    "815": "Desjardins",
    "828": "Central 1 Credit Union",
    "837": "Meridian Credit Union",
    "865": "Alterna Savings",
}


# ---------------------------------------------------------------------------
# CANADIAN ROUTING NUMBER VALIDATOR
# ---------------------------------------------------------------------------

def validate_ca_routing(routing: str) -> dict:
    """
    Validates a Canadian routing number (transit + institution).

    Structure (8 digits):
        TTTTT III
        ^^^^^ ^^^
        |     institution number (3 digits) — identifies the bank
        transit number (5 digits) — identifies the branch

    Note:
        Canadian routing numbers have no check digit algorithm.
        Validation is based on format and institution number recognition.

    Args:
        routing: Routing string — accepts formats like "000110011" or "00011-001"
                 Can be 8 digits (TTTTTIII) or 9 digits with leading zero

    Returns:
        dict: {
            "valid":       bool,
            "bank":        str | None,   # bank name if institution recognized
            "institution": str,          # 3-digit institution code
            "transit":     str,          # 5-digit transit number
            "error":       str | None
        }

    Example:
        >>> validate_ca_routing("000110011")
        {"valid": True, "bank": "Bank of Montreal (BMO)", "institution": "001", "transit": "00011", "error": None}
    """
    routing = _digits_only(routing)

    # Accept 8 digits (TTTTTIII) or 9 digits (0TTTTTIII — paper format)
    if len(routing) == 9 and routing[0] == "0":
        routing = routing[1:]  # strip leading zero (paper format)

    if len(routing) != 8:
        return _response(False, "Canadian routing number must be 8 digits (TTTTTIII)")

    # Extract components
    transit     = routing[:5]   # branch transit number
    institution = routing[5:8]  # institution number

    # Validate institution number
    bank_name = _INSTITUTIONS.get(institution)

    return _response(
        True,
        bank=bank_name,
        institution=institution,
        transit=transit,
    )


# ---------------------------------------------------------------------------
# CANADIAN ACCOUNT NUMBER VALIDATOR
# ---------------------------------------------------------------------------

def validate_ca_account(account: str) -> dict:
    """
    Validates a Canadian bank account number format.

    Note:
        Canadian account numbers vary by bank (7-12 digits).
        No standardized check digit algorithm exists across all banks.
        Validation is format-based only.

    Args:
        account: Account number string — digits only, 7 to 12 digits

    Returns:
        dict: {"valid": bool, "error": str | None}

    Example:
        >>> validate_ca_account("1234567")
        {"valid": True, "error": None}
    """
    account = _digits_only(account)

    if not (7 <= len(account) <= 12):
        return _response(False, "Canadian account number must be between 7 and 12 digits")

    return _response(True)