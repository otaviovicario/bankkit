# tests/northamerica/test_ca.py
# Test suite for Canadian banking validators
# Run with: pytest tests/

import pytest
from bankkit.validators.northamerica.validator_ca import (
    validate_ca_routing,
    validate_ca_account,
)


class TestCARouting:

    def test_valid_routing_bmo(self):
        """Accepts valid BMO routing number."""
        result = validate_ca_routing("000011001")  # 0 + transit(00001) + inst(001)
        assert result["valid"] is True
        assert result["institution"] == "001"
        assert result["transit"] == "00011"
        assert result["bank"] == "Bank of Montreal (BMO)"

    def test_valid_routing_rbc(self):
        """Accepts valid RBC routing number."""
        result = validate_ca_routing("000013003")  # 0 + transit(00013) + inst(003)
        assert result["valid"] is True
        assert result["institution"] == "003"
        assert result["bank"] == "Royal Bank of Canada (RBC)"

    def test_valid_routing_paper_format(self):
        """Accepts 9-digit paper format with leading zero."""
        result = validate_ca_routing("000011001")
        assert result["valid"] is True

    def test_valid_routing_electronic_format(self):
        """Accepts 8-digit electronic format."""
        result = validate_ca_routing("00011001")
        assert result["valid"] is True

    def test_valid_routing_unknown_institution(self):
        """Accepts routing with unknown institution — still valid format."""
        result = validate_ca_routing("00011999")
        assert result["valid"] is True
        assert result["bank"] is None

    def test_invalid_routing_too_short(self):
        """Rejects routing with less than 8 digits."""
        result = validate_ca_routing("0001100")
        assert result["valid"] is False
        assert "8 digits" in result["error"]

    def test_invalid_routing_too_long(self):
        """Rejects routing with more than 9 digits."""
        result = validate_ca_routing("0000110011234")
        assert result["valid"] is False

    def test_invalid_routing_empty(self):
        """Rejects empty string."""
        result = validate_ca_routing("")
        assert result["valid"] is False


class TestCAAccount:

    def test_valid_account_7_digits(self):
        """Accepts account with 7 digits."""
        result = validate_ca_account("1234567")
        assert result["valid"] is True

    def test_valid_account_12_digits(self):
        """Accepts account with 12 digits."""
        result = validate_ca_account("123456789012")
        assert result["valid"] is True

    def test_invalid_account_too_short(self):
        """Rejects account with less than 7 digits."""
        result = validate_ca_account("123456")
        assert result["valid"] is False

    def test_invalid_account_too_long(self):
        """Rejects account with more than 12 digits."""
        result = validate_ca_account("1234567890123")
        assert result["valid"] is False

    def test_invalid_account_empty(self):
        """Rejects empty string."""
        result = validate_ca_account("")
        assert result["valid"] is False