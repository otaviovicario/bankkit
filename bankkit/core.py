from .data import BANKS


class BankKit:
    def __init__(self):
        self.banks = BANKS

    def resolve(self, name: str, country: str = None):
        bank = self.banks.get(name.lower())

        if not bank:
            return None

        if country and bank["country"] != country:
            return None

        return bank

    def get_swift(self, name: str):
        bank = self.banks.get(name.lower())
        if not bank:
            return None
        return bank["swift"]