# cores/northamerica/core_us.py
# BankKit US methods
# Delegates to validators/northamerica/validator_us.py

from bankkit.cores.northamerica.core_us import validate_routing


class BankKitUS:
    """United States banking validators."""

    def validate_routing(self, routing: str) -> dict:
        """Validates a US ABA Routing Number. See validators/northamerica/validator_us.py for details."""
        return validate_routing(routing)