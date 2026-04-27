# tests/universal/test_passport.py
# Test suite for passport validator
# Run with: pytest tests/

import pytest
from bankkit.validators.universal.validator_passport import validate_passport


class TestPassport:

    # --- Brazil ---
    def test_valid_br_passport(self):
        """Accepts valid Brazilian passport."""
        result = validate_passport("AB123456", "BR")
        assert result["valid"] is True
        assert result["country"] == "BR"

    def test_invalid_br_passport_wrong_format(self):
        """Rejects Brazilian passport with wrong format."""
        result = validate_passport("A123456", "BR")
        assert result["valid"] is False

    # --- USA ---
    def test_valid_us_passport(self):
        """Accepts valid US passport."""
        result = validate_passport("A12345678", "US")
        assert result["valid"] is True
        assert result["country"] == "US"

    def test_invalid_us_passport_too_short(self):
        """Rejects US passport with wrong length."""
        result = validate_passport("A1234567", "US")
        assert result["valid"] is False

    # --- Argentina ---
    def test_valid_ar_passport(self):
        """Accepts valid Argentine passport."""
        result = validate_passport("AAB123456", "AR")
        assert result["valid"] is True

    # --- Mexico ---
    def test_valid_mx_passport(self):
        """Accepts valid Mexican passport."""
        result = validate_passport("AB12345678", "MX")
        assert result["valid"] is True

    # --- Chile ---
    def test_valid_cl_passport(self):
        """Accepts valid Chilean passport."""
        result = validate_passport("A1234567", "CL")
        assert result["valid"] is True

    # --- Canada ---
    def test_valid_ca_passport(self):
        """Accepts valid Canadian passport."""
        result = validate_passport("AB123456", "CA")
        assert result["valid"] is True

    # --- Germany ---
    def test_valid_de_passport(self):
        """Accepts valid German passport."""
        result = validate_passport("C01X00T47", "DE")
        assert result["valid"] is True

    # --- UK ---
    def test_valid_gb_passport(self):
        """Accepts valid UK passport."""
        result = validate_passport("123456789", "GB")
        assert result["valid"] is True

    # --- Case insensitive ---
    def test_lowercase_input(self):
        """Accepts lowercase passport number."""
        result = validate_passport("ab123456", "br")
        assert result["valid"] is True

    # --- Unsupported country ---
    def test_unsupported_country(self):
        """Returns error for unsupported country."""
        result = validate_passport("AB123456", "ZZ")
        assert result["valid"] is False
        assert "not supported" in result["error"]

    # --- Empty ---
    def test_empty_number(self):
        """Rejects empty passport number."""
        result = validate_passport("", "BR")
        assert result["valid"] is False

    def test_empty_country(self):
        """Rejects empty country code."""
        result = validate_passport("AB123456", "")
        assert result["valid"] is False