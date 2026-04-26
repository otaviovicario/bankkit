from bankkit.core import BankKit

bk = BankKit()

# CPF
print(bk.validate_cpf("111.444.777-35"))

# CNPJ
print(bk.validate_cnpj("11.222.333/0001-81"))

# PIX
print(bk.validate_pix("user@email.com"))

# Conta BR
print(bk.validate_br_account("0001", "123456", code="341"))