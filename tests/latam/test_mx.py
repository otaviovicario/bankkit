# tests/latam/test_mx.py
# Test suite for Mexican banking validators
# Run with: pytest tests/

import pytest
from bankkit.validators.latam.validator_mx import validate_clabe


class TestCLABE:

    def test_valid_clabe(self):
        """Accepts a valid CLABE."""
        result = validate_clabe("032180000118359719")
        assert result["valid"] is True
        assert result["bank_code"] == "032"

    def test_valid_clabe_with_spaces(self):
        """Accepts CLABE with spaces."""
        result = validate_clabe("0321 8000 0118 3597 19")
        assert result["valid"] is True

    def test_valid_clabe_with_dashes(self):
        """Accepts CLABE with dashes."""
        result = validate_clabe("032-180-000118359719")
        assert result["valid"] is True

    def test_invalid_check_digit(self):
        """Rejects CLABE with wrong check digit."""
        result = validate_clabe("032180000118359710")
        assert result["valid"] is False
        assert "check digit" in result["error"]

    def test_invalid_too_short(self):
        """Rejects CLABE with less than 18 digits."""
        result = validate_clabe("03218000011835971")
        assert result["valid"] is False
        assert "18 digits" in result["error"]

    def test_invalid_too_long(self):
        """Rejects CLABE with more than 18 digits."""
        result = validate_clabe("0321800001183597190")
        assert result["valid"] is False

    def test_invalid_empty(self):
        """Rejects empty string."""
        result = validate_clabe("")
        assert result["valid"] is False

    def test_returns_bank_code(self):
        """Returns bank_code in response."""
        result = validate_clabe("032180000118359719")
        assert result["bank_code"] == "032"