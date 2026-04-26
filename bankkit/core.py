from .data import BANKS
from .validators import validate_br_account


class BankKit:
    def __init__(self):
        self.banks = BANKS

    # -------------------------
    # internal helpers
    # -------------------------
    def resolve(self, name: str, country: str = None):
        bank = self.banks.get(name.lower())

        if not bank:
            return None

        if country and bank.get("country") != country:
            return None

        return bank

    def find_by_code(self, code: str, country: str = None):
        for bank in self.banks.values():
            if bank.get("code") == code:
                if country and bank.get("country") != country:
                    continue
                return bank
        return None

    # -------------------------
    # public API (SDK)
    # -------------------------
    def bank(self, name: str, country: str = None):
        result = self.resolve(name, country)

        if not result:
            return self._response(
                error=f"Bank '{name}' not found"
            )

        return self._response(data=result)

    def code(self, code: str, country: str = None):
        result = self.find_by_code(code, country)

        if not result:
            return self._response(
                error=f"Bank code '{code}' not found"
            )

        return self._response(data=result)

    def swift(self, name: str):
        bank = self.banks.get(name.lower())

        if not bank:
            return None

        return bank.get("swift")

    def validate_account(self, country: str, agency: str, account: str):
        if country.upper() == "BR":
            return validate_br_account(agency, account)

        return {
            "valid": False,
            "reason": f"Account validation for country '{country}' is not supported."
        }

    # -------------------------
    # response format
    # -------------------------
    def _response(self, data=None, error=None):
        return {
            "success": error is None,
            "data": data,
            "error": error
        }