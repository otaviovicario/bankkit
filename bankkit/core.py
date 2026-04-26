# core.py
# BankKit — main entry point
# Aggregates all regional cores into a single class

from bankkit.cores.latam.core_br import BankKitBR
from bankkit.cores.universal.core_card import BankKitCard


class BankKit(BankKitBR, BankKitCard):
    """
    BankKit — Python SDK for validating banking data.
    Built for Latin America, ready for the world.

    Usage:
        from bankkit import BankKit

        bk = BankKit()
        bk.validate_cpf("111.444.777-35")
        bk.validate_card("4111 1111 1111 1111")
    """
    pass
