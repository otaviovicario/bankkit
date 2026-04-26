from bankkit.core import BankKit

bank = BankKit()

print(bank.resolve("itau"))
print(bank.get_swift("itau"))
