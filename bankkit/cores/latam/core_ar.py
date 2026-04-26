# cores/latam/core_ar.py
# BankKit Argentine methods
# Delegates to validators/latam/validator_ar.py

from bankkit.validators.latam.validator_ar import validate_cbu


class BankKitAR:
    """Argentine banking validators."""

    def validate_cbu(self, cbu: str) -> dict:
        """Validates an Argentine CBU. See validators/latam/validator_ar.py for details."""
        return validate_cbu(cbu)