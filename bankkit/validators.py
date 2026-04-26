def validate_br_account(agency: str, account: str) -> bool:
    """
    Validates a Brazilian bank account number.

    Args:
        agency (str): The bank agency number.
        account (str): The bank account number.

    Returns:
        bool: True if the account number is valid, False otherwise.
    """
    # Implement validation logic here

    agency = agency.strip()
    account = account.strip()

    if not agency.isdigit() or len(agency) != 4:
        return {"valid": False, "message": "Invalid agency number. It should be 4 digits."}

    if not account.isdigit() or len(account) < 5 or len(account) > 12:
        return {"valid": False, "message": "Invalid account number. It should be between 5 and 12 digits."}

    return {"valid": True, "message": "Valid account number for Brazilian banks."}
