from bankkit.core import BankKit

bank = BankKit()

print("--- Testando API do BankKit ---\n")

print("Buscar banco por nome:")
print(bank.bank("itau"))

print("Buscar banco por código:")
print(bank.code("341"))

print("Buscar SWIFT por nome:")
print(bank.swift("itau"))

print("Validar conta:")
print(bank.validate_account("BR", "0001", "567890"))

