# bankkit/core.py
# Main entry point for BankKit SDK
# All public methods are defined here and delegate to the appropriate validators

from .validators.latam.br import (
    validate_cpf,
    validate_cnpj,
    validate_pix,
    validate_br_account,
)


class BankKit:
    """
    BankKit — Python SDK for validating banking data.
    Built for Latin America, ready for the world.

    Usage:
        from bankkit import BankKit

        bk = BankKit()
        bk.validate_cpf("111.444.777-35")
        bk.validate_pix("user@email.com")
    """

    # -------------------------------------------------------------------------
    # BRAZIL
    # -------------------------------------------------------------------------

    def validate_cpf(self, cpf: str) -> dict:
        """
        Validates a Brazilian CPF number.

        Args:
            cpf: CPF string — accepts "111.444.777-35" or "11144477735"

        Returns:
            dict: {"valid": bool, "error": str | None}

        Example:
            >>> bk.validate_cpf("111.444.777-35")
            {"valid": True, "error": None}
        """
        return validate_cpf(cpf)

    def validate_cnpj(self, cnpj: str) -> dict:
        """
        Validates a Brazilian CNPJ number.

        Args:
            cnpj: CNPJ string — accepts "11.222.333/0001-81" or "11222333000181"

        Returns:
            dict: {"valid": bool, "error": str | None}

        Example:
            >>> bk.validate_cnpj("11.222.333/0001-81")
            {"valid": True, "error": None}
        """
        return validate_cnpj(cnpj)

    def validate_pix(self, key: str) -> dict:
        """
        Validates a Brazilian PIX key and identifies its type.

        Args:
            key: PIX key — CPF, CNPJ, email, phone (+55), or random UUID

        Returns:
            dict: {"valid": bool, "type": str, "error": str | None}

        Example:
            >>> bk.validate_pix("user@email.com")
            {"valid": True, "type": "EMAIL", "error": None}
        """
        return validate_pix(key)

    def validate_br_account(self, agency: str, account: str, code: str = None) -> dict:
        """
        Validates a Brazilian bank account (agency + account number).

        Args:
            agency:  Agency number — must be exactly 4 digits
            account: Account number — must be between 5 and 12 digits
            code:    Optional COMPE bank code (e.g. "077" for Banco Inter)

        Returns:
            dict: {"valid": bool, "bank": str | None, "error": str | None}

        Example:
            >>> bk.validate_br_account("0001", "123456", code="341")
            {"valid": True, "bank": "Itaú Unibanco", "error": None}
        """
        return validate_br_account(agency, account, code)

    # -------------------------------------------------------------------------
    # COMING SOON
    # -------------------------------------------------------------------------
    # validate_iban()       — ISO 13616
    # validate_swift()      — ISO 9362
    # validate_card()       — ISO 7812 + Luhn
    # validate_bin()        — BIN lookup
    # validate_clabe()      — Mexico BANXICO
    # validate_cbu()        — Argentina BCRA
    # validate_routing()    — US ABA