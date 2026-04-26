from .data import BANKS
from .validators import validate_br_account


class BankKit:
    def __init__(self):
        self.banks = BANKS

    # -------------------------
    # API PUBLICA
    # -------------------------
    def bank(self, name: str, country: str = None):
        bank = self.banks.get(name.lower())

        if not bank:
            return self._response(error=f"Bank '{name}' not found")

        if country and bank.get("country") != country:
            return self._response(error=f"Bank '{name}' not found in {country}")

        return self._response(data=bank)

    def code(self, code: str, country: str = None):
        for bank in self.banks.values():
            if bank.get("code") == code:
                if country and bank.get("country") != country:
                    continue
                return self._response(data=bank)

        return self._response(error=f"Bank code '{code}' not found")

    def swift(self, name: str):
        bank = self.banks.get(name.lower())

        if not bank:
            return self._response(error=f"Bank '{name}' not found")

        return self._response(data=bank.get("swift"))

    def validate_account(self, country: str, agency: str, account: str):
        if country.upper() == "BR":
            return self._wrap_validate(validate_br_account(agency, account))

        return self._response(
            error=f"Account validation for country '{country}' is not supported."
        )

    # -------------------------
    # helpers
    # -------------------------
    def _response(self, data=None, error=None):
        return {
            "success": error is None,
            "data": data,
            "error": error
        }

    def _wrap_validate(self, result: dict):
        return {
            "success": result.get("valid", False),
            "data": None,
            "error": None if result.get("valid") else result.get("reason")
        }