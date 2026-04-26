# tests/universal/test_card.py
# Test suite for card and BIN validators
# Run with: pytest tests/

import pytest
from bankkit.validators.universal.card import validate_card, validate_bin


# ---------------------------------------------------------------------------
# CARD VALIDATOR
# ---------------------------------------------------------------------------

class TestCard:

    def test_valid_visa(self):
        """Accepts valid Visa card number."""
        result = validate_card("4111111111111111")
        assert result["valid"] is True
        assert result["brand"] == "Visa"

    def test_valid_visa_with_spaces(self):
        """Accepts Visa card with spaces."""
        result = validate_card("4111 1111 1111 1111")
        assert result["valid"] is True
        assert result["brand"] == "Visa"

    def test_valid_visa_with_dashes(self):
        """Accepts Visa card with dashes."""
        result = validate_card("4111-1111-1111-1111")
        assert result["valid"] is True

    def test_valid_mastercard(self):
        """Accepts valid Mastercard number."""
        result = validate_card("5500005555555559")
        assert result["valid"] is True
        assert result["brand"] == "Mastercard"

    def test_valid_amex(self):
        """Accepts valid American Express number."""
        result = validate_card("378282246310005")
        assert result["valid"] is True
        assert result["brand"] == "Amex"

    def test_valid_discover(self):
        """Accepts valid Discover card number."""
        result = validate_card("6011111111111117")
        assert result["valid"] is True
        assert result["brand"] == "Discover"

    def test_valid_diners(self):
        """Accepts valid Diners Club card number."""
        result = validate_card("30569309025904")
        assert result["valid"] is True
        assert result["brand"] == "Diners Club"

    def test_valid_jcb(self):
        """Accepts valid JCB card number."""
        result = validate_card("3530111333300000")
        assert result["valid"] is True
        assert result["brand"] == "JCB"

    def test_invalid_luhn(self):
        """Rejects card that fails Luhn check."""
        result = validate_card("4111111111111112")
        assert result["valid"] is False
        assert "Luhn" in result["error"]

    def test_invalid_too_short(self):
        """Rejects card number that is too short."""
        result = validate_card("41111111111")
        assert result["valid"] is False

    def test_invalid_too_long(self):
        """Rejects card number that is too long."""
        result = validate_card("411111111111111111111")
        assert result["valid"] is False

    def test_invalid_letters(self):
        """Rejects card number with letters."""
        result = validate_card("4111111111111abc")
        assert result["valid"] is False

    def test_invalid_empty(self):
        """Rejects empty string."""
        result = validate_card("")
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# BIN VALIDATOR
# ---------------------------------------------------------------------------

class TestBIN:

    def test_valid_visa_bin(self):
        """Detects Visa from BIN."""
        result = validate_bin("411111")
        assert result["valid"] is True
        assert result["brand"] == "Visa"

    def test_valid_mastercard_bin(self):
        """Detects Mastercard from BIN."""
        result = validate_bin("550000")
        assert result["valid"] is True
        assert result["brand"] == "Mastercard"

    def test_valid_amex_bin(self):
        """Detects Amex from BIN."""
        result = validate_bin("378282")
        assert result["valid"] is True
        assert result["brand"] == "Amex"

    def test_valid_elo_bin(self):
        """Detects Elo (Brazilian) from BIN."""
        result = validate_bin("401100")
        assert result["valid"] is True
        assert result["brand"] == "Elo"

    def test_invalid_bin_too_short(self):
        """Rejects BIN with less than 6 digits."""
        result = validate_bin("41111")
        assert result["valid"] is False

    def test_invalid_bin_too_long(self):
        """Rejects BIN with more than 6 digits."""
        result = validate_bin("4111111")
        assert result["valid"] is False

    def test_invalid_bin_unrecognized(self):
        """Rejects unrecognized BIN."""
        result = validate_bin("000000")
        assert result["valid"] is False

    def test_invalid_bin_empty(self):
        """Rejects empty BIN."""
        result = validate_bin("")
        assert result["valid"] is False