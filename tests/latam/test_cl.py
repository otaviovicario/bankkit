# tests/latam/test_cl.py
# Test suite for Chilean banking validators
# Run with: pytest tests/

import pytest
from bankkit.validators.latam.validator_cl import validate_rut


class TestRUT:

    def test_valid_rut_formatted(self):
        """Accepts valid RUT with dots and dash."""
        result = validate_rut("12.345.678-5")
        assert result["valid"] is True

    def test_valid_rut_digits_only(self):
        """Accepts valid RUT with digits only."""
        result = validate_rut("123456785")
        assert result["valid"] is True

    def test_valid_rut_with_k(self):
        """Accepts valid RUT with K check digit."""
        result = validate_rut("76.354.771-K")
        assert result["valid"] is True

    def test_valid_rut_with_k_lowercase(self):
        """Accepts valid RUT with lowercase k check digit."""
        result = validate_rut("76.354.771-k")
        assert result["valid"] is True

    def test_valid_rut_short(self):
        """Accepts valid short RUT (7 digits)."""
        result = validate_rut("5.126.663-3")
        assert result["valid"] is True

    def test_invalid_check_digit(self):
        """Rejects RUT with wrong check digit."""
        result = validate_rut("12.345.678-0")
        assert result["valid"] is False
        assert "check digit" in result["error"]

    def test_invalid_too_short(self):
        """Rejects RUT that is too short."""
        result = validate_rut("1")
        assert result["valid"] is False

    def test_invalid_letters_in_number(self):
        """Rejects RUT with letters in number part."""
        result = validate_rut("1234ABC-5")
        assert result["valid"] is False

    def test_invalid_empty(self):
        """Rejects empty string."""
        result = validate_rut("")
        assert result["valid"] is False