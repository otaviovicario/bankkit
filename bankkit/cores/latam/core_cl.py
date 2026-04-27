# cores/latam/core_cl.py
# BankKit Chilean methods
# Delegates to validators/latam/validator_cl.py

from bankkit.validators.latam.validator_cl import validate_rut


class BankKitCL:
    """Chilean banking validators."""

    def validate_rut(self, rut: str) -> dict:
        """Validates a Chilean RUT. See validators/latam/validator_cl.py for details."""
        return validate_rut(rut)