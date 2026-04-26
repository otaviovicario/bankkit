# tests/universal/test_swift.py
# Test suite for SWIFT/BIC validator
# Run with: pytest tests/

import pytest
from bankkit.validators.universal.validator_swift import validate_swift


class TestSWIFT:

    def test_valid_swift_8_chars(self):
        """Accepts valid 8-character SWIFT (no branch)."""
        result = validate_swift("BRASBRRJ")
        assert result["valid"] is True
        assert result["bank_code"] == "BRAS"
        assert result["country"] == "BR"
        assert result["branch"] == "XXX"

    def test_valid_swift_11_chars(self):
        """Accepts valid 11-character SWIFT (with branch)."""
        result = validate_swift("BRASBRRJXXX")
        assert result["valid"] is True
        assert result["branch"] == "XXX"

    def test_valid_swift_lowercase(self):
        """Accepts lowercase SWIFT input."""
        result = validate_swift("brasbrrjxxx")
        assert result["valid"] is True

    def test_valid_swift_with_spaces(self):
        """Accepts SWIFT with leading/trailing spaces."""
        result = validate_swift("  BRASBRRJ  ")
        assert result["valid"] is True

    def test_valid_swift_itau(self):
        """Accepts Itaú SWIFT code."""
        result = validate_swift("ITAUBRSP")
        assert result["valid"] is True
        assert result["bank_code"] == "ITAU"
        assert result["country"] == "BR"

    def test_valid_swift_deutsche(self):
        """Accepts Deutsche Bank SWIFT code."""
        result = validate_swift("DEUTDEDB")
        assert result["valid"] is True
        assert result["country"] == "DE"

    def test_invalid_wrong_length(self):
        """Rejects SWIFT with wrong length."""
        result = validate_swift("BRASPRRJ12")
        assert result["valid"] is False
        assert "8 or 11" in result["error"]

    def test_invalid_country_code(self):
        """Rejects SWIFT with invalid country code."""
        result = validate_swift("BRASXXRJ")
        assert result["valid"] is False
        assert "country code" in result["error"]

    def test_invalid_format_digits_in_bank(self):
        """Rejects SWIFT with digits in bank code position."""
        result = validate_swift("1234BRRJ")
        assert result["valid"] is False

    def test_invalid_empty(self):
        """Rejects empty string."""
        result = validate_swift("")
        assert result["valid"] is False