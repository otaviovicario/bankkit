# 🏦 BankKit

> **Python SDK for validating banking data — built for Latin America, ready for the world.**

[![PyPI version](https://badge.fury.io/py/bankkit.svg)](https://badge.fury.io/py/bankkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-131%20passing-brightgreen.svg)]()

BankKit validates banking identifiers, account numbers, documents, and financial keys across Latin America and international standards — no API calls, no dependencies, just fast and reliable validation.

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
# → {"valid": True, "type": "CPF", "error": None}

# Validate an IBAN
bk.validate_iban("GB82WEST12345698765432")
# → {"valid": True, "country": "United Kingdom", "code": "GB", "error": None}

# Validate a passport
bk.validate_passport("AB123456", "BR")
# → {"valid": True, "country": "BR", "format": "2 letters + 6 digits", "error": None}
```

---

## Features

### 🇧🇷 Brazil
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_cpf(cpf)` | CPF check digit | Receita Federal |
| `validate_cnpj(cnpj)` | CNPJ check digit | Receita Federal |
| `validate_pix(key)` | PIX key by type (CPF, CNPJ, email, phone, UUID) | BACEN |
| `validate_br_account(agency, account, code?)` | Bank account + optional bank lookup | BACEN / COMPE |

### 🇦🇷 Argentina
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_cbu(cbu)` | CBU/CVU (22 digits, dual block check) | BCRA |

### 🇲🇽 Mexico
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_clabe(clabe)` | CLABE (18 digits, weighted check digit) | BANXICO |

### 🇨🇱 Chile
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_rut(rut)` | RUT — accepts formats like "12.345.678-5" or "K" | SII |

### 🇺🇸 United States
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_routing(routing)` | ABA Routing Number + Federal Reserve district | ABA |

### 🇨🇦 Canada
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_ca_routing(routing)` | Routing number (transit + institution) | Payments Canada |
| `validate_ca_account(account)` | Account number format | Payments Canada |

### 🌍 International
| Function | What it validates | Standard |
|----------|-------------------|----------|
| `validate_iban(iban)` | IBAN format + MOD 97 checksum (80+ countries) | ISO 13616 |
| `validate_swift(swift)` | SWIFT/BIC format + country code | ISO 9362 |
| `validate_card(number)` | Card number + brand detection (Luhn) | ISO 7812 |
| `validate_bin(bin)` | BIN (first 6 digits) + brand detection | ISO 7812 |
| `validate_passport(number, country)` | Passport format by country (30+ countries) | ICAO 9303 |

---

## Usage Examples

### Brazil

```python
# CPF
bk.validate_cpf("111.444.777-35")
# → {"valid": True, "error": None}

# CNPJ
bk.validate_cnpj("11.222.333/0001-81")
# → {"valid": True, "error": None}

# PIX — auto-detects key type
bk.validate_pix("user@email.com")
# → {"valid": True, "type": "EMAIL", "error": None}

bk.validate_pix("+5511999999999")
# → {"valid": True, "type": "PHONE", "error": None}

# Bank account with optional bank code
bk.validate_br_account("0001", "123456", code="341")
# → {"valid": True, "bank": "Itaú Unibanco", "error": None}
```

### Latin America

```python
# Argentina — CBU
bk.validate_cbu("0720599600000057836902")
# → {"valid": True, "bank": None, "error": None}

# Mexico — CLABE
bk.validate_clabe("032180000118359719")
# → {"valid": True, "bank_code": "032", "bank": "IXE Banco", "error": None}

# Chile — RUT
bk.validate_rut("76.354.771-K")
# → {"valid": True, "error": None}
```

### North America

```python
# USA — ABA Routing Number
bk.validate_routing("021000021")
# → {"valid": True, "district": "New York", "error": None}

# Canada — Routing Number
bk.validate_ca_routing("000011001")
# → {"valid": True, "institution": "001", "bank": "Bank of Montreal (BMO)", "error": None}

# Canada — Account
bk.validate_ca_account("12345678")
# → {"valid": True, "error": None}
```

### International

```python
# IBAN
bk.validate_iban("GB82WEST12345698765432")
# → {"valid": True, "country": "United Kingdom", "code": "GB", "error": None}

# SWIFT/BIC
bk.validate_swift("BRASBRRJXXX")
# → {"valid": True, "bank_code": "BRAS", "country": "BR", "error": None}

# Card number
bk.validate_card("4111111111111111")
# → {"valid": True, "brand": "Visa", "error": None}

# BIN
bk.validate_bin("636368")
# → {"valid": True, "brand": "Elo", "error": None}

# Passport
bk.validate_passport("AB123456", "BR")
# → {"valid": True, "country": "BR", "format": "2 letters + 6 digits", "error": None}

bk.validate_passport("A12345678", "US")
# → {"valid": True, "country": "US", "format": "1 letter + 8 digits", "error": None}
```

### Accessing specific fields

```python
result = bk.validate_iban("GB82WEST12345698765432")
result["country"]  # → "United Kingdom"
result["code"]     # → "GB"
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
- **Passport** → [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303)
- **PIX / COMPE / ISPB** → [BACEN](https://www.bcb.gov.br)
- **CLABE** → [BANXICO](https://www.banxico.org.mx)
- **CBU/CVU** → [BCRA](https://www.bcra.gob.ar)
- **RUT** → [SII Chile](https://www.sii.cl)
- **ABA Routing** → [ABA](https://www.aba.com)
- **CA Routing** → [Payments Canada](https://www.payments.ca)

---

## Contributing

Contributions are welcome — especially for expanding country coverage and bank data.

1. Fork the repository
2. Create your branch (`git checkout -b feat/add-colombia`)
3. Add your validator in the correct folder (`validators/latam/validator_co.py`)
4. Add tests (`tests/latam/test_co.py`)
5. Open a Pull Request

Looking for ideas? Check issues labeled [`good first issue`](../../issues?q=label%3A%22good+first+issue%22).

---

## License

MIT © [Otavio Vicario Muraca](https://github.com/otaviovicario)