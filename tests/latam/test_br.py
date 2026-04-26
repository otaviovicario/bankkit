# tests/latam/test_br.py
# Test suite for Brazilian banking validators
# Run with: pytest tests/

import pytest
from bankkit.validators.latam.br import (
    validate_cpf,
    validate_cnpj,
    validate_pix,
    validate_br_account,
)


# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------

class TestCPF:

    def test_valid_cpf_formatted(self):
        """Accepts formatted CPF with dots and dash."""
        result = validate_cpf("111.444.777-35")
        assert result["valid"] is True

    def test_valid_cpf_digits_only(self):
        """Accepts CPF with digits only."""
        result = validate_cpf("11144477735")
        assert result["valid"] is True

    def test_invalid_cpf_wrong_digit(self):
        """Rejects CPF with wrong check digit."""
        result = validate_cpf("111.444.777-00")
        assert result["valid"] is False
        assert result["error"] is not None

    def test_invalid_cpf_all_same_digits(self):
        """Rejects CPF where all digits are the same."""
        result = validate_cpf("111.111.111-11")
        assert result["valid"] is False

    def test_invalid_cpf_too_short(self):
        """Rejects CPF with less than 11 digits."""
        result = validate_cpf("1234567")
        assert result["valid"] is False

    def test_invalid_cpf_too_long(self):
        """Rejects CPF with more than 11 digits."""
        result = validate_cpf("123456789012")
        assert result["valid"] is False

    def test_invalid_cpf_empty(self):
        """Rejects empty string."""
        result = validate_cpf("")
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------

class TestCNPJ:

    def test_valid_cnpj_formatted(self):
        """Accepts formatted CNPJ with dots, slash and dash."""
        result = validate_cnpj("11.222.333/0001-81")
        assert result["valid"] is True

    def test_valid_cnpj_digits_only(self):
        """Accepts CNPJ with digits only."""
        result = validate_cnpj("11222333000181")
        assert result["valid"] is True

    def test_invalid_cnpj_wrong_digit(self):
        """Rejects CNPJ with wrong check digit."""
        result = validate_cnpj("11.222.333/0001-00")
        assert result["valid"] is False
        assert result["error"] is not None

    def test_invalid_cnpj_all_same_digits(self):
        """Rejects CNPJ where all digits are the same."""
        result = validate_cnpj("00.000.000/0000-00")
        assert result["valid"] is False

    def test_invalid_cnpj_too_short(self):
        """Rejects CNPJ with less than 14 digits."""
        result = validate_cnpj("1122233300018")
        assert result["valid"] is False

    def test_invalid_cnpj_empty(self):
        """Rejects empty string."""
        result = validate_cnpj("")
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# PIX
# ---------------------------------------------------------------------------

class TestPIX:

    def test_valid_pix_cpf(self):
        """Detects and validates CPF PIX key."""
        result = validate_pix("11144477735")
        assert result["valid"] is True
        assert result["type"] == "CPF"

    def test_valid_pix_cnpj(self):
        """Detects and validates CNPJ PIX key."""
        result = validate_pix("11222333000181")
        assert result["valid"] is True
        assert result["type"] == "CNPJ"

    def test_valid_pix_email(self):
        """Detects valid email PIX key."""
        result = validate_pix("user@email.com")
        assert result["valid"] is True
        assert result["type"] == "EMAIL"

    def test_valid_pix_phone(self):
        """Detects valid phone PIX key in E.164 format."""
        result = validate_pix("+5511999999999")
        assert result["valid"] is True
        assert result["type"] == "PHONE"

    def test_valid_pix_random(self):
        """Detects valid random UUID PIX key."""
        result = validate_pix("123e4567-e89b-12d3-a456-426614174000")
        assert result["valid"] is True
        assert result["type"] == "RANDOM"

    def test_invalid_pix_cpf_bad_digit(self):
        """Rejects PIX key that looks like CPF but has wrong check digit."""
        result = validate_pix("11144477700")
        assert result["valid"] is False

    def test_invalid_pix_unknown_format(self):
        """Rejects unrecognized PIX key format."""
        result = validate_pix("not-a-valid-key")
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# BRAZILIAN BANK ACCOUNT
# ---------------------------------------------------------------------------

class TestBRAccount:

    def test_valid_account_no_code(self):
        """Validates account and agency format without bank code."""
        result = validate_br_account("0001", "123456")
        assert result["valid"] is True

    def test_valid_account_with_formatted_input(self):
        """Accepts account with dash (e.g. 12345-6)."""
        result = validate_br_account("0001", "12345-6")
        assert result["valid"] is True

    def test_invalid_agency_too_short(self):
        """Rejects agency with less than 4 digits."""
        result = validate_br_account("001", "123456")
        assert result["valid"] is False

    def test_invalid_agency_too_long(self):
        """Rejects agency with more than 4 digits."""
        result = validate_br_account("00011", "123456")
        assert result["valid"] is False

    def test_invalid_account_too_short(self):
        """Rejects account with less than 5 digits."""
        result = validate_br_account("0001", "1234")
        assert result["valid"] is False

    def test_invalid_account_too_long(self):
        """Rejects account with more than 12 digits."""
        result = validate_br_account("0001", "1234567890123")
        assert result["valid"] is False

    def test_invalid_bank_code(self):
        """Rejects unknown bank code."""
        result = validate_br_account("0001", "123456", code="999")
        assert result["valid"] is False
        assert result["error"] is not None