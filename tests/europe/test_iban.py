# tests/europe/test_iban.py
# Test suite for IBAN validator
# Run with: pytest tests/

import pytest
from bankkit.validators.europe.validator_iban import validate_iban


class TestIBAN:

    def test_valid_gb(self):
        """Accepts valid UK IBAN."""
        result = validate_iban("GB82WEST12345698765432")
        assert result["valid"] is True
        assert result["code"] == "GB"
        assert result["country"] == "United Kingdom"

    def test_valid_gb_with_spaces(self):
        """Accepts UK IBAN formatted with spaces."""
        result = validate_iban("GB82 WEST 1234 5698 7654 32")
        assert result["valid"] is True

    def test_valid_de(self):
        """Accepts valid German IBAN."""
        result = validate_iban("DE89370400440532013000")
        assert result["valid"] is True
        assert result["code"] == "DE"
        assert result["country"] == "Germany"

    def test_valid_fr(self):
        """Accepts valid French IBAN."""
        result = validate_iban("FR7630006000011234567890189")
        assert result["valid"] is True
        assert result["code"] == "FR"
        assert result["country"] == "France"

    def test_valid_pt(self):
        """Accepts valid Portuguese IBAN."""
        result = validate_iban("PT50000201231234567890154")
        assert result["valid"] is True
        assert result["code"] == "PT"
        assert result["country"] == "Portugal"

    def test_valid_br(self):
        """Accepts valid Brazilian IBAN."""
        result = validate_iban("BR1800360305000010009795493C1")
        assert result["valid"] is True
        assert result["code"] == "BR"
        assert result["country"] == "Brazil"

    def test_valid_ch(self):
        """Accepts valid Swiss IBAN."""
        result = validate_iban("CH5604835012345678009")
        assert result["valid"] is True
        assert result["code"] == "CH"
        assert result["country"] == "Switzerland"

    def test_invalid_check_digit(self):
        """Rejects IBAN with wrong check digit (MOD 97 fails)."""
        result = validate_iban("GB00WEST12345698765432")
        assert result["valid"] is False
        assert "MOD 97" in result["error"]

    def test_invalid_country_code(self):
        """Rejects IBAN with unknown country code."""
        result = validate_iban("XX82WEST12345698765432")
        assert result["valid"] is False
        assert "Unknown country code" in result["error"]

    def test_invalid_wrong_length(self):
        """Rejects IBAN with incorrect length for country."""
        result = validate_iban("GB82WEST123456987654")
        assert result["valid"] is False
        assert "length" in result["error"]

    def test_invalid_format_no_letters(self):
        """Rejects IBAN that does not start with letters."""
        result = validate_iban("8282WEST12345698765432")
        assert result["valid"] is False

    def test_invalid_empty(self):
        """Rejects empty string."""
        result = validate_iban("")
        assert result["valid"] is False