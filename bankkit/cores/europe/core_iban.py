# cores/europe/core_iban.py
# BankKit IBAN methods
# Delegates to validator_iban.py

from bankkit.validators.europe.validator_iban import validate_iban


class BankKitIBAN:
    """IBAN validator — covers 80+ countries worldwide."""

    def validate_iban(self, iban: str) -> dict:
        """Validates an IBAN and returns country info. See validators/europe/iban.py for details."""
        return validate_iban(iban)