# tests/northamerica/test_us.py
# Test suite for US banking validators
# Run with: pytest tests/

import pytest
from bankkit.validators.northamerica.validator_us import validate_routing


class TestRoutingNumber:

    def test_valid_jpmorgan(self):
        """Accepts JPMorgan Chase routing number."""
        result = validate_routing("021000021")
        assert result["valid"] is True
        assert result["district"] == "New York"

    def test_valid_citibank(self):
        """Accepts Citibank routing number."""
        result = validate_routing("021000089")
        assert result["valid"] is True
        assert result["district"] == "New York"

    def test_valid_bank_of_america(self):
        """Accepts Bank of America routing number."""
        result = validate_routing("011000138")
        assert result["valid"] is True
        assert result["district"] == "Boston"

    def test_valid_wells_fargo(self):
        """Accepts Wells Fargo routing number."""
        result = validate_routing("121000248")
        assert result["valid"] is True
        assert result["district"] == "San Francisco"

    def test_valid_with_dashes(self):
        """Accepts routing number with dashes."""
        result = validate_routing("021-000-021")
        assert result["valid"] is True

    def test_invalid_check_digit(self):
        """Rejects routing number with wrong check digit."""
        result = validate_routing("021000022")
        assert result["valid"] is False
        assert "check digit" in result["error"]

    def test_invalid_district(self):
        """Rejects routing number with invalid Federal Reserve district."""
        result = validate_routing("991000021")
        assert result["valid"] is False
        assert "district" in result["error"]

    def test_invalid_too_short(self):
        """Rejects routing number with less than 9 digits."""
        result = validate_routing("02100002")
        assert result["valid"] is False
        assert "9 digits" in result["error"]

    def test_invalid_too_long(self):
        """Rejects routing number with more than 9 digits."""
        result = validate_routing("0210000210")
        assert result["valid"] is False

    def test_invalid_empty(self):
        """Rejects empty string."""
        result = validate_routing("")
        assert result["valid"] is False