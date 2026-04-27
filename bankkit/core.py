# core.py
# BankKit — main entry point
# Aggregates all regional cores into a single class

from bankkit.cores.latam.core_br import BankKitBR
from bankkit.cores.universal.core_card import BankKitCard
from bankkit.cores.universal.core_swift import BankKitSWIFT
from bankkit.cores.europe.core_iban import BankKitIBAN
from bankkit.cores.latam.core_ar import BankKitAR
from bankkit.cores.northamerica.core_us import BankKitUS
from bankkit.cores.latam.core_mx import BankKitMX
from bankkit.cores.latam.core_cl import BankKitCL
from bankkit.cores.northamerica.core_ca import BankKitCA
from bankkit.cores.universal.core_passport import BankKitPassport


class BankKit(BankKitBR, BankKitCard, BankKitIBAN, BankKitSWIFT, BankKitAR, BankKitUS, BankKitMX, BankKitCL, BankKitCA, BankKitPassport):
    """
    BankKit — Python SDK for validating banking data.
    Built for Latin America, ready for the world.

    Usage:
        from bankkit import BankKit

        bk = BankKit()
        bk.validate_cpf("111.444.777-35")
        bk.validate_card("4111 1111 1111 1111")
        bk.validate_iban("GB82WEST12345698765432")
        bk.validate_swift("BRASBRRJXXX")
    """
    pass