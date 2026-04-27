# cores/latam/core_mx.py
# BankKit Mexican methods
# Delegates to validators/latam/validator_mx.py

from bankkit.validators.latam.validator_mx import validate_clabe


class BankKitMX:
    """Mexican banking validators."""

    def validate_clabe(self, clabe: str) -> dict:
        """Validates a Mexican CLABE. See validators/latam/validator_mx.py for details."""
        return validate_clabe(clabe)