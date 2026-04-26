# cores/latam/core_br.py
# BankKit Brazilian methods
# Delegates to validator_br.py

from bankkit.validators.latam.validator_br import (
    validate_cpf,
    validate_cnpj,
    validate_pix,
    validate_br_account,
)


class BankKitBR:
    """Brazilian banking validators."""

    def validate_cpf(self, cpf: str) -> dict:
        """Validates a Brazilian CPF. See validators/latam/br.py for details."""
        return validate_cpf(cpf)

    def validate_cnpj(self, cnpj: str) -> dict:
        """Validates a Brazilian CNPJ. See validators/latam/br.py for details."""
        return validate_cnpj(cnpj)

    def validate_pix(self, key: str) -> dict:
        """Validates a Brazilian PIX key and identifies its type. See validators/latam/br.py for details."""
        return validate_pix(key)

    def validate_br_account(self, agency: str, account: str, code: str = None) -> dict:
        """Validates a Brazilian bank account. See validators/latam/br.py for details."""
        return validate_br_account(agency, account, code)