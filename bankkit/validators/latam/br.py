# validators/latam/br.py
# Brazilian banking validators
# Standards: Receita Federal (CPF/CNPJ), BACEN (PIX, COMPE)

import re


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _digits_only(value: str) -> str:
    """Strip any non-digit characters from a string."""
    return re.sub(r"\D", "", value)


def _response(valid: bool, error: str = None, **extra) -> dict:
    """
    Standard response format for all validators.
    Always returns at least {"valid": bool, "error": str | None}.
    Extra keyword arguments are merged in when valid is True.
    """
    result = {"valid": valid, "error": error if not valid else None}
    if valid and extra:
        result.update(extra)
    return result


# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------

def validate_cpf(cpf: str) -> dict:
    """
    Validates a Brazilian CPF (Cadastro de Pessoas Físicas).

    Algorithm:
        - Must have exactly 11 digits
        - All digits cannot be the same (e.g. 111.111.111-11 is invalid)
        - Two check digits are calculated using weighted sums (mod 11)

    Args:
        cpf: CPF string — accepts formats like "111.222.333-96" or "11122233396"

    Returns:
        dict: {"valid": bool, "error": str | None}

    Example:
        >>> validate_cpf("111.222.333-96")
        {"valid": True, "error": None}
    """
    cpf = _digits_only(cpf)

    # Must have exactly 11 digits
    if len(cpf) != 11:
        return _response(False, "CPF must have 11 digits")

    # Reject sequences like 111.111.111-11 (technically pass the algorithm but are invalid)
    if len(set(cpf)) == 1:
        return _response(False, "Invalid CPF: all digits are the same")

    # --- First check digit ---
    # Multiply each of the first 9 digits by weights 10 down to 2
    total = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder = (total * 10) % 11
    first_digit = 0 if remainder >= 10 else remainder

    if first_digit != int(cpf[9]):
        return _response(False, "Invalid CPF: check digit mismatch")

    # --- Second check digit ---
    # Multiply each of the first 10 digits by weights 11 down to 2
    total = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder = (total * 10) % 11
    second_digit = 0 if remainder >= 10 else remainder

    if second_digit != int(cpf[10]):
        return _response(False, "Invalid CPF: check digit mismatch")

    return _response(True)


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------

def validate_cnpj(cnpj: str) -> dict:
    """
    Validates a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica).

    Algorithm:
        - Must have exactly 14 digits
        - All digits cannot be the same
        - Two check digits are calculated using weighted sums (mod 11)

    Args:
        cnpj: CNPJ string — accepts formats like "11.222.333/0001-81" or "11222333000181"

    Returns:
        dict: {"valid": bool, "error": str | None}

    Example:
        >>> validate_cnpj("11.222.333/0001-81")
        {"valid": True, "error": None}
    """
    cnpj = _digits_only(cnpj)

    # Must have exactly 14 digits
    if len(cnpj) != 14:
        return _response(False, "CNPJ must have 14 digits")

    # Reject sequences like 00.000.000/0000-00
    if len(set(cnpj)) == 1:
        return _response(False, "Invalid CNPJ: all digits are the same")

    # --- First check digit ---
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(cnpj[i]) * weights[i] for i in range(12))
    remainder = total % 11
    first_digit = 0 if remainder < 2 else 11 - remainder

    if first_digit != int(cnpj[12]):
        return _response(False, "Invalid CNPJ: check digit mismatch")

    # --- Second check digit ---
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(cnpj[i]) * weights[i] for i in range(13))
    remainder = total % 11
    second_digit = 0 if remainder < 2 else 11 - remainder

    if second_digit != int(cnpj[13]):
        return _response(False, "Invalid CNPJ: check digit mismatch")

    return _response(True)


# ---------------------------------------------------------------------------
# PIX
# ---------------------------------------------------------------------------

# PIX key types and their patterns
# Defined by BACEN (Banco Central do Brasil)
_PIX_PATTERNS = {
    "cpf":      r"^\d{11}$",
    "cnpj":     r"^\d{14}$",
    "phone":    r"^\+55\d{10,11}$",
    "email":    r"^[^@]+@[^@]+\.[^@]+$",
    "random":   r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
}


def validate_pix(key: str) -> dict:
    """
    Validates a Brazilian PIX key and identifies its type.

    PIX key types (defined by BACEN):
        - CPF:    11 digits
        - CNPJ:   14 digits
        - Phone:  E.164 format starting with +55
        - Email:  Standard email format
        - Random: UUID v4 format

    Args:
        key: The PIX key string in any supported format

    Returns:
        dict: {"valid": bool, "type": str, "error": str | None}

    Example:
        >>> validate_pix("11122233344")
        {"valid": True, "type": "CPF", "error": None}

        >>> validate_pix("user@email.com")
        {"valid": True, "type": "email", "error": None}
    """
    key = key.strip()

    for key_type, pattern in _PIX_PATTERNS.items():
        if re.match(pattern, key, re.IGNORECASE):

            # For CPF and CNPJ keys, also run the full check digit validation
            if key_type == "cpf":
                cpf_result = validate_cpf(key)
                if not cpf_result["valid"]:
                    return _response(False, f"PIX key looks like CPF but is invalid: {cpf_result['error']}")

            if key_type == "cnpj":
                cnpj_result = validate_cnpj(key)
                if not cnpj_result["valid"]:
                    return _response(False, f"PIX key looks like CNPJ but is invalid: {cnpj_result['error']}")

            return _response(True, type=key_type.upper())

    return _response(False, "Unrecognized PIX key format")


# ---------------------------------------------------------------------------
# BRAZILIAN BANK ACCOUNT
# ---------------------------------------------------------------------------

def validate_br_account(agency: str, account: str, code: str = None) -> dict:
    """
    Validates a Brazilian bank account (agency + account number).

    Note:
        Each Brazilian bank has its own check digit algorithm.
        Without knowing the bank, only format validation is possible.
        If a bank code (COMPE) is provided, the bank name is returned.

    Args:
        agency:  Agency number — must be exactly 4 digits
        account: Account number — must be between 5 and 12 digits
        code:    Optional COMPE bank code (e.g. "077" for Banco Inter)

    Returns:
        dict: {"valid": bool, "bank": str | None, "error": str | None}

    Example:
        >>> validate_br_account("0001", "123456", code="077")
        {"valid": True, "bank": "Banco Inter", "error": None}
    """
    agency = _digits_only(agency)
    account = _digits_only(account)

    # Agency must be exactly 4 digits
    if len(agency) != 4:
        return _response(False, "Agency must have exactly 4 digits")

    # Account must be between 5 and 12 digits
    if not (5 <= len(account) <= 12):
        return _response(False, "Account must have between 5 and 12 digits")

    # If a bank code is provided, look it up
    bank_name = None
    if code:
        from bankkit.data.latam.br import BANKS
        bank = BANKS.get(code.strip())
        if bank:
            bank_name = bank.get("name")
        else:
            return _response(False, f"Bank code '{code}' not found in COMPE registry")

    return _response(True, bank=bank_name)