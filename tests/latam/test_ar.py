# tests/latam/test_ar.py
# Test suite for Argentine banking validators
# Run with: pytest tests/

import pytest
from bankkit.validators.latam.validator_ar import validate_cbu


class TestCBU:

    def test_valid_cbu(self):
        """Accepts a valid CBU."""
        result = validate_cbu("0720599600000057836902")
        assert result["valid"] is True

    def test_valid_cbu_with_spaces(self):
        """Accepts CBU with spaces."""
        result = validate_cbu("0720 5996 0000 0057 8369 02")
        assert result["valid"] is True

    def test_invalid_cbu_wrong_length_short(self):
        """Rejects CBU with less than 22 digits."""
        result = validate_cbu("072059960000005783690")
        assert result["valid"] is False
        assert "22 digits" in result["error"]

    def test_invalid_cbu_wrong_length_long(self):
        """Rejects CBU with more than 22 digits."""
        result = validate_cbu("07205996000000578369020")
        assert result["valid"] is False

    def test_invalid_cbu_block1_check_digit(self):
        """Rejects CBU with wrong block 1 check digit."""
        result = validate_cbu("0720599700000057836902")
        assert result["valid"] is False
        assert "block 1" in result["error"]

    def test_invalid_cbu_block2_check_digit(self):
        """Rejects CBU with wrong block 2 check digit."""
        result = validate_cbu("0720599600000057836901")
        assert result["valid"] is False
        assert "block 2" in result["error"]

    def test_invalid_cbu_empty(self):
        """Rejects empty string."""
        result = validate_cbu("")
        assert result["valid"] is False