# cores/universal/core_passport.py
# BankKit passport methods
# Delegates to validators/universal/validator_passport.py

from bankkit.validators.universal.validator_passport import validate_passport


class BankKitPassport:
    """Universal passport validator — covers 30+ countries."""

    def validate_passport(self, number: str, country: str) -> dict:
        """Validates a passport number by country format. See validators/universal/validator_passport.py for details."""
        return validate_passport(number, country)