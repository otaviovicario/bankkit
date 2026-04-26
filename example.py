from bankkit.core import BankKit

bank = BankKit()

print(bank.bank("itau"))
print(bank.code("341"))
print(bank.swift("itau"))
print(bank.validate_account("BR", "0001", "567890"))