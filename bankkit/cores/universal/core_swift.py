# cores/universal/core_swift.py
# BankKit SWIFT methods
# Delegates to validators/universal/validator_swift.py

from bankkit.validators.universal.validator_swift import validate_swift


class BankKitSWIFT:
    """Universal SWIFT/BIC validator."""

    def validate_swift(self, swift: str) -> dict:
        """Validates a SWIFT/BIC code. See validators/universal/validator_swift.py for details."""
        return validate_swift(swift)