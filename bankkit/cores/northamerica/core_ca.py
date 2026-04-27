# cores/northamerica/core_ca.py
# BankKit Canadian methods
# Delegates to validators/northamerica/validator_ca.py

from bankkit.validators.northamerica.validator_ca import (
    validate_ca_routing,
    validate_ca_account,
)


class BankKitCA:
    """Canadian banking validators."""

    def validate_ca_routing(self, routing: str) -> dict:
        """Validates a Canadian routing number. See validators/northamerica/validator_ca.py for details."""
        return validate_ca_routing(routing)

    def validate_ca_account(self, account: str) -> dict:
        """Validates a Canadian account number. See validators/northamerica/validator_ca.py for details."""
        return validate_ca_account(account)
    