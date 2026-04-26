# cores/universal/core_card.py
# BankKit card methods
# Delegates to validator_card.py

from bankkit.validators.universal.validator_card import validate_card, validate_bin


class BankKitCard:
    """Universal card validators."""

    def validate_card(self, number: str) -> dict:
        """Validates a credit or debit card number. See validators/universal/card.py for details."""
        return validate_card(number)

    def validate_bin(self, bin_number: str) -> dict:
        """Validates a BIN (first 6 digits) and identifies the card brand. See validators/universal/card.py for details."""
        return validate_bin(bin_number)