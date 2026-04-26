# 🏦 BankKit

> **Python SDK for validating banking data — built for Latin America, ready for the world.**

[![PyPI version](https://badge.fury.io/py/bankkit.svg)](https://badge.fury.io/py/bankkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

BankKit validates banking identifiers, account numbers, and financial keys across Latin America and international standards — no API calls, no dependencies, just fast and reliable validation.

---

## Why BankKit?

Most validation libraries are built for Europe. BankKit was built with **Latin America first** — covering Brazil, Mexico, Argentina, and Chile — while also supporting global standards like IBAN, SWIFT, and card numbers.

---

## Installation

```bash
pip install bankkit
```

---

## Quick Start

```python
from bankkit import BankKit

bk = BankKit()

# Validate a PIX key
bk.validate_pix("11122233344")
# → {"valid": True, "type": "CPF"}

# Validate an IBAN
bk.validate_iban("GB82WEST12345698765432")
# → {"valid": True, "country": "GB", "bank": "West Bank"}

# Validate a credit card
bk.validate_card("4111111111111111")
# → {"valid": True, "brand": "Visa", "type": "credit"}
```

---

## Features

| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_iban(iban)` | IBAN format + checksum | ISO 13616 |
| `validate_swift(swift)` | SWIFT/BIC format | ISO 9362 |
| `validate_card(number)` | Card number + brand detection | ISO 7812 / Luhn |
| `validate_bin(bin)` | BIN + issuing bank | ISO 7812 |
| `validate_pix(key)` | PIX key by type | BACEN |
| `validate_cpf(cpf)` | CPF check digit | Receita Federal |
| `validate_cnpj(cnpj)` | CNPJ check digit | Receita Federal |
| `validate_br_account(agency, account, code?)` | Brazilian bank account | BACEN / COMPE |
| `validate_clabe(clabe)` | Mexican CLABE | BANXICO |
| `validate_cbu(cbu)` | Argentine CBU/CVU | BCRA |
| `validate_routing(number)` | US Routing Number (ABA) | ABA |

---

## Usage Examples

### Brazil

```python
# PIX key — auto-detects type
bk.validate_pix("11122233344")
# → {"valid": True, "type": "CPF"}

bk.validate_pix("user@email.com")
# → {"valid": True, "type": "email"}

# CPF
bk.validate_cpf("111.222.333-96")
# → {"valid": True}

# CNPJ
bk.validate_cnpj("11.222.333/0001-81")
# → {"valid": True}

# Bank account — optional bank code enriches the response
bk.validate_br_account("0001", "12345-6", code="077")
# → {"valid": True, "bank": "Banco Inter"}
```

### Latin America

```python
# Mexico — CLABE
bk.validate_clabe("032180000118359719")
# → {"valid": True, "bank": "IXE Banco"}

# Argentina — CBU
bk.validate_cbu("0720599520000005783690")
# → {"valid": True, "bank": "Santander Argentina"}
```

### International

```python
# IBAN
bk.validate_iban("GB82WEST12345698765432")
# → {"valid": True, "country": "GB", "bank": "West Bank"}

# SWIFT/BIC
bk.validate_swift("BRASBRRJXXX")
# → {"valid": True, "country": "BR", "institution": "Banco do Brasil"}

# Card number
bk.validate_card("4111111111111111")
# → {"valid": True, "brand": "Visa", "type": "credit"}

# BIN lookup
bk.validate_bin("411111")
# → {"valid": True, "brand": "Visa", "bank": "Itaú", "country": "BR"}

# US Routing Number
bk.validate_routing("021000021")
# → {"valid": True, "bank": "JPMorgan Chase", "state": "NY"}
```

### Accessing specific fields

```python
result = bk.validate_iban("GB82WEST12345698765432")
result["bank"]     # → "West Bank"
result["country"]  # → "GB"
result["valid"]    # → True
```

---

## Response Format

Every function returns a consistent dict:

```python
{
  "valid": bool,        # always present
  "error": str | None,  # present when valid is False
  # + additional fields depending on the validator
}
```

---

## Standards & References

BankKit follows official specifications:

- **IBAN** → [ISO 13616](https://www.swift.com/standards/data-standards/iban)
- **SWIFT/BIC** → [ISO 9362](https://www.iso.org/standard/60390.html)
- **Card Numbers** → [ISO 7812](https://www.iso.org/standard/70484.html) + Luhn Algorithm
- **PIX / COMPE / ISPB** → [BACEN](https://www.bcb.gov.br)
- **CLABE** → [BANXICO](https://www.banxico.org.mx)
- **CBU/CVU** → [BCRA](https://www.bcra.gob.ar)

---

## Contributing

Contributions are welcome — especially for expanding Latin American bank data.

1. Fork the repository
2. Create your branch (`git checkout -b feature/add-colombia`)
3. Commit your changes
4. Open a Pull Request

Looking for a good first issue? Check issues labeled [`good first issue`](../../issues?q=label%3A%22good+first+issue%22).

---

## License

MIT © [Your Name](https://github.com/otaviovicario)