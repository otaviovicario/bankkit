from .data import BANKS
from . validators import validate_br_account


class BankKit:
    def __init__(self):
        self.banks = BANKS

    def bank(self, name: str, country: str = None):
        bank = self.banks.get(name.lower())

        if not bank:
            return None

        if country and bank["country"] != country:
            return None

        return bank

    def code(self, code: str, country: str = None):
        for bank in self.banks.values():
            if bank.get("code") == code:
                if country and bank.get("country") != country:
                    continue
                return bank
        return None

    def swift(self, name: str):
        bank = self.banks.get(name.lower())
        if not bank:
            return None
        return bank["swift"]

    def validate_account(self,country: str, agency: str, account: str):
        if country.upper() == "BR":
            return validate_br_account(agency, account)

        return {"valid": False,
                "message": f"Account validation for country '{country}' is not supported."}

